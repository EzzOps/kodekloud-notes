# Span or span-events scoping can also be expressed with conditional selectors:
# - rename_attributes:
#     attribute_map:
#       old_label: new_label
#     # apply_to_spans: ["service.span.name"]
#     # apply_to_events: ["span.event.name"]
```

<Callout icon="lightbulb">
  Best practice: Always set `schema_url` to the highest schema version you list in the configuration. The schema URL travels with telemetry and the collector uses it to decide which transforms to apply when upgrading or downgrading. For further details, see the OpenTelemetry schema docs: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/).
</Callout>

Final recap — rules to remember

* Schema versioning follows semantic versioning: patch = no change, minor = backward-compatible additions, major = breaking changes.
* Schema files have organized sections: `all`, `resources`, `spans`, `span_events`, `metrics`, and `logs`. Use each section for focused transforms.
* The collector’s schema processor applies transforms sequentially, version-by-version (X → X+1 → ... → target).
* Favor rename-only transforms and minimal change sets to avoid accidental semantic shifts.

<Callout icon="warning">
  Validate your YAML and ensure keys and `schema_url` values are spelled correctly (for example, `opentelemetry.io`). YAML syntax errors or incorrect keys can prevent the collector from loading schema transforms.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/aec14517-49d2-4509-bc8c-2f1f8c0ffdbc" />
</CardGroup>


# Demo OTTL Filter

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Demo-OTTL-Filter/page

Shows using OTTL with the OpenTelemetry Collector to filter and drop spans by service, span name, attributes, regex and error_mode configuration

In this lesson we'll demonstrate using the OpenTelemetry Transformation Language (OTTL) with the OpenTelemetry Collector to filter and transform telemetry before exporting it. Examples focus on traces for clarity, but the same OTTL concepts apply to metrics and logs by targeting the appropriate context in the processor configuration.

## What you'll need

* An OpenTelemetry Collector instance.
* One or more instrumented services that send OTLP (gRPC or HTTP) to the collector.
* The demo services in this article (auth, flight, payment) or any services that produce spans to validate filter behavior.

## Starting Collector configuration

Below is a minimal collector configuration used for this demo. It receives OTLP on the standard ports and prints telemetry to the `debug` exporter so you can easily validate filtering behavior.

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  prometheusremotewrite:
    endpoint: "http://prometheus:9090/api/v1/write"
  debug:
    verbosity: detailed

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
```

Run your sample apps (for example `./app.sh`) to generate spans from each service. The collector debug exporter prints spans to the console and is useful for verifying whether OTTL rules are including or dropping spans as expected.

## Adding the OTTL filter processor

To filter spans with OTTL, add the `filter/ottl` processor and configure rules under the `traces` context. The processor has an `error_mode` setting that determines how OTTL evaluation errors are handled:

<Callout icon="lightbulb">
  Three `error_mode` options:

  * `ignore`: Log errors and continue evaluating other rules (no telemetry dropped due to OTTL evaluation errors).
  * `silent`: Do not log errors and continue evaluating other rules.
  * `propagate`: Stop processing and drop the telemetry when an OTTL error occurs.
</Callout>

Example of wiring the processor into a traces pipeline:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [filter/ottl]
      exporters: [debug]
```

Key point: under the processor, the `traces` section lists rule categories (e.g., `span`) and each rule is an OTTL expression. If an expression evaluates to true for a span, that span will be dropped by the filter processor.

## Filter by resource attribute (service name)

Drop spans originating from a specific service by matching the `resource.attributes["service.name"]` resource attribute:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'resource.attributes["service.name"] == "flight-service"'
```

Drop multiple services by adding multiple rules:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'resource.attributes["service.name"] == "flight-service"'
        - 'resource.attributes["service.name"] == "payment-service"'
```

Keep only one service (drop all others) by inverting the comparison:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'resource.attributes["service.name"] != "flight-service"'
```

## Filter by span name

Match spans by their name. When writing YAML, wrap the OTTL expression in single quotes and use double quotes inside as needed:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'name == "validate card"'
```

This will drop any span named `validate card` across all services.

## Filter by span attributes

OTTL can read span attributes for flexible filtering. Examples:

Match a single attribute value:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'attributes["username"] == "john"'
```

Combine conditions using logical operators:

* OR example (drop spans for username `john` or `mary`):

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'attributes["username"] == "john" or attributes["username"] == "mary"'
```

* AND example (both conditions must match to drop the span):

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'attributes["username"] == "john" and attributes["email"] == "john@gmail.com"'
```

## Regular expression matching with IsMatch

Use `IsMatch` to evaluate regex patterns. For example, to drop spans where the username is exactly `john` or `mary`:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'IsMatch(attributes["username"], "^(john|mary)$")'
```

This is case-sensitive by default. Adjust the regex for case-insensitive matching (e.g., use `(?i)`).

## Negation (not)

Invert conditions using `not`. If the inner expression contains logical operators, wrap it in parentheses:

```yaml theme={null}
processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'not (attributes["username"] == "john" and attributes["email"] == "john@gmail.com")'
```

The above will drop any span that does *not* match both username `john` and email `john@gmail.com`.

## Quick reference: common OTTL span filters

| Goal                                           | OTTL expression (YAML string)                                            |              |
| ---------------------------------------------- | ------------------------------------------------------------------------ | ------------ |
| Drop spans from `flight-service`               | `'resource.attributes["service.name"] == "flight-service"'`              |              |
| Drop spans named `validate card`               | `'name == "validate card"'`                                              |              |
| Drop spans with username `john` or `mary` (OR) | `'attributes["username"] == "john" or attributes["username"] == "mary"'` |              |
| Drop spans matching regex on username          | \`'IsMatch(attributes\["username"], "^(john                              | mary)\$")'\` |
| Keep only `flight-service` (drop others)       | `'resource.attributes["service.name"] != "flight-service"'`              |              |

Note: In YAML, put each OTTL expression as a quoted string (single quotes recommended) to avoid parsing issues.

<Callout icon="warning">
  Be careful with `error_mode: propagate`. If an OTTL rule errors under `propagate`, telemetry may be dropped. Use `ignore` during testing to avoid inadvertently losing data.
</Callout>

## Putting it into the Collector pipeline (complete example)

A typical configuration that applies a simple username regex-based drop looks like this:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  filter/ottl:
    error_mode: ignore
    traces:
      span:
        - 'IsMatch(attributes["username"], "^(john|mary)$")'

exporters:
  prometheusremotewrite:
    endpoint: "http://prometheus:9090/api/v1/write"
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [filter/ottl]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

After updating the config, restart the collector and re-run your sample apps (e.g., `./app.sh`) to validate that matching spans are filtered. Inspect the collector logs and the `debug` exporter output to confirm behavior.

## Summary

* OTTL lets you write expressive, targeted rules to drop spans based on span properties (name, trace ID, span ID), resource attributes (for example `service.name`), and span attributes.
* Use logical operators (`and`, `or`, `not`) and regex via `IsMatch` for flexible matching.
* `error_mode` determines collector behavior on OTTL evaluation errors: `ignore`, `silent`, or `propagate`.
* The same OTTL concepts apply to metrics and logs; use the appropriate context (`metrics`, `logs`) within the processor configuration.

Transforming telemetry (e.g., setting/removing attributes or renaming metrics) is a separate use of OTTL and is outside the scope of this article.

## Links and References

* [OpenTelemetry Collector – Processors](https://opentelemetry.io/docs/collector/)
* [OTTL (OpenTelemetry Transformation Language) reference](https://opentelemetry.io/docs/reference/specification/otel-collector/processor/filter-ottl/)
* [OpenTelemetry Python - OTLP exporter](https://opentelemetry-python.readthedocs.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/b94924e7-ed0b-4378-9f33-a2a27ca2c463" />
</CardGroup>
