# REQ-4.3 Test: Create a shelf with the bootstrap shelf’s metadata (WB-04)

## Description

Saving a new shelf with the exact bootstrap metadata reports success and returns the existing shelf’s identity.

## Requirement: Expected Output

Under REQ-4.3, a successful **Save Shelf** creates a separate user shelf. The existing bootstrap shelf must keep its original identity. [Course requirement](../../requirements/requirements.yaml#L248)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Open **Shelves → Benchmark Bootstrap Shelf**. Note its URL and displayed description.
2. Click **New Shelf**. Enter `Benchmark Bootstrap Shelf` as Name and `Entry shelf for the New Shelf creation action.` as Description, including the final period. Leave Tags empty.
3. Click **Save Shelf**. Inspect the returned Shelf list and open its entry. Compare its URL and available actions with step 1. The browser Network panel can also show the response to the save.
4. Repeat with the same name, empty tags and description `Team 04 editable shelf`. Count the list entries and compare the two save responses.

## Observed Output

The exact match returned HTTP 200 with the existing shelf’s ID `1`. The list still contained one shelf. Changing only the description produced ID `2` and a second list entry. [Shelf list after the exact match](assets/seed-collision-list.png) · [Recorded identities and responses](assets/seed-comparison.json)

## Test design and baseline coverage

White-box test of the existing-row branch in shelf creation. REQ-4.3 says a successful save creates a shelf and distinguishes user-created shelves from the immutable bootstrap shelf. The creation lookup compares Name, Description and Tags against every shelf, including the bootstrap row. Compare an exact match with a one-field change. The assertion concerns the identity returned by a successful save. [Requirement](../../requirements/requirements.yaml) · [Existing-row and insert branches](../../backend/src/slices/bookstack.ts#L265)

The baseline uses unique names, so every successful creation goes through the insert branch. It does not check what the form treats as success when the lookup selects an immutable object. [Baseline](../baseline/REQ-4.3.spec.ts)

The Playwright check is `Team04Workflows.test_new_shelf_is_separate_from_bootstrap`. [Setup and run command](README.md#automated-workflow-checks)
