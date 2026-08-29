# OpenTelemetry Goals Mission Vision and Values

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/OpenTelemetry-Goals-Mission-Vision-and-Values/page

Overview of OpenTelemetry’s goals, mission, vision, and values for unified, portable, low-overhead application telemetry

In this lesson we explain OpenTelemetry’s goals, mission, vision, and engineering values so you can understand the project’s direction and how it fits into a modern observability strategy. Knowing these fundamentals makes it easier to adopt OpenTelemetry consistently across teams and platforms and helps you decide where and how to integrate telemetry into your architecture.

Why this matters: unifying telemetry reduces duplicated effort, improves interoperability across languages and tools, and enables faster incident detection and resolution.

## Goal: Make instrumentation easy, consistent, and universal

OpenTelemetry’s primary goal is to simplify application instrumentation across languages and environments (Java, Python, Node.js, containers, serverless, etc.). The project provides APIs, SDKs, and auto-instrumentation libraries so developers don’t have to build bespoke instrumentation for each platform.

<Frame>
  <img alt="The image outlines the goal of OpenTelemetry, focusing on making instrumentation easy, consistent, and universal, with a diagram showing various programming environments like Java, Python, Node.js, and Containers connecting to an Instrumentation Layer." />
</Frame>

OpenTelemetry focuses on generating telemetry—traces, metrics, and logs—and exporting it to the backend of your choice. It is not a storage or visualization layer; those responsibilities belong to the observability backend you select (for example, commercial APMs or open-source platforms).

> **lightbulb** OpenTelemetry provides APIs, SDKs, auto-instrumentation libraries, and the Collector for generating and exporting telemetry. Storage and visualizations are handled by your chosen observability backend.

## Mission: Enable effective observability with high-quality, portable telemetry

The mission is to make high-quality, portable telemetry ubiquitous so teams can achieve effective observability. Portable telemetry means data is consistent and usable across tools and vendors—so you can change backends without losing signal fidelity.

<Frame>
  <img alt="The image features a mission statement about enabling effective observability with high-quality telemetry, alongside a globe graphic with connected user icons." />
</Frame>

Focus areas for the mission:

* Consistent semantic conventions and signal formats.
* Portable instrumentation that works across languages and platforms.
* High signal quality so telemetry is actionable for debugging, SLOs, and capacity planning.

## Vision: How telemetry should work in practice

OpenTelemetry’s vision is about the practical experience for developers and operators:

* Easy to adopt with fast time to value and sensible defaults.
* Universal: unified protocols and conventions across signals and languages.
* Vendor-neutral: freedom to choose or switch observability backends.
* Composable: use only the components you need—the in-app SDKs, auto-instrumentation, and/or the Collector.

<Frame>
  <img alt="The image outlines a vision for telemetry to be easy, universal, and vendor-neutral, emphasizing fast implementation, unified protocols, and freedom from vendor lock-in." />
</Frame>

Practical note: you can mix and match components. For simple setups, use SDKs that export directly to your backend. For advanced routing, enrichment, sampling, or protocol translation, route telemetry through the OpenTelemetry Collector.

## Why built-in telemetry matters

Telemetry should be a first-class engineering concern: available early, native to the application lifecycle, and consistent across services. Treating telemetry as a foundational part of development reduces fragmentation, accelerates troubleshooting, and prevents costly rework.

<Frame>
  <img alt="The image explains the importance of consistent telemetry for observability, and mentions that OpenTelemetry helps teams achieve this without custom instrumentation. It features a target and arrow graphic alongside the text." />
</Frame>

Benefits of built-in telemetry:

* Faster incident detection and root-cause analysis
* Consistent metrics and trace context across services
* Easier onboarding for new teams and tools

## Engineering values that guide OpenTelemetry

OpenTelemetry is guided by several engineering principles that shape design and implementation choices:

* Compatibility: follow open standards and ensure interoperability with multiple backends and protocols.
* Stability: maintain stable APIs and backward compatibility to protect integrations.
* Resilience: minimize data loss and ensure instrumentation does not cause application failures.
* Performance: keep telemetry overhead very low so instrumentation does not degrade application performance.

<Frame>
  <img alt="The image presents three engineering values: Compatibility, Stability, and Resilience, each with a brief description and icon representing follow standards, API stability, and handling failure gracefully." />
</Frame>

> **warning** When adding telemetry to production systems, prioritize safe defaults and low overhead. Instrumentation must not cause application instability or unacceptable performance regressions.

## Recap: Goals, Mission, Vision, and Values (Quick Reference)

| Area               | Purpose                                                              | Key takeaway                                             |
| ------------------ | -------------------------------------------------------------------- | -------------------------------------------------------- |
| Goal               | Simplify and unify instrumentation across languages and platforms    | Make telemetry easy, consistent, and universal           |
| Mission            | Produce high-quality, portable telemetry for effective observability | Telemetry should be useful across tools and environments |
| Vision             | How telemetry should feel and be composed in practice                | Easy adoption, vendor-neutral, and composable components |
| Engineering values | Design principles for implementation                                 | Compatibility, stability, resilience, and performance    |

<Frame>
  <img alt="The image is a summary slide for OpenTelemetry, highlighting its goals to simplify instrumentation, provide consistent and vendor-neutral telemetry data, and reduce engineering burden." />
</Frame>

In practice, many popular libraries and frameworks (for example, web frameworks and common HTTP client libraries) already provide OpenTelemetry instrumentation integrations. Often you can start collecting telemetry by enabling or adding these libraries and configuring an exporter or Collector.

<Frame>
  <img alt="The image is a summary slide with points highlighting the ease, universality, and engineering values of OpenTelemetry, emphasizing compatibility, stability, resilience, and performance." />
</Frame>

OpenTelemetry aims to make telemetry built-in, consistent, and effortless so teams can achieve observability without the burden of custom, platform-specific instrumentation.

## Links and References

* OpenTelemetry official site: [https://opentelemetry.io/](https://opentelemetry.io/)
* OpenTelemetry GitHub: [https://github.com/open-telemetry](https://github.com/open-telemetry)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Instrumentation libraries and language guides: [https://opentelemetry.io/docs/instrumentation/](https://opentelemetry.io/docs/instrumentation/)

Thank you for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/57d103bc-7e92-4e08-b14f-5ae839871731)
