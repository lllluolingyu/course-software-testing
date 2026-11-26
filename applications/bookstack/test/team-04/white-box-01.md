# WB-01 · Saving a reopened draft overwrites it with another draft's text

**Method and requirement.** White-box test of draft identity across navigation. REQ-6.1 lets the author reopen an owned draft and resume its saved work. REQ-1 requires content metadata to persist across navigation and reload. In `PageViewPage`, two draft identities both render `PageEditor` in the same position. Its title and body initialize from `initial`, and the editor's loading effect returns when `initial` is supplied. A direct browser-history traversal between two open drafts exercises this path. [Requirements](../../requirements/requirements.yaml) · [Editor state](../../frontend/src/slices/bookstack.tsx#L612) · [Draft rendering branch](../../frontend/src/slices/bookstack.tsx#L685)

**New coverage.** The draft baseline creates one draft and checks dashboard membership. The read/edit baseline reopens one published page. Neither checks that the editor and save action agree on the identity when navigating between two saved drafts. [Draft baseline](../baseline/REQ-6.1.spec.ts) · [Editor baseline](../baseline/REQ-6.4.spec.ts)

## Reproduce

1. Start a [fresh instance and sign in](README.md#run-manually). Create the book `Field notes`. Choose **New Page**, enter title `North` and body `North observations`, then **Save Draft**. Repeat for `South` with body `South observations`.
2. Open **North** from the book's Page list. Verify its fields and note the draft URL. Click **Back to book** inside the editor and open **South**. Verify its fields and different URL.
3. In Chromium, open the browser Back button's history menu and select the entry **two positions back**, North. This goes from South to North in one navigation. The equivalent browser-history command is `history.go(-2)`.
4. At North's URL, read both fields. Reload without saving and compare. This is a control showing what North actually contained.
5. To verify the effect on these disposable drafts, repeat the traversal from the reloaded North via **Back to book → South → two positions back**. Click **Save Draft** with the displayed fields untouched, reload, then open the parent book's Page list.

| Observation | Expected | Observed |
| --- | --- | --- |
| North's URL after the history jump | North / North observations | South / South observations, even after North's response completed |
| Reload North before saving | North / North observations | North / North observations |
| Save at North's URL after the second jump and reload | North keeps its original contents | North's ID now stores South / South observations. The book shows two drafts titled South. |

The recorded IDs were 1 for North and 2 for South. IDs may differ between instances. [Navigation and save observations](assets/draft-navigation.tsv) · [Book after saving](assets/draft-after-save.png) · [Automated identity check and run command](README.md#automated-workflow-checks)

The automation now includes both `test_history_returns_to_selected_draft` and `test_save_after_history_preserves_selected_draft`. The latter records an editor-identity subtest failure, continues with Save Draft, reloads, and separately asserts that North's saved title/body remain North. Thus the run reports the persistent overwrite as well as the initial display mismatch. It only modifies disposable drafts in a fresh in-memory instance. [Recorded persistence observations](assets/workflows-run-1/draft-persistence.json) · [Second run](assets/workflows-run-2/draft-persistence.json).
