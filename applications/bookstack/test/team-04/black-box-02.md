# REQ-5.3 Test: Choose a default page template for a book (BB-02)

## Description

The default page template setting is missing from both the book creation and edit forms.

## Requirement: Expected Output

REQ-5.3 allows a default page template to be chosen, and REQ-5.4 covers the selected template during editing. The reference forms show the setting. [Course requirement](../../requirements/requirements.yaml#L480)

## Test description

**Manual browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create a book named `Field handbook`.
2. On the book, choose **New Page**, enter `Packing list` and body `Pack a map.`, then **Save Page**. Confirm the book's Page list contains the page.
3. Open **Edit** on the book and inspect the complete metadata form for a way to choose or change its default page template.
4. Click **Cancel**, open **Books → Create New Book**, and enter `Expedition handbook`. Try to open the default-template selection on this form too.

## Observed Output

Both forms offered only Name, Description, and Tags as metadata fields. Neither had a template setting or a way to open a selector. [Creation form](assets/template-create.png) · [Edit form](assets/template-edit.png)

## Test design and baseline coverage

Black-box feature test under REQ-5.3, with an edit-form cross-check under REQ-5.4. The book metadata includes a default page template. The reference shows its own expandable selection section. The test asks whether selection can be started and makes no assumption about catalog entries. [Requirements](../../requirements/requirements.yaml) · [Reference creation form](../../requirements/reference/create_book.png) · [Reference edit form](../../requirements/reference/edit_book.png)

The baseline creates and edits books using Name, Description and Tags. It never attempts template selection. [Create baseline](../baseline/REQ-5.3.spec.ts) · [Edit baseline](../baseline/REQ-5.4.spec.ts)
