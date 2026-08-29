# Layout Options For Projects

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/Layout-Options-For-Projects/page

Overview of three synchronized GitHub Projects layouts—Table for bulk data management, Board for workflow tracking, and Roadmap for timeline planning with guidance on when to use each.

In this lesson we review the three primary, dynamic layout options available in GitHub Projects. Each view offers a distinct perspective—data, process, or time—but they are connected: updates in one view sync across the others in real time. Choose the layout that matches the work you’re doing (data entry, workflow tracking, or timeline planning) and switch as needed.

> **lightbulb** These three layouts — Table, Board, and Roadmap — are complementary. Use the view that fits your current task and switch when necessary; all changes remain synchronized across views so your project data stays consistent.

## Table view (data-centric)

The Table view provides a spreadsheet-like interface for managing large volumes of issues and pull requests. It’s optimized for high-density data management, bulk editing, and detailed analysis.

Key uses:

* Rapid data entry and bulk updates across many items
* Sorting, filtering, and grouping by custom fields (priority, estimate, team, etc.)
* Viewing all project metadata in rows and columns for easy reporting

Tips:

* Use filters and saved views to focus on specific slices of work (e.g., by team or priority).
* Leverage custom fields to surface the exact columns you need for status reporting.

<Frame>
  <img alt="The image shows a project management interface titled &#x22;Solar System Project&#x22; with task details, assignees, status, priority, and progress. There is also a sidebar menu for adjusting table views and sorting options." />
</Frame>

## Board view (process-centric)

The Board view presents a Kanban-style layout to track the movement of work through your workflow. It’s ideal for day-to-day progress monitoring and for visualizing the status of individual items.

Best for:

* Managing work-in-progress and identifying bottlenecks
* Moving cards between columns (Backlog, In Progress, Done) to reflect current state
* Customizing columns, fields, and filters; creating swimlanes by grouping cards into rows

From a practical standpoint, the Board view improves team visibility into bottlenecks, helps balance work in progress, and supports a steady flow by modeling customizable lifecycle stages.

<Frame>
  <img alt="The image displays a digital task board with sections like &#x22;Todo,&#x22; &#x22;In Progress,&#x22; and &#x22;Done,&#x22; along with options for sorting and organizing tasks by fields such as status and assignees." />
</Frame>

## Roadmap view (time-centric)

The Roadmap view shows a timeline of milestones and deliverables, mapping start and target (or due) dates across a horizontal calendar. Use this layout for long-term planning and communicating schedule progress to stakeholders.

When to use it:

* Planning releases and tracking deadlines
* Visualizing task duration and sequencing across weeks or months
* Detecting scheduling conflicts and aligning development velocity with upcoming milestones

From a technical perspective, the Roadmap view helps teams detect schedule collisions early and coordinate across teams by visualizing how work items overlap over time.

<Frame>
  <img alt="The image shows a &#x22;Roadmap View&#x22; interface with filtering and sorting options on the left, and a timeline of tasks or issues on the right, dated from January to February 2026." />
</Frame>

## Quick comparison

| Layout  | Best for                                    | Key features                                                           |
| ------- | ------------------------------------------- | ---------------------------------------------------------------------- |
| Table   | Bulk data management and detailed reporting | Sort, group, filter, bulk edit columns and custom fields               |
| Board   | Workflow tracking and WIP management        | Kanban columns, drag-and-drop cards, customizable fields and swimlanes |
| Roadmap | Timeline planning and release coordination  | Horizontal timeline, start/target dates, milestone alignment           |

## How teams combine views

* Use Table for intake and bulk edits (triage, labeling, estimates).
* Use Board to manage daily work and enforce workflow policies.
* Use Roadmap for release planning, stakeholder updates, and dependency visualization.

All views access the same underlying issues and pull requests, so edits made in one view update the others instantly.

## Links and references

* [GitHub Projects documentation](https://docs.github.com/en/issues/organizing-your-work-with-projects)
* [Managing work with issues and pull requests](https://docs.github.com/en/issues)

> **lightbulb** Tip: Create saved views and templates for recurring workflows (e.g., sprint planning, release triage) to reduce setup time and ensure consistency across your team.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/6b1f91eb-f697-4d70-b254-bc249ff98098)
