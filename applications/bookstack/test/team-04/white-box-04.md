# WB-04 · Save Shelf reports success with the immutable bootstrap shelf's identity

**Method and requirement.** White-box test of the existing-row branch in shelf creation. REQ-4.3 says a successful save creates a shelf and distinguishes user-created shelves from the immutable bootstrap shelf. The creation lookup compares Name, Description and Tags against every shelf, including the bootstrap row. Compare an exact match with a one-field change. The assertion concerns the identity returned by a successful save. [Requirement](../../requirements/requirements.yaml) · [Existing-row and insert branches](../../backend/src/slices/bookstack.ts#L265)

**New coverage.** The baseline uses unique names, so every successful creation goes through the insert branch. It does not check what the form treats as success when the lookup selects an immutable object. [Baseline](../baseline/REQ-4.3.spec.ts)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Open **Shelves → Benchmark Bootstrap Shelf**. Note its URL and displayed description.
2. Click **New Shelf**. Enter `Benchmark Bootstrap Shelf` as Name and `Entry shelf for the New Shelf creation action.` as Description, including the final period. Leave Tags empty.
3. Click **Save Shelf**. Inspect the returned Shelf list and open its entry. Compare its URL and available actions with step 1. The browser Network panel can also show the response to the save.
4. Repeat with the same name, empty tags and description `Team 04 editable shelf`. Count the list entries and compare the two save responses.

**Expected.** A save that reports success creates a shelf separate from the immutable seed. The requirement gives no general policy for duplicate names. This case checks the successful creation outcome and does not prescribe wording for a validation error.

**Observed.** Both submissions returned to the list. The exact match received HTTP 200 with the seed's ID 1. The list still had only the original entry, whose details offered neither Edit nor Delete. Changing only the description produced ID 2 and two list entries with the same name. [Shelf list after the exact match](assets/seed-collision-list.png) · [Recorded identities and responses](assets/seed-comparison.json) · [Automated identity check and run command](README.md#automated-workflow-checks)
