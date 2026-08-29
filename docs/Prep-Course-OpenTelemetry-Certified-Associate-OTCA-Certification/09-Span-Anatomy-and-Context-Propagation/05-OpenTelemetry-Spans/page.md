# start from an existing context (None is acceptable)
ctx = None
ctx = baggage.set_baggage("product_id", "SKU-12345", context=ctx)
ctx = baggage.set_baggage("cart_id", "cart-42", context=ctx)
ctx = baggage.set_baggage("promo_code", "SUMMER10", context=ctx)

# Inject baggage into outgoing HTTP headers (carrier is a dict here)
headers = {}
propagate.inject(headers, context=ctx)
# headers now contains a W3C Baggage header like:
# baggage: product_id=SKU-12345,cart_id=cart-42,promo_code=SUMMER10
```

## Python example — extract baggage from incoming headers and copy into span attributes

On the receiving side, extract the context from incoming headers, read baggage values, and optionally copy them into span attributes for better observability.

```python theme={null}
from opentelemetry import baggage, propagate, trace

# incoming request headers (a dict-like carrier)
headers = {
    # e.g. 'baggage': 'product_id=SKU-12345,cart_id=cart-42,promo_code=SUMMER10'
}

# Extract context from incoming headers
ctx = propagate.extract(headers)

# Read baggage values from the extracted context
product = baggage.get_baggage("product_id", context=ctx)
cart = baggage.get_baggage("cart_id", context=ctx)
promo = baggage.get_baggage("promo_code", context=ctx)

# Copy baggage into a span for observability or use in business logic
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("downstream.process", context=ctx) as span:
    span.set_attribute("commerce.product.id", product or "")
    span.set_attribute("commerce.cart.id", cart or "")
    span.set_attribute("commerce.promo.code", promo or "")
```

Resulting span attributes (example):

```json theme={null}
{
  "commerce.product.id": "SKU-12345",
  "commerce.cart.id": "cart-42",
  "commerce.promo.code": "SUMMER10"
}
```

Once a downstream service has the promo code in its context, it can trigger actions (for example, send an email that references the promo code) or propagate the baggage further downstream.

## Real-world use cases

| Category                  | Example baggage keys                      | Purpose                                                                   |
| ------------------------- | ----------------------------------------- | ------------------------------------------------------------------------- |
| Correlation               | `correlation_id`                          | Link related business operations across services (distinct from trace ID) |
| Commerce                  | `cart_id`, `product_id`, `transaction_id` | Route or enrich commerce flows                                            |
| Routing / Personalization | `region`, `origin`, `tier`                | Use for routing decisions or personalized responses                       |
| Analytics                 | `non-identifying_user_attr`               | Aggregate business metrics without exposing PII                           |

<Frame>
  <img alt="The image illustrates real-world use cases of data tracking and personalization, featuring colorful arrows pointing towards different identifiers like correlation IDs, cart IDs, and non-identifying user IDs." />
</Frame>

## Security considerations

Baggage travels in HTTP headers and is visible to every intermediate and downstream service. Because baggage does not provide integrity or confidentiality guarantees by default:

* Values can be modified or tampered with by intermediaries.
* Sensitive data can be exposed if baggage leaves trusted networks.
* Avoid putting PII, credentials, tokens, or sensitive secrets into baggage.

> **warning** Baggage is not a secure transport. Avoid putting sensitive or identifying data in baggage, and exercise caution when propagating baggage beyond trusted boundaries.

<Frame>
  <img alt="The image lists security considerations regarding baggage, highlighting issues like visibility via headers, lack of integrity checks, risk of sensitive data exposure, and the need for caution beyond trusted boundaries." />
</Frame>

## Best practices

* Keep baggage small to limit header size and avoid network overhead.
* Standardize key names and conventions across teams to reduce collisions and simplify downstream processing.
* Never include PII, credentials, or tokens in baggage.
* Monitor performance and header sizes when enabling baggage propagation.

> **lightbulb** Define a small, consistent set of baggage keys and document their intended use. This keeps cross-team usage predictable and reduces the risk of accidental sensitive data propagation.

<Frame>
  <img alt="The image lists three best practices: keeping baggage small, standardizing keys for consistency, and avoiding sensitive data, accompanied by relevant icons. There's also a thumbs-up badge illustration." />
</Frame>

## Key takeaways

* Baggage carries small contextual metadata along with requests and complements traces, metrics, and logs.
* Use baggage to enable richer cross-service observability and business-level processing when appropriate.
* Keep baggage minimal, standardized, and free of sensitive data to avoid performance and security issues.

<Frame>
  <img alt="The image is a &#x22;Key Takeaways&#x22; slide listing four points about observability, including metadata handling, complementing observability signals, enabling cross-service analysis, and handling carefully to avoid risks." />
</Frame>

Further lessons will dive deeper into context and propagation mechanisms, including W3C standards and language-specific propagation implementations.

## Links and references

* W3C Baggage: [https://www.w3.org/TR/baggage/](https://www.w3.org/TR/baggage/)
* OpenTelemetry Propagation: [https://opentelemetry.io/docs/reference/specification/context/api/](https://opentelemetry.io/docs/reference/specification/context/api/)
* OpenTelemetry Python docs: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/3da5cbd9-6112-4395-b0e2-8714c057511d)


# OpenTelemetry Spans

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/OpenTelemetry-Spans/page

Overview of OpenTelemetry spans, explaining their structure, purpose, examples, and best practices for tracing operations, attributes, events, links, and parent child relationships.

When we talk about distributed tracing with OpenTelemetry, everything begins with spans.

A span records a single operation: what happened, when it started and ended, and contextual details that help you understand behavior and performance. Spans link together into traces to tell the full story of a request as it traverses services.

So, a trace represents the full journey

<Frame>
  <img alt="The image depicts a funnel diagram representing a trace composed of several spans labeled A to H, with an arrow indicating the flow from top to bottom." />
</Frame>

of a request across multiple services. Each bar here is a span — a discrete operation — and the connections between them form the trace. The root span starts the trace; child spans represent downstream operations. Together, they form an end-to-end timeline of work.

A span represents a single operation within a trace, clearly marked

<Frame>
  <img alt="The image explains the concept of a &#x22;Span,&#x22; describing it as a fundamental unit of work within a trace with a defined start and end." />
</Frame>

with a defined start and end time. A span is the fundamental unit of work: combine many spans and you reconstruct the request lifecycle.

## What can a span represent?

Think of a span as one measurable piece of work inside your application. Typical examples include:

* A function or internal business-logic execution.
* An outgoing HTTP/gRPC call (for example, fetching product details from another service).
* A database operation such as a SQL query.
* File I/O, encryption/decryption, or image compression.
* Lightweight work like JSON parsing or payload validation.
* Message processing (consuming a single Kafka message).
* UI rendering (for instance, a React component render).
* Background tasks, retries, authentication flows, and notification delivery.

Choose spans around the operations you care about measuring (latency and errors). Too coarse and you miss detail; too fine and you generate noise and overhead.

This table shows practical examples and typical measurements.

<Frame>
  <img alt="The image is a table showing different span operations, what they measure in duration, possible exceptions, span type, and status for each operation in a monitoring or tracing system." />
</Frame>

Additional examples include parsing JSON payloads (measuring payload handling), internal business functions (execution time and logic errors), external API calls (network latency and authentication failures), and cache lookups (e.g., Redis key lookup latency and misses).

<Frame>
  <img alt="The image is a table explaining what a span can represent in a computing context, detailing the span operation, what it measures, possible exceptions, span kind, and status. Different operations like JSON parsing, internal functions, and external API calls are mentioned with their related exceptions and statuses." />
</Frame>

## Span structure: what a span includes

An OpenTelemetry span captures a consistent set of fields that let you reason about the operation and how it relates to other work:

* The span name (human-readable).
* The span ID and the parent span ID (`parent_id` is `null` for a root span).
* Start and end timestamps.
* The span context (the trace identifiers that propagate across services).
* Attributes (key/value pairs that add descriptive metadata).
* Events (time-stamped annotations, commonly used to record exceptions or milestones).
* Links (optional references to other spans or traces).
* Span status (for example, `OK`, `ERROR`, or `UNSET`).

Resource attributes indicate where the span originated (for example, `service.name`). The `schema_url` can describe the semantics of attribute keys.

<Frame>
  <img alt="The image lists components included in a span in OpenTelemetry, such as Name, Span ID, Parent span ID, Timestamps, Span Context, Attributes, Span Events, and Span Links." />
</Frame>

## Example: a recorded span (JSON)

Below is a representative OpenTelemetry span encoded as JSON. It models a client span that performed an HTTP GET and recorded an event when the response arrived.

```json theme={null}
{
  "name": "call_httpbin_delay",
  "context": {
    "trace_id": "089f12de04e7927b486956fda8c89d95",
    "span_id": "6ce906987b32cfe5",
    "trace_state": ""
  },
  "kind": "SpanKind.CLIENT",
  "parent_id": "8c18abb071ce362d",
  "start_time": "2025-04-28T13:02:19.535763Z",
  "end_time": "2025-04-28T13:02:22.429104Z",
  "status": {
    "status_code": "OK"
  },
  "attributes": {
    "http.method": "GET",
    "http.url": "http://httpbin.org/delay/2",
    "response.content_length": 358
  },
  "events": [
    {
      "name": "Received response",
      "timestamp": "2025-04-28T13:02:22.429067Z",
      "attributes": {
        "response_length": 358
      }
    }
  ],
  "links": [],
  "resource": {
    "attributes": {
      "service.name": "unknown_service"
    }
  },
  "schema_url": ""
}
```

Key fields to note:

* `name`: human-readable operation name.
* `context.trace_id` and `context.span_id`: identifiers that link spans into traces.
* `kind`: the span kind (for example, `SpanKind.CLIENT` or `SpanKind.SERVER`).
* `parent_id`: links a span to its parent (or is `null` for the root).
* `start_time` and `end_time`: timestamps; duration = `end_time - start_time`.
* `status.status_code`: for example, `OK`, `ERROR`, or `UNSET`.
* `attributes`: contextual key/value pairs (network info, DB statement, user id, etc.).
* `events`: time-stamped events within the span (exceptions, response reception).
* `links`: optional cross-trace relations, useful for batching or forks.
* `resource.attributes`: metadata about the originating service (for example, `service.name`).
* `schema_url`: optional pointer to attribute semantics.

A span marked with `status.status_code: "OK"` indicates success. When an exception occurs, it's common to record the exception as an event and set the span status to `ERROR`.

> **lightbulb** Choose span granularity deliberately — capture operations you need for latency and error visibility. Avoid over-instrumentation (which creates noise and overhead) and under-instrumentation (which loses useful diagnostic detail).

## Summary

* A span captures one operation or unit of work with start/end times and contextual data.
* Parent/child relationships and links join spans into traces that represent the end-to-end request journey.
* Spans include IDs, timestamps, attributes, events, links, status, and resource metadata.
* Be intentional about span boundaries: balance observability detail against system overhead.

## Links and References

* OpenTelemetry Specification: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* OpenTelemetry Trace Semantic Conventions: [https://opentelemetry.io/docs/reference/specification/trace/semantic\_conventions/](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/24ed6d32-cf1a-4c47-936f-697e3ebb7617)
