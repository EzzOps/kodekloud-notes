# payment.py
from opentelemetry import trace
from opentelemetry.trace import Tracer

tracer: Tracer = trace.get_tracer(__name__, "0.1.0")

def process_payment():
    span = trace.get_current_span()
    span.set_attribute("user", "john")
    span.set_attribute("account_number", "7372349")
    span.set_attribute("bank", "BankOfAmerica")

    print("processing payment")
    validate_card()
    charge_bank()

@tracer.start_as_current_span("Validating Card")
def validate_card():
    print("validating card")

@tracer.start_as_current_span("Charge Bank")
def charge_bank():
    print("charging bank")

if __name__ == "__main__":
    with tracer.start_as_current_span("Payment Service"):
        process_payment()
```

Key points:

* `trace.get_tracer(...)` creates a tracer instance used to start spans.
* `trace.get_current_span()` accesses the active span to set attributes (user, account number, bank).
* Helper functions use the tracer decorator to create child spans for validation and charging.

Uninstrumented Flask charge service (initial state)
The external service that performs the charge is a minimal Flask app. Below is the uninstrumented version:

```python theme={null}
# charge.py (uninstrumented)
from flask import Flask

app = Flask(__name__)

@app.route("/charge")
def charge():
    return "Charging Users Bank Account"

if __name__ == "__main__":
    app.run(debug=True)
```

Quick local verification
Run the uninstrumented service and verify the endpoint responds:

```bash theme={null}
# Activate your virtualenv if needed, then:
python charge.py

# In a new terminal:
curl 127.0.0.1:5000/charge
# Expected output:
# Charging Users Bank Account
```

Instrumenting the Flask API with OpenTelemetry
To export traces from the Flask API, we will:

* Configure a TracerProvider and set resource attributes (`service.name`, `service.version`).
* Attach a span processor (BatchSpanProcessor) and an OTLP exporter pointing at an OTLP HTTP endpoint (`http://localhost:4318/v1/traces` in this example).
* Start a server span for incoming requests and enrich it with HTTP attributes: `http.method`, `net.peer.ip`, and `http.path`.

Below is a cohesive, instrumented `charge.py`:

```python theme={null}
# charge.py (instrumented)
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def configure_tracer():
    # Export spans to an OTLP endpoint (e.g., Collector running on localhost)
    exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")

    span_processor = BatchSpanProcessor(exporter)

    resource = Resource.create({
        "service.name": "charge-service",
        "service.version": "0.5.0"
    })

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer("charge.py", "0.5.0")

tracer = configure_tracer()
app = Flask(__name__)

@app.route("/charge")
@tracer.start_as_current_span("Charge Account", kind=SpanKind.SERVER)
def charge():
    # Enrich the current span with HTTP-related attributes
    span = trace.get_current_span()
    span.set_attribute("http.method", request.method)
    span.set_attribute("net.peer.ip", request.remote_addr)
    span.set_attribute("http.path", request.path)
    return "Charging Users Bank Account"

if __name__ == "__main__":
    app.run(debug=True)
```

Notes:

* `OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")` sends traces over HTTP to an OTLP-compatible collector or backend.
* `BatchSpanProcessor` is recommended in production to improve performance.
* Setting `Resource` attributes like `service.name` and `service.version` improves trace filtering and service identification in a backend.

> **lightbulb** Make sure an [OTLP-compatible collector](https://opentelemetry.io/docs/collector/) (or backend) is reachable at the OTLP endpoint you configured (here, `http://localhost:4318/v1/traces`). If you want console output only for quick testing, you can swap `OTLPSpanExporter` for `ConsoleSpanExporter`.

Start the instrumented service and test

```bash theme={null}
# Activate your virtualenv if needed, then:
python charge.py

# In another terminal:
curl 127.0.0.1:5000/charge
# Output:
# Charging Users Bank Account
```

If you have a tracing backend (Jaeger, Tempo, or an OpenTelemetry Collector forwarding to a backend), refresh the tracing UI and look for the `charge-service` traces. The server spans should contain the attributes we set: `http.method`, `net.peer.ip`, and `http.path`.

Best practices and tips

* Use consistent `service.name` and versioning across your services for easier filtering.
* Prefer `BatchSpanProcessor` in production and `ConsoleSpanExporter` while developing locally.
* Enrich spans with HTTP and network attributes (method, path, client IP) so you can search and correlate traces easily.
* Reuse the tracer provider and exporter configuration pattern across services; only change `service.name` and `service.version`.

Common attributes to set on spans

| Attribute         | Purpose                              | Example          |
| ----------------- | ------------------------------------ | ---------------- |
| `service.name`    | Identify the service producing spans | `charge-service` |
| `service.version` | Version of the service               | `0.5.0`          |
| `http.method`     | HTTP verb of the request             | `GET`            |
| `http.path`       | Path requested                       | `/charge`        |
| `net.peer.ip`     | Client IP address                    | `127.0.0.1`      |
| `user`            | Application-level user id            | `john`           |
| `account_number`  | Application-level account identifier | `7372349`        |

Summary

* The client (`payment.py`) demonstrates creating spans and adding attributes to describe a payment workflow.
* The Flask service (`charge.py`) is instrumented to create server spans and enrich them with HTTP attributes for better observability.
* You can reuse the tracer provider, exporter, span processor, and resource configuration across services—only update `service.name` and `service.version`.

Links and References

* [OpenTelemetry](https://opentelemetry.io/)
* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
* [OTLP protocol](https://opentelemetry.io/docs/specs/otel/protocol/otlp/)
* [Flask](https://flask.palletsprojects.com/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [Grafana Tempo](https://grafana.com/oss/tempo/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/6937673a-33fe-4a40-aa41-a889659c3b64)


# Demo Instrumenting Application Configuring OpenTelemetry

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Instrumenting-Application-Configuring-OpenTelemetry/page

Guide to instrumenting a simple Python payment app with OpenTelemetry tracing, creating nested spans, printing to console, and configuring exporters for backend telemetry

In this lesson we'll instrument a small Python application using OpenTelemetry tracing. The demo app is intentionally tiny so tracing concepts are clear — the same ideas apply to other languages (JavaScript, Java, C#, etc.). By the end you'll have a working example that prints spans locally and a clear path to send telemetry to a backend.

What you'll learn

* How to add OpenTelemetry packages to a Python project
* How to configure a TracerProvider and ConsoleSpanExporter
* How to create spans that represent operations and nested child operations
* Where to go next to export traces to a backend (OTLP, Jaeger, Zipkin)

Prerequisites

* Python 3.7+
* pip

Demo application (simple payment flow)

```python theme={null}
def process_payment():
    print("processing payment")
    validate_card()
    charge_bank()

def validate_card():
    print("validating card")

def charge_bank():
    print("charging bank")

if __name__ == "__main__":
    process_payment()
```

This tiny application represents a dummy payment service:

* `process_payment()` starts the flow.
* `validate_card()` simulates credit-card validation.
* `charge_bank()` simulates charging the user's bank.

We will instrument these functions so running the program generates trace spans for each step.

Installing OpenTelemetry packages
Install the core API and SDK packages:

```bash theme={null}
pip install opentelemetry-api opentelemetry-sdk
```

Example of packages installed (condensed):

```plaintext theme={null}
Successfully installed opentelemetry-api-1.36.0 opentelemetry-sdk-1.36.0 opentelemetry-semantic-conventions-0.57b0 typing-extensions-4.15.0 importlib-metadata-8.7.0 zipp-3.23.0
```

> **lightbulb** OpenTelemetry is split into API and SDK: the API provides the interfaces you call from application code, while the SDK provides concrete implementations (exporters, processors, and providers) that produce and export telemetry.

Configuring tracing in Python
Below is a small helper that configures a tracer provider, a span processor, and a `ConsoleSpanExporter`. The `ConsoleSpanExporter` prints spans to stdout — this is useful for local development and debugging.

```python theme={null}
