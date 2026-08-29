# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP celery_tasks_total Number of Celery tasks executed
# TYPE celery_tasks_total counter
# HELP celery_task_failures_total Number of Celery task failures
# TYPE celery_task_failures_total counter
# HELP celery_task_duration_seconds Task execution time in seconds
# TYPE celery_task_duration_seconds histogram
# HELP http_requests_total Total HTTP Requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/metrics",method="GET",status_code="200"} 15
http_requests_total{endpoint="/health",method="GET",status_code="200"} 14
http_requests_total{endpoint="/favicon.ico",method="GET",status_code="404"} 1
http_requests_total{endpoint="/docs",method="GET",status_code="200"} 1
http_requests_total{endpoint="/openapi.json",method="GET",status_code="200"} 1
# HELP http_requests_created Total HTTP Requests timestamp
# TYPE http_requests_created gauge
http_requests_created{endpoint="/metrics",method="GET",status_code="200"} 1.7449748268583556e+09
http_requests_created{endpoint="/health",method="GET",status_code="200"} 1.744974834539342e+09
http_requests_created{endpoint="/favicon.ico",method="GET",status_code="404"} 1.7449749339448135e+09
http_requests_created{endpoint="/docs",method="GET",status_code="200"} 1.7449750247689226e+09
http_requests_created{endpoint="/openapi.json",method="GET",status_code="200"} 1.7449750251944983e+09
# HELP http_request_duration_seconds HTTP Request Duration in seconds
# TYPE http_request_duration_seconds histogram
```

* Logs — timestamped event records that provide rich context: error stacks, request/response payloads, and state transitions. Logs validate metrics and are essential for root-cause analysis. Example log entries:

```text theme={null}
> 2025-04-18 12:15:33.000 {"container_name":"/kodekloud-record-store-api","source":"stderr","log":"{\"message\": \"http_error\", \"level\": \"ERROR\", \"trace_id\": \"c7bfc8714e3720b74732fa905609705a\", \"span_id\": \"3fc595b17c3a83c8\", \"method\": \"GET\", \"endpoint\": \"/favicon.ico\", \"status_code\": 404, \"duration_ms\": 1.71}", "container_id":"2e81ab28c31116a274347a761369610ebe21e08103f2aa66cd86dd0570ac8d36"}
> 2025-04-18 12:13:37.000 {"source":"stderr","log":"{\"message\": \"Test error log\", \"level\": \"ERROR\", \"trace_id\": \"d5050e46f1e150a21145fe58b15aff89\", \"span_id\": \"cb34a453a247be9b\", \"error_type\": \"SimulatedError\", \"operation\": \"error_test\"}", "container_id":"2e81ab28c31116a274347a761369610ebe21e08103f2aa66cd86dd0570ac8d36","container_name":"/kodekloud-record-store-api"}
```

<Frame>
  <img alt="A presentation slide titled &#x22;The Three Data Types for Reliability Measurements&#x22; highlighting &#x22;Logs&#x22; as a data type. It lists examples relevant for SLIs: error logs, access logs, and service logs." />
</Frame>

* Traces — record the life of a single request across services and network hops. Traces are vital in distributed systems to pinpoint which service added latency or propagated an error.

<Frame>
  <img alt="A presentation slide titled &#x22;The Three Data Types for Reliability Measurements&#x22; highlighting &#x22;Traces&#x22; with three bullet examples (end-to-end request paths, service dependency maps, cross-service error propagation). Below is a trace timeline screenshot showing a GET /health request for &#x22;kodekloud-record-store-api&#x22; with span durations and service operations." />
</Frame>

Together: metrics describe what happened, logs explain what went wrong, and traces reveal where it happened.

## Minimal set of SLIs — Google's four golden signals

If you can only measure four things, capture Google’s golden signals — essential SLIs for reliability and incident response:

1. Latency — time to serve a request. Use percentiles (p95, p99) to surface slow requests rather than averages.
   * Example: 99% of requests complete under 200 ms.
2. Traffic — volume of requests (requests per second). Important for capacity planning and impact assessment.
   * Example: 1,000 requests/s with under 1% errors.
3. Saturation — how close resources are to limits (CPU, memory, queue depth). Saturation is an early warning sign of trouble.
4. Errors — rate of failed requests. Define what constitutes an error for your system (HTTP 5xx, timeouts, application exceptions).

Read more in the SRE book: [Monitoring Distributed Systems (Google SRE)](https://sre.google/sre-book/monitoring-distributed-systems/).

## Black box vs white box monitoring

* Black box (external) monitoring simulates user interactions and measures availability/latency from the end-user perspective: pings, synthetic transactions, page load timings.
* White box (internal) monitoring exposes service-internal telemetry (metrics, logs, traces) so you can diagnose why an SLO failed.

Use both: black box shows real user impact; white box enables fast diagnosis.

<Frame>
  <img alt="A slide illustration titled &#x22;Monitoring Techniques&#x22; that compares Blackbox Monitoring (a closed black cube with arrows labeled load time, ping, API call, response time, SSH) and Whitebox Monitoring (an open box with upward arrows labeled metrics, logs, traces). The graphic visually contrasts external checks versus internal telemetry." />
</Frame>

## Measurement windows: short, medium, long

Choose measurement windows to match their operational purpose:

* Short windows (minutes or hours): immediate alerting and action.
* Medium windows (a few hours): detect gradual degradation and provide operational context.
* Long windows (weeks to months): SLO compliance tracking and long-term reliability goals (e.g., 30-day or quarterly windows).

You need all three: short for action, medium for context, and long for compliance.

<Frame>
  <img alt="A presentation slide titled &#x22;Designing Basic Monitoring for SLIs&#x22; that compares three measurement windows for SLO monitoring — short (immediate alerting), medium (operational awareness), and long (SLO compliance tracking) — shown with colored arrows and brief descriptions. The slide is copyrighted by KodeKloud." />
</Frame>

> **warning** Common pitfalls when building SLI-based monitoring:

  * Using infrastructure metrics (CPU, disk) as SLIs — they rarely reflect user experience.
  * Using averages rather than percentiles — averages can hide tail latency that affects users.
  * Setting thresholds that are too sensitive (alert fatigue) or too lax (missed incidents).
  * Measuring in the wrong place — always measure as close to the user as possible (use synthetic and real-user monitoring).

Synthetic monitoring (black box) uses scripted, repeatable user actions — logins, API calls, page loads — to validate external availability and measure the true user experience.

This completes the introduction to reliability measurements. Subsequent material will dive deeper into defining effective SLIs, designing SLOs, and applying error budgets to guide product and engineering decisions.

Further reading and references:

* [Prometheus exposition formats](https://prometheus.io/docs/instrumenting/exposition_formats/)
* [Google SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
* [Observability resources and practices](https://sre.google/sre-book/observability/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/eeb0b057-483e-4977-ae2b-affd3ae03709)


# SLO Development and Strategy

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Service-Level-Objectives-and-Measurements/SLO-Development-and-Strategy/page

Guides creating and operationalizing service level objectives by mapping user journeys to SLIs, setting data driven SLO targets, using error budgets, and reviewing trade offs between reliability and cost.

Welcome to the lesson on developing service-level objectives (SLOs) and the strategies that make them practical tools for reliability engineering.

By the end of this lesson you'll understand how SLOs link user expectations to engineering reality, and why they are the foundation of measurable reliability.

Why can't we promise 100% uptime? And why do SLOs matter?

> **warning** At real-world scale, 100% uptime is infeasible. Trying to guarantee it leads to unsustainable costs, brittle systems, and slow innovation. SLOs help teams balance reliability, cost, and speed by defining realistic, measurable targets.

SLOs are far more than just target numbers. Well-crafted SLOs:

* Quantify acceptable unreliability (error budgets).
* Create a shared language across engineering and business stakeholders.
* Prioritize engineering effort and operational investment according to business risk.
* Surface the incidents that matter most to users.
* Make reliability visible, measurable, and actionable across the organization.

<Frame>
  <img alt="An infographic titled &#x22;The Strategic Value of SLOs&#x22; showing a colorful stacked-ring &#x22;SLO Benefits Pyramid&#x22; on the left and a labeled list on the right. The list outlines benefits like Error Budgets, Common Language, Measure Risk Tolerance, Prioritization, Problem Identification, and Clarity." />
</Frame>

Start with the customer: what do users actually care about?

Map critical user journeys, convert the steps into measurable service-level indicators (SLIs), and set SLO targets that meet business goals while leaving room to evolve the service. SRE and reliability teams translate customer needs into engineering priorities — and user satisfaction is the metric that determines success.

When converting business goals into SLOs, ask:

* Which user journeys are critical?
* What does “good enough” look like for those journeys (latency, availability, correctness)?
* What trade-offs between cost and reliability are acceptable?

A structured business impact analysis helps justify SLO trade-offs.

<Frame>
  <img alt="A presentation slide titled &#x22;Developing Customer-Focused SLOs&#x22; showing a &#x22;Business Impact Analysis&#x22; with four colored boxes. The boxes are labeled Revenue Impact, Cost Implications, Competitive Landscape, and Brand Perception, each accompanied by an icon and a short guiding question." />
</Frame>

Consider these business dimensions when setting SLOs:

* Revenue: how do downtime and slow responses affect conversions and sales?
* Costs: what operational or engineering investments are required at each reliability level?
* Competitive position: what reliability levels do competitors promise?
* Brand perception: how does reliability affect trust and retention?

Compare cost vs. business benefit before chasing higher availability targets.

<Frame>
  <img alt="A presentation slide titled &#x22;Developing Customer-Focused SLOs&#x22; with a chart labeled &#x22;Cost vs Revenue Improvement for Availability.&#x22; It shows four cylindrical bars comparing annual cost and revenue saved for 99.9% vs 99.99% availability, labeled 1,000, 1,500, 5,000 and 500." />
</Frame>

The general pattern is that each additional “nine” of availability typically costs more (often exponentially) while customer or revenue benefit increases more slowly. Your goal is the economic optimum: the point where the cost to improve reliability further equals the business value gained.

<Frame>
  <img alt="A slide titled &#x22;Developing Customer-Focused SLOs&#x22; presenting an economic framework that defines &#x22;Optimal Reliability = Point where (cost of improving reliability) = (business value gained from improvement)&#x22; in a blue callout." />
</Frame>

Translate user needs into technical metrics

For each user journey, enumerate failure modes and acceptable outcomes:

* How can this app fail?
* Which failures are acceptable for the user experience?
* Are different user segments treated differently?
* What counts as an error?

Then choose appropriate SLI types — availability, latency, quality, throughput, durability — and define precise measurement methods.

<Frame>
  <img alt="A presentation slide titled &#x22;Translating Expectations to Metrics&#x22; showing a target icon on the left and a teal box of bullet questions about failures and errors. Dotted arrows point from that box to an orange box on the right labeled &#x22;Availability SLIs.&#x22;" />
</Frame>

Common SLI types and examples

|              SLI Type | What it measures                    | Example                                  |
| --------------------: | ----------------------------------- | ---------------------------------------- |
|          Availability | Fraction of successful requests     | `probe_success{endpoint="/health"}`      |
|               Latency | Response-time distribution          | 95th/99th percentile of request duration |
| Quality / Correctness | Whether responses are correct       | Rate of valid responses vs errors        |
|            Throughput | Requests or transactions per second | `requests_total` per minute              |
|            Durability | Data persisted without loss         | Backup success rate, replication lag     |

Map SLI measurements to SLO statements that are understandable by product and business teams.

Example: KodeKloud record store (search and orders)

<Frame>
  <img alt="A presentation slide titled &#x22;KodeKloud Record Store SLOs&#x22; showing a microservices architecture diagram with a central KodeKloud Record Store linked to Observability (Prometheus, Grafana, Jaeger, etc.), Storage (PostgreSQL), a Core Microservice (API, Orders, Products) and Async Processing (RabbitMQ, Celery). On the right is a user icon with a speech bubble saying &#x22;I can't wait to get The Elvis Presley Record!&#x22;" />
</Frame>

Search experience: users expect quick, reliable search results.

A simple Prometheus expression to measure a probe-success availability SLI over one day:

```promql theme={null}
avg_over_time(probe_success{endpoint="/health"}[1d])
```

If that query evaluates to 0.999, it indicates 99.9% availability over the last 24 hours.

Example SLOs for the search journey:

* Availability SLO: 99.9% of API requests succeed (catalog API).
* Latency SLO: 99% of search queries complete within 300 ms.

Why 300 ms and 99%? Research on perceived latency shows users notice delays above \~300 ms; 99% is often achievable without extreme cost while protecting the vast majority of users.

Order-processing journey: placing and processing an order must be reliable and timely.

A Prometheus expression to compute error rate for the orders endpoint:

```promql theme={null}
sum(rate(http_requests_total{endpoint="/orders", status_code!~"2.."}[5m])) /
sum(rate(http_requests_total{endpoint="/orders"}[5m]))
```

This calculates the fraction of non-2xx responses over the last 5 minutes.

Suggested SLIs and SLOs for orders:

* SLIs: processing success rate, end-to-end order processing latency.
* SLO (availability/orders): 99.9% of order requests process successfully.
* SLO (latency/orders): 95% of orders complete processing within 3 seconds.

We selected the 3-second, 95th-percentile target because customer satisfaction declines sharply after that threshold and it aligns with current system capacity.

<Frame>
  <img alt="A presentation slide titled &#x22;KodeKloud Record Store SLOs&#x22; and &#x22;SLO Development&#x22; with text about customers expecting orders to be processed quickly and reliably. Below is an illustration of a delivery person emerging from a smartphone to hand a package to a seated woman." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;KodeKloud Record Store SLOs&#x22; showing target SLOs: an Availability SLO (99.9% of order requests process successfully) and a Latency SLO (95% of orders complete within 3 seconds). A brief rationale notes satisfaction drops when orders exceed 3 seconds." />
</Frame>

Use historical data, not guesswork

Wherever possible, derive SLO targets from historical telemetry. Historical SLIs give you realistic baselines and show what is achievable without major investment. Always document the rationale for each SLO: why it was chosen, the assumptions, the data used, and expected limitations.

> **lightbulb** Always record the rationale and assumptions for every SLO. This documentation enables future teams to understand why targets were chosen and how to adjust them over time.

Make SLOs a living process

Establish a regular SLO review cadence and a clear escalation path:

* Start with data-driven, educated estimates (benchmarks, architecture, stakeholder input).
* Record assumptions and measurement methods.
* Analyze actual performance during reviews: SLO adherence, trends, and patterns.
* Combine quantitative metrics with qualitative feedback (customer surveys, stakeholder concerns).
* Reassess business risk and operational cost (alert noise, toil).
* Adjust SLOs and error-budget policies based on evidence.

<Frame>
  <img alt="A presentation slide titled &#x22;Implementing a Data-Driven SLO Review Process&#x22; that outlines the initial SLO setting process. It shows four colored rounded panels labeled &#x22;Industry Benchmarks,&#x22; &#x22;Technical Architecture,&#x22; &#x22;Business Stakeholder Input,&#x22; and &#x22;Existing Performance Data.&#x22;" />
</Frame>

Not all services require the same SLO tightness. Align SLO strictness with business criticality:

* Critical customer-facing systems (payments, authentication): very strict SLOs (e.g., 99.99%).
* Content delivery and public APIs: high availability but tuned to cost-impact.
* Internal tools and background jobs: more lenient SLOs, optimized for cost and throughput.

<Frame>
  <img alt="An infographic titled &#x22;SLO Target Levels for Different Service Types&#x22; showing &#x22;Service-Level Objectives&#x22; branching into four numbered, colored categories: 1) Critical Business Systems, 2) Internal Tools, 3) Content Delivery, and 4) Background Processing. Each category is represented by a colored ribbon and small icon indicating priority." />
</Frame>

Operationalize SLOs with error budgets

Error budgets translate SLOs into governance and operational policy. They enable teams to make explicit decisions about whether to prioritize feature velocity or reliability:

* If the error budget is healthy, teams can safely ship features and experiments.
* If the error budget is depleted, the team focuses on reliability work until the budget is replenished.

Use dashboards and automated checks to track SLO consumption, and define clear runbooks for error-budget breaches (e.g., reduce rollouts, increase QA, emergency fixes).

Summary checklist for SLO development

* Identify critical user journeys.
* Define SLIs with precise measurement methods.
* Set SLOs based on business impact and historical data.
* Document rationale, assumptions, and measurement details.
* Implement monitoring, dashboards, and alerting tied to SLOs and error budgets.
* Review and iterate SLOs regularly with business stakeholders.

Links and references

* [Google SRE Book — Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
* [Prometheus — Monitoring system & time series database](https://prometheus.io/)
* [Site Reliability Engineering (SRE) — Principles and Practices](https://landing.google.com/sre/)
* [SLO Playbooks and Guides — Practical SLO design](https://sre.google/sre-book/)

Further reading

* How to measure latency percentiles and why p95/p99 matter for UX.
* Error budgets: policy templates and runbooks.
* Prometheus query examples for SLIs and SLO dashboards.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-sre/module/e801ee3d-7ee7-4029-8c2d-b95c6b6bdf7e/lesson/c21406c6-f090-4bae-be7a-72b0140a881a)
