# python
span.set_attributes(
    {
        "user_id": "jal23343j3kflsd83",
        "email": "john@gmail.com",
        "username": "john"
    }
)
span.add_event("something is happening!!!")
print("processing payment")
```

OTTL rule to set an attribute on all span events:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
      - context: span
        statements:
          - set(attributes["some-key"], "some-value")
      - context: spanevent
        statements:
          - set(attributes["some-event-key"], "some-event-value")
```

Debug output showing an event with the new event attribute:

```plaintext theme={null}
Events:
  SpanEvent #0
    Name: something is happening!!!
    Timestamp: 2025-10-04 22:52:53.663619 +0000 UTC
    Attributes:
      -> some-event-key: Str(some-event-value)
```

***

## Conditional statements: restrict statements to specific spans

Avoid modifying every span by using `where` clauses to apply statements conditionally.

Example: add an attribute only to spans with `name == "process payment"`.

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
      - context: span
        statements:
          - set(attributes["some-key"], "some-value") where name == "process payment"
      - context: spanevent
        statements:
          - set(attributes["some-event-key"], "some-event-value")
```

You can also check attribute existence before applying a change (useful for optional attributes):

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - set(attributes["some-key"], "some-value") where attributes["bank"] != nil
```

Match on a specific attribute value:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - set(attributes["some-key"], "some-value") where attributes["bank"] == "BankOfAmerica"
```

***

## Use the `conditions` block to avoid repeating `where`

When multiple statements share the same condition, group them under `conditions` for readability and maintainability.

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")

      - context: span
        conditions:
          - attributes["bank"] != nil
        statements:
          - set(attributes["some-key"], "some-value")
          - set(attributes["where"], true)

      - context: spanevent
        statements:
          - set(attributes["some-event-key"], "some-event-value")
```

All `statements` under a context with `conditions` are executed only when the condition(s) evaluate to true.

***

## Best practices and summary

* Use the `transform` processor to modify resource, span, and span event data where necessary.
* Choose the appropriate context (`resource`, `span`, `spanevent`) for targeted changes.
* Prefer scoped transformations using `where` or `conditions` rather than global modifications.
* Use `error_mode` to control how statement errors are handled while testing or in production.
* Test with a `debug` exporter to verify expected output before deploying changes.

This lesson covered basic `set` operations and scoping with contexts and conditions. OTTL supports more advanced expressions and transformations for complex use cases.

## Links and references

* [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
* [OTTL specification and examples](https://github.com/open-telemetry/opentelemetry-collector-[SECRET_REDACTED])
* [OpenTelemetry Python instrumentation](https://opentelemetry-python.readthedocs.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/3b7cc72b-5faa-439d-8c69-13bff1cbe2ba" />
</CardGroup>


# Demo OTTL Transform Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Demo-OTTL-Transform-Part-2/page

Explains using the OpenTelemetry transform processor to modify traces logs and metrics with OTTL examples and best practices

In this lesson we apply the transform processor to logs and metrics. The core ideas are the same as for traces: use the `transform` processor with signal-specific `*_statements` and, when needed, `conditions` to selectively modify telemetry.

Key takeaway: the transform processor only affects telemetry for the pipeline it is attached to (traces, metrics, or logs). Make sure you wire it into the correct pipeline.

<Callout icon="lightbulb">
  When you change the transform configuration, restart the collector and the apps sending telemetry so you can observe the effects.
</Callout>

***

## Quick recap: trace transformations

A typical transform configuration that updates resource attributes, spans, and span events looks like this:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
      - context: span
        conditions:
          - attributes["bank"] != nil
        statements:
          - set(attributes["some-key"], "some-value")
      - context: spanevent
        statements:
          - set(attributes["some-other-key"], "some-other-value")
```

Collector debug output for a span will show the modified resource and span attributes, for example:

```plaintext theme={null}
otel-collector -> platform: Str(kubernetes)
otel-collector | ScopeSpans #0
otel-collector | Span #0
otel-collector |   Name: process flight
otel-collector |   Kind: Internal
otel-collector |   Start time: 2025-10-04 23:01:09.565017 +0000 UTC
```

***

## Logs

We'll generate logs using a small `log.py` script that prints logs at different severities. Before you add transforms, inspect the raw records using the collector's debug exporter.

Example transform configuration that updates log attributes, severity, and body:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    log_statements:
      - context: log
        statements:
          - set(attributes["log_key"], "value")
          - set(severity_text, "INFO")
          - set(body, "new body")
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
      - context: span
        conditions:
          - attributes["bank"] != nil
        statements:
          - set(attributes["some-key"], "some-value")
```

What to remember:

* `context: log` operates on the LogRecord.
* Use `attributes[...]` to add/modify log attributes.
* Overwrite `severity_text` to change severity label (e.g., `INFO`, `ERROR`).
* Overwrite `body` to replace the log message.
* Without `conditions`, statements apply to every log record.

Example collector debug output (before transform):

```plaintext theme={null}
otel-collector LogRecord #0
ObservedTimestamp: 2025-10-04 23:03:32.563379 +0000 UTC
Timestamp: 2025-10-04 23:03:32.563460496 +0000 UTC
SeverityText: INFO
Body: Str(INFO:root:User sent request)
Attributes:
  -> code.file.path: Str(/Users/sanjeev/Documents/courses/ottl-demo/scripts/log.py)
  -> code.function.name: Str(<module>)
  -> code.line.number: Int(30)
```

After applying the transform above, you will see the updated body, severity, and added attribute:

```plaintext theme={null}
otel-collector | LogRecord #4
ObservedTimestamp: 2025-10-04 23:06:31.159749 +0000 UTC
Timestamp: 2025-10-04 23:06:31.159740 +0000 UTC
SeverityText: INFO
SeverityNumber: Info(9)
Body: Str(new body)
Attributes:
  -> code.file.path: Str(/Users/sanjeev/Documents/courses/ottl-demo/scripts/log.py)
  -> code.function.name: Str(<module>)
  -> code.line.number: Int(34)
  -> log_key: Str(value)
```

Make sure the transform processor is included in the logs pipeline:

```yaml theme={null}
logs:
  receivers: [otlp]
  processors: [transform]
  exporters: [debug]
```

***

## Additional log contexts

The transform processor supports other contexts for logs besides `log`, such as `resource` and `scope`. These allow you to modify resource-level attributes and instrumentation scope metadata.

Example:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    log_statements:
      - context: log
        statements:
          - set(attributes["log_key"], "value")
          - set(severity_text, "INFO")
          - set(body, "new body")
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
      - context: scope
        statements:
          - set(attributes["scope_key"], "value")
          - set(name, "my.scope.name")
```

Resulting debug output shows updated resource attributes and instrumentation scope:

```plaintext theme={null}
otel-collector | Resource attributes:
  -> telemetry.sdk.language: Str(python)
  -> telemetry.sdk.version: Str(1.37.0)
  -> service.name: Str(unknown_service)
  -> platform: Str(kubernetes)

InstrumentationScope my.scope.name:
InstrumentationScope attributes:
  -> scope_key: Str(value)

LogRecord #0
ObservedTimestamp: 2025-10-04 23:07:47.626684 +0000 UTC
Timestamp: 2025-10-04 23:07:47.626674 +0000 UTC
SeverityNumber: Info(9)
Body: Str(new body)
Attributes:
  -> code.file.path: Str(/Users/sanjeev/Documents/courses/ottl-demo/scripts/log.py)
  -> code.function.name: Str(<module>)
  -> code.line.number: Int(33)
  -> log_key: Str(value)
```

***

## Metrics

Metrics use `metric_statements` and support contexts like `metric`, `datapoint`, and `resource`. You can modify metric descriptors (name, description, unit), and operate on individual datapoints.

Example: change a metric descriptor only when the metric name matches `current_temperature_fahrenheit`:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    metric_statements:
      - context: metric
        conditions:
          - name == "current_temperature_fahrenheit"
        statements:
          - set(description, "new description")
          - set(name, "new.metric.name")
          - set(unit, "ms")

    log_statements:
      - context: log
        statements:
          - set(attributes["log_key"], "value")
          - set(severity_text, "INFO")
          - set(body, "new body")
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
```

Attach the transform processor to the metrics pipeline:

```yaml theme={null}
metrics:
  receivers: [otlp]
  processors: [transform]
  exporters: [debug]
```

After wiring, `current_temperature_fahrenheit` will be transformed and appear as `new.metric.name` with updated descriptor fields:

```plaintext theme={null}
otel-collector | Metric #0
otel-collector | Descriptor:
otel-collector |   -> Name: new.metric.name
otel-collector |   -> Description: new description
otel-collector |   -> Unit: ms
otel-collector |   -> DataType: Gauge
otel-collector | NumberDataPoints #0
otel-collector | Value: 81.788748
```

***

## Data point context

Use `context: datapoint` to modify individual datapoints — add datapoint attributes, override timestamps, or change values.

Example:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    metric_statements:
      - context: metric
        conditions:
          - name == "current_temperature_fahrenheit"
        statements:
          - set(description, "new description")
          - set(name, "new.metric.name")
          - set(unit, "ms")
      - context: datapoint
        statements:
          - set(attributes["datapoint_key"], "value")
          - set(start_time_unix_nano, 1000000)
          - set(time_unix_nano, 2000000000)
          - set(value_int, 100)
      - context: resource
        statements:
          - set(attributes["service.name"], "my-service")
```

Collector debug will show modified datapoint timestamps, values, and datapoint-level attributes:

```plaintext theme={null}
otel-collector | StartTimestamp: 1970-01-01 00:00:00.001 +0000 UTC
otel-collector | Timestamp: 1970-01-01 00:00:02.000 +0000 UTC
otel-collector | Value: 100
otel-collector | Data point attributes:
otel-collector |   -> datapoint_key: Str(value)
```

Use datapoint transformations for unit conversions, value overrides, or adding metadata to datapoints.

***

## Deleting or keeping keys (attribute filtering)

You can delete specific attribute keys or keep only a whitelist. The same APIs exist for traces, logs, and metrics — below examples use trace/span context.

Delete a key:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - delete_key(attributes, "bank")
```

This removes the `bank` attribute from spans where the statement executes. To run only when that key exists, add a condition such as `attributes["bank"] != nil`.

Keep only a whitelist of keys:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - keep_keys(attributes, ["username", "account_number"])
```

`keep_keys(attributes, [...])` removes all other keys from the attributes map except those specified.

Example debug output after keeping only `username` and `account_number`:

```plaintext theme={null}
Attributes:
  -> username: Str(john)
  -> account_number: Str(7333928)
```

If you applied `keep_keys(attributes, ["username", "account_number"])`, other keys such as `some-key` would be removed.

***

## Transform contexts quick reference

| Context type         | Signals supported     | What you can modify                           | Example statement                           |
| -------------------- | --------------------- | --------------------------------------------- | ------------------------------------------- |
| `resource`           | traces, logs, metrics | Resource attributes                           | `set(attributes["platform"], "kubernetes")` |
| `span` / `spanevent` | traces                | Span attributes, events                       | `set(attributes["some-key"], "some-value")` |
| `log`                | logs                  | LogRecord attributes, `body`, `severity_text` | `set(body, "new body")`                     |
| `scope`              | logs, traces          | Instrumentation scope name/attributes         | `set(name, "my.scope.name")`                |
| `metric`             | metrics               | Metric descriptor (name, description, unit)   | `set(name, "new.metric.name")`              |
| `datapoint`          | metrics               | Datapoint attributes, timestamps, values      | `set(value_int, 100)`                       |

***

## Final checklist and best practices

* Add the transform processor to the correct pipeline(s): traces, metrics, and/or logs.
* Confirm your YAML structure: each `context` block must include `statements:` and, optionally, `conditions:` (as a list).
* Use valid OTTL expressions inside `conditions:`, for example:
  * `attributes["bank"] != nil`
  * `name == "current_temperature_fahrenheit"`
* When iterating on rules, use the collector debug exporter and restart both the collector and telemetry-generating processes so changes take effect.
* Test incrementally: apply simple transformations first (e.g., set a single attribute), verify output, then expand to more complex rules.

<Callout icon="lightbulb">
  Use the debug exporter in the collector to inspect the transformed telemetry while you iterate on OTTL rules.
</Callout>

***

## Links and references

* [OpenTelemetry Collector Transform Processor](https://opentelemetry.io[AWS_SECRET_ACCESS_KEY]/transformprocessor/)
* [OTTL (OpenTelemetry Transformation Language) Reference](https://opentelemetry.io/docs/reference/specification/otel-otl/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/4dcf8d5a-bee7-4c5a-999a-b6d6a1bbfdc9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/06dc04f4-69ee-4fa3-9970-5d371786e296" />
</CardGroup>
