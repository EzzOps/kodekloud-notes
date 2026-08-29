# Demo OpenTelemetry Collector Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/Demo-OpenTelemetry-Collector-Configuration/page

Guide to configuring an OpenTelemetry Collector with a single YAML file, covering receivers, processors, exporters, pipelines, validation, Docker usage, telemetrygen testing, and production extension tips.

This guide demonstrates how to configure an OpenTelemetry Collector using a single YAML file. It covers the top-level sections, a minimal working example, how to validate the configuration, running the Collector (Docker example), generating test telemetry with telemetrygen, and suggestions for extending the configuration for production.

Core Collector configuration sections (in order):

* `receivers`: how the Collector accepts telemetry (from applications, agents, or other collectors)
* `processors`: optional transformers, batching, filtering, sampling, etc.
* `exporters`: destinations for processed telemetry (backends, files, console)
* `service.pipelines`: wiring that connects `receivers` → `(processors)` → `exporters` for each signal (`traces`, `metrics`, `logs`)

Summary table of the top-level sections:

| Section             | Purpose                                                                            | Example snippet                                                                         |
| ------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `receivers`         | Defines how telemetry is ingested (OTLP, Jaeger, Prometheus, Fluent Forward, etc.) | `yaml\nreceivers:\n  otlp:\n    protocols:\n      grpc: {}\n`                           |
| `processors`        | Optional processing (batching, sampling, resource enrichment)                      | `yaml\nprocessors:\n  batch: {}\n`                                                      |
| `exporters`         | Where telemetry is sent (OTLP, Prometheus, Jaeger, logging/debug)                  | `yaml\nexporters:\n  otlp:\n    endpoint: example:4317\n`                               |
| `service.pipelines` | Connects receivers → processors → exporters per signal                             | `yaml\nservice:\n  pipelines:\n    traces: { receivers: [otlp], exporters: [debug] }\n` |

## Minimal configuration skeleton

A minimal skeleton to remind the top-level layout:

```yaml theme={null}
receivers:

processors:

exporters:

service:
  pipelines:
    traces: {}
    metrics: {}
    logs: {}
```

Validate a Collector config with the built-in validator:

```bash theme={null}
otelcol validate --config=customconfig.yaml
```

Note: Use the correct binary for your distribution (for example `otelcol` or `otelcol-contrib`).

> **lightbulb** If validation fails, carefully check YAML indentation and keys—most issues are typos or mis-indentation. You can also run `otelcol --config customconfig.yaml --dry-run` with some builds to surface runtime validation errors.

## Receivers

Receivers determine how the Collector accepts telemetry. The Collector supports many receiver types (examples: Fluent Forward, Prometheus, Jaeger, Kafka, OpenCensus, OTLP, Zipkin). Below are example snippets for several common receivers.

Example receiver snippets:

```yaml theme={null}
receivers:
  # Fluent Forward (logs)
  fluentforward:
    endpoint: 0.0.0.0:8006

  # Host-level metrics (Linux)
  hostmetrics:
    scrapers:
      cpu:
      disk:
      filesystem:
      load:
      memory:
      network:
      process:
      processes:
        paging:

  # Jaeger traces
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      thrift_binary:
      thrift_compact:
      thrift_http:

  # Generic Kafka receiver
  kafka:
    protocol_version: 2.0.0
```

OTLP receiver (recommended for examples & local testing — supports gRPC and HTTP):

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

Notes:

* `0.0.0.0` binds to all interfaces. For local-only testing, use `127.0.0.1` or a specific interface.
* Add TLS (cert/key) or authentication under each protocol if required.

## Processors

Processors run between receivers and exporters and can transform, filter, aggregate, or limit telemetry. Common processors: `batch`, `memory_limiter`, `attributes`, `resource`, `probabilistic_sampler`. Processors are optional—omit them for minimal configs.

Example placeholder:

```yaml theme={null}
