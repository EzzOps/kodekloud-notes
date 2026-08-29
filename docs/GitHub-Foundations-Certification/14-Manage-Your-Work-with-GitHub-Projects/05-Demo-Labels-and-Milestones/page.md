# Demo Labels and Milestones

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/Demo-Labels-and-Milestones/page

Explains using GitHub labels and milestones to organize, categorize, and track issues and pull requests for releases, converting drafts, assigning labels, creating milestones, and monitoring progress.

This guide shows how to organize repository work using GitHub labels and milestones. You’ll learn how to convert drafts to issues, apply labels to categorize work, create milestones to represent releases or targets, and track progress across issues and pull requests.

Converting draft issues

* If you have draft issues, open each draft, choose the correct target repository if prompted, and publish it. Once published the item becomes a normal issue that can be labeled, assigned, and added to projects.
* After publishing, you’ll see the issue details, comment controls, and the sidebar controls to add labels, assignees, and project membership.

<Frame>
  <img alt="The image shows a GitHub issue page titled &#x22;Update documentation for new power-ups,&#x22; with options to add comments, labels, and assign the issue. A dropdown menu for label application is open, showing various label options like &#x22;bug&#x22; and &#x22;high-priority.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  If a draft doesn’t belong to any repository yet, GitHub will prompt you to choose one when you publish. Confirm the repository before publishing to avoid placing the issue in the wrong project.
</Callout>

Adding labels

Labels allow you to categorize and filter issues and pull requests by type, priority, or any team convention. Common label examples include `bug`, `documentation`, and `enhancement`.

How to add a label:

1. Open the issue and find the Labels dropdown in the issue sidebar.
2. Select one or more existing labels.
3. If no existing label fits, create a custom label in your repository’s Labels management area.

Examples:

* Add `documentation` to a docs-related issue.
* Add `enhancement` to a feature request such as a new pop-up.

Benefits:

* Visual categorization for faster triage.
* Power to filter issues across the repository or project boards.

Creating and using milestones

Milestones group issues and pull requests for a specific release or target and display progress toward completion (open vs. closed items).

To create a milestone:

1. Go to the repository Issues tab and click Milestones.
2. Create a new milestone with a clear title, for example “Version 2.0 Launch”.
3. Optionally add a due date and a descriptive summary to clarify scope.

<Frame>
  <img alt="The image shows a GitHub interface where a user is creating a milestone titled &#x22;Version 2.0 Launch,&#x22; with fields for a due date and description." />
</Frame>

Assign issues to the milestone:

* Open the issue list or an individual issue.
* Select the relevant issues and choose the milestone you created.

<Frame>
  <img alt="This image shows a GitHub interface with a list of issues for a project. Two issues are selected, and a milestone option for &#x22;Version 2.0 Launch&#x22; is being highlighted." />
</Frame>

Tracking progress

* The Milestones view shows a count of issues and how many are closed, along with a progress bar.
* When you close an issue that belongs to a milestone, the milestone progress automatically updates (for example, 1 of 2 issues closed = 50% complete).

<Frame>
  <img alt="The image shows a GitHub issue page titled &#x22;Update documentation for new power-ups #9,&#x22; which is marked as closed. It includes activity details like issue creation, label assignments, and milestone additions." />
</Frame>

<Callout icon="warning">
  Milestones show aggregated progress but don’t automatically reassign or re-prioritize issues. Make sure to review linked issues and update labels, assignees, or descriptions as scope changes.
</Callout>

When to use labels vs milestones

| Resource  | Best use case                                                                  | Example                                 |
| --------- | ------------------------------------------------------------------------------ | --------------------------------------- |
| Label     | Categorize or filter issues and PRs by type, priority, or team                 | `bug`, `documentation`, `high-priority` |
| Milestone | Group issues/PRs for a release or specific project target and track completion | `Version 2.0 Launch`                    |

Summary

* Use labels to categorize and filter work (`bug`, `documentation`, `enhancement`).
* Use milestones to group issues and pull requests for releases and to track progress.
* Combining labels and milestones helps you quickly organize work, prioritize issues, and monitor release status.

Links and references

* [GitHub Issues documentation](https://docs.github.com/en/issues)
* [Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
* [About milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/35468742-f165-40be-a212-bb79ab651713" />
</CardGroup>
