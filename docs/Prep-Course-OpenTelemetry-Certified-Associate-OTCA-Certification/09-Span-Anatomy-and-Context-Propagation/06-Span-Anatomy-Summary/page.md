# Span Anatomy Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Span-Anatomy-Summary/page

Overview of OpenTelemetry span anatomy, context propagation, span data model, span kinds, and instrumentation approaches for tracing distributed systems

This lesson summarizes the anatomy of a span and the related concepts used in distributed tracing with OpenTelemetry. It explains what spans capture, how context is propagated between services, and the common approaches to instrumenting applications.

## What is tracing?

Tracing tracks requests as they flow through a distributed system to capture latency, errors, and contextual metadata across the whole request path. A trace is composed of spans, which represent units of work and their relationships.

## Span basics

* Span: the smallest unit of work in a trace, representing an operation such as "HTTP GET /orders", "DB query", or "ProcessPayment".
* Trace ID: a unique identifier shared by all spans in a single trace.
* Span ID: a unique identifier for an individual span; used to link spans together.
* Span name: a human-readable label describing the operation, e.g., `GET /api/orders` or `ProcessPayment`.

## Key span concepts

* Context
  * Carries trace state (trace ID, current span ID, trace flags, optional trace state) across process boundaries.
  * Context propagation is how this state flows from one service to another using propagators (e.g., W3C Trace Context).
* Span links
  * Link spans that are not in a parent-child relationship—useful for correlating related work or asynchronous workflows.
* Span timing
  * Each span has a start and end timestamp. Duration = end - start. Observability systems use span timings to find slow operations and bottlenecks.

<Frame>
  <img alt="The image is a table summarizing OpenTelemetry span concepts, including terms like tracing, spans, span links, and span timings with their descriptions." />
</Frame>

## Span data model

* Span attributes
  * Key-value pairs attached to a span to add contextual detail (e.g., `user.id`, `db.statement`, `http.method`).
* Span events
  * Timestamped events recorded within a span (e.g., "DB query executed" at time T). Often used for exceptions and log-like entries; events can include attributes such as stack traces or error messages.
* Exceptions and status
  * Exceptions are typically recorded as span events and should also be reflected in span status.
  * Common span status values: `UNSET` (default), `OK`, `ERROR`.
* Span resource
  * Resource attributes describe the telemetry-producing entity (service name, host, region, process).
  * Resource detectors can auto-populate details (cloud provider, OS, CPU architecture).
* Context propagation
  * Propagators carry tracing context across service boundaries (by default OpenTelemetry supports W3C Trace Context and W3C Baggage via text-map carriers).
* Baggage
  * Propagated key-value metadata attached to the trace context and sent to every downstream service.
  * Keep baggage small and avoid sensitive data.

<Frame>
  <img alt="The image is a summary table of OpenTelemetry Span Concepts, outlining various concepts like Span Attributes, Span Events, Span Status & Exception Recording, Span Resource, Context Propagation, and Baggage, along with their descriptions." />
</Frame>

<Callout icon="lightbulb">
  Keep baggage minimal and never include sensitive or personally identifiable information. Baggage is propagated to every downstream service that receives the trace context.
</Callout>

## Span kinds (roles)

Span kinds describe a span’s role in an interaction. They help consumers interpret the trace topology.

| Span kind | Typical usage                                         |
| --------- | ----------------------------------------------------- |
| CLIENT    | Outgoing request caller (e.g., HTTP client)           |
| SERVER    | Request receiver (e.g., HTTP server)                  |
| INTERNAL  | In-process operations (e.g., business logic)          |
| PRODUCER  | Creates a message or event (e.g., publishes to Kafka) |
| CONSUMER  | Processes a message or event (e.g., Kafka consumer)   |

## How spans are used in practice

* Troubleshooting: identify slow spans via duration and stack traces captured in events.
* Error analysis: record exceptions as span events and set span status to `ERROR`.
* Service mapping: use span kinds and resource attributes to build service-to-service graphs.
* Debugging distributed flows: use span links to correlate asynchronous or multi-trace work.

## Instrumentation: how spans and contexts are created

Instrumentation is the process of creating spans and propagating context. There are three common approaches:

* Manual instrumentation — explicitly create and manage spans in application code using the SDK.
* Library (SDK) instrumentation — use language or framework libraries with helper APIs to instrument standard operations.
* Auto-instrumentation — zero-code agents that instrument supported libraries automatically; great for rapid coverage.

<Frame>
  <img alt="The image is a diagram depicting different instrumentation techniques: Manual Instrumentation, Library Instrumentation, and Auto-Instrumentation. It's part of a presentation titled &#x22;Next Section: Instrumentation Deep Dive.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Choosing an instrumentation approach depends on your goals: start with auto-instrumentation for quick coverage, add library instrumentation for framework-specific support, and use manual spans for business-critical or custom operations.
</Callout>

We’ll next take a deep dive into instrumentation: starting with manual instrumentation to understand fundamentals, then covering library-based helpers, and finally exploring auto-instrumentation for large-scale, low-effort tracing.

## Further reading and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* W3C Trace Context: [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/)
* OpenTelemetry Specification (Tracing): [https://github.com/open-telemetry/opentelemetry-[SECRET_REDACTED]](https://github.com/open-telemetry/opentelemetry-[SECRET_REDACTED])

Well done completing the span anatomy section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/21cd96a5-0c33-444b-bca5-b98883617c7e" />
</CardGroup>
