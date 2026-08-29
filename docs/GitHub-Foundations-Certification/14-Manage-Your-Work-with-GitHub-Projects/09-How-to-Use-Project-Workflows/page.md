# How to Use Project Workflows

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Manage-Your-Work-with-GitHub-Projects/How-to-Use-Project-Workflows/page

Guide to GitHub Projects workflows that automate assigning new issues and pull requests to a To do status and compare built-in, Actions, and GraphQL automation options

Project workflows let you automate routine project management tasks inside GitHub Projects. Choose the level of automation that fits your needs:

* Built-in workflows — Fast, no-code automations for common project tasks.
* [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions) — Highly customizable CI/CD and automation when you need conditional logic or custom scripts.
* [GraphQL API](https://docs.github.com/en/graphql) — Programmatic access for large-scale integrations and advanced automation.

Below is a concise comparison to help you pick the right approach.

| Automation Type    |                                                   Best for | Example                                                    |
| ------------------ | ---------------------------------------------------------: | ---------------------------------------------------------- |
| Built-in workflows |       Teams who want quick, no-code automation in Projects | Automatically move newly added items into a "To do" column |
| GitHub Actions     |       Complex or conditional automations with custom logic | Add an item to a project only when specific labels exist   |
| GraphQL API        | Large-scale programmatic integrations or custom dashboards | Bulk sync project state with an external tool              |

Project workflows reduce manual steps by automatically ingesting new issues and pull requests into your project board with consistent statuses — keeping your project board current and reducing administrative overhead.

What we’ll do: enable the "Item added to project" workflow so any new issue or pull request added to the project automatically receives the `To do` status.

The first step is to access the project menu.

<Frame>
  <img alt="The image shows a GitHub project workflow configuration for the &#x22;Item added to project&#x22; event, which sets the status to &#x22;Todo&#x22; when an item like an issue or pull request is added. It also includes a sidebar with other workflow options and a step guide on accessing the project menu." />
</Frame>

Steps to enable the workflow

1. Open your GitHub project and click the menu button in the top-right corner.
2. From the drop-down, select **Workflows** to open the project automation management interface.
3. In the Workflows sidebar, expand the default workflows group and click the **Item added to project** workflow — this trigger runs when an issue or pull request is added.
4. In the configuration panel, confirm the filters include both Issues and Pull Requests so every new item type triggers the automation.
5. Under the action settings:
   * Choose **Set value**.
   * Select the **Status** field.
   * Set the value to `To do` (this places all newly added items into the To do column).
6. If you need to modify the workflow, click **Edit** (top right), make your changes, then click **Save** and turn on the workflow to enable it.

<Callout icon="lightbulb">
  Make sure the filters include both Issues and Pull Requests if you want the automation to apply to both types. If you only include one type, items of the other type will not trigger the workflow.
</Callout>

<Frame>
  <img alt="The image shows steps to enable the &#x22;Item Added&#x22; workflow in a project management interface, alongside a screenshot of a workflow setup for adding an item to a project." />
</Frame>

After enabling the workflow

* Test by adding a new issue and a new pull request to confirm both are assigned the `To do` status.
* Revisit the Workflows UI to adjust filters or field values as your process evolves.
* Audit your workflow periodically to ensure it still aligns with team conventions or any new custom fields.

<Callout icon="warning">
  You must have appropriate project permissions (usually project admin or maintainer) to enable or edit project workflows. If you can’t access Workflows, request access from a project administrator.
</Callout>

Strategic benefits of using project workflows

* Consistency — Automatically place every new item into the initial phase so nothing is missed.
* Reduced overhead — Remove repetitive administrative work like dragging items between columns.
* Real-time accuracy — Keep project boards synchronized with repository activity, giving stakeholders an up-to-date view of progress.

<Frame>
  <img alt="The image is a diagram titled &#x22;Strategic Benefits,&#x22; highlighting three main points: Consistency, Reduced Overhead, and Real-Time Accuracy." />
</Frame>

Links and references

* [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions) — Create custom workflows when built-in automations aren’t enough.
* [GitHub GraphQL API](https://docs.github.com/en/graphql) — Programmatic access for advanced or large-scale automation.
* GitHub Projects Workflows — Configure and manage automations from the Project > Workflows UI.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/a8015214-1737-4c3f-b9a2-17cef4769a60/lesson/10dc4132-3e18-4b31-856c-a7bfcb1f9194" />
</CardGroup>
