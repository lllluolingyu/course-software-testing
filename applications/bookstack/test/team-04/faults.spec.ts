import { test, expect } from '@playwright/test';
import { begin, beginBook, button, createBook, createShelf, entry, evidence, home, login,
  metadata, openBootstrap, region, uniqueName, visibleCount } from './helpers.js';

test.beforeEach(async ({ page }) => { await begin(page); });

test('F01 REQ-4.5 existing books can be associated with a shelf', async ({ page }, info) => {
  const book = uniqueName('F01-Book');
  const shelf = uniqueName('F01-Shelf');
  await createBook(page, book);
  await createShelf(page, shelf);
  await button(page, 'Edit').click();
  await expect(page.getByLabel('Name', { exact: true })).toHaveValue(shelf);
  const main = page.locator('main');
  // Accept several control forms; do not require reference-image drag and drop.
  const association = main.getByRole('button', { name: /(?:add|select|manage|attach|associate).*books?/i })
    .or(main.getByRole('link', { name: /(?:add|select|manage|attach|associate).*books?/i }))
    .or(main.getByLabel(/(?:available|related|associated|shelf).*books?|books? on this shelf/i))
    .or(main.getByText(/^(?:books|books on this shelf|available books|related books)$/i))
    .or(main.getByText(book, { exact: true }));
  const observed = await visibleCount(association);
  await evidence(page, info, 'F01', { book, shelf, associationControls: observed });
  expect(observed, 'REQ-4.5: an existing book must be assignable; the entire shelf form has no association UI').toBeGreaterThan(0);
});

test('F02 REQ-5.3 book creation offers optional cover configuration', async ({ page }, info) => {
  await beginBook(page);
  const main = page.locator('main');
  const cover = main.getByLabel(/cover|cover image/i)
    .or(main.getByRole('button', { name: /cover|(?:select|upload|choose).*image/i }))
    .or(main.getByRole('link', { name: /cover|(?:select|upload|choose).*image/i }));
  const observed = await visibleCount(cover);
  const fileInputs = await main.locator('input[type="file"]').count();
  await evidence(page, info, 'F02', { coverControls: observed, fileInputs });
  expect(observed + fileInputs, 'REQ-5.3: optional cover means a user may set one; no cover or upload control exists').toBeGreaterThan(0);
});

test('F03 REQ-5.3 book creation offers a default page template', async ({ page }, info) => {
  await beginBook(page);
  const main = page.locator('main');
  const template = main.getByLabel(/template/i)
    .or(main.getByRole('button', { name: /template/i }))
    .or(main.getByRole('link', { name: /template/i }))
    .or(main.getByText(/default page template|select a template/i));
  const observed = await visibleCount(template);
  await evidence(page, info, 'F03', { templateControls: observed });
  expect(observed, 'REQ-5.3: default page template selection is absent, not merely an empty template catalogue').toBeGreaterThan(0);
});

test('F04 REQ-3.1 authenticated dashboard includes Recent Activity', async ({ page }, info) => {
  await login(page);
  const book = uniqueName('F04-Book');
  await createBook(page, book);
  await home(page);
  await page.reload();
  for (const name of ['My Recent Drafts', 'My Recently Viewed', 'My Most Viewed Favorites', 'Recently Updated Pages']) {
    await expect(region(page, name)).toBeVisible();
  }
  const activity = page.locator('main').getByText('Recent Activity', { exact: true })
    .or(region(page, 'Recent Activity'));
  const observed = await visibleCount(activity);
  await evidence(page, info, 'F04', { book, recentActivityElements: observed });
  expect(observed, 'REQ-3.1 and index_after_login.png require a Recent Activity section; all four baseline panels exist but this section does not').toBeGreaterThan(0);
});

test('F05 REQ-3.1 authenticated dashboard exposes its referenced controls', async ({ page }, info) => {
  await login(page);
  await page.reload();
  await expect(region(page, 'My Recent Drafts')).toBeVisible();
  const names = [/toggle details/i, /dark mode|light mode/i];
  const counts: number[] = [];
  for (const name of names) {
    const control = page.getByRole('button', { name }).or(page.getByRole('link', { name }))
      .or(page.getByRole('switch', { name })).or(page.getByRole('checkbox', { name }));
    counts.push(await visibleCount(control));
  }
  await evidence(page, info, 'F05', { toggleDetailsControls: counts[0], themeControls: counts[1] });
  // One case for the omitted dashboard controls, not one bug per missing button.
  expect.soft(counts[0], 'REQ-3.1 reference: Toggle Details control is missing').toBeGreaterThan(0);
  expect.soft(counts[1], 'REQ-3.1 reference: Dark Mode control is missing').toBeGreaterThan(0);
});

test('F06 REQ-4.3 immutable bootstrap shelf rejects adding a book', async ({ page }, info) => {
  await openBootstrap(page);
  await expect(button(page, 'Edit')).toHaveCount(0);
  await expect(button(page, 'Delete')).toHaveCount(0);
  const book = uniqueName('F06-BootstrapBook');
  await expect(entry(region(page, 'Book list'), book)).toHaveCount(0);
  if (await button(page, 'Create New Book').count() === 0) return;
  await button(page, 'Create New Book').click();
  await metadata(page, book);
  // Observe the real UI request. No direct API creation or private-storage setup.
  const saved = page.waitForResponse(r => r.request().method() === 'POST' && /\/api\/shelves\/\d+\/books$/.test(r.url()));
  await button(page, 'Save Book').click();
  const response = await saved;
  if (response.ok()) {
    await expect(page.getByRole('heading', { name: book, exact: true })).toBeVisible();
    await entry(page, 'Benchmark Bootstrap Shelf').click();
  } else {
    await openBootstrap(page);
  }
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Benchmark Bootstrap Shelf', exact: true })).toBeVisible();
  const observed = await entry(region(page, 'Book list'), book).count();
  await evidence(page, info, 'F06', { book, saveStatus: response.status(), entriesAfterReload: observed });
  await expect(entry(region(page, 'Book list'), book),
    'REQ-4.3: the immutable bootstrap shelf must remain unchanged; Create New Book bypasses that protection').toHaveCount(0);
});
