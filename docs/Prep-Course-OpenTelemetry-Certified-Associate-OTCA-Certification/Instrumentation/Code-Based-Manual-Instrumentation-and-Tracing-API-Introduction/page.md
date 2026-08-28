# Code Based Manual Instrumentation and Tracing API Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Code-Based-Manual-Instrumentation-and-Tracing-API-Introduction/page

Explains manual code instrumentation with the OpenTelemetry Tracing API, how to create and export spans, configure SDKs, and best practices for tracing and context propagation.

In this lesson we dive into code-based (manual) instrumentation to understand how telemetry—traces, spans, metrics, and logs—is produced. Once you grasp manual instrumentation with the OpenTelemetry Tracing API, library-based auto-instrumentation becomes straightforward.

Instrumentation = explicit telemetry calls in application code (via the OpenTelemetry API) so you can control:

* which operations are traced,
* which metadata (attributes/events/exceptions) is captured, and
* which signals are produced and exported.

<Callout icon="lightbulb">
  This lesson uses `ConsoleSpanExporter` so spans are visible on your console for demonstration. In production you would normally use an OTLP exporter (via the Collector) or a vendor-specific exporter.
</Callout>

OpenTelemetry architecture (quick recap)

<Frame>
  <img alt="The image is an overview of the OpenTelemetry architecture, illustrating various components such as the OpenTelemetry API, SDK, and Collector, along with integrations for Kubernetes and observability backends." />
</Frame>

Key components and responsibilities:

| Component            | Purpose                                                                      | Example / Notes                             |
| -------------------- | ---------------------------------------------------------------------------- | ------------------------------------------- |
| OpenTelemetry API    | Language-neutral contract you code against (tracing, metrics, logs, context) | `trace.get_tracer(...)`, `start_span`       |
| SDK                  | Language-specific implementation that records, samples, batches              | `TracerProvider`, `SpanProcessor`           |
| Span export pipeline | Buffers/batches spans and passes to exporters                                | `SimpleSpanProcessor`, `BatchSpanProcessor` |
| Exporter             | Sends spans to backends (Console, OTLP, vendor)                              | `ConsoleSpanExporter`, `OTLPSpanExporter`   |
| Collector / Backend  | Receives, stores, and visualizes telemetry                                   | Jaeger, Tempo, commercial APMs              |

What is manual (code-based) instrumentation?

<Frame>
  <img alt="The image explains manual or code-based instrumentation, describing it as a process where developers add telemetry calls using the OpenTelemetry API in their source code to control tracing, metadata capture, and telemetry signal creation." />
</Frame>

Manual instrumentation means you explicitly call the OpenTelemetry API in your source:

* create tracers,
* start and end spans,
* set attributes,
* add events or record exceptions,
* and handle context propagation.

This approach gives the most control and the most accurate representation of application behavior.

Tracing API workflow

<Frame>
  <img alt="The image shows a &#x22;Tracing API Workflow&#x22; diagram with seven steps: Requesting a Tracer, Creating a Span, Sampling Decision, Span Processor, Applying SpanLimits, Exporting the Span, and Trace Visualization." />
</Frame>

High-level flow:

1. Configure a TracerProvider (SDK wiring).
2. Request a `Tracer`.
3. Create spans (`start_span` / `start_as_current_span`).
4. Sampling decision — spans are recorded or dropped.
5. `SpanProcessor` receives spans and enforces `SpanLimits`, batching/retrying as needed.
6. `Exporter` sends spans to the configured backend (OTLP, Console, vendor exporter).
7. Backend visualizes traces.

TracerProvider is the factory and central access point for tracers. The Context API binds spans into traces and supports propagation across process/network boundaries.

Core Tracing API components and definitions

* TracerProvider: provides `Tracer` instances (SDK-managed).
* Tracer: used to start spans.
* Span: represents a single timed operation.
* SpanProcessor: processes spans (batching, exporting).
* SpanExporter: converts and sends span data to backends.

Examples

Basic application (no OpenTelemetry calls yet)

```python theme={null}
