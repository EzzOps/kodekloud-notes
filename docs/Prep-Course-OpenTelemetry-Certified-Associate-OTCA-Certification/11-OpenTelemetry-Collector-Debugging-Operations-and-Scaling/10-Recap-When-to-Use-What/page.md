# HELP otel_scope_info Instrumentation Scope metadata
# TYPE otel_scope_info gauge
otel_scope_info{otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 1
otel_scope_info{otel_scope_name="go.opentelemetry.io/collector/processor/batchprocessor",otel_scope_version=""} 1
otel_scope_info{otel_scope_name="go.opentelemetry.io/collector/receiver/receiverhelper",otel_scope_version=""} 1
otel_scope_info{otel_scope_name="go.opentelemetry.io/collector/service",otel_scope_version=""} 1

# HELP otelcol_exporter_send_failed_log_records_total Number of log records in failed attempts to send to destination. [alpha]
# TYPE otelcol_exporter_send_failed_log_records_total counter
otelcol_exporter_send_failed_log_records_total{exporter="debug",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 0

# HELP otelcol_exporter_send_failed_metric_points_total Number of metric points in failed attempts to send to destination. [alpha]
# TYPE otelcol_exporter_send_failed_metric_points_total counter
otelcol_exporter_send_failed_metric_points_total{exporter="debug",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 0

# HELP otelcol_exporter_send_failed_spans_total Number of spans in failed attempts to send to destination. [alpha]
# TYPE otelcol_exporter_send_failed_spans_total counter
otelcol_exporter_send_failed_spans_total{exporter="debug",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 0

# HELP otelcol_exporter_sent_log_records_total Number of log records successfully sent to destination. [alpha]
# TYPE otelcol_exporter_sent_log_records_total counter
otelcol_exporter_sent_log_records_total{exporter="debug",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 42
```

Scraping and forward-ing

* Scrape with Prometheus or any compatible scrape-based monitoring system.
* The Collector can also ingest its own metrics and forward them to any supported backend for dashboards, alerts, and long-term analysis.

Troubleshooting approach (quick checklist)

* Check receiver accepted/refused counters for ingestion issues.
* Inspect exporter send failures to identify backend problems.
* Monitor queue size and processor metrics for backpressure.
* Correlate process CPU/memory metrics with spikes in refused or failed counts.
* Use zPages for quick, live introspection; use pprof for deep performance profiling.

Quiz: which OpenTelemetry Collector metric indicates that the Collector is refusing new span data due to memory constraints?

* A. Memory usage
* B. Exported queue size
* C. Rejected traces
* D. otelcol\_processor\_refused\_spans\_total

<Frame>
  <img alt="The image is a quiz question about identifying which OpenTelemetry Collector metric indicates span refusal due to memory constraints, with four answer options. Option D, &#x22;otelcol_processor_refused_spans_total,&#x22; is highlighted." />
</Frame>

Answer explanation

* The phrasing "refusing new span data" maps directly to a refused-spans metric. The metric `otelcol_processor_refused_spans_total` explicitly records spans that were refused by a processor (for example, because of memory pressure or configured dropping rules). Parse metric names logically: component → action → signal.

Takeaway

* Focus on the consistent naming pattern: `otelcol_<component>_<action>_<signal>_<suffix>`.
* Use metrics to pinpoint where the problem lies (receivers, processors, exporters, or resource exhaustion) and then apply targeted debugging (zPages, logs, pprof) as needed.

Links and references

* [OpenTelemetry Collector docs](https://opentelemetry.io/docs/collector/)
* [Prometheus documentation](https://prometheus.io/)
* [zPages extension repo](https://github.com/open-telemetry/opentelemetry-collector/tree/main/extension/zpages)
* [pprof (net/http/pprof)](https://pkg.go.dev/net/http/pprof)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/080eea24-a1d3-48e7-8e67-194225f719a9" />
</CardGroup>


# Recap When to Use What

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Recap-When-to-Use-What/page

Overview of OpenTelemetry Collector diagnostic endpoints and when to use metrics, health checks, zPages, and pprof for operational visibility and performance troubleshooting

Quickly review the diagnostic endpoints built into the OpenTelemetry Collector and when to use each. These tools help with operational visibility, orchestration readiness, live component inspection, and deep runtime profiling.

We have four main endpoints for troubleshooting the Collector:

* Metrics: operational visibility and ingestion verification.
* Health check: simple heartbeat for orchestration Liveness/Readiness checks.
* zPages: live, in-browser component views for interactive debugging.
* pprof: advanced Go runtime profiles (CPU, memory, contention).

Metrics validate that data is being received and delivered to backends. They reveal ingestion/delivery patterns and surface internal resource usage trends inside the Collector.

<Frame>
  <img alt="The image compares different metrics and tools for tracking and ingestion, like &#x22;Metrics,&#x22; &#x22;Health Check,&#x22; &#x22;zPages,&#x22; and &#x22;pprof,&#x22; with numbers beside each. There are options related to &#x22;Enable and track ingestion,&#x22; &#x22;Delivery,&#x22; and &#x22;Resource Usage.&#x22;" />
</Frame>

Health check endpoints are primarily for orchestration systems (Kubernetes, Nomad, etc.). Use them during rollouts, restarts, or whenever the orchestrator needs a simple OK/Not-OK probe to manage lifecycle operations.

zPages provides quick, live, in-browser views of what Collector components are doing. Use zPages for hands-on troubleshooting when you want to inspect component internals without attaching debuggers or altering configuration.

<Frame>
  <img alt="The image is a screenshot showing different components with associated ports, specifically &#x22;Metrics (8888),&#x22; &#x22;Health Check (13133),&#x22; &#x22;zPages (55679),&#x22; and &#x22;pprof (1777).&#x22; The &#x22;zPages&#x22; component is highlighted, with a note about live, in-browser component views." />
</Frame>

pprof is for advanced investigations: capture CPU profiles, inspect heap allocations, and analyze mutex contention. Use pprof when you suspect performance bottlenecks or need to profile under realistic load.

<Frame>
  <img alt="The image is a diagram titled &#x22;pprof — When to Use,&#x22; showing four sections: Metrics, Health Check, zPages, and pprof, each with a port number. Below pprof, there are options for CPU, Memory, and Contention analysis." />
</Frame>

Below is a concise example Collector configuration showing where to enable these diagnostic extensions and how to expose the Collector’s own Prometheus metrics for scraping. Note that metrics are configured under `service.telemetry.metrics`, while health check, pprof, and zPages are configured as extensions and then referenced under `service.extensions`.

```yaml theme={null}
extensions:
  health_check:
    endpoint: "0.0.0.0:13133"    # GET http://localhost:13133/ -> 200 OK when healthy
  pprof:
    endpoint: "0.0.0.0:1777"     # http://localhost:1777/debug/pprof/
  zpages:
    endpoint: "0.0.0.0:55679"    # http://localhost:55679/debug/servicez/

receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"  # matches your load generator defaults

processors:
  batch: {}

exporters:
  debug:
    verbosity: detailed          # if this errors in your build, use: debug: {}

service:
  telemetry:
    metrics:
      # optional level: basic | normal | detailed
      level: normal
    readers:
      - pull:
          exporter:
            prometheus:
              host: "0.0.0.0"
              port: 8888               # Prometheus scrape at http://localhost:8888/metrics

extensions: [health_check, pprof, zpages]

pipelines:
  traces:
    receivers: [otlp]
    processors: [batch]
    exporters: [debug]
```

<Callout icon="lightbulb">
  pprof is powerful but advanced. Use it when you need CPU or memory profiles to diagnose performance bottlenecks. For day-to-day checks, rely on metrics, health checks, and zPages.
</Callout>

Below is a quick reference table for these endpoints and when to use them:

|     Endpoint |   Port  | Purpose                                        | Typical Use                                                      |
| -----------: | :-----: | ---------------------------------------------- | ---------------------------------------------------------------- |
|      Metrics |  `8888` | Prometheus-compatible operational metrics      | Validate ingestion and delivery patterns; monitor resource usage |
| Health check | `13133` | Liveness/readiness heartbeat                   | Orchestration probes during rollouts and restarts                |
|       zPages | `55679` | In-browser component insights                  | Live troubleshooting of component internals without a debugger   |
|        pprof |  `1777` | Go runtime profiling (CPU, memory, contention) | Deep performance analysis under load                             |

Links and references:

* OpenTelemetry Collector diagnostics overview (conceptual)
* Advanced Golang profiling: [https://learn.kodekloud.com/user/courses/advanced-golang](https://learn.kodekloud.com/user/courses/advanced-golang)
* Prometheus basics and scraping: [https://learn.kodekloud.com/user/courses/prep-course-prometheus-certified-associate-pca-certification](https://learn.kodekloud.com/user/courses/prep-course-prometheus-certified-associate-pca-certification)

<Frame>
  <img alt="The image shows a &#x22;Wrap Up&#x22; slide with four sections: Metrics 8888, Health 13133, zPages 55679, and pprof 1777, each with related features like built-in metrics, heartbeat signal, in-browser view, and live debug." />
</Frame>

That wraps up this topic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/1aa0f7c7-0925-4936-bccc-608de6aa3a8d" />
</CardGroup>
