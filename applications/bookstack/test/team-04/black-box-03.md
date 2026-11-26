# BB-03 · Look up a completed page edit in Recent Activity

**Method and requirement.** Black-box state transition under REQ-3.1. An identified user's edit creates recent activity. The authenticated reference displays an actor, an action and the affected page in **Recent Activity**. The expected behavior comes from that explicit dashboard requirement and its image. [Requirement](../../requirements/requirements.yaml) · [Reference dashboard](../../requirements/reference/index_after_login.png)

**New coverage.** The dashboard baseline stops after finding four named regions immediately after login. The updated-pages baseline opens a published page from its list. Neither checks the activity feed after an edit. [Dashboard baseline](../baseline/REQ-3.1.spec.ts) · [Updated-pages baseline](../baseline/REQ-9.1.spec.ts)

## Reproduce

1. Start a [fresh instance and sign in](README.md#run-manually). Create the book `Research log`. Choose **New Page**, enter title `Tide tables` and body `Morning observation`, and click **Save Page**.
2. Open **Tide tables** from the book's Page list, choose **Edit**, change the body to `Evening observation`, and click **Save Page**. Verify the reading page displays the new body.
3. Open the homepage and reload. Find **Tide tables** in **Recently Updated Pages** as a control. Look for the activity feed and the page edit.

**Expected.** The authenticated dashboard shows recent activity, including an identifiable page update. No exact wording, timestamp or order is required.

**Observed.** The edited page appeared in the updated-pages list. The dashboard had no activity feed and no entry describing the update. [Authenticated dashboard after the edit](assets/activity.png)
