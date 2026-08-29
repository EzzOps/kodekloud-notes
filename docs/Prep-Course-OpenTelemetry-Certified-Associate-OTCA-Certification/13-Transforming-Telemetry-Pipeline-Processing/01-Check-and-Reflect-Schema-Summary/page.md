# Check and Reflect Schema Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Transforming-Telemetry-Pipeline-Processing/Check-and-Reflect-Schema-Summary/page

Summary of OpenTelemetry schema transform rules and best practices for collector schema files, covering rename-focused transforms, ordering, versioning, and scoping for metrics, spans, events, and resources.

This page summarizes the essential rules and best practices for OpenTelemetry schema transforms. Use it as a quick reference when authoring schema files for the collector's schema processor.

Key takeaways:

* Patch increments imply no behavioral changes for consumers.
* Minor increments add optional, backward-compatible items.
* The `all` section may only contain `rename_attributes` and runs before signal-specific rules.
* Transform order matters: apply global (`all`) rules before signal-specific transforms.
* When migrating between schema versions, step through intermediate versions sequentially (X → X+1 → ... → Y).
* Use `rename_metrics` to change a metric's name and `rename_attributes` to change labels/attributes.
* Resource-level renames use `rename_attributes`.
* Always set `schema_url` to the highest schema version declared; it travels with telemetry.
* In `metrics.rename_attributes`, omitting `apply_to_metrics` makes the renaming apply to all metrics.
* Span selectors and event selectors can scope renames to specific spans or span events.
* The collector’s schema processor upgrades/downgrades telemetry by applying rename-based transforms in version order.
* Keep transforms minimal and rename-focused to limit complexity and reduce the chance of unintended semantic changes.

<Frame>
  <img alt="The image is a slide titled &#x22;Knowledge Check #1 – File Format and Order,&#x22; showing five concepts related to software versioning processes, including patch increment, minor increment, all section, transform orders, and version stepping." />
</Frame>

Practical notes and rules of thumb

* Always put `all` (global) `rename_attributes` rules first so broad attribute renames are applied before signal-specific renames.
* Use `rename_metrics` for the metric name itself and `rename_attributes` for metric labels.
* Use `apply_to_metrics` (when available) to scope an attribute rename to selected metric names; if omitted, the rename applies to all metrics.
* For spans and span events, use selectors such as `apply_to_spans` or `apply_to_events` to limit renames to specific names or patterns.

<Frame>
  <img alt="The image outlines four steps about URLs and schema evolution, focusing on schema URLs, processors, versioning, and transformation types, using icons and colored backgrounds to distinguish each step." />
</Frame>

Quick reference table — transform types and example usage

| Transform type                  | Purpose                                                     | Example                                                                                                                                                                              |
| ------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rename_metrics`                | Change the metric's canonical name                          | `yaml<br> - rename_metrics:<br>     old.metric.name: new.metric.name<br>`                                                                                                            |
| `rename_attributes` (metrics)   | Rename metric labels; can be scoped with `apply_to_metrics` | `yaml<br> - rename_attributes:<br>     attribute_map:<br>       old_label: new_label<br>     apply_to_metrics: ["new.metric.name"]<br>`                                              |
| `rename_attributes` (resources) | Rename resource attributes                                  | `yaml<br> - rename_attributes:<br>     attribute_map:<br>       old_resource_attr: new_resource_attr<br>`                                                                            |
| Conditional selectors           | Scope renames to spans or events                            | `yaml<br> - rename_attributes:<br>     attribute_map:<br>       old_label: new_label<br>     apply_to_spans: ["service.span.name"]<br>     apply_to_events: ["span.event.name"]<br>` |

Example schema snippet (concise)

```yaml theme={null}
schema_url: https://opentelemetry.io/schemas/1.26.0

metrics:
  changes:
    - rename_metrics:
        old.metric.name: new.metric.name
    - rename_attributes:
        attribute_map:
          old_label: new_label
        # Optional scoping (commented examples):
        # apply_to_metrics: ["new.metric.name"]

resources:
  changes:
    - rename_attributes:
        attribute_map:
          old_resource_attr: new_resource_attr
