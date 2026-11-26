# BB-05 · Switch the authenticated dashboard to dark mode

**Method and requirement.** Black-box test of a display preference under REQ-3.1. Start with the browser in light mode and try to select dark mode in the application. The reference shows a **Dark Mode** control on the authenticated dashboard. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

**New coverage.** The dashboard baseline checks the personal and content lists. It makes no attempt to change the dashboard's color scheme. [Baseline](../baseline/REQ-3.1.spec.ts)

## Reproduce

1. Use a browser with a light color preference. Start a [fresh instance and sign in](README.md#run-manually).
2. Create `Research log` and publish `Tide tables` with body `Morning observation`. Open the homepage and reload. Verify that **BookStack User** and the newly published page are visible.
3. Inspect the header, user area and dashboard actions for a way to switch the application to dark mode. Activate it if available.

**Expected.** The authenticated dashboard offers the dark-mode action shown in the reference. No particular colors or cross-session persistence are required by this check.

**Observed.** The header offered navigation, favorites and logout. The dashboard offered its list entries. Neither exposed a theme action. The captured light dashboard matches the separate details-control run pixel for pixel. [Full dashboard on the target](assets/details.png)
