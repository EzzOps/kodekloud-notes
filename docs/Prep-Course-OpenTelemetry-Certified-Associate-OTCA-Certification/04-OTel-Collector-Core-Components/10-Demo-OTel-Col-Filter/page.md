# Demo OTel Col Filter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Demo-OTel-Col-Filter/page

Guide to using OpenTelemetry Collector filter processor to include or exclude metrics and logs, with regex examples, pipeline wiring, and best practices

In this lesson we cover the OpenTelemetry Collector filter processor to keep only the application metrics you care about (for example, temperature and humidity) and exclude the rest. We assume you already have metrics scraped from a Python application and are ingesting them via Prometheus or OTLP.

Problem: the application emits many metrics (for example `python_info`, `process_open_fds`, `process_cpu_seconds_total`, etc.) that you likely do not want to collect. Below is a small excerpt of scraped output showing both useful and noisy metrics:

```text theme={null}
-> DataType: Gauge
NumberDataPoints: #0
StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Timestamp: 2025-09-30 00:39:34.415 +0000 UTC
Value: 20480.000000
Metric #14
Descriptor:
  -> Name: current_temperature_fahrenheit_degF
  -> Description: Current Temperature
  -> Unit: degF
  -> DataType: Gauge
NumberDataPoints: #0
StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Timestamp: 2025-09-30 00:39:34.415 +0000 UTC
Value: 84.381217
Metric #15
Descriptor:
  -> Name: scrape_samples_scraped
  -> Description: The number of samples the target exposed
  -> Unit: 
  -> DataType: Gauge
NumberDataPoints: #0
StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Timestamp: 2025-09-30 00:39:34.415 +0000 UTC
Value: 19.000000
```

Resource metadata and other details are emitted as JSON-style resource attributes:

```json theme={null}
{"resource":{"service.instance.id":"52df403-4390-4afb-ab14-9736284847a8","service.name":"otelcol-contrib","service.version":"0.135.0","otelcol.component.id":"debug","otelcol.component":"metrics"}}
```

Goal: remove noisy metrics and keep only the ones you care about (for example `current_temperature_fahrenheit_degF` and `current_humidity_percentage`) using the filter processor.

Overview

* Add a `filter` processor under `processors`.
* Configure rules for metrics (either `include` or `exclude`) and choose a `match_type` (`strict`, `regexp`, `expr`).
* Wire the processor into the service pipeline so it runs for the intended telemetry type.
* Prefer `regexp` for flexible pattern matching.

> **lightbulb** Processor ordering matters: filter early in the pipeline (usually before heavy processors like `batch` or `attributes`) so unwanted telemetry is removed as soon as possible.

> **warning** Common startup errors stem from typos in the configuration keys. For example, use `metric_names` (not `metric_namees`). If the Collector fails on restart, inspect logs for configuration parse errors.

## Filter out metric names with a regular expression

Below is a minimal example that excludes metrics whose names start with `python` or `process`. Note the correct key is `metric_names`.

```yaml theme={null}
processors:
  filter:
    metrics:
      exclude:
        match_type: regexp
        metric_names:
          - "^(python|process).*"
  batch:
    timeout: 15s
    send_batch_size: 512
```

Make sure the `filter` processor is included in your metrics pipeline so it executes:

```yaml theme={null}
service:
  pipelines:
    metrics:
      receivers: [prometheus, otlp]
      exporters: [debug]
      processors: [filter, batch]
```

If you still see metrics such as `scrape_samples_scraped` after applying the filter, either update the regex to exclude them or switch to an include-only strategy (see the next section).

After the filter is applied, expected Collector output should include only application metrics like:

```text theme={null}
ResourceMetrics #0
  -> service.name: Str(python-app)
ScopeMetrics #0
Metric #0
  -> Name: current_temperature_fahrenheit_degF
  -> Description: Current Temperature
  -> Unit: degF
  -> DataType: Gauge
  -> Value: 77.01332

Metric #1
  -> Name: current_humidity_percentage
  -> Description: Current Humidity
  -> DataType: Gauge
  -> Value: 0.904944
```

## Include-only vs Exclude — which approach to use?

* Exclude approach: use `exclude` to remove undesired metrics by pattern. Useful when noise is limited to a few predictable prefixes.
* Include approach: use `include` to allow only the named metrics you want. Safer when you want to strictly control which metrics are collected.

Example: include-only for `current_temperature_fahrenheit_degF` and `current_humidity_percentage`:

```yaml theme={null}
processors:
  filter:
    metrics:
      include:
        match_type: regexp
        metric_names:
          - "^(current_temperature_fahrenheit_degF|current_humidity_percentage)$"
  batch:
    timeout: 15s
    send_batch_size: 512
```

Summary table — include vs exclude

| Strategy | Use case                                                   | Example pattern                            |                                    |
| -------- | ---------------------------------------------------------- | ------------------------------------------ | ---------------------------------- |
| Exclude  | Remove known noisy prefixes (e.g., Python runtime metrics) | \`^(python                                 | process).\*\`                      |
| Include  | Only allow a short, explicit set of metrics                | \`^(current\_temperature\_fahrenheit\_degF | current\_humidity\_percentage)\$\` |

## Filtering logs by severity

The filter processor can target logs as well. If your application emits logs at many severities (DEBUG, INFO, WARN, ERROR, FATAL) and you want to collect only ERROR and above, configure the logs section of the filter processor.

Example log severity samples:

```text theme={null}
SeverityText: DEBUG
SeverityNumber: Debug(5)
Body: Str(DEBUG:root:Ip address 172.16.1.1 sent request)

SeverityText: WARN
SeverityNumber: Warn(13)
Body: Str(WARNING:root:Email has been sent)

SeverityText: FATAL
SeverityNumber: Fatal(21)
Body: Str(FATAL:root:Catastrophic failure)
```

Filter configuration to include only ERROR+ logs and exclude noisy metrics:

```yaml theme={null}
processors:
  filter:
    logs:
      include:
        severity_number:
          min: ERROR
    metrics:
      exclude:
        match_type: regexp
        metric_names:
          - "^(python|process).*"
  batch:
    timeout: 15s
    send_batch_size: 512
  attributes/add_env:
    actions:
      - key: deployment.environment
        value: production
        action: insert
```

Wire the filter into both logs and metrics pipelines:

```yaml theme={null}
service:
  pipelines:
    logs:
      receivers: [otlp]
      exporters: [debug]
      processors: [filter, batch]
    metrics:
      receivers: [prometheus, otlp]
      exporters: [debug]
      processors: [filter, batch]
```

After restarting the Collector and running your logging workload, only ERROR and FATAL lines should appear in Collector output; INFO/DEBUG will be filtered out.

## Full processors example (combined)

A consolidated processors block that demonstrates metrics exclusion, logs inclusion, batching, and an attributes inserter:

```yaml theme={null}
processors:
  filter:
    metrics:
      exclude:
        match_type: regexp
        metric_names:
          - "^(python|process).*"
    logs:
      include:
        severity_number:
          min: ERROR
  batch:
    timeout: 15s
    send_batch_size: 512
  attributes/add_env:
    actions:
      - key: deployment.environment
        value: production
        action: insert
```

Reference the processors by name in each pipeline that should use them (order matters). Example service pipelines:

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
      processors: [attributes/add_env, batch]
    metrics:
      receivers: [prometheus, otlp]
      exporters: [debug]
      processors: [filter, batch]
    logs:
      receivers: [otlp]
      exporters: [debug]
      processors: [filter, batch]
```

Best practices

* Place the filter processor early in pipelines to minimize downstream processing on unwanted telemetry.
* Prefer `match_type: regexp` for flexible pattern-based rules.
* Use include-only when you require strict control over which metrics are collected.
* Double-check configuration key names to avoid parse errors (e.g., `metric_names`).

Links and references

* OpenTelemetry Collector filter processor docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OpenTelemetry Collector contrib repo: [https://github.com/open-telemetry/opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib)

Summary

* The filter processor provides powerful include/exclude rules for metrics and logs.
* Use regex patterns for flexible matching and include-only for tight control.
* Verify processor ordering and configuration keys to avoid startup issues.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/0c79aa6d-2956-47c5-8820-8f5f0b2e9a86)
