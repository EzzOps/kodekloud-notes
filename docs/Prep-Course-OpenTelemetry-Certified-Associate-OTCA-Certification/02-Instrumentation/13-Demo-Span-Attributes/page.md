# Demo Span Attributes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Span-Attributes/page

Explains span attributes in OpenTelemetry Python how to set them best practices and privacy guidance for enriching traces and debugging

In this lesson we'll cover span attributes: what they are, how to attach them to spans in OpenTelemetry (Python), and best practices for using them safely to enrich traces and speed up debugging.

## What are span attributes?

Span attributes are key/value metadata attached to individual spans. They enrich trace data with contextual information (for example, user IDs, account numbers, or external system identifiers) so you can filter, group, and diagnose trace data more effectively.

Resource attributes, in contrast, describe the service that generates telemetry (for example `service.name` and `service.version`). A typical tracer/provider setup looks like this:

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

span_processor = BatchSpanProcessor(exporter)  # exporter configured elsewhere

resource = Resource.create({
    "service.name": "payment-service",
    "service.version": "0.2.0"
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("payment.py", "0.1.0")
```

## Setting span attributes

You can add attributes to spans in multiple ways:

* Set multiple attributes at once with `span.set_attributes({...})`.
* Set a single attribute with `span.set_attribute(key, value)`.
* Provide attributes when creating a span (many APIs accept an `attributes` parameter).

Example: creating spans and adding attributes to the current span

```python theme={null}
from opentelemetry import trace

tracer = configure_tracer()  # configure_tracer should set up provider, exporter, etc.

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    # Get the current span and set multiple attributes at once
    span = trace.get_current_span()
    span.set_attributes({
        "user": "john",
        "account_number": "7372349",
        "bank": "BankOfAmerica"
    })

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
    process_payment()
```

Or set a single attribute:

```python theme={null}
span.set_attribute("user", "john")
```

You can also pass attributes when starting a span (if the API supports it):

```python theme={null}
with tracer.start_as_current_span("Starting Payment", attributes={"user": "john", "env": "prod"}):
    # span already has attributes set at start
    ...
```

Running the earlier script prints:

```plaintext theme={null}
$ python payment.py
processing payment
validating card
charging bank
```

If you inspect the "Starting Payment" span in your tracing backend (for example, [Jaeger](https://www.jaegertracing.io/)), you'll typically see the attributes attached to the span (often displayed as tags): `user`, `account_number`, and `bank`.

> **lightbulb** Avoid placing highly sensitive data (such as full credit card numbers, passwords, or unmasked PII) into span attributes. Traces may be accessible to multiple teams and stored long term. Instead, consider hashing, tokenizing, truncating, or excluding sensitive fields.

## Quick reference: attribute methods

| Method                                       | Use case                                    | Example                                                           |
| -------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------- |
| `span.set_attributes()`                      | Set multiple attributes in one call         | `span.set_attributes({"user":"john","account_number":"7372349"})` |
| `span.set_attribute()`                       | Set or update a single attribute            | `span.set_attribute("user", "john")`                              |
| `start_as_current_span(..., attributes=...)` | Initialize span with attributes at creation | `tracer.start_as_current_span("name", attributes={"env":"prod"})` |

## Best practices

* Instrument with meaningful attributes that help answer operational questions (e.g., which customer, which endpoint, which upstream service).
* Keep cardinality reasonable: avoid unbounded values (like raw identifiers that create a new value per request) that can blow up your backend index.
* Avoid or obfuscate PII and secrets. Use tokens, IDs with limited scope, or aggregated metrics where appropriate.
* Consistently name attributes using clear, lowercase keys (for example, `user.id`, `http.method`, `db.statement`) to make querying easier.

## Links and references

* [OpenTelemetry for Python](https://opentelemetry.io/docs/instrumentation/python/)
* [Jaeger — Distributed Tracing](https://www.jaegertracing.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/f1fdd2bb-7498-48f9-a149-47d09d172baa)
