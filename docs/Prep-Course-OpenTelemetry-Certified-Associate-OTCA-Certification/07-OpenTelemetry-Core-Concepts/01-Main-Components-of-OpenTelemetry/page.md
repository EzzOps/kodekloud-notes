# Main Components of OpenTelemetry

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Core-Concepts/Main-Components-of-OpenTelemetry/page

Overview of OpenTelemetry components, explaining standards, APIs and SDKs, instrumentation, the Collector for processing and routing, and ecosystem tools for deploying and exporting telemetry data.

In this lesson we examine the primary components of the OpenTelemetry ecosystem from a high-level, practical perspective. OpenTelemetry standardizes how telemetry is created, transported, and processed so you can reliably instrument applications and route observability data to backends.

Understanding these layers and how they connect helps you design robust observability pipelines for traces, metrics, and logs.

## Foundational standards (what defines behavior)

These core specifications govern behavior across the OpenTelemetry ecosystem:

* [Specifications](https://opentelemetry.io/docs/reference/specification/) — Define expected behavior for APIs and SDKs (API surface, SDK responsibilities, semantics for errors and exceptions).
* [OpenTelemetry Protocol (OTLP)](https://opentelemetry.io/docs/specs/otel/otlp/) — The standard wire format and transport protocol for sending traces, metrics, and logs.
* [Semantic Conventions](https://opentelemetry.io/docs/reference/specification/semantic_conventions/) — Standard attribute names and conventions for common telemetry types (HTTP spans, database calls, resource attributes).

<Frame>
  <img alt="The image is an overview of OpenTelemetry components, highlighting Specification, OpenTelemetry Protocol (OTLP), and Semantic Conventions as key elements in defining behaviors, standards, and formats for telemetry data." />
</Frame>

## Code-level tooling (how telemetry is created)

This layer includes the libraries and runtime components you use to produce telemetry from applications:

|                                                                                                     Component | Purpose                                                                               | When to use                                                     |
| ------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
|                                                        [APIs](https://opentelemetry.io/docs/instrumentation/) | Language-specific interfaces and helpers to create spans, metrics, and logs           | When writing manual instrumentation or calling SDKs             |
|                                                        [SDKs](https://opentelemetry.io/docs/instrumentation/) | Implementations of the API that configure exporters, processors, and batching         | In your application runtime to collect and export telemetry     |
|                                   [Instrumentation libraries](https://opentelemetry.io/docs/instrumentation/) | Pre-built integrations for frameworks (e.g., Flask, Express) to minimize code changes | To quickly instrument common frameworks and libraries           |
| [Auto-instrumentation agents & wrappers](https://opentelemetry.io/docs/instrumentation/auto-instrumentation/) | Runtime agents (e.g., Java agent) that instrument apps without source changes         | For rapid deployment or when source modification is not desired |

The API and SDK are intentionally separated so instrumentation code remains stable while implementations evolve.

## Processing and routing (the Collector)

Telemetry often needs to be transformed, filtered, or routed before reaching a backend. The central component for this is:

* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) — A vendor-agnostic, configurable service that receives, processes, and exports telemetry. The Collector supports batching, retries, transformations, filtering, and multi-destination routing, and can act as a gateway between instrumented applications and backends.

> **lightbulb** The Collector centralizes processing logic (filtering, batching, and exporting), reducing the need for exporter implementations inside each application and enabling consistent telemetry handling across environments.

## Deployment, distributions, and ecosystem tooling

Beyond the core components, the OpenTelemetry ecosystem includes tools to deploy and extend your observability stack:

* Operator & deployment tools: [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator), Helm charts, and other utilities to run Collector and agents in Kubernetes and cloud environments.
* Community distributions: Project-specific or vendor-provided distributions that bundle collectors, exporters, and preconfigured pipelines.
* Integrations & platform tooling: Support for serverless platforms, CI/CD pipelines, and language-specific helpers.

After processing in the Collector (or directly from SDK exporters), telemetry is sent to one or more backends for storage, analysis, and visualization.

<Frame>
  <img alt="The image provides an overview of OpenTelemetry components, showing a flow from software systems through data generation and processing to the backend, with a focus on the OpenTelemetry Collector and supporting tools." />
</Frame>

## How the pieces fit together

* Left side (producers): Applications instrumented via APIs/SDKs, instrumentation libraries, or auto-instrumentation agents generate telemetry.
* Middle (processing): The Collector aggregates, processes, and routes telemetry—applying transformations, batching, or sampling as configured.
* Right side (consumers): Backends and observability platforms receive OTLP or other exporter data for long-term storage, querying, and visualization.

Together, these components form a consistent, extensible pipeline for generating, transporting, and processing observability data across diverse environments.

## Quick reference & further reading

* OpenTelemetry Specification: [https://opentelemetry.io/docs/reference/specification/](https://opentelemetry.io/docs/reference/specification/)
* OTLP (Protocol): [https://opentelemetry.io/docs/specs/otel/otlp/](https://opentelemetry.io/docs/specs/otel/otlp/)
* Semantic Conventions: [https://opentelemetry.io/docs/reference/specification/semantic\_conventions/](https://opentelemetry.io/docs/reference/specification/semantic_conventions/)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Instrumentation: [https://opentelemetry.io/docs/instrumentation/](https://opentelemetry.io/docs/instrumentation/)
* OpenTelemetry Operator (Kubernetes): [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/da1c735f-c606-45b0-9bbf-04fe366fbd23/lesson/47de1dd5-e85f-4612-9c7a-02c8d128de52)
