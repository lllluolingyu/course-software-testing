# BookStack fault-revealing tests · Team 04

Submitted by **shaoven** for Team 04.

| Case | Requirement | Reproduced behavior |
| --- | --- | --- |
| [WB-01 · Reopen and save a draft](white-box-01.md) | REQ-1, REQ-6.1 | At North's URL the editor shows South's text. Saving overwrites North. |
| [WB-02 · Rank five favorites](white-box-02.md) | REQ-8, REQ-8.2 | The book with six extra visits drops out of the four-item panel. All five remain favorited. |
| [WB-03 · Add an existing book to a shelf](white-box-03.md) | REQ-4, REQ-4.5 | Shelf Edit updates text metadata only and offers no path to modify related books. |
| [WB-04 · Create a shelf matching the seed](white-box-04.md) | REQ-4.3 | An exact metadata match returns the immutable seed as a successful creation. |
| [WB-05 · Remove a page favorite after saving a draft edit](white-box-05.md) | REQ-8.1, REQ-8.2 | The page remains in favorites, but opening it leads to an editor without Unfavorite. |
| [WB-06 · Create a book on the bootstrap shelf](white-box-06.md) | REQ-4, REQ-4.3, REQ-5.6 | After a book is created on the immutable bootstrap shelf, it appears there on reload. |
| [WB-07 · Publish identical pages in each login state](white-box-07.md) | REQ-2, REQ-6.1 | Two successful submissions produce one page while logged out and two while signed in. |
| [BB-01 · Supply a book cover](black-box-01.md) | REQ-5.3 | The book creation form has no way to select a cover image. |
| [BB-02 · Select a default page template](black-box-02.md) | REQ-5.3, REQ-5.4 | The template setting is absent on the creation and edit forms. |
| [BB-03 · Find a page edit in Recent Activity](black-box-03.md) | REQ-3.1 | The page appears in Recently Updated Pages, while the activity feed is absent. |
| [BB-04 · Toggle dashboard details](black-box-04.md) | REQ-3.1 | The authenticated dashboard lacks the referenced details toggle. |
| [BB-05 · Switch the dashboard to dark mode](black-box-05.md) | REQ-3.1 | The authenticated dashboard lacks the referenced theme control. |

## Run manually

Use Node.js 22.12 or newer. From the repository root, on Linux or macOS run the following.

```sh
cd applications/bookstack
npm ci --include=dev --include=optional
DATABASE_URL=:memory: sh start.sh
```

Open the URL printed by the launcher in a fresh browser context. Stop the process with Ctrl+C and repeat the last command for each case. This starts each case with BookStack's own verified account and immutable bootstrap shelf. For signed-in cases use `bookstack_user@example.com` and `Password123!`. The [course startup guide](../../../../README.md#start-an-application) includes Windows commands. Each case links its actual screenshots or observations and the expected behavior's source.

## Automated workflow checks

The [Python Playwright tests](check_workflows.py) assert the expected behavior for WB-01, WB-02, WB-04, WB-05, WB-06 and WB-07. From `applications/bookstack`, after installing the Node dependencies above, run the following in a Python 3.11+ environment.

```sh
npm run build
python -m pip install playwright
python -m playwright install chromium
python test/team-04/check_workflows.py
```

The script starts a loopback BookStack process on a free port with a new in-memory database for each case. To use an existing Chromium installation, set `CHROMIUM_EXECUTABLE` to its full executable path. On course revision `024c2bc` the expected reproduction is six failed assertions. Each case can also be run by appending its unittest name, for example `Team04Workflows.test_history_returns_to_selected_draft`.

## Verification

The expected results come from the course requirements and reference images. On course revision `024c2bc`, all six Playwright checks failed at their documented assertions using Node.js 22.23.5 and Chromium 143.0.7499.4. Each of the six manual cases includes screenshots of the observed behavior.
