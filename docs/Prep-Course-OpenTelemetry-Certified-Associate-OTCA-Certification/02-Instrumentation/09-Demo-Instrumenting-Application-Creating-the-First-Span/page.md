# payment.py (tracing configuration)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def configure_tracer():
    # Export spans to the console (useful for local testing)
    exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(exporter)

    # TracerProvider is the root object that manages tracers and span processors
    provider = TracerProvider()
    provider.add_span_processor(span_processor)

    # Make this provider the global default so trace.get_tracer() works across modules
    trace.set_tracer_provider(provider)

    # Return a named tracer for this service (name and optional version)
    return trace.get_tracer("payment", "0.1.0")
```

Instrumenting the application to generate spans
Use the tracer returned by `configure_tracer()` to create spans. The recommended pattern is to use the context manager `start_as_current_span` so spans are properly nested and automatically ended.

Complete instrumented example:

```python theme={null}
# payment.py (complete)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer("payment", "0.1.0")

def process_payment(tracer):
    # Create a root span for the payment processing flow
    with tracer.start_as_current_span("process_payment"):
        print("processing payment")
        validate_card(tracer)
        charge_bank(tracer)

def validate_card(tracer):
    # Child span for card validation
    with tracer.start_as_current_span("validate_card"):
        print("validating card")

def charge_bank(tracer):
    # Child span for charging the bank
    with tracer.start_as_current_span("charge_bank"):
        print("charging bank")

if __name__ == "__main__":
    tracer = configure_tracer()
    process_payment(tracer)
```

Running the instrumented application

```bash theme={null}
$ python payment.py
processing payment
validating card
charging bank
```

Because we used `ConsoleSpanExporter`, you will also see formatted span output printed to the console. A simplified example of what `ConsoleSpanExporter` might print (exact formatting may vary by OpenTelemetry version):

```plaintext theme={null}
Span(name="process_payment", context=TraceId(0x...), parent=None, kind=SpanKind.INTERNAL, status=Status(StatusCode.UNSET), start_time=..., end_time=..., attributes={})
Span(name="validate_card", context=TraceId(0x...), parent=..., kind=SpanKind.INTERNAL, status=Status(StatusCode.UNSET), start_time=..., end_time=..., attributes={})
Span(name="charge_bank", context=TraceId(0x...), parent=..., kind=SpanKind.INTERNAL, status=Status(StatusCode.UNSET), start_time=..., end_time=..., attributes={})
```

Exporters and next steps
When you move beyond local testing, replace `ConsoleSpanExporter` with an exporter for your backend. Common choices:

| Exporter | Use case                                                         | Docs                                                                                                                                         |
| -------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| OTLP     | Send traces to the OpenTelemetry Collector or supported backends | [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/) |
| Jaeger   | Send traces directly to a Jaeger backend                         | [https://www.jaegertracing.io/](https://www.jaegertracing.io/)                                                                               |
| Zipkin   | Send traces directly to Zipkin                                   | [https://zipkin.io/](https://zipkin.io/)                                                                                                     |

You can also configure the OpenTelemetry Collector to receive OTLP and forward traces to many backends. See the OpenTelemetry Collector docs for pipeline examples.

Best practices and considerations

* Add meaningful span names, attributes, and events to capture the context that helps debugging (e.g., masked card identifier, user id, HTTP status).
* Use automatic instrumentation libraries for frameworks and popular libraries when available; complement them with manual spans for business logic.
* Keep spans short-lived and focused on logical units of work.
* Avoid logging sensitive data to spans or attributes. Use masking or hashing when necessary.

<Callout icon="warning">
  Do not store unmasked sensitive data (full card numbers, personal identifiers, secrets) in span attributes. Use masking or tokenization to protect user data in telemetry.
</Callout>

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* OpenTelemetry Python instrumentation: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* OTLP exporter docs: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/](https://opentelemetry.[AWS_SECRET_ACCESS_KEY]/otlp/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Zipkin: [https://zipkin.io/](https://zipkin.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/59f4df72-f060-49ab-9e7d-e475b134b20b" />
</CardGroup>


# Demo Instrumenting Application Creating the First Span

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Instrumenting-Application-Creating-the-First-Span/page

Guide to creating and managing OpenTelemetry spans in Python, using context managers, nesting, function-level instrumentation and decorators for reliable tracing.

In this lesson you'll generate and inspect the first OpenTelemetry span in a simple Python application. We'll cover:

* Explicit span lifecycle with `start_span()` / `end()`
* The recommended Python context manager `start_as_current_span`
* Nesting spans to form parent/child relationships
* Moving span creation inside functions
* Using the context manager as a decorator for concise function-level instrumentation

Prerequisite: a `configure_tracer()` helper that returns a configured tracer (for example via `trace.get_tracer(...)` after installing a `TracerProvider` and a span exporter). See the OpenTelemetry Python docs for setup details: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)

***

## 1) Creating a span with start\_span / span.end()

You can explicitly start and end a span. This is straightforward but becomes noisy as code grows.

Example (payment.py):

```python theme={null}
