# Service A (outbound)
propagator.inject(context, headers, setter)

# Service B (inbound)
context = propagator.extract(headers, getter)
```

<Frame>
  <img alt="The image explains how W3C headers work, detailing injection and extraction by TextMapPropagator methods and maintaining trace continuity across distributed systems." />
</Frame>

TextMapPropagator is transport-agnostic because it operates on generic key-value pairs. It works for HTTP headers, gRPC metadata, messaging attributes, and custom carriers.

<Frame>
  <img alt="The image provides an overview of TextMapPropagators, an OpenTelemetry API interface for serializing and deserializing trace context, with icons representing these processes." />
</Frame>

The propagator bridges in-process context to out-of-process communication, enabling traces to be stitched across microservices.

<Frame>
  <img alt="The image explains why TextMap Propagators are used, highlighting their function in enabling context propagation over protocols and bridging in-process context to out-of-process communication." />
</Frame>

API operations summary:

* Inject: serialize a `context` into an outgoing carrier (e.g., HTTP headers).
* Extract: deserialize a `context` from an incoming carrier for continued tracing.

<Frame>
  <img alt="The image explains two API operations: &#x22;Inject&#x22; which writes context into an outgoing carrier like HTTP headers, and &#x22;Extract&#x22; which reads context from an incoming carrier to continue the trace." />
</Frame>

API building blocks:

* Carrier: typically a dictionary-like map of headers or metadata.
* Setter/Getter: functions for writing/reading the carrier entries.
* Global propagator: application-level configuration that defines which propagation formats are used (e.g., W3C, B3, composite).

<Frame>
  <img alt="The image outlines key concepts: Carrier, Setter/Getter, and Global Propagator, explaining their roles in data transport and configuration." />
</Frame>

B3 propagation

B3 (from Zipkin) is a simpler, legacy propagation format still used by many systems (including Istio/Envoy). B3 headers include `X-B3-TraceId`, `X-B3-SpanId`, `X-B3-ParentSpanId` (optional), and `X-B3-Sampled`.

<Frame>
  <img alt="The image explains B3 Propagation Basics, highlighting its purpose for Zipkin due to its simplicity and compatibility, and listing the headers used: X-B3-TraceId, X-B3-SpanId, and the optional X-B3-ParentSpanId." />
</Frame>

Example B3 headers:

```text theme={null}
X-B3-TraceId: 4bf92f3577b34da6a3ce929d0e0e4736
X-B3-SpanId: 00f067aa0ba902b7
X-B3-Sampled: 1
```

To enable B3 propagation in Python OpenTelemetry:

```python theme={null}
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat

set_global_textmap(B3MultiFormat())
```

B3 remains useful for backward compatibility with Zipkin-based ecosystems and tools that expect B3 headers.

Composite propagators

OpenTelemetry supports CompositePropagator, which injects and extracts using multiple formats (for example, W3C + B3). This is useful in mixed environments or during migrations.

<Frame>
  <img alt="The image illustrates the use of composite propagators in OpenTelemetry, showing how the OpenTelemetry SDK injects and extracts context through multiple propagation formats and services." />
</Frame>

When injecting, the SDK can write both W3C and B3 headers to outgoing requests. On extraction, it will try multiple propagators until it finds a valid trace context.

Composite propagators are useful for:

* Supporting multiple vendors that require different formats
* Hybrid environments where some services use W3C and others use B3
* Migrating formats while preserving backward compatibility

<Frame>
  <img alt="The image explains when to use composite propagators in OpenTelemetry, highlighting scenarios involving multiple vendor integrations, different standards, and migration needs." />
</Frame>

Python example configuring a CompositePropagator:

```python theme={null}
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagators.tracecontext import TraceContextTextMapPropagator

set_global_textmap(
    CompositePropagator([
        TraceContextTextMapPropagator(),  # W3C Trace Context
        B3MultiFormat()                   # B3 (Zipkin)
    ])
)
```

<Frame>
  <img alt="The image is a table comparing scenarios with the benefits of composite propagation, highlighting support for B3 and W3C formats and integration solutions." />
</Frame>

Quick reference tables

Headers and their purpose

| Header         | Purpose                                                  | Example                            |
| -------------- | -------------------------------------------------------- | ---------------------------------- |
| `traceparent`  | Core W3C trace identifiers and flags                     | `00-4bf92f35...-01`                |
| `tracestate`   | Vendor-specific trace metadata                           | `vendorname=value`                 |
| `baggage`      | Arbitrary key-value metadata that travels with the trace | `user_id=42,region=us-east`        |
| `X-B3-TraceId` | B3 trace identifier                                      | `4bf92f3577b34da6a3ce929d0e0e4736` |
| `X-B3-SpanId`  | B3 span identifier                                       | `00f067aa0ba902b7`                 |
| `X-B3-Sampled` | B3 sampling flag                                         | `1`                                |

Propagator types

| Propagator          | Use case                                   | Notes                                   |
| ------------------- | ------------------------------------------ | --------------------------------------- |
| Trace Context (W3C) | Default in OpenTelemetry                   | Uses `traceparent`/`tracestate`         |
| W3C Baggage         | Carry arbitrary metadata                   | Uses `baggage` header                   |
| B3                  | Legacy/Zipkin ecosystems                   | `X-B3-*` headers                        |
| CompositePropagator | Multi-format compatibility                 | Combines multiple propagators           |
| Custom propagator   | Proprietary carriers or unusual transports | Implement `TextMapPropagator` interface |

<Frame>
  <img alt="The image is a table comparing various trace context propagation formats, including &#x22;W3C TraceContext,&#x22; &#x22;W3C Baggage,&#x22; &#x22;B3,&#x22; &#x22;Jaeger,&#x22; &#x22;OT Trace,&#x22; &#x22;OpenCensus BinaryFormat,&#x22; and &#x22;Vendor-specific,&#x22; each with a brief description of its purpose or use." />
</Frame>

Other formats and legacy options

You may still encounter other propagation formats (Jaeger headers, ot-trace from OpenTracing, OpenCensus binary formats, or vendor-specific headers). However, W3C Trace Context and W3C Baggage are the industry-standard defaults that OpenTelemetry prefers.

<Frame>
  <img alt="The image is a table summarizing key takeaways about composite propagation benefits in various scenarios, such as Trace ID/Span ID, Context, Carrier, and more. Each scenario is paired with its corresponding benefit, detailing how metadata and APIs are used for context propagation." />
</Frame>

Recap — key concepts

* Trace ID: unique identifier for a trace
* Span ID: unique for a span; used as parent ID for child spans
* Context: object that holds trace data (trace ID, span ID, flags, trace state)
* Carrier: transport medium for context (HTTP headers, gRPC metadata, messaging attributes)
* Inject/Extract: operations for writing/reading context to/from a carrier
* TextMapPropagator: API responsible for serializing/deserializing context
* Global propagator: config that selects active propagation formats in your application

<Frame>
  <img alt="The image is a table summarizing key takeaways about propagation standards, including W3C Trace Context, W3C Baggage, B3 Propagation, and Composite Propagator. It details the headers used and provides a brief description of each standard." />
</Frame>

Final summary

Context is the object that carries trace data (trace ID, span ID, trace flags, optional tracestate). Propagation is the mechanism that serializes and deserializes that context across process or service boundaries. OpenTelemetry defaults to W3C Trace Context and W3C Baggage, but supports other formats (B3, composite, and vendor-specific) via propagators to ensure backward compatibility and smooth migrations.

<Frame>
  <img alt="The image is a summary of points regarding context and propagation in OpenTelemetry, highlighting standards, APIs, and support for older formats." />
</Frame>

<Callout icon="lightbulb">
  OpenTelemetry defaults to the W3C Trace Context and W3C Baggage formats. Use composite propagators when you need to support multiple propagation standards simultaneously (for example, during a migration or when integrating with legacy tooling).
</Callout>

Links and references

* W3C Trace Context: [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/)
* W3C Baggage: [https://www.w3.org/TR/baggage/](https://www.w3.org/TR/baggage/)
* OpenTelemetry Propagation (official docs): [https://opentelemetry.io/docs/reference/specification/context/api-propagators/](https://opentelemetry.io/docs/reference/specification/context/api-propagators/)
* B3 Propagation (Zipkin): [https://github.com/openzipkin/b3-propagation](https://github.com/openzipkin/b3-propagation)

That's it for this article on context propagation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/01d79812-b5b1-4b5d-b791-136c910bb5a2" />
</CardGroup>


# Demo Tracing Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Span-Anatomy-and-Context-Propagation/Demo-Tracing-Overview/page

Walkthrough of using OpenTelemetry, Jaeger, and Grafana to inspect distributed traces, read spans, and troubleshoot performance and errors across services.

In this lesson we'll walk through real distributed traces so you can quickly see what trace data looks like, how to read spans, and how to use traces to troubleshoot production issues. The demo uses an application instrumented with OpenTelemetry that exports traces to Jaeger. Grafana is connected to the Jaeger datasource so we can search and inspect traces inside Grafana’s Explore view.

<Callout icon="lightbulb">
  This guide assumes you have traces being exported to a Jaeger-compatible backend and Grafana configured with a Jaeger datasource. If you need setup guidance, see the OpenTelemetry, Jaeger, and Grafana docs linked in References.
</Callout>

How to query traces in Grafana

* Open Grafana → Explore.
* Select the Jaeger datasource.
* Enter filters such as `service` or `operation` (span name), and optional attribute matches or min/max duration.
* Limit the time range (e.g., last 5 minutes) before running the query.

Below I start from the frontend service because user-initiated flows originate there.

<Frame>
  <img alt="The image shows a Grafana interface with a Jaeger query panel where a service name is being selected. The user is choosing between &#x22;Frontend Service,&#x22; &#x22;Product Backend Service,&#x22; and &#x22;jaeger-all-in-one.&#x22;" />
</Frame>

After selecting the service you can inspect available operation names (span names) such as `getUserCart`, `getIndividualProduct`, `getRecommendedProduct`, `requestToTheProductsAPI`, `updateProduct`. For this walkthrough I select all operations to capture a representative trace.

<Frame>
  <img alt="The image shows a Grafana interface with Jaeger integration, displaying an operation name dropdown for querying services like &#x22;Delete Product,&#x22; &#x22;Get User Cart,&#x22; and &#x22;Update Product.&#x22;" />
</Frame>

Run the query with a narrow time window (last 5 minutes). Grafana lists traces with metadata such as trace name, start time, and total duration. Open an interesting trace and undock the details panel for more room.

This selected trace shows:

* Trace ID and start timestamp.
* Total duration (\~80 ms).
* Involved services: frontend and backend.
* Total spans: four.\
  Expand each span to view service-level or span-level details. The first span is the frontend root span representing the initial update product action.

<Frame>
  <img alt="The image shows a Jaeger UI interface used for tracing operations in a &#x22;Frontend Service: Update Product&#x22; process, displaying span details and timings for various service operations." />
</Frame>

Reading the frontend root span

* Root span: starts at 0 relative to the trace.
* Duration: \~79 ms (matches trace total because the root waits for children).
* Resource attributes: host, pod, region, etc. (this demo instruments a minimal set).
* Span attributes: in-application metadata such as service name and version.

The frontend span has a child that issues an HTTP request to the product backend. That child span includes richer HTTP attributes.

<Frame>
  <img alt="The image shows a Jaeger UI interface displaying trace details for a &#x22;Frontend Service: Update Product&#x22; operation, including span attributes like HTTP method and status code." />
</Frame>

Typical HTTP client span details

* Request URL and path (backend endpoint).
* HTTP method (`PATCH`) and status code (`200`).
* Span kind: `client`.
* Events: timestamped logs such as `request.sent`. Events are ideal for attaching exceptions or custom logs to spans.

<Frame>
  <img alt="The image shows an interface from Jaeger, a distributed tracing system, displaying a trace for a &#x22;Frontend Service: Update Product&#x22; operation. It includes details like HTTP method, status code, URL, and service duration." />
</Frame>

The backend receives the request and performs the `update-product` operation.

<Frame>
  <img alt="The image shows a Jaeger UI displaying tracing information for a service called &#x22;Frontend Service: Update Product,&#x22; including query types, trace IDs, and detailed span information." />
</Frame>

Backend span highlights

* Service name: `product-backend-service`.
* Backend span total: \~73 ms.
* A DB child span: \~1.23 ms.
* Start times are relative to the trace root; e.g., frontend root = 0 µs, backend starts at \~21 µs, DB child at \~1.23 ms — these offsets show timing relationships between steps.

Common backend span and resource attributes

| Attribute                    | Meaning / Example                               |
| ---------------------------- | ----------------------------------------------- |
| `span.kind`                  | Role of span: `server` for incoming HTTP        |
| `net.peer.ip` / `client.ip`  | Client address (may be loopback in local demos) |
| `http.method`                | HTTP verb (e.g., `PATCH`, `GET`)                |
| `http.target` / `http.url`   | Path/URL called (e.g., `/products`)             |
| `db.statement` / `SQL_QUERY` | SQL query text or signature (if instrumented)   |
| `service.version`            | App version for troubleshooting regressions     |

<Frame>
  <img alt="The image shows a Jaeger UI interface displaying trace details for a &#x22;Frontend Service: Update Product&#x22; operation, including span attributes such as client IP, HTTP method, and service attributes." />
</Frame>

Instrumenting database calls
I instrumented the SQL executed by the backend so the DB query appears as its own span. Including either the full SQL or a query signature in a span attribute makes it far easier to find slow or incorrect queries.

```sql theme={null}
UPDATE products SET /* column = value */ WHERE product_id = 12;
```

Recording the SQL in a span attribute speeds escalation to DB or query-optimization teams with exact text and timing.

Why traces matter for performance troubleshooting
Traces provide a step-by-step timeline across services. Use duration filters to find slow requests (e.g., search for traces with min duration > 1s). In the next example I filter for traces longer than 1 second and open a trace that took 1.61 s. The initial spans are microseconds–milliseconds, but a final DB call to fetch recommended products consumed the full 1.61 s — isolating the query as the latency source.

<Frame>
  <img alt="The image shows a Jaeger UI screen displaying the trace details of a &#x22;Frontend Service: Get recommended Products&#x22; operation, including various span attributes and service durations." />
</Frame>

Example span attributes for the slow DB client span:

* `otel.scope.name`: "charge.py"
* `otel.scope.version`: "0.5.0"
* `span.kind`: "client"
* `SQL_QUERY`: "select \* from recommended\_products"

These attributes let you hand off the exact problematic query and timing to the team that owns the database.

<Callout icon="lightbulb">
  Use duration filters when troubleshooting performance problems: start broad (for example, `min duration > 1s`) and then drill into individual traces to identify the single offending span(s).
</Callout>

Traces and errors
Traces capture errors and exceptions. When a request fails, the span may be marked `error = true` and include an exception event with a stack trace. Searching for traces where `error = true` helps you quickly surface failing requests.

Below is an example exception recorded as a span event. The frontend failed to connect to the cart service (connection refused). The exception payload includes the HTTP client error message and the Python stack trace, which drastically reduces time-to-fix.

<Frame>
  <img alt="The image is a screenshot of a monitoring dashboard, likely from Jaeger, showing trace details for a &#x22;Frontend Service: Get User Cart&#x22; operation, including span attributes and an error indication." />
</Frame>

```plaintext theme={null}
event: "exception"
exception.escaped: "False"
message: "HTTPConnectionPool(host='127.0.0.1', port=4000): Max retries exceeded with url: /cart (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x10117fb10>: Failed to establish a new connection: [Errno 61] Connection refused'))"

Traceback (most recent call last):
  File "/Users/sanjeev/.local/share/mise/installs/python3.11/lib/python3.11/site-packages/urllib3/connection.py", line 198, in _new_conn
    sock = connection.create_connection(...)
  File "/Users/sanjeev/.local/share/mise/installs/python3.11/lib/python3.11/site-packages/urllib3/util/connection.py", line 73, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [Errno 61] Connection refused

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/sanjeev/Documents/courses/traces-overview-demo/frontend.py", line 152, in get_cart
    resp = requests.get(url, headers=headers)
  File "/Users/sanjeev/.local/share/virtualenvs/python3.11.13/lib/python3.11/site-packages/requests/api.py", line 73, in get
    return request('GET', url, **kwargs)
  File "/Users/sanjeev/.local/share/virtualenvs/python3.11.13/lib/python3.11/site-packages/requests/sessions.py", line 589, in send
    r = adapter.send(request, **kwargs)
  File "/Users/sanjeev/.local/share/mise/installs/python3.11/site-packages/requests/adapters.py", line 677, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=4000): Max retries exceeded with url: /cart (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x101177fb0>: Failed to establish a new connection: [Errno 61] Connection refused'))
```

Embedding exceptions and stack traces into spans eliminates guesswork: you can see the exact failing call and error, enabling faster diagnosis of network or application faults.

Summary and next steps

* Traces provide correlated, time-ordered telemetry across service boundaries to pinpoint latency hotspots and failing calls.
* Instrument your services with the OpenTelemetry SDK for your language and configure an exporter (e.g., Jaeger) so services emit spans like the ones shown above.
* Focus on these practical steps when troubleshooting:
  1. Filter traces by duration to find slow flows.
  2. Drill into a trace and inspect per-span attributes and events.
  3. Look for `error = true` spans and exception events for root cause details.
  4. If available, use `db.statement` or `SQL_QUERY` to escalate DB problems.

References

* [OpenTelemetry](https://opentelemetry.io/)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [Grafana](https://grafana.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/08ca5e35-f17f-4d9e-8af0-b682096c902d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/2708459f-e4ca-4659-9878-5769d439a274/lesson/ea587a18-6533-4256-96a8-6a0a20fea583" />
</CardGroup>
