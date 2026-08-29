# Demo Project View and Insights

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/Demo-Project-View-and-Insights/page

Explains GitHub Projects automation and Insights, showing how workflows sync project boards with repository issues and visualize progress with charts

In this lesson we’ll examine how GitHub Projects keeps your board and repository in sync using project workflows (automation) and how the Insights dashboards help you measure progress over time. You’ll learn how board actions can trigger repository changes and how repository events can update cards on your board automatically.

I’m back in the project view and the repository. Notice one of the issues on the project board has been automatically marked as closed.

<Frame>
  <img alt="The image shows a GitHub project board titled &#x22;Block Buster v2.0 Launch,&#x22; listing tasks with priorities, assignees, and statuses." />
</Frame>

That card moved from the “To do” column to “Done” without manual intervention — project automation handled the update. Let’s step through how this synchronization works.

Switching to the board view you can see the issue was moved to the Done column after it was closed in the repository’s Issues page.

<Frame>
  <img alt="The image shows a project management board on GitHub with columns for &#x22;Todo,&#x22; &#x22;In Progress,&#x22; and &#x22;Done,&#x22; displaying tasks with different priorities." />
</Frame>

## How project automation works

Project automation is implemented as workflows powered by GitHub Actions. Some workflows are enabled by default, while others are available but disabled. You can enable, disable, or edit workflows to control how your project reacts to board or repository events.

> **lightbulb** Project automation in GitHub Projects runs as workflows backed by [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions). These workflows can react to board status changes, issue opens/closes, pull request events, and other triggers — keeping the project board and repository in sync.

The project settings list several default workflows with clear behaviors. Common defaults include auto-adding child issues to a project, auto-closing issues when a card is marked Done, auto-archiving old items, and updating card status when an issue or PR is closed.

<Frame>
  <img alt="The image shows a GitHub project workflow interface with various workflow options listed on the left sidebar and a specific workflow titled &#x22;Auto-add sub-issues to project&#x22; displayed on the right." />
</Frame>

### Example: Auto-close issue workflow

The `Auto-close issue` workflow will close the associated issue in the repository when its project card status is changed to `Done`.

<Frame>
  <img alt="The image shows a GitHub interface displaying a workflow titled &#x22;Auto-close issue,&#x22; where the action is set to close the issue when the status is updated to &#x22;Done&#x22;." />
</Frame>

To demonstrate, I changed the status of the “Create a new Laser power-up” card from To do to Done on the project board. That action triggered the workflow and automatically closed the issue in the repository.

Initially, the issue was open in the repository Issues page:

<Frame>
  <img alt="The image shows a GitHub issues page for the repository &#x22;block-buster&#x22; with open issues, including &#x22;Create a new Laser power up&#x22; labeled as an enhancement." />
</Frame>

After marking the card Done, the automation closed the issue. Refreshing the Issues page shows the item under closed issues. The reverse also works: the `Item closed` workflow updates a project card’s status to `Done` when the linked issue or pull request is closed.

You can edit any workflow to change the triggers and actions, or disable it if you prefer manual control. Other default workflows you may encounter (often disabled) include auto-archive items, code change request, and item reopen — each automating a different project behavior.

<Frame>
  <img alt="The image shows a GitHub Issues page for the repository &#x22;block-buster,&#x22; listing closed issues related to power-ups and performance, with labels like &#x22;documentation&#x22; and &#x22;enhancement.&#x22;" />
</Frame>

### Quick reference: Default project workflows

| Workflow name                    |                                          Typical behavior | Default state          |
| -------------------------------- | --------------------------------------------------------: | ---------------------- |
| `Auto-add sub-issues to project` |       Adds child issues to the same project automatically | Enabled / configurable |
| `Auto-close issue`               |          Closes linked issue when card is moved to `Done` | Often enabled          |
| `Item closed`                    | Sets the card status to `Done` when an issue/PR is closed | Often enabled          |
| `Auto-archive items`             |                   Archives stale cards after a set period | Often disabled         |
| `Item reopen`                    |   Reopens card status when corresponding issue/PR reopens | Often disabled         |

(States can vary by repository or organization; check your project settings to confirm.)

## Insights: charts and metrics for project health

The Insights section provides charts and metrics to help you monitor project progress over time. The default visualization is the Burn up chart, which shows the count of open vs. completed items across a chosen time range.

<Frame>
  <img alt="The image shows a GitHub Insights page with a &#x22;Burn up&#x22; chart, displaying project progress over time and options to view data over different time frames. The chart helps in identifying progress and trends for managing projects." />
</Frame>

By default the chart may display the last two weeks. The green line represents currently open items and the purple line represents closed items. You can adjust:

* Time range (last week, two weeks, month, custom)
* Data scope (issues, pull requests, or both)
* Visualization type (burn up, stacked column, x–y axis)
* Grouping (milestones, assignees, labels)

These options let you create custom charts that surface the metrics most important to your workflow.

<Frame>
  <img alt="The image shows a GitHub Insights graph displaying the progress of open and completed issues over a two-week period. The graph indicates a rise in both open and completed issues towards the end of April." />
</Frame>

Use Insights to identify trends (e.g., rising open items, burst of completions) and to refine workflows or team priorities. Combining automation and Insights gives you both control (via workflows) and visibility (via charts), enabling more predictable project delivery.

## Links and references

* [GitHub Projects documentation](https://docs.github.com/en/issues/organizing-your-work-with-project-boards)
* [GitHub Actions overview](https://learn.kodekloud.com/user/courses/github-actions)
* [Tracking project progress with Insights](https://docs.github.com/en/organizing-your-work-with-projects/working-with-projects/viewing-insights)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/d8a59370-f849-4e53-b53b-04e6d1b8a67d)
