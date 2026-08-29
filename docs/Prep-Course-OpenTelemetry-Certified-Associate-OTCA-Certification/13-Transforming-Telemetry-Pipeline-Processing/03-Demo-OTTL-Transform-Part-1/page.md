# Demo OTTL Transform Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Demo-OTTL-Transform-Part-1/page

Demonstrates using the OpenTelemetry Transformation Language transform processor to modify trace resource attributes, spans, and span events with conditional rules and examples

In this lesson we continue the OpenTelemetry Transformation Language (OTTL) demo by focusing on the `transform` processor. Instead of filtering, we'll apply transformations to telemetry signals — primarily traces — to set or modify attributes on resources, spans, and span events.

Start by replacing or commenting out any previous `filter` processor configuration and enable the `transform` processor in your Collector configuration. A minimal OpenTelemetry Collector snippet to enable the processor looks like this:

```yaml theme={null}
grpc:
  endpoint: 0.0.0.0:4317
http:
  endpoint: 0.0.0.0:4318

processors:
  transform: {}

exporters:
  prometheusremotewrite: {}
```

Example debug output from the agent (trimmed for clarity):

```plaintext theme={null}
otel-collector    ID            : fa24a2af8f8be8ef0
otel-collector    Name          : authenticate user
otel-collector    Kind          : Internal
otel-collector    Start time    : 2025-10-04 22:38:53.216794 +0000 UTC
otel-collector    End time      : 2025-10-04 22:38:53.216797 +0000 UTC
otel-collector    Status code   : Unset
Attributes:
  -> user_id: Str(jal2334j3kflsd83)
  -> email: Str(john@gmail.com)
  -> username: Str(john)

Span #1
otel-collector    Trace ID     : 9e35c26e825b581c16dfc59abda2d80e
otel-collector    Parent ID    : c41919f58383e461
otel-collector    ID           : 41
otel-collector    Kind         : Internal
```

Local test runs (example; reduced duplicates):

```bash theme={null}
$ python auth2.py
processing payment
processing payment
processing payment
```

***

## Transform processor basics

The `transform` processor executes OTTL statements to modify signals. It supports an `error_mode` option that controls behavior when a statement errors.

```yaml theme={null}
grpc:
  endpoint: 0.0.0.0:4317
http:
  endpoint: 0.0.0.0:4318

processors:
  transform:
    error_mode: ignore
```

<Callout icon="lightbulb">
  Setting `error_mode: ignore` prevents a single statement failure from stopping processing of the signal. This is useful for experimentation or when applying many optional transformations.
</Callout>

Transform rules are scoped by signal type. Use the appropriate statements block per signal:

* Traces: `trace_statements`
* Metrics: `metric_statements`
* Logs: `log_statements`

This guide focuses on traces. A minimal traces configuration:

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      # trace-level rules go here
```

A typical service pipeline wiring the `transform` processor looks like this:

```yaml theme={null}
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [transform]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

***

## Contexts available in OTTL

OTTL exposes contexts that map to parts of a telemetry signal. Use the appropriate context for what you want to modify.

| Context     | Targets                                                       | Typical use                                              |
| ----------- | ------------------------------------------------------------- | -------------------------------------------------------- |
| `resource`  | Resource attributes                                           | Add service-level metadata (e.g., environment, platform) |
| `span`      | Span attributes and core span properties (name, kind, status) | Modify span-level metadata                               |
| `spanevent` | Span events                                                   | Add or modify attributes on span events                  |
| `metric`    | Metric resource-level metric fields                           | Transform metric metadata                                |
| `datapoint` | Individual metric datapoints                                  | Modify values or labels                                  |
| `log`       | Log records                                                   | Enrich or alter log attributes                           |

Each context has different available fields you can read and modify. For traces, choose `resource`, `span`, or `spanevent` as needed.

***

## Example: Set a resource attribute

Add a `platform` resource attribute to all traces using the `resource` context.

```yaml theme={null}
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["platform"], "kubernetes")
```

With the Collector wired to the `debug` exporter, you should see `platform: Str(kubernetes)` in resource attributes for incoming traces (trimmed):

```plaintext theme={null}
Resource attributes:
  -> telemetry.sdk.language: Str(python)
  -> telemetry.sdk.name: Str(opentelemetry)
  -> telemetry.sdk.version: Str(1.37.0)
  -> service.name: Str(flight-service)
  -> service.version: Str(0.2.0)
  -> service.region: Str(us-east-1)
  -> service.env: Str(development)
  -> platform: Str(kubernetes)
```

<Callout icon="warning">
  In production, avoid applying broad resource or span changes to all signals. Scope transformations to only the resources or spans that need modification to reduce risk of unintended side effects.
</Callout>

***

## Example: Add an attribute to a span

To set an attribute on spans, use the `span` context:

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
```

Debug output showing the new span attribute:

```plaintext theme={null}
Span #0
  Trace ID : 10f6c947a0d5e7c164a9f7414ba929
  ID       : 97249f6133b402e
  Kind     : Internal
  Attributes:
    -> source: Str(jfk)
    -> dest: Str(lax)
    -> flight_number: Str(4427)
    -> airline: Str(delta)
    -> some-key: Str(some-value)
```

***

## Span events: add attributes to events

Ensure your instrumentation emits span events. Example Python snippet that sets span attributes and adds an event:

```python theme={null}
