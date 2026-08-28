# Internal Logs of the Collector

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Internal-Logs-of-the-Collector/page

How to view and configure OpenTelemetry Collector internal logs, control log levels and formats, stream logs in environments, and troubleshoot startup and runtime issues

In this lesson we cover how to read and configure the OpenTelemetry Collector's internal logs to help diagnose startup, pipeline loading, configuration issues, and runtime problems.

By default the Collector writes internal logs to standard error (stderr) at the INFO level even if you do not configure `service.telemetry.logs`. These logs include startup/shutdown messages, pipeline readiness confirmations, component warnings, and metadata such as the Collector version and service instance ID.

<Callout icon="lightbulb">
  By default the Collector logs internal activity at INFO to standard error (`stderr`). This provides immediate visibility into startup and runtime behavior without adding any telemetry configuration.
</Callout>

## Minimal configuration example

A minimal Collector config without a `service.telemetry.logs` section still emits INFO logs to stderr:

```yaml theme={null}
receivers:
  # No-op receiver - does nothing, lightweight placeholder
  nop:

exporters:
  # No-op exporter - discards all data, lightweight placeholder
  nop:

service:
  pipelines:
    # noop traces pipeline
    traces:
      receivers: [nop]
      exporters: [nop]
