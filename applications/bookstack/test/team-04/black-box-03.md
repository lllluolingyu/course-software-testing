# REQ-3.1 Test: Find a completed page edit in Recent Activity (BB-03)

## Description

A saved edit appears in Recently Updated Pages. The authenticated dashboard has no Recent Activity feed showing who edited the page.

## Requirement: Expected Output

REQ-3.1 requires recent activity to follow the dashboard reference, where an entry identifies the actor, action, and affected page. [Course requirement](../../requirements/requirements.yaml#L147)

## Test description

**Manual browser steps.**

1. Start a [fresh instance and sign in](README.md#run-manually). Create the book `Research log`. Choose **New Page**, enter title `Tide tables` and body `Morning observation`, and click **Save Page**.
2. Open **Tide tables** from the book's Page list, choose **Edit**, change the body to `Evening observation`, and click **Save Page**. Verify the reading page displays the new body.
3. Open the homepage and reload. Find **Tide tables** in **Recently Updated Pages** as a control. Look for the activity feed and the page edit.

## Observed Output

Recently Updated Pages contained `Tide tables`. The dashboard had no Recent Activity feed or entry identifying the edit. [Authenticated dashboard after the edit](assets/activity.png)

## Test design and baseline coverage

Black-box state transition under REQ-3.1. An identified user's edit creates recent activity. The authenticated reference displays an actor, an action and the affected page in **Recent Activity**. The expected behavior comes from that explicit dashboard requirement and its image. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

The dashboard baseline stops after finding four named regions immediately after login. The updated-pages baseline opens a published page from its list. Neither checks the activity feed after an edit. [Dashboard baseline](../baseline/REQ-3.1.spec.ts) · [Updated-pages baseline](../baseline/REQ-9.1.spec.ts)
