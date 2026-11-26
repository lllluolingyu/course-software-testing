# REQ-6.1 Test: Reopen the selected draft through browser history (WB-01)

## Description

A direct history jump between two drafts leaves the previous draft’s text in the editor. Saving those fields overwrites the draft at the current URL.

## Requirement: Expected Output

Under REQ-6.1 and REQ-1, reopening North must show North’s saved title and body. Saving without changing either field must preserve North’s contents. [Course requirement](../../requirements/requirements.yaml#L654)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance and sign in](README.md#run-manually). Create the book `Field notes`. Choose **New Page**, enter title `North` and body `North observations`, then **Save Draft**. Repeat for `South` with body `South observations`.
2. Open **North** from the book's Page list. Verify its fields and note the draft URL. Click **Back to book** inside the editor and open **South**. Verify its fields and different URL.
3. In Chromium, open the browser Back button's history menu and select the entry **two positions back**, North. This goes from South to North in one navigation (`history.go(-2)`).
4. At North's URL, read both fields. Reload without saving and compare as a control showing what North actually stored on the server.
5. Repeat the traversal from the reloaded North via **Back to book → South → two positions back**. Click **Save Draft** with the displayed fields untouched, reload, then open the parent book's Page list.

## Observed Output

North’s URL showed `South` and `South observations`. Reloading before saving restored North. After the second jump and save, North’s stored title and body both matched South, and the book listed two drafts titled `South`. [Navigation and save observations](assets/draft-navigation.tsv) · [Book after saving](assets/draft-after-save.png)

## Test design and baseline coverage

White-box test of editor identity. Both draft routes render the same editor component. The component initializes its fields on mount and skips reloading them when it receives an initial page. The save action uses the current page ID. A single history jump changes the draft ID while the editor stays mounted. [Editor state and save action](../../frontend/src/slices/bookstack.tsx#L612) · [Draft view](../../frontend/src/slices/bookstack.tsx#L685)

The draft baseline creates one draft and checks dashboard membership. The read/edit baseline reopens one published page. Neither checks whether the editor fields and mutation actions agree on the draft identity when navigating between two saved drafts. [Draft baseline](../baseline/REQ-6.1.spec.ts) · [Editor baseline](../baseline/REQ-6.4.spec.ts)

The Playwright check is `Team04Workflows.test_history_returns_to_selected_draft`. [Setup and run command](README.md#automated-workflow-checks)
