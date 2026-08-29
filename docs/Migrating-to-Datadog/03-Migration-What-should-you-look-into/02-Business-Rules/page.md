# Business Rules

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-What-should-you-look-into/Business-Rules/page

Guidance and business rules for planning and auditing a safe migration from Prometheus monitoring to Datadog, preserving alerts, metrics, cost control, and validation steps.

This lesson explains the core business rules and planning considerations when migrating monitoring from Prometheus to Datadog. It focuses on what to audit, how to preserve critical alerting and metric coverage, and how to avoid cost or performance surprises in Datadog. This is less about low-level implementation and more about planning and risk mitigation for a safe migration.

Prometheus is often the central piece of an observability stack because it collects both built-in and custom application metrics (for example, via Spring Boot Actuator). Audit Prometheus early so you can safely decommission it later—review configuration, scrape targets, metric filtering, and alerting rules that depend on those metrics.

<Callout icon="lightbulb">
  Audit Prometheus before deactivating it: verify alerts, scrape targets and paths, and any metric filtering to ensure Datadog will provide equivalent coverage.
</Callout>

## Key Prometheus items to verify before migrating

Start with a focused audit of Prometheus to capture everything you'll need to reproduce monitoring and alerting behavior in Datadog.

| Area                          | What to check                                                                                                              | Why it matters                                                                                                 |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Alerts (Alertmanager)         | Review alert rule expressions, thresholds, and severity. Inspect Alertmanager configuration (routes, receivers, silences). | Ensures critical alerts are retained, notification logic is replicated, and incident routing behaves the same. |
| Scraping endpoints            | Inventory `scrape_configs`, targets, and each job's `metrics_path` (note apps that expose non-standard endpoints).         | Missing endpoints cause blind spots; custom paths must be configured in Datadog or the app.                    |
| Metric filtering & relabeling | Document `metric_relabel_configs` / `relabel_configs` used to drop, rename, or change labels.                              | Prevents importing noisy or high-cardinality metrics and preserves intended metric names/tags.                 |
| Custom metrics                | List metric names, label/tag sets, and cardinality estimates. Capture how each metric is generated and used.               | Guides decisions on Datadog ingestion method (custom metrics, DogStatsD, SDKs) and cost/scale planning.        |

* Alerts from Alertmanager
  * Check alert rule expressions and thresholds. Make sure you understand which alerts are critical and why.
  * Inspect Alertmanager configuration (routes, receivers, and silences) so you can replicate notification logic in Datadog.
* Scraping endpoints
  * Identify all scrape targets and the `metrics_path` used by each job. Some applications expose metrics on custom endpoints that are not the default `/metrics`.
  * Note any service discovery or static configurations used by `scrape_configs`.
* Metrics filter
  * See whether Prometheus uses `metric_relabel_configs` or `relabel_configs` to drop or rename metrics. This prevents ingesting noisy or high-cardinality metrics that are not needed.
  * Document any metric transformations so you can apply similar filtering in Datadog or during ingestion.

<Frame>
  <img alt="The image is a diagram of a Prometheus setup for migration, highlighting three key components: Alerts from AlertManager, Scraping Endpoints, and Metrics Filter. Each section provides a brief description of its function, such as configuring alerts, defining endpoints, and filtering metrics." />
</Frame>

<Callout icon="warning">
  Do not decommission Prometheus until you have validated parity in Datadog: test dashboards, alerting behavior, and run a parallel ingestion period to compare metrics and alerts.
</Callout>

Those are the essential Prometheus checkpoints—capture them in a migration runbook to avoid unexpected gaps in monitoring.

## Datadog planning concerns

When mapping Prometheus concepts into Datadog, plan for ingestion method, cost, and operational practices. The following table summarizes common Datadog-focused items and practical actions to take.

| Concern              | Action                                                                                                 | Notes                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Custom metrics       | Inventory metrics and choose ingestion path: Datadog custom metrics, DogStatsD, or language SDKs.      | Consider metric naming conventions and tag schemas mapped from Prometheus labels.                            |
| Log-based metrics    | Use sparingly; prefer direct metric ingestion where possible.                                          | Log-based metrics can be fragile and expensive when log formats change. See Datadog docs for best practices. |
| Dashboards & queries | Translate PromQL queries into Datadog queries; simplify dashboards and avoid high-cardinality queries. | Optimize queries for performance and cost; test equivalent visualizations in Datadog.                        |
| Cost control         | Limit collection to required metrics, reduce cardinality, and tune retention.                          | Monitor ingestion rates and set alerting on cost/volume anomalies.                                           |
| Access control       | Implement RBAC, use API and application keys appropriately, and limit privileges.                      | Follow Datadog API key best practices to protect data and control usage.                                     |

* Custom metrics
  * Inventory all custom metrics currently sent to Prometheus. For each metric, capture its name, labels/tags, cardinality, and purpose. This helps decide how to re-ingest them into Datadog (custom metrics, `DogStatsD`, or direct SDKs).
* Log-based metrics
  * Use log-based metrics sparingly. They are convenient but can be expensive and fragile because log formats and fields change frequently. See Datadog's log-based metrics documentation for details.
* Dashboards and queries
  * Keep dashboards simple and queries efficient. Translate Prometheus queries into Datadog equivalents and avoid overly complex, high-cardinality queries that increase cost and reduce performance.
* Cost control
  * Limit collection to required data only. Reduce metric cardinality, tune retention, and avoid unnecessary high-volume ingest to control costs.
* Access control
  * Implement Role-Based Access Control (RBAC). Use Datadog API keys and application keys appropriately, and structure IAM so users have the access they need without excessive privileges. Refer to Datadog's API and application keys docs for best practices: `https://docs.datadoghq.com/account_management/api-app-keys/`

<Frame>
  <img alt="The image outlines concerns related to Datadog, focusing on custom metrics, performance, cost, and access control, each with brief descriptions and icons." />
</Frame>

## Recommended migration workflow (high level)

1. Audit Prometheus (alerts, scrape targets, relabeling, custom metrics).
2. Map metrics and alerts to Datadog equivalents; document transformations and tag mappings.
3. Set up Datadog ingestion and replicate a subset of alerts and dashboards.
4. Run both systems in parallel and compare results for a validation period.
5. Adjust metric filters, dashboards, and alert thresholds in Datadog as needed.
6. Decommission Prometheus only after validation and stakeholder sign-off.

## Links and references

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Alertmanager: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)
* Spring Boot Actuator: [https://docs.spring.io/spring-[SECRET_REDACTED].html](https://docs.spring.io/spring-[SECRET_REDACTED].html)
* Datadog docs: [https://docs.datadoghq.com/](https://docs.datadoghq.com/)
* Datadog DogStatsD: [https://docs.datadoghq.com/developers/dogstatsd/](https://docs.datadoghq.com/developers/dogstatsd/)
* Datadog API & application keys: [https://docs.datadoghq.com/account\_management/api-app-keys/](https://docs.datadoghq.com/account_management/api-app-keys/)

That's it for this lesson. I hope you found the checklist and planning guidance helpful for a safe Prometheus to Datadog migration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/d7aaa833-22da-4f94-af5c-5d196f04ab31/lesson/f3291bd4-ca3a-4ef2-86e4-8d8ab2061865" />
</CardGroup>
