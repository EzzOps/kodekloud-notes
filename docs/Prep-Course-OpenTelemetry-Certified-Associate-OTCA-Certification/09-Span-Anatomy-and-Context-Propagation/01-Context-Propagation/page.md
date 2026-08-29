# Context Propagation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Context-Propagation/page

Explains OpenTelemetry context propagation including trace context and baggage, W3C and B3 formats, propagators, inject and extract workflows, and composite support for cross service distributed tracing.

Hello, span explorers.

This article explains context propagation — a core concept in distributed tracing — and shows how OpenTelemetry moves trace context and baggage across processes and services. Building on span basics (start/end time, events, attributes, span context, and baggage), you'll learn:

* What span context and baggage contain
* Why a universal trace format matters
* How OpenTelemetry injects and extracts context across carriers
* Common propagation formats you will encounter (W3C Trace Context, B3, Composite)

Quick recap — what span context and baggage hold:

* Trace ID: ties the entire trace together
* Span ID: uniquely identifies a single span
* Trace flags: indicates whether the span was sampled
* Trace state: vendor-specific data

Baggage is arbitrary key-value metadata that travels with the context (e.g., product ID, cart ID, promo code). This helps services downstream make decisions or add useful attributes to spans.

<Frame>
  <img alt="The image illustrates the flow of key-value pairs in a request context from Service A to Service B to Service C, including information like product ID, cart ID, and promo code." />
</Frame>

Trace context contains the tracing identifiers and flags; baggage carries custom key/value metadata. To move both across service boundaries we need a standard wire format.

<Frame>
  <img alt="The image illustrates the flow of request context and trace information between three services, labeled Service A, Service B, and Service C, highlighting the need for a universal trace format." />
</Frame>

Why a standard format?

Historically, many APM vendors and open-source tools used proprietary HTTP headers for propagation. Non-standard headers are often dropped by middleware, load balancers, or proxies, which breaks distributed traces. To solve these interoperability problems, the W3C Trace Context standard (circa 2018) became the industry default and is the OpenTelemetry default format. W3C Trace Context ensures cross-vendor compatibility so services and tools can read and continue traces reliably.

<Frame>
  <img alt="The image illustrates how APM vendors and open-source tools use their own defined HTTP headers, leading to issues like middleware complications and broken transactions. It emphasizes the importance of W3C TraceContext and Baggage for OTel." />
</Frame>

W3C Trace Context and W3C Baggage are HTTP header formats. The primary headers are `traceparent`, `tracestate`, and `baggage`.

Example (illustrative):

```text theme={null}
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: vendorname=value
baggage: user_id=42,region=us-east
```

* `traceparent`: core trace identifiers and flags
* `tracestate`: optional vendor-specific metadata
* `baggage`: arbitrary key-value pairs that travel with the request

Note: propagation extends beyond HTTP. The same header concepts apply to gRPC metadata, message attributes in queues, and other carriers.

When OpenTelemetry is configured and instrumented correctly, propagators automatically inject and extract these headers so traces continue across service boundaries.

<Frame>
  <img alt="The image illustrates the flow of headers through a sequence of services labeled Service 1 to Service 4, under the concept of &#x22;W3C Trace Context & Baggage.&#x22;" />
</Frame>

Propagation workflow

Before making an outbound call, the current trace context is injected into a carrier (HTTP headers, gRPC metadata, or a message). On the receiving side, the trace context is extracted from that carrier and restored into the receiving process so the trace can continue.

<Frame>
  <img alt="The image illustrates the process of propagating context from &#x22;Service A&#x22; to &#x22;Service B&#x22; using HTTP/gRPC carriers, with context injected into and extracted from W3C headers." />
</Frame>

Propagation is simply the serialization and deserialization of the context object. That context contains trace ID, span ID, trace state, trace flags — plus baggage. Most OpenTelemetry instrumentation handles propagation automatically, but custom integrations use the propagators API directly.

<Frame>
  <img alt="The image is an overview of propagation concepts, explaining the passing of context across processes, serialization/deserialization for information transfer, and the use of libraries and APIs for handling propagation." />
</Frame>

Context management

A single process may have multiple spans concurrently (especially in async or multithreaded apps). The context manager tracks the active span and baggage so the correct span ID is injected into outgoing requests. Proper context management is essential to avoid leaking or mis-associating spans.

<Frame>
  <img alt="The image explains the functions of a Context Manager in tracking active spans, including maintaining context, ensuring active spans, handling contexts, and supporting asynchronous and multi-threaded apps." />
</Frame>

Propagator API: core concepts

* TextMapPropagator: interface that reads/writes context into carriers (key-value maps).
* Carrier: the transport medium (HTTP headers, gRPC metadata, message attributes).
* Setter/Getter: functions that write/read keys to/from the carrier.
* inject: write the current context into an outgoing carrier.
* extract: read context from an incoming carrier and restore it to the process.

Pseudocode example:

```python theme={null}
