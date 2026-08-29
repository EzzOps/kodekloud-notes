# Data Visualization

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Data-Visualization/page

Guide to turning telemetry into actionable dashboards, alerts, and log-based metrics in Datadog, covering notebooks, anomaly detection, and best practices for visibility and cost control.

This lesson explains how to convert the telemetry you already collect — from infrastructure, instrumented applications, end-user experience, and security guardrails — into useful monitoring and observability surfaces. With Datadog as your ingestion layer, the goal is to turn raw signals into clarity and actionable insight.

## Dashboards

Dashboards are the central surface for presenting everything you need to know about your environment. They can visualize metrics, logs, traces, and profiles, often without requiring you to manipulate raw payloads directly. Use dashboards to:

* Transform data with functions and mathematical expressions.
* Aggregate and filter to present focused, role-specific views.
* Create log-based metrics and panels derived from log queries.
* Embed explanatory text, diagrams, and links for onboarding and runbooks.

When using logs as a source, craft and validate queries in `Live Tail` or the Logs Explorer before embedding them in dashboard panels so widgets render reliably. For onboarding and cross-team clarity, add panel descriptions, links to runbooks, and diagrams to reduce ramp-up time.

Datadog Powerpacks let you create templated collections of dashboards and panels that can be shared across teams. A Powerpack is a customizable template: after importing, users only supply environment-specific variables to populate panels and queries.

Notebooks complement dashboards by offering a narrative-friendly, formatted editor that mixes text, images, and live query cells. Notebooks are ideal for postmortems, runbooks, architecture notes, and design documents so operational knowledge remains discoverable during incidents and after-action reviews.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Data Visualization: Dashboards,&#x22; showing &#x22;Dashboards&#x22; connected to five categories: Manipulate data, Log-based telemetry, General instructions, Powerpacks, and Notebooks." />
</Frame>

Quick reference: dashboard widget guidance

| Widget type      | Best use case                             | Tip                                                               |
| ---------------- | ----------------------------------------- | ----------------------------------------------------------------- |
| Timeseries       | Application metrics, resource utilization | Use aggregation functions and math to normalize across hosts      |
| Heatmap          | Distribution and latency visibility       | Aggregate by percentile to reduce noise                           |
| Logs-based panel | Error rates, unique events                | Convert frequent queries into `log-based metrics` for performance |
| Top list / Table | Service ranking, top errors               | Add links to the originating traces or logs                       |
| Markdown / Image | On-call instructions, diagrams            | Include links to Notebooks or runbooks for context                |

## Alerts

Alerts notify you when conditions change and are the primary mechanism for driving action. Datadog supports:

* State-change alerts (thresholds, multi-condition).
* Anomaly detection and forecasting (ML-powered).
* Watchdog: automated ML-based monitoring that surfaces anomalous behavior without hand-crafted rules.

Use centralized views of triggered alerts and historical trends to analyze incidents and identify long-term improvements. Combine state-change alerts with anomaly detection to capture both known conditions and unusual patterns.

<Frame>
  <img alt="The image is a data visualization diagram showing alerts being used for &#x22;Change of state&#x22; and &#x22;Anomaly detection.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Use ML-powered anomaly detection (Watchdog) to catch unusual patterns you may not anticipate with static thresholds. Combine it with state-change alerts for clear, actionable notifications.
</Callout>

## Logs

Logs hold rich operational context and can feed dashboards, metrics, and alerts. Datadog logging features let you:

* Inspect live traffic with `Live Tail`.
* Search by fields, phrases, or numeric values in the Logs Explorer.
* Group and aggregate logs by common fields (for example: `endpoint`, `status_code`, `service`).
* Segregate logs into indexes to improve query performance, enforce retention, and manage access control.

Indexing improves performance for high-volume datasets and enables cost management through targeted retention policies.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Data Visualization: Logs&#x22; showing categories like &#x22;Advanced queries,&#x22; &#x22;Live tail,&#x22; &#x22;History,&#x22; and &#x22;Index,&#x22; all branching from &#x22;Logs.&#x22;" />
</Frame>

## Best Practices and Engineering Considerations

* Prefer precomputed or `log-based metrics` for frequently used time-series panels to reduce dashboard latency and cost.
* Describe panels: include intent, expected behavior, and links to runbooks or Notebooks so newcomers can act quickly.
* Guard against alert fatigue: tune thresholds, use multi-condition alerts, and periodically review alert value and signal-to-noise ratio.
* Investigate noisy signals at their root cause instead of adding superficial filters. Persistent noise often indicates engineering or design issues.
* Make every panel purposeful: dashboards should deliver visibility and actionable context, not just visual appeal.

<Callout icon="warning">
  Querying your entire log dataset directly from dashboard panels can lead to higher latencies and unexpected cost spikes. Prefer precomputed log-based metrics or indexed queries for high-traffic dashboards.
</Callout>

Creating dashboards and visualizations is both practical and creative. Focus on clarity, reuse, and actionability so your telemetry becomes a reliable decision-making surface for your teams.

That's it for this lesson. I hope you found it useful.

## Links and References

* Datadog Dashboards: [https://docs.datadoghq.com/dashboards/](https://docs.datadoghq.com/dashboards/)
* Datadog Logs: [https://docs.datadoghq.com/logs/](https://docs.datadoghq.com/logs/)
* Datadog Notebooks: [https://docs.datadoghq.com/notebooks/](https://docs.datadoghq.com/notebooks/)
* Datadog Watchdog & Anomaly Detection: [https://docs.datadoghq.com/monitors/monitor\_types/watchdog/](https://docs.datadoghq.com/monitors/monitor_types/watchdog/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/0771537c-cf42-466f-a605-4ec0c452fefc" />
</CardGroup>
