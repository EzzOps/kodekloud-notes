# No service.telemetry.logs section configured
# Even without a service.telemetry.logs section, logs appear at the default INFO level.
```

When you run the Collector with this config, you will see internal logs like the example below printed to the console:

```powershell theme={null}
PS C:\ProgramData\OpenTelemetry Collector> otelcol-contrib --config .\nop.yaml
2025-11-09T18:49:19.745+1100 info service@v0.132.0/service.go:187 Setting up own {"resource": {"service.instance.id": "512d76cd-f7d6-4dee-ae03-a0fd687f6143", "service.name": "otelcol-contrib", "service.version": "0.132.0"}}
2025-11-09T18:49:19.745+1100 info service@v0.132.0/service.go:249 Starting otelcol-contrib... {"resource": {"service.instance.id": "512d76cd-f7d6-4dee-ae03-a0fd687f6143", "service.name": "otelcol-contrib", "service.version": "0.132.0"}, "Version": "0.132.0"}
2025-11-09T18:49:19.745+1100 info extensions/extensions.go:41 Starting extensions... {"resource": {"service.instance.id": "512d76cd-f7d6-4dee-ae03-a0fd687f6143", "service.version": "0.132.0"}}
2025-11-09T18:49:19.745+1100 info service@v0.132.0/service.go:272 Everything is ready. {"resource": {"service.instance.id": "512d76cd-f7d6-4dee-ae03-a0fd687f6143", "service.name": "otelcol-contrib", "service.version": "0.132.0"}}
```

These messages indicate the Collector version, a unique service instance ID, and readiness confirmations.

## Where to view Collector logs in production

Common ways to stream Collector logs by environment:

| Environment     | Command                                                         |
| --------------- | --------------------------------------------------------------- |
| Linux (systemd) | `sudo journalctl -u otelcol-contrib -f`                         |
| Docker          | `docker logs -f otelcol`                                        |
| Kubernetes      | `kubectl logs -n observability <pod-name> -c otel-collector -f` |

Tip: in Kubernetes, replace `<pod-name>` with your actual Collector pod name or use a label selector with `-l`. See [Kubernetes Logs](https://kubernetes.io/docs/concepts/cluster-administration/logging/) for more details.

## Configuring service.telemetry.logs

To control Collector internal logging (verbosity, format, sampling, and destinations), add a `service.telemetry.logs` block under `service`. The `level` field accepts `DEBUG`, `INFO`, `WARN`, and `ERROR`.

* DEBUG: detailed component-level activity — useful for development and troubleshooting.
* INFO: default operational messages.
* WARN / ERROR: reduce output to only problematic events — recommended for production.

Example: enable debug-level logs to get more detailed initialization output:

```powershell theme={null}
PS C:\ProgramData\OpenTelemetry Collector> otelcol-contrib --config .\nop-w-telemetry.yaml
2025-11-09T19:04:35.396+1100 info  service@v0.132.0:187 Setting up own telemetry... {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0"}}
2025-11-09T19:04:35.397+1100 debug builders/builders.go:24 Beta component. May change in the future. {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0", "otelcol.component.id": "nop", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}}
2025-11-09T19:04:35.397+1100 debug builders/builders.go:24 Beta component. May change in the future. {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0", "otelcol.component.id": "nop", "otelcol.component.kind": "receiver", "otelcol.signal": "traces"}}
2025-11-09T19:04:35.397+1100 info  service@v0.132.0/service.go:249 Starting otelcol-contrib... {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0"}, "Version": "0.132.0"}
2025-11-09T19:04:35.397+1100 info  extensions/extensions.go:41 Starting extensions... {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0"}}
2025-11-09T19:04:35.397+1100 info  service@v0.132.0/service.go:272 Everything is ready. {"resource": {"service.instance.id": "21fa506d-662f-467f-9e0c-77de328804d6", "service.name": "otelcol-contrib", "service.version": "0.132.0"}}
```

YAML to set the level to DEBUG:

```yaml theme={null}
service:
  telemetry:
    logs:
      level: "DEBUG"
```

For production use a higher threshold such as ERROR:

```yaml theme={null}
service:
  telemetry:
    logs:
      level: "ERROR"  # DEBUG | INFO | WARN | ERROR
```

> **warning** Writing logs to local files or enabling DEBUG in production can increase disk usage and expose sensitive details. Review retention and access controls if you persist Collector logs.

## Advanced logging options

Beyond `level`, the `service.telemetry.logs` block supports additional fields to fine-tune behavior: `development`, `encoding`, caller info, stack traces, sampling, and output paths.

Example advanced configuration:

```yaml theme={null}
service:
  telemetry:
    logs:
      level: "DEBUG"                              # DEBUG | INFO | WARN | ERROR
      development: true                           # Enables developer mode (richer error context)
      encoding: json                              # "console" (default) or "json"
      disable_caller: false                       # Include source file & line number in log messages
      disable_stacktrace: false                   # Include stacktraces for WARN/ERROR logs
      sampling:
        enabled: true                             # Enable log sampling to prevent floods
        tick: 5s                                  # Reset sampling every 5 seconds
        initial: 5                                # Log the first 5 identical messages
        thereafter: 50                            # Then log every 50th repeated message
      output_paths: ["stderr", "/var/log/otelcol.log"]       # Normal logs (stderr or file paths)
      error_output_paths: ["/var/log/otelcol_error.log"]     # Error logs (file paths or stderr)
      initial_fields:                             # Key-value pairs added to every log entry
        service: "otelcol-contrib"
        environment: "dev-lab"
```

Notes:

* Use `encoding: json` for structured logs that integrate with log aggregation systems.
* Enable `sampling` to prevent repeated identical messages from flooding logs.
* `output_paths` and `error_output_paths` let you persist logs to files in addition to stderr.

<Frame>
  <img alt="The image is a table outlining various logging settings, their default values, purposes, and typical use cases. It provides guidance on configuring logging for different scenarios such as debugging, development, and high-volume environments." />
</Frame>

## Structured logging and troubleshooting

When `encoding: json` is enabled, each log line is a JSON object which is much easier to ingest and query in centralized log systems. During debugging, keep `disable_stacktrace: false` and `disable_caller: false` to get file/line and stack traces for errors.

Example pipeline + telemetry configuration — ensure the `telemetry` block is nested under `service`:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
      http:

exporters:
  debug:
    verbosity: detailed  # basic | normal | detailed

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
  telemetry:
    logs:
      level: "INFO"  # DEBUG | INFO | WARN | ERROR
```

This setup validates pipelines and allows you to inspect telemetry data and internal Collector logs via the `debug` exporter.

## Quick references

Log level summary:

| Level | Purpose                                | When to use                                     |
| ----- | -------------------------------------- | ----------------------------------------------- |
| DEBUG | Verbose, component-level messages      | Development, deep troubleshooting               |
| INFO  | General operational messages (default) | Normal operations, startup checks               |
| WARN  | Warnings about potential issues        | Restricted noise while still surfacing concerns |
| ERROR | Only errors                            | Production when you want minimal logs           |

Commands to stream Collector logs (repeat):

| Platform   | Example                                                                      |
| ---------- | ---------------------------------------------------------------------------- |
| systemd    | `sudo journalctl -u otelcol-contrib -f`                                      |
| Docker     | `docker logs -f otelcol`                                                     |
| Kubernetes | `kubectl logs -n observability \` + "`<pod-name>`" + ` -c otel-collector -f` |

## Key takeaways

* `service.telemetry.logs.level` controls the Collector's internal log verbosity (this is separate from telemetry data you collect or export).
* By default, the Collector emits INFO-level logs to `stderr`.
* Use `journalctl`, `docker logs`, or `kubectl logs` to access Collector logs in common environments.
* Tune `level`, `encoding`, `sampling`, and `output_paths` to balance visibility and performance.
* Persist or forward internal logs to a centralized backend to aid cross-system troubleshooting and historical analysis.

<Frame>
  <img alt="The image outlines key takeaways related to service telemetry logs, including details on log control, verbosity, export, and debugging for centralized monitoring and troubleshooting." />
</Frame>

This is the first place to inspect when validating pipeline initialization or diagnosing why telemetry data is not reaching its backend. For more details, see the Collector documentation and the OpenTelemetry specifications:

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Kubernetes logging: [https://kubernetes.io/docs/concepts/cluster-administration/logging/](https://kubernetes.io/docs/concepts/cluster-administration/logging/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/a1ac613f-7abd-4588-9cff-80505f44f58b)


# Internal Metrics of the Collector

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Internal-Metrics-of-the-Collector/page

Guide to OpenTelemetry Collector internal telemetry, exposing Prometheus metrics, health checks, zPages and pprof for diagnosing performance, resource issues, and troubleshooting pipelines.

In this lesson we continue the Collector diagnostics journey by focusing on internal telemetry. Telemetry logs show activities across the Collector, while internal metrics reveal how each component is performing over time. The OpenTelemetry Collector exposes built-in telemetry (Prometheus format) and several debugging extensions for deeper inspection. Together, these signals provide a clear view of Collector health, performance, and where to investigate when things go wrong.

Key diagnostic tools and endpoints:

* Internal metrics (Prometheus format) for runtime visibility and alerting.
* Health checks to confirm the Collector is up and ready.
* zPages to inspect live traces, spans, and internal workings of receivers and exporters.
* Performance profiler (pprof) for detailed CPU and memory profiling.

> **lightbulb** pprof is an advanced diagnostic tool used for deep performance investigations. It’s usually not necessary for routine troubleshooting.

<Frame>
  <img alt="The image is a diagram titled &#x22;Exploring Internal Telemetry Endpoints,&#x22; featuring the &#x22;OpenTelemetry Collector&#x22; and various components like Metrics, Health Checks, zPages, and pprof." />
</Frame>

Why these endpoints matter

* Metrics let you quantify throughput, error rates, drops, and resource pressure.
* Health checks give a quick boolean of liveness/readiness.
* zPages provide an interactive look at pipeline internals without stopping the Collector.
* pprof helps find hotspots, memory leaks, and expensive code paths.

Tool summary

| Diagnostic tool               | Purpose                                                            | Where to learn more                  |
| ----------------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| Internal metrics (Prometheus) | Monitor pipeline throughput, failures, queue sizes, resource usage | [Prometheus](https://prometheus.io/) |
| Health checks                 | Liveness/readiness probes for orchestration platforms              | Collector docs                       |
| zPages                        | Live inspection of receivers/exporters and internal spans          | zPages extension                     |
| pprof                         | CPU/memory profiling for deep performance analysis                 | `net/http/pprof` docs                |

> **warning** Important: Do not expose Collector telemetry endpoints (metrics, pprof, zPages, health) to the public internet. Restrict access with network controls, authentication, or internal-only interfaces.

How the Collector exposes internal metrics
By default many Collector setups expose internal metrics on port 8888 via a Prometheus pull-style reader. Example telemetry configuration:

```yaml theme={null}
service:
  telemetry:
    metrics:
      readers:
        - pull:
            exporter:
              prometheus:
                host: "0.0.0.0"
                port: 8888
```

You can change the port or binding as needed to fit your deployment model. The metrics are available at `http://<collector-host>:8888/metrics` (or the host/port you configure).

What these metrics reveal
Internal metrics provide insights into:

* Pipeline health and stability
* Throughput for receivers, processors, and exporters
* Performance hotspots and bottlenecks
* Backpressure and queue growth indicating possible drops
* Resource pressure (CPU, memory) and potential leaks
* Which components are loaded and their versions (metadata)

<Frame>
  <img alt="The image is a table listing various metrics related to telemetry, organized into categories such as Receiver, Exporter, Processor, and Process/Resource Metrics. It details metric names, types, descriptions of what they measure, and when they are useful." />
</Frame>

Naming pattern overview
Metrics follow a consistent, readable pattern. Parse names logically rather than memorizing them.

* Prefix: `otelcol_` — indicates the metric is from the OpenTelemetry Collector.
* Component: `receiver`, `exporter`, `processor`, `extension`, etc.
* Signal (optional): `traces`, `metrics`, `logs`.
* Suffix: e.g., `_total` for counters, `_bytes`, `_duration_seconds`.

Common examples and what to look for

* Receiver activity: `otelcol_receiver_accepted_traces_total` — incoming traffic accepted by receivers.
* Refused/Rejected metrics: `otelcol_receiver_refused_traces_total` — indicates drops due to limits or malformed inputs.
* Exporter success/failure: `otelcol_exporter_sent_spans_total`, `otelcol_exporter_send_failed_spans_total` — failures often mean connectivity/backend issues.
* Queue/Buffer metrics: queue size growth suggests backpressure or downstream slowness.
* Processor metrics: batch sizes and timeout metrics help tune throughput vs. latency.
* Process/resource metrics: CPU, memory, heap allocations (`process_cpu_seconds_total`, memory-related metrics) show resource pressure.
* Metadata metrics: `otel_scope_info` and similar indicate active components and versions.

<Frame>
  <img alt="The image is a table listing OpenTelemetry metrics with categories, metric names, types, descriptions of what they measure, and their use cases." />
</Frame>

Example: Prometheus-format metrics output
Here is a sample of metrics as exposed by the Collector (available at `http://<collector-host>:8888/metrics` when using the example config above):

```text theme={null}
