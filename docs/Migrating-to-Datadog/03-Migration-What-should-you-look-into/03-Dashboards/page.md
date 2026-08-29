# Dashboards

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Dashboards/page

Guidance on migrating, designing, and managing observability dashboards in Datadog to preserve visibility, improve performance, and enable collaboration

In this lesson we cover dashboards: what they are, why they matter for observability, and practical guidance for migrating and designing dashboards—especially when moving to Datadog.

Dashboards are a core component of any observability strategy. They translate raw telemetry into visual insights that help teams spot anomalies, investigate incidents, monitor SLAs, and make data-driven business decisions. During migration, the single non-negotiable requirement is: preserve full visibility. Manually recreating dashboards risks omitting panels, queries, template variables, or configuration details that engineering and business teams depend on. A reliable migration guarantees every metric, log view, and visualization used for decision-making is preserved in the new platform.

<Callout icon="lightbulb">
  When planning a dashboard migration, treat dashboards as code: export, version, and validate visualizations before decommissioning legacy views. This reduces risk and ensures parity between old and new dashboards.
</Callout>

## Dashboard migration: high-level workflow

Follow a repeatable process to ensure visibility is preserved and stakeholders remain informed.

| Step                             | Goal                                      | Key actions                                                                                                               |
| -------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1. Export all dashboard data     | Capture exact visualizations and metadata | Export dashboards using the platform's JSON/YAML export (panels, queries, variables, layout, permissions).                |
| 2. Structure and organize panels | Make dashboards discoverable and reusable | Group related panels, use consistent naming and template variables, and create focused dashboards for specific use cases. |
| 3. Communicate and activate      | Minimize disruption to teams              | Announce new dashboards, provide migration links, and only deactivate old dashboards after confirmation.                  |

Below we expand each step and include practical design and performance guidance.

### 1) Export all dashboard data

Most observability platforms (including Datadog) offer an export mechanism—usually JSON or YAML. Exporting captures panels, queries, template variables, layout, display options, and other metadata. Keep these exports in version control so you can:

* Compare before/after states.
* Recreate dashboards programmatically.
* Audit changes during the migration.

Recommended checklist:

* Export each dashboard JSON/YAML.
* Verify template variables and linked queries are present.
* Record dashboard ownership and permissions.

### 2) Structure and organize panels

Recreate dashboards so they are easy to navigate and maintain.

* Group related visualizations into logical sections (e.g., latency, errors, throughput).
* Use collapsible groups inside dashboards to reduce visual noise.
* Standardize naming, descriptions, and template variables to make dashboards discoverable.
* Favor several focused dashboards over one monolithic dashboard that tries to show everything.

Benefits:

* Faster troubleshooting (teams find relevant panels quickly).
* Easier reuse of panels by other teams.
* Better performance and maintainability.

<Frame>
  <img alt="The image depicts a layered structure for &#x22;Efficient Dashboard Design in Datadog,&#x22; with categories like Metric, Log, Infrastructure, and Errors inside nested sections labeled Panel, Group, and Dashboard." />
</Frame>

### Performance considerations

Dashboard performance directly impacts incident response and user experience. Avoid placing too many heavy queries, high-cardinality or long time-range queries across dozens of visible panels. Use template variables and collapsed groups to limit the number of simultaneous queries.

Tips to improve load time:

* Limit query time ranges for default views.
* Use aggregations and rollups where possible.
* Collapse rarely used groups or move them to separate dashboards.
* Cache or snapshot expensive queries if platform supports it.

<Callout icon="warning">
  Avoid placing too many high-cardinality or long-time-range queries across dozens of visible panels. Keep dashboards focused and use groups/templates to reduce rendering cost and query load.
</Callout>

## Collaboration and discoverability in Datadog

Datadog supports scale-focused features to help teams share and manage dashboards:

* Dashboard lists: curate related dashboards for teams or functions.
* Sharing and permissions: grant access so teams can reuse panels and iterate faster.
* Copyable panels and groups: speed up adoption and standardization across teams.

The diagram below shows how shared dashboards accelerate troubleshooting and platform visibility across engineering, ops, and stakeholders.

<Frame>
  <img alt="The image shows a diagram illustrating collaborative dashboards, with Team A, Team B, and OPS using a centralized dashboard for troubleshooting and monitoring systems." />
</Frame>

Benefits of shared dashboards:

* Engineering teams get faster debugging paths.
* Centralized operations monitor across environments.
* Stakeholders receive consistent, reliable KPIs.

## What dashboards enable

By converting telemetry into clear dashboards:

* Business teams make better data-driven decisions.
* Managers and executives review KPIs more effectively.
* Operations and SREs detect and act on incidents faster.

## Scheduled reports and automated delivery

Include scheduled reports as part of your visibility strategy. Reports automate delivery of key views and summaries—common examples include incident counts, recent production deployments, and cost overviews. Reports can be delivered as emails, images/snapshots, or sent to collaboration tools and distribution lists.

<Frame>
  <img alt="The image is a diagram showing the most common uses of reports, which include the number of incidents, costs, and deployments made into production." />
</Frame>

Typical report flow:

1. Query or summarize data (metrics, logs, traces).
2. Generate an output (email body, image snapshot, PDF).
3. Deliver to stakeholders or target groups determined by the platform.

Use cases for scheduled reports:

* Weekly incident summaries for engineering managers.
* Daily cost reports for finance/ops.
* Post-deployment health summaries for product owners.

## Best practices checklist

| Area          | Best practice                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| Export        | Save dashboard JSON/YAML into version control and tag exports by date/owner.                            |
| Design        | Build focused dashboards, use template variables, and group related panels.                             |
| Performance   | Limit concurrent heavy queries, use rollups, and collapse groups.                                       |
| Governance    | Standardize naming/description, assign owners, and maintain access controls.                            |
| Communication | Announce new dashboards, run onboarding sessions, and deprecate old dashboards only after confirmation. |

## Resources

* Datadog Dashboards: [https://docs.datadoghq.com/dashboards/](https://docs.datadoghq.com/dashboards/)
* Observability best practices: [https://www.oreilly.com/library/view/observability-by-example/](https://www.oreilly.com/library/view/observability-by-example/)

That's it for this lesson. I hope you found it helpful.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/7e5a48dd-ddf8-45c5-b798-0f5aedff31f1" />
</CardGroup>
