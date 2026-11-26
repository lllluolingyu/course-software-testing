import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const teamDir = fileURLToPath(new URL('.', import.meta.url));
const port = Number(process.env.TEAM04_PORT ?? 3104);
if (!Number.isInteger(port) || port < 1024 || port > 65535) {
  throw new Error('TEAM04_PORT must be an integer between 1024 and 65535');
}
const baseURL = `http://127.0.0.1:${port}`;

export default defineConfig({
  testDir: teamDir,
  testMatch: 'faults.spec.ts',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 45_000,
  expect: { timeout: 4_000 },
  outputDir: 'output/playwright/test-results',
  reporter: [
    ['list'],
    ['json', { outputFile: 'output/playwright/results.json' }],
    ['html', { outputFolder: 'output/playwright/report', open: 'never' }],
  ],
  use: {
    baseURL,
    browserName: 'chromium',
    viewport: { width: 1440, height: 1000 },
    locale: 'en-US',
    timezoneId: 'UTC',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  // The application seeds its own prerequisites. No SQL or session injection.
  // A separate in-memory database prevents changes to the user's existing site.
  webServer: {
    command: 'node ../../backend/dist/server.js',
    cwd: teamDir,
    url: `${baseURL}/api/health`,
    env: { HOST: '127.0.0.1', PORT: String(port), DATABASE_URL: ':memory:' },
    reuseExistingServer: false,
    timeout: 30_000,
    gracefulShutdown: { signal: 'SIGTERM', timeout: 5_000 },
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
