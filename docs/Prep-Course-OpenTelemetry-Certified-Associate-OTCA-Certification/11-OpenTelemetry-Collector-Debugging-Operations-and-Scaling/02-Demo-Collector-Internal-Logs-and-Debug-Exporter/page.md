# Demo Collector Internal Logs and Debug Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Demo-Collector-Internal-Logs-and-Debug-Exporter/page

Guide explaining an OpenTelemetry Collector contrib configuration including receivers processors exporters extensions telemetry settings and using the debug exporter to inspect internal metrics and logs

This guide walks through a live OpenTelemetry Collector (contrib) configuration — the exact config used on the host at `/etc/otelcol-contrib/config.yaml`. It explains how receivers, processors, exporters, extensions, service pipelines, and the `telemetry` / `debug` exporter interact. You’ll also learn how to control Collector log verbosity via the `telemetry` section and how to adjust the debug exporter verbosity to inspect metric/log payloads.

To edit the config file:

```bash theme={null}
sudo nano /etc/otelcol-contrib/config.yaml
```

## Receivers

This Collector uses two receivers:

* `filelog` — tails a JSON file and emits log entries.
* `prometheus` — exposes/scrapes internal Collector metrics for pipelines.

Quick receiver summary:

|     Receiver | Purpose                | Typical use-case                                           |
| -----------: | ---------------------- | ---------------------------------------------------------- |
|    `filelog` | Tail file-based logs   | Read application or device JSON logs (e.g., aircraft.json) |
| `prometheus` | Expose/collect metrics | Scrape internal Collector metrics or application metrics   |

Example receiver section:

```yaml theme={null}
receivers:
  filelog:
    include: ["/run/dump1090-mutability/aircraft.json"]
    start_at: beginning
    include_file_path: true
    multiline:
      line_start_pattern: '^\{'

  # Prometheus receiver to scrape internal collector metrics
  prometheus:
    config:
      scrape_configs:
        - job_name: 'otelcol-internal-metrics'
          scrape_interval: 30s
          static_configs:
            - targets: ['localhost:8888']
              labels:
                collector_instance: 'rpi24-adsb-collector'
                environment: 'production'
```

## Processors

Processors enrich, transform, or otherwise manipulate telemetry data before export. This configuration includes:

* `resource_detection` — auto-detect system/host attributes.
* `attributes` — upsert or transform log/metric attributes.
* `cumulativetodelta` — convert cumulative metrics to delta form (useful for backends expecting deltas).
* `transform/fix_names` — optional transform processor declared but not attached to pipelines by default.

Example processor declarations:

```yaml theme={null}
processors:
  resource_detection:
    detectors: [env, system]
    timeout: 5s
    override: false
    system:
      hostname_sources: ["os", "dns"]
      resource_attributes:
        host.name:
          enabled: true
        host.id:
          enabled: true
        host.arch:
          enabled: true
        host.cpu.vendor.id:
          enabled: true

  attributes:
    actions:
      - key: log.source
        value: opentelemetry-iot-dump1090-collector
        action: upsert
      - key: iot-device
        value: rpi24-adsb-receiver
        action: upsert
      - key: loglevel
        value: INFO
        action: upsert
      - key: device.address
        value: IJWJHUD768H
        action: upsert

  cumulativetodelta: {}

  transform/fix_names:
    error_mode: ignore
    metric_statements:
      - context: metric
        statements:
          - replace_pattern(name, "\\{", "-")
          - replace_pattern(name, "\\}", "-")
```

Note: To use the `transform/fix_names` processor, add it to a pipeline’s `processors` list (e.g., `processors: [resource_detection, transform/fix_names]`).

## Exporters

This configuration uses two OTLP exporters and the `debug` exporter for local inspection.

```yaml theme={null}
exporters:
  otlphttp/dynatrace:
    endpoint: "${DT_ENDPOINT}"
    headers:
      Authorization: "Api-Token ${DT_API_TOKEN}"

  otlp/collector2:
    endpoint: "192.168.1.88:44317"  # Update with actual collector-2 address
    tls:
      insecure: true  # In production, configure proper TLS

  debug:
    verbosity: detailed  # options: basic | normal | detailed
```

Tips:

* Replace `${DT_ENDPOINT}` and `${DT_API_TOKEN}` with actual Dynatrace OTLP HTTP endpoint and API token.
* Avoid `tls.insecure: true` in production; configure proper TLS for OTLP exporters.

## Extensions

Common extensions enable health checks, profiling, and zPages for debugging:

```yaml theme={null}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679
```

## Service and Pipelines

The `service` section wires receivers, processors, and exporters into pipelines. Important: the `debug` exporter must be listed in a pipeline for it to emit debug output for that signal.

```yaml theme={null}
service:
  extensions: [health_check, pprof, zpages]
  pipelines:
    logs:
      receivers: [filelog]
      processors: [attributes, resource_detection]
      exporters: [otlphttp/dynatrace, otlp/collector2]

    # Metrics pipeline - internal collector metrics
    metrics:
      receivers: [prometheus]
      processors: [resource_detection, cumulativetodelta]
      exporters: [otlphttp/dynatrace, debug]
```

## Telemetry (Collector internal logs & metrics)

The `telemetry` section controls the Collector’s own logs and how internal metrics are exposed to readers (e.g., Prometheus). Setting `telemetry.logs.level` adjusts the verbosity of the Collector’s operational logs.

Example telemetry block with metrics reader:

```yaml theme={null}
telemetry:
  logs:
    # level: "ERROR"  # DEBUG | INFO | WARN | ERROR
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

* If `telemetry.logs.level` is not set, the Collector defaults to `INFO`.
* The Prometheus reader above exposes internal metrics on the configured host/port so the Prometheus receiver (or other collectors) can scrape them.

## Viewing Collector logs

Follow the Collector service logs with systemd/journalctl:

```bash theme={null}
sudo journalctl -u otelcol-contrib -f
```

When `telemetry.logs.level` is not explicitly set, you’ll typically see info-level messages about receivers, exporters, and pipeline processing. If the `debug` exporter is included in a pipeline and `telemetry.logs.level` permits, you’ll also see debug exporter output in the logs.

## Changing Collector telemetry log level

To reduce log noise temporarily, set `telemetry.logs.level` to `"ERROR"` and restart the Collector:

```yaml theme={null}
telemetry:
  logs:
    level: "ERROR" # DEBUG | INFO | WARN | ERROR
  metrics:
    level: detailed
    readers:
      - pull:
          exporter:
            prometheus:
              host: "0.0.0.0"
              port: 8888
```

Restart the service:

```bash theme={null}
sudo systemctl restart otelcol-contrib
```

With `level: "ERROR"`, routine informational lines no longer appear in `journalctl`; only error-level telemetry is shown. Revert to `"INFO"` (or remove the setting) and restart to restore normal operational logs.

## Debug exporter verbosity

The `debug` exporter prints telemetry payloads to the Collector logs and has three verbosity levels:

* `basic` — minimal detail
* `normal` — more detail
* `detailed` — full metric data including histogram buckets and attributes

Example debug exporter configuration:

```yaml theme={null}
debug:
  verbosity: detailed  # basic | normal | detailed
```

To see debug exporter output for a given signal (e.g., metrics):

1. Ensure `debug` is declared under `exporters`.
2. Add `debug` to the pipeline’s `exporters` list for the signal you want to inspect.
3. Make sure `telemetry.logs.level` is at least `INFO` so the debug exporter prints to logs.

Example metrics pipeline that sends internal metrics to both Dynatrace and the debug exporter:

```yaml theme={null}
service:
  pipelines:
    metrics:
      receivers: [prometheus]
      processors: [resource_detection, cumulativetodelta]
      exporters: [otlphttp/dynatrace, debug]
```

## Common runtime commands

| Task              | Command                                      |
| ----------------- | -------------------------------------------- |
| Edit config       | `sudo nano /etc/otelcol-contrib/config.yaml` |
| Restart Collector | `sudo systemctl restart otelcol-contrib`     |
| Follow logs       | `sudo journalctl -u otelcol-contrib -f`      |

## Callouts

> **lightbulb** Ensure the `debug` exporter is declared under `exporters` and also listed in the pipeline `exporters` for the signal you want to inspect. Also keep `telemetry.logs.level` at or above `INFO` so debug exporter output is visible in logs.

> **warning** Do not use `tls.insecure: true` in production. Configure proper TLS for OTLP exporters and for any remote collectors to protect telemetry data.

## Summary

* Receivers collect logs and internal metrics (`filelog`, `prometheus`).
* Processors enrich and transform telemetry (`resource_detection`, `attributes`, `cumulativetodelta`, optional `transform`).
* Exporters send data to remote backends (`otlphttp/dynatrace`, `otlp/collector2`) and `debug` for local inspection.
* `telemetry` controls the Collector’s own logs and internal metrics exposure; adjust `telemetry.logs.level` to control noise.
* Use `debug` exporter with `verbosity: detailed` to inspect full payloads; use `basic` or `normal` to reduce output.
* After changing config, restart the service and follow logs with `journalctl -u otelcol-contrib -f`.

## Links and References

* OpenTelemetry Collector documentation: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Prometheus scrape configs: [https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape\_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config)
* Dynatrace OTLP ingestion (reference your Dynatrace docs for the exact endpoint and headers)

If you need an example to attach the `transform/fix_names` processor into a pipeline or want a sample `service` block with more pipelines (traces, logs, metrics) let me know and I’ll add a fully annotated example.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/4be96d1d-c9d9-4f65-aeff-2f110549c0f6)
