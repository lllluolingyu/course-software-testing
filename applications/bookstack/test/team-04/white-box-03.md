# REQ-4.5 Test: Add an existing book when editing a shelf (WB-03)

## Description

Shelf Edit changes a shelf’s text metadata but offers no way to add an existing book to it.

## Requirement: Expected Output

Under REQ-4 and REQ-4.5, editing related books must allow the user to add `Unassigned atlas` while retaining `Resident handbook`. Both books should appear after saving. [Course requirement](../../requirements/requirements.yaml#L301)

## Test description

**Manual browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create `Unassigned atlas` from the global Books list.
2. Open **Shelves → Benchmark Bootstrap Shelf → New Shelf**. Name it `Field library` and save. In the returned Shelf list, open **Field library**.
3. On that shelf choose **Create New Book**. Save `Resident handbook` and follow the **Field library** parent action. Check that the shelf's Book list contains **Resident handbook**.
4. Click **Edit** on the shelf. Try to add **Unassigned atlas** (or inspect whether **Resident handbook** can be managed) while updating Description to `Field guides` as a control, then click **Save Shelf** and reload.

## Observed Output

The editor offered Name, Description, and Tags as its only fields. The description change persisted. The shelf still listed only `Resident handbook`. [Editor](assets/shelf-edit.png) · [Shelf after save and reload](assets/shelf-after.png)

## Test design and baseline coverage

White-box data-flow test. A book stores its shelf membership in its shelf ID. The shelf and book edit forms submit text metadata, and their update handlers leave that membership untouched. Preparing one resident book and one unassigned book makes the missing edit observable. [Book schema](../../backend/src/foundation/schema.ts#L30) · [Shelf form](../../frontend/src/slices/bookstack.tsx#L282) · [Shelf update](../../backend/src/slices/bookstack.ts#L286) · [Book update](../../backend/src/slices/bookstack.ts#L340) · [Reference shelf editor](../../requirements/reference/edit_shelve.png)

The shelf edit baseline changes text metadata only. The shelf-book baseline creates a brand-new book inside a shelf (`POST /api/shelves/:id/books`). Neither tests editing a shelf's related-book membership after creation. [Shelf edit baseline](../baseline/REQ-4.5.spec.ts) · [Shelf-book baseline](../baseline/REQ-5.6.spec.ts)
