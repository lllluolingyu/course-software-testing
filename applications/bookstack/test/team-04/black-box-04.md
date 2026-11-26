# BB-04 · Toggle details on a populated dashboard

**Method and requirement.** Black-box test of the authenticated dashboard controls in REQ-3.1. The reference offers **Toggle Details** above the personal lists. Use a populated list so there is content for the display control to affect. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

**New coverage.** The dashboard baseline confirms four list regions after login. It never tries to change the amount of detail displayed. [Baseline](../baseline/REQ-3.1.spec.ts)

## Reproduce

1. Start a [fresh instance and sign in](README.md#run-manually). Create `Research log`, then publish a page titled `Tide tables` with body `Morning observation`.
2. Return home and reload. Confirm **Recently Updated Pages** contains **Tide tables**.
3. Inspect the dashboard and its available actions. Try to switch the amount of detail displayed for the lists, then switch back if possible.

**Expected.** The dashboard offers a details toggle corresponding to the reference. The check requires no specific placement, accessible role or list of secondary fields.

**Observed.** The populated list offered the page entry. The dashboard had no details toggle. [Full dashboard on the target](assets/details.png)
