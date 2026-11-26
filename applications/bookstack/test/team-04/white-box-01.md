# WB-01 · Saving a reopened draft overwrites it with another draft's text

**Method and requirement.** White-box test of draft identity across navigation under REQ-6.1 and REQ-1. REQ-6.1 lets the author reopen an owned draft to resume editing or delete it, and REQ-1 requires content metadata to persist across navigation and reload. In `PageViewPage`, two draft routes both render `PageEditor` at the same React tree position without a `key`. `PageEditor` initializes `page`, `title` and `body` via `useState(initial)` and exits its fetch effect early whenever `initial` is truthy (`if (initial || pageId == null) return;`). Direct browser-history traversal between two drafts exercises this branch while updating `pageId`. [Requirements](../../requirements/requirements.yaml) · [Editor state and effect guard](../../frontend/src/slices/bookstack.tsx#L612) · [Delete Draft target](../../frontend/src/slices/bookstack.tsx#L652) · [Draft rendering branch](../../frontend/src/slices/bookstack.tsx#L685)

**New coverage.** The draft baseline creates one draft and checks dashboard membership. The read/edit baseline reopens one published page. Neither checks whether the editor fields and mutation actions agree on the draft identity when navigating between two saved drafts. [Draft baseline](../baseline/REQ-6.1.spec.ts) · [Editor baseline](../baseline/REQ-6.4.spec.ts)

## Reproduce

1. Start a [fresh instance and sign in](README.md#run-manually). Create the book `Field notes`. Choose **New Page**, enter title `North` and body `North observations`, then **Save Draft**. Repeat for `South` with body `South observations`.
2. Open **North** from the book's Page list. Verify its fields and note the draft URL. Click **Back to book** inside the editor and open **South**. Verify its fields and different URL.
3. In Chromium, open the browser Back button's history menu and select the entry **two positions back**, North. This goes from South to North in one navigation (`history.go(-2)`).
4. At North's URL, read both fields. Reload without saving and compare as a control showing what North actually stored on the server.
5. Repeat the traversal from the reloaded North via **Back to book → South → two positions back**. Click **Save Draft** with the displayed fields untouched, reload, then open the parent book's Page list.

| Step | Expected | Observed |
| --- | --- | --- |
| North's URL after the history jump | North / North observations | South / South observations, even after `GET /api/pages/1` returned North |
| Reload North before saving | North / North observations | North / North observations |
| Save at North's URL after the second jump and reload | North keeps its original contents | `PUT /api/pages/1` writes South / South observations into North; the book shows two drafts titled South |

**Expected.** Navigating back to North's URL displays North's saved title and body so that saving updates North with North's own draft content (REQ-6.1, REQ-1).

**Observed.** After `GET /api/pages/1` completed with North's JSON, `PageEditor` still displayed South's fields (and `Delete Draft` still pointed to South's stale `page.id`). Clicking **Save Draft** sent South's fields to `PUT /api/pages/1`, overwriting North (`ID 1`, with South at `ID 2`; IDs may vary across runs). [Navigation and save observations](assets/draft-navigation.tsv) · [Book after saving](assets/draft-after-save.png) · [Automated identity check and run command](README.md#automated-workflow-checks)
