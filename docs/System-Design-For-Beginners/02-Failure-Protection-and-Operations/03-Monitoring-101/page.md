# Monitoring 101

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Failure-Protection-and-Operations/Monitoring-101/page

Overview of monitoring and observability principles, explaining logs metrics and traces, alerting and automation, and common tools for detecting diagnosing and responding to distributed system issues.

Our photo app has evolved into a full distributed system: load balancer, application servers, databases, caches, queues, workers, and object storage. The big question is: how do we know the system is broken or slow before users notice?

Monitoring (part of observability) gives you visibility into the system. It relies on three core signals — logs, metrics, and traces — and you want all three because each answers a different question about behavior and performance.

<Callout icon="lightbulb">
  Monitoring and observability are complementary: monitoring detects and alerts on problems; observability lets you investigate and understand root causes using logs, metrics, and traces.
</Callout>

<Frame>
  <img alt="The image illustrates a system architecture showing the flow from a user's app through load balancer, app servers, cache, and database, while highlighting monitoring components: logs (what happened), metrics (how much/how fast), and traces (where did time go)." />
</Frame>

Quick summary table

| Signal  | Primary question answered       | Example uses                                        |
| ------- | ------------------------------- | --------------------------------------------------- |
| Logs    | What exactly happened?          | Error messages, user actions, event details         |
| Metrics | How much / how fast / how many? | Request rate, latency percentiles, CPU, queue depth |
| Traces  | Where did time go in a request? | Distributed latency breakdown across services       |

## Logs

Logs are timestamped records of discrete events in your application. When something important happens — a user uploads a photo, a cache miss occurs, or a database query fails — your app writes a log line describing the event. Logs answer: what happened, when, and where?

Think of logs as receipts for your system: each line proves a specific event occurred at a given time. Because busy systems emit large volumes of logs, you should ship them to a centralized store so you can search, filter, and correlate events across many machines.

Example log lines:

```text theme={null}
12:04:03 GET /feed user=42 200 38ms
12:04:04 cache hit feed:42
12:04:07 user=42 uploaded photo=99
12:04:08 POST /upload 201 120ms
12:04:09 ERROR database call failed
12:04:09 retry 1/3 db timeout
12:04:11 GET /feed user=88 200 41ms
12:04:12 cache miss feed:88
12:04:13 GET /photo/512 200 22ms
12:04:14 POST /like 201 18ms
```

When an incident occurs, logs give you the detailed story — timestamps, stack traces, and contextual fields — that help you diagnose the root cause.

## Metrics

Metrics are numeric values tracked over time: requests per second, feed latency, cache hit rate, queue depth, CPU usage, or the percentage of error responses. While logs represent single events, metrics aggregate behavior and let you answer: how much load is there? how often are requests failing? is latency trending up?

<Frame>
  <img alt="The image depicts a system architecture diagram with components like a user's app, load balancer, app servers, cache, database, queue, workers, and object storage. Additionally, it displays performance metrics including requests per second, latency, cache hit rate, queue depth, and error percentage." />
</Frame>

Some metrics aggregate millions of events (counters), while others are current-state gauges (e.g., queue length, CPU). Metrics are what you display on dashboards and use for alerting — they surface changes quickly. A good analogy is your car dashboard: it reduces many internal signals into readable numbers (speed, temperature, fuel).

<Frame>
  <img alt="The image shows a system architecture diagram with components like a user's app, load balancer, app servers, cache, database, queue, workers, and object storage. It also features a metrics dashboard displaying sum events, gauge levels, and feed latency." />
</Frame>

Useful metric examples:

* Requests per second (RPS)
* 95th / 99th percentile latency for the feed API
* Cache hit ratio
* Queue depth (number of messages waiting)
* Error rate (percent of 5xx responses)

## Traces

Traces show the end-to-end timing of a single request as it travels through multiple services. When a user upload or feed request slows down, traces let you pinpoint which component added the latency.

Traces are composed of spans. Each span records the start and end time for a unit of work (for example, a database query or an external HTTP call). By assembling spans across services, a trace reveals the critical path — the spans that consumed most of the time.

<Frame>
  <img alt="The image illustrates a simplified server architecture diagram, showing a user's app sending requests through a load balancer to application servers, a cache, and a database, with components like a queue, workers, and object storage. Additionally, it provides trace timing for load balancer, app code, and cache." />
</Frame>

Example: a trace shows 30 ms in app code and 900 ms waiting on a single database call — that immediately points you to the database as the hotspot. Once you know which service is slow, you can use logs and metrics from that service to investigate further.

## Alerts and automation

You don’t want humans staring at dashboards 24/7, so set alerts on the metrics that matter. Alerts trigger when a metric breaches a threshold for some duration and notify the right responder (email, Slack, pager).

Example alert rule:

```text theme={null}
alert if error_rate > 1% for 5m:
  page(on_call)
```

Think of an alert like a smoke detector: it notifies you when something is wrong. Be careful with thresholds and durations: overly sensitive alerts (false positives) cause alert fatigue, while overly lax thresholds delay detection.

<Callout icon="warning">
  Avoid alert fatigue by choosing thresholds and durations that reduce false positives. If alerts are noisy, responders will start ignoring them and real incidents may be missed.
</Callout>

When metrics are reliable, you can automate responses. Auto-scaling is a common example: use metrics (average CPU, request latency, queue depth) to grow or shrink capacity automatically, keeping user experience stable without manual intervention.

<Frame>
  <img alt="The image is a flowchart illustrating a server architecture with a user's app interacting through a load balancer to app servers, cache, and database, featuring autoscaling instructions for server adjustments based on CPU usage." />
</Frame>

## Common jargon and tools

* Observability: the practice of understanding internal system state from external signals.
* Core signals: logs, metrics, traces.
* Dashboard: visual display of important metrics and alerts.
* Alerting: rules that trigger notifications when metrics breach thresholds.

Common tools and ecosystems:

* Metrics: Prometheus (scraping & storage), Grafana (dashboards) — [https://prometheus.io](https://prometheus.io), [https://grafana.com](https://grafana.com)
* Logs: Elasticsearch (indexing & search), commonly used in ELK/EFK stacks — [https://www.elastic.co/elasticsearch](https://www.elastic.co/elasticsearch)
* Tracing: OpenTelemetry instrumentation, with backends such as Jaeger or Grafana Tempo — [https://opentelemetry.io](https://opentelemetry.io), [https://www.jaegertracing.io](https://www.jaegertracing.io), [https://grafana.com/oss/tempo](https://grafana.com/oss/tempo)

<Frame>
  <img alt="The image is a diagram illustrating an application's architecture, including components like app servers, cache, database, and object storage, with a focus on observability tools such as Prometheus, Grafana, Elasticsearch, and OpenTelemetry." />
</Frame>

## Summary

Monitoring combines three complementary signals:

* Metrics: high-level, aggregated indicators that show something is changing.
* Traces: distributed timing that pinpoints where a request spent time.
* Logs: detailed event-level records that explain what happened.

Together, these signals help you detect incidents early, diagnose root causes, and automate responses so users notice problems less often. For next steps, instrument your services for metrics and traces, centralize logs, and create focused dashboards and alerts for the most important user-facing workflows.

Links and references

* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana: [https://grafana.com](https://grafana.com)
* Elasticsearch: [https://www.elastic.co/elasticsearch](https://www.elastic.co/elasticsearch)
* OpenTelemetry: [https://opentelemetry.io](https://opentelemetry.io)
* Jaeger: [https://www.jaegertracing.io](https://www.jaegertracing.io)
* Grafana Tempo: [https://grafana.com/oss/tempo](https://grafana.com/oss/tempo)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/7109fb48-acaa-4566-b95b-9e43a9592708" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/a08be415-3992-4549-96d3-6be1bc1ac88f" />
</CardGroup>
