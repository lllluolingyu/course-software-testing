# WB-07 · Publishing identical pages drops the second page when logged out but creates it when signed in

**Method and requirement.** White-box SQL-predicate test under REQ-6.1 and REQ-2. In `createPage`, the pre-insert lookup checks `((author_id IS NULL AND ? IS NULL) OR author_id = ?)` using `draft ? user!.id : null` (`bookstack.ts:127-133`), which always binds `null` when `draft` is `false`. Yet the `INSERT` statement on line 137 binds `draft ? user!.id : user?.id ?? null`, storing `null` for anonymous publishers and `user.id` for signed-in publishers. Compare two identical published pages while logged out (`author_id IS NULL`, matching `existing` and skipping `INSERT`) against the exact same two saves while signed in (`author_id = 1`, missing `existing` and inserting a new row). [Requirements](../../requirements/requirements.yaml) · [Lookup vs insert parameter mismatch](../../backend/src/slices/bookstack.ts#L127)

**New coverage.** `REQ-6.1.spec.ts` publishes one uniquely named page while logged out and saves one draft while signed in. `WB-04` tests shelf creation against the bootstrap seed. Neither exercises `createPage`'s `author_id` mismatch between anonymous and authenticated `Save Page` submissions. [Page baseline](../baseline/REQ-6.1.spec.ts) · [Shelf seed collision](white-box-04.md)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create book `Anonymous log`.
2. Click **New Page**, enter title `Shift report` and body `All clear.`, and click **Save Page**. Repeat **New Page → `Shift report` / `All clear.` → Save Page** a second time on `Anonymous log`. Count the entries in **Page list** and inspect both `POST /api/books/:id/pages` responses.
3. Click **Login**, sign in as `bookstack_user@example.com` / `Password123!`, and create book `Signed-in log`.
4. Repeat step 2 identically twice on `Signed-in log`. Count the entries in **Page list** and compare the `POST` responses with step 2.

**Expected.** REQ-2 keeps content mutations consistent while logged out, and REQ-6.1 states that **Save Page** *"publishes the entered title and body, returns to the book, and adds exactly one entry to `Page list`, including while logged out. REQ-2.2 is required only for the Save Draft branch."* Each successful **Save Page** should behave consistently across login states and add a newly created page entry.

**Observed.** While logged out, both saves on `Anonymous log` returned HTTP 200 with the same page `id: 1`, silently dropping the second creation and leaving **1** `Shift report` entry in **Page list**. While signed in, the identical two saves on `Signed-in log` returned distinct IDs (`2` and `3`) and left **2** `Shift report` entries in **Page list**. [Logged-out Page list](assets/page-publish-anon.png) · [Signed-in Page list](assets/page-publish-auth.png) · [Recorded responses and counts](assets/page-publish-comparison.json) · [Automated check](README.md#automated-workflow-checks)
