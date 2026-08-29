# python
# Inside a span context
with tracer.start_as_current_span("process_order") as span:
    # Set order attributes using actual variables
    span.set_attribute("order_id", order_id)              # e.g., 12345
    span.set_attribute("payment_method", payment_method)  # e.g., "Credit Card"
    span.set_attribute("inventory_status", inventory_status)  # e.g., "In Stock"
    
    # Continue with your business logic
    process_order_logic()
```

Use the span object's `set_attribute` method (dot notation) to attach keys and values. Keys are strings and values must conform to supported types (see rules below). Add important attributes as early as possible so they are available for SDK-level sampling decisions.

<Frame>
  <img alt="The image illustrates the use of span attributes in e-commerce for tracing order life cycles, filtering orders by payment method, and debugging inventory fulfillment issues. The information is presented with a three-part circular diagram." />
</Frame>

Attribute rules and best practices

| Rule        | Recommendation                                                                              |
| ----------- | ------------------------------------------------------------------------------------------- |
| Key type    | Keys must be non-null strings. Use concise, consistent naming.                              |
| Value types | Values may be `string`, `boolean`, `integer`, `float`, or arrays of these primitives.       |
| Avoid nulls | Do not record null values; omit attributes when the value is unknown.                       |
| Key naming  | Prefer short, stable keys; use semantic conventions for common technical attributes.        |
| When to set | Add business-critical attributes early in execution to influence sampling and availability. |

<Frame>
  <img alt="The image shows a set of attribute rules for key-value pairs, emphasizing non-null keys, specific data types for values, and guidance on adding attributes. There's also an illustration of a person standing next to a checklist." />
</Frame>

<Callout icon="lightbulb">
  Use [semantic conventions](https://opentelemetry.io/docs/reference/specification/semantic_conventions/) (standardized attribute keys such as `http.method`, `db.system`, `messaging.operation`) where possible. These conventions promote consistency across services and make cross-system analysis easier.
</Callout>

Semantic attributes are predefined keys from the OpenTelemetry semantic conventions. Many auto-instrumentation libraries populate these automatically (for example, HTTP libraries add `http.method`, `http.url`, etc.), so you often do not need to add them manually. Use manual attributes for business-specific metadata (e.g., `order_id`, `payment_method`) to make traces searchable and filterable by business context.

Summary — key takeaways

* Span attributes are key-value metadata attached to spans to provide contextual, queryable information.
* Keys must be non-null strings; values must be primitives (`string`, `boolean`, `integer`, `float`) or arrays of primitives.
* Use semantic conventions for technical attributes; use manual instrumentation for business attributes.
* Add attributes early so they are available to sampling and analysis.
* Attributes enable trace filtering, aggregation, and more precise alerting based on business context.

<Frame>
  <img alt="The image lists five key takeaways related to span attributes, including guidelines on metadata, keys, business context, SDK rules, and trace management. The takeaways are presented in a sequential, numbered format." />
</Frame>

Attributes are attached to individual spans and do not automatically propagate to child spans (unlike the trace ID). If you need to propagate key-value pairs across process boundaries or between spans, use baggage.

<Callout icon="warning">
  Span attributes are not propagated across spans. To propagate key-value pairs across process boundaries, use baggage instead.
</Callout>

Links and references

* [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/instrumentation/python/)
* [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)
* [OpenTelemetry Specification](https://opentelemetry.io/docs/reference/specification/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/91d8fdff-0330-4591-b923-9cd10c509c3b" />
</CardGroup>


# Span Events vs Span Attributes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Events-vs-Span-Attributes/page

Explains when to use span events for timestamped occurrences and span attributes for persistent contextual metadata in traces

If both span events and span attributes can hold key-value pairs, how do you decide which to use?

Here’s a simple rule of thumb:

* If the timing of the action matters, use a span event.
* If it’s descriptive context about the span, use an attribute.

Example scenario: file upload span

* A user uploads a file and a virus scan runs during that flow.
  * Detecting a virus is a point-in-time action — it occurred at a specific moment during the span. Use a span event for that.
  * Details like file type and file size describe the span but are not tied to a single instant. Use span attributes for those.

Example (single, consolidated code snippet):

```python theme={null}
