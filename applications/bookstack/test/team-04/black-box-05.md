# BB-05 · Switch the authenticated dashboard to dark mode

**Method and requirement.** Black-box test of a display preference under REQ-3.1. Start with the browser in light mode and try to select dark mode in the application. REQ-3.1 states that dashboard controls follow the visual reference, which exposes a **Dark Mode** action on the authenticated dashboard. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

**New coverage.** The dashboard baseline checks the four named personal and content list regions after login. It makes no attempt to switch the dashboard's color scheme, and `BB-04` separately checks the list-detail toggle. [Baseline](../baseline/REQ-3.1.spec.ts)

## Reproduce

1. Use a browser with a light color preference. Start a [fresh instance and sign in](README.md#run-manually).
2. Create book `Solar atlas` and publish page `Daylight chart` with body `Noon observation`. Open `/` and reload. Verify that **BookStack User** and **Daylight chart** (under **Recently Updated Pages**) are visible.
3. Inspect the header, user area and dashboard controls for a way to switch the application to dark mode, and activate it if available.

**Expected.** The authenticated dashboard offers a dark-mode control corresponding to the reference. No particular palette values or cross-session persistence rules are assumed by this check.

**Observed.** The header offered navigation links, `My Favourites`, `BookStack User` and `Log out`, while the dashboard body rendered only the four list panels with no theme control anywhere on the page. [Full dashboard on the target](assets/dark-mode.png)
