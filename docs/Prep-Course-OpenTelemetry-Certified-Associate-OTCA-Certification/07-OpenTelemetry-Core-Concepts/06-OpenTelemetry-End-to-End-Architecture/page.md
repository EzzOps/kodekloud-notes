# Set up a TracerProvider
trace.set_tracer_provider(TracerProvider())

# Add a Console Exporter (prints spans to stdout)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Get a tracer
tracer = trace.get_tracer(__name__)

# Create a span
with tracer.start_as_current_span("my-first-span"):
    print("Inside the span")

print("Done")
```

This article explains why clients are designed this way so you can use them safely and extend them when needed.

## Core design goals

OpenTelemetry clients are designed around three high-level principles:

* Easy to use — minimal effort required to add telemetry to applications.
* Uniform — consistent APIs across languages to reduce cognitive load for adopters.
* Flexible — support a variety of runtime use cases and backends.

<Frame>
  <img alt="The image illustrates the design principles for OpenTelemetry clients, highlighting that they must be easy to use, uniform, and flexible, represented in a Venn diagram." />
</Frame>

Clients aim to deliver two practical capabilities:

* Full features out of the box — basic telemetry generation, batching, and export should work without custom implementation.
* Extensibility — you can customize exporters, sampling, processors, and experiment safely without touching core behavior.

<Frame>
  <img alt="The image outlines OpenTelemetry Client Design Principles, highlighting full features availability and support for extensibility to foster innovation and experimentation." />
</Frame>

## API vs SDK — the fundamental separation

The OpenTelemetry specification enforces a clear separation of concerns:

* API: stable, language-level interfaces used by instrumentations and application code to generate telemetry.
* SDK: the pluggable runtime that implements sampling, processing, batching, and exporting.

Key requirements driven by this separation:

* Third-party libraries should depend only on the API, not on any specific SDK.
* Final application owners choose whether to include an SDK or which SDK/distribution to use.
* Instrumented libraries must behave correctly even if no SDK is present — relying solely on API behavior keeps them resilient.

<Frame>
  <img alt="The image outlines four requirements for client design in the context of OpenTelemetry, focusing on API definition, third-party library dependencies, application developer choices, and functionality of instrumented libraries." />
</Frame>

<Callout icon="lightbulb">
  Keep instrumentation dependent only on the API. This enables swapping SDKs or running with no SDK without breaking instrumented libraries.
</Callout>

## SDK responsibilities and exporters

SDKs implement protocol-independent runtime behaviors such as batching, queuing, retry logic, and sampling. Exporters are protocol- or backend-specific components that send telemetry to external systems.

Common exporters and uses:

* OTLP: a common protocol to communicate with collectors and backends (see the OpenTelemetry proto definitions).
* Jaeger, Zipkin: tracing backends with their specific formats.
* Prometheus: metrics scraping and exposition.
* Console exporters: quick debugging or development.
* In-memory/mock exporters: unit and integration tests.

Vendor-specific exporters should be kept separate from the core clients (provided in vendor distributions or contrib packages).

<Frame>
  <img alt="The image lists requirements for client design, focusing on SDK separation, included exporters, and keeping vendor-specific exporters separate in the context of OpenTelemetry." />
</Frame>

## Modular client layout

OTel clients are typically modularized per signal (traces, metrics, logs). Each signal usually exposes four packages/modules:

* API — public interfaces, types, and constants used by instrumentation.
* SDK — the runtime implementation offering configuration and pluggable components.
* Semantic Conventions — a catalog of recommended attribute names and conventions.
* Contrib — community-maintained integrations and auto-instrumentation plugins.

<Frame>
  <img alt="The image explains the modular design of OpenTelemetry clients, showing how each signal is divided into four packages: API, SDK, Semantic Conventions, and Contrib." />
</Frame>

Contrib packages are where community-driven instrumentation and integrations live (for example, Flask instrumentation for Python). They simplify adoption by providing ready-made instrumentations for popular frameworks.

## How clients fit into an observability architecture (example: Kubernetes)

Typical data flow and responsibilities:

* Application code uses the API to create telemetry.
* SDKs handle sampling, processing, and exporting inside the application or service.
* The OpenTelemetry Collector receives telemetry from one or more sources, transforms it, and forwards it to external backends.
* In Kubernetes, the OTel Operator automates deployment and scaling of Collectors.

This layered separation enables independent evolution and replacement of any layer.

<Frame>
  <img alt="The image is a diagram showing how each layer of the OpenTelemetry (OTel) system works independently, highlighting the roles of applications, SDKs, collectors, and operators." />
</Frame>

In practice, most deployments combine API + SDK + Collector; Kubernetes users commonly add the Operator to manage Collector lifecycle.

## Quick recap: components and what they do

* API — how telemetry is generated and instrumented in your code.
* SDK — runtime logic: sampling strategy, batching, processing, exporting.
* Instrumentation libraries — automatic instrumentation for frameworks (e.g., Flask, Spring).
* Distributions — vendor-provided packaging and opinionated defaults for upstream OTel components (not forks).

<Frame>
  <img alt="The image is a table outlining OpenTelemetry components and their roles, such as API, SDK, Instrumentation Libraries, and Distributions, with corresponding purposes." />
</Frame>

Note: distributions are not forks. A distribution packages upstream OTel components with vendor- or community-specific defaults, integrations, or configuration.

<Frame>
  <img alt="The image shows the OpenTelemetry Ecosystem page with a list of sections like &#x22;Demo,&#x22; &#x22;Registry,&#x22; &#x22;Adopters,&#x22; and &#x22;Vendors,&#x22; detailing components and integrations." />
</Frame>

Other components worth knowing:

* Exporters — adapters that connect telemetry to a backend.
* Collector — a centralized component to receive, transform, and export telemetry from multiple sources.
* Operator — a Kubernetes-native controller to manage Collector deployments.

These design decisions and terminology appear throughout the official OpenTelemetry documentation and are commonly tested in certification exams and interviews: see the OpenTelemetry docs for detailed guidance and references.

## Registry, contrib, and distributions

The OpenTelemetry registry lists instrumentation libraries and contrib packages (for example, Flask instrumentation points to the `opentelemetry-python-contrib` repo and Flask tracing integration).

<Frame>
  <img alt="The image shows the OpenTelemetry Registry web page allowing users to search for libraries and tools, with a search result for &#x22;Flask Instrumentation&#x22; highlighted, which is related to tracking web requests in Flask applications." />
</Frame>

Distributions (vendor or community curated) are documented along with guidance on types and how to create one. Examples include AWS Distro for OpenTelemetry, Azure Distro, and other vendor-maintained packages.

<Frame>
  <img alt="The image shows a webpage from the OpenTelemetry documentation discussing distributions, including types like &#x22;Pure,&#x22; &#x22;Plus,&#x22; and &#x22;Minus,&#x22; along with guidance on creating a distribution." />
</Frame>

The OpenTelemetry site maintains a list of third-party distributions and clearly states it does not endorse any specific distribution; the page documents who maintains each distribution.

<Frame>
  <img alt="The image displays a webpage from the OpenTelemetry site, listing third-party distributions with links for various programming languages like .NET, Go, Java, and more. There's a disclaimer at the top indicating that OpenTelemetry does not endorse these distributions." />
</Frame>

The ecosystem page also lists many observability backends and vendors that natively support OpenTelemetry and the OTLP protocol; this is a non-exhaustive catalog of organizations offering and consuming OTel data.

<Frame>
  <img alt="The image shows a webpage listing vendors that support OpenTelemetry, including a table with organizations and information about their open-source status and support for native OTLP." />
</Frame>

## References and further reading

* OpenTelemetry official docs: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OpenTelemetry Registry: [https://opentelemetry.io/registry/](https://opentelemetry.io/registry/)
* OTel Operator: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)

That concludes this lesson on OpenTelemetry client design principles. Use the API for instrumentation, select the SDK or distribution that fits your deployment needs, and prefer the Collector when you need central processing, transformation, or cross-service telemetry routing.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/e6689d1f-364b-465e-b79a-ea2967614616" />
</CardGroup>


# OpenTelemetry End to End Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-End-to-End-Architecture/page

Overview of OpenTelemetry end-to-end architecture, detailing APIs, SDKs, Collector, integrations, and signal flow for traces, metrics, and logs to observability backends.

Hello, Signal Seekers.

In this lesson we map how all core OpenTelemetry (OTel) parts fit together: how the API defines telemetry creation, how language SDKs process and export it, how the Collector centralizes and enriches it, and how Kubernetes/FaaS integrations and distributions complete the pipeline. By the end you’ll understand the end-to-end journey of traces, metrics, and logs from application code to an observability backend.

## High-level overview

OpenTelemetry provides a vendor-agnostic, modular stack for telemetry collection:

* The OpenTelemetry specification defines semantic conventions and signal formats.
* OpenTelemetry APIs expose language-level contracts for creating traces, metrics, and logs, and for context propagation.
* Language SDKs implement the APIs and handle sampling, batching, resource detection, processing, and exporting.
* The OpenTelemetry Collector aggregates telemetry from many sources, performs transformations, and forwards data to one or more backends.
* Kubernetes and FaaS integrations make instrumentation and Collector deployment practical in cloud-native environments.
* Observability backends store, visualize, and analyze telemetry data.

This architecture decouples application instrumentation from backend choices and enables consistent signal processing and enrichment.

## OpenTelemetry APIs

The APIs are the lightweight contracts you call from your code. They define how telemetry is created and how context is propagated, but they do not implement runtime behavior.

Core API components:

* Tracing API: `Tracer`, `Span` — create and manage spans and context.
* Metrics API: `Meter`, Instruments — create instruments and record measurements.
* Logging API: `Logger`, `LogRecord` — create and emit structured log records.
* Propagators — encode/decode context across process boundaries (for example, W3C Trace Context headers).
* Semantic conventions — standardized attribute names such as `service.name`, `http.method`, and `db.system`.

<Callout icon="lightbulb">
  Semantic conventions enable consistent attribute naming across languages and libraries so telemetry from different sources can be correlated more easily.
</Callout>

## The SDKs (language implementations)

SDKs implement the APIs and provide runtime behavior: providers, processors, exporters, and resource detection. Each language (Java, Python, Go, JavaScript, etc.) has its own SDK implementation.

Table — SDK core components and responsibilities

| Component                                           | Purpose                                              | Example / Notes                                           |
| --------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| `TracerProvider`, `MeterProvider`, `LoggerProvider` | Factories for creating Tracers, Meters, and Loggers  | Configure global providers at app startup                 |
| Resource detectors                                  | Auto-attach environment attributes to telemetry      | Detect `service.name`, container/host IDs, cloud metadata |
| Span/Log processors & metric pipelines              | Control batching, synchronous export, and processing | `BatchSpanProcessor`, custom attribute filtering          |
| Exporters                                           | Send telemetry to Collector or backend               | OTLP, Jaeger, Zipkin, Prometheus exporters                |

Use SDK configuration to control sampling, batching, and export behavior close to the application.

## Tracing: components and flow

Tracing signal flow in an instrumented app:

* Tracer: used by application code to create spans.
* Span: unit of work representing an operation; spans form a distributed trace.
* SpanProcessor: receives ended spans and controls export behavior.
  * `SimpleSpanProcessor` — forwards spans immediately (low latency, no batching).
  * `BatchSpanProcessor` — buffers spans and exports in batches (recommended for production).
* Exporters: transport spans to a Collector or backend (OTLP, Jaeger, Zipkin).
* Samplers: decide which traces are recorded/exported:
  * `AlwaysOn`, `AlwaysOff`
  * `ParentBased`
  * `TraceIdRatioBased` (probabilistic sampling)
* Resource detectors: attach attributes like `service.name`, `service.version`, host/container identifiers.

Best practice: use batch processing in production and tune sampling to balance signal quality versus cost.

## Metrics: components and flow

Metrics provide aggregated, numeric insights about your system. Key concepts:

* `MeterProvider` — factory for `Meter` instances.
* `Meter` — used to create instruments.
* Instruments — types of measures you record:
  * `Counter`, `UpDownCounter`, `Histogram`, `ObservableCounter`, `ObservableGauge`, etc.
* Measurements — recorded data points produced by instruments.
* Views & Aggregations:
  * Views allow you to reconfigure aggregation, rename instruments, or drop attributes without changing application code.
  * Aggregators produce output such as sums, last-values, or histogram buckets.
* Exporters — send metric data (often via OTLP) to a Collector or backend.

Table — Common metric instruments

| Instrument        | Use case                                               |
| ----------------- | ------------------------------------------------------ |
| `Counter`         | Increment-only measurements (requests served)          |
| `UpDownCounter`   | Counters that can go up and down (current concurrency) |
| `Histogram`       | Distribution of values (latency)                       |
| `ObservableGauge` | Poll-based, gauge-style values (current memory)        |

Views are powerful for controlling cardinality and aggregation strategy without redeploying code.

## Logging: components and flow

Logging in OpenTelemetry focuses on structured logs and consistent resource attachment:

* `LoggerProvider` — factory for creating `Logger` instances.
* `Logger` — used by application code to create `LogRecord`s.
* `LogRecord` — structured log: message, severity, attributes, timestamp.
* Log processors — batch and process log records similar to span processors.
* Log exporters — OTLP or backend-specific exporters to send logs to a Collector or backend.
* Resource detectors attach the same resource attributes (e.g., `service.name`) to logs.

Structured logs plus resource attributes and trace correlation improve searchability and context in backends.

## OpenTelemetry Collector

The OpenTelemetry Collector is a standalone, vendor-agnostic service that centralizes telemetry processing and forwarding. It decouples SDKs from backend configurations and enables powerful, reusable pipelines.

Collector architecture:

* Receivers — accept telemetry from SDKs or other systems (examples: `otlp`, Jaeger, Zipkin, Prometheus).
* Processors — transform, filter, sample, or enrich telemetry (examples: `batch`, `attributes`, `memory_limiter`, `probabilistic_sampler`).
* Exporters — forward processed telemetry to backends or other collectors (examples: `otlp`, `prometheusremotewrite`, vendor exporters).
* Service / pipelines — configuration that wires receivers → processors → exporters.

Table — Collector building blocks

| Role      | Examples                                       | Purpose                                        |
| --------- | ---------------------------------------------- | ---------------------------------------------- |
| Receiver  | `otlp`, Jaeger, Zipkin, Prometheus             | Ingest telemetry from SDKs and systems         |
| Processor | `batch`, `attributes`, `probabilistic_sampler` | Enrich, filter, sample, or limit data          |
| Exporter  | `otlp`, `prometheusremotewrite`, vendor        | Send telemetry to backends or other collectors |

<Callout icon="lightbulb">
  Use the Collector to centralize configuration, reduce per-host resource usage, and perform transformations such as sampling, redaction, and enrichment before sending data to backends.
</Callout>

Benefits of the Collector:

* Centralized sampling and enrichment policies.
* Reduced SDK footprint (send to Collector instead of many backends).
* Consistent processing across languages and environments.

## Kubernetes integration

OpenTelemetry is designed for cloud-native environments and integrates with Kubernetes:

* Helm charts for deploying the Collector and related components.
* OpenTelemetry Operator: manages Collector instances and generates Collector configs from CRDs.
* Collector deployment patterns: DaemonSet (per-node), Deployment (shared), sidecar (per-pod) depending on collection needs.

These tools simplify lifecycle management and consistent configuration at scale.

## Functions as a Service (FaaS)

OpenTelemetry supports serverless environments (AWS Lambda, Azure Functions, Google Cloud Functions):

* Use lightweight SDKs or proxy/Collector approaches to minimize cold-start impact.
* Configure propagators to ensure context flows across invocations and downstream services.
* Ensure exporters or the Collector are reachable from the execution environment, and securely provide credentials.

Practical tip: prefer minimal in-function processing and use a network-accessible Collector or proxy to avoid increased cold-start times.

## Distributions

There are multiple OpenTelemetry distributions—vendor or community-maintained packages that bundle the Collector, processors, exporters, and opinionated defaults. Distributions can provide optimized pipelines, extra processors, or backend-specific exporters.

When choosing a distribution, evaluate:

* Included processors and exporters
* Security and compliance features
* Maintenance and upgrade path

## Putting it all together

End-to-end telemetry flow:

1. Application code calls the OpenTelemetry APIs (Tracing, Metrics, Logging).
2. Language SDKs implement the APIs: apply sampling, batching, resource detection, and processors.
3. SDK exporters send telemetry to the OpenTelemetry Collector or directly to a backend.
4. The Collector receives telemetry via receivers, processes it (processors), and exports it (exporters) to one or more backends or other collectors.
5. Kubernetes Operator/Helm charts and FaaS integrations help deploy and configure SDKs and Collectors in cloud-native environments.
6. Observability backends receive, store, and visualize telemetry for querying and analysis.

<Callout icon="warning">
  Carefully choose sampling and aggregation strategies. Aggressive sampling or overly coarse Views can lose important signals; overly fine-grained telemetry increases cost and cardinality. Tune sampling, Views, and collectors to match your observability goals and budget.
</Callout>

## Links and references

* OpenTelemetry Specification: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OpenTelemetry Operator: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Zipkin: [https://zipkin.io/](https://zipkin.io/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)

That’s the OpenTelemetry end-to-end architecture. This overview should give you a clear mental model of the components involved and how traces, metrics, and logs flow from application APIs through SDKs and the Collector into your observability backend.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/b4609151-d001-40a6-a5e8-ac1f6e6165a8" />
</CardGroup>
