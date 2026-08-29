# Role of Metrics in Observability

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/Metrics-Data-Model/Role-of-Metrics-in-Observability/page

Introductory guide to using time series metrics for observability, instrumentation, and monitoring across apps, infrastructure, databases, CI CD and cloud to detect issues and inform operations.

This lesson explains the role metrics play in observability, with practical analogies and concrete guidance for instrumentation and monitoring. If you're already experienced with metrics you may skip ahead; if not, follow this introductory guide to learn why metrics are the primary “vital signs” of systems and how to use them effectively.

Think of how doctors monitor health: they continuously check a few high-level numbers—temperature, blood pressure, blood sugar—to detect issues before symptoms appear.

<Frame>
  <img alt="The image shows an illustration of a person in a lab coat holding a document, with a speech bubble containing a bar chart icon. The title above reads &#x22;Metrics: The Vital Signs of Every System.&#x22;" />
</Frame>

Similarly, everyday devices capture metrics continuously: an electricity meter is a counter of consumed units, and a car dashboard displays speed, RPM, and fuel to help prevent problems before they occur.

<Frame>
  <img alt="The image features a heading &#x22;The Universal Need for Metrics,&#x22; a subheading about understanding car performance, and an illustration of a speedometer displaying both MPH and km/h." />
</Frame>

In software systems we measure CPU cycles, memory usage, request rates, and user interactions. These time-series metrics give a quick view of system health and enable early detection—much like a dashboard helps prevent car breakdowns.

Key operational questions metrics answer:

* Is my app healthy right now?
* Is traffic growing?
* Are things degrading over time?
* Is latency increasing?
* Should I add more servers or CPU?

<Frame>
  <img alt="The image depicts key questions about application health, featuring a smartphone graphic and three questions: &#x22;Is my app healthy right now?&#x22;, &#x22;Is traffic growing?&#x22;, and &#x22;Are things slowly degrading over time?&#x22;." />
</Frame>

What are metrics?
Metrics are quantitative measurements captured over time and typically stored as time series (a sequence of data points indexed by time). Common examples include requests per second, memory used, CPU utilization, and response latency. Correlating multiple time-series reveals system behavior—e.g., CPU usage climbing to 75%—and points to actionable follow-up.

<Frame>
  <img alt="The image shows a line graph depicting CPU usage over time, with various metrics listed below. It emphasizes that metrics provide insights into system performance and behavior." />
</Frame>

Metrics can be different types:

* Gauges: instantaneous values like memory used or temperature.
* Counters: monotonically increasing values such as total requests or error counts (good for rates and delta calculations).
* Histograms/Summaries: distributions of latencies or sizes, useful for percentile calculations and SLIs.

Counters often drive alerts when growth or thresholds indicate a problem.

<Frame>
  <img alt="The image shows a simple line graph with &#x22;Error Counts&#x22; on the y-axis and &#x22;Time&#x22; on the x-axis, displaying an upward trend with a bell icon indicating an alert." />
</Frame>

Metric anatomy
Use consistent naming and metadata so metrics are discoverable, aggregatable, and actionable.

| Metric component    |                                        What it is | Example                                                              |
| ------------------- | ------------------------------------------------: | -------------------------------------------------------------------- |
| Metric name         |   A descriptive path reflecting domain and intent | `container.cpu.usage`                                                |
| Data point          |            The numeric measurement at a timestamp | `0.65` (represents 65% usage)                                        |
| Unit                | Unit of measurement (ratio, seconds, bytes, etc.) | `ratio`, `seconds`                                                   |
| Dimensions / labels | Key/value pairs that add context (aka attributes) | `container_id`, `container_name`, `runtime`, `region`, `environment` |

<Frame>
  <img alt="The image displays the anatomy of a CPU usage metric for a container, including details like metric name, data point value, unit, and various dimensions such as container ID, name, runtime, and environment." />
</Frame>

Metrics across layers of the stack
Applications span multiple layers—each layer needs targeted metrics to answer operational questions. Below is a concise mapping of where to collect metrics and why.

| Layer          |                          Key metrics to collect | Why it matters                                           |
| -------------- | ----------------------------------------------: | -------------------------------------------------------- |
| Front-end      |  Page load time, JS error rate, rendering times | Measures user experience and regression impact           |
| API gateway    |     Request count, error rate, endpoint latency | Detects traffic issues and failing endpoints             |
| Backend / App  | DB query time, cache hit rate, request duration | Reveals internal bottlenecks and performance regressions |
| Infrastructure |       CPU, memory, disk I/O, network throughput | Tracks resource utilization and capacity needs           |

When instrumenting microservices, combine service-level metrics (e.g., request durations from a Cart service) with platform-level metrics (e.g., node CPU utilization) to form a holistic view of performance and resource consumption.

<Frame>
  <img alt="The image illustrates a Kubernetes-based microservices architecture, featuring a Cart Service and a Payment Service, with metrics like http.server.duration and payment.failure.count." />
</Frame>

Database visibility
Databases are a frequent source of latency and capacity constraints. Track metrics such as query duration, connection counts, and cache hit/miss rates to detect slow queries, connection leaks, and growing workload trends before they cause outages.

<Frame>
  <img alt="The image is a slide about database monitoring, showing key metrics like query duration and a line graph depicting query duration over time. It also highlights insights for detecting slow queries, spotting connection leaks, and watching workload trends." />
</Frame>

CI/CD and delivery metrics
Observability should include delivery pipelines. Useful pipeline metrics: build duration, build failure counts, deployment latency, and test coverage ratio. These metrics help track developer productivity and DORA-style indicators (deployment frequency, lead time for changes, change failure rate, MTTR).

<Frame>
  <img alt="The image illustrates CI/CD pipeline metrics with stages: Source, Build, Test, and Deploy, alongside metrics like build duration, failure count, deployment latency, and test coverage ratio." />
</Frame>

Cloud cost and utilization metrics
In cloud environments, metrics also drive cost-awareness. Track function invocation counts, egress bytes, storage utilization, and compute cost to allocate spend by account, subscription, or project and to optimize for efficiency.

<Frame>
  <img alt="The image displays a diagram of cloud cost metrics, including function invocation count, egress bytes, storage utilization, and compute cost, along with cost trends, usage indicators, and a monthly cost summary." />
</Frame>

Best practices (brief)

* Define clear naming conventions and consistent units.
* Limit label cardinality to avoid high storage and query cost.
* Collect rates from counters rather than raw counters for alerting (e.g., requests/sec).
* Use histograms or summaries for latency percentiles (SLOs/SLIs).
* Correlate metrics with logs and traces—metrics tell you what, logs/traces help explain why.

Summary

* Metrics are time-series quantitative measurements used for real-time monitoring and trend analysis.
* They are efficient at surface-level detection and alerting but rarely contain full context for root-cause analysis.
* Combine metrics with logs and traces for diagnosis: metrics tell you what is happening; logs and traces explain why.
* Instrument the right metrics at each layer (frontend, gateway, backend, infra, DB, CI/CD, cloud) to build a complete observability strategy.

> **lightbulb** This article provided a high-level introduction to metrics in observability. For deeper study, explore metric types, aggregation methods, label cardinality, and instrumentation best practices with tools such as OpenTelemetry, Prometheus, and vendor observability platforms.

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)
* DORA metrics overview: [https://cloud.google.com/devops/blueprints/monitoring/dora-metrics](https://cloud.google.com/devops/blueprints/monitoring/dora-metrics)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/fffcb239-a53d-4a2c-beab-cc23c3514158/lesson/b30743d0-0acb-4e1a-be51-46d4f51095df)
