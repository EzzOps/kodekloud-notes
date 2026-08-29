# processors:
#   batch:
#   attributes:
#   resource:
```

## Exporters

Exporters send processed telemetry to destinations. Typical exporters include OTLP, Prometheus, Jaeger, Zipkin, Kafka, file, cloud vendor backends, and a debug exporter that prints telemetry to stdout.

Example exporter snippets:

```yaml theme={null}
exporters:
  # Send to another OTLP endpoint (e.g., vendor ingest)
  otlp:
    endpoint: otel-collector-upstream:4317
    tls:
      cert_file: cert.pem
      key_file: cert-key.pem

  # Prometheus exporter (exposes a scrape endpoint)
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: default

  # Debug exporter: prints telemetry to stdout (useful for testing)
  debug:
    verbosity: detailed
```

Note: Historically some distributions used `logging` instead of `debug`—check the Collector version and distribution.

## Wiring it together: service.pipelines

Pipelines connect `receivers` to `processors` and `exporters`. You must define a pipeline for each signal you want to process (`traces`, `metrics`, `logs`). Each pipeline lists `receivers`, optionally `processors`, and `exporters`.

Minimal complete config (receives OTLP gRPC + HTTP; exports all signals to `debug`):

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors: {}

exporters:
  debug:
    verbosity: detailed

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

With this configuration the Collector accepts traces, metrics, and logs via OTLP and prints them to the console for inspection.

## Running the Collector (Docker example)

You can run the Collector as a binary, Docker image, Docker Compose service, or inside Kubernetes. Example using the contrib Docker image (includes many receivers/exporters):

```bash theme={null}
docker pull otel/opentelemetry-collector-contrib:0.136.0

# Run the Collector interactively (example only):
docker run \
  -p 127.0.0.1:4317:4317 \
  -p 127.0.0.1:4318:4318 \
  -p 127.0.0.1:55679:55679 \
  -v "$(pwd)/otel-collector-config.yaml":/conf/otel-collector-config.yaml:ro \
  otel/opentelemetry-collector-contrib:0.136.0 \
  --config /conf/otel-collector-config.yaml 2>&1 | tee collector-output.txt
```

When OTLP is configured you should see logs indicating the gRPC and HTTP OTLP servers started and that the service is ready. Example (trimmed):

```plaintext theme={null}
otel-collector | 2025-09-29T23:04:46.098Z info otlpreceiver@v0.135.0/otlp.go:121 Starting GRPC server
otel-collector | 2025-09-29T23:04:46.098Z info otlpreceiver@v0.135.0/otlp.go:179 Starting HTTP server
otel-collector | 2025-09-29T23:04:46.098Z info service@v0.135.0/service.go:234 Everything is ready. Begin processing data. {"resource":{"service.instance.id":"...","service.name":"otelcol-contrib","service.version":"0.135.0"}}
```

<Callout icon="warning">
  Be mindful of which image you use: `otel/opentelemetry-collector` (core) includes fewer components than `otel/opentelemetry-collector-contrib`. Choose the image that contains the receivers/exporters you need. Binding ports to `127.0.0.1` restricts access to localhost; remove `127.0.0.1:` to expose to all interfaces.
</Callout>

## Generating test telemetry with telemetrygen

Use telemetrygen to generate test traces, metrics, and logs to validate the Collector without instrumenting an application.

Install telemetrygen (Go required):

```bash theme={null}
# Optionally set GOBIN so go installs to a known dir
export GOBIN=$(go env GOPATH)/bin

# Install the telemetrygen CLI
go install github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest
```

Generate traces (OTLP via HTTP, insecure—suitable for local testing):

```bash theme={null}
$GOBIN/telemetrygen traces --otlp-http --otlp-insecure --traces 3
```

Expected telemetrygen output (informational):

```plaintext theme={null}
2025-09-29T17:09:51.954-0600  INFO  traces/traces.go:40    starting HTTP exporter
2025-09-29T17:09:51.956-0600  INFO  traces/traces.go:118   generation of traces is limited {'per-second': 1}
```

Collector debug exporter will print received spans like:

```plaintext theme={null}
otel-collector  | Span #1
otel-collector  | Trace ID     : 79b8fc5226d6465d3237317511b05a98
otel-collector  | Parent ID    : bac24f1a582a5e8c
otel-collector  | ID           : lets-go
otel-collector  | Kind         : Client
otel-collector  | Start time   : 2025-09-29 23:09:51.95737 +0000 UTC
otel-collector  | End time     : 2025-09-29 23:09:51.957493 +0000 UTC
otel-collector  | Attributes:
otel-collector  |    -> network.peer.address: Str(1.2.3.4)
otel-collector  |    -> peer.service: Str(telemetrygen-server)
otel-collector  | 2025-09-29T23:09:51.957493Z info  ResourceSpans #0
otel-collector  | Resource SchemaURL: https://opentelemetry.io/schemas/1.37.0
otel-collector  | Resource attributes:
otel-collector  |    -> service.name: Str(telemetrygen)
```

Generate logs:

```bash theme={null}
$GOBIN/telemetrygen logs --otlp-http --otlp-insecure --logs 3
```

Collector debug output for logs:

```plaintext theme={null}
otel-collector | 2025-09-29T23:11:22.712Z info Logs {"resource": {"service.name": "otelcol-contrib"}, "otelcol.component.id": "debug", "otelcol.signal": "logs", "resource logs": 1, "log records": 1}
otel-collector | LogRecord #0
otel-collector | Timestamp: 2025-09-29T23:11:21.730219Z
otel-collector | SeverityText: Info
otel-collector | Body: Str(the message)
otel-collector | Attributes:
otel-collector |   -> app: Str(server)
```

If you see the spans and log records printed, the pipelines are functioning and the Collector is receiving and exporting telemetry correctly.

## Common receivers and exporters (quick reference)

| Category  | Examples                                                   | When to use                                                                      |
| --------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Receivers | `otlp`, `prometheus`, `jaeger`, `fluentforward`, `kafka`   | Use based on the telemetry source (instrumentation, agent, or external pipeline) |
| Exporters | `otlp`, `prometheus`, `jaeger`, `zipkin`, `kafka`, `debug` | Send telemetry to vendor ingest, monitoring systems, or stdout for testing       |

## Extending this configuration

* Replace the `debug` exporter with a production backend exporter (e.g., OTLP to vendor ingest, Prometheus remote write, Jaeger, Zipkin, Kafka).
* Add processors like `batch`, `memory_limiter`, `resource`, or `attributes` to shape telemetry.
* Add multiple receivers and create pipelines that route different signals to different exporters.
* For production, enable TLS/authentication for receivers and exporters, and tune processor parameters (e.g., `batch` sizes, sampling rate).

## Final full example (copy/paste)

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors: {}

exporters:
  debug:
    verbosity: detailed

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

## Links and references

* [OpenTelemetry Collector — official docs](https://opentelemetry.io/docs/collector/)
* [OpenTelemetry Collector Contrib repository](https://github.com/open-telemetry/opentelemetry-collector-contrib)
* [telemetrygen (telemetry generator) — contrib command](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen)
* [Kubernetes Concepts (for running Collector in K8s)](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

This concludes the basic OpenTelemetry Collector configuration guide: receivers, processors, exporters, wiring, validation, and local testing using the debug exporter and telemetrygen.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/d8eb9774-43b0-441c-9361-96903e7e2135" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/5787e363-fb66-4f68-a9b1-77367dc3d3a7" />
</CardGroup>


# OTel Collector Anatomy

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/OTel-Collector-Anatomy/page

High-level overview of OpenTelemetry Collector architecture showing receivers, processors, exporters, connectors, and extensions for handling traces, metrics, and logs through configurable pipelines.

In this lesson we present a concise, high-level overview of the OpenTelemetry Collector architecture and how telemetry flows through it. Understanding these building blocks will help you design robust, scalable observability pipelines for traces, metrics, and logs.

Everything begins with telemetry sources — the origins of your data. Typical examples include:

* Traces emitted by application instrumentation (e.g., OpenTelemetry SDKs).
* Metrics scraped from a Prometheus server or exposed by applications.
* Logs from files, agents, or structured log streams.

The Collector ingests these inputs and moves them through a configurable pipeline where each component performs a focused responsibility.

## Receivers

Receivers are the Collector's entry points. They accept data over external protocols and translate it into the Collector's internal data model. Each signal type (traces, metrics, logs) usually has its own receiver implementations. Common examples include `otlp`, `prometheus`, `jaeger`, and `filelog`.

Key responsibilities:

* Decode wire formats (gRPC, HTTP, protobuf, text).
* Perform protocol-specific validation or minimal parsing.
* Hand data into the Collector's internal pipeline model.

## Processors

Processors operate on data after reception but before export. They refine, enrich, and reduce data volumes to prepare telemetry for backends.

Typical processor tasks:

* Batching: group items to increase throughput and reduce exporter load.
* Filtering and routing: drop or route data based on attributes.
* Transformation / enrichment: add or rewrite attributes, map resource information.
* Sampling: keep a representative subset of spans to control costs.

<Callout icon="warning">
  Processor order matters. Place `sampling` before `batch` when you need to avoid batching sampled-out items, and apply `resource`/`attributes` processors early if later processors rely on those attributes.
</Callout>

## Exporters

Exporters convert the Collector's internal model into backend-specific wire formats and transmit data over HTTP, gRPC, or other protocols. Examples include exporters for `otlp`, `prometheus`, `logging`, and commercial backends.

Exporter responsibilities:

* Marshal data to the target format (JSON, protobuf).
* Manage network communication, retries, and timeouts.
* Optionally implement buffering or queuing logic.

## Pipelines and Service

Each signal type (traces, metrics, logs) runs in its own pipeline configured under the Collector's `service` section. A pipeline executes components in sequence:

receiver -> processor(s) -> exporter

This modular architecture lets you configure independent processing paths for each signal type and tailor behavior to different backends.

Example pipeline configuration (YAML):

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp, jaeger]
      processors: [batch, resource, tail_sampling]
      exporters: [otlp, logging]
    metrics:
      receivers: [prometheus]
      processors: [memory_limiter]
      exporters: [prometheus_remote_write, logging]
```

<Callout icon="lightbulb">
  Each pipeline is signal-specific (traces, metrics, logs). Receivers translate protocols, processors modify or enrich data, and exporters deliver processed telemetry to your chosen backends.
</Callout>

## Connectors

Connectors bridge data between pipelines or transform one signal into another. Use cases include:

* Deriving metrics from traces (e.g., counting specific trace events).
* Routing logs into metrics or traces for correlation.
* Forwarding data from one pipeline to another without touching the original instrumentation.

Connectors enable cross-signal workflows and richer observability without changing application code.

## Extensions

Extensions run outside the main signal pipelines and add operational capabilities to the Collector process itself. Examples:

* Health checks and readiness probes.
* zPages for debugging and insight into internal state.
* Authentication, TLS termination, and observability endpoints.

<Frame>
  <img alt="The image illustrates the architecture of an OpenTelemetry Collector, detailing how it processes traces, metrics, and logs from various sources to different backends through receivers, processors, and exporters. It also includes service extensions like health checks and zPages." />
</Frame>

## Putting it all together

Telemetry enters via receivers, flows through configured processors inside a pipeline, and exits through exporters to one or more backends. Connectors let you bridge pipelines when you need cross-signal conversions, while extensions provide operational and administrative capabilities for the Collector process itself.

This architecture allows you to compose multiple independent pipelines and components to match your deployment, scaling, and observability requirements.

## Component Summary

| Component Type | Purpose                                                          | Examples                                                 |
| -------------: | ---------------------------------------------------------------- | -------------------------------------------------------- |
|      Receivers | Ingest and translate external protocols into the Collector model | `otlp`, `prometheus`, `jaeger`, `filelog`                |
|     Processors | Enrich, filter, sample, and batch telemetry                      | `batch`, `attributes`, `tail_sampling`, `memory_limiter` |
|      Exporters | Send processed telemetry to backends                             | `otlp`, `prometheus_remote_write`, `logging`             |
|     Connectors | Bridge or convert between signal pipelines                       | `metrics_from_traces`, `logs_to_metrics`                 |
|     Extensions | Operational endpoints and management features                    | `health_check`, `zpages`, `pprof`                        |

## Best Practices

* Design pipelines around signal types to keep configuration clear and maintainable.
* Use batching and memory-limiting processors to avoid spikes in exporter load.
* Apply sampling strategically to control cost while preserving signal fidelity.
* Monitor the Collector (using extensions like zPages or Prometheus metrics) to detect backpressure and resource issues.

## Links and References

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Collector GitHub repo: [https://github.com/open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector)
* OpenTelemetry Specification: [https://github.com/open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification)

<Callout icon="lightbulb">
  Start small: configure a single pipeline, validate end-to-end telemetry flow, then iterate with processors and exporters as your needs grow.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/bb91b22f-c7d4-4279-9c6b-ef4a21d5f815" />
</CardGroup>
