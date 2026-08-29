# Service and Pipelines Explained

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Service-and-Pipelines-Explained/page

Explains OpenTelemetry Collector service and pipelines, wiring receivers processors exporters and extensions to build route and manage telemetry flows with examples and best practices.

In this lesson we break down the service and pipelines of the OpenTelemetry Collector and show how to wire receivers, processors, exporters, and runtime extensions together for reliable telemetry collection.

Each telemetry signal (traces, metrics, logs) flows through its own pipeline. The `service` section acts as the Collector's control plane — it activates pipelines, selects which component instances are used, and defines processor execution order and internal telemetry settings.

<Frame>
  <img alt="The image is a diagram showing the OpenTelemetry Collector's structure, including pipelines for traces, metrics, and logs, each consisting of receivers, processors, and exporters." />
</Frame>

Overview: how pipelines fit together

* Receivers ingest telemetry into the Collector.
* Processors transform, filter, or enrich telemetry; order is significant (executed left-to-right).
* Exporters send telemetry to backends (or local logging/debugging exporters).
* The `service` block references component instances and binds them to each pipeline.

Quick reference: component roles

| Component type |                                         Purpose | Example usage                                |
| -------------- | ----------------------------------------------: | -------------------------------------------- |
| Receiver       |                   Ingest telemetry from sources | `otlp` (gRPC/HTTP), `prometheus`             |
| Processor      | Transform/filter/limit telemetry; order matters | `attributes`, `batch`, `memory_limiter`      |
| Exporter       |    Deliver telemetry to backends or local debug | `otlphttp`, `prometheusremotewrite`, `debug` |
| Extension      |          Runtime features not part of pipelines | `health_check`, `pprof`, `file_storage`      |

Basic idea (visualized):

```text theme={null}
Pipelines:
  service
    ├─ pipelines
    │   └─ traces
    └─ processors  ← left-to-right order matters
```

Minimal YAML example showing component definitions and pipeline activation:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  otlp/ingest2:       # type/name — second instance of the otlp receiver

processors:
  batch: {}
  attributes/sanitize: {}

exporters:
  otlphttp:
    endpoint: https://vendorname.example.com:4318
    debug:
      verbosity: normal

service:
  pipelines:
    traces/prod:
      receivers: [otlp]
      processors: [attributes/sanitize, batch]   # processor order matters
      exporters: [otlphttp]

    traces/dev:
      receivers: [otlp/ingest2]
      processors: [attributes/sanitize]
      exporters: [debug]
```

Naming and instances

* You can create multiple instances of a component type using `type/name` (example: `otlp/ingest2`).
* Any instance referenced by a pipeline must exist under the corresponding top-level `receivers`, `processors`, or `exporters` section.
* If a component is not listed in the `service` pipelines, it will not be active.

Telemetry and internal metrics

* The `service` block also configures the Collector’s internal logs and metrics.
* Older configs used a single `metrics.address` field. Current Collector releases prefer `telemetry.metrics.readers` for flexible pull (Prometheus) and push (periodic) strategies.

> **lightbulb** Processor order matters. Put limiters or normalizers (for example `memory_limiter`, `attributes`) before the `batch` processor so transformations and limits are applied prior to batching.

Deprecated (older style):

```yaml theme={null}
