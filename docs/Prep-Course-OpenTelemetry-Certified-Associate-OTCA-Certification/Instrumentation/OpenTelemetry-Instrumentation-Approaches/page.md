# app.py
import requests

def call_slow_api():
    url = "http://httpbin.org/delay/2"
    response = requests.get(url)
    return response.text

def main():
    print("Calling slow API...")
    result = call_slow_api()
    print("Done! Response length:", len(result))

if __name__ == "__main__":
    main()
```

The call to `requests.get(url)` makes a network call to a remote service. We want to measure how long that HTTP call takes and capture additional metadata about the request and response.

## Manual instrumentation (explicit spans)

You can create spans manually around application code to record timing and metadata. This requires setting up a TracerProvider, span processor, and exporter, and creating spans with the tracer API:

```python theme={null}
# manual_instrumentation.py
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# SDK setup (so spans are recorded and exported)
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

def call_slow_api():
    # Manually create a span around the HTTP call
    with tracer.start_as_current_span("call_httpbin_delay"):
        url = "http://httpbin.org/delay/2"
        response = requests.get(url)
        return response.text

def main():
    with tracer.start_as_current_span("main_function_span"):
        print("Calling slow API...")
        result = call_slow_api()
        print("Done! Response length:", len(result))

if __name__ == "__main__":
    main()
```

A console exporter prints spans similar to the following (abbreviated):

```json theme={null}
{
  "name": "call_httpbin_delay",
  "kind": "SPAN_KIND_INTERNAL",
  "start_time": "2023-05-16T11:17:59.783592Z",
  "end_time": "2023-05-16T11:17:59.979302Z",
  "attributes": {},
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.31.1",
      "service.name": "unknown_service"
    }
  }
}
```

Manual instrumentation works well for targeted tracing, but applying it across many libraries and frameworks you do not own is time-consuming and error-prone.

## The challenge: so many frameworks and libraries

The Python ecosystem (and other ecosystems) contains many frameworks and clients — web frameworks, HTTP clients, ORMs, messaging clients, and more. Instrumenting each call site manually across services quickly becomes unrealistic.

<Frame>
  <img alt="The image lists various frameworks and tools categorized under web frameworks, libraries and clients, ORMs and DB clients, messaging and RPC, and observability targets. It highlights the problem of having too many frameworks." />
</Frame>

What we want:

* Observability out of the box for commonly used libraries
* Minimal effort for application developers
* No vendor lock-in
* Reuse across multiple apps and teams

<Frame>
  <img alt="The image outlines the need for instrumentation libraries, highlighting four key points: &#x22;Observability out of the box,&#x22; &#x22;Minimal effort,&#x22; &#x22;No vendor lock-in,&#x22; and &#x22;Reuse across apps,&#x22; each represented with a respective icon." />
</Frame>

## OpenTelemetry Instrumentation Libraries

OpenTelemetry instrumentation libraries provide automatic tracing and/or metrics for popular third-party libraries. They are pre-built packages that apply language-specific techniques (in Python this is typically monkey patching) to wrap functions and capture telemetry with minimal or zero changes to your application code.

Common targets:

* HTTP clients: `requests`, `httpx`, `aiohttp`
* Web frameworks: `Flask`, `Django`, `FastAPI`
* ORMs and DB drivers: `SQLAlchemy`, database-specific drivers
* Messaging and RPC: `kafka-python`, `pika`, `celery`
* Cloud SDKs: `boto3`, etc.

Package naming convention (typical):

* `opentelemetry-instrumentation-<library-name>`

<Frame>
  <img alt="The image lists five features of OTel Instrumentation Libraries: pre-built packages, language-specific techniques, zero-touch observability, comprehensive coverage, and standardized data." />
</Frame>

Examples of instrumentation packages:

<Frame>
  <img alt="The image lists three OpenTelemetry instrumentation examples, each with a colorful numbered icon: requests for HTTP calls, Django for apps, and SQLAlchemy for database queries." />
</Frame>

## Auto-instrumenting the example using RequestsInstrumentor

Instead of adding spans manually around each HTTP call, enable the `requests` instrumentation package. Instrumentation libraries themselves use only the OpenTelemetry API — your application still configures the SDK and exporters.

```python theme={null}
# auto_instrument_requests.py
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# SDK setup (needed so spans are recorded and exported)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

# Auto-instrument the requests library (one line)
RequestsInstrumentor().instrument()

def call_slow_api():
    url = "http://httpbin.org/delay/2"
    response = requests.get(url)  # This call is automatically traced
    return response.text

def main():
    print("Calling slow API...")
    result = call_slow_api()
    print("Done! Response length:", len(result))

if __name__ == "__main__":
    main()
```

The instrumentation automatically creates spans for the HTTP client with semantic attributes (for example: `http.method`, `http.url`, `http.status_code`). A console-exported span for an instrumented HTTP GET might look like:

```json theme={null}
{
  "name": "HTTP GET",
  "kind": "SpanKind.CLIENT",
  "start_time": "2025-09-26T13:12:30.431667Z",
  "end_time": "2025-09-26T13:12:31.087899Z",
  "status": { "status_code": "ERROR" },
  "attributes": {
    "http.method": "GET",
    "http.url": "http://httpbin.org/delay/2",
    "http.status_code": 503
  },
  "resource": {
    "attributes": {
      "telemetry.sdk.language": "python",
      "telemetry.sdk.name": "opentelemetry",
      "telemetry.sdk.version": "1.14.0",
      "service.name": "unknown_service"
    }
  }
}
```

## How the instrumentation library works (high level)

When you call `RequestsInstrumentor().instrument()`, the instrumentor finds and wraps the relevant methods in the `requests` package (for example, `get`, `post`, `put`, `delete`) and replaces them with instrumented wrappers. This is usually implemented via monkey patching. Each instrumented call typically:

1. Creates a client span using the OpenTelemetry API,
2. Executes the original `requests` call, and
3. Ends the span and attaches semantic attributes based on the response.

<Frame>
  <img alt="The image is a diagram explaining the functions of an instrumentation library, highlighting method interception, automatic span creation, and data captured without code changes." />
</Frame>

### Simplified illustration of monkey patching (conceptual)

```python theme={null}
# Conceptual pseudocode (not a real implementation)
original_get = requests.get

def instrumented_get(url, *args, **kwargs):
    # start a client span using the OpenTelemetry API
    # call original_get(url, *args, **kwargs)
    # set span attributes such as http.method, http.url, http.status_code
    # end the span
    return original_get(url, *args, **kwargs)

# Replace requests.get at runtime with the instrumented wrapper
requests.get = instrumented_get
```

## Instrumentation libraries only use the OpenTelemetry API

Instrumentation packages should depend only on the OpenTelemetry API, not on any particular SDK implementation. The application sets up the SDK (TracerProvider, processors, exporters) to record and export telemetry. This separation ensures:

* SDK-agnostic instrumentations,
* App developers can choose exporters and processors,
* Reusable, composable instrumentations across organizations.

<Frame>
  <img alt="The image is an infographic titled &#x22;Instrumentation Libraries&#x22; depicting three main points: using only OpenTelemetry API, hooking into library behavior, and starting/ending spans." />
</Frame>

## When to use instrumentation libraries

Instrumentation libraries are appropriate when:

* You want automatic observability without modifying application source code.
* You need consistent semantic data across services (instrumentations follow OpenTelemetry semantic conventions).
* You want to share observability setup across teams and projects.
* You want to extend OpenTelemetry support for in-house libraries by authoring custom instrumentations.

<Frame>
  <img alt="The image outlines four scenarios for using instrumentation libraries with OpenTelemetry, focusing on using and sharing frameworks, extending support for custom libraries, achieving consistent observability, and supporting custom or internal libraries." />
</Frame>

## What instrumentation libraries include — and what they don't

* They hook into third-party libraries and start spans or collect metrics where appropriate.
* They populate semantic attributes automatically.
* They provide instrumented methods so your source code remains unchanged.

What they do not do:

* They do not configure or export telemetry; the application must set up the SDK, span processors, and exporters.
* They should not depend on a particular SDK implementation.

| Instrumentation libraries include                        | Instrumentation libraries do not include     |
| -------------------------------------------------------- | -------------------------------------------- |
| Hook into third-party libraries and create spans/metrics | Configure SDKs, processors, or exporters     |
| Populate semantic attributes automatically               | Depend on a particular SDK implementation    |
| Provide zero/low-touch observability for apps            | Handle backend-specific exporting or storage |

<Frame>
  <img alt="The image compares what instrumentation libraries include versus what they don't. It highlights tasks like wrapping third-party libraries and starting spans as included, while exporting telemetry data and configuring processors are aspects not included." />
</Frame>

## Design goals when authoring instrumentation libraries

If you author an instrumentation library, follow these design goals:

* Be SDK-agnostic — use only the OpenTelemetry API.
* Allow application developers to configure SDKs and exporters.
* Be composable and pluggable across projects.
* Follow OpenTelemetry semantic conventions for attribute naming and events.

<Frame>
  <img alt="The image outlines the design goals of an Instrumentation Library, which include being SDK-agnostic, allowing app developers to configure SDK and exporters, being composable and pluggable, and following semantic conventions." />
</Frame>

<Callout icon="lightbulb">
  When writing an instrumentation, rely only on the OpenTelemetry API (not the SDK). Let applications decide which SDK, processors, and exporters to use.
</Callout>

## Summary — responsibilities: instrumentation libraries vs applications

* Instrumentation libraries: decide what to collect (spans/metrics), how to name/annotate them, and how to hook into library behavior. They should be reusable and depend only on the OpenTelemetry API.
* Applications: decide how to process and export telemetry. Applications configure SDKs, span processors, and exporters to send data to chosen observability backends.

<Frame>
  <img alt="The image compares key takeaways between Instrumentation Libraries and Applications, highlighting features like reuse, configuration, and data flow customization in the context of OpenTelemetry." />
</Frame>

Further reading and references:

* OpenTelemetry Documentation: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Python instrumentation packages: search PyPI for `opentelemetry-instrumentation-<library-name>`

This article covered instrumentation libraries.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/d97970ef-6201-45c2-813e-e03bc75ad77a/lesson/1c859e64-d3c2-4519-92a9-a797e05ae804" />
</CardGroup>


# OpenTelemetry Instrumentation Approaches

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Instrumentation/OpenTelemetry-Instrumentation-Approaches/page

Overview of OpenTelemetry instrumentation approaches including manual, library-based, and auto-instrumentation, how to create custom spans, evaluate trade-offs, and practical recommendations for application observability

This lesson explains the primary OpenTelemetry instrumentation approaches, when to use each, and how to create custom spans with the OpenTelemetry API. You'll learn how to instrument applications for traces, metrics, and logs to gain visibility into performance and reliability.

By the end of this section you should be able to:

* Distinguish manual, automatic, and library-based instrumentation and know when to use each.
* Create custom spans using the OpenTelemetry API.
* Enable auto-instrumentation for applications without source-code changes (with minimal setup).
* Use instrumentation libraries for common frameworks and evaluate trade-offs between approaches.

<Frame>
  <img alt="The image lists four objectives related to instrumentation techniques, including manual and automatic methods, knowing when to use each, creating custom spans with an API, and enabling auto-instrumentation with minimal setup." />
</Frame>

You should also be able to decide when to adopt library-based instrumentation for frameworks you commonly use, and weigh trade-offs such as control, effort, and setup speed.

<Frame>
  <img alt="The image features a list of objectives with two points: &#x22;Use instrumentation libraries for common frameworks&#x22; and &#x22;Evaluate trade-offs in each approach,&#x22; labeled as steps 5 and 6. It has a turquoise gradient background on the left labeled &#x22;Objectives.&#x22;" />
</Frame>

## What is instrumentation?

Instrumentation is the practice of adding code or runtime tooling that generates telemetry—traces, metrics, and logs—so you can observe application behavior. Think of instrumentation like installing meters or probes in a system: it enables measurement and helps you understand how components perform and interact.

<Frame>
  <img alt="The image illustrates the concept of instrumentation, with a person holding a laptop next to a large smartphone displaying app icons. The text explains that instrumentation involves adding code or tools to generate telemetry for observing application behavior." />
</Frame>

## Why instrumentation matters

Instrumentation provides the visibility required for diagnosing performance issues, improving reliability, and automating operational responses. Without instrumentation, troubleshooting becomes guesswork—similar to trying to manage electricity usage without meters. Instrumentation is essential in production, but also valuable during development and testing.

<Frame>
  <img alt="The image explains the importance of visibility in software, highlighting application behavior, performance, and reliability, and the necessity of seeing software operations in production." />
</Frame>

Instrumentation is the foundation for observability: it standardizes how telemetry is collected, enables end-to-end tracing of requests, and unlocks automation and actionable insights.

<Frame>
  <img alt="The image is an infographic titled &#x22;Importance of Instrumentation&#x22; highlighting four points: foundation for observability, standardized data collection, enabling end-to-end tracing, and driving automation and insights. Each point is numbered and represented by a corresponding icon and color." />
</Frame>

## Three main instrumentation approaches

1. Manual (code-based) instrumentation
   * Developers add explicit OpenTelemetry API calls in application code to create spans, attributes, events, and links.
   * Offers the most control and flexibility for custom business logic and fine-grained traces, but requires developer effort and ongoing maintenance.

2. Library-based instrumentation
   * Uses framework- or library-specific packages (instrumentation libraries) that hook into common operations (HTTP servers/clients, database drivers, messaging libraries) to produce spans automatically.
   * Requires access to the codebase to add libraries but reduces the need to implement per-operation spans manually.

3. Auto-instrumentation (zero-code changes)
   * Uses agents, sidecars, or runtime wrappers to instrument applications at runtime without modifying source code.
   * No source changes required; typically involves adding a JVM agent, language runtime wrapper, or a container sidecar/startup flag.

<Frame>
  <img alt="The image illustrates three types of instrumentation: manual instrumentation, library-based instrumentation, and auto-instrumentation, each represented with different icons and colors." />
</Frame>

### When to use each approach

* Manual instrumentation
  * Use when you need full control or must capture business-specific operations and context that automatic tools cannot infer.
* Library-based instrumentation
  * Use when your framework is supported by instrumentation libraries and you want broad coverage with moderate implementation effort.
* Auto-instrumentation
  * Use when you cannot modify source code (e.g., legacy apps) or when you need rapid coverage across many services with minimal developer time.

<Callout icon="lightbulb">
  Auto-instrumentation still requires deployment or runtime changes (for example adding a JVM agent or language-specific runtime hook). It does not require source code edits, but it does require configuring the runtime or deploying an agent/sidecar.
</Callout>

## Example: creating custom spans (manual instrumentation)

Below is a concise Python example demonstrating manual instrumentation with the OpenTelemetry API. It shows how to configure a tracer provider, add a console exporter, and create nested spans (parent and child). This pattern maps to other languages: initialize a tracer provider/exporter, then use the tracer API to start spans and add attributes, events, or links.

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
