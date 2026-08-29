# Tail Sampling

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Tail-Sampling/page

Tail sampling for OpenTelemetry Collector that defers sampling until traces complete, evaluates ordered policies to retain outcome relevant traces while managing memory, latency, and scaling

Tail sampling defers the sampling decision until a trace completes — after all spans for that trace have been collected. This lets you make decisions using the trace’s final outcome (errors, latency, span counts, attributes) instead of sampling early without full context.

When traces arrive at an OpenTelemetry Collector, the tail sampler buffers each trace until it finishes (or the configured decision wait expires). The sampler evaluates policies in order, retains traces that match a policy, and drops or further samples the remainder. Selected traces are then exported to the configured backend.

Example high-level tail-sampling configuration:

```yaml theme={null}
