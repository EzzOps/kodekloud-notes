# Example span context values (replace with real trace/span ids)
span_context = SpanContext(
    trace_id=0x0123456789abcdef0123456789abcdef,
    span_id=0x0123456789abcdef,
    is_remote=True,
    trace_flags=TraceFlags(1),
    trace_state=TraceState()
)

link = Link(span_context, attributes={"order.id": "12345"})

with tracer.start_as_current_span("process_item", links=[link]) as span:
    span.set_attribute("worker", "inventory-updater")
    # perform work for this independent span...
```

<Callout icon="lightbulb">
  Use span links when related work is produced and consumed asynchronously, when multiple independent workers process parts of a single logical operation, or when you need to associate messages and events without creating parent-child spans.
</Callout>

## Practical use cases

* Scatter-gather / Map-Reduce: link each worker span to the initiating job span.
* Message aggregation: link each message-processing span to the aggregator span.
* Transactional messaging: trace participating messages in a distributed transaction via links.
* Event sourcing: associate event-processing spans to the originating action or final state.

To make links useful, include identifying attributes (e.g., `order.id`, `message.id`, `job.id`) so backend systems can filter and join related spans.

<Frame>
  <img alt="The image outlines the practical uses of span links, which include Scatter-Gather/Map-Reduce, Message Aggregation, Transactional Messaging, and Event Sourcing, each with a brief description." />
</Frame>

## Quick comparison table

| Model        | When to use                                                                         | Example                                              |
| ------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Parent-Child | Synchronous call chains where one operation directly invokes another                | Service A calls Service B over HTTP                  |
| Span Links   | Asynchronous, parallel, or otherwise independent work that shares a trigger/context | Workers consuming messages related to the same order |

## Summary

Span links are a core OpenTelemetry feature for connecting related spans that are not in a parent-child relationship. They enable accurate tracing of modern asynchronous, parallel, and message-driven systems by allowing independent spans to reference one another via context and attributes.

<Frame>
  <img alt="The image is a summary of points about span links in OpenTelemetry, highlighting their role in connecting spans, being crucial for async and batch systems, and allowing workflow tracing." />
</Frame>

## Links and references

* OpenTelemetry specification — Tracing: [https://opentelemetry.io/docs/specs/trace/](https://opentelemetry.io/docs/specs/trace/)
* OpenTelemetry Python documentation: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* Distributed tracing concepts: [https://opentracing.io/](https://opentracing.io/) (conceptual background)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/9475eb2b-5716-40df-8215-df264b39f0d7" />
</CardGroup>


# Span Name and Context

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Name-and-Context/page

Guidance on naming spans and explaining span context and its components trace_id span_id trace_flags trace_state for effective distributed tracing and propagation

Hello, span gurus.

In this lesson we focus on span names and span context — two small but critical pieces that make distributed tracing useful. First we’ll cover naming guidance and how to capture important details as attributes. Then we’ll explain span context (the immutable metadata that travels between processes) and its components: trace\_id, span\_id, trace\_flags, and trace\_state.

## Span names

Span names are the human-readable labels you give to each span. They communicate, at a glance, what an operation represents (for example, `GET /home`, `processPayment`, or `validateUserInput`). Clear, consistent names make traces easier to read than raw IDs or hex strings and help you spot patterns and failures quickly.

Best practices

* Be consistent: adopt a small set of naming patterns across services (verb-object is a simple and effective convention, e.g., `process payment`, `send invoice`, `render ad`).
* Be generic: keep the span name focused on the operation, not request-specific details (put those in attributes).
* Use automatic instrumentation for common operations (HTTP, DB). Reserve custom spans for unique business logic or important internal steps.

Common examples of span names:

* `call httpbin` (external endpoint used in demos)
* `processPayment`
* `validateUserInput`
* `getProducts`
* `postOrders`
* `getProduct`
* `convertCurrency`
* `getCart`
* `listRecommendations`
* `listAdsByCategory`
* `getLoyaltyStatus`

<Callout icon="lightbulb">
  Keep span names generic and stable. Put request-specific details (URLs, IDs, amounts) into span attributes rather than the span name.
</Callout>

<Frame>
  <img alt="The image illustrates the concept of naming custom spans, differentiating between auto-instrumentation (handling standard operations like HTTP requests and DB queries) and custom spans (capturing unique business logic), with a naming convention of &#x22;verb object&#x22;." />
</Frame>

## Well-named business spans and attributes

Use a concise, generic span name for the operation and record request-specific data as attributes (key-value pairs) attached to the span. Backends may index frequently queried attributes, so choose and document the attributes you rely on.

Example patterns:

* Name: `processPayment`\
  Attributes: `payment.method`, `payment.amount`, `payment.currency`

* Name: `validateUserInput`\
  Attributes: `user.id`, `input.type`, `validation.result`

* Name: `getProducts` or `postOrders`\
  Attributes: `http.method`, `http.url`, `http.route`, `db.statement` (as applicable)

<Frame>
  <img alt="The image is a table titled &#x22;Well Named Business Spans and Their Context,&#x22; showing examples of span names, their representations, and associated attribute captures. It includes examples such as calling httpbin, processing payments, and validating user input." />
</Frame>

## Span context (the metadata that moves)

Span context is the immutable bundle of metadata attached to every span. It is the serialized object that is propagated between services and is essential for linking spans into a single distributed trace.

Key fields

| Field         | Purpose                                             | Typical format / example                                          |
| ------------- | --------------------------------------------------- | ----------------------------------------------------------------- |
| `trace_id`    | Links all spans in a single trace                   | `32-character hex` — e.g., `089f12de04e7927b486956fda8c89d95`     |
| `span_id`     | Identifies this specific span within the trace      | `16-character hex` — e.g., `8c18abb071c362d0`                     |
| `trace_flags` | 8-bit field controlling sampling behavior           | `00` or `01` (sampled)                                            |
| `trace_state` | Optional vendor-specific metadata (key=value pairs) | Comma/semicolon-separated list, e.g., `vendor1=val1,vendor2=val2` |

A representative (illustrative) span context (JSON-style for clarity):

```json theme={null}
{
  "context": {
    "trace_id": "089f12de04e7927b486956fda8c89d95",
    "span_id": "8c18abb071c362d0",
    "trace_state": [
      "f4fe05b2-bd92206c@eg=fw4;3;abf102d9;c4592;0;0;2ee;5607;2h01",
      "apmvendor=boo",
      "foo=bar",
      "ot=rv:6e6d1a75832a2f"
    ],
    "trace_flags": "0x01"
  }
}
```

Note: the HTTP propagation format is defined by the W3C Trace Context spec (for example, `traceparent` and `tracestate` headers). The JSON above is illustrative — the essential idea is that the trace id, span id, flags, and optional trace\_state are what get propagated between processes.

<Callout icon="lightbulb">
  Exam tip: When asked "which part moves across process boundaries?", the answer is the span context (trace\_id, span\_id, trace\_flags, and trace\_state), typically carried in headers during propagation.
</Callout>

## Trace ID

Trace ID links all spans in a single trace and remains the same for the life of that trace.

* Size & format: 16 bytes (128 bits), typically represented as a 32-character hexadecimal string (for example, `089f12de04e7927b486956fda8c89d95`).
* Purpose: allows trace tools to map a request path across services, databases, proxies, and more.
* Immutability: the trace ID does not change during the trace — if it changes, you are observing a different trace.

<Frame>
  <img alt="The image explains the size and format of a Trace ID, highlighting its uniqueness, 16-byte length in a hexadecimal format, and its purpose in mapping requests through systems." />
</Frame>

<Frame>
  <img alt="The image is a slide titled &#x22;Trace ID: Scope and stability,&#x22; explaining that a Trace ID can cover multiple services and locations, and is immutable once created." />
</Frame>

## Span ID

Span ID uniquely identifies a single span (one operation) within a trace.

* Size & format: 8 bytes (64 bits), typically represented as a 16-character hexadecimal string (for example, `8c18abb071c362d0`).
* Scope: unique within its trace (two spans in different traces can have the same span ID).
* Purpose: enables reconstruction of parent-child relationships, timing charts, and waterfall views.
* Parent relationships: a child span carries the span ID of its parent in its context; the root span has no parent span ID.

<Frame>
  <img alt="The image is an informational slide about Span ID Uniqueness, detailing the uniqueness of Span IDs within a trace, their length and format as a 16-character hexadecimal string, and a placeholder for purpose information." />
</Frame>

## Trace flags

Trace flags are an 8-bit field included in every trace context; they are primarily used for sampling decisions.

* Size & format: 8 bits (1 byte), commonly shown as two hex characters (e.g., `00`, `01`).
* Example values: `00` (no flags set), `01` (sampled).
* Common usage: when the sampled flag (`0x01`) is set, the trace is a candidate for export, subject to SDK/exporter configuration.

Example: access trace flags in OpenTelemetry Python

```python theme={null}
