# Understanding configyaml in OpenTelemetry Collector

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/Understanding-configyaml-in-OpenTelemetry-Collector/page

Guide to OpenTelemetry Collector config.yaml explaining component structure, wiring receivers processors exporters into pipelines, connectors, multi-file splitting, and environment variable parameterization for production deployments.

This guide explains how the OpenTelemetry Collector parses and uses the `config.yaml` file. You'll learn the configuration structure, how to wire receivers/processors/exporters into pipelines, how connectors enable cross-pipeline flows, and how to split and parameterize configuration for production use.

The Collector configuration is organized by component type. The primary groups are:

| Component  | Purpose                                                      | Example                                         |
| ---------- | ------------------------------------------------------------ | ----------------------------------------------- |
| receivers  | Ingest telemetry (traces, metrics, logs)                     | `otlp` receiving gRPC on `0.0.0.0:4317`         |
| processors | Transform, filter, or batch data inside pipelines (optional) | `batch`, `attributes`                           |
| exporters  | Send telemetry to backends                                   | `otlp`, `prometheus`, `debug`                   |
| connectors | Bridge pipelines (acts as exporter and receiver)             | `count` connector producing metrics from traces |
| extensions | Run outside pipelines (health checks, zPages, auth)          | `health_check`, `zpages`                        |
| service    | Declares enabled extensions and `pipelines` wiring           | `service.pipelines.traces`                      |

High-level conceptual layout:

```yaml theme={null}
