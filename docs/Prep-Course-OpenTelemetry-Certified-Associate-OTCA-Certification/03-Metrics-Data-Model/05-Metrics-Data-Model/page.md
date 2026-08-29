# Metrics Data Model

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Metrics-Data-Model/page

Overview of the OpenTelemetry metrics data model, detailing standardization, transformations, and interoperability for exporting and reaggregating metrics

This section explains the OpenTelemetry metrics data model: how metrics are structured, standardized, and transformed for compatibility and efficiency. Think of it as a blueprint showing how OpenTelemetry organizes metric data from collection through export to any backend.

The metrics data model rests on four core foundations: protocol & semantics, interoperability, smart data handling, and future-proof design. Together they ensure a consistent model so metrics mean the same thing regardless of source.

<Frame>
  <img alt="The image is an overview of a Metrics Data Model highlighting four components: Protocol & Semantics, Interoperability, Smart Data Handling, and Future-Proof Design, each detailing specific features." />
</Frame>

## End-to-end flow: existing systems → OpenTelemetry → targets

The diagram below shows the end-to-end flow. On the left are existing collectors (for example, Prometheus or StatsD) that already instrument your infrastructure but use different formats and conventions. OpenTelemetry sits in the middle as a translator and normalizer: it ingests diverse metric inputs, standardizes semantics and structure, and exports consistent metric data to dashboards, long-term storage, remote write endpoints, or vendor tools.

This design reduces vendor lock-in: you can reuse existing data sources and send normalized metrics to multiple backends without changing your instrumentation.

<Frame>
  <img alt="The image illustrates the flow of metrics in the OpenTelemetry Metrics Data Model, showing data moving from existing systems through the OpenTelemetry model to target systems like dashboards and vendors." />
</Frame>

## Prometheus Remote Write and OpenTelemetry

Prometheus excels at scraping cloud-native metrics but typically lacks built-in long-term storage. Prometheus Remote Write streams scraped metrics to an external backend for durable storage and analysis. When OpenTelemetry sits between Prometheus and a backend, it can:

* Translate Prometheus metrics into a canonical OpenTelemetry (OTel) format.
* Apply unit normalization, temporality adjustments, and label enrichment.
* Export metrics to Remote Write endpoints or reshape them for other systems.

In short: Prometheus collects, OpenTelemetry standardizes and transforms, and Remote Write delivers metrics reliably to the target backend—preserving compatibility and avoiding vendor lock-in.

Useful references:

* OpenTelemetry Metrics: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Prometheus Remote Write: [https://prometheus.io/docs/practices/remote\_write/](https://prometheus.io/docs/practices/remote_write/)

## Transformations and semantics that enable compatibility

OpenTelemetry provides explicit mechanisms for transforming and interpreting metric data so downstream systems understand values correctly and interoperate reliably. Key transformation types and semantic concerns include:

* Unit standardization: Convert and normalize units (for example, ns, ms, s) so consumers interpret values consistently.
* Aggregation temporality: Specify whether a metric is cumulative (running total) or delta (change since last point). Making temporality explicit prevents misinterpretation.
* Cumulative ↔ Delta conversion: OTel can convert between delta and cumulative temporality to match backend expectations while preserving correctness.
* Dimension (label/attribute) enrichment: Add contextual attributes such as `region=us-east-1` or `instance=vm-42` to make metrics more actionable.

> **lightbulb** Be cautious with high-cardinality attributes (for example, user IDs). Enriching every metric with high-cardinality labels can blow up the number of time series. Use enrichment and re-aggregation strategically to balance observability and cost.

### Common transformation patterns

| Transformation type     |                                          Purpose | Example                                         |
| ----------------------- | -----------------------------------------------: | ----------------------------------------------- |
| Unit normalization      |           Ensure consistent units across sources | Convert `ns` → `s` for latency metrics          |
| Temporality conversion  | Match backend expectations (cumulative vs delta) | Convert cumulative counter to delta per export  |
| Spatial re-aggregation  |        Reduce cardinality by grouping attributes | Aggregate by `region` instead of `instance`     |
| Temporal re-aggregation |      Reduce resolution / storage by downsampling | Convert per-second samples to 1-minute averages |
| Label enrichment        |    Add context for filtering and troubleshooting | Add `service`, `region`, or `env` attributes    |

### Cumulative vs Delta: quick comparison

| Temporality | What it represents                  | When to use                               |
| ----------- | ----------------------------------- | ----------------------------------------- |
| Cumulative  | A running total since process start | Counters that only increase               |
| Delta       | Change since last export            | Backends that expect rate-style ingestion |

## Configurability, cost control, and re-aggregation

Transformations are central to controlling volume and cost while retaining useful signal. Two common re-aggregation patterns are:

* Spatial re-aggregation: Reduce cardinality by grouping or aggregating across attributes (for example, aggregate by `region` or `service` instead of by individual user ID).
* Temporal re-aggregation: Reduce resolution by rolling up high-frequency samples into larger intervals (for example, convert per-second samples into 1-minute averages).

These techniques help preserve trends and actionable insights while limiting the number of stored series and query costs.

<Frame>
  <img alt="The image is a diagram of the OpenTelemetry Metrics Data Model, highlighting configurability and cost control, with spatial and temporal reaggregation, reliability, and statelessness." />
</Frame>

> **warning** Be intentional about where you perform re-aggregation. Aggressive rollups can hide short-lived spikes or outliers; insufficient aggregation can cause excessive storage and query costs. Test configurations against representative workloads.

## Reliability and statelessness

OpenTelemetry’s transformation design emphasizes predictable behavior and operational reliability. Where possible, transformations avoid hidden dependencies on prior state so pipelines remain horizontally scalable and robust. When state is required (for example, to compute deltas), that state should be explicit and managed so processing remains reliable across restarts and distributed components.

Key operational principles:

* Prefer stateless transforms for horizontal scaling.
* Make state explicit and durable (or reconstructable) where needed for correctness.
* Document temporality and conversion rules so downstream systems interpret metrics correctly.

## Summary: what the metrics data model delivers

At its core, the OTel metrics data model defines how metrics are structured, labeled, and transmitted so they are consistent across systems like Prometheus and StatsD. Its main qualities:

* Standardized: Clear protocol and semantic conventions for pre-aggregated time series.
* Compatible: Works with existing sources (Prometheus, StatsD) and many backends.
* Flexible: Supports transformations like spatial and temporal re-aggregation and unit conversion.
* Controllable: Enables explicit handling of cumulative vs delta temporality and cardinality.
* Outcome-focused: Designed to deliver reliable, semantically rich, and interoperable metrics for modern observability.

<Frame>
  <img alt="The image outlines the OpenTelemetry Metrics Data Model, emphasizing its properties of being standardized, transformable, and compatible, and highlights its goal to deliver reliable, semantically rich, interoperable metrics." />
</Frame>

The protocol and semantics define a clear framework for delivering pre-aggregated metric time series. Compatibility with existing data sources and flexible transformation capabilities make OpenTelemetry a practical integration layer: it lets you shape metrics to your backend needs while avoiding vendor lock-in.

<Frame>
  <img alt="The image is an overview of the OpenTelemetry Metrics Data Model, highlighting six aspects: Protocol + Semantics, Compatibility, Flexibility, Control, Interoperability, and Outcome. Each aspect is briefly described, focusing on metrics' data handling and observability." />
</Frame>

This section covered the OpenTelemetry metrics data model. For further reading, see the OpenTelemetry documentation and the Prometheus Remote Write guidelines linked above.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/8b85e7d8-cd94-47c8-8067-4dcb78b0e6ee)
