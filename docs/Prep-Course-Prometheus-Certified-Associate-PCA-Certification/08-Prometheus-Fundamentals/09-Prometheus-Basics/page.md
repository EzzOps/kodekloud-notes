# Prometheus Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Basics/page

Overview of Prometheus fundamentals including metric collection, TSDB storage, PromQL queries, exporters, and Alertmanager alerting

In this guide you'll learn the fundamentals of Prometheus: what it is, how it collects metrics, where it fits in an observability stack, and a few concrete configuration and exposition examples to get started.

Prometheus is an open-source monitoring and alerting toolkit that:

* Collects numeric time-series metrics from configured targets.
* Stores metrics in a local time-series database (TSDB) optimized for high-write, high-query workloads.
* Provides a powerful query language, PromQL, for aggregating and analyzing time-series data.
* Integrates with an alerting pipeline (Alertmanager) to route notifications when metrics cross thresholds.

Prometheus uses a pull-based scrape model: it periodically sends HTTP GET requests to configured targets that expose metrics (commonly at the `/metrics` HTTP path). Scraped samples are persisted in the local TSDB and can be queried with PromQL or visualized in tools like Grafana.

<Frame>
  <img alt="The image provides a description of Prometheus, an open-source monitoring tool that collects metrics data, enables alert generation, scrapes metrics from targets via HTTP, and stores them in a time series database for querying with PromQL." />
</Frame>

What you can query with PromQL
Prometheus focuses on numeric time-series data. Common queries include rates, aggregates, and quantiles over sliding time windows. Use PromQL to compute things like request rates, error ratios, or p95 latency across services.

What kinds of metrics can Prometheus monitor?

Prometheus is flexible and commonly collects:

* Host and OS metrics: CPU, memory, disk, and network statistics.
* Service metrics: uptime, request/sec, error rates, and latency percentiles (p50/p95/p99).
* Application/business metrics: exceptions, queue depth, job counts, revenue metrics.

Because Prometheus stores numeric time series, you can compute derivative metrics (e.g., per-second rates), windowed aggregates, and quantiles using PromQL.

<Frame>
  <img alt="The image lists metrics that Prometheus can monitor, including CPU/memory utilization, disk space, service uptime, and application-specific data like exceptions, latency, and pending requests." />
</Frame>

Common metric ingestion patterns

* Instrument code directly using a Prometheus client library (Go, Java, Python, Ruby, etc.).
* Use exporters for systems that cannot be instrumented natively (for example, `node_exporter` for host metrics, `blackbox_exporter` for probing endpoints, or database exporters).
* Use Pushgateway for short-lived batch jobs that cannot be scraped periodically.

Prometheus is purpose-built for numeric time-series monitoring. It is not a replacement for log management or distributed tracing—use specialized tools for logs/traces and integrate them into your observability pipeline.

<Frame>
  <img alt="The image is an informative slide discussing Prometheus, which monitors numeric time-series data and lists types of data it should not monitor: events, system logs, and traces." />
</Frame>

<Callout icon="lightbulb">
  Prometheus includes an [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) component for routing notifications (email, PagerDuty, Slack, etc.). For long-term metric retention beyond Prometheus' local TSDB retention window, integrate remote storage solutions using Prometheus' `remote_write`/`remote_read` APIs.
</Callout>

Quick example: Prometheus scrape configuration

```yaml theme={null}
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'my-app'
    static_configs:
      - targets: ['my-app:8080']
```

Example: Prometheus text exposition format

```text theme={null}
