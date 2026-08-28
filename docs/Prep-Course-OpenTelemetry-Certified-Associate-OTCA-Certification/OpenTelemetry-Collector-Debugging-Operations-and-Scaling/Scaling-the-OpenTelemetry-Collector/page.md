# Scaling the OpenTelemetry Collector

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Scaling-the-OpenTelemetry-Collector/page

Practical strategies to safely scale the OpenTelemetry Collector using load balancing, sharding, and consistent routing, and diagnosing when scaling versus backend changes are appropriate

Given diagnostic signals from your Collector, the next question is: what action should you take? This guide explains practical, safe strategies to scale the OpenTelemetry Collector, how to interpret internal metrics to drive those decisions, and when scaling is ineffective.

This article will:

* show the high-level Collector topology and load distribution patterns,
* explain which Collector components actually require scaling,
* describe when scaling will help and when it will not,
* outline safe scaling strategies for common workloads (stateless ingestion, Prometheus-style scrapers, and stateful processors).

<Frame>
  <img alt="The image is a diagram showing the scaling of the OpenTelemetry Collector, illustrating a structure with a &#x22;Telemetry&#x22; component feeding into multiple &#x22;Collector&#x22; and &#x22;Load Balancer&#x22; pairs." />
</Frame>

Overview

Telemetry typically flows from clients into multiple Collector instances. Each Collector generally forwards data to the same backend(s). Load balancers are commonly placed in front of stateless receivers to distribute incoming traffic. The tasks when scaling are:

* identify which component in a pipeline is under pressure,
* choose a scaling pattern appropriate to that component (load balancing, sharding, or consistent routing),
* verify that the backend and network can absorb increased load before increasing Collector replicas.

<Frame>
  <img alt="The image is a slide titled &#x22;Introduction – Scaling the OpenTelemetry Collector,&#x22; listing topics such as what to scale, when scaling is needed, when scaling is not effective, and how to execute scaling strategies." />
</Frame>

<Callout icon="lightbulb">
  When planning scale operations, focus on the overloaded signal (logs, metrics, or traces), inspect collector metrics that indicate processor, queue, or exporter pressure, and decide whether to scale the Collector, tune configuration, or scale the backend.
</Callout>

What to scale: three broad categories

Use the table below to decide which scaling strategy fits each component type.

| Component type              |                                                                                                             Description | Primary scaling strategy                                                                         | Key signals / considerations                                        |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Stateless components        | Receivers/processors that forward data without keeping per-entity state (e.g., OTLP ingestion that immediately exports) | Horizontal scaling behind a load balancer                                                        | Use load balancing; watch `memory`, `cpu`, `exporter_queue` metrics |
| Scrapers (Prometheus-style) |                                                                      Components that actively pull metrics from targets | Shard scrape targets across collectors (target allocator)                                        | Avoid duplicate metrics; use per-collector `http_sd_config`         |
| Stateful processors         |                                          Processors that keep per-trace or per-entity state (e.g., tail-based sampling) | Consistent routing (trace ID hashing) or pinned routing so all related data reaches same replica | Requires routing that preserves group affinity for correctness      |

<Frame>
  <img alt="The image shows a diagram titled &#x22;Scaling Categories,&#x22; displaying three types: Stateless, Scraping, and Stateful, with Best Practices linked to Load Balancing and Sharding." />
</Frame>

Mapping diagnostics to actions

Inspect the Collector's internal metrics and exporter telemetry to determine if you should scale the Collector tier, tune queue/configuration, or fix the backend/network. The table below summarizes common symptoms and recommended responses.

| Symptom                                                    |                              Typical metric(s) | Recommended action                                                                                   |
| ---------------------------------------------------------- | ---------------------------------------------: | ---------------------------------------------------------------------------------------------------- |
| Spans dropped by processor / memory pressure               | `processor_refused_spans`, other `*_refused_*` | Increase Collector CPU/memory or add replicas; tune memory\_limiter settings                         |
| Growing exporter queue / sustained queue utilization \~70% |         exporter queue size, queue utilization | Increase queue capacity, adjust timeouts/retry settings, or scale Collector tier                     |
| Exporter enqueue failures (queues full)                    |                `exporter_enqueue_failed_spans` | Investigate queue limits and backpressure; scale Collectors or tune queue policies                   |
| High exporter latency / backend slow to respond            |   `exporter_latency`, backend response metrics | Likely backend or network bottleneck — scale or optimize backend, do not only add Collector replicas |

<Frame>
  <img alt="The image depicts a diagram illustrating how scaling collectors might not solve backend and network bottlenecks, highlighting issues like a rising queue and persistent errors." />
</Frame>

<Callout icon="warning">
  If the network link to your backend is saturated or your backend is unable to ingest more telemetry, adding Collector replicas amplifies failures rather than resolving them. Diagnose and resolve backend or network issues before scaling the Collector tier.
</Callout>

Scaling patterns by component type

Stateless components

* Stateless receivers and processors (for example, OTLP ingestors that simply forward data) are the easiest to scale horizontally. Place a load balancer in front of multiple identical Collector replicas and scale replicas as demand grows.
* Typical setup: clients -> load balancer -> N stateless Collector replicas -> exporter(s).

<Frame>
  <img alt="The image illustrates a load balancing setup for scaling stateless components, showing a load balancer distributing requests to multiple collectors. The components are organized into categories: Stateless Components, Scrapers (Prometheus), and Stateful Processors." />
</Frame>

Prometheus-style scrapers

* Multiple collectors scraping the same targets will produce duplicate metrics. To avoid this, assign each collector a unique subset of targets (sharding).
* Implement a target allocator or similar orchestration that:
  1. Discovers scrape endpoints,
  2. Divides them into non-overlapping sets,
  3. Generates per-collector service discovery configurations (for example, a dedicated `http_sd_config`) so each collector scrapes only its assigned targets.
* After scraping, collectors export metrics (e.g., Prometheus Remote Write) to the backend. Sharding guarantees each metric stream is emitted exactly once.

<Frame>
  <img alt="The image is a diagram titled &#x22;Scaling Scrapers Across Shared Targets,&#x22; showing how scrapers (Prometheus) interact with shared scrape targets and collectors. It also mentions stateless components and stateful processors." />
</Frame>

Target allocator workflow

* Operator updates scrape configuration and hands it to the target allocator.
* Target allocator discovers all scrape endpoints and partitions them into unique sets.
* For each Collector pod, the allocator generates an `http_sd_config` so each collector scrapes only its assigned endpoints.

<Frame>
  <img alt="The image is a flowchart illustrating the coordination of Prometheus scraping with a Target Allocator, showing the process from operator updates to the assignment of unique scrape endpoints and configuration for each collector pod." />
</Frame>

Stateful processors (e.g., tail-based sampling)

* Stateful processors need complete per-trace context to make correct decisions (for example, in tail-based sampling).
* Ensure all spans for a trace are routed to the same Collector replica. Two common approaches:
  * Client-side / load-balancing exporter with consistent hashing on the trace ID so all spans for a trace land on the same replica.
  * A front-end router that performs consistent hashing and forwards trace data to the appropriate Collector.
* Consistent hashing preserves trace-to-replica affinity even as replicas scale up or down, allowing stateful operations (like tail-sampling) to function correctly.

<Frame>
  !\[The image is a diagram illustrating "Scaling Stateful Data-Dependent Components," showing a flow from a "Tail-Sampling Processor" to a "Load Balancer." It also categorizes components as "Stateless," "Scrapers (Prometheus)," and "Stateful processors."]\(/images/Prep-Course-OpenTelemetry- Certified-Associate-OTCA-Certification/OpenTelemetry-Collector-Debugging-Operations-and-Scaling/Scaling-the-OpenTelemetry-Collector/scaling-stateful-data-dependent-components-diagram.jpg)
</Frame>

Client traces and consistent routing

* Typical flow: client -> load-balancing exporter -> consistent-hash routing -> Collector replicas -> tail-sampling / stateful processing -> backend.
* With consistent trace ID hashing, every span for a trace is forwarded to the same Collector replica, preserving the required context for stateful processing even when replicas change.

<Frame>
  <img alt="The image is a flowchart illustrating how client traces are managed with a load-balancing exporter and multiple collector replicas, highlighting the use of consistent trace ID hashing to ensure complete traces during scaling." />
</Frame>

Operational checklist for scaling

* Identify the overloaded signal (logs, metrics, traces). If your pipelines are separated by signal, scale only the affected pipeline.
* Monitor these Collector metrics closely:
  * CPU and memory usage,
  * `processor_refused_*` (e.g., `processor_refused_spans`),
  * queue sizes and utilization,
  * `exporter_enqueue_failed_*`,
  * `exporter_latency`.
* If the Collector is dropping data or refusing spans, scale the Collector or increase resource limits and tune the memory\_limiter.
* If exporter latency / send failures indicate backend or network issues, fix or scale the backend before increasing Collector replicas.
* For scrapers: shard targets (target allocator) so each Collector scrapes a unique set and avoid duplicates.
* For stateful processors: use consistent hashing or pinned routing so all spans from a trace route to the same replica.

<Frame>
  <img alt="The image is a slide titled &#x22;Wrap-Up,&#x22; summarizing key points about signal type, collector metrics, scaling considerations, stateless collectors, scrapers, and stateful processors, with a focus on scalability and load balancing." />
</Frame>

Wrap-up

* Start by identifying the overloaded signal and inspect the corresponding Collector metrics.
* Scale stateless Collectors behind a load balancer for straightforward horizontal scaling.
* Shard Prometheus-style scrapers or use a target allocator to avoid duplicate metrics.
* Use consistent hashing (trace ID-based routing) for stateful components (e.g., tail-based sampling) so all spans in a trace arrive at the same replica.
* Never scale Collectors blindly when the backend or network is the root cause — that only amplifies errors.

References and further reading

* [OpenTelemetry Collector Concepts](https://opentelemetry.io/docs/collector/)
* [Prometheus Sharding and Scraping Patterns](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config)
* [Designing for Observability at Scale (patterns)](https://opentelemetry.io)

This concludes the discussion on safe and effective scaling strategies for the OpenTelemetry Collector.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/9c72c1a7-4e0b-4541-8811-755843e69659/lesson/da1341b9-9657-425c-9619-1a8370e327cd" />
</CardGroup>
