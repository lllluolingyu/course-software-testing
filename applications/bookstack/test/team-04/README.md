# BookStack fault-revealing tests · Team 04

Group 04: **shaoven**. Members: **Aoyu Luo, Siqi Yao, Chenglu Peng**.

This directory contains ten documented cases, browser evidence, and Python/TypeScript Playwright checks. Each case identifies its requirements, baseline coverage gap, setup, expected behavior and observed result. The additional bootstrap-mutation case is conditional on the course's immutability interpretation. Application source and baseline files are unchanged.

| Case | Requirement | Reproduced behavior | Automation |
| --- | --- | --- | --- |
| [WB-01 · Reopen and save a draft](white-box-01.md) | REQ-1, REQ-6.1 | At North's URL the editor shows South's text; saving persistently overwrites North | Python: identity and persistence |
| [WB-02 · Rank five favorites](white-box-02.md) | REQ-8, REQ-8.2 | The book with six extra visits drops out of the four-item panel; all five remain favorites | Python: ranking interpretation |
| [WB-03 · Add an existing book to a shelf](white-box-03.md) | REQ-4.5 | Shelf Edit has no operation to associate an existing book | TypeScript F01 |
| [WB-04 · Create a shelf matching the seed](white-box-04.md) | REQ-4.3 | A successful creation returns the immutable seed instead of a new identity | Python: creation identity |
| [WB-05 · Immutable shelf changes through book creation](white-box-05.md) | REQ-4.3 | Create New Book adds a persistent member to the protected bootstrap shelf | TypeScript F06; interpretation noted |
| [BB-01 · Supply a book cover](black-box-01.md) | REQ-5.3 | Book creation has no cover-selection operation | TypeScript F02 |
| [BB-02 · Select a default page template](black-box-02.md) | REQ-5.3, REQ-5.4 | Template setting is absent on creation and edit forms | TypeScript F03 checks creation |
| [BB-03 · Find an edit in Recent Activity](black-box-03.md) | REQ-3.1 | Edited page appears in Recently Updated Pages but the activity feed is absent | TypeScript F04 checks the missing feed after book creation |
| [BB-04 · Toggle dashboard details](black-box-04.md) | REQ-3.1 | Dashboard lacks the referenced details toggle | TypeScript F05, first assertion |
| [BB-05 · Switch dashboard to dark mode](black-box-05.md) | REQ-3.1 | Dashboard lacks the referenced theme control | TypeScript F05, second assertion |

Automation supplements these documents: F01–F05 are not additional defects, and the two Python draft checks concern one defect. Ten documents do not imply ten independently awarded cases.

## Run manually

Requires Node.js 22.12+ and npm. From the repository root:

```sh
cd applications/bookstack
npm ci --include=dev --include=optional
DATABASE_URL=:memory: sh start.sh
```

Open the printed URL in a fresh browser context. Stop with Ctrl+C and restart for each manual case. The application initializes its verified account and immutable bootstrap shelf itself. For authenticated cases, use the public course fixture `bookstack_user@example.com` / `Password123!`. No private storage or session injection is needed. On Windows PowerShell, set `$env:DATABASE_URL=':memory:'` before `./start.bat`; see the [course startup guide](../../../../README.md#start-an-application).

## Automated workflow checks

The [Python tests](check_workflows.py) check WB-01, WB-02 and WB-04. WB-01 has separate identity and save/reload tests so that the first assertion does not hide the persistent overwrite. From `applications/bookstack`, after installing the Node dependencies:

```sh
npm run build
python3 -m venv test/team-04/.venv
test/team-04/.venv/bin/python -m pip install -r test/team-04/requirements-tests.txt
test/team-04/.venv/bin/python -m playwright install chromium
test/team-04/.venv/bin/python test/team-04/check_workflows.py
```

Python 3.11+ is required. On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. The pinned Playwright dependency is in [requirements-tests.txt](requirements-tests.txt). An existing Chromium binary can be selected with `CHROMIUM_EXECUTABLE`.

The script starts a fresh loopback BookStack process and application-seeded in-memory database for each test, then closes it. On course revision `024c2bc`, all **four tests fail at the documented requirement assertions**; unittest reports five failures because the persistence test also records an editor-identity subtest failure before continuing to save. This is one draft defect, not three defects. Use a test name to run one check, for example `Team04Workflows.test_save_after_history_preserves_selected_draft`.

Set `TEAM04_EVIDENCE_DIR=test/team-04/output/workflows` to save screenshots and observations during a run. Generated output, virtual environments and dependencies are excluded from Git. Checked-in evidence is under [workflows-run-1](assets/workflows-run-1/verification.txt) and [workflows-run-2](assets/workflows-run-2/verification.txt).

## Automated feature and bootstrap checks

The [TypeScript tests](faults.spec.ts) cover WB-03, BB-01–05 and WB-05. From `applications/bookstack`, build once and install the separate test dependencies:

```sh
npm run build
cd test/team-04
npm ci --ignore-scripts --no-audit --no-fund
npx playwright install chromium
npm run typecheck
npm test
```

`npm test` starts its own loopback instance on port 3104 with an in-memory database, using the application's normal initialization. It refuses to reuse a running instance, so it does not reset or mutate an existing site. If the port is occupied, use `TEAM04_PORT=3105 npm test` (PowerShell: `$env:TEAM04_PORT='3105'; npm test`). Use `npm run test:headed` to watch, or `npm test -- --grep F06` to run one case.

The expected result on the supplied implementation is **six failed tests and exit code 1**. Each test asserts required behavior; failures are not inverted or marked expected-pass. F05 groups two control checks. Browser-launch/setup errors are not fault evidence. Feature checks stop at missing entry points and do not claim successful upload, template selection or theme changes. Their selectors target this English implementation; full-page screenshots and source inspection corroborate the observations, but they are not universal selectors for arbitrary alternative interfaces.

Reports and traces go to ignored `output/playwright/`. `node export-evidence.mjs run-4` copies completed requirement failures into `assets/run-4/`, rejecting missing evidence and setup errors. [Run 1](assets/run-1/results.json), [Run 2](assets/run-2/results.json), and the [final integrated run](assets/run-3/results.json) each contain six assertion failures, screenshots, observed counts and source hashes.

## Verification and interpretation

- Target application revision: `024c2bcef427351918168a0eb414cf907822b4ac`.
- Original manual cases: reported in two independent Chromium runs using Node.js 22.23.5 and Chromium 143.0.7499.4, with the original screenshots retained. Chapter-specific page membership, chapter favorite persistence and recently updated-page opening also passed in that exploration.
- Added automation: Node.js v25.9.0, Python 3.14.5, Python Playwright 1.65.2, TypeScript Playwright 1.64.1, Chromium headless shell on macOS arm64. Application build and TypeScript checking passed. Both workflow runs used fresh state per test; both recorded TypeScript runs used fresh state per suite. See the [validation record](assets/validation.md).
- Expected behavior is derived from the course requirements and supplied reference images. An independent live reference deployment was not exercised. WB-02's visit-frequency ranking is an interpretation of “Most Viewed,” not a quoted numeric algorithm. BB-03–05 use REQ-3.1's explicit reference-dashboard clause. WB-05 interprets “immutable” as protecting related books as well as text metadata.
- Final requirement interpretation, case independence and credit are subject to course review. The TA's rich-text and recently-viewed/favorite-filter examples are excluded.

## Submission scope

Submit only this directory's documents, scripts, pinned dependency manifests, configuration and selected evidence. Do not commit `node_modules`, `.venv`, `output`, application build artifacts or runtime databases. Team submission title: `[BookStack][Team 04] Add fault-revealing tests`.
