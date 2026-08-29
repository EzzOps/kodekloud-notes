# Schema Translation Rules by Signal Type

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Schema-Translation-Rules-by-Signal-Type/page

Guide to writing YAML schema translation rules to evolve and transform telemetry by signal type, controlling renames, additions, removals, splits, and execution order across schema versions.

This guide explains how to author and apply schema translation rules (YAML) to evolve telemetry across schema versions. Rules are organized by telemetry signal type to give you precise control over renames, additions, removals, splits, and filters. Use the examples below as templates for common transformations.

Key sections (signal-focused):

* all — global rules applied to every signal type
* resources — resource-level attributes shared across signals
* spans — span-level attributes (with optional span-name filters)
* span\_events — events that occur within spans (exceptions, logs)
* metrics — metric names, metric attributes, and splitting metrics by attribute values
* logs — log record attributes

<Frame>
  <img alt="The image outlines &#x22;Schema Translation Rules&#x22; with six signal sections: All, Resources, Spans, Span Events, Metrics, and Logs, each with a brief description." />
</Frame>

<Callout icon="lightbulb">
  Schema translation rules live under version blocks. Each version contains signal-specific sections. Start with `all` for global normalizations, then add targeted rules per signal. Test changes in staging since transforms are applied in a fixed order and are often non-commutative.
</Callout>

## Quick reference table

|      Section | Purpose                                                           | Common operations                                          |
| -----------: | ----------------------------------------------------------------- | ---------------------------------------------------------- |
|          all | Global normalizations applied to every signal                     | `rename_attributes`, `add_attributes`, `remove_attributes` |
|    resources | Resource attributes (service, host, cloud)                        | `rename_attributes`, `add_attributes`                      |
|        spans | Span attributes and optional filtering by span name               | `rename_attributes`, `remove_attributes`, `add_attributes` |
| span\_events | Events within spans (exceptions, logs)                            | `rename_events`, `rename_attributes`, `remove_attributes`  |
|      metrics | Metric names/attributes and splitting metrics by attribute values | `rename_metrics`, `rename_attributes`, `split`             |
|         logs | Log record attributes                                             | `rename_attributes`, `remove_attributes`, `add_attributes` |

## Execution order (important)

Transforms execute in this fixed sequence:

1. `all` (applies to every signal type)
2. Signal-specific sections:
   * `spans` runs before `span_events`
   * `resources`, `metrics`, and `logs` run after `all` and effectively in parallel relative to each other

Because `all` runs first, any subsequent transformations must reference attribute names as transformed by `all`.

***

## all — Global transformations

Run once per version as a first pass for broad renames or normalizations that should apply to every signal (resources, spans, metrics, logs). Useful for standardizing vendor or SDK attribute names.

Example: Global attribute renames

```yaml theme={null}
versions:
  1.1.0:
    all:
      changes:
        - rename_attributes:
            attribute_map:
              # Map old names to new names
              # Applies to ALL signal types
              k8s.cluster.name: kubernetes.cluster.name
              k8s.pod.name: kubernetes.pod.name
              k8s.container.name: kubernetes.container.name
              k8s.namespace.name: kubernetes.namespace.name
```

## resources — Resource attribute rules

Use this section for attributes attached to resources (shared metadata across multiple signals). Typical uses include standardizing cloud or SDK-provided resource keys.

Example: Resource attribute renames

```yaml theme={null}
versions:
  1.1.0:
    resources:
      changes:
        - rename_attributes:
            attribute_map:
              # Old name -> New name (only Resource attributes)
              telemetry.auto.version: telemetry.auto_instr.version
              telemetry.sdk.language: telemetry.sdk.name
```

## spans — Span-level transformations

Span rules apply to attributes recorded on spans. You can scope operations to specific span names using `apply_to_spans`. If `apply_to_spans` is omitted, the change applies to all spans.

Example: Rename span attributes (with optional span-name filter)

```yaml theme={null}
versions:
  1.1.0:
    spans:
      changes:
        - rename_attributes:
            attribute_map:
              peer.service: peer.service.name
            apply_to_spans:
              # Optional: Only apply to these spans (if omitted => all spans)
              - HTTP GET
              - HTTP POST

        - rename_attributes:
            attribute_map:
              http.status_code: http.response.status_code
            # No apply_to_spans => applies to all spans
```

## span\_events — Events inside spans

Span events are timestamped records inside spans (exceptions, logs, custom events). Supported operations include renaming event names and renaming event attributes. Both `apply_to_spans` and `apply_to_events` can be used to scope a change; if omitted, changes apply broadly.

Example span event JSON (a span with an exception event)

```json theme={null}
{
  "events": [
    {
      "name": "exception",
      "timestamp": "2025-05-01T12:58:08.969805Z",
      "attributes": {
        "exception.type": "HTTPErrors",
        "exception.message": "404 Not Found",
        "exception.stacktrace": "raise_for_status() -> HTTPErrors",
        "exception.escaped": "False"
      }
    }
  ]
}
```

Example: Rename events and event attributes

```yaml theme={null}
versions:
  1.1.0:
    span_events:
      changes:
        - rename_events:
            name_map:
              stacktrace: stack_trace
              log: log_record

        - rename_attributes:
            attribute_map:
              peer.service: peer.service.name
            apply_to_spans:
              - HTTP GET
            apply_to_events:
              - exception
```

## metrics — Metric transformations and splitting

Metrics support renaming metric identifiers (`rename_metrics`), renaming metric attributes (`rename_attributes` with `apply_to_metrics` filter), and splitting a metric into multiple metrics based on an attribute (`split`).

Example: Rename metric names and metric attributes

```yaml theme={null}
versions:
  1.1.0:
    metrics:
      changes:
        - rename_metrics:
            container.cpu.usage.total: cpu.usage.total
            container.memory.usage.max: memory.usage.max

        - rename_attributes:
            attribute_map:
              status: state
            apply_to_metrics:
              - system.cpu.utilization
              - system.memory.usage
              - system.paging.usage
```

Example: Split a metric by an attribute value

```yaml theme={null}
versions:
  1.1.0:
    metrics:
      changes:
        - split:
            # Metric to split
            apply_to_metric: system.paging.operations
            # Attribute to split by (this attribute will be removed)
            by_attribute: direction
            # New metric names mapped to attribute values
            metrics_from_attributes:
              system.paging.operations.in: in
              system.paging.operations.out: out

        - split:
            apply_to_metric: http.requests
            by_attribute: method
            metrics_from_attributes:
              http.requests.get: GET
              http.requests.post: POST
```

Using `split` transforms a metric with an attribute (e.g., `direction=in`) into separate metrics (e.g., `system.paging.operations.in`), simplifying queries and aggregation.

## logs — Log record attribute rules

Target log record attributes only. Common uses: standardizing executable names, severity fields, and message/body fields.

Example: Rename log attributes

```yaml theme={null}
versions:
  1.1.0:
    logs:
      changes:
        - rename_attributes:
            attribute_map:
              # Old attribute -> New attribute (only Log Record attributes)
              process.executable_name: process.executable.name
              severity: severity_text
              message: body
```

## Ordering pitfalls and best practices

Transforms are not generally commutative. Renaming or removing an attribute that a later transform depends on (for example, a `split` by that attribute) will break the later transform. Always reason about dependencies and ordering when composing changes.

<Callout icon="warning">
  Order matters: if you rename or remove an attribute that a later transform depends on (for example `split`), the later transform will fail because the attribute is missing. Apply `split` (or other operations that depend on original attributes) before renames that remove or change those attributes.
</Callout>

Problem example (incorrect order — `direction` renamed before `split`)

```yaml theme={null}
versions:
  1.1.0:
    all:
      changes:
        - rename_attributes:
            attribute_map:
              direction: dir
              # Renaming "direction" → "dir" will make later split fail

    metrics:
      changes:
        - split:
            apply_to_metric: system.paging.operations
            by_attribute: direction   # <-- missing because it was renamed above
            metrics_from_attributes:
              system.paging.operations.in: in
              system.paging.operations.out: out
```

Correct approach: perform `split` (or other dependent transforms) while the original attribute exists, then rename or remove attributes afterwards.

## Upgrading schema versions

* Apply schema upgrades sequentially (for example: 1.0 → 1.1 → 1.2). Do not skip intermediate versions.
* Many transforms depend on prior state; apply each version's rules in order to guarantee reproducibility.
* When refactoring a large set of attributes, consider a multi-step upgrade plan:
  1. Add new attributes or split metrics without removing originals.
  2. Migrate consumers (dashboards, alerts) to new names.
  3. Remove old attributes in a subsequent version.

## Summary / Checklist

* Use `all` for global, first-pass normalizations.
* Use signal-specific sections to refine or add targeted transformations.
* Scope changes with `apply_to_spans`, `apply_to_metrics`, and `apply_to_events`.
* Remember fixed execution order: `all` → signal sections (spans before span\_events).
* Apply schema upgrades sequentially and test each version in staging.

Further reading:

* [OpenTelemetry Specification](https://opentelemetry.io/docs/)
* Refer to your vendor/collector docs for implementation details and supported operations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/85787c66-c021-47d9-bd3d-db54bc002465/lesson/b06b0465-70d8-416d-a32f-4256a671894d" />
</CardGroup>
