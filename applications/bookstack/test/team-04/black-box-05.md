# REQ-3.1 Test: Switch the dashboard to dark mode (BB-05)

## Description

A signed-in user starting in light mode cannot select dark mode from the dashboard.

## Requirement: Expected Output

REQ-3.1 points to the authenticated dashboard reference, which includes a **Dark Mode** control. [Course requirement](../../requirements/requirements.yaml#L147)

## Test description

**Manual browser steps.**

1. Use a browser with a light color preference. Start a [fresh instance and sign in](README.md#run-manually).
2. Create book `Solar atlas` and publish page `Daylight chart` with body `Noon observation`. Open `/` and reload. Verify that **BookStack User** and **Daylight chart** (under **Recently Updated Pages**) are visible.
3. Inspect the header, user area and dashboard controls for a way to switch the application to dark mode, and activate it if available.

## Observed Output

The dashboard displayed the account, navigation, and four list panels. None offered a theme control. [Full dashboard on the target](assets/dark-mode.png)

## Test design and baseline coverage

Black-box test of a display preference under REQ-3.1. Start with the browser in light mode and try to select dark mode in the application. REQ-3.1 states that dashboard controls follow the visual reference, which exposes a **Dark Mode** action on the authenticated dashboard. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

The dashboard baseline checks the four named personal and content list regions after login. It makes no attempt to switch the dashboard's color scheme, and `BB-04` separately checks the list-detail toggle. [Baseline](../baseline/REQ-3.1.spec.ts)
