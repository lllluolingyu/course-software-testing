# WB-06 · Create New Book mutates the immutable bootstrap shelf

**Method and requirement.** White-box guard-consistency test under REQ-4, REQ-4.3 and REQ-5.6. Both `PUT /api/shelves/:id` and `DELETE /api/shelves/:id` guard `if (row.is_bootstrap)` with HTTP 403 (`"The bootstrap shelf cannot be changed"` / `"cannot be deleted"`), and `ShelfDetailPage` hides **Edit** and **Delete** when `shelf.isBootstrap` is true. However, `ShelfDetailPage` leaves **Create New Book** enabled unconditionally, and neither `POST /api/shelves/:id/books` nor `POST /api/books` checks `is_bootstrap`. Exercise that unguarded path directly on `Benchmark Bootstrap Shelf`. [Requirements](../../requirements/requirements.yaml) · [Frontend shelf actions](../../frontend/src/slices/bookstack.tsx#L266) · [Guarded PUT/DELETE vs unguarded book POST](../../backend/src/slices/bookstack.ts#L281) · [Shelf book creation route](../../backend/src/slices/bookstack.ts#L301)

**New coverage.** `REQ-5.6.spec.ts` creates a user shelf first and adds a book only to that user-created shelf. `WB-04` tests `POST /api/shelves` colliding with the bootstrap shelf's metadata. Neither tests mutating `Benchmark Bootstrap Shelf`'s `books` collection via **Create New Book**. [Shelf-book baseline](../baseline/REQ-5.6.spec.ts) · [Shelf seed collision](white-box-04.md)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Open **Shelves → Benchmark Bootstrap Shelf**.
2. Confirm its **Book list** displays `No books on this shelf yet` and that **Edit** and **Delete** are absent from **Actions**.
3. Click **Create New Book** in `Benchmark Bootstrap Shelf`'s **Actions** sidebar, enter `Intruder volume` in **Name** and `Added directly to bootstrap shelf` in **Description**, and click **Save Book**.
4. On the opened book details, activate the **Benchmark Bootstrap Shelf** parent button and reload the shelf page.

**Expected.** REQ-4 specifies *"One immutable bootstrap shelf"* and REQ-4.3 states *"The existing Benchmark Bootstrap Shelf has description Entry shelf for the New Shelf creation action., no tags and no books. It remains an immutable entry shelf for New Shelf."* Creating books inside the bootstrap shelf should be disallowed (either by omitting **Create New Book** on the bootstrap shelf or rejecting the mutation like `PUT` and `DELETE`) so its **Book list** stays empty.

**Observed.** **Create New Book** was exposed on `Benchmark Bootstrap Shelf`, `POST /api/shelves/1/books` succeeded with HTTP 200, and reloading `Benchmark Bootstrap Shelf` displayed `Intruder volume` in its **Book list** while **Edit** and **Delete** remained hidden. [Mutated bootstrap shelf after reload](assets/bootstrap-mutated.png) · [Automated check](README.md#automated-workflow-checks)
