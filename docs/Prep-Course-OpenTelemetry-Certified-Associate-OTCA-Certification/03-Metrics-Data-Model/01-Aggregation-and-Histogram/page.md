# Example: set service name and OTLP exporter
OTEL_SERVICE_NAME="orders-service"
OTEL_EXPORTER_OTLP_ENDPOINT="https://otel-collector.example.com:4317"
OTEL_TRACES_EXPORTER="otlp"
OTEL_PROPAGATORS="tracecontext,baggage"
```

<Frame>
  <img alt="The image displays a graphic titled &#x22;Common Configuration Settings&#x22; with four sections labeled: Service Name, Exporter, Propagator, and Resource Attributes, each with icons and examples." />
</Frame>

Why is zero-code instrumentation popular?

* Fast and non-invasive: enables telemetry quickly without code changes.
* Great for initial observability: provides immediate visibility into production systems.
* Low developer effort: only change how the app is started or its runtime environment.
* Configurable and extensible: environment variables and startup options let you tailor behavior.

<Frame>
  <img alt="The image presents the advantages of zero-code instrumentation, highlighting four benefits: fast and non-invasive setup, suitability for initial observability, no developer effort required, and being configurable and extensible." />
</Frame>

<Callout icon="lightbulb">
  Zero-code instrumentation is an excellent first step for gaining observability quickly. Use it to get baseline telemetry, then add code-based instrumentation selectively where you need domain-specific traces or richer context.
</Callout>

That covers the essentials of zero-code automatic instrumentation. Use it to bootstrap observability, and augment with code-based instrumentation when you need custom, business-level spans.

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* OpenTelemetry eBPF project: [https://github.com/open-telemetry/opentelemetry-ebpf](https://github.com/open-telemetry/opentelemetry-ebpf)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/75aa998f-6fba-4547-9859-83ca424db6be" />
</CardGroup>


# Aggregation and Histogram

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Aggregation-and-Histogram/page

Explains metric aggregation and histograms for summarizing telemetry, bucket types, and using percentiles to analyze distributions and detect latency outliers.

In this lesson we cover aggregation: the process of transforming raw metric samples into summarized statistics. Aggregation reduces high-volume telemetry into compact, queryable summaries that answer higher-level operational questions about your system.

<Frame>
  <img alt="The image presents a definition of aggregation, explaining it as the process of combining raw metric data points into a statistical summary." />
</Frame>

## What is aggregation?

Aggregation takes individual measurements (for example, request latencies or current memory usage) and produces a summary such as a sum, a last-seen value, or a distribution. The aggregation type you choose determines what questions you can answer later from the stored metrics.

### Common aggregation types

| Aggregation type |                                                  Description | Typical use case                            |
| ---------------- | -----------------------------------------------------------: | ------------------------------------------- |
| Sum              |     Totals values over time to produce a cumulative measure. | `total_requests` or throughput counters.    |
| Gauge            | Reports the latest observed value at scrape/collection time. | Current temperature, in-progress requests.  |
| Histogram        | Captures the distribution of values across buckets (ranges). | Response time distributions, payload sizes. |

<Frame>
  <img alt="The image shows a table describing aggregation types and their descriptions, and a flowchart illustrating data flow from OTLP to TimeSeries." />
</Frame>

The image above also illustrates how OTLP metric types map to backend time series. Consistent mapping ensures aggregated metrics are interpreted correctly across collectors and storage backends.

## Why use histograms?

Histograms capture a distribution instead of a single scalar. This is crucial when averages hide important behavior (for example, latency spikes). Histograms let you:

* See the shape of latency or size distributions.
* Compute percentiles (P50, P95, P99) to characterize tail behavior.
* Detect and debug outliers and performance anomalies.

Exponential histograms are a compact representation that scales well for datasets with wide dynamic ranges, providing space-efficient aggregation while preserving percentile estimates.

## Example: histogram for HTTP request durations

Consider a histogram metric that tracks server request durations:

* Metric name: `http.server.duration`
* Unit: milliseconds
* Instrument type: histogram
* Observed values: 12 ms, 18 ms, 20 ms, 30 ms, 75 ms, 200 ms, 300 ms

<Frame>
  <img alt="The image is a table summarizing a histogram aggregation use case example, detailing metric, unit, instrument type, scenario, and recorded observations for tracking request durations in a web server." />
</Frame>

Rather than a single average, the histogram places these values into buckets (ranges) and counts how many observations fall into each one. A bucket is a contiguous range of values; the histogram records the count per bucket plus overall metadata that enables percentile estimation.

<Frame>
  <img alt="The image provides an explanation of what a bucket in a histogram is, defining it as a range of values that the histogram uses to count how many recorded measurements fall into each of those ranges." />
</Frame>

Buckets (bins) can be configured in two common ways:

* Explicit buckets: you define threshold boundaries manually (e.g., 0–10 ms, 10–50 ms, 50–100 ms, …).
* Exponential buckets: boundaries grow exponentially and adapt better to wide-ranging values.

<Frame>
  <img alt="The image explains what a bucket in a histogram is, showing buckets as bins that group values with different numerical ranges. It highlights that buckets can be explicit or exponential." />
</Frame>

When you count recorded values into buckets, you can visualize the distribution as a bar chart and compute percentiles. For the example above, bucket counts produce a column chart that highlights that most requests are under 50 ms, a smaller group near 100 ms, and a few outliers at 300 ms.

<Frame>
  <img alt="The image shows a table and a histogram, both displaying data about request durations in milliseconds, categorized into different bucket ranges. The table lists the count and values for each bucket, while the histogram visualizes the request count for each duration range." />
</Frame>

### Percentiles from histograms

Percentiles summarize the distribution:

* P50 (median) — half the requests are at or below this value. In the example above: `P50 ≈ 30 ms`.
* P90 — 90% of requests are at or below this value; useful to measure typical tail latency.
* P95 and P99 — isolate heavier tails and outliers to guide performance tuning and alerting.

Use percentiles to set meaningful SLOs and to prioritize optimization efforts where tail latencies hurt user experience.

## Quick reference & resources

* OpenTelemetry Metrics overview: [https://opentelemetry.io/docs/messaging/metrics/](https://opentelemetry.io/docs/messaging/metrics/)
* Histogram guidance and best practices: check your backend docs for supported histogram types (`explicit` vs `exponential`) and percentile computation guarantees.

<Callout icon="lightbulb">
  Histograms are essential when distribution matters. Percentiles and distribution summaries derived from histograms reveal performance characteristics that averages alone can hide.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/e93febbf-8931-4ddc-b3d9-c7b85f6c9d88" />
</CardGroup>
