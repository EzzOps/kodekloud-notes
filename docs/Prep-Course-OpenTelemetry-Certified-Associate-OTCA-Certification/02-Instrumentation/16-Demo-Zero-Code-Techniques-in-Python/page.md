# configure_tracer.py
import requests
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.propagate import inject
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

def configure_tracer():
    resource = Resource.create({
        "service.name": "payment-service",
        "service.version": "0.2.0"
    })
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__, "0.1.0")
```

* Then use the tracer when making HTTP calls, set attributes, record events, and set status:

```python theme={null}
# payment.py
import requests
from opentelemetry.propagate import inject
from opentelemetry.trace import Status, StatusCode
from configure_tracer import configure_tracer

tracer = configure_tracer()

def call_charge_api():
    url = "http://127.0.0.1:5002/charge"

    with tracer.start_as_current_span("Request to Charge API") as span:
        # Use semantic attribute names
        span.set_attributes({
            "http.method": "GET",
            "http.url": url
        })

        headers = {}
        inject(headers)  # propagate context
        span.add_event("Sending Request")

        try:
            resp = requests.get(url, headers=headers)
            span.add_event("Request sent", {"url": url})
            # record HTTP status code as an attribute
            span.set_attribute("http.status_code", resp.status_code)

            # Set span status explicitly based on response
            # Treat 2xx responses as success, others as errors (adjust as needed)
            if 200 <= resp.status_code < 300:
                span.set_status(Status(StatusCode.OK))
            else:
                span.set_status(Status(StatusCode.ERROR))

            return resp

        except requests.RequestException as exc:
            # Network/connection failures should set status to ERROR
            span.record_exception(exc)
            span.set_status(Status(StatusCode.ERROR))
            raise
```

Mapping HTTP responses to span status (recommended defaults)

| HTTP result       | Example codes | Recommended span status   | Why                                                                  |
| ----------------- | ------------- | ------------------------- | -------------------------------------------------------------------- |
| Success           | `200–299`     | `OK`                      | Successful response; mark span successful.                           |
| Client error      | `400–499`     | `ERROR` (or custom logic) | Most client errors are failures; you may treat some codes specially. |
| Server error      | `500–599`     | `ERROR`                   | Server-side failures indicate error conditions.                      |
| Network/exception | N/A           | `ERROR`                   | Exceptions and timeouts should mark the span `ERROR`.                |

<Callout icon="warning">
  Do not rely solely on span status for debugging. Always record attributes like `http.status_code`, add meaningful events, and call `span.record_exception()` when catching exceptions to preserve stack/exception details.
</Callout>

Notes and best practices

* Import and use `Status` and `StatusCode` from `opentelemetry.trace` and call `span.set_status(Status(StatusCode.OK))` or `span.set_status(Status(StatusCode.ERROR))`.
* Recording `http.status_code` as an attribute helps trace UIs and analysis tools provide richer context and filters.
* Define your application's notion of "success"—for example, some APIs return 404 or 409 in normal flows; you may decide to mark those as `OK` in specific contexts.
* Always propagate context (`inject`) for distributed traces so downstream services are linked.

After implementing the above and running the application with a successful request, the trace timeline will show the "Request to Charge API" span marked as `OK`. The Jaeger UI for that trace is shown below (image preserved from original content):

<Frame>
  <img alt="The image shows a Jaeger UI displaying a trace timeline for a payment service. It details various spans, including HTTP method and status code for the &#x22;Request to Charge API.&#x22;" />
</Frame>

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Jaeger Tracing: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* OpenTelemetry semantic conventions (HTTP): [https://opentelemetry.io/docs/reference/specification/trace/semantic\_conventions/http/](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/http/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/b38469f5-8819-4aea-8538-63233d729256" />
</CardGroup>


# Demo Zero Code Techniques in Python

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Zero-Code-Techniques-in-Python/page

Demonstrates zero-code OpenTelemetry auto-instrumentation for Python Flask applications using opentelemetry-distro, bootstrap and opentelemetry-instrument to capture traces, metrics and database and HTTP spans

This article demonstrates zero-code (auto) instrumentation for Python applications using OpenTelemetry. We'll:

* Start with a minimal Flask app that has no OpenTelemetry packages.
* Install the OpenTelemetry distro and OTLP exporter.
* Use the auto-instrumentation tooling to capture traces and metrics without modifying application code.
* Show a slightly more complex example that exercises HTTP and database instrumentation.

Relevant links:

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Flask: [https://palletsprojects.com/p/flask/](https://palletsprojects.com/p/flask/)
* OTLP spec: [https://opentelemetry.io/docs/reference/specification/protocol/otlp/](https://opentelemetry.io/docs/reference/specification/protocol/otlp/)

## 1. Minimal Flask app (products.py)

This tiny Flask application is the whole codebase used for the initial demo.

```python theme={null}
