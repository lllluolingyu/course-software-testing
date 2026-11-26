# REQ-5.3 Test: Choose a cover image when creating a book (BB-01)

## Description

The creation form has no control for supplying an optional book cover.

## Requirement: Expected Output

REQ-5.3 allows a book to be saved without a cover and also allows the user to select one. The reference creation form shows a **Cover image** section. [Course requirement](../../requirements/requirements.yaml#L480)

## Test description

**Manual browser steps.**

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Have a local image ready to select. The supplied [reference PNG](../../requirements/reference/create_book.png) works as test input for this step.
2. Open **Books → Create New Book**. Enter `Cover control` as the name and click **Save Book**. Confirm its detail heading appears.
3. Open **Books → Create New Book** again. Enter `Illustrated atlas` as the name and `A book with a cover` as the description.
4. Inspect the complete form and its available actions. Try to open the cover selection and supply the image.

## Observed Output

The control book saved. The second form offered Name, Description, Tags, Cancel, and Save Book. There was no way to start selecting an image. [Full form on the target](assets/cover.png)

## Test design and baseline coverage

Black-box equivalence partitioning under REQ-5.3. The two inputs are a book with its optional cover omitted and a book for which the user wants to supply one. The reference creation form exposes a **Cover image** section. [Requirement](../../requirements/requirements.yaml) · [Reference form](../../requirements/reference/create_book.png)

The baseline saves or cancels books with text metadata. The TA demonstration exercises rich-text descriptions. Neither attempts to supply a cover. [Baseline](../baseline/REQ-5.3.spec.ts) · [TA demonstration](../../../../FOLLOWING.md)
