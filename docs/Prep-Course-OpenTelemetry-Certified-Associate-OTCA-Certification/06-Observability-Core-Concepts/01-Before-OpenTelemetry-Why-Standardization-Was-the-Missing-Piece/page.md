# config.yaml (conceptual)
receivers: {…}
processors: {…}
exporters: {…}
connectors: {…}
service:
  extensions: [...]
  pipelines:
    traces|metrics|logs:
      receivers: [...]
      processors: [...]
      exporters: [...]
```

> **lightbulb** Minimal required components for a running pipeline are a receiver and an exporter. If `service.pipelines` is present, each pipeline must reference the relevant receivers and exporters.

## Minimal valid configuration

The smallest working Collector config needs a receiver to ingest data and an exporter to send it out. The following diagram shows a minimal pipeline: receiver → service.pipeline → exporter.

<Frame>
  <img alt="The image shows a minimal, valid pipeline diagram with components labeled &#x22;Receivers,&#x22; &#x22;Exporters,&#x22; and &#x22;service.pipeline,&#x22; sequentially connected with arrows." />
</Frame>

Example: a simple OTLP gRPC receiver on port 4317 and a `debug` exporter that prints incoming spans to the console.

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

exporters:
  debug: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: []
      exporters: [debug]
```

This configuration omits processors; the `debug` exporter is useful for testing because it logs the telemetry it receives.

## Adding processors and extensions

Processors sit in pipelines to modify, filter, or batch telemetry. Extensions run outside pipelines and provide auxiliary features such as health checks and debugging pages.

Example adding a `batch` processor and two extensions (`health_check`, `zpages`):

```yaml theme={null}
processors:
  batch: {}

extensions:
  health_check: {}
  zpages: {}

service:
  extensions: [health_check, zpages]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
```

The `batch` processor accumulates telemetry to improve throughput and reduce exporter load.

## Multiple instances and pipelines

You can declare multiple instances of a component (different names) and multiple pipelines — even multiple pipelines for the same signal type. This enables routing telemetry to different backends or applying distinct processing.

Example: two OTLP receivers on different ports, each routed to a different trace pipeline and exporter.

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
  otlp/ingest2:
    protocols:
      grpc: { endpoint: 0.0.0.0:55690 }

exporters:
  otlp:
    endpoint: backend-1:4317
  otlp/alt:
    endpoint: backend-2:4317

processors:
  batch: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
    traces/2:
      receivers: [otlp/ingest2]
      processors: [batch]
      exporters: [otlp/alt]
```

Notes:

* `otlp` and `otlp/ingest2` are distinct receiver instances.
* `traces` and `traces/2` are independent trace pipelines.
* Reusing a processor (like `batch`) across pipelines is common.

## Connectors: cross-pipeline flows

Connectors act as an exporter on one side and a receiver on the other, enabling telemetry conversion or flow between pipelines without an external process. This is useful for generating metrics from traces, for example.

Example: count span events from production spans and expose them as a metric via a connector named `count`.

```yaml theme={null}
connectors:
  count:
    spanevents:
      my.prod.event.count:
        description: Count of span events from prod
        conditions:
          - 'attributes["env"] == "prod"'

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: []
      exporters: [count]   # connector acts as an exporter for traces

    metrics:
      receivers: [count]  # connector acts as a receiver for metrics
      processors: []
      exporters: [debug]
```

How it works:

* The `count` connector inspects spans in the traces pipeline and applies the condition `attributes["env"] == "prod"`.
* When a span matches, it emits a metric named `my.prod.event.count`.
* The metrics pipeline receives that metric via the `count` receiver and exports it (here, to `debug`).

## Splitting configuration across files and parameterizing

The Collector supports including and merging multiple YAML files. Use `${file:...}` to include files and `${env:VAR:-default}` for environment variable substitution. This pattern helps keep sensitive or environment-specific settings separate.

Main `config.yaml` example:

```yaml theme={null}
# config.yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }

exporters: ${file:exporters.yaml}

service:
  extensions: []
  pipelines:
    traces:
      receivers: [otlp]
      processors: []
      exporters: [otlp]
```

Included `exporters.yaml` example:

```yaml theme={null}
# exporters.yaml
otlp:
  endpoint: ${env:OTLP_ENDPOINT:-otelcol:4317}
```

At startup, the Collector expands `${file:exporters.yaml}`, substitutes any environment variables, and merges everything into a single runtime configuration.

> **warning** When splitting files, ensure included paths are correct and the merged configuration produces valid references (names in `service.pipelines` must match declared component names). Test locally before deploying to production.

## Quick reference

* Minimum: receiver + exporter wired in `service.pipelines`.
* Common optional components: `processors` (transform/batch) and `extensions` (health, zPages).
* Use multiple instances and pipelines for flexible routing.
* Connectors bridge pipelines for conversions like traces → metrics.
* Use `${file:...}` and `${env:...}` to modularize and parameterize configuration.

Further reading:

* [OpenTelemetry Collector GitHub repository](https://github.com/open-telemetry/opentelemetry-collector)
* [Collector configuration docs](https://opentelemetry.io/docs/collector/configuration/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/06f2b9f7-4571-42a6-9e8a-58dddb6ec162)


# Before OpenTelemetry Why Standardization Was the Missing Piece

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Observability-Core-Concepts/Before-OpenTelemetry-Why-Standardization-Was-the-Missing-Piece/page

Explains how OpenTelemetry standardized telemetry collection to solve fragmentation and vendor lock-in, offering vendor-neutral instrumentation and a configurable Collector for flexible observability.

In this lesson we set the context for why OpenTelemetry (OTel) emerged and how it addresses long-standing challenges in collecting telemetry—metrics, logs, and traces—across modern distributed systems. As you read, ask: What was missing before OTel, and how does it fix those gaps?

Telemetry is the process of recording and transmitting readings from an instrument. Think of weather systems: satellites, ground sensors, and weather stations all send measurements into a central system for analysis and forecasting.

<Frame>
  <img alt="The image explains the basics of telemetry, showing how data from different sources such as weather stations and satellites is transmitted to a weather radar." />
</Frame>

Similarly, software systems emit signals that reveal the system’s operating condition. Telemetry can originate at multiple layers of the stack: application code, libraries, runtime, OS, kernel, and the underlying hardware. For example, a checkout service running on an EC2 instance is a workload composed of application code and libraries that call the OS and kernel and consume hardware resources.

<Frame>
  <img alt="The image illustrates telemetry data sources in software systems, featuring a layered model from hardware to application and elements such as a shopping cart interface and EC2." />
</Frame>

In distributed systems the overall health is the aggregate of signals from these layers. For brevity we’ll call this unit—application, process, or service—a “software system.”

How does telemetry leave a software system? Two common collection modes exist:

* Push: an agent or SDK inside the system sends telemetry out (for example, via HTTP POST to a collector or vendor endpoint).
* Pull: an external scraper polls an exposed endpoint (for example, Prometheus scraping `/metrics`) to collect metrics.

You can install an agent on a VM or in a container to push telemetry, or configure your application to call an API/SDK directly. Alternatively, an external scraper can poll the application to collect metrics.

<Frame>
  <img alt="The image illustrates push and pull telemetry data collection methods in software, featuring inbound and outbound data flows with components like agents, scrapers, APIs/SDKs, and polling." />
</Frame>

Comparison: Push vs Pull

| Mode | How it works                                                | Typical tools / examples                             |
| ---- | ----------------------------------------------------------- | ---------------------------------------------------- |
| Push | Application/agent sends telemetry to a collector or backend | Agents, SDKs, vendor agents (HTTP/gRPC exporters)    |
| Pull | External system scrapes exposed endpoints                   | `Prometheus` scraping `/metrics`, HTTP health checks |

Once collected, telemetry is routed to dedicated systems for visualization and analysis: a metrics system (e.g., Prometheus), a logs pipeline and dashboard (e.g., the ELK stack), and a tracing backend (e.g., Jaeger or Zipkin). Each pipeline typically has its own ingestion, storage, and query tools.

<Frame>
  <img alt="The image is a flowchart illustrating how metrics and logs are visualized from a software system, involving agents, APIs/SDKs, and dashboards for metrics and logs. It shows outbound data flow from the software system to the dashboards." />
</Frame>

Historically, observability developed in a pillar-based way: metrics, traces, and logs often used separate tools, standards, and vendor pipelines. Different teams adopted different instrumentation approaches—OpenTracing, OpenCensus, vendor-specific agents, or homegrown log agents—resulting in many isolated telemetry silos.

<Frame>
  <img alt="The image shows a diagram of several &#x22;Software System&#x22; blocks connected by arrows, illustrating the challenges in pillar-based observability systems. It includes labels like OpenTracing, Open Source Telemetry, and vendor-specific agents and SDKs." />
</Frame>

This fragmentation led many organizations to consolidate on a single vendor to reduce operational complexity: deploy that vendor’s agent everywhere and send all telemetry to its backend.

<Frame>
  <img alt="The image illustrates a single-vendor adoption model where multiple software systems use a vendor's agent to connect to a single observability backend, highlighting potential lock-in risks." />
</Frame>

While consolidation reduces short-term complexity, it creates vendor lock-in. Changing backends later can require replacing agents, re-instrumenting code, and migrating pipelines—costly and risky at scale.

A better approach is a vendor-neutral layer between systems and backends. Each software system outputs metrics, logs, and traces into that neutral layer; from there, data can be routed to any backend—Vendor A, Vendor B, a data lake, or multiple destinations—without re-instrumenting the source.

<Frame>
  <img alt="The image shows a flowchart titled &#x22;A Neutral Pipeline for All Observability Backends,&#x22; illustrating a process involving Instrumentation, Collection, and Export stages for telemetry data." />
</Frame>

With a neutral pipeline, changing where telemetry ends up is a configuration change—not a code or agent replacement. Instrument once; control destinations via telemetry middleware configuration.

OpenTelemetry provides that vendor-neutral instrumentation and processing layer. OTel SDKs and agents standardize how applications produce metrics, logs, and traces. The OpenTelemetry Collector acts as configurable middleware to receive, process, and export telemetry to one or many backends. As a result, routing telemetry becomes a matter of editing Collector configuration rather than reinstalling agents.

<Frame>
  <img alt="The image illustrates the OpenTelemetry data pipeline, showing system software sending metrics, traces, and logs through OpenTelemetry agents or SDKs to the OpenTelemetry Collector, which then directs the data to various destinations like vendor backends and data lakes." />
</Frame>

OTel was designed to coexist with existing vendors and tools. The Collector can export to vendor backends, open-source systems, object stores, or multiple destinations simultaneously—making hybrid observability and gradual migration practical.

<Frame>
  <img alt="The diagram illustrates how modern observability involves hybrid systems integrating seamlessly with OpenTelemetry. It shows different system software sending metrics, traces, and logs to various backends, including OpenTelemetry Collector and Prometheus." />
</Frame>

OTel supports hybrid environments where some services are instrumented with OpenTelemetry and others are not. You can continue accepting vendor-specific telemetry while incrementally adopting OTel, enabling coexistence and staged migration.

To summarize the key challenges before standardization:

* Fragmentation: multiple tools and standards across metrics, traces, and logs.
* Vendor lock-in: switching backends often required replacing agents and re-instrumenting code.
* No single standard: vendors and teams shipped their own agents/SDKs.
* Limited flexibility: hard to send the same telemetry to multiple destinations.
* Hybrid reality: many environments had a mix of instrumented and non-instrumented services.

<Frame>
  <img alt="The image outlines key challenges before standardization in telemetry, highlighting issues like fragmentation, vendor lock-in, lack of standard approaches, low flexibility, and commonality of hybrid setups." />
</Frame>

OpenTelemetry addresses these issues by standardizing APIs and formats for metrics, logs, and traces, and by providing a flexible Collector to process and export telemetry to any backend. This reduces vendor lock-in, supports gradual adoption, and enables exporting the same telemetry to multiple destinations for future-proofing.

> **lightbulb** OpenTelemetry provides a vendor-neutral instrumentation layer plus a configurable Collector. Instrument once; export anywhere. This enables flexibility, easier migrations, and hybrid coexistence with existing vendor ecosystems.

That concludes this lesson.

References and further reading:

* OpenTelemetry: [https://opentelemetry.io](https://opentelemetry.io)
* OpenTelemetry Collector docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* Jaeger: [https://www.jaegertracing.io](https://www.jaegertracing.io)
* ELK Stack: [https://www.elastic.co/what-is/elk-stack](https://www.elastic.co/what-is/elk-stack)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/79b34fea-6f94-4854-a31e-9ac0fbc10eca/lesson/79d6185c-e761-46ee-b4a1-fc552c0272b3)
