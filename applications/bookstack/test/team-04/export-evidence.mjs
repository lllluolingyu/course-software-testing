import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = fileURLToPath(new URL('.', import.meta.url));
const run = process.argv[2];
if (!/^run-\d+$/.test(run ?? '')) throw new Error('Usage: node export-evidence.mjs run-1');
const report = JSON.parse(await readFile(resolve(root, 'output/playwright/results.json'), 'utf8'));
const cases = [];
function visit(suites) {
  for (const suite of suites) {
    for (const spec of suite.specs ?? []) {
      for (const test of spec.tests) {
        for (const result of test.results) cases.push({ title: spec.title, result });
      }
    }
    visit(suite.suites ?? []);
  }
}
visit(report.suites);
if (cases.length !== 6) throw new Error(`Expected six completed cases, received ${cases.length}`);
const destination = resolve(root, 'assets', run);
await mkdir(destination, { recursive: true });
const exported = [];
for (const { title, result } of cases) {
  const id = title.match(/^F0[1-6]\b/)?.[0];
  if (!id || result.status !== 'failed' || !result.errors?.every(e => e.message.startsWith('Error: REQ-'))) {
    throw new Error(`Not a requirement assertion failure: ${title}`);
  }
  const errors = result.errors.map(e => e.message.replace(/\u001b\[[0-9;]*m/g, ''));
  for (const [kind, ext] of [['screenshot', 'png'], ['observations', 'json']]) {
    const attachment = result.attachments.find(a => a.name === `${id} ${kind}`);
    if (!attachment?.path) throw new Error(`Missing ${id} ${kind}`);
    const source = resolve(attachment.path);
    if (relative(root, source).startsWith(`..${sep}`)) throw new Error('Unexpected evidence path');
    await copyFile(source, resolve(destination, `${id}.${ext}`));
  }
  exported.push({ id, title, status: result.status, durationMs: result.duration, errors,
    screenshot: `${id}.png`, observations: `${id}.json` });
}
const hashFiles = ['faults.spec.ts', 'helpers.ts', 'playwright.config.ts', 'package-lock.json'];
const hashes = {};
for (const file of hashFiles) hashes[file] = createHash('sha256').update(await readFile(resolve(root, file))).digest('hex');
await writeFile(resolve(destination, 'results.json'), JSON.stringify({
  sourceCommit: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
  node: process.version,
  playwright: JSON.parse(await readFile(resolve(root, 'node_modules/@playwright/test/package.json'), 'utf8')).version,
  browser: 'Playwright Chromium (headless)',
  command: 'npm test', exitCode: 1,
  startTime: report.stats.startTime, durationMs: report.stats.duration,
  appState: 'Fresh application-seeded in-memory database; all scenario data created through the GUI',
  oracle: 'Course requirements.yaml and supplied reference images; independent live reference system not exercised',
  hashes, cases: exported,
}, null, 2) + '\n');
console.log(`Exported six requirement failures and evidence to assets/${run}/`);
