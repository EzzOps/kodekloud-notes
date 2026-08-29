# payment.py
import requests
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.propagate import inject

tracer = trace.get_tracer(__name__)

def charge_bank():
    print("charging bank")
    with tracer.start_as_current_span("Request to Charge API", kind=SpanKind.CLIENT) as span:
        url = "http://127.0.0.1:5000/charge"
        span.set_attributes({
            "http.method": "GET",
            "http.url": url,
        })

        headers = {}
        inject(headers)

        span.add_event("Sending Request")
        resp = requests.get(url, headers=headers)
        span.add_event("Request sent", {"url": url})
        span.set_attribute("http.status_code", resp.status_code)


if __name__ == "__main__":
    with tracer.start_as_current_span("Payment Service"):
        charge_bank()
```

If the remote service is unreachable (for example, if you mistakenly target port 5002 where nothing is listening) the `requests.get` call will raise an exception. You can catch that exception and add it to the span as a plain event:

```python theme={null}
# payment.py (with explicit try/except)
import requests
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.propagate import inject

tracer = trace.get_tracer(__name__)

def charge_bank():
    print("charging bank")
    with tracer.start_as_current_span("Request to Charge API", kind=SpanKind.CLIENT) as span:
        try:
            url = "http://127.0.0.1:5002/charge"  # intentionally incorrect port to force failure
            span.set_attributes({
                "http.method": "GET",
                "http.url": url,
            })

            headers = {}
            inject(headers)

            span.add_event("Sending Request")
            resp = requests.get(url, headers=headers)
            span.add_event("Request sent", {"url": url})
            span.set_attribute("http.status_code", resp.status_code)

        except Exception as err:
            # Record the exception as an event (string form)
            span.add_event("exception", attributes={"error": str(err)})


if __name__ == "__main__":
    with tracer.start_as_current_span("Payment Service"):
        charge_bank()
```

This approach attaches an "exception" event to the span and includes the error message as an attribute. A better approach is to use the span API's built-in helper so the instrumentation captures richer exception metadata (type, message, and stack trace):

```python theme={null}
# payment.py (use record_exception)
import requests
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.propagate import inject

tracer = trace.get_tracer(__name__)

def charge_bank():
    print("charging bank")
    with tracer.start_as_current_span("Request to Charge API", kind=SpanKind.CLIENT) as span:
        try:
            url = "http://127.0.0.1:5002/charge"  # intentionally incorrect port to force failure
            span.set_attributes({
                "http.method": "GET",
                "http.url": url,
            })

            headers = {}
            inject(headers)

            span.add_event("Sending Request")
            resp = requests.get(url, headers=headers)
            span.add_event("Request sent", {"url": url})
            span.set_attribute("http.status_code", resp.status_code)

        except Exception as err:
            # record_exception captures type, message and stack trace
            span.record_exception(err)
            # Optionally set the span status to error (if desired)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(err)))


if __name__ == "__main__":
    with tracer.start_as_current_span("Payment Service"):
        charge_bank()
```

> **lightbulb** Using `span.record_exception(err)` will include the exception type, message, and stack trace in the span. You can also set the span status to error with `span.set_status(...)` to make the error state explicit.

Best practices and behavior

* Prefer `span.record_exception(err)` when you want structured exception data (type, message, stack trace) in the span.
* Use `span.set_status(trace.Status(trace.StatusCode.ERROR, "..."))` if you want the span to be explicitly marked as an error in UI/analytics.
* You do not always need an explicit try/except: if an exception propagates out of a span and your instrumentation/exporter is configured to capture uncaught exceptions, the tracing system may automatically record the exception on that span.
* For richer context, include relevant attributes (HTTP method, URL, status code, and other request metadata) so backends can correlate exceptions with request details.

Comparison: event vs record\_exception vs automatic capture

| Approach                                        | Captures                                                              | Use when                                                                        |
| ----------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `span.add_event("exception", attributes={...})` | Arbitrary attributes you add (e.g. `{"error": "Connection refused"}`) | You want custom, lightweight event data.                                        |
| `span.record_exception(err)`                    | Exception type, message, stack trace                                  | You want structured exception data for debugging and stack traces.              |
| Automatic capture by instrumentation            | Depends on instrumentation/exporter configuration                     | You rely on automatic capture for uncaught exceptions and minimal code changes. |

When recorded, tracing backends such as [Jaeger](https://www.jaegertracing.io/) will display the exception event and stack trace in the trace timeline, making it easy to correlate a failure with the specific span and service.

References

* OpenTelemetry Python API: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* Jaeger tracing: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)

<Frame>
  <img alt="The image shows a Jaeger UI interface displaying the trace timeline of a payment service with multiple spans and logs, including a request to a charge API." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/dbdf3b73-09ff-4daf-b818-93f3ab397891)


# Demo Exporters

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Exporters/page

Guide to replacing ConsoleSpanExporter with an OTLP HTTP exporter to send OpenTelemetry traces to Jaeger, including configuration, installation, and verification steps.

In this lesson we'll replace the ConsoleSpanExporter (which prints spans to stdout) with an exporter that sends traces to a tracing backend. Printing spans to the console is useful for local debugging, but production systems typically send traces to a backend such as Jaeger or a hosted OTLP-compatible service.

Why this matters:

* ConsoleSpanExporter: good for quick debugging and tests.
* OTLP exporter: sends traces to real backends for storage, visualization, and correlation across services.

## Current tracer configuration (ConsoleSpanExporter)

Example: a minimal tracer setup that prints spans to the console:

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)  # trace.get_tracer(...)
```

A typical ConsoleSpanExporter output for a span might look like this JSON representation:

```json theme={null}
{
  "span_id": "0x3bad5c03252174ba",
  "trace_state": "{}",
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-09-01T01:10:06.523273Z",
  "end_time": "2025-09-01T01:10:06.523365Z",
  "status": {}
}
```

## Exporting to Jaeger via OTLP

Rather than printing spans locally, we’ll send them to Jaeger. Jaeger accepts traces via the OpenTelemetry Protocol (OTLP), so we can use the OTLP HTTP exporter provided by OpenTelemetry instead of a Jaeger‑specific exporter. This keeps your instrumentation portable to any OTLP-compatible backend.

> **lightbulb** Jaeger supports OTLP (HTTP and gRPC). Using the OTLP exporter keeps your instrumentation portable to any backend that accepts OTLP, not just Jaeger.

Install the OTLP HTTP exporter package:

```bash theme={null}
pip install opentelemetry-exporter-otlp-proto-http
```

Verify installation (example output; versions may differ):

```plaintext theme={null}
importlib_metadata==8.7.0
opentelemetry-api==1.36.0
opentelemetry-exporter-otlp-proto-common==1.36.0
opentelemetry-exporter-otlp-proto-http==1.36.0
opentelemetry-proto==1.36.0
opentelemetry-sdk==1.36.0
opentelemetry-semantic-conventions==0.57b0
protobuf==6.32.0
requests==2.32.5
typing_extensions==4.15.0
urllib3==2.5.0
zipp==3.23.0
```

### Update tracer configuration to use OTLPSpanExporter

When sending to a local Jaeger instance, the OTLP HTTP endpoint is typically `http://localhost:4318/v1/traces`. Update your tracer configuration to use the OTLP HTTP exporter:

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def configure_tracer():
    exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    span_processor = BatchSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)  # trace.get_tracer(...)
```

Notes:

* Use `BatchSpanProcessor` in production; it buffers spans and sends them efficiently. `SimpleSpanProcessor` sends synchronously and can hurt performance.
* OTLP over HTTP commonly uses port `4318` and the `/v1/traces` path. If using OTLP/gRPC or a hosted service, verify the endpoint and protocol in the backend docs.

> **warning** Make sure the endpoint, protocol (HTTP vs gRPC), and any required authentication match your Jaeger or hosted OTLP service. Sending to the wrong endpoint or protocol will result in dropped traces.

## Quick comparison

| Exporter                | Use case                                             | Example configuration                                          |
| ----------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| ConsoleSpanExporter     | Local debugging and development                      | `ConsoleSpanExporter()`                                        |
| OTLPSpanExporter (HTTP) | Send traces to Jaeger or any OTLP-compatible backend | `OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")` |

## Run your instrumented application

Save the updated configuration and run your application. The application’s runtime output (print statements) will remain the same, but span data will be exported to Jaeger:

```bash theme={null}
python payment.py
