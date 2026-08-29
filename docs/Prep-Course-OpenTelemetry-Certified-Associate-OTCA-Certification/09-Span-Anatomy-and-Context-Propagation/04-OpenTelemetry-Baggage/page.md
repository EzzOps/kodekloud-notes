# OpenTelemetry Baggage

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/OpenTelemetry-Baggage/page

Explains OpenTelemetry baggage propagation, differences from span attributes, usage examples, security risks, and best practices for contextual key value metadata across services

In this lesson we cover OpenTelemetry Baggage: what it is, how it differs from span attributes, common use cases, code examples for setting and reading baggage, and security and best-practice guidance.

Baggage is a small set of contextual key-value pairs that travel with requests across service boundaries via headers. Downstream services can read those keys to enable business-level routing, personalization, or to copy values into span attributes for observability.

## Observability signals — quick recap

| Signal  | Purpose                                              | Typical examples                   |
| ------- | ---------------------------------------------------- | ---------------------------------- |
| Traces  | End-to-end execution paths for requests              | Request spans, latency             |
| Metrics | Aggregated numeric measurements                      | CPU, throughput, error rates       |
| Logs    | Event-level diagnostic messages                      | Exceptions, debug events           |
| Baggage | Small contextual metadata propagated across services | `user_id`, `cart_id`, `promo_code` |

Baggage commonly carries non-sensitive values such as `user_id` (non-identifying), `region`, `tier=gold`, `product_id`, `cart_id`, or promotion codes like `SUMMER10`. A frontend service can capture a promo code and propagate it so downstream services can use it for personalized messaging or business logic.

## Baggage vs. span attributes

* Baggage: propagated across services using request headers (W3C Baggage format). It is intended to be read by all services that participate in context propagation.
* Span attributes: local to a span and used to enrich trace data for that single span. They are stored in your observability backend but are not automatically forwarded downstream.

<Frame>
  <img alt="The image compares &#x22;Baggage&#x22; and &#x22;Span Attributes,&#x22; showing how product ID, cart ID, and promo code are represented in HTTP request headers and span attributes, with similar values formatted differently in each context." />
</Frame>

Span attributes are visible in tracing backends but not automatically propagated. If downstream services need specific values (for example, to send a promotional email), propagate them via baggage headers; the downstream service may decide to copy those values into span attributes for observability or use them in application logic.

The diagram below shows baggage being set in Service A, flowing via headers through Service B, and being consumed or copied into span attributes in Service C.

<Frame>
  <img alt="The image depicts a diagram illustrating &#x22;Baggage in Action&#x22; within a microservices architecture, showing the flow of request context and attributes between Service A, Service B, and Service C." />
</Frame>

## Python example — set baggage and inject into outgoing headers

Steps:

1. Use the baggage API to set key-value pairs into a context.
2. Use the propagation API to inject the context into outgoing HTTP headers.

```python theme={null}
from opentelemetry import baggage, propagate
