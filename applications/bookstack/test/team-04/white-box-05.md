# REQ-8.1 Test: Remove a page favorite after saving a draft edit (WB-05)

## Description

Saving an edit as a draft changes what opens from the favorites panel. The page stays in the panel, but its editor has no Unfavorite action.

## Requirement: Expected Output

Under REQ-8.1 and REQ-8.2, the saved favorite persists across navigation. Opening the sole favorite from the homepage must let its owner remove it. [Course requirement](../../requirements/requirements.yaml#L918)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance and sign in](README.md#run-manually). Create book `Navigation manual`, click **New Page**, enter title `Beacon signals` and body `Published v1`, and click **Save Page**.
2. Open **Beacon signals**, click **Favorite**, and confirm **Unfavorite** reports `aria-pressed="true"`. Return to `/` as a control and confirm **Beacon signals** appears in both **My Most Viewed Favorites** and **Recently Updated Pages**. In a separate logged-out window, open the page URL and verify that it shows `Published v1`.
3. In the signed-in window, open **Beacon signals**, click **Edit**, change its body to `Draft v2`, and click **Save Draft**.
4. Return to `/`, reload, and inspect all dashboard regions. Click **Beacon signals** inside **My Most Viewed Favorites** and look for **Unfavorite**.
5. Open a logged-out browser context (or click **Log out**), inspect `Navigation manual`'s **Page list**, and open **Beacon signals**'s URL.

## Observed Output

The favorite reopened **Edit Page** with no **Unfavorite** action. It still appeared in **My Favourites**. The page also disappeared from **Recently Updated Pages**, and a logged-out visitor saw **Page not found** at the previously working URL. [Dashboard after Save Draft](assets/published-draft-home.png) · [Favorite opened into editor without Unfavorite](assets/published-draft-editor.png) · [Recorded before/after states](assets/published-draft-state.json)

## Test design and baseline coverage

White-box state-transition test. Saving a draft sets the draft flag on the existing page. Favorites still include that page, and the draft view returns the editor before rendering the favorite action. The assertion checks favorite removal. The public reading view and updated-pages list provide additional observations. [Page update](../../backend/src/slices/bookstack.ts#L431) · [Homepage favorites](../../backend/src/slices/bookstack.ts#L205) · [Draft and reading views](../../frontend/src/slices/bookstack.tsx#L685)

The editor baseline reopens a published page. The favorites baselines use a book. This case follows an already-favorited page through a draft save and tries to remove the same preference. [Editor baseline](../baseline/REQ-6.4.spec.ts) · [Favorite baseline](../baseline/REQ-8.1.spec.ts) · [Homepage favorite baseline](../baseline/REQ-8.2.spec.ts)

The Playwright check is `Team04Workflows.test_draft_edit_keeps_favorite_removable`. [Setup and run command](README.md#automated-workflow-checks)
