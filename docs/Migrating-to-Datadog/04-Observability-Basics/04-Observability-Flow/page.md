# Observability Flow

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Observability-Basics/Observability-Flow/page

Describes telemetry flow from user requests through collection pipelines to monitoring backends, covering traces metrics logs and best practices for diagnosis and reliability

In this lesson we examine the observability flow — the end-to-end path telemetry takes from a user action through your distributed system to the monitoring backend — and why each stage matters for diagnosing issues and improving reliability and performance.

## Overview

When a user initiates a request (from mobile, web, or another client), multiple components collaborate to fulfill it. Each hop emits signals (logs, metrics, traces, events) that, when collected and correlated, answer operational and business questions such as:

* Why is the system slow?
* Why are customers abandoning carts?
* Which service or function causes a performance regression?
* Why do some services fail under load?

Understanding where telemetry is generated and how it flows helps you reduce MTTI/MTTR, control costs, and improve customer experience.

## User request journey and where telemetry is generated

Typical request flow:

* The user accesses the platform via a client.
* The request reaches an ingress layer or API gateway that may perform authentication, authorization, rate-limiting, and policy checks.
* The gateway forwards the request to one or more microservices that implement the business logic.
* Microservices may resolve the request directly or call downstream systems such as databases, caches, or message queues.
* Inside each service, methods and modules execute, performing reads/writes and invoking external APIs.

Every stage of this journey generates telemetry — traces (spans), metrics, logs, and events — which can be correlated to form an end-to-end picture of system behavior.

<Frame>
  <img alt="The image illustrates the importance of monitoring data, highlighting tasks like identifying system lag points, detecting why customers abandon shopping, analyzing downtime during high traffic, and fixing performance issues at the call level." />
</Frame>

## Telemetry types (what to collect and why)

| Telemetry type | What it is                                 | Primary use cases                                                |
| -------------: | ------------------------------------------ | ---------------------------------------------------------------- |
|         Traces | Distributed spans with timing and context  | Root-cause latency, end-to-end request flow, distributed tracing |
|        Metrics | Time-series numeric measurements           | Capacity planning, SLOs, alerts, trend analysis                  |
|           Logs | Structured or unstructured event records   | Forensics, debugging, audit trails                               |
|  Events/Alerts | Discrete notifications about state changes | Incident notifications, automated workflows                      |

Collecting the right combination of these signals allows teams to correlate symptoms (e.g., a spike in error rates) with causes (e.g., slow downstream DB queries) and business impact (e.g., checkout abandonment).

## Telemetry collection pipeline

A reliable, efficient collection pipeline is critical. A common pipeline consists of the following stages:

1. Instrumentation and collection
   * Applications emit telemetry via automatic instrumentation (language SDKs, middleware) or manual instrumentation (explicit API calls).
   * Use consistent context propagation and standardized formats (e.g., OpenTelemetry) to ensure traces can be reassembled.
2. Agent or collector
   * An agent or collector runs on the host, in a sidecar, or as a centralized service.
   * Collection models include push (apps send telemetry) and pull (the collector scrapes endpoints such as Prometheus exporters).
3. Local processing
   * Agents/collectors perform batching, buffering, sampling, aggregation, enrichment (adding metadata/tags), and filtering to reduce noise and manage cost.
   * Make processing rules configurable per component/environment.
4. Export to backend
   * Processed telemetry is exported securely to the monitoring backend using retries, backoff, compression, and encryption.
5. Storage and visualization
   * The backend stores telemetry for a configured retention period and provides querying, alerting, and visualization to turn signals into action.

The following diagram illustrates systems interacting with a monitoring agent using push/pull mechanisms and an agent forwarding processed telemetry to a monitoring solution for visualization and analysis.

<Frame>
  <img alt="The image illustrates a data collection pipeline where systems interact with a monitoring agent using push and pull mechanisms, which then sends data to a monitoring solution for users to create visualizations and insights." />
</Frame>

## Operational considerations — best practices

* Correlation and context propagation
  * Use distributed tracing and propagate trace/span IDs across process and network boundaries so traces can be stitched end-to-end. See OpenTelemetry for standards and examples: [https://opentelemetry.io/docs/concepts/signals/traces/](https://opentelemetry.io/docs/concepts/signals/traces/)
* Sampling and aggregation
  * Apply sampling and aggregation at the agent/collector to control ingestion volume and cost while preserving representative traces for debugging and SLO calculations.
* Enrichment and tagging
  * Add service, environment, region, version, or customer identifiers at collection time to improve filtering and troubleshooting in the backend.
* Reliability
  * Ensure agents buffer locally and retry exports on transient failures so telemetry is not lost during outages.
* Security and privacy
  * Redact sensitive data before export, use encryption in transit, and enforce access controls to meet compliance requirements.

<Callout icon="lightbulb">
  Retention and compliance are business decisions. Configure retention lengths and data redaction according to your regulatory and cost requirements.
</Callout>

## Putting it together: actionable outcomes

With properly instrumented applications and a resilient collection pipeline, teams can:

* Build dashboards that map system health to business KPIs.
* Create alerts tied to SLOs and operational thresholds.
* Perform deep-dive investigations using traces and logs to identify and fix the root cause.
* Optimize cost by tuning sampling, retention, and aggregation policies.

## Links and references

* OpenTelemetry Traces: [https://opentelemetry.io/docs/concepts/signals/traces/](https://opentelemetry.io/docs/concepts/signals/traces/)
* Prometheus exporters and instrumentation: [https://prometheus.io/docs/instrumenting/exporters/](https://prometheus.io/docs/instrumenting/exporters/)
* Kubernetes concepts (for platform-native collectors): [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/9d4795bc-91eb-4262-ae9c-f7153c17438e/lesson/d46abd80-d46f-475c-9f1c-13f32290e68b" />
</CardGroup>
