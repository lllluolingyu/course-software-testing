# BB-01 · Create a book with a cover image

**Method and requirement.** Black-box equivalence partitioning under REQ-5.3. The two inputs are a book with its optional cover omitted and a book for which the user wants to supply one. The reference creation form exposes a **Cover image** section. [Requirement](../../requirements/requirements.yaml) · [Reference form](../../requirements/reference/create_book.png)

**New coverage.** The baseline saves or cancels books with text metadata. The TA demonstration exercises rich-text descriptions. Neither attempts to supply a cover. [Baseline](../baseline/REQ-5.3.spec.ts) · [TA demonstration](../../../../FOLLOWING.md)

## Reproduce

1. Start a [fresh instance](README.md#run-manually) and stay logged out. Have a local image available, for example the supplied reference PNG linked above.
2. Open **Books → Create New Book**. Enter `Cover control` as the name and click **Save Book**. Confirm its detail heading appears.
3. Open **Books → Create New Book** again. Enter `Illustrated atlas` as the name and `A book with a cover` as the description.
4. Inspect the complete form and its available actions. Try to open the cover selection and supply the image.

**Expected.** Creating a book without a cover succeeds. A user who wants a cover can start selecting one. Acceptance of a specific image format is outside this check.

**Observed.** The control book saved. The second form offered Name, Description, Tags, Cancel and Save Book. There was no way to start selecting a cover. The failure occurred before choosing a file. [Full form on the target](assets/cover.png)
