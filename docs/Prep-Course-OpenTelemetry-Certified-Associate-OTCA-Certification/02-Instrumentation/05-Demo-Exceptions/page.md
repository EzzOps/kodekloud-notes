# tracer_setup.py
from typing import Dict, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

def configure_tracer() -> trace.Tracer:
    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",  # adjust if needed
        headers=None,
        timeout=10.0,
    )

    provider = TracerProvider(
        resource=Resource.create({"service.name": "payment-service"})
    )
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer("payment.py", "0.1.0")
```

Run your application and ensure the exporter endpoint is reachable. The tracer configuration above uses a BatchSpanProcessor for efficient export.

Expected local console output (example when running the client application — separate from the tracer export):

```plaintext theme={null}
Documents/courses/Instrumentation-demo via 🐍 v3.13.7 (venv) on 💻 (us-east-1)
> python payment.py
processing payment
validating card
charging bank
```

## Payment client: add attributes, events, and inject context

This client example demonstrates:

* creating a span for the payment flow,
* adding attributes to make spans searchable,
* adding timestamped events before and after an HTTP call,
* injecting trace context into outgoing request headers so downstream services can correlate traces.

```python theme={null}
# payment.py
import requests
from opentelemetry import trace
from opentelemetry.propagate import inject

from tracer_setup import configure_tracer

tracer = configure_tracer()

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    span = trace.get_current_span()

    # Set attributes on the span (avoid sensitive fields in production)
    span.set_attributes({
        "user": "john",
        "bank": "BankOfAmerica"
    })
    print("processing payment")
    print("validating card")

    url = "http://127.0.0.1:5000/charge"
    # Add an event before sending the request
    span.add_event("Sending request", {"http.method": "GET", "http.url": url})

    # Inject trace context into outgoing headers
    headers = {}
    inject(headers)

    resp = requests.get(url, headers=headers)

    # Record response status as an attribute and as an event
    span.set_attribute("http.status_code", resp.status_code)
    span.add_event("Request sent", {"http.status_code": resp.status_code, "http.url": url})

    print("charging bank")

if __name__ == "__main__":
    process_payment()
```

Run the client:

```bash theme={null}
python payment.py
```

When you inspect this trace in a tracing UI (for example [Jaeger](https://www.jaegertracing.io/), [Tempo](https://grafana.com/oss/tempo/), or any OTLP-compatible backend), open the span for "Starting Payment". You should see the two timestamped events:

* "Sending request" (includes `http.method` and `http.url`)
* "Request sent" (includes `http.status_code` and `http.url`)

These events appear in the span timeline and help you understand the sequence of actions around the outgoing request.

## Server-side (Flask) example: record an error event on the server span

On the server side you want to annotate the server span with request metadata and record events for application-level conditions such as errors, retries, or business rule violations.

```python theme={null}
# cart_service.py
from flask import Flask, request
from opentelemetry import trace

from tracer_setup import configure_tracer

app = Flask(__name__)
tracer = configure_tracer()

@app.route('/charge')
@tracer.start_as_current_span("Charge Account", kind=trace.SpanKind.SERVER)
def charge():
    span = trace.get_current_span()
    # Annotate the server span with request metadata
    span.set_attributes({
        "http.method": request.method,
        "client.ip": request.remote_addr,
        "http.path": request.path
    })

    # Example error event — attach a message and optional attributes
    span.add_event("User has insufficient funds", {"available_balance": 5})

    return "Charging Users Bank Account"
    
if __name__ == "__main__":
    app.run(debug=True)
```

Run the Flask server, then execute the client. In the server span details you will see the "User has insufficient funds" event with the `available_balance` attribute. This makes it easier to correlate failures with the originating trace.

Expected combined console output (client + server example):

```plaintext theme={null}
Documents/courses/Instrumentation-demo via 🐍 v3.13.7 (venv) on ☁️ (us-east-1)
> python payment.py
processing payment
validating card
charging bank
```

## Quick reference: span attributes vs events

Use attributes to add searchable, indexed metadata to a span. Use events to attach timestamped, ordered observations within the span.

| Use                     | API                                     | Example                                                    |
| ----------------------- | --------------------------------------- | ---------------------------------------------------------- |
| Add a single attribute  | `span.set_attribute(key, value)`        | `span.set_attribute("http.status_code", resp.status_code)` |
| Add multiple attributes | `span.set_attributes(dict)`             | `span.set_attributes({ "user": "john", "bank": "BOA" })`   |
| Add a timestamped event | `span.add_event(name, attributes=None)` | `span.add_event("Sending request", {"http.url": url})`     |

Note: In the table above any curly-brace examples are shown as code to avoid parsing as JS/MDX objects.

## Best practices

* Add events for meaningful, timestamped occurrences (request sent/received, error, retry).
* Use attributes for metadata you want to filter or search on (user ID, status code, service name).
* Inject trace context into outgoing HTTP requests so downstream services can join traces.
* Avoid recording sensitive or excessive data in attributes/events. Use truncated values, hashes, or identifiers where needed.

> **lightbulb** When instrumenting production systems, prefer structured keys for attributes and events (for example `error.type`, `http.method`, `http.status_code`) to make querying and visualization easier in your tracing backend.

## Links and references

* [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [Grafana Tempo](https://grafana.com/oss/tempo/)
* [OTLP HTTP Exporter docs](https://opentelemetry.io/docs/specs/exporter/otlp/)

## Summary

* Use `span.set_attribute` / `span.set_attributes` to store searchable metadata on spans.
* Use `span.add_event(name, attributes=None)` to record timestamped events inside a span (useful for "request sent/received", errors, retries).
* Inject context for outgoing HTTP calls so downstream services can correlate traces.
* Avoid storing sensitive or excessive data in span attributes and events.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/fe1000df-3f75-44d0-a7df-f3308e550a4b)


# Demo Exceptions

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Exceptions/page

Demonstrates recording exceptions in OpenTelemetry traces, showing add_event, record_exception, and best practices for capturing error metadata and annotating spans

In this lesson we'll show how to record exceptions in your OpenTelemetry traces. Exceptions occur when something unexpected fails — for example, a request to an external Charge API might fail because the remote service is down or the network is unavailable. Attaching exception details to spans helps you answer: what failed, when did it fail, and where in the trace timeline the failure occurred.

Below are three progressively richer examples that demonstrate:

* creating a client span for an outgoing HTTP request,
* annotating spans with events and attributes,
* recording exceptions explicitly, and
* using the built-in helper to capture exception type, message, and stack trace.

First, a simple, clean example that creates a client span and annotates it with events and attributes:

```python theme={null}
