# Cloud Monitoring

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Cloud-Observability/Cloud-Monitoring/page

Overview of Google Cloud Monitoring, covering telemetry sources, agents, dashboards, alerts, custom metrics, and integration with logging and tracing for observability and troubleshooting.

Welcome back.

In this lesson we explore Cloud Monitoring — Google Cloud’s observability control room. You’ll learn where telemetry comes from, how it flows into Cloud Operations, which agents to use, and the key features that help you monitor, visualize, and troubleshoot systems and applications.

## What is Cloud Monitoring?

Cloud Monitoring provides visibility into the health and performance of your infrastructure and applications. It collects metrics, surfaces them in dashboards, triggers alerts, and links to logs and traces so you can quickly find root causes when something goes wrong. Use it to:

* Monitor system and application health across Google Cloud, hybrid, and multi‑cloud environments.
* Build dashboards and charts to visualize trends and anomalies.
* Configure alerting policies and notification channels to detect and respond to incidents.
* Connect metric spikes to logs and traces for fast troubleshooting.

## Where telemetry comes from

Cloud Monitoring receives telemetry from several sources:

* Google Cloud services (Compute Engine, GKE, Cloud SQL, VPC, etc.)
* Hybrid environments (on‑premises and AWS)
* Your applications (via client libraries and custom metrics)

On VM instances and other hosts, telemetry is collected by agents. The two primary agent options are:

* The Monitoring agent — collects system and application metrics and can be extended with plugins.
* The Ops Agent — a unified agent that collects both logs and metrics, and is the recommended choice for most workloads.

Both agents send metrics and logs to Cloud Monitoring and Cloud Logging. Traces come from instrumented applications (for example via OpenTelemetry or Cloud Trace client libraries) and are sent to Cloud Trace. Once ingested, you can create dashboards, alerting policies, and use Error Reporting and tracing tools to diagnose problems.

## Agents: Monitoring agent vs Ops Agent

| Agent            |                                                What it collects |                   Recommended?                  | Typical use case                                                |
| ---------------- | --------------------------------------------------------------: | :---------------------------------------------: | --------------------------------------------------------------- |
| Monitoring agent |         System and application metrics; extendable with plugins | Legacy; use if you need specific legacy plugins | Older workloads that require plugin-specific metrics            |
| Ops Agent        | Unified metrics and logs collection, fewer components to manage |   Yes — recommended for most modern workloads   | New deployments, simplified management and consistent telemetry |

See the official Ops Agent docs for installation and configuration details:

* [Ops Agent documentation](https://cloud.google.com/ops-agent)

## How telemetry flows (summary)

1. Infrastructure and applications generate metrics, logs, and traces.
2. Agents on hosts (Monitoring agent or Ops Agent) push metrics and logs to Google Cloud. Instrumented applications or tracer libraries send traces to Cloud Trace.
3. Cloud Operations ingests the data into Cloud Monitoring, Cloud Logging, and Cloud Trace.
4. Dashboards, alerts, Error Reporting, and trace analysis provide visibility and debugging paths.

## Key capabilities that make Cloud Monitoring powerful

* Unified metric collection across Google Cloud, AWS, and on‑prem systems.
* Real‑time dashboards: Use prebuilt or custom dashboards to visualize CPU, latency, error rate, throughput, and business KPIs.
* Alerting and uptime checks: Configure threshold-based alerts, notification channels, and synthetic checks to detect issues proactively.
* Service monitoring: Define SLIs (Service Level Indicators), SLOs (Service Level Objectives), and error budgets to measure and manage reliability.
* Integration with Cloud Logging and Cloud Trace: Jump from a metric spike to correlated logs and traces to speed up root-cause analysis.
* Custom metrics: Publish application-specific metrics (for example, `orders_processed_per_minute` or session durations) to monitor business-relevant signals.

<Frame>
  <img alt="A presentation slide titled &#x22;Cloud Monitoring.&#x22; It shows six feature boxes—Unified Metrics Collection, Real‑Time Dashboards, Alerting and Uptime Checks, Service Monitoring, Integration with Cloud Logging, and Custom Metrics—each with a brief description." />
</Frame>

## Custom metrics and instrumentation

Publish custom metrics from your applications using client libraries or the Cloud Monitoring API. Custom metrics let you measure business KPIs and application-specific signals not available as system metrics.

Example structure of a `timeSeries` payload you’d send to Cloud Monitoring (JSON example):

```json theme={null}
{
  "timeSeries": [
    {
      "metric": { "type": "custom.googleapis.com/my_metric" },
      "resource": { "type": "global", "labels": { "project_id": "my-project" } },
      "points": [
        {
          "interval": { "endTime": "2024-01-01T00:00:00Z" },
          "value": { "doubleValue": 3.14 }
        }
      ]
    }
  ]
}
```

Use official client libraries (Java, Python, Go, Node.js) or the REST API for production integration:

* [Cloud Monitoring client libraries](https://cloud.google.com/monitoring/docs/reference/libraries)

## Exam-focused summary (what to remember)

* Cloud Monitoring is part of the Cloud Operations suite, alongside Cloud Logging, Cloud Trace, and Error Reporting.
* Metrics vs logs:
  * Metrics are numeric measurements over time (e.g., CPU usage, request latency).
  * Logs are event records with detailed messages (e.g., container restart, error stacktrace).
* Service monitoring concepts: SLIs (what you measure), SLOs (targets for SLIs), and error budgets (tolerated unreliability).
* Alerts and notification channels: Know how to create alerting policies, configure notification channels, and route on-call duties.
* Integration: Cloud Monitoring and Cloud Logging complement each other — you can navigate from metric anomalies to correlated logs and traces for debugging.

> **lightbulb** Tip: For most modern workloads, prefer the Ops Agent because it unifies logs and metrics collection, simplifies management, and is the recommended agent for Cloud Monitoring and Cloud Logging.

## Links and references

* [Cloud Operations (Monitoring, Logging, Trace, Error Reporting)](https://cloud.google.com/products/operations)
* [Ops Agent documentation](https://cloud.google.com/ops-agent)
* [OpenTelemetry](https://opentelemetry.io/)
* [Cloud Trace documentation](https://cloud.google.com/trace)
* [Cloud Monitoring client libraries](https://cloud.google.com/monitoring/docs/reference/libraries)

That covers the essentials of Cloud Monitoring and how it fits into end-to-end observability. Further related topics will be covered in subsequent content.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/d6a06810-5ad4-420a-8025-4b368685733c/lesson/e65cd383-00d1-41f5-995c-2c9fe2a02d23)
