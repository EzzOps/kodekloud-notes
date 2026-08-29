# payment.py
import requests
from opentelemetry.propagate import inject
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
# Optional OTLP exporter:
def configure_tracer():
    resource = Resource.create({
        "service.name": "payment service",
        "service.version": "0.2.0",
    })
    provider = TracerProvider(resource=resource)

    exporter = ConsoleSpanExporter()
    # exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

tracer = configure_tracer()

@tracer.start_as_current_span("Charge Bank")
def charge_bank():
    print("charging bank")

    # Create a client span for the outgoing HTTP request
    with tracer.start_as_current_span("Request to Charge API", kind=trace.SpanKind.CLIENT) as span:
        url = "http://127.0.0.1:5000/charge"
        # Set useful attributes for the request span
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", url)

        # Inject current context into headers
        headers = {}
        inject(headers)

        # Make the HTTP request with the propagated headers
        resp = requests.get(url, headers=headers)
        span.set_attribute("http.status_code", resp.status_code)

if __name__ == "__main__":
    charge_bank()
```

Key points

* `inject(headers)` mutates your headers dictionary to include propagation fields (traceparent, tracestate, etc.).
* Use `headers=headers` when calling `requests.get()` so the downstream service receives the context.

## Charge service (server) — extract and attach context from incoming headers

Goals

* Configure tracer provider and exporter for the charge service.
* Extract the incoming context from request headers and attach it so the propagated trace becomes active for the request handler.
* Save the returned token to `request.environ` and detach it in `teardown_request` to restore the previous context.

Important functions: `opentelemetry.propagate.extract`, `opentelemetry.context.attach`, and `opentelemetry.context.detach`.

Example charge service:

```python theme={null}
# charge.py
from flask import Flask, request
from opentelemetry.propagate import extract
from opentelemetry import trace
from opentelemetry.context import attach, detach
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
# Optional OTLP exporter:
def configure_tracer():
    resource = Resource.create({
        "service.name": "charge service",
        "service.version": "0.5.0",
    })
    provider = TracerProvider(resource=resource)

    exporter = ConsoleSpanExporter()
    # exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    span_processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

tracer = configure_tracer()
app = Flask(__name__)

@app.before_request
def before_request_func():
    # Extract the context from incoming request headers and make it active
    token = attach(extract(request.headers))
    # Save the token so we can detach in teardown
    request.environ["context_token"] = token

@app.teardown_request
def teardown_request_func(exc):
    # Detach previously attached context token to restore previous context
    token = request.environ.get("context_token", None)
    if token:
        detach(token)

@app.route("/charge")
@tracer.start_as_current_span("Charge Account", kind=trace.SpanKind.SERVER)
def charge():
    span = trace.get_current_span()
    span.set_attribute("http.method", request.method)
    span.set_attribute("client.ip", request.remote_addr)
    span.set_attribute("http.path", request.path)
    return "Charging Users Bank Account"

if __name__ == "__main__":
    app.run(debug=True)
```

<Callout icon="warning">
  Flask passes an exception argument to `teardown_request`. The teardown function must accept that parameter (for example `def teardown_request_func(exc):`) even if you don't use it, otherwise Flask will raise an error.
</Callout>

## Run and verify

1. Start the charge service (server): `python charge.py`
2. Start the payment service (client) and trigger the request: `python payment.py`
3. Observe the console output or your tracing backend. With the Console exporter you will see both client and server spans logged; with OTLP -> Jaeger you will see a single distributed trace containing both services.

Expected behavior

* Both client and server spans should share the same `trace_id`.
* The server span's `parent_id` should match the client span's `span_id`, indicating correct parent/child relationships.

Example of a client span (trimmed):

```json theme={null}
{
  "name": "Request to Charge API",
  "context": {
    "trace_id": "0x026ef7be217ce0d83fe16a255578eb4",
    "span_id": "0xafb59c6fb586f176",
    "trace_state": "[]"
  },
  "kind": "SpanKind.CLIENT",
  "attributes": {
    "http.method": "GET",
    "http.url": "http://127.0.0.1:5000/charge",
    "http.status_code": 200
  }
}
```

Corresponding server span (trimmed):

```json theme={null}
{
  "name": "Charge Account",
  "context": {
    "trace_id": "0x026ef7be217ce0d83fe16a255578eb4",
    "span_id": "0xbfdc2355760919cb",
    "trace_state": "[]"
  },
  "kind": "SpanKind.SERVER",
  "parent_id": "0xafb59c6fb586f176",
  "attributes": {
    "http.method": "GET",
    "client.ip": "127.0.0.1",
    "http.path": "/charge"
  }
}
```

Notice:

* Shared `trace_id` confirms both spans belong to the same distributed trace.
* `parent_id` on the server span matches the client span's `span_id`, confirming the correct parent-child relationship.

If you use OTLP -> Jaeger or another backend, you should see a single trace containing both services (payment and charge). Example screenshot of Jaeger UI showing both services inside the same trace:

<Frame>
  <img alt="The image shows a Jaeger UI interface displaying a trace for a &#x22;payment service,&#x22; detailing operations like &#x22;Starting Payment&#x22; and &#x22;Charge Account,&#x22; along with timing information for each step." />
</Frame>

With these propagation changes the two services are connected in the same trace, enabling end-to-end visibility across the request path.

Links and references

* [OpenTelemetry](https://opentelemetry.io/)
* [OpenTelemetry Python API docs](https://opentelemetry-python.readthedocs.io/en/latest/)
* [Flask documentation](https://flask.palletsprojects.com/)
* [Jaeger project](https://www.jaegertracing.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/e3b8486b-732b-461f-ac44-c1596dc10ee0" />
</CardGroup>


# Demo Resource Attributes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Resource-Attributes/page

How to set OpenTelemetry resource attributes so traces include service metadata and appear correctly in Jaeger for better filtering and identification

In this lesson we address a common issue: traces showing up in Jaeger as `unknown_service`, which makes it difficult to identify which application produced them. The fix is to configure resource attributes. Resource attributes are an immutable set of key/value pairs that describe the entity producing telemetry (for example, service name, service version, host, and environment). When set correctly, observability backends such as Jaeger and Tempo can surface and filter traces by these attributes.

Dependencies used in this demo:

```text theme={null}
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

Example run before configuring resource attributes:

```bash theme={null}
python payment.py
processing payment
validating card
charging bank
```

What to change

* Import `Resource` from `opentelemetry.sdk.resources`.
* Create a `Resource` instance with semantic keys such as `service.name` and `service.version`.
* Pass the `Resource` to the `TracerProvider` so spans inherit the resource metadata.

Compact, corrected tracer configuration and example payment function:

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def configure_tracer():
    exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    span_processor = BatchSpanProcessor(exporter)

    # Create a Resource that identifies this service
    resource = Resource.create({
        "service.name": "payment-service",
        "service.version": "0.2.0"
    })

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)

    # Return an instrumented tracer for the application code
    return trace.get_tracer("payment.py", "0.1.0")

tracer = configure_tracer()

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    print("processing payment")
    print("validating card")
    print("charging bank")

if __name__ == "__main__":
    process_payment()
```

Quick checklist

* Use standard semantic keys (for example, `service.name`, `service.version`) so observability backends can detect and display them.
* Prefer attributes that describe the resource (the entity producing telemetry), not attributes that belong on individual spans.
* Add other resource attributes as needed (for example: `host.name`, `host.ip`, `deployment.environment`) to support searching and filtering.

Common resource attribute examples

|                   Attribute | Description                                       | Example                                                                              |
| --------------------------: | ------------------------------------------------- | ------------------------------------------------------------------------------------ |
|              `service.name` | Canonical name of the service producing telemetry | `payment-service`                                                                    |
|           `service.version` | Version of the service                            | `0.2.0`                                                                              |
|    `deployment.environment` | Deployment environment (prod, staging, dev)       | `production`                                                                         |
|                 `host.name` | Hostname of the machine/container                 | `web-01`                                                                             |
|                   `host.ip` | IP address of the host                            | `10.0.0.5`                                                                           |
| `resource` creation example | How to create a Resource in code                  | `Resource.create({ "service.name": "payment-service", "service.version": "0.2.0" })` |

Before configuring resource attributes, traces appeared as `unknown_service` in Jaeger (screenshot below). After adding the Resource to the tracer and rerunning the script, the CLI output remains the same but spans include the resource attributes (service name, service.version), and Jaeger now lists the correct service.

```bash theme={null}
python payment.py
processing payment
validating card
charging bank
```

<Frame>
  <img alt="The image shows a screenshot of the Jaeger UI, displaying a search interface for tracing services with search results highlighting a trace for &#x22;unknown_service&#x22; related to a Payment Service." />
</Frame>

Now the Jaeger UI shows the correct service name (`payment-service`) in the service list, making it much easier to find and analyze relevant traces.

<Callout icon="lightbulb">
  Resource attributes are intended to describe the entity producing telemetry and are treated as immutable metadata for that entity. Use standard keys (for example, `service.name`, `service.version`) to maximize interoperability with observability backends.
</Callout>

<Frame>
  <img alt="The image shows a Jaeger UI trace analysis for a &#x22;Payment Service,&#x22; detailing spans related to a payment process with specific tags and process information." />
</Frame>

Inspecting individual traces in Jaeger will show the attached resource attributes (service name and version), along with automatically added SDK attributes such as the OpenTelemetry SDK language and version. These attributes make traces far easier to filter, group, and interpret.

Links and references

* [OpenTelemetry — Resources](https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [OpenTelemetry Python SDK](https://opentelemetry.io/docs/instrumentation/python/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/bb2393a3-03e3-4528-90cb-f3073471ba57" />
</CardGroup>
