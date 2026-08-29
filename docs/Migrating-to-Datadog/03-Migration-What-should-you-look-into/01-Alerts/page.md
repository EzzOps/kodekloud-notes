# datadog.yaml
logs_enabled: true
log_level: INFO
```

Key settings:

* `logs_enabled`: enable or disable the Agent’s log collection.
* `log_level`: recommended `INFO` for production; use `DEBUG` only for short-lived troubleshooting.

Tip: Manage Agent config changes via your configuration management (Git, CI/CD) and document why any non-default settings are used.

## Log collection, filtering, and masking

Collect only the logs you need and apply processing as close to the source as possible. The Agent supports local processing rules, and Datadog provides server-side log pipelines and dedicated masking/redaction processors—prefer server-side when possible.

Best practices:

* Scope file paths and services narrowly (avoid wildcards that capture unrelated logs).
* Exclude noisy endpoints (health checks, probes) before ingestion.
* Mask or redact PII and secrets as early as possible, ideally in a controlled pipeline.
* Test any regex-based exclusions or redactions in staging to avoid losing important data.

Example per-integration Agent log configuration (`conf.d/<integration>.d/conf.yaml`):

```yaml theme={null}
# conf.d/myapp.d/conf.yaml
logs:
  - type: file
    path: /var/log/myapp/*.log
    service: myapp
    source: myapp
    tags:
      - env:prod
    log_processing_rules:
      - type: exclude_at_match
        name: exclude_healthchecks
        pattern: '^(GET|HEAD) /health'
      - type: multi_line
        name: new_log_start_with_date
        pattern: '^\d{4}-\d{2}-\d{2}'
```

Notes:

* `exclude_at_match` prevents known noisy lines from being forwarded.
* `multi_line` preserves stack traces and multiline exceptions.
* Verify that the Agent version you use supports the processors you plan to run locally. See the Agent logs documentation for supported processors and syntax.

> **warning** Avoid broad regex-based exclusions or redactions that can remove useful diagnostic data. Always validate processing rules in a staging environment and review their effects on a representative sample of logs.

## Metrics scraping and cardinality control

Unrestricted metric collection and high-cardinality tags are common drivers of cost. Apply strict controls on which metrics and tags are collected.

Recommendations:

* Enable only the integrations and checks you actively use.
* Avoid high-cardinality tags (unique IDs, user IDs, request IDs).
* Normalize tags to coarse-grained values such as `region`, `role`, or `service`.
* Use allowlists/deny-lists (where supported) to limit scraped metrics.

Example (Prometheus-style integration):

```yaml theme={null}
# conf.d/prometheus.d/conf.yaml (example)
instances:
  - prometheus_url: http://localhost:9100/metrics
    namespace: node
    # If supported by the check, prefer white-listing metrics:
    # metrics: ['node_cpu_seconds_total', 'node_memory_MemAvailable_bytes']
    tags:
      - env:prod
      - role:web
```

Do / Don’t summary:

| Action                                             | Recommended                                     |
| -------------------------------------------------- | ----------------------------------------------- |
| Add `instance-id` or `request-id` as a metric tag  | Don’t — high cardinality                        |
| Use `region`, `service`, `role` tags               | Do — low cardinality and useful for aggregation |
| Collect every Prometheus metric by default         | Don’t — use a whitelist where possible          |
| Aggregate or roll up metrics at source if feasible | Do — reduces downstream cardinality and cost    |

Periodic housekeeping:

* Review your metric catalog regularly and delete unused or noisy metrics.
* Use metric roll-ups or aggregates when raw metrics are not required for troubleshooting.

## Debugging and troubleshooting

When investigating issues, temporarily increase verbosity and enable additional integrations. Always revert these changes.

Temporary debug example:

```yaml theme={null}
# datadog.yaml (temporary change)
log_level: DEBUG
```

Guidelines:

* Restrict `DEBUG` to a short troubleshooting window.
* For logs, enable only the integration(s) generating the data you need.
* Revert settings and remove any temporary tag or metrics changes immediately after resolving the incident.

## Cost optimization checklist

Use this checklist to validate your configuration before wide deployment.

|  Category | Action                                                                                |
| --------: | ------------------------------------------------------------------------------------- |
|      Logs | Disable collection for unused services, scope file paths, and exclude noisy endpoints |
|   Privacy | Mask/redact PII and secrets in pipelines or at the Agent if necessary                 |
|   Metrics | Remove high-cardinality tags and whitelist important metrics                          |
| Retention | Configure indexing and retention policies to limit long-term storage                  |
|     Audit | Periodically review integration configs, dashboards, and alerts for stale data        |

## Links and references

* Datadog Logs Processing and Pipelines: [https://docs.datadoghq.com/logs/processing/pipelines/](https://docs.datadoghq.com/logs/processing/pipelines/)
* Datadog Logs Processors (masking/redaction): [https://docs.datadoghq.com/logs/processing/processors/](https://docs.datadoghq.com/logs/processing/processors/)
* Datadog Agent Logs documentation: [https://docs.datadoghq.com/agent/logs/](https://docs.datadoghq.com/agent/logs/)
* Prometheus metrics best practices: [https://prometheus.io/docs/practices/naming/](https://prometheus.io/docs/practices/naming/)

## Final notes

Make all filters and rules explicit, incremental, and reversible. Conservative collection combined with deliberate, documented exceptions delivers observability that is more actionable, secure, and cost-effective.

That’s a concise overview of Agent-level tuning for efficient Datadog usage. Implement these steps iteratively and validate their effects on both observability and billing before rolling them out broadly.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/fd555480-82df-40f4-b8ad-2ea920d51077/lesson/fb698905-9310-4fe0-b2c7-703f3859fab7)


# Alerts

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Alerts/page

Guidance on migrating, testing, and managing monitoring alerts to ensure telemetry availability, reduce noise, and validate notifications when moving to Datadog or replacing legacy alerting systems.

Alerts make monitoring manageable by continuously evaluating telemetry (metrics, logs, traces) and notifying the right teams when predefined conditions are met. Proper alerting reduces mean time to detection and enables controlled responses instead of frantic firefights.

What alerts do, in short:

* Continuously evaluate telemetry.
* Fire when a configured condition or threshold is met.
* Deliver notifications to your teams or channels so they can take action.

A concrete example

Your company processes payroll for multiple businesses. Payments execute at 1 a.m. on the last day of every month. If payroll jobs fail or are delayed, employees will likely contact support en masse. Without proactive alerting, you’ll wake up to dozens (or hundreds) of complaints and have to scramble to diagnose and remediate.

An alert that detects failed or delayed payroll jobs would notify the on-call team immediately, enabling a controlled investigation and remediation before employee outreach escalates.

<Frame>
  <img alt="The image shows a person sitting at a desk, working on a computer displaying bug icons, with a caption about alerts handling issues." />
</Frame>

Use alerts to catch performance regressions early

Alerts aren’t only for failures. Track application latency, error rates, throughput, or resource saturation so you can detect regressions before customers notice. For example, a latency alert that triggers when p95 response time increases beyond a threshold lets you investigate before SLA breaches occur.

<Frame>
  <img alt="The image illustrates a scenario where two people are discussing issues with a computer, emphasizing the importance of alerts in identifying latency problems before customers complain." />
</Frame>

Alert migration: a recommended sequence

When migrating alerts into a new monitoring system (for example, migrating to Datadog), follow a repeatable, low-risk sequence:

1. Ensure required data is available
   * Confirm collection of metrics, logs, and traces for the services you want to monitor.
   * Request any necessary changes to the Datadog Agent configuration from your DevOps/infra team: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)

2. Confirm access to the monitoring console
   * Verify your team has permissions to create and manage monitors in Datadog: [https://docs.datadoghq.com/monitors/](https://docs.datadoghq.com/monitors/)

3. Validate notification targets
   * Ensure recipients (email groups, PagerDuty services, Slack channels, Microsoft Teams, etc.) are configured and reachable.

4. Test alerts
   * Simulate conditions or temporarily lower thresholds to confirm monitors fire and notifications are delivered.

5. Deactivate legacy alerts
   * After Datadog monitors are validated in production, disable the old alerts in Grafana, Alertmanager, Dynatrace, or other tools you’re replacing.

<Frame>
  <img alt="The image shows a flowchart outlining the steps for alert migration, which include listing data, accessing Datadog, verifying targets, testing alert rules, and deactivating legacy alerts." />
</Frame>

Migration checklist (summary)

| Step                     | Purpose                                          | Example / Link                                                                                 |
| ------------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Ensure telemetry         | Make sure metrics/logs/traces exist for services | Datadog Agent docs: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)     |
| Console access           | Grant permissions to create/manage monitors      | Datadog Monitors: [https://docs.datadoghq.com/monitors/](https://docs.datadoghq.com/monitors/) |
| Notification targets     | Validate recipients and routing                  | PagerDuty, Slack, Teams, email groups                                                          |
| Test alerts              | Verify firing and delivery                       | Simulate incidents or lower thresholds                                                         |
| Deactivate legacy alerts | Avoid duplicate notifications once validated     | Grafana, Alertmanager, Dynatrace                                                               |

Common alert notification integrations

* Datadog mobile app
* Jira
* PagerDuty
* Slack
* Microsoft Teams
* ServiceNow

Best practices and tips

> **lightbulb** Tune thresholds and use multi-condition monitors to reduce noise. Prefer cloud-native integrations (PagerDuty, Slack) for reliable on-call routing, and run repeatable tests for each alert before decommissioning legacy monitors.

When you disable legacy alerts, keep them active until you have validated the new monitors in production and verified notifications reach the intended recipients. Accidentally deactivating early can blind you to outages.

> **warning** When disabling legacy alerts, keep them enabled until Datadog monitors are fully validated in production. Accidentally deactivating alerts too early can leave you blind to outages.

Further reading and references

* Datadog Agent: [https://docs.datadoghq.com/agent/](https://docs.datadoghq.com/agent/)
* Datadog Monitors: [https://docs.datadoghq.com/monitors/](https://docs.datadoghq.com/monitors/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Prometheus Alertmanager: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)
* Dynatrace: [https://www.dynatrace.com/](https://www.dynatrace.com/)
* PagerDuty: [https://www.pagerduty.com/](https://www.pagerduty.com/)
* Slack: [https://slack.com/](https://slack.com/)
* Microsoft Teams: [https://www.microsoft.com/en-us/microsoft-teams/group-chat-software](https://www.microsoft.com/en-us/microsoft-teams/group-chat-software)
* ServiceNow: [https://www.servicenow.com/](https://www.servicenow.com/)

That’s it for this lesson—use the migration checklist, validate thoroughly, and iterate to keep alerting effective and actionable.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/584aa954-f0c2-4747-a570-8204b915d0ab)
