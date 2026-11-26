# REQ-4.3 Test: Check the bootstrap shelf after creating a book (WB-06)

## Description

The built-in shelf starts empty. A book added through its Create New Book action appears in the shelf’s list after reload.

## Requirement: Expected Output

REQ-4 and REQ-4.3 define the bootstrap shelf as immutable and describe its related-book list as empty. Its membership should stay empty after this workflow. REQ-5.6 describes the ordinary shelf workflow used for comparison. [Course requirement](../../requirements/requirements.yaml#L248)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Open **Shelves → Benchmark Bootstrap Shelf**.
2. Confirm its **Book list** displays `No books on this shelf yet` and that **Edit** and **Delete** are absent from **Actions**.
3. Click **Create New Book** in `Benchmark Bootstrap Shelf`'s **Actions** sidebar, enter `Intruder volume` in **Name** and `Added directly to bootstrap shelf` in **Description**, and click **Save Book**.
4. On the opened book details, activate the **Benchmark Bootstrap Shelf** parent button and reload the shelf page.

## Observed Output

The book saved successfully. After reloading the bootstrap shelf, its **Book list** contained `Intruder volume`. The shelf still offered neither **Edit** nor **Delete**. [Mutated bootstrap shelf after reload](assets/bootstrap-mutated.png)

## Test design and baseline coverage

White-box branch comparison. The shelf view checks the bootstrap flag when rendering Edit and Delete. Create New Book is also available on the bootstrap shelf. The shelf-book creation handler writes the selected shelf ID onto the book. This case follows the visible creation action and checks the resulting shelf membership. [Shelf actions](../../frontend/src/slices/bookstack.tsx#L265) · [Shelf and book creation handlers](../../backend/src/slices/bookstack.ts#L301)

The shelf-book baseline adds a book to a user-created shelf. WB-04 checks the identity returned by shelf creation. This case starts on the built-in shelf and examines its book list after saving a book. [Shelf-book baseline](../baseline/REQ-5.6.spec.ts) · [WB-04](white-box-04.md)

The Playwright check is `Team04Workflows.test_bootstrap_shelf_remains_immutable`. [Setup and run command](README.md#automated-workflow-checks)
