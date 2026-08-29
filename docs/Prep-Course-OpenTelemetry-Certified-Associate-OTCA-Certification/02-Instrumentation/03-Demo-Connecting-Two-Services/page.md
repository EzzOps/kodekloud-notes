# 00_basic_app.py
def do_work():
    print("doing some work...")

def main():
    print("Calling the do_work function")
    do_work()
    print("End: Back from the main function")

if __name__ == "__main__":
    main()
```

Instrumenting with the OpenTelemetry API only (no SDK configured)

* Calling `trace.get_tracer(...)` without setting a TracerProvider results in a no-op (non-recording) provider. Calls are safe, maintain context, and do not raise errors, but spans are non-recording and will not be exported.

Example (API-only; default no-op provider):

```python theme={null}
# 01_api_only_noop.py
from opentelemetry import trace

# Using the default no-op tracer provider (no SDK configured)
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("parent"):
        print("doing some work...")
        with tracer.start_as_current_span("child"):
            print("doing some nested work...")

def main():
    with tracer.start_as_current_span("main_function_span"):
        print("Calling the do_work function")
        do_work()
        print("End: Back from the main function")

if __name__ == "__main__":
    main()
```

Run (no span output because no SDK exporter is configured):

```bash theme={null}
> python 01_api_only_noop.py
Calling the do_work function
doing some work...
doing some nested work...
End: Back from the main function
```

This is the no-op (non-recording) behavior: the API calls work and maintain context, but attributes, events, and spans are not recorded or exported until an SDK is configured.

No-op benefits

<Frame>
  <img alt="The image lists the benefits of No-Op in four points, highlighting code safety, telemetry readiness, TracerProvider compatibility, and secure API usage." />
</Frame>

Why this design?

* Safe: instrumentation calls won't break an application if telemetry isn't configured.
* Telemetry-ready: libraries and apps can include instrumentation before choosing a backend.
* Swappable: plug a real SDK and exporter later without changing instrumentation code.

Wiring an SDK to produce recording spans

To record and export spans you must configure an SDK `TracerProvider` and add a `SpanProcessor` + `Exporter`. The demo below uses `SimpleSpanProcessor` with `ConsoleSpanExporter`.

```python theme={null}
# 02_with_sdk_console_exporter.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# 1. Set up the tracer provider (enable SDK recording)
trace.set_tracer_provider(TracerProvider())

# 2. Configure a processor with a ConsoleSpanExporter
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# 3. Create a tracer (from the now-configured provider)
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("parent"):
        print("doing some work...")
        with tracer.start_as_current_span("child"):
            print("doing some nested work...")

def main():
    with tracer.start_as_current_span("main_function_span"):
        print("Calling the do_work function")
        do_work()
        print("End: Back from the main function")

if __name__ == "__main__":
    main()
```

Run the instrumented application (Console exporter prints spans in a JSON-like format):

```bash theme={null}
> python 02_with_sdk_console_exporter.py
Calling the do_work function
doing some work...
doing some nested work...
{
  "name": "child",
  "context": {
    "trace_id": "0x86637c13bf2e369e70c7962c33a3fd8d",
    "span_id": "0x534e8bbda33f2f4d",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": "0xd0070b7c88e250ff",
  "start_time": "2025-10-21T10:25:30.348403Z",
  "end_time": "2025-10-21T10:25:30.348508Z",
  "status": {
    "status_code": "UNSET"
  },
  "attributes": {},
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.37.0",
      "service.name": "unknown_service"
    }
  },
  "schema_url": ""
}
```

Notes:

* The root span (`main_function_span`) will have `parent_id: null` indicating it is the root of the trace.
* Resource attributes default to `service.name: "unknown_service"` unless you explicitly configure the `Resource` when creating the `TracerProvider`.
* To send spans to a backend, swap `ConsoleSpanExporter` for an OTLP exporter (or another vendor exporter) and configure its endpoint (e.g., point it at your Collector).

Why the SDK is required

* The API defines the contract (`get_tracer`, `start_span`, `set_attribute`, `add_event`, etc.).
* The SDK defines how spans are recorded, sampled, batched, and exported.
* Without the SDK, your instrumentation code is a safe no-op.

Language idioms

* Python: `tracer.start_as_current_span(...)`
* Java: `tracer.spanBuilder(...).startSpan()`
* JavaScript: `tracer.startSpan(...)`
* .NET: Activity-based starts

Core Tracing API functions and features

<Frame>
  <img alt="The image is a table describing the core features of a tracing API, including functions like get_tracer(), start_span(), set_attribute(), and add_event(), along with their descriptions and example usages." />
</Frame>

Common operations (Python examples):

```python theme={null}
from opentelemetry import trace
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation") as span:
    span.set_attribute("http.method", "GET")
    span.add_event("authorization_received", {"user": "alice"})
    try:
        # perform operation
        pass
    except Exception as exc:
        span.record_exception(exc)
        span.set_status(StatusCode.ERROR)
```

Key API operations:

* `get_tracer(module_name)`: organize telemetry per module.
* `start_span` / `start_as_current_span`: create spans and manage lifecycle.
* `set_attribute`: attach key-value metadata to spans.
* `add_event`: record transient events (e.g., `"request_received"`).
* `record_exception`: attach exception details to a span.
* `set_status`: mark span success/failure.
* End spans properly (use context managers / `with` blocks) to correctly measure duration.
* Context API & Propagators: preserve and propagate trace context across threads/processes and network boundaries.
* Baggage: small key-value pairs propagated across services.

No-op, safe defaults, and concurrency

<Frame>
  <img alt="The image illustrates &#x22;No-Op Implementation: Safe Defaults&#x22; with three features: absence of SDK and NoOp tracers, safe code execution, and secure instrumentation." />
</Frame>

OpenTelemetry falls back to no-op providers if no SDK is installed. This guarantees:

* Instrumentation does not break applications.
* Libraries may safely include instrumentation.
* The same instrumentation starts producing telemetry when an SDK is wired.

All OpenTelemetry tracing components are safe for concurrent use.

<Frame>
  <img alt="The image is a diagram showcasing various tracing API components that are safe for concurrent use, including TracerProvider, Tracer, Span, Context, and Events/Links." />
</Frame>

Example: a web server handling thousands of concurrent requests can use a single tracer instance; each request receives its own span context without manual locking.

Best practices

<Frame>
  <img alt="The image displays a summary of best practices for using tracers, including setting up one TracerProvider globally, naming tracers per module, ending spans properly, setting span names wisely, and using context propagation for distributed tracing." />
</Frame>

* Configure one `TracerProvider` per application (global or injected).
* Use `get_tracer(__name__)` or a per-module name to identify span origins.
* End spans properly (prefer context managers / `with`).
* Name spans after the operation type (e.g., `FetchUser`, `DatabaseQuery`) — avoid embedding identifiers (`FetchUser:alice`).
* Add attributes and follow semantic conventions whenever possible.
* Use context propagation (Propagators) for distributed tracing across services.
* Prefer configuring sampling and exporters outside application code so backends can be changed without modifying instrumentation.

That concludes this lesson on code-based (manual) instrumentation and the OpenTelemetry Tracing API.

Links and references

* OpenTelemetry Documentation: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Tracing specification: [https://opentelemetry.io/docs/specs/otel/trace/](https://opentelemetry.io/docs/specs/otel/trace/)
* OTLP Protocol: [https://github.com/open-telemetry/opentelemetry-proto](https://github.com/open-telemetry/opentelemetry-proto)
* Collector: [https://opentelemetry.io/docs/collector/intro/](https://opentelemetry.io/docs/collector/intro/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/254a6366-034f-4488-96f6-6fc45a2a0c93" />
</CardGroup>


# Demo Connecting Two Services

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Connecting-Two-Services/page

Guide to instrumenting two services with OpenTelemetry to propagate trace context across HTTP calls so client and server spans form a single correlated distributed trace

This guide shows how to connect two services so that an outgoing HTTP call from the Payment service to the Charge service is represented as a single correlated distributed trace. The objective: when the payment service executes its `charge_bank` step, it should call the charge service (`/charge`) and produce spans that are correlated across both services so a tracing backend like [Jaeger](https://www.jaegertracing.io/) can display one end-to-end trace.

What you'll learn

* How to configure a tracer provider for each service.
* How to instrument a Flask-based charge service (server).
* How to instrument the payment service (client) and inject trace context into HTTP headers.
* How to create client-side spans for outgoing requests.
* How to debug cases where two separate traces appear instead of a single correlated trace.

Quick overview

* Both services must establish a tracer provider (resource attributes: `service.name`, `service.version`) and a span processor + exporter.
* For local debugging use `ConsoleSpanExporter`; for production collection use the OTLP exporter to a collector or backend.
* Propagate context with `opentelemetry.propagate.inject` on the client and extract it on the server (or rely on automatic instrumentation).

Configure tracing (shared pattern)

Each service reuses a common tracer configuration module. This ensures consistent resource attributes and exporter configuration across services.

tracing\_config.py

```python theme={null}
