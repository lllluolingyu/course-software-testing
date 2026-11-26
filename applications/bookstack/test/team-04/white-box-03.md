# WB-03 · An existing book cannot be added to a shelf through Edit

**Method and requirement.** White-box data-flow test under REQ-4 and REQ-4.5. In `schema.ts`, shelf membership is stored in `books.shelf_id`. Tracing all write paths shows `shelf_id` is written only during `INSERT INTO books` (`createBook`), while `ShelfFormPage` holds only `name`, `description` and `tags` state and sends `{ name, description, tags }` to `PUT /api/shelves/:id` (which updates `shelves` without touching `books.shelf_id`), and `BookFormPage` / `PUT /api/books/:id` likewise omit `shelf_id`. Prepare one resident shelf book and one unassigned global book to test whether shelf editing can modify related books as required by REQ-4.5 and pictured in the reference editor. [Requirement](../../requirements/requirements.yaml) · [Reference editor](../../requirements/reference/edit_shelve.png) · [Schema column](../../backend/src/foundation/schema.ts#L30) · [Shelf form state](../../frontend/src/slices/bookstack.tsx#L282) · [Shelf PUT handler](../../backend/src/slices/bookstack.ts#L286) · [Book PUT handler](../../backend/src/slices/bookstack.ts#L340)

**New coverage.** The shelf edit baseline changes text metadata only. The shelf-book baseline creates a brand-new book inside a shelf (`POST /api/shelves/:id/books`). Neither tests editing a shelf's related-book membership after creation. [Shelf edit baseline](../baseline/REQ-4.5.spec.ts) · [Shelf-book baseline](../baseline/REQ-5.6.spec.ts)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create `Unassigned atlas` from the global Books list.
2. Open **Shelves → Benchmark Bootstrap Shelf → New Shelf**. Name it `Field library` and save. In the returned Shelf list, open **Field library**.
3. On that shelf choose **Create New Book**. Save `Resident handbook` and follow the **Field library** parent action. Check that the shelf's Book list contains **Resident handbook**.
4. Click **Edit** on the shelf. Try to add **Unassigned atlas** (or inspect whether **Resident handbook** can be managed) while updating Description to `Field guides` as a control, then click **Save Shelf** and reload.

**Expected.** Shelf Edit exposes related-book selection so **Unassigned atlas** can be added while retaining **Resident handbook**, after which the shelf's Book list contains both books.

**Observed.** Because neither `ShelfFormPage` nor `PUT /api/shelves/:id` handles `books.shelf_id`, the editor rendered only Name, Description, Tags, Cancel and Save Shelf, offering no control to add `Unassigned atlas` or remove `Resident handbook`. Only the description change persisted across reload. [Editor](assets/shelf-edit.png) · [Shelf after save and reload](assets/shelf-after.png)
