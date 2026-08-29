# Demo Span Processors

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Span-Processors/page

Guide for switching OpenTelemetry Python span processors, comparing SimpleSpanProcessor and BatchSpanProcessor, with code samples, trade-offs, and shutdown tips to ensure spans flush.

This guide shows how to switch the span processor used by your OpenTelemetry Python instrumentation. It explains the trade-offs between SimpleSpanProcessor and BatchSpanProcessor, provides sample code you can copy, and includes tips to ensure spans are flushed at process exit.

At a high level:

* SimpleSpanProcessor exports each span synchronously when it ends — convenient for local debugging but adds latency and should not be used in production.
* BatchSpanProcessor buffers spans and exports them from a background worker thread in batches — recommended for production to minimize impact on application latency.

Quick comparison

|           Processor | Behavior                                        | Use case                             |
| ------------------: | ----------------------------------------------- | ------------------------------------ |
| SimpleSpanProcessor | Exports each span synchronously when it ends    | Local development, debugging         |
|  BatchSpanProcessor | Buffers spans and exports in background batches | Production (low-latency deployments) |

Keywords: OpenTelemetry, span processor, BatchSpanProcessor, SimpleSpanProcessor, Python instrumentation, exporter, OTLP

## Example: SimpleSpanProcessor (local testing)

Keep this minimal configuration for local debugging. It uses the ConsoleSpanExporter and SimpleSpanProcessor. Do not use this in production because exporting occurs on the same thread as your application code.

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(exporter)
    provider = TracerProvider()
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("payment.py", "0.1.0")

tracer = configure_tracer()

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    print("processing payment")
    # validate_card()
    # charge_card()

if __name__ == "__main__":
    process_payment()
    # Optionally flush/shutdown provider to ensure all spans are exported before exit:
    trace.get_tracer_provider().shutdown()
```

Explanation:

* SimpleSpanProcessor synchronously invokes the exporter when each span ends, which can block the application thread and increase latency.

<Callout icon="lightbulb">
  Use SimpleSpanProcessor only for local development or interactive debugging. For production deployments, prefer BatchSpanProcessor to avoid adding latency to your application's main threads.
</Callout>

## Switching to BatchSpanProcessor (production)

BatchSpanProcessor aggregates spans and exports them on a schedule from a separate worker thread. To switch, replace SimpleSpanProcessor with BatchSpanProcessor and pass the exporter instance to its constructor.

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)  # exporter is required
    provider = TracerProvider()
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("payment.py", "0.1.0")

tracer = configure_tracer()

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    print("processing payment")
    # validate_card()
    # charge_card()

if __name__ == "__main__":
    process_payment()
    # Ensure the provider (and its span processors) are shutdown to flush remaining spans:
    trace.get_tracer_provider().shutdown()
```

<Callout icon="warning">
  If you call `BatchSpanProcessor()` without passing an exporter you will see:

  ```Python theme={null}
  TypeError: BatchSpanProcessor.__init__() missing 1 required positional argument: 'span_exporter'
  ```

  Always pass the exporter instance (for example, `ConsoleSpanExporter()` or an `OTLP` exporter).
</Callout>

Notes on behavior and best practices:

* BatchSpanProcessor reduces application-thread latency by exporting spans on a worker thread in batches.
* Because batching is asynchronous, console output or exported spans may appear slightly delayed compared to SimpleSpanProcessor.
* Always call `trace.get_tracer_provider().shutdown()` (or otherwise shut down the provider) at process termination to flush any remaining spans.
* For production, prefer an exporter suited to your backend (for example, OTLP exporter). See the References section below for exporter options and configuration details.

## Sample console output (ConsoleSpanExporter)

Below is a representative example of a span exported by ConsoleSpanExporter (formatted JSON):

```json theme={null}
{
  "name": "Payment Service",
  "context": {
    "trace_id": "0x4b2740333ec9c3ac90445cb3a9a3de",
    "span_id": "0x3bad5c03252174ba",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-09-09T01:10:06.523273Z",
  "end_time": "2025-09-09T01:10:06.523365Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {},
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry"
    }
  }
}
```

Summary

* Use SimpleSpanProcessor for quick local debugging only.
* Use BatchSpanProcessor in production to reduce the latency impact on your main application threads.
* Always provide an exporter instance to BatchSpanProcessor and ensure the tracer provider is shut down at application exit to flush spans.

## Links and References

* [OpenTelemetry Python Instrumentation](https://opentelemetry.io/docs/instrumentation/python/)
* [OpenTelemetry Python Exporters — Console and OTLP](https://opentelemetry.io/docs/instrumentation/python/exporters/)
* [OTLP exporter configuration](https://opentelemetry.io/docs/reference/specification/protocol/otlp/)
* [OpenTelemetry Tracing SDK for Python](https://github.com/open-telemetry/opentelemetry-python)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/cde88149-90da-4fb4-ab35-8e277e8e6960" />
</CardGroup>
