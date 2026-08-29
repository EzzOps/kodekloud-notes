# HELP otelcol_scope_info Instrumentation Scope metadata
# TYPE otelcol_scope_info gauge
otelcol_scope_info{otel_scope_name="github.com/open-telemetry/opentelemetry-collector-contrib/pkg/stanza/fileconsumer",otel_scope_version=""} 1
otelcol_scope_info{otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper",otel_scope_version=""} 1
otelcol_scope_info{otel_scope_name="go.opentelemetry.io/collector/processor/batchprocessor",otel_scope_version=""} 1

# HELP otelcol_exporter_queue_capacity Fixed capacity of the retry queue (in batches) [alpha]
# TYPE otelcol_exporter_queue_capacity gauge
otelcol_exporter_queue_capacity{data_type="logs",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 2048
otelcol_exporter_queue_capacity{data_type="metrics",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 2048
otelcol_exporter_queue_capacity{data_type="traces",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 2048

# HELP otelcol_exporter_queue_size Current size of the retry queue (in batches) [alpha]
# TYPE otelcol_exporter_queue_size gauge
otelcol_exporter_queue_size{data_type="logs",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 0
otelcol_exporter_queue_size{data_type="metrics",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 0
otelcol_exporter_queue_size{data_type="traces",exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 0
```

* Exporter send/failed counters and fileconsumer metrics:

```text theme={null}
# HELP otelcol_exporter_send_failed_metric_points_total Number of metric points in failed attempts to send to destination. [alpha]
# TYPE otelcol_exporter_send_failed_metric_points_total counter
otelcol_exporter_send_failed_metric_points_total{exporter="debug",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 0
otelcol_exporter_send_failed_metric_points_total{exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 4885

# HELP otelcol_exporter_sent_metric_points_total Count of metric points successfully sent to destination. [alpha]
# TYPE otelcol_exporter_sent_metric_points_total counter
otelcol_exporter_sent_metric_points_total{exporter="otlp/failing",otel_scope_name="go.opentelemetry.io/collector/exporter/exporterhelper"} 0

# TYPE otelcol_fileconsumer_open_files_ratio gauge
otelcol_fileconsumer_open_files_ratio{otel_scope_name="github.com/open-telemetry/opentelemetry-collector-contrib/pkg/stanza/fileconsumer"} 0
```

* Process-level resource metrics (CPU, memory, heap, uptime):

```text theme={null}
# HELP otelcol_process_cpu_seconds_total Total CPU time used in seconds [alpha]
# TYPE otelcol_process_cpu_seconds_total counter
otelcol_process_cpu_seconds_total{service="go.opentelemetry.io/collector/service"} 2.546875

# HELP otelcol_process_memory_rss_bytes Total physical memory (resident set size) [alpha]
# TYPE otelcol_process_memory_rss_bytes gauge
otelcol_process_memory_rss_bytes{otel_scope_name="go.opentelemetry.io/collector/service"} 30443776

# HELP otelcol_process_runtime_heap_alloc_bytes Bytes of allocated heap objects (see 'go doc runtime.MemStats')
# TYPE otelcol_process_runtime_heap_alloc_bytes gauge
otelcol_process_runtime_heap_alloc_bytes{otel_scope_name="go.opentelemetry.io/collector/service"} 140424

# HELP otelcol_process_uptime_seconds_total Uptime of the process [alpha]
# TYPE otelcol_process_uptime_seconds_total counter
otelcol_process_uptime_seconds_total{otel_scope_name="go.opentelemetry.io/collector/service"} 125979
```

* Processor counters (incoming/outgoing items) and exporter sent log counts:

```text theme={null}
# HELP otelcol_processor_incoming_items_items_total Number of items passed to the processor. [alpha]
# TYPE otelcol_processor_incoming_items_items_total counter
otelcol_processor_incoming_items_items_total{otel_signal="logs",otel_scope_name="go.opentelemetry.io/collector/service"} 125979
otelcol_processor_incoming_items_items_total{otel_signal="metrics",otel_scope_name="go.opentelemetry.io/collector/service"} 214406

# HELP otelcol_exporter_sent_log_records__records__total Number of log records successfully sent to destinations
# TYPE otelcol_exporter_sent_log_records__records__total counter
otelcol_exporter_sent_log_records__records__total{exporter="otlp/collector2",otel_scope_name="go.opentelemetry.io/collector"} 214369
```

## Interpreting these metrics

Use the table below for a quick reference of metric types and what they typically represent.

| Metric Type             | Meaning                                                                                      | Example usage                                                                               |
| ----------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `counter`               | Cumulative value that only increases (monotonic). Useful for totals and rates.               | Count of log records successfully sent: `otelcol_exporter_sent_log_records__records__total` |
| `gauge`                 | Instantaneous value that can go up or down. Useful for current resource usage or queue size. | Current retry queue size: `otelcol_exporter_queue_size`                                     |
| `[alpha]` label in HELP | Experimental metric that may change between Collector releases.                              | `otelcol_exporter_queue_capacity` marked `[alpha]`                                          |

Common metric labels:

* `data_type` — the signal type: `logs`, `metrics`, or `traces`
* `exporter` — which exporter produced the metric (useful to tie metrics to a destination)
* `otel_scope_name` — the instrumentation or component scope

## Scaling and collection strategies

* Manually curling each Collector's `/metrics` endpoint (e.g., `http://<collector-ip>:8888/metrics`) is feasible for a few instances but does not scale for large deployments.
* Recommended production pattern:
  * Configure a central Prometheus server (or a centralized scraping pipeline) to scrape each Collector instance's `/metrics` endpoint.
  * Forward aggregated data from Prometheus (or the scraping pipeline) to a long-term backend for visualization and alerting.
  * Alternatively, use the Collector’s Prometheus receiver itself to scrape other Collector instances and forward their internal metrics to a central backend.

Useful references:

* Prometheus overview: [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
* OpenTelemetry Collector components: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

> **warning** Be cautious when exposing internal metrics publicly—ensure your network and authentication policies prevent unauthorized access to the `/metrics` endpoint. Limit exposure to trusted networks and enforce firewall and authentication controls as appropriate.

## Summary and quick checklist

* Enable zpages (optional) for quick debugging.
* Add a metrics pipeline that includes the Prometheus receiver.
* Add a Prometheus-format reader under `telemetry.metrics.readers` and set `host`/`port` (e.g., `8888`).
* Confirm by visiting `http://<collector-ip>:8888/metrics`.
* For scale: configure a central Prometheus scrape or a centralized scraping pipeline and forward to a backend for aggregation, alerting, and storage.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/f0507d60-5de4-4ed8-a6dd-3c4e04249ce1)


# Demo OTel Collector Extensions

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Demo-OTel-Collector-Extensions/page

Guide to enabling and configuring OpenTelemetry Collector extensions such as health_check pprof and zpages with example configurations endpoints and security recommendations

This guide shows how to enable and configure extensions in the OpenTelemetry Collector. Extensions provide additional HTTP endpoints and runtime diagnostics (health, debug pages, pprof, etc.). You declare extensions in the top-level `extensions` section and activate them by listing them in `service.extensions`. Below we cover the minimal configuration, a more complete example with TLS/debug settings, example responses, and how to access each extension.

## Minimal configuration example

A compact configuration that enables three extensions together with log and metrics pipelines:

```yaml theme={null}
extensions: [health_check, pprof, zpages]

service:
  pipelines:
    logs:
      receivers: [filelog]
      exporters: [otlphttp/dynatrace, otlp/collector2]
      processors: [attributes, resourcedetection]
    metrics:
      receivers: [prometheus]
      processors: [resourcedetection, cumulativetodelta]
      exporters: [otlphttp/dynatrace, debug]

telemetry:
  logs:
    level: "INFO"  # DEBUG | INFO | WARN | ERROR
  metrics:
    level: detailed
  readers:
    - pull:
        exporter:
          prometheus:
            host: "0.0.0.0"
            port: 8888
```

## Full example showing TLS/debug and extension endpoints

This more complete configuration demonstrates TLS/debug settings, explicit extension endpoints, and enabling the extensions in the `service` block:

```yaml theme={null}
tls:
  insecure: true  # Configure proper TLS in production

debug:
  verbosity: basic  # basic | normal | detailed

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

service:
  extensions: [health_check, pprof, zpages]
  pipelines:
    logs:
      receivers: [filelog]
      exporters: [otlphttp/dynatrace, otlp/collector2]
      processors: [attributes, resourcedetection]
    metrics:
      receivers: [prometheus]
      processors: [resourcedetection, cumulativetodelta]
      exporters: [otlphttp/dynatrace, debug]
```

> **warning** `tls.insecure: true` is useful for local testing. Do NOT use it in production—configure TLS properly for production deployments.

> **lightbulb** Extensions must be both declared under `extensions` and enabled by listing them in `service.extensions`. Declaring them alone does not activate them.

After updating the Collector configuration, restart the Collector process (or redeploy your Collector pod/container) so the configuration changes take effect.

## Common extensions and their default endpoints

|      Extension | Purpose                                                        | Example endpoint |
| -------------: | -------------------------------------------------------------- | ---------------- |
| `health_check` | Liveness / availability information                            | `0.0.0.0:13133`  |
|        `pprof` | Go runtime profiling endpoints (CPU, memory, goroutines, etc.) | `0.0.0.0:1777`   |
|       `zpages` | Runtime debug pages for collectors (servicez, tracez, etc.)    | `0.0.0.0:55679`  |

## Health check output example

When `health_check` is active, requesting the endpoint returns a short JSON payload showing availability, start time, and uptime:

```json theme={null}
{
  "status": "Server available",
  "upSince": "2025-11-17T13:06:55.882681836Z",
  "uptime": "3m17.886915133s"
}
```

Use the health check for liveness probes and basic operational checks in orchestration platforms (for example, Kubernetes liveness/readiness probes).

## zPages: runtime debug pages

The zPages extension exposes several debug pages. Use the Collector host/IP and the configured zPages port, then append the debug path. Examples:

* Service info: `http://collector-host:55679/debug/servicez`
* Traces: `http://collector-host:55679/debug/tracez`

The `servicez` page includes build/runtime information (start time, Go version, OS/arch, command used to run the Collector) and visualizes the configured/built pipelines.

<Frame>
  <img alt="The image shows a webpage with information about the OpenTelemetry Collector Contrib service, including build and runtime details such as the command, version, Go version, operating system, and architecture." />
</Frame>

The `servicez` view also shows built pipelines with details such as full name, input type, whether the pipeline mutates data, receivers, ordered processors, and exporters.

<Frame>
  <img alt="The image shows a web page displaying a table titled &#x22;builtPipelines,&#x22; detailing data processing pipelines with columns for FullName, InputType, MutatesData, Receivers, Processors, and Exporters." />
</Frame>

There is also a `featurez` section that lists feature gates and their current state. Example entries you might see:

| Feature gate                                      | State   |
| ------------------------------------------------- | ------- |
| `cloudfoundry.resourceAttributes.allow`           | `true`  |
| `confilhttp.framedSnappy`                         | `true`  |
| `conflmap.enableMergeAppendOption`                | `false` |
| `connector.datadogconnector.NativeIngest`         | `true`  |
| `connector.servicegraph.legacyLatencyMetricNames` | `false` |
| `connector.servicegraph.legacyLatencyUnitMs`      | `false` |
| `connector.servicegraph.virtualNode`              | `true`  |
| `connector.spanmetrics.legacyMetricNames`         | `false` |
| `connector.EnableOperationAndResourceV2`          | `true`  |

## tracez: inspect traces and spans

To view a live trace/span overview, open:

`http://collector-host:55679/debug/tracez`

`tracez` shows incoming and sampled spans grouped by span name and request path. You can inspect span counts, latency buckets, error samples, and drill into sampled trace IDs and span IDs. Sampled traces are commonly highlighted (for example, in blue).

<Frame>
  <img alt="The image shows a table from a web page labeled &#x22;Trace Spans,&#x22; displaying data on different spans, latency samples, and error samples for various HTTP requests. It includes details on running processes and latency buckets ranging from microseconds to minutes." />
</Frame>

## pprof: Go runtime profiling

If you enable `pprof` (for example on port 1777), the pprof index is available at:

`http://collector-host:1777/debug/pprof/`

The index lists profiles such as `allocs`, `heap`, `block`, `mutex`, `cpu` (profiling for a duration), and `goroutine` (stack traces). Clicking a profile endpoint (for example a 30-second CPU profile) downloads a pprof file that you can analyze locally with the `pprof` tool or upload to web viewers like Speedscope.

<Frame>
  <img alt="The image shows a web page displaying profiling data from the /debug/pprof/ endpoint, listing types of profiles available and their respective descriptions. The profiles include allocations, goroutines, heap, and others, with associated counts." />
</Frame>

Typical pprof visualizations:

* Graph view: call graph showing relationships between functions during the profiling window.
* Flame graph: highlights hot paths; width corresponds to CPU time consumed by the call stack.

pprof helps diagnose CPU hotspots, contention, blocking, and memory allocation patterns—useful for advanced debugging and performance tuning.

## Useful links and references

* zPages extension: [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/zpages](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/zpages)
* pprof tool: [https://github.com/google/pprof](https://github.com/google/pprof)
* Speedscope (online profile viewer): [https://speedscope.app](https://speedscope.app)
* OpenTelemetry Collector docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

This page focused on enabling and accessing the Collector extensions. For production use, ensure you secure debug endpoints, configure TLS correctly, and restrict access to diagnostic endpoints.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/b1ff1d0d-674b-42f4-90c1-dc6ca407c8ef)
