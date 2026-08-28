# Deprecated style (older releases)
metrics:
  address: "0.0.0.0:8888"  # single endpoint for Prometheus scraping

telemetry:
  logs:
    level: "INFO"
```

Recommended (current) style using readers:

```yaml theme={null}
telemetry:
  logs:
    level: "INFO"
  metrics:
    level: normal
    readers:
      - pull:
          exporter:
            prometheus:
              host: "0.0.0.0"
              port: 8888
      - periodic:
          exporter:
            otlp:
              endpoint: "https://telemetry.vendorname.example.com:4318"
```

Using readers:

* `pull`: exposes a Prometheus scrape endpoint.
* `periodic`: periodically pushes Collector-internal metrics to an OTLP endpoint.
* Both readers can run concurrently to support mixed workflows.

Fan-out: send same telemetry to multiple exporters

<Frame>
  <img alt="The image depicts a &#x22;Fan-Out&#x22; pattern workflow, showing a data flow from a &#x22;Receivers: otlp&#x22; component to a &#x22;Processor: batch,&#x22; and then branching out to &#x22;Exporters: otlphttp.&#x22;" />
</Frame>

Example — fan-out to multiple backends:

```yaml theme={null}
service:
  pipelines:
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp, kafka/audit, prometheusremotewrite/edge] # fan-out
```

Fan-in: multiple receivers into a single pipeline

<Frame>
  <img alt="The image illustrates a &#x22;Fan-In&#x22; pattern with multiple receivers feeding into one pipeline through a processor that handles transformation and batching." />
</Frame>

Example — fan-in to normalize and forward metrics:

```yaml theme={null}
service:
  pipelines:
    metrics:
      receivers: [otlp, prometheus, hostmetrics]
      processors: [transform, batch]
      exporters: [prometheusremotewrite/edge]
```

Multi-pipeline scenarios (prod/dev split)

<Frame>
  <img alt="The image illustrates a pattern for a multi-pipeline split with separate configurations for a PROD and DEV environment, showing the flow from receivers to processors to exporters in each pipeline." />
</Frame>

You can run multiple pipelines for the same signal (e.g., `traces/prod` and `traces/dev`) with different receivers/processors/exporters:

```yaml theme={null}
service:
  pipelines:
    traces/prod:
      receivers: [otlp]
      processors: [attributes/sanitize, batch]
      exporters: [otlphttp]

    traces/dev:
      receivers: [otlp/ingest2]
      processors: [attributes/sanitize]
      exporters: [debug] # local inspection
```

Blue/green pipeline pattern — safe testing of new processors

<Frame>
  <img alt="The image depicts a diagram of a Blue/Green pipeline pattern for safe cutovers, showing a flow from &#x22;Receivers: otlp&#x22; to two branches labeled &#x22;logs/blue transform/v1&#x22; and &#x22;logs/green transform/v2&#x22; with respective export sections." />
</Frame>

Blue/green lets you test a new transform chain in parallel with the current pipeline:

```yaml theme={null}
service:
  pipelines:
    logs/blue:
      receivers: [otlp]
      processors: [transform/v1, batch]
      exporters: [otlphttp]

    logs/green:
      receivers: [otlp]
      processors: [transform/v2, batch]
      exporters: [otlphttp]
# Flip upstream routing or switch receiver instances when ready
```

<Callout icon="warning">
  If both blue and green pipelines are active and receive the same input, you will produce duplicate telemetry at the destination(s). Use routing rules or switch receivers to avoid duplication during cutover.
</Callout>

Common failure modes and quick fixes

<Frame>
  <img alt="The image shows a table titled &#x22;Common Failure Modes (quick fixes)&#x22; listing problems and their corresponding quick fixes. It includes issues like component pipeline errors and deprecated addresses, along with suggested solutions." />
</Frame>

Table: common problems and remedies

| Problem                              | Quick fix                                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Component not active                 | Ensure the instance name is referenced in `service.pipelines`.                                              |
| Processor order incorrect            | Run normalizers/limiters before `batch` (e.g., `memory_limiter` before `batch`).                            |
| Deprecated metrics address in config | Replace with `telemetry.metrics.readers`.                                                                   |
| Debug/logging exporters in prod      | Remove or replace with production exporters; keep `debug` for troubleshooting only.                         |
| Port conflicts                       | Assign unique host/port values for Prometheus receivers or internal metrics endpoints.                      |
| Configuration errors                 | Validate config with `otelcol --config config.yaml --validate` (or your distribution's validation command). |

Extensions — runtime features (not part of pipelines)

Extensions are long-running features that support the Collector runtime but do not process telemetry within pipelines. Common use cases include Kubernetes health endpoints, runtime profiling, and durable local storage for queues.

<Frame>
  <img alt="The image explains the role of &#x22;Extensions&#x22; as long-running features supporting the Collector runtime but not processing telemetry in pipelines, with typical roles including health endpoints for Kubernetes and runtime profiling." />
</Frame>

Example: enabling extensions and referencing them in `service.extensions`:

```yaml theme={null}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133   # liveness/readiness probe
  pprof:
    endpoint: 0.0.0.0:1777     # CPU/heap profiling
  file_storage:
    directory: /var/lib/otelcol/file_storage

service:
  extensions: [health_check, pprof, file_storage]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp]
```

Durable sending queues with file storage

* If an exporter uses retries and a sending queue, bind the queue storage to a `file_storage` extension so telemetry is persisted locally while the backend is unavailable:

```yaml theme={null}
extensions:
  file_storage:
    directory: /var/lib/otelcol/file_storage

exporters:
  otlphttp:
    endpoint: https://vendorname.example.com:4318
    retry_on_failure:
      enabled: true
      max_elapsed_time: 10m
    sending_queue:
      queue_size: 5000
      storage: file_storage # ties the exporter queue to the file_storage extension

service:
  extensions: [file_storage]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp]
```

Health checks

* When `health_check` is enabled and added to `service.extensions`, the Collector exposes a health endpoint (useful for Kubernetes liveness/readiness probes) on the configured port (example: 13133).

Recap — actionable rules to remember

<Frame>
  <img alt="The image contains a list of five exam tips and a recap with colorful numbered icons. The tips cover topics like service, processors, fan-out, debugging, and internal telemetry." />
</Frame>

* The `service` section is mandatory: unreferenced components are ignored.
* Processor execution order is left-to-right — put limiters/normalizers before `batch`.
* Fan-out: a pipeline can export the same data to multiple destinations.
* Fan-in: multiple receivers can feed a single normalized pipeline.
* Use `debug` or `logging` exporters only for troubleshooting; avoid in production.
* Use `telemetry.metrics.readers` to expose internal metrics (Prometheus pull or periodic pushes).
* Validate configuration before starting the Collector and use internal metrics/debug exporter to analyze behavior:
  * `otelcol --config config.yaml --validate`

Links and references

* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Kubernetes probes and readiness/liveness: [https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

That's it for the Collector's service section and pipelines — use these patterns to design robust collection flows, avoid duplicates during cutovers, and ensure internal telemetry is observable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/3cf8dbc3-c711-4775-b58a-e59eef131a92" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/69d88262-9bbf-42aa-9d85-a532e07d7b2a" />
</CardGroup>


# Debug Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Debug-Exporter/page

Practical guide to the OpenTelemetry Collector debug exporter explaining purpose, configuration, verbosity levels, sampling usage, and best practices for debugging traces, metrics, and logs during development.

This article gives a concise, practical guide to the OpenTelemetry Collector debug exporter: what it is, how to configure it, and when to use it. The debug exporter writes telemetry (traces, metrics, logs) to the collector’s logs (stdout/stderr) with configurable verbosity and optional sampling. It is ideal for validating data, testing new configurations, and troubleshooting pipeline behavior during development.

<Callout icon="lightbulb">
  The debug exporter is intended for debugging and testing only — it is not recommended for production use.
</Callout>

<Frame>
  <img alt="The image is a flowchart introducing a &#x22;Debug Exporter&#x22; involving stages like Testing, Validation, and Troubleshooting within Pipelines." />
</Frame>

## What the debug exporter does

* Emits telemetry payloads to the collector log stream so you can inspect them in real time.
* Supports verbosity levels to control how much information is printed.
* Offers sampling controls to limit output volume in high-throughput environments.

Sampling is useful to keep log output manageable when telemetry rates are high.

```yaml theme={null}
exporters:
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 200
```

Note: Setting `sampling_initial` and `sampling_thereafter` reduces how many items are printed (for example, the first N items are printed, then 1 in M thereafter).

To actually see output for a given signal (traces, metrics, logs), include the debug exporter in that signal’s pipeline. If not referenced in a pipeline, the collector will not print that signal’s data.

Example minimal configuration that enables the debug exporter for all three signals:

```yaml theme={null}
exporters:
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 200

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

## Verbosity levels

Verbosity controls how much the debug exporter prints. The three supported levels are `basic`, `normal`, and `detailed`. Use the appropriate level depending on how much inspection you need.

| Verbosity  | What it prints                                                                          | When to use it                                             |
| ---------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `basic`    | One-line summaries with resource metadata, component ID, signal type, and counts.       | Quick confirmation of data flow and volume.                |
| `normal`   | Resource and instrumentation scope metadata plus counts.                                | Inspect provenance and scopes without full payloads.       |
| `detailed` | Full payloads: complete spans, metrics, or log records including attributes and events. | Deep debugging; inspect attribute values, events, and IDs. |

<Frame>
  <img alt="The image shows three verbosity options: &#x22;Basic,&#x22; &#x22;Normal,&#x22; and &#x22;Detailed.&#x22; The &#x22;Basic&#x22; option is highlighted and indicates it &#x22;prints one-line summaries of counts.&#x22;" />
</Frame>

Example log entries produced with `basic` verbosity:

```text theme={null}
2025-09-13T15:59:41.427Z info Metrics {"otelcol.signal": "metrics", "metrics": 3, "data points": 3}
2025-09-13T15:59:41.427Z info Logs {"otelcol.signal": "logs", "log records": 50}
2025-09-13T15:59:41.627Z info Traces {"otelcol.signal": "traces", "spans": 100}
```

The `normal` level augments the above with resource and scope metadata. The `detailed` level prints full payloads including attributes and events.

<Frame>
  <img alt="The image shows three verbosity options: Basic, Normal, and Detailed, with Detailed being highlighted and described as printing full payloads including attributes and events." />
</Frame>

A trimmed example of a `detailed` span record:

```text theme={null}
Span #99
 Trace ID   : 463e0fd125c7a4f513172fd76ad105af
 ID         : cfc32bcb41a321a2
 Name       : demo_operation
 Attributes:
  -> user.id: Str(mr9a9pa511)
  -> session.id: Str(6xgsbqnw6jivfnwi)
 Events:
  SpanEvent #0
   -> Name: step
   -> Attributes:
      -> state: Str(mid)
```

Detailed output is particularly useful to:

* validate payload structure,
* confirm context propagation (e.g., consistent trace IDs across spans),
* inspect attribute and field transformations applied by processors, and
* diagnose pipeline routing or dropping issues.

<Callout icon="warning">
  Be cautious: detailed debug output can include sensitive information and generate very large log volumes. Do not enable `detailed` verbosity in production. If needed, redirect collector stdout/stderr to a controlled file and restrict access.
</Callout>

## Additional notes and best practices

* The collector’s global logging level (e.g., `DEBUG`, `INFO`, `WARN`, `ERROR`) controls the collector’s own logs and is separate from the debug exporter `verbosity`.
* Debug exporter verbosity options: `basic | normal | detailed`.
* Persisting debug output: redirect stdout/stderr when launching the collector (for example, shell redirection or container log drivers).
* Use sampling parameters (`sampling_initial`, `sampling_thereafter`) to reduce noise when testing high-throughput pipelines.

## Links and references

* OpenTelemetry Collector — official docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OpenTelemetry configuration examples: [https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/examples](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/examples)

This concludes the overview of the debug exporter.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/ea53fa1a-71bb-4cd4-9768-48f5bb3aadc7" />
</CardGroup>
