# REQ-3.1 Test: Toggle details on a populated dashboard (BB-04)

## Description

The dashboard offers no way to change how much detail the lists display.

## Requirement: Expected Output

REQ-3.1 points to the authenticated dashboard reference, which includes a **Toggle Details** control for the lists. [Course requirement](../../requirements/requirements.yaml#L147)

## Test description

**Manual browser steps.**

1. Start a [fresh instance and sign in](README.md#run-manually). Create `Research log`, then publish a page titled `Tide tables` with body `Morning observation`.
2. Return home and reload. Confirm **Recently Updated Pages** contains **Tide tables**.
3. Inspect the dashboard and its available actions. Try to switch the amount of detail displayed for the lists, then switch back if possible.

## Observed Output

The populated panel displayed the page entry. No details toggle was available. [Full dashboard on the target](assets/details.png)

## Test design and baseline coverage

Black-box test of the authenticated dashboard controls in REQ-3.1. The reference offers **Toggle Details** above the personal lists. Use a populated list so there is content for the display control to affect. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

The dashboard baseline confirms four list regions after login. It never tries to change the amount of detail displayed. [Baseline](../baseline/REQ-3.1.spec.ts)
