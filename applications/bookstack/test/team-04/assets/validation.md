# Validation record

Application source: `024c2bcef427351918168a0eb414cf907822b4ac`. The integrated submission starts from teammate commit `a686a838ff3f42c4c8398ffe42efe2c02ea98414`, which changes only team test materials. Application code is identical to the baseline. Validation used new in-memory application instances initialized through the application's own startup, then normal browser login and content creation.

## Static checks

`npm run build` passed for the application. Vite emitted its existing warning about the non-module `/api/clock.js` script; both frontend and backend builds completed. `npm run typecheck` passed for the TypeScript suite. Python files parsed successfully. All relative document and evidence file links were checked. No application source or baseline tests were edited.

## Python workflow suite

Command, from `applications/bookstack`: `python test/team-04/check_workflows.py`. The recorded environment used Python 3.14.5, Playwright 1.65.2, Node.js v25.9.0 and the locally installed Playwright Chromium headless shell. `CHROMIUM_EXECUTABLE` selected that binary, and `TEAM04_EVIDENCE_DIR` selected each evidence directory. Browser startup ran outside the restricted execution sandbox; no application security setting was changed.

| Run | Result | Evidence |
| --- | --- | --- |
| 1 | Four methods exercised; five recorded assertion failures; no setup errors | [Output](workflows-run-1/verification.txt), [metadata and script hash](workflows-run-1/metadata.json) |
| 2 | Same four methods and five assertion failures on new instances | [Output](workflows-run-2/verification.txt), [metadata and script hash](workflows-run-2/metadata.json) |

Five assertion failures arise because `test_save_after_history_preserves_selected_draft` records both an editor-identity subtest failure and the final persistence assertion failure. This does not represent five independent bugs. Both runs recorded page ID 1 being saved as South and remaining South after reload. [Run 1 persistence](workflows-run-1/draft-persistence.json) · [Run 2 persistence](workflows-run-2/draft-persistence.json).

## TypeScript suite

Command, from `applications/bookstack/test/team-04`: `npm test`. Playwright 1.64.1; Chromium; one worker; no retries.

The [first](run-1/results.json) and [second](run-2/results.json) source-identical test runs each reached all six requirement checks and failed at those checks. The [third run in the integrated worktree](run-3/results.json) reproduced all six failures. Run records include test/configuration hashes and individual observations/screenshots. No browser-startup failures are included in these exported evidence sets.

F01–F05 correspond to the existing association, cover, template, activity and display-control findings. F06 is the additional immutable-bootstrap-shelf candidate. Screenshots establish the missing UI operations; no successful upload or template save was possible or claimed.

## Boundaries

Expected results come from the supplied requirements and reference images. No independent live reference deployment was tested. WB-02's visit-frequency interpretation and WB-05's related-book immutability interpretation are stated explicitly in their case documents. Requirement interpretation and independent case counting remain subject to course review.
