# REQ-8.2 Test: Rank five favorites in a four-item panel (WB-02)

## Description

The homepage omits the only favorite with repeated visits when four books were favorited more recently.

## Requirement: Expected Output

Under REQ-8 and REQ-8.2, the uniquely most-viewed favorite belongs in the homepage’s four-item panel. Any three of the four tied books can accompany it. The full collection should contain all five. [Course requirement](../../requirements/requirements.yaml#L970)

## Test description

**Playwright and browser steps.**

1. Start a [fresh instance and sign in](README.md#run-manually). Begin with no favorites or viewing history.
2. From **Books → Create New Book**, create `Atlas`. On its details click **Favorite** and verify **Unfavorite** is pressed. Repeat once each for `Birch`, `Cedar`, `Dune`, and `Elm`, in that order.
3. Open **Books**, select **Atlas** from the Book list and wait for its heading. Repeat this list-to-details visit six times. Leave the other four books at their single creation visit.
4. Open the homepage and inspect **My Most Viewed Favorites**. Open the complete favorites collection from the header and check all five identities.

## Observed Output

The homepage listed Elm, Dune, Cedar, and Birch. Atlas appeared only in the complete collection, where all five favorites were present. [Homepage panel](assets/ranking-home.png) · [Complete collection](assets/ranking-all.png)

## Test design and baseline coverage

White-box boundary test for REQ-8 and REQ-8.2. The homepage displays at most four most-viewed favorites. The backend stores only the last visit on repeated views. Its homepage code sorts favorites by the time they were favorited and selects four. Use five favorites and give the oldest favorite more visits than every other book. This distinguishes the two selection rules without relying on a ranking tie. [Requirements](../../requirements/requirements.yaml) · [Repeat-visit update](../../backend/src/slices/bookstack.ts#L36) · [Homepage selection](../../backend/src/slices/bookstack.ts#L217)

The baseline opens one favorite from the homepage. The TA example tests whether favoriting removes a recent visit. This case checks which favorites the four-slot panel admits when there are five candidates. [Baseline](../baseline/REQ-8.2.spec.ts) · [TA demonstration](../../../../FOLLOWING.md)

The Playwright check is `Team04Workflows.test_most_viewed_favorite`. [Setup and run command](README.md#automated-workflow-checks)
