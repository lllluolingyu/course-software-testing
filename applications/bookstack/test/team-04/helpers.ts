import { expect, type Locator, type Page, type TestInfo } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';

export const uniqueName = (label: string) => `T04-${label}-${randomUUID().slice(0, 8)}`;
export const button = (page: Page, name: string) => page.getByRole('button', { name, exact: true });
export const region = (page: Page, name: string) => page.getByRole('region', { name, exact: true });
export const entry = (scope: Page | Locator, name: string) =>
  scope.getByRole('button', { name, exact: true }).or(scope.getByRole('link', { name, exact: true }));

export async function begin(page: Page) {
  await page.goto('/');
  await expect(page.getByRole('link', { name: 'Login', exact: true })).toBeVisible();
}

export async function login(page: Page) {
  await page.getByRole('link', { name: 'Login', exact: true }).click();
  // Public course fixture, identical to baseline/helpers.ts; not a personal account.
  await page.getByLabel('Email', { exact: true }).fill('bookstack_user@example.com');
  await page.getByLabel('Password', { exact: true }).fill('Password123!');
  await button(page, 'Login').click();
  await expect(region(page, 'My Recent Drafts')).toBeVisible();
}

export async function home(page: Page) {
  await page.getByRole('link', { name: 'BookStack Demo', exact: true }).click();
  await expect(region(page, 'Recently Updated Pages')).toBeVisible();
}

export async function metadata(page: Page, name: string) {
  await page.getByLabel('Name', { exact: true }).fill(name);
  await page.getByLabel('Description', { exact: true }).fill('Team 04 isolated test fixture');
  await page.getByLabel('Tags', { exact: true }).fill('team04');
}

export async function beginBook(page: Page) {
  await page.getByRole('link', { name: 'Books', exact: true }).click();
  await button(page, 'Create New Book').click();
  await expect(page.getByRole('heading', { name: 'Create New Book', exact: true })).toBeVisible();
}

export async function createBook(page: Page, name: string) {
  await beginBook(page);
  await metadata(page, name);
  await button(page, 'Save Book').click();
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible();
}

export async function openBootstrap(page: Page) {
  await page.getByRole('link', { name: 'Shelves', exact: true }).click();
  await entry(region(page, 'Shelf list'), 'Benchmark Bootstrap Shelf').click();
  await expect(page.getByRole('heading', { name: 'Benchmark Bootstrap Shelf', exact: true })).toBeVisible();
}

export async function createShelf(page: Page, name: string) {
  await openBootstrap(page);
  await button(page, 'New Shelf').click();
  await metadata(page, name);
  await button(page, 'Save Shelf').click();
  await entry(region(page, 'Shelf list'), name).click();
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible();
}

export async function visibleCount(locator: Locator): Promise<number> {
  let count = 0;
  for (const candidate of await locator.all()) if (await candidate.isVisible()) count++;
  return count;
}

// Capture evidence before the expected-behavior assertion fails. DOM inspection is
// read-only; all account and content setup above uses the normal GUI.
export async function evidence(page: Page, info: TestInfo, id: string, details: Record<string, unknown>) {
  const screenshot = info.outputPath(`${id}.png`);
  const observation = info.outputPath(`${id}.json`);
  await page.screenshot({ path: screenshot, fullPage: true });
  const controls = await page.locator('main').evaluateAll(nodes => nodes.flatMap(main =>
    Array.from(main.querySelectorAll('input, textarea, select, button, a')).map(el => ({
      tag: el.tagName.toLowerCase(),
      type: el.getAttribute('type'),
      label: el.getAttribute('aria-label') ?? el.textContent?.trim() ?? '',
      id: el.id,
    }))));
  await writeFile(observation, JSON.stringify({
    id, url: page.url(), time: new Date().toISOString(), ...details, controls,
    visibleText: await page.locator('main').innerText(),
  }, null, 2));
  await info.attach(`${id} screenshot`, { path: screenshot, contentType: 'image/png' });
  await info.attach(`${id} observations`, { path: observation, contentType: 'application/json' });
}
