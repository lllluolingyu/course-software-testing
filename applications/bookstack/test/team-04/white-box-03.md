# WB-03 · An existing book cannot be added to a shelf through Edit

**Method and requirement.** White-box test under REQ-4.5. In edit mode, `ShelfFormPage` loads Name, Description and Tags. Its submit path sends those three values to the shelf update handler. Select one existing member and one available nonmember to exercise a change to the shelf's books. REQ-4.5 explicitly supports editing related books, and the reference editor shows both sets. [Requirement](../../requirements/requirements.yaml) · [Reference editor](../../requirements/reference/edit_shelve.png) · [Form and update branch](../../frontend/src/slices/bookstack.tsx#L282) · [Server update](../../backend/src/slices/bookstack.ts#L286)

**New coverage.** The shelf edit baseline changes text metadata. The shelf-book baseline creates a new book inside a shelf. Neither adds an already-existing global book through the shelf editor. [Shelf edit baseline](../baseline/REQ-4.5.spec.ts) · [Shelf-book baseline](../baseline/REQ-5.6.spec.ts)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create `Unassigned atlas` from the global Books list.
2. Open **Shelves → Benchmark Bootstrap Shelf → New Shelf**. Name it `Field library` and save. In the returned Shelf list, open **Field library**.
3. On that shelf choose **Create New Book**. Save `Resident handbook` and follow the **Field library** parent action. Check that the shelf's Book list contains **Resident handbook**.
4. Click **Edit** on the shelf. Try to add **Unassigned atlas** while retaining **Resident handbook**. As a control, change the description to `Field guides`, click **Save Shelf** and reload.

**Expected.** The editor allows the available book to be selected. After saving the selection, the shelf's Book list should contain both books.

**Observed.** The editor contained only the three text fields and Save/Cancel actions. It offered no way to select the existing global book. The description change survived reload, and the shelf still contained only Resident handbook. [Editor](assets/shelf-edit.png) · [Shelf after save and reload](assets/shelf-after.png)
