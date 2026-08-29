# Standards and Specification

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/Standards-and-Specification/page

Explains OpenTelemetry standards and specifications for interoperable, vendor neutral telemetry, covering APIs SDKs protocols semantic conventions stability and the OTEP change process.

In this lesson we cover specifications and standards in observability—why they matter, what the OpenTelemetry specification defines, how changes are proposed, and which parts are important for certification and production use.

Why do we need standards?

Telemetry is produced by applications written in many languages (C, C++, Go, Java, Python, PHP, Ruby, etc.) and consumed by varied backends (Jaeger, Prometheus, OpenSearch, Zipkin, and commercial vendors). Without a common standard, integrating each language with each backend becomes a fragile, custom effort.

OpenTelemetry solves this fragmentation by providing a vendor-neutral, language-agnostic specification plus language-specific APIs and SDKs so telemetry can be collected, correlated, and exported consistently across environments.

<Frame>
  <img alt="The image outlines the need for cross-language telemetry standards, showing various programming languages, the OpenTelemetry framework, and different observability backends. The central focus is on creating vendor or language-agnostic APIs for integration." />
</Frame>

Think of early connector ecosystems (pre-USB): without a single connector standard, device integrations were brittle. Specifications give us that common connector for telemetry—enabling interoperability across languages, frameworks, and backends.

<Frame>
  <img alt="The image explains why specifications drive consistency, highlighting two points: &#x22;Foundation for Interoperability&#x22; and &#x22;Vendor-Neutral Telemetry,&#x22; each with accompanying icons." />
</Frame>

How standards simplify observability

* Provide consistent approaches across diverse technologies and stacks.
* Prevent vendor lock-in by enabling backend swaps without re-instrumentation.
* Allow vendors to implement compatible collectors and backends that accept telemetry from any instrumented code.

OpenTelemetry defines a single, vendor-neutral specification that brings this consistency to the ecosystem.

What the OpenTelemetry specification defines

The specification is the authoritative source for how telemetry should be produced, transported, and interpreted. Core areas include APIs, SDK behaviors, data models, protocols, and conventions.

| Specification component       | Purpose / Example                                                                                                                                                                                                                      |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| APIs and SDKs                 | Definitions for capturing traces, metrics, and logs in each language (what the API surface should look like).                                                                                                                          |
| Semantic conventions          | Standard attribute names such as `http.method` or `db.system` to ensure consistent naming across spans/metrics/logs.                                                                                                                   |
| OTLP (OpenTelemetry Protocol) | Binary/JSON protocol definitions and protobufs used to transport telemetry between SDKs, collectors, and backends. See: [https://github.com/open-telemetry/opentelemetry-proto](https://github.com/open-telemetry/opentelemetry-proto) |
| Context propagation           | Rules and formats for carrying context and baggage across service boundaries to correlate telemetry.                                                                                                                                   |
| Instrumentation guidelines    | Best practices for consistent instrumentation, sampling, and attribute usage.                                                                                                                                                          |

<Frame>
  <img alt="The image presents the core structure of a specification, consisting of five components: &#x22;API and SDK,&#x22; &#x22;Semantic Conventions,&#x22; &#x22;OTLP Protocol,&#x22; &#x22;Context Propagation,&#x22; and &#x22;Instrumentation Guidelines.&#x22;" />
</Frame>

The specification is organized by signals—traces, metrics, logs—and by core components. The OpenTelemetry docs site contains the specification and a status summary showing the stability of each component.

<Frame>
  <img alt="The image shows a webpage from the OpenTelemetry documentation, specifically the specification status summary, detailing the current status of components like Tracing, with sections indicating stability levels and notes." />
</Frame>

Specification stability levels

| Level        | Description                                                      |
| ------------ | ---------------------------------------------------------------- |
| Draft        | Under active design; not part of the formal specification yet.   |
| Experimental | Released for testing; APIs/behaviors may change.                 |
| Stable       | Backward compatible and safe for production / long-term support. |
| Deprecated   | Supported for now but planned for removal in future versions.    |

You can inspect each signal’s section on the docs site to see which components are stable or experimental—for example, the tracing API is currently marked stable.

<Frame>
  <img alt="The image shows a webpage from the OpenTelemetry documentation, detailing the current status of various specifications such as Tracing and Metrics with information about stability and support." />
</Frame>

Recording exceptions in traces — a concrete spec example

The specification gives recommended patterns for common scenarios. For example, when an exception is thrown, the recommended approach is to record it as an event on the span and set the span status accordingly. Here’s the Java pattern the spec suggests:

```java theme={null}
Span span = myTracer.startSpan("operation.name");
try {
    // Code that does the actual work which the Span represents
} catch (Throwable e) {
    span.recordException(e);
    span.setAttribute(AttributeKey.stringKey("error.type"), e.getClass().getCanonicalName());
    span.setStatus(StatusCode.ERROR, e.getMessage());
} finally {
    span.end();
}
```

How to propose changes to the specification

Changes are proposed via the OpenTelemetry Enhancement Proposal (OTEP) process—an RFC-like workflow where contributors document rationale, design, and impact. Follow the repository guidance to determine whether a change needs an OTEP (new features, behavioral changes) or can be handled as a bug fix/minor clarification.

<Frame>
  <img alt="The image shows a GitHub repository page for &#x22;opentelemetry-specification&#x22; with a focus on the OpenTelemetry Enhancement Proposal (OTEP) section. It includes a list of files and a README document describing the purpose and process of OTEPs." />
</Frame>

The OTEP process documents what requires an OTEP and what does not—examples and submission guidelines live in the specification repository.

<Frame>
  <img alt="The image shows a GitHub repository page for OpenTelemetry, detailing the requirements for using an OpenTelemetry Enhancement Proposal (OTEP). It includes examples of changes that require an OTEP, like new tracer options, and changes that do not, like bug fixes." />
</Frame>

Why specifications matter

Specifications let developers instrument code consistently across languages, enable vendors to build compatible collectors and backends, and provide end users with portable telemetry pipelines that avoid vendor lock-in. This transparency is the foundation of long-term interoperability.

<Frame>
  <img alt="The image explains the importance of specifications in enabling developers to instrument code across languages, allowing vendors to build compatible collectors, and helping end-users with portable telemetry pipelines." />
</Frame>

Semantic conventions

Semantic conventions define standardized attribute names and structures (written in `YAML 1.2` and auto-generated into language constants). They ensure common attributes—like HTTP method or database system—are consistently named across spans, metrics, and logs.

Examples:

* `http.method` — standard attribute for the HTTP method.
* `db.system` — identifies the database type (for example, `mysql`, `postgresql`), not the database name.

> **lightbulb** Semantic conventions are the reason instrumentation libraries across languages can reliably set and query attributes without name collisions or ambiguity.

<Frame>
  <img alt="The image explains consistent attributes with semantic conventions defined in YAML 1.2, featuring examples like &#x22;http.method&#x22; used in HTTP spans, metrics, and logs, and &#x22;db.system&#x22; identifying database types such as MySQL and PostgreSQL." />
</Frame>

Exam-relevant specification topics

For the OTCA exam and practical implementation, focus on these specification topics:

| Topic                     | What to study                                                                    |
| ------------------------- | -------------------------------------------------------------------------------- |
| API vs SDK                | Responsibilities of the API surface vs runtime SDK implementations.              |
| Signals                   | Separate spec sections and behaviors for Tracing, Metrics, Logs.                 |
| Data models               | How spans, metrics, and logs are modeled and represented.                        |
| Context propagation       | Baggage, trace context formats, cross-process propagation rules.                 |
| Composability & extension | SDK design, plugins, and extension points (collectors/plugins).                  |
| Configuration             | Environment variables, config model, and standard settings.                      |
| Agents and Collectors     | Collector architecture, receivers, exporters, and pipeline design.               |
| Versioning & stability    | Understanding stable/experimental/deprecated components and compatibility rules. |

<Frame>
  <img alt="The image outlines four core specification topics for the OTCA Exam: API and SDK, Signals, Data Models, and Context Propagation, each with a brief description." />
</Frame>

<Frame>
  <img alt="The image lists core specifications for OTCA exam topics, focusing on &#x22;Composability and Extension,&#x22; &#x22;Configuration,&#x22; and &#x22;Agents,&#x22; with brief descriptions for each." />
</Frame>

Spec versioning and compatibility

Each spec component is versioned to indicate its stability and compatibility guarantees. For production, prefer stable components; experimental components are intended for evaluation and may change.

<Frame>
  <img alt="The image illustrates &#x22;Spec Versioning and Stability&#x22; with tags indicating statuses: &#x22;Stable,&#x22; &#x22;Experimental,&#x22; and &#x22;Deprecated,&#x22; highlighting their reliability for production and likelihood of changes. It emphasizes that specification stability ensures long-term compatibility." />
</Frame>

> **warning** Do not rely on experimental components for critical production paths—experimental APIs or behaviors can change and may require rework.

Summary

OpenTelemetry is more than a collection of libraries—it's an open, transparent specification that provides long-term standards for telemetry. Signals, APIs, SDKs, the telemetry data model, OTLP, and semantic conventions together enable interoperable, vendor-neutral observability.

<Frame>
  <img alt="The image is a summary slide about OpenTelemetry, highlighting its specifications, the importance of transparent standards, and key components like signals and APIs." />
</Frame>

Links and references

* OpenTelemetry docs: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
* Specification repo & OTEPs: [https://github.com/open-telemetry/opentelemetry-specification/tree/main/oteps](https://github.com/open-telemetry/opentelemetry-specification/tree/main/oteps)
* OTLP proto repo: [https://github.com/open-telemetry/opentelemetry-proto](https://github.com/open-telemetry/opentelemetry-proto)
* YAML 1.2 spec: [https://yaml.org/spec/1.2/spec.html](https://yaml.org/spec/1.2/spec.html)

Study these resources and focus on stable spec components for production readiness and exam preparation.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/a7472e8e-99c8-4498-9542-970b44d258bb)
