# BB-02 · Choose a default page template for a book

**Method and requirement.** Black-box feature test under REQ-5.3, with an edit-form cross-check under REQ-5.4. The book metadata includes a default page template. The reference shows its own expandable selection section. The test asks whether selection can be started and makes no assumption about catalog entries. [Requirements](../../requirements/requirements.yaml) · [Reference creation form](../../requirements/reference/create_book.png) · [Reference edit form](../../requirements/reference/edit_book.png)

**New coverage.** The baseline creates and edits books using Name, Description and Tags. It never attempts template selection. [Create baseline](../baseline/REQ-5.3.spec.ts) · [Edit baseline](../baseline/REQ-5.4.spec.ts)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create a book named `Field handbook`.
2. On the book, choose **New Page**, enter `Packing list` and body `Pack a map.`, then **Save Page**. Confirm the book's Page list contains the page.
3. Open **Edit** on the book and inspect the complete metadata form for a way to choose or change its default page template.
4. Click **Cancel**, open **Books → Create New Book**, and enter `Expedition handbook`. Try to open the default-template selection on this form too.

**Expected.** Creation offers a way to select a default template, as pictured in the reference. The test does not require the ordinary page created in step 2 to be an eligible template.

**Observed.** Both book forms exposed only Name, Description, Tags, Cancel and Save Book. Neither offered a template setting or picker. [Creation form](assets/template-create.png) · [Edit form](assets/template-edit.png)
