# Span Attributes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Attributes/page

Explains OpenTelemetry span attributes and best practices for attaching key value metadata to spans for filtering debugging aggregation and business analytics

In this lesson we cover span attributes: what they are, why they matter, and how to use them effectively with OpenTelemetry.

Span attributes are key-value pairs attached to individual spans to provide contextual metadata about the operation being tracked. Without attributes, a span is essentially a timestamped name; attributes make spans rich, searchable, and actionable for filtering, debugging, aggregation, and alerting.

<Frame>
  <img alt="The image is a diagram about &#x22;Span Attributes,&#x22; describing them as key-value pairs attached to spans. It highlights two points: carrying metadata about the operation being tracked, and enriching spans with contextual information." />
</Frame>

Why use span attributes?

* Provide business context (order IDs, payment types) that makes traces searchable.
* Improve debugging by attaching relevant runtime details to an operation.
* Enable fine-grained alerting and aggregation (e.g., only alert on errors for a specific payment method).
* Support metric generation by aggregating attribute values across spans.

Example: e-commerce order processing

* Add `order_id`, `payment_method`, or `inventory_status` to the `process_order` span.
* Use these attributes to filter traces (for example, all spans where `payment_method` is `"Credit Card"`), or to group and analyze failures for specific products.

<Frame>
  <img alt="The image illustrates &#x22;Span Attributes&#x22; showing an example of attributes such as order ID, customer ID, payment method, and inventory status used to enrich spans for filtering, alerts, and analysis." />
</Frame>

Span attributes power trace filtering, aggregation, and targeted alerts. For example, you can configure your observability backend to surface exceptions only for spans related to credit card payments if it supports slicing trace data by attributes.

<Frame>
  <img alt="The image describes the importance of span attributes, highlighting trace filtering, aggregation, and alerting with corresponding icons." />
</Frame>

Types of attributes to capture

* Business data: `order_id`, `payment_method`, `product_sku`
* User data: `user_id`, `account_tier`
* Technical data: `http.status_code`, `db.system`, cache `hit`/`miss`

Combining these categories provides a 360-degree view of what occurred in a span and enables both technical troubleshooting and business analytics.

<Frame>
  <img alt="The image illustrates the concept of exposing business, user, and technical metadata with a graphic showing a person using a laptop, surrounded by a cloud and various devices. It is titled &#x22;Importance of Span Attributes.&#x22;" />
</Frame>

Attributes are especially valuable for modeling the lifecycle of business processes. For example, a `process_order` span that contains `order_id`, `payment_method`, and `inventory_status` lets you filter and debug fulfillment issues by order attributes.

<Frame>
  <img alt="The image shows a table with attributes related to e-commerce, including order ID, payment method, and inventory status with their corresponding values." />
</Frame>

How to set attributes (Python example)

Manual instrumentation is how you add business-focused attributes. With OpenTelemetry Python you obtain a span from the tracer and call `set_attribute` on the span object:

```python theme={null}
