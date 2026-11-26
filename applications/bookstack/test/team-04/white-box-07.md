# REQ-6.1 Test: Publish two identical pages in each login state (WB-07)

## Description

Two separate New Page submissions produce different page counts depending on whether the author is signed in.

## Requirement: Expected Output

Under REQ-6.1, each **New Page → Save Page** submission adds exactly one page to the book, including while logged out. After two successful submissions, each book should list two distinct pages. REQ-2 makes publishing available in both login states. [Course requirement](../../requirements/requirements.yaml#L654)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Create book `Anonymous log`.
2. Click **New Page**, enter title `Shift report` and body `All clear.`, and click **Save Page**. Repeat **New Page → `Shift report` / `All clear.` → Save Page** a second time on `Anonymous log`. Count the entries in **Page list** and inspect both `POST /api/books/:id/pages` responses.
3. Click **Login**, sign in as `bookstack_user@example.com` / `Password123!`, and create book `Signed-in log`.
4. Use two fresh **New Page** forms on `Signed-in log` and submit the same title and body once per form. Count the entries in **Page list** and compare the `POST` responses with step 2.

## Observed Output

All four saves returned HTTP 200. The logged-out book listed one page, with ID `1` returned twice. The signed-in book listed two pages, with IDs `2` and `3` in the recorded run. [Logged-out Page list](assets/page-publish-anon.png) · [Signed-in Page list](assets/page-publish-auth.png) · [Recorded responses and counts](assets/page-publish-comparison.json)

## Test design and baseline coverage

White-box test of the existing-page lookup. For a published page, the lookup uses a null author. The insert stores a null author for a logged-out visitor and the account ID for a signed-in author. Two identical submissions per fresh book exercise both paths. [Page lookup and insert](../../backend/src/slices/bookstack.ts#L127)

The baseline publishes a single page and separately creates an owned draft. This case checks two deliberate submissions of identical content within each login state. [Page baseline](../baseline/REQ-6.1.spec.ts)

The Playwright check is `Team04Workflows.test_anonymous_page_publish_matches_authenticated_creation`. [Setup and run command](README.md#automated-workflow-checks)
