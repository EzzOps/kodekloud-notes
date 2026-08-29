# OTel Col Load Balancing Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/OTel-Col-Load-Balancing-Exporter/page

Explains the OpenTelemetry Collector load balancing exporter, its use cases, routing key options, resolver types, and configuration patterns for sticky, reliable routing of telemetry to downstream collectors.

This article explains the OpenTelemetry Collector load-balancing exporter: what it does, common use cases, routing key options, resolver types, and practical configuration patterns for reliable, sticky routing of telemetry to downstream collectors.

What the load-balancing exporter does

* Distributes telemetry (traces, metrics, logs) across a pool of downstream collectors (backends).
* Ensures related telemetry stays "sticky" to the same backend using a routing key so downstream processors (e.g., tail-based samplers) can operate on complete data.
* Creates an OTLP sub-exporter per backend so each backend gets independent queuing, retries, and resilience behavior.

Common uses

* Tail-based sampling: keep all spans of a trace together so downstream samplers can decide with full trace context.
* Sharding hot services: route high-volume services to a dedicated collector group.
* Metric scaling: shard metric streams across backends to balance ingestion.

Routing keys overview

Choose a routing key that preserves the consistency required by your downstream processing. The following table summarizes the most common routing key choices and when to use them.

| Routing key  | Applies to                             | Purpose / When to use                                                                                   |
| ------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `traceID`    | Traces                                 | Default for traces. Keeps all spans of a trace on the same backend — essential for tail-based sampling. |
| `service`    | Traces & Metrics (default for metrics) | Routes by `service.name`. Useful for grouping telemetry at the service level.                           |
| `resource`   | Traces & Metrics                       | Routes by resource attributes (e.g., host, deployment). Use to group telemetry by resource identity.    |
| `metric`     | Metrics only                           | Routes by metric name. Good for coarse metric sharding.                                                 |
| `streamID`   | Metrics only                           | Routes by metric stream ID (hash of attributes). Most granular for metrics.                             |
| `attributes` | Traces & Metrics                       | Custom attribute routing. Requires a `routing_attributes` list to define keys to hash on.               |

<Callout icon="lightbulb">
  Choose the routing key that preserves the data consistency you need. For tail-based sampling, prefer `traceID`. For metric sharding, prefer `metric` or `streamID`.
</Callout>

Example: routing\_key variants

```yaml theme={null}
