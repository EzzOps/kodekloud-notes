# Set global tracer provider (application-level configuration)
trace.set_tracer_provider(provider)

# Create a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")
```

The above shows how the API is used by application code. The SDK is the component that provides batching, sampling, and exporting behavior you configure at deployment time.

<Frame>
  <img alt="The image describes the OpenTelemetry API, highlighting its role in defining standardized interfaces for creating and managing traces, metrics, logs, and propagating context across service boundaries. It enables telemetry generation without relying on a specific backend or SDK implementation." />
</Frame>

Key characteristics of the OpenTelemetry API

Your application and third-party libraries call the OpenTelemetry API to record telemetry without needing knowledge of how it will be processed or where it will be sent. The API provides:

* Standardized contracts (tracer, meter, logger interfaces).
* A minimal no-op (NOP) implementation so instrumentation is safe even if no SDK is installed.
* The ability to plug in a full SDK later for sampling, processing, and exporting—without changing instrumented code.

<Frame>
  <img alt="The image outlines three API key characteristics: self-sufficient dependency, no telemetry output by default, and minimal default implementation, with brief descriptions of each." />
</Frame>

Runtime behavior when no SDK is present

If only the API artifacts are available, calls like `trace.get_tracer()` or `meter.get_meter()` succeed and return functional objects. Spans and metrics created in this state are no-op (silently discarded). This design makes library and framework instrumentation safe: instrumentation remains present but harmless if the application never configures an SDK.

API vs SDK — responsibilities comparison

* API: defines the "what" — interfaces for creating and managing spans, metrics, logs, and context propagation.
* SDK: defines the "how" — sampling, batching, exporting, and advanced processing.

Common SDK responsibilities:

* Sampling policies to limit telemetry volume.
* Batching spans and metrics for efficient export.
* Exporters that send telemetry to collectors or observability backends.

<Frame>
  <img alt="The image explains the roles of OpenTelemetry API and SDK, highlighting the API's focus on defining the creation and management of spans, metrics, and logs, and the SDK's role in managing context propagation, sampling, batching, and exporting data to backends." />
</Frame>

Binding contract and portability

The API + SDK form a binding contract between application code and the telemetry implementation. As long as SDK implementations follow the API contract, instrumented code remains unchanged when switching SDKs or backends. This enables consistent instrumentation across languages and flexible backend choices.

<Frame>
  <img alt="The image illustrates the benefits of separating APIs and SDKs, showing app code interfacing with an API layer that includes language-specific APIs (Java, Python, Node.js, Go) and a language-agnostic core specification. It highlights consistent instrumentation across languages and the ability to swap or update SDKs without changing code." />
</Frame>

Practical benefits

* Instrumentation patterns remain similar across languages while staying idiomatic.
* Exporters or SDK implementations can be swapped without touching instrumentation code.
* Application owners choose SDK configuration (exporters, samplers, processors) at deployment time.

<Frame>
  <img alt="The image illustrates the OpenTelemetry API benefits, highlighting consistent code instrumentation across different environments and the ability to update SDKs without changing instrumentation logic." />
</Frame>

Guidelines for library authors

Most apps rely on third-party libraries (DB clients, HTTP clients, messaging libraries). Library authors should instrument using only the OpenTelemetry API (not the SDK) so applications remain free to choose the SDK and configuration.

Do:

* Depend only on the OpenTelemetry API.
* Obtain tracer/meter from the global provider (safe when SDK is absent).
* Propagate and respect context across call paths.
* Use official semantic conventions for spans and attributes: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]\_conventions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)

Don't:

* Leak SDK classes or types in public library signatures.
* Configure exporters, samplers, or processors inside library code.

<Callout icon="lightbulb">
  Library authors: prefer API-only instrumentation. This ensures your instrumented library works regardless of which SDK or exporter the application selects.
</Callout>

<Callout icon="warning">
  Do not configure SDK components (exporters, processors, samplers) inside libraries. SDK setup belongs to the application or deployment environment.
</Callout>

<Frame>
  <img alt="The image provides guidelines for using the OpenTelemetry API, recommending library authors to use the API for its advantages and application developers to choose the SDK while listing &#x22;do&#x22; and &#x22;avoid&#x22; practices." />
</Frame>

Instrumenting libraries — a small Python example

Instrument libraries with API-only calls so the host application decides the SDK:

```python theme={null}
from opentelemetry import trace

tracer = trace.get_tracer(__name__)  # API-only

def handler(req):
    # Start a span (API usage only)
    with tracer.start_as_current_span("lib.operation") as span:
        span.set_attribute("http.route", "/items/{id}")
        # perform library work...
```

<Frame>
  <img alt="The image is a guide on using the OpenTelemetry API for instrumenting libraries, suggesting that library authors use the API to maintain self-sufficiency and portability, while applications should choose the SDK for components like exporters and processors. It includes a &#x22;Do&#x22; list for using OpenTelemetry effectively." />
</Frame>

Language-neutral specification and idiomatic APIs

The specification is language-neutral and does not mandate exact method names. Each language provides idiomatic APIs:

* Python: `start_as_current_span()`
* Java: `SpanBuilder().startSpan()`
* JavaScript: `tracer.startSpan()`
* Go: language-idiomatic start functions

The core principle: use the OpenTelemetry API for spans, metrics, and context propagation; method names are idiomatic per language.

Roles and responsibilities

OpenTelemetry encourages clear role separation so the system remains modular:

* Instrumentation authors: use the API to generate telemetry (spans, metrics, logs). API stability minimizes churn for authors.
* Application owners: configure the SDK at deployment time—choose sampling, exporters, and processing strategies.
* Plugin/SDK authors: implement exporters, processors, and samplers to connect telemetry to backends or to transform/filter data.

<Frame>
  <img alt="The image is a flowchart showing how different roles interact with the OpenTelemetry SDK, including Instrumentation Authors using API, Application Owners for setup, and Plugin Authors with plugin interfaces." />
</Frame>

<Frame>
  <img alt="The image illustrates how different roles, such as instrumentation authors, application owners, and plugin authors, interact with the OpenTelemetry SDK through various components like API, setup, and plugin interfaces. It highlights interactions involving traces, metrics, configurations, exporters, and processors." />
</Frame>

Together these roles let developers add telemetry, operators decide how to handle it, and plugin authors extend the platform to integrate with backends.

Knowledge check

Use these quick questions to verify your understanding.

1. What is the primary purpose of the OpenTelemetry API?

* Options: Export telemetry to backends; provide language-specific SDKs; define the interface for creating telemetry; collect and store telemetry locally.
* Correct: Define the interface for creating telemetry data (traces, metrics, logs). Exporting is handled by SDKs/plugins.

<Frame>
  <img alt="The image is a &#x22;Knowledge Check&#x22; slide asking about the primary purpose of the OpenTelemetry API, with three options listed as answers." />
</Frame>

2. In OpenTelemetry, what does a tracer object do?

* Options: Collect metrics; export spans; create and manage spans; aggregate logs.
* Correct: Create and manage spans to trace operations. Exporting is done by SDK/exporters.

3. Which statement about OpenTelemetry API and SDK is correct?

* Options: API and SDK are tightly coupled; Applications only use the SDK directly; The API is designed to be used independently of the SDK; The API requires a specific backend at compile time.
* Correct: The API is designed to be used independently of the SDK. It is no-op-safe.

4. What happens if an application only uses the OpenTelemetry API and no SDK is configured?

* Options: Application fails to start; Telemetry is generated and exported by default; The API operates in no-op mode without errors; The API throws runtime exceptions for missing SDKs.
* Correct: The API operates in a no-op mode without errors; telemetry is discarded unless an SDK is configured.

<Frame>
  <img alt="The image is a knowledge check slide asking what happens if an application uses the OpenTelemetry API without configuring an SDK, with three possible answers provided." />
</Frame>

That’s it for this lesson/article.

Links and references

* OpenTelemetry documentation: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Python instrumentation guide: [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/)
* Semantic conventions: [https://opentelemetry.[AWS_SECRET_ACCESS_KEY]\_conventions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/81da0512-b628-459a-941a-7ed90b163b3c" />
</CardGroup>


# OpenTelemetry Client Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-Client-Architecture/page

Explains OpenTelemetry client architecture, detailing layers Instrumentation, Semantic Conventions, API, SDK, Contrib for traces, metrics, logs and baggage, plus best practices for instrumentation and runtime configuration

Hello OTel client experts — in this lesson we'll examine how OpenTelemetry clients are layered and how the pieces relate. This article keeps the original ordering and diagrams while clarifying responsibilities, common patterns, and best practices for instrumentation authors and runtime operators.

<Callout icon="lightbulb">
  OpenTelemetry defines a vendor-agnostic model for telemetry signals: traces, metrics, logs, and baggage. Each signal follows a consistent layering pattern — Instrumentation, Semantic Conventions, API, SDK, and Contrib — which separates the contract from runtime behavior and integrations.
</Callout>

Overview

* OpenTelemetry ([https://opentelemetry.io/](https://opentelemetry.io/)) standardizes telemetry signals (traces, metrics, logs) and cross-process baggage.
* For each signal you typically have:
  * Instrumentation — application or framework code that emits telemetry.
  * Semantic conventions — standardized attribute/metric/log keys and meanings.
  * API — the public contract used by instrumentation to create telemetry.
  * SDK — runtime implementation that handles sampling, aggregation, batching, and exporting.
  * Contrib — integration packages, auto-instrumentation, and vendor exporters.

Table: Signal responsibilities at a glance

| Signal  |                          Instrumentation | Semantic Conventions                            | API                                      | SDK                                        | Contrib / Examples                             |
| ------- | ---------------------------------------: | ----------------------------------------------- | ---------------------------------------- | ------------------------------------------ | ---------------------------------------------- |
| Traces  | Create and end spans in application code | `http.method`, `db.statement`                   | Tracer API to create/manage spans        | Sampling, batching, exporting spans        | Auto-instrumentation, exporters (e.g., Jaeger) |
| Metrics |          Emit counters/histograms/gauges | `http.server.duration`, `process.cpu.time`      | Meter API for counters/histograms/gauges | Aggregation, temporality, export           | Prometheus exporters/instrumentation           |
| Logs    |              Emit structured log records | `log.record.original`, `log.file.path.resolved` | Logger API for structured logs           | Processing, enrichment, batching, export   | Fluentd exporters, bridges                     |
| Baggage |       Attach key/value pairs to contexts | Naming conventions for keys                     | Baggage API for get/set                  | Propagation storage and context management | Propagators (B3, Jaeger, W3C Trace Context)    |

Traces

* Instrumentation: application code or instrumented libraries create spans representing operations.
* Semantic conventions: standard attributes such as `http.method` and `db.statement` ensure consistent meaning across services and languages.
* Tracer API: the stable contract libraries and apps call to create and manage spans.
* SDK: implements runtime behavior — sampling policies, span processors (batching/exporting), and the exporter to backends.
* Contrib: integration packages and exporters (for example, Flask instrumentation or Jaeger exporter).

Metrics

* Emitted similarly to traces, but as numerical time-series.
* Semantic conventions: standard metric names (e.g., `http.server.duration`) and units.
* Meter API: defines counters, histograms, and gauges as the instrumentation contract.
* SDK: implements aggregation, temporality, and exporting of metric data.
* Contrib: exporters and integrations such as Prometheus instrumentation.

Logs

* Application code and frameworks can emit structured logs as a first-class signal.
* Semantic conventions standardize log fields to enable correlation with traces and metrics.
* Logger API: how structured logs are created and annotated.
* SDK: log processors, enrichers, batching, and exporters.
* Contrib: log exporters and bridge packages (e.g., Fluentd).

Baggage

* Baggage is for propagating small, application-defined key/value pairs (for example, `user.id` or `session.id`) across process boundaries.
* Pattern: API defines how to set/get baggage; SDK supports context storage and propagation; contrib supplies propagators and integrations (B3, Jaeger, W3C Trace Context).
* In many cases, built-in OTel propagators meet common baggage needs.

The common design principle

* All signals follow the same architectural pattern:
  * API = “what” the instrumentation emits (stable contract).
  * SDK = “how” telemetry is processed and delivered (runtime).
  * Contrib = ecosystem integrations and exporters.
* This separation preserves stable instrumentation while allowing flexible runtime implementations.

<Frame>
  <img alt="The image is a diagram titled &#x22;OpenTelemetry Client Architecture by Layer,&#x22; illustrating different components and layers like Traces, Metrics, Logs, and Baggage, along with their respective APIs, SDKs, and Contribs." />
</Frame>

Best practice: instrumentation libraries should depend only on the API and semantic conventions. The SDK is an implementation detail that varies by deployment. Coupling libraries to the SDK reduces portability.

<Callout icon="warning">
  Do not import or rely on SDK internals from instrumentation libraries. Instrumentation should use the OpenTelemetry API (and semantic conventions) only. The SDK can be configured by the application or platform at runtime.
</Callout>

Quizzes

1. What makes OpenTelemetry a cross-cutting concern?

* It only works with front-end code.
* It provides centralized logging only.
* It is mixed into multiple parts of the application to provide observability.
* It replaces business logic in application layers.

Answer: It is mixed into multiple parts of the application to provide observability.

Explanation: Cross-cutting concerns—like telemetry, logging, authentication, and error handling—touch multiple layers and modules rather than being confined to a single component. Observability must be present across UI, business logic, and data-access layers, so it cuts across the clean boundaries defined by Separation of Concerns.

<Frame>
  <img alt="The image is a quiz question asking what makes OpenTelemetry a cross-cutting concern, with four multiple-choice options. Option 3 is highlighted in red as the correct answer." />
</Frame>

2. Which software design principle is challenged by cross-cutting concerns like OpenTelemetry?

* Inheritance
* Separation of Concerns
* Single Responsibility Principle
* Encapsulation

Answer: Separation of Concerns.

Explanation: Cross-cutting concerns must be applied across modules and layers, which complicates strict isolation of responsibilities that Separation of Concerns aims to achieve.

<Frame>
  <img alt="The image is a quiz question asking which software design principle is challenged by cross-cutting concerns like OpenTelemetry. It provides four options: Inheritance, Separation of Concerns, Single Responsibility Principle, and Encapsulation." />
</Frame>

3. What is the main purpose of the OpenTelemetry API in the client architecture?

* To export telemetry to a vendor backend?
* To define cross-cutting interfaces and constants for instrumentation.
* To store metrics in a database.
* To monitor OpenTelemetry itself.

Answer: To define cross-cutting interfaces and constants for instrumentation.

Explanation: The API defines the contract that libraries and applications use to create telemetry in a vendor-agnostic way, keeping instrumentation stable even when the SDK or exporters change.

<Frame>
  <img alt="The image is a quiz question about the main purpose of the OpenTelemetry API in client architecture, offering four possible answers." />
</Frame>

4. Which part of the OpenTelemetry client should NOT be used inside instrumentation libraries?

* Semantic conventions
* API
* SDK
* Constants

Answer: SDK.

Explanation: Instrumentation libraries should depend only on the OpenTelemetry API (and conventions/constants). The SDK is an implementation detail and may vary by deployment; coupling libraries to the SDK reduces portability.

<Frame>
  <img alt="The image is a quiz question asking which part of the OpenTelemetry client should not be used inside instrumentation libraries, with answer options: Semantic Conventions, API, SDK, and Constants." />
</Frame>

5. Which of the following best describes the role of semantic conventions in OpenTelemetry?

* Provide a UI for visualizing telemetry
* Define standard attribute keys and values for consistent telemetry
* Authenticate telemetry between services
* Automatically deploy OTel agents

Answer: Define standard attribute keys and values for consistent telemetry.

Explanation: Semantic conventions standardize the names and meanings of attributes, metrics, and log fields so data from different services and languages can be understood and correlated consistently.

That’s it for this lesson.

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Fluentd: [https://www.fluentd.org/](https://www.fluentd.org/)
* B3 Propagation: [https://github.com/openzipkin/b3-propagation](https://github.com/openzipkin/b3-propagation)
* W3C Trace Context: [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/a8aa4a33-4e6c-4aa1-8ad4-7f1f98235b0b" />
</CardGroup>
