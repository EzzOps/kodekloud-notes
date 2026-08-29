# OpenTelemetry Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-Introduction/page

OpenTelemetry is a vendor-neutral observability framework unifying instrumentation, collection, processing, and export of metrics, traces, and logs across languages and backends.

Now that you have a basic understanding of what OpenTelemetry is, let’s examine the historical context that motivated its creation and why it matters for observability today.

Historically, software systems emitted telemetry—metrics, traces, and logs—to a variety of observability backends. There were many open-source projects (for example, [Prometheus](https://prometheus.io), [Jaeger](https://www.jaegertracing.io), [Zipkin](https://zipkin.io)) and numerous vendor-specific platforms. To send telemetry from an application to a backend, teams typically installed and configured an agent or exporter tailored to that backend. The result was many backends, many agents, and many formats—no single, shared standard.

<Frame>
  <img alt="The image illustrates the lack of a shared standard in observability, showing how software systems, agents, and observability backends like Prometheus and Jaeger are interconnected without a unified approach." />
</Frame>

This “multiple connectors” problem is similar to the old era of device cables: laptops, tablets, external HDDs, iOS and Android phones all used different connectors (USB-A, USB-B, USB-C, Lightning, COM ports, etc.). Each connector did the same basic job—connect devices—but the ecosystem lacked a single, common interface.

<Frame>
  <img alt="The image illustrates the problem of multiple incompatible connector types for devices like laptops, tablets, external HDDs, iOS, and Android phones." />
</Frame>

Early efforts to standardize telemetry included two complementary projects: [OpenTracing](https://opentracing.io) and [OpenCensus](https://opencensus.io). OpenTracing focused on distributed tracing (spans and context propagation), while OpenCensus provided libraries for both metrics and traces with built-in exporters. Although each project advanced observability, their overlap left gaps in signal coverage and led to competing standards rather than a single, consistent approach.

<Frame>
  <img alt="The image illustrates early standardization attempts with OpenTracing and OpenCensus connecting software systems to observability backends like Prometheus and Jaeger. It highlights that two standards still did not equate to a unified standard." />
</Frame>

In response, the maintainers of OpenTracing and OpenCensus merged efforts in 2019 to form OpenTelemetry. Today OpenTelemetry is a Cloud Native Computing Foundation (CNCF) project that combines the best ideas from both predecessors into a single, vendor-neutral, language-agnostic specification and set of libraries. If you still use OpenTracing or OpenCensus, [migration guides are available](https://opentelemetry.io/docs/migration/) to help move to OpenTelemetry.

OpenTelemetry is a standard and framework—not a storage or visualization backend. It defines how telemetry signals (metrics, traces, logs) are instrumented, collected, processed, and exported. Using OpenTelemetry (OTel), you can route telemetry to any backend of your choice; the project does not provide long-term storage or dashboards itself.

<Frame>
  <img alt="The image illustrates OpenTelemetry as a standard for collecting and exporting telemetry data, showing its connection between software systems and observability backends like Prometheus and Jaeger. It also notes that OpenTelemetry is not an observability backend itself." />
</Frame>

Think of OpenTelemetry like a universal connector (similar to USB-C in the device world): a single, consistent interface to collect telemetry across many languages, platforms, and backend targets.

<Frame>
  <img alt="The image compares multiple types of connectors on the left with a single unified connector on the right, suggesting a standard interface for observability across various devices." />
</Frame>

Definition

OpenTelemetry is an open-source observability framework that provides standard APIs, SDKs, and tools to instrument, collect, process, and export metrics, traces, and logs from applications and services across multiple programming languages.

<Frame>
  <img alt="The image is a presentation slide about OpenTelemetry, describing it as an open-source observability framework that provides APIs, SDKs, and tools for collecting and exporting metrics, traces, and logs." />
</Frame>

A few clarifications about terminology and scope

* The common short form used in the ecosystem is OTel (short for OpenTelemetry). Avoid ambiguous acronyms like OT by themselves.
* OpenTelemetry supports many programming languages, including Java, Node.js, .NET, Go, and Python; language support varies by SDK maturity and version.
* OTel can export telemetry to open-source backends ([Prometheus](https://prometheus.io), [Jaeger](https://www.jaegertracing.io), [Zipkin](https://zipkin.io)) or to commercial observability platforms—there is no vendor lock-in.
* OpenTelemetry itself does not store or visualize data; it supplies instrumentation, SDKs, collectors, and exporters so you can pick the storage and visualization solution that fits your needs.

<Callout icon="lightbulb">
  OpenTelemetry is a vendor-neutral framework for collecting telemetry—it is not a storage or visualization backend. Use OTel to instrument applications and route data to the backend of your choice.
</Callout>

Key characteristics

<Frame>
  <img alt="The image illustrates the key characteristics of OpenTelemetry, highlighting features such as being vendor-neutral and open-source, language-agnostic, portable, and compatible with any backend." />
</Frame>

|     Characteristic | What it means                                                                                                                     |
| -----------------: | --------------------------------------------------------------------------------------------------------------------------------- |
|     Vendor-neutral | Designed to avoid vendor lock-in; works with many backend providers.                                                              |
|        Open source | Community-driven project under CNCF governance.                                                                                   |
|  Language-agnostic | SDKs and APIs for languages including Java, Node.js, .NET, Go, Python, and more.                                                  |
|           Portable | Instrumentation can be used across on-prem, cloud, and hybrid environments.                                                       |
|           Flexible | Supports metrics, traces, and logs with customizable processors, samplers, and exporters.                                         |
| Backend-compatible | Exporters and the OpenTelemetry Collector let you route data to Prometheus, Jaeger, Zipkin, commercial APMs, or custom pipelines. |

Summary

Telemetry used to be fragmented across multiple tools and exporters. OpenTracing and OpenCensus improved interoperability, but overlap remained. Their merger in 2019 produced OpenTelemetry—a unified, community-driven standard backed by major cloud and observability vendors. OpenTelemetry provides consistent APIs, SDKs, and tooling for instrumenting and exporting telemetry, enabling flexible observability without vendor lock-in.

<Frame>
  <img alt="The image is a summary of the evolution of telemetry, highlighting its initial fragmentation, efforts by OpenTracing and OpenCensus to standardize it, and their eventual merger into OpenTelemetry for a unified approach." />
</Frame>

<Frame>
  <img alt="The image is a summary slide outlining key points about OpenTelemetry, highlighting it as a vendor-neutral framework for telemetry and emphasizing its consistent, flexible observability without vendor lock-in." />
</Frame>

That concludes this lesson.

Links and references

* OpenTelemetry project: [https://opentelemetry.io](https://opentelemetry.io)
* OpenTelemetry migration guides: [https://opentelemetry.io/docs/migration/](https://opentelemetry.io/docs/migration/)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* Jaeger: [https://www.jaegertracing.io](https://www.jaegertracing.io)
* Zipkin: [https://zipkin.io](https://zipkin.io)
* CNCF: [https://www.cncf.io](https://www.cncf.io)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/73f40b03-85d2-4492-b99a-10cd80d62cb7" />
</CardGroup>
