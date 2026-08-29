# payment.py
def validate_card():
    print("validating card")

def charge_bank():
    print("charging bank")

def process_payment():
    print("processing payment")
    validate_card()
    charge_bank()

if __name__ == "__main__":
    tracer = configure_tracer()
    span = tracer.start_span("Starting Payment")
    process_payment()
    span.end()
```

Console output:

```text theme={null}
processing payment
validating card
charging bank
```

Example of a simple span export:

```json theme={null}
{
  "name": "Starting Payment",
  "context": {
    "trace_id": "0xc93db6fa28200f8c912670aa9a348424",
    "span_id": "0xb54cc43ed995902d",
    "trace_state": "[]"
  },
  "kind": "SpanKind.INTERNAL",
  "parent_id": null,
  "start_time": "2025-09-09T00:50:07.754666Z",
  "end_time": "2025-09-09T00:50:07.754685Z",
  "status": { "status_code": "UNSET" },
  "attributes": {},
  "events": [],
  "links": [],
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.36.0",
      "service.name": "unknown_service"
    },
    "schema_url": ""
  }
}
```

Key concepts:

* `trace_id` ties all spans in a trace (for example, one user request).
* `span_id` uniquely identifies the current span.
* `parent_id` is `null` for root spans.
* `kind` for in-process spans is `SpanKind.INTERNAL`. Other kinds include `CLIENT` and `SERVER`.

***

## 2) Using the Python context manager (recommended)

Starting and ending spans manually gets error-prone. The recommended pattern in Python is `tracer.start_as_current_span("name")` used as a context manager. It automatically sets the active span and ends it when the block exits (including on exceptions).

Basic example:

```python theme={null}
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("Starting Payment"):
        process_payment()
```

All code inside the `with` block is part of the `"Starting Payment"` span. Use context managers to ensure deterministic start/stop semantics and less boilerplate.

***

## 3) Nesting spans to create parent/child relationships

Nest context-managed spans to model the call hierarchy. The outer span is the parent of the inner span and they share the same `trace_id`.

Example:

```python theme={null}
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("Payment Service"):
        with tracer.start_as_current_span("Starting Payment"):
            process_payment()
```

Result:

* Both spans have the same `trace_id`.
* The `"Starting Payment"` span's `parent_id` is the `"Payment Service"` span's `span_id`.
* Trace backends can visualize these parent/child relationships to show execution flow.

***

## 4) Moving span creation inside functions

Place spans inside the functions they represent so instrumentation is local to the code being traced. This ensures any call to the function automatically creates the span.

Example:

```python theme={null}
def process_payment():
    with tracer.start_as_current_span("Starting Payment"):
        print("processing payment")
        validate_card()
        charge_bank()
```

And call from a top-level parent span:

```python theme={null}
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("Payment Service"):
        process_payment()
```

Keeping spans close to the implementation reduces coupling and makes instrumentation more maintainable.

***

## 5) Adding spans for smaller operations

Instrument smaller operations as child spans so traces reveal finer-grained behavior:

```python theme={null}
def validate_card():
    with tracer.start_as_current_span("Validating Card"):
        print("validating card")

def charge_bank():
    with tracer.start_as_current_span("Charging Bank"):
        print("charging bank")
```

Complete module structure (context managers inside functions):

```python theme={null}
def process_payment():
    with tracer.start_as_current_span("Starting Payment"):
        print("processing payment")
        validate_card()
        charge_bank()

def validate_card():
    with tracer.start_as_current_span("Validating Card"):
        print("validating card")

def charge_bank():
    with tracer.start_as_current_span("Charging Bank"):
        print("charging bank")

if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("Payment Service"):
        process_payment()
```

When executed, you should see multiple spans exported with correct parent/child `parent_id` relationships, providing clear observability into the operation.

<Callout icon="lightbulb">
  Use context managers for deterministic start/stop semantics and for clearer scope handling. They automatically end spans even if exceptions occur.
</Callout>

***

## 6) Using decorators to start a span for a function

You can reuse the context manager as a decorator to start a span every time a function is invoked. Important: the tracer instance used by the decorator must be available at function-definition time.

<Callout icon="warning">
  If using `@tracer.start_as_current_span("...")` as a decorator, initialize the `tracer` (for example with `tracer = configure_tracer()`) before defining the decorated functions. Otherwise the decorator won't have access to the tracer and will raise an error.
</Callout>

Example (initialize tracer first):

```python theme={null}
tracer = configure_tracer()

@tracer.start_as_current_span("Starting Payment")
def process_payment():
    print("processing payment")
    validate_card()
    charge_bank()

@tracer.start_as_current_span("Validating Card")
def validate_card():
    print("validating card")

@tracer.start_as_current_span("Charging Bank")
def charge_bank():
    print("charging bank")

if __name__ == "__main__":
    with tracer.start_as_current_span("Payment Service"):
        process_payment()
```

Notes:

* The decorator starts and ends the span on each function invocation.
* Decorators are concise and readable for simple functions.
* For dynamic span names or attributes, prefer explicit context managers inside the function body.

***

## Quick comparison

| Method                                              | When to use                                                                                                | Example                                                |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `tracer.start_span()` + `span.end()`                | Simple explicit control, rarely recommended for complex code                                               | `span = tracer.start_span("name"); ...; span.end()`    |
| `with tracer.start_as_current_span("name"):`        | Recommended Python pattern for deterministic end and clear scope                                           | `with tracer.start_as_current_span("name"): do_work()` |
| `@tracer.start_as_current_span("name")` (decorator) | Concise instrumentation for small, self-contained functions (tracer must be initialized before decoration) | `@tracer.start_as_current_span("name")\ndef f(): ...`  |

***

## Summary

* Manual spans (`start_span` / `end`) work but are verbose.
* Use `tracer.start_as_current_span("name")` as a context manager for safer, idiomatic Python instrumentation.
* Nest context managers to create parent/child spans and show the call hierarchy.
* Move span creation into functions to ensure instrumentation is applied consistently.
* Use the context manager as a decorator for short, self-contained functions — but initialize the tracer before defining decorated functions.

Further reading and references:

* OpenTelemetry Python documentation: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* OpenTelemetry specification: [https://opentelemetry.io/technical-specification/trace/](https://opentelemetry.io/technical-specification/trace/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/d6517599-f23f-4881-ab12-3f733c4cebd6" />
</CardGroup>


# Demo Propagating Context

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/Demo-Propagating-Context/page

Explains propagating OpenTelemetry trace context across HTTP between payment client and charge server using inject and extract in Python Flask.

In this guide you'll learn how to fix a common tracing problem: two services (payment and charge) producing separate traces for the same user request. The root cause is that the OpenTelemetry context (trace id, span, trace state) is not being propagated across the HTTP boundary. The solution is to inject the current context as headers on the client side and to extract and activate that context on the server side.

Overview

* Client (payment service): inject the current OpenTelemetry context into outgoing HTTP headers.
* Server (charge service): extract the context from incoming headers, attach it for the request lifecycle, and detach it in teardown.

<Callout icon="lightbulb">
  We inject the context into an HTTP carrier (headers) with `inject(...)` and retrieve it on the server with `extract(...)`. Both utilities are available from `opentelemetry.propagate`.
</Callout>

Quick reference

| Action                                | Function                   | Typical use                                           |
| ------------------------------------- | -------------------------- | ----------------------------------------------------- |
| Inject context into outgoing carrier  | `inject(headers)`          | Client: add propagation fields to `requests` headers  |
| Extract context from incoming carrier | `extract(request.headers)` | Server: read propagation fields from incoming request |

## Payment service (client) — inject context into request headers

Goals

* Configure the tracer provider and exporter for the payment service.
* Create a client span for the outgoing HTTP request.
* Call `inject(headers)` before sending the request so propagation fields are added to the HTTP headers.
* Pass `headers` to `requests.get(..., headers=headers)`.

Example payment service (simplified):

```python theme={null}
