# All files under /docs/ are owned by the docs team
/docs/ @my-org/docs-team

# All Python files anywhere are owned by the python team
*.py @my-org/python-team

# A specific file owned by an individual
/scripts/deploy.sh @alice
```

Why `CODEOWNERS` matters:

* Reduces reviewer fatigue by routing reviews to the right experts
* Ensures specialized areas (security, infra, APIs) always receive appropriate oversight
* Integrates with branch protection to require owners’ approvals automatically

## 3) Required reviewers

Requiring reviewers makes code review a blocking policy: a pull request cannot be merged until the required approvals are provided. This helps share knowledge across the team and prevents a single developer from bypassing review controls.

Branch protection rules can be configured to:

* Require one or more approving reviews
* Dismiss stale reviews when new commits are pushed
* Enforce that reviews come from `CODEOWNERS` when enabled

<Frame>
  <img alt="The image is a table describing features related to code management: Branch Protections, CODEOWNERS, and Required Reviewers, each with its technical purpose and key benefits." />
</Frame>

> **lightbulb** Enable "Require pull request reviews before merging" and, if you use CODEOWNERS, also enable "Require review from Code Owners" in branch protection rules to ensure owners are automatically requested and their approvals enforced.

## Recommended branch protection settings

| Setting                                       | Purpose                                                    |
| --------------------------------------------- | ---------------------------------------------------------- |
| Require pull requests before merging          | Prevents direct pushes and forces merges to go through PRs |
| Require status checks to pass                 | Gate merges on CI/CD and other automated checks            |
| Require a minimum number of approving reviews | Ensure multiple eyes on changes                            |
| Require review from CODEOWNERS                | Force owner approvals for designated file areas            |
| Dismiss stale pull request approvals          | Require re-review after new commits are added              |
| Restrict who can push or merge                | Limit merge rights to specific users or teams              |
| Lock the branch                               | Prevent deletion and block force pushes                    |

Applying these governance controls ensures that changes are reviewed, tested, and auditable before reaching production branches. Combined, branch protections, CODEOWNERS, and required reviewers create a "trust but verify" culture that enables teams to move quickly while maintaining code quality and an auditable history.

## Links and references

* [Protecting branches - GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/about-protected-branches)
* [CODEOWNERS - GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
* [Pull request reviews - GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/42ae61a8-fcc4-43d7-9ad9-523659e89b28)


# Comparing Projects and Projects Classic

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/Comparing-Projects-and-Projects-Classic/page

Comparison of Projects Classic and modern GitHub Projects highlighting custom fields flexible views built-in analytics and advanced automation for data driven project management

This lesson explains the key differences between Projects (Classic) and the modern GitHub Projects. The shift from Projects (Classic) to the modern GitHub Projects moves teams from simple, task-oriented boards to a data-driven project management platform that supports flexible views, richer metadata, automation, and analytics.

Below is a concise comparison to help you quickly understand where each approach shines.

| Area         | Projects (Classic)                                                     | GitHub Projects (Modern)                                                                                                          |
| ------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Layouts      | Basic Kanban-style boards with fixed columns and manual drag-and-drop. | Multiple views (table, board, roadmap) plus draft issues and real-time presence indicators for collaborators.                     |
| Data model   | Fixed columns and cards with limited metadata per card.                | Custom fields (text, number, date, etc.), iteration fields for sprints, integrated PR tracking, and richer item metadata.         |
| Organization | Manual organization; fixed column structures.                          | Dynamic sorting, ranking, and grouping by any custom field or metadata for multiple perspectives on the same dataset.             |
| Analytics    | Simple progress indicators only.                                       | Built-in insights with custom bar, line, and area charts and aggregation options (sum, average) to visualize velocity and health. |
| Automation   | Basic column-movement presets.                                         | Advanced automation through APIs, Actions, and webhooks for event-driven workflows and external integrations.                     |

Layouts

* Projects (Classic): Limited to fixed Kanban columns; items are moved manually and views are single-purpose.
* GitHub Projects (Modern): Supports table, board, and roadmap views so you can choose the visualization that fits your workflow. Modern Projects also support draft issues to capture early ideas and display user presence so collaborators can see who’s viewing or editing a project in real time.

Data model

* Projects (Classic): Uses a simple, fixed model of columns and cards with small amounts of per-card metadata.
* GitHub Projects (Modern): Uses flexible custom fields (text, number, date, select), plus a dedicated iteration field to manage sprints or cycles with flexible date ranges. Items can connect to pull requests, issues, and more rich metadata to support reporting and automation.

Organization

* Projects (Classic): Organization is mostly manual and constrained by column layout.
* GitHub Projects (Modern): Offers instant sorting, ranking, and grouping by any custom field or metadata so you can create multiple live perspectives (for example by assignee, priority, or sprint).

Analytics

* Projects (Classic): Only basic progress metrics are available.
* GitHub Projects (Modern): Includes an insights layer for custom charts (bar, line, area) with aggregation modes (sum, average, count) so teams can track velocity, throughput, and project health.

The last one is about automation. The classic project offers basic column movement presets, whereas the modern project

<Frame>
  <img alt="The image is a comparison chart between &#x22;Projects (Classic)&#x22; and &#x22;GitHub Projects (Modern)&#x22; detailing features like layouts, data models, organization, analytics, and automation. GitHub Projects (Modern) offers more advanced features compared to the Classic version." />
</Frame>

features extensive automation via the [GraphQL API](https://docs.github.com/en/graphql), [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions), and [webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks). With these integrations you can:

* Automatically add or move items based on labels, milestones, or custom field values.
* Trigger project updates from CI/CD events, pull request merges, or external systems.
* Build event-based workflows that update status, populate fields, or notify stakeholders without manual steps.

> **lightbulb** Modern GitHub Projects turn work into structured data. That data enables flexible views, powerful reporting, and automation that scales across repositories and teams.

Summary
Migrating to modern GitHub Projects gives teams a more powerful, flexible, and data-driven way to plan, track, and automate work. The modern experience adds custom fields, richer metadata, multiple views, integrated analytics, and robust automation—enabling deeper insights, multiple perspectives on the same work items, and integrations that support scalable, cross-repository workflows.

Links and references

* [GraphQL API Documentation](https://docs.github.com/en/graphql)
* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Webhooks and Events](https://docs.github.com/en/developers/webhooks-and-events/webhooks)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/29bed77c-9fa7-4118-a261-af44216935a7)
