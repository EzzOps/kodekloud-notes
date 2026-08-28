# Demo OTel Col Connectors

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Connectors/page

Guide on using an OpenTelemetry Collector connector to convert incoming traces into a metric that counts observed traces and spans and forwards metrics to a metrics pipeline

This guide shows how to use a connector in the OpenTelemetry Collector to convert incoming traces into a metric that counts the number of traces (or spans) received. A connector bridges two pipelines: it acts as an exporter on the source pipeline (traces) and as a receiver on the destination pipeline (metrics). The high-level goal: if you send 10 traces to the collector, the connector produces an OpenTelemetry metric with value 10.

Why this is useful

* Create metrics derived from traces (e.g., span counts) without changing instrumented applications.
* Translate signals inside the collector to power downstream monitoring (Prometheus, remote write, etc.).
* Implement lightweight transformations or aggregations between pipelines.

Example Collector topology
A typical Collector configuration separates traces, metrics, and logs into distinct pipelines:

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes/add_env, batch]
      exporters: [debug, otlp/jaeger]
    metrics:
      receivers: [prometheus, otlp]
      processors: [filter]
      exporters: [prometheusremotewrite, debug]
    logs:
      receivers: [otlp]
      processors: [filter]
      exporters: [debug]
```

To convert traces into a span-count metric, add a connector named `count`. The connector receives traces from the traces pipeline and emits metrics into the metrics pipeline.

Prometheus remote write + debug exporters
Below is an exporter configuration that sends metrics to Prometheus remote write and also prints output via the `debug` exporter for visibility:

```yaml theme={null}
exporters:
  prometheusremotewrite:
    endpoint: "http://prometheus:9090/api/v1/write"
    tls:
      insecure: true
  debug:
    verbosity: detailed
```

Wiring the connector into pipelines
List the connector as an exporter on the traces pipeline and as a receiver on the metrics pipeline. This dual registration is what lets the connector receive the incoming traces and inject generated metrics into the metrics pipeline.

```yaml theme={null}
connectors:
  count: traces

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes/add_env, batch]
      exporters: [debug, otlp/jaeger, count]
    metrics:
      receivers: [prometheus, otlp, count]
      processors: [filter]
      exporters: [prometheusremotewrite, debug]
    logs:
      receivers: [otlp]
      processors: [filter]
      exporters: [debug]
```

How the flow works (step-by-step)

1. Traces enter the `traces` pipeline via the `otlp` receiver (OTLP protocol).
2. The `traces` pipeline applies processors (attributes, batch) and exports traces to configured exporters (e.g., debug, Jaeger).
3. Because `count` is listed as an exporter on the `traces` pipeline, the connector also receives the trace data there.
4. The connector implements counting logic and emits a metric (for example, `trace.span.count`) representing the number of spans observed.
5. Since `count` is also listed as a receiver on the `metrics` pipeline, the generated metric is ingested and processed by the metrics pipeline and forwarded to exporters such as Prometheus remote write and debug.

Quick reference: connector roles

|         Connector role | Pipeline placement                    | Purpose                                                                             |
| ---------------------: | ------------------------------------- | ----------------------------------------------------------------------------------- |
|      Exporter (source) | `service.pipelines.traces.exporters`  | Receives traces from the traces pipeline and performs conversion/aggregation.       |
| Receiver (destination) | `service.pipelines.metrics.receivers` | Accepts the emitted metric into the metrics pipeline for further processing/export. |

<Callout icon="lightbulb">
  The connector functions as an exporter on the source pipeline and as a receiver on the destination pipeline. That dual role is why it must be listed in both places.
</Callout>

Run a generator that emits a few traces to the OTLP receiver. After the connector processes them, the `debug` exporter prints the generated metric. Example debug output (abbreviated) showing `trace.span.count` with value 5:

```text theme={null}
otel-collector-config.yaml
otel-collector  | 2025-09-30T13:27:20.578Z info Metrics {"resource": {"service.instance.id": "494fc409-124e-46a6-b7ec-f22b9140f496", "service.name": "otelcol-contrib", "service.version": "0.135.0"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "metrics", "resource metrics": 1, "data points": 1}
2025-09-30T13:27:20.578Z info ResourceMetrics #0
Resource SchemaURL:
  Resource attributes:
    - telemetry.sdk.language: Str(python)
    - telemetry.sdk.name: Str(opentelemetry)
    - telemetry.sdk.version: Str(1.37.0)
    - service.name: Str(demo)
ScopeMetrics #
ScopeMetrics SchemaURL:
  InstrumentationScope github.com/open-telemetry/opentelemetry-collector-contrib/connector/co
Metric #0
Descriptor:
  -> Name: trace.span.count
  -> Description: The number of spans observed.
  -> Unit:
  -> DataType: Sum
  -> IsMonotonic: true
  -> AggregationTemporality: Delta
NumberDataPoints #0
  StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
  Timestamp: 2025-09-30 13:27:20.57675923 +0000 UTC
  Value: 5
```

Best practices and considerations

* Ensure the connector name is registered both as an exporter for the source pipeline and as a receiver for the destination pipeline; omitting either registration breaks the flow.
* Use the `debug` exporter when testing to validate that the generated metrics look correct before sending them to a production backend.
* Consider aggregation temporality and monotonicity: this example produces a monotonic sum with delta temporality; choose semantics that match your monitoring needs.
* If you translate high-volume signals into metrics, review resource and cardinality implications to avoid metric explosion.

<Callout icon="warning">
  Be careful to register the connector name both where it should act as an exporter (source pipeline) and where it should act as a receiver (destination pipeline). Omitting either will break the flow.
</Callout>

Further reading and references

* [OpenTelemetry Collector: Connectors](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector)
* [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
* [OTLP protocol specification](https://opentelemetry.io/docs/reference/specification/protocol/otlp/)
* [Prometheus remote write configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
* [Jaeger Tracing](https://www.jaegertracing.io/docs/latest/)

This example demonstrates a simple, practical use-case: turning traces into a span count metric using a connector. Connectors are flexible and can perform richer transformations or signal translations when needed.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/4c81863b-6c00-4438-bd44-3e475092a574" />
</CardGroup>
