# Demo Internal Metrics of the Collector

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Demo-Internal-Metrics-of-the-Collector/page

How to expose, inspect, and interpret OpenTelemetry Collector internal metrics in Prometheus format and configure scraping and scaling

This guide shows how to expose and inspect the OpenTelemetry Collector's internal telemetry (metrics) in Prometheus exposition format. You will learn how to enable the collector to serve Prometheus-format metrics and how to interpret the most useful metric families for debugging and scaling.

* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Prometheus exposition format: [https://prometheus.io/docs/instrumenting/exposition\_formats/](https://prometheus.io/docs/instrumenting/exposition_formats/)

## What you will do

1. Optionally enable the zpages extension for quick debugging.
2. Add a metrics pipeline that includes the Prometheus receiver.
3. Configure `telemetry.metrics.readers` to expose the Collector's internal metrics in Prometheus format on a chosen host:port.

## Minimal example configuration

The following corrected YAML config shows the minimal settings to expose internal Collector metrics via a Prometheus reader. Place this in your Collector config file (e.g., `collector-config.yaml`) and restart the Collector.

```yaml theme={null}
zpages:
  endpoint: 0.0.0.0:55679

service:
  extensions: [health_check, pprof, zpages]
  pipelines:
    logs:
      receivers: [filelog]
      processors: [attributes, resourcedetection]
      exporters: [otlphttp/dynatrace, otlp/collector2]

    # Metrics pipeline - internal collector metrics
    metrics:
      receivers: [prometheus]
      processors: [resourcedetection, cumulativetodelta]
      exporters: [otlphttp/dynatrace, debug]

telemetry:
  logs:
    level: "INFO" # DEBUG | INFO | WARN | ERROR
  metrics:
    level: detailed
    readers:
      - pull:
          exporter:
            prometheus:
              host: "0.0.0.0"
              port: 8888
```

Notes:

* This example exposes internal metrics on port `8888`. Adjust `host` and `port` to match your network and security requirements.
* After applying the configuration, visit `http://<collector-ip>:8888/metrics` to view the Prometheus-format metrics.

<Callout icon="lightbulb">
  Exposed metrics are presented in Prometheus exposition format. Some metric names are marked `[alpha]`, which indicates experimental metrics that may change across Collector releases.
</Callout>

## Typical Prometheus-format metric excerpts

Below are representative metric families and sample lines you will commonly see from the Collector. The examples are cleaned up for clarity.

* Instrumentation scope metadata and exporter queue capacity/size:

```text theme={null}
