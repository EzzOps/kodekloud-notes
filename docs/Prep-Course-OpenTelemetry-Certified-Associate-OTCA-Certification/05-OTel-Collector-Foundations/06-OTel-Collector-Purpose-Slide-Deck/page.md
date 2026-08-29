# Run the Contrib binary (many distros ship a separate binary such as otelcol-contrib)
otelcol-contrib --config=collector-config.yaml --feature-gates=<gate>=enabled

# Or set via environment variable
OTEL_FEATURE_GATES=<gate>=enabled otelcol-contrib --config=collector-config.yaml
```

## Core vs Contrib — quick comparison

| Aspect         | Core                                              | Contrib                                                       |
| -------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| Scope          | Minimal, vetted components                        | Wide range of community/vendor integrations                   |
| Change cadence | Slower, conservative                              | Faster, more experimental                                     |
| Risk           | Lower upgrade/surface area risk                   | Higher; validate maturity per component                       |
| Use case       | Production-critical, audit-sensitive environments | Integration testing, rapid prototyping, broad connector needs |

<Frame>
  <img alt="The image compares &#x22;Core&#x22; and &#x22;Contrib&#x22; components, highlighting attributes like minimal set and slower change for Core, versus broad coverage and faster change for Contrib. It also suggests guidelines for production usage of these components." />
</Frame>

## When to build your own collector

If Contrib components you rely on are stable but you want a smaller, more controlled runtime, build a custom collector. Benefits:

* Smaller images/binaries containing only needed components.
* Reduced attack surface and fewer third-party dependencies.
* Easier compliance and security reviews.
* Predictable upgrades and consistent test results across environments.

<Frame>
  <img alt="The image is an infographic titled &#x22;Why Build Your Own Collector?&#x22; outlining benefits such as smaller images, reduced attack surface, easier compliance, and operational ease at scale." />
</Frame>

## How to build a custom collector (OCB)

Use the OpenTelemetry Collector Builder (OCB) to generate a tailored collector binary or container image:

1. Create a manifest YAML that lists the receivers, processors, exporters, and extensions you require.
2. Run OCB to generate a custom binary or container image containing only those components.
3. Publish the resulting image to your registry and deploy it.

Example minimal OCB manifest snippet:

```yaml theme={null}
components:
  receivers:
    otlp:
  processors:
    batch:
  exporters:
    otlp:
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
```

Recommended workflow

* Build the OCB image in CI, pinning component versions.
* Run integration tests in staging and validate upgrade paths.
* Push the image to a private registry and roll out via your normal deployment pipelines.

<Frame>
  <img alt="The image outlines a process for using the OpenTelemetry Collector Builder (OCB), involving defining a manifest file, running OCB to generate a binary/container, and publishing the image to a registry." />
</Frame>

Useful commands and links

* OCB repository and docs: [https://github.com/open-telemetry/opentelemetry-collector-builder](https://github.com/open-telemetry/opentelemetry-collector-builder)
* Example: build a container image in CI and push to your registry

## Support models: community vs vendor

| Support type             | Typical characteristics                                   | Recommended when                                           |
| ------------------------ | --------------------------------------------------------- | ---------------------------------------------------------- |
| Community (Core/Contrib) | GitHub issues, community discussions, best-effort support | Development, experimentation, and early testing            |
| Vendor distributions     | SLAs, tested bundles, official support channels           | Production-critical deployments needing guaranteed support |

Vendor distributions often include compatibility testing with that vendor’s backend and may be preferable for production environments that require SLAs.

<Frame>
  <img alt="The image compares community support with vendor support models, highlighting features like GitHub issues and discussions for community and SLAs and tested bundles for vendors. It notes vendor distros are recommended for production." />
</Frame>

## Where to find releases

Core and Contrib binaries, OS packages, and container images are published in the OpenTelemetry Collector Releases repository:

* [https://github.com/open-telemetry/opentelemetry-collector-releases](https://github.com/open-telemetry/opentelemetry-collector-releases)

Use official artifacts for development and early testing. For production, prefer a validated OCB-built image or a vendor-supported distribution.

<Frame>
  <img alt="The image outlines two production paths for running collectors: building your own collector with OCB using validated components, or using a vendor-supported distribution for production." />
</Frame>

## Best practices

* Start by experimenting with Contrib to validate integrations and workflow.
* Track component stability labels and record feature gate usage.
* Pin versions and run upgrade tests in staging before promoting to production.
* Right-size your collector with OCB so only vetted components are included.
* Avoid enabling unnecessary or unstable components in production unless protected by feature gates and covered by tests.
* Automate build and deployment (CI/CD) and deploy collectors declaratively.

## Kubernetes deployment patterns (high-level)

Common deployment patterns:

* Sidecar: a collector runs alongside each application pod — ideal for fine-grained telemetry capture and low-latency forwarding.
* DaemonSet: one collector per node — useful for node-level and host-level telemetry collection.
* Centralized Deployment: a set of centralized collectors that aggregate, process, and export telemetry for multiple services.

These patterns are covered in depth in a dedicated Kubernetes lesson.

<Frame>
  <img alt="The image illustrates a high-level view of Kubernetes deployment, highlighting three patterns: Sidecar, DaemonSet, and Deployment. Each pattern is demonstrated through diagrams involving nodes, pods, and collectors within a Kubernetes cluster." />
</Frame>

## Operator-driven management

An OpenTelemetry Operator automates collector lifecycle management in Kubernetes:

* Declare a Custom Resource (CR) manifest.
* The operator watches and reconciles the CR, creating and managing collector pods.
* This approach fits GitOps practices and simplifies upgrades and scaling.

Operator repo and docs: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)

<Frame>
  <img alt="The image illustrates an operator-driven setup concept in Kubernetes, showing a flow from a Custom Resource Definition (CRD) in a YAML file to an operator (controller), and finally to collector pods running in Kubernetes." />
</Frame>

> **lightbulb** For production, prefer validated OCB builds or vendor-supported distributions and deploy collectors declaratively (for example, via the OpenTelemetry Operator) to ensure reproducibility and easier operations.

## Wrap-up

* Collector Core: minimal and stable — ideal for predictable, low-risk deployments.
* Collector Contrib: broad integrations and faster innovation — validate component maturity and stability before production use.
* Use feature gates to control experimental behavior and test thoroughly.
* For scale and safety, build a tailored collector with OCB or adopt a vendor-supported distribution.
* In Kubernetes, deploy collectors declaratively (Operator/CRDs) and choose the deployment pattern that fits your telemetry and operational needs.

## Links and references

* OpenTelemetry Collector Builder (OCB): [https://github.com/open-telemetry/opentelemetry-collector-builder](https://github.com/open-telemetry/opentelemetry-collector-builder)
* OpenTelemetry Collector Releases: [https://github.com/open-telemetry/opentelemetry-collector-releases](https://github.com/open-telemetry/opentelemetry-collector-releases)
* OpenTelemetry Operator: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)
* OpenTelemetry project: [https://opentelemetry.io/](https://opentelemetry.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/79639a16-6b5a-40d9-9ec8-f0b6d576dd9e)


# OTel Collector Purpose Slide Deck

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Foundations/OTel-Collector-Purpose-Slide-Deck/page

Explains the OpenTelemetry Collector role in centralizing ingestion, processing, and exporting of traces metrics and logs to decouple applications from backends while enabling scaling security and governance

Welcome to the OpenTelemetry Collector lesson.

In this lesson we explore the OpenTelemetry Collector — the scalable, central observability component that ingests, processes, and exports telemetry (traces, metrics, logs, and context/baggage). The collector decouples instrumented applications from backend destinations so you can centralize configuration, enforce data governance, and scale observability reliably.

For full reference, see the official OpenTelemetry Collector docs: [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) and the YAML specification: [YAML 1.2](https://yaml.org/spec/1.2/spec.html).

<Frame>
  <img alt="The image illustrates the need for a collector in a system, showing two terminal interfaces with language-specific exporters connecting to a central database, with warning symbols indicating potential issues." />
</Frame>

Why you shouldn’t rely on console debugging at scale

During development it’s common to print telemetry to the console: quick, immediate feedback for local debugging. But console output doesn’t scale — you won’t have centralized visibility across many services or environments, and you can’t retain, filter, or route this data to backends.

<Frame>
  <img alt="The image illustrates a concept that console output is intended for debugging, not observability, using a diagram of services with trace, metric, and log components. It emphasizes that console output is for learning and debugging only." />
</Frame>

Why sending telemetry directly from every service becomes impractical

Each application can export telemetry directly to backends (OTLP, Jaeger, Zipkin, Prometheus, StatsD, etc.). That works for a few services but creates operational pain at scale: per-service exporter configuration, duplicated credentials, and redeploys for backend changes.

<Frame>
  <img alt="The image depicts a diagram showing why sending telemetry directly to multiple backends is impractical, highlighting added complexity and overhead with icons indicating issues." />
</Frame>

What the OpenTelemetry Collector provides

The Collector is a standalone service that decouples telemetry production from backend delivery. Applications send telemetry in supported formats (OTLP, Jaeger, Zipkin, Prometheus, StatsD, etc.) to the collector. The collector receives the data, optionally processes it (batching, sampling, filtering, enrichment), and exports it to one or more backends. Configuration is centralized in a YAML file, making pipeline and exporter management consistent across environments.

<Frame>
  <img alt="The image is an introduction to the OpenTelemetry Collector, depicting it as a standalone service that decouples telemetry production from where it's sent, with inputs like OTLP, Jaeger, Zipkin, Prometheus, and StatsD. It also mentions YAML version 1.2 or greater." />
</Frame>

Example: minimal collector configuration

Below is a simple YAML snippet illustrating receivers, processors, exporters, and pipelines. Use this as a starting point and adapt to your environment.

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
  memory_limiter:
    check_interval: 1s
    limit_mib: 4000

exporters:
  logging:
    loglevel: info
  otlp/production:
    endpoint: "otel-collector.backend.example:4317"
    tls:
      insecure: false

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, memory_limiter]
      exporters: [logging, otlp/production]
    metrics:
      receivers: [otlp, prometheus]
      processors: [batch]
      exporters: [otlp/production]
```

Collector architecture and telemetry flow

* Receivers: Ingest telemetry in many formats (OTLP, Prometheus scrape, Jaeger, Zipkin, etc.).
* Processors: Transform data (batching, sampling, filtering, attribute manipulation, memory limiting).
* Exporters: Send processed telemetry to backends (OTLP, vendor-specific exporters such as Jaeger/Zipkin, Prometheus remote write, or logging).
* Extensions: Non-pipeline components that enhance the collector (health\_check, zpages, authentication, observability endpoints).

Receivers → Processors → Exporters form the pipelines. Extensions run at the collector level for monitoring and management. You can define separate pipelines per signal type (traces, metrics, logs) and route them to multiple backends.

Use this quick reference table to map components to responsibilities and examples:

| Component | Responsibility                                      | Examples                                                       |
| --------- | --------------------------------------------------- | -------------------------------------------------------------- |
| Receiver  | Intake telemetry from instrumented apps or scrapers | `otlp`, `prometheus`, `jaeger`, `zipkin`                       |
| Processor | Transform or protect data before export             | `batch`, `tail_sampling`, `memory_limiter`, `attributes`       |
| Exporter  | Send telemetry to backend systems                   | `otlp`, `jaeger`, `zipkin`, `prometheusremotewrite`, `logging` |
| Extension | Collector-level support services                    | `health_check`, `zpages`, `auth`, `pprof`                      |

<Frame>
  <img alt="The image illustrates a &#x22;Collector Architecture Overview,&#x22; showing a flow from receiving telemetry data through receivers, processors, and exporters, with extensions for services like health checks." />
</Frame>

Benefits of deploying the Collector

| Benefit                    | What it delivers                                                                                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Decoupling                 | Applications send telemetry to a local or central collector instead of embedding exporter logic. This simplifies application code and reduces reconfiguration needs. |
| Centralized configuration  | Manage pipelines, processors, and exporters in one YAML, enabling consistent routing, sampling, and transformations across services.                                 |
| Scalability                | Scale collectors horizontally (sidecars, agents, or centralized gateways) and centralize exporter instances to reduce config drift and operational overhead.         |
| Data governance & security | Apply filtering, redaction, and enrichment in the collector to protect sensitive data before it leaves your environment.                                             |

<Frame>
  <img alt="The image outlines three key benefits of deploying the Collector: decoupling code from the backend, centralizing configuration, and allowing horizontal scaling." />
</Frame>

Deployment considerations and best practices

* Resource allocation: Provision sufficient CPU and memory for ingestion and processing. Use the `memory_limiter` and `batch` processors to control memory and throughput.
* Reliability: Avoid single points of failure by running multiple replicas behind a load balancer, or deploy local agents (sidecars) with a centralized gateway to aggregate data.
* Monitoring: Enable `health_check`, `zpages`, and the collector’s own metrics to monitor pipeline latency, queue sizes, error rates, and resource usage.
* Security: Protect receiver endpoints with TLS and mTLS, authenticate clients, and apply exporter-level encryption. Manage credentials centrally and rotate them as part of your security policy.
* Operational workflows: Keep collector configuration in version control, use CI/CD to validate YAML changes, and test sampling/filtering rules in lower environments before rolling out to production.

<Frame>
  <img alt="The image outlines deployment considerations for a Collector, highlighting the need for a resource allocation plan for CPU and memory usage, reliability through replicas behind a load balancer, and monitoring via health-check and z-pages endpoints." />
</Frame>

> **warning** Always secure collector receivers. Use TLS and mutual TLS (mTLS) where clients must be authenticated, and apply access controls so only authorized services can send telemetry.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/94d2710a-c270-4c49-9e4b-df67653f1b47/lesson/c2c3c349-a9bf-4562-87d1-7567b20e78a9)
