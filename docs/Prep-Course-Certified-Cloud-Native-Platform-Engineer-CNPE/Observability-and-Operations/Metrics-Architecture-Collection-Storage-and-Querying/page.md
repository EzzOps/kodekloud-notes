# Metrics Architecture Collection Storage and Querying

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Metrics-Architecture-Collection-Storage-and-Querying/page

Overview of Prometheus metrics architecture, collection, metric types, labeling, PromQL querying and Kubernetes integration for reliable, scalable observability and consistent dashboards

Metrics are the first pillar of observability — they answer "what is happening" in your system. Collecting metrics at scale, however, introduces challenges: fragmentation, inconsistent labeling, and difficulty correlating signals across components.

By the end of this lesson you'll understand how Prometheus collects metrics, the three primary metric types and when to use each, how labels enable multi-dimensional queries, and enough PromQL to build Grafana dashboards and alerts.

<Frame>
  <img alt="The image lists learning objectives related to metrics collection and Prometheus, including understanding architectures, the pull-based model, differentiating metric types, using labels, and writing PromQL queries." />
</Frame>

## Why consistent labeling matters — a concrete example

A logistics platform ran 60 microservices across three Kubernetes clusters. Each team chose different metric approaches. During a database connection-pool exhaustion incident, the platform team needed to correlate:

* API error rates
* Database connection counts
* Pod memory usage

Those metrics existed across three different systems, with different time granularities and distinct label sets — there was no reliable way to join them. What should have been a five-minute correlation became a ninety-minute merge of spreadsheets.

After migrating to Prometheus and enforcing consistent labeling, the same correlation was a single-line PromQL query and returned instant results.

<Frame>
  <img alt="The image illustrates three teams handling microservices, with respective tasks and time taken: Team 1 pushed StatsD to Graphite in 10 seconds, Team 2 exposed JSON endpoints in 30 seconds, and Team 3 adopted Prometheus exporters in 60 seconds." />
</Frame>

## The problem: data everywhere

Without a unified approach you get:

* No single source of truth
* Format fragmentation
* Push-sprawl
* Difficult correlation and inconsistent dashboards

A unified collection architecture prevents multiple dashboards from telling different stories about the same incident. Prometheus is the de-facto standard for that unified approach.

<Frame>
  <img alt="The image outlines common types of metrics teams have and explains why these metrics setups often fail, highlighting issues like lack of a single source of truth, format fragmentation, push sprawl, and lack of correlation." />
</Frame>

## Prometheus architecture — four conceptual layers

Prometheus provides a predictable, Kubernetes-native collection model. Conceptually it has four layers:

* Targets: applications expose a `/metrics` HTTP endpoint.
* Service discovery: finds targets automatically (Kubernetes, Consul, etc.).
* Prometheus server: scrapes targets and stores time-series samples in its TSDB.
* PromQL: queries the time-series database for analysis, dashboards, and alerts.

Why pull instead of push?

* Central control: scrape intervals and targets are controlled centrally.
* Health detection and debugging: if a target stops responding, Prometheus notices immediately and you can inspect the exact `/metrics` output.

Operational benefits:

* No client-side scrape scheduling
* Easier debugging (query the target directly)
* Strong Kubernetes-native integration

<Callout icon="warning">
  Prometheus is primarily pull-based. For short-lived batch jobs that can't be scraped, the official escape hatch is the Pushgateway. Use Pushgateway sparingly — it’s an exception, not the default pattern. See the Prometheus push practices for details: [https://prometheus.io/docs/practices/pushing/](https://prometheus.io/docs/practices/pushing/)
</Callout>

<Frame>
  <img alt="The image is a diagram explaining Prometheus' pull-based collection process, highlighting components like scrape targets, service discovery, time series database, and PromQL. It also lists benefits such as central control, health monitoring, no client-side configuration, ease of debugging, and Kubernetes-native features." />
</Frame>

## Metric types — what to use and how to query them

Choosing the correct metric type and query pattern is critical. Applying the wrong PromQL function to a metric type is the most common mistake.

| Metric Type | What it answers                                                                     | How to compute/query                                                                | Notes / Example                                                                                                   |
| ----------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Counter     | "How many" (monotonic, non-decreasing)                                              | Use range-vector functions: `rate()` (per-second) or `increase()` over a window     | Counters can reset on restart — `rate()` and `increase()` handle resets. Example: `rate(http_requests_total[5m])` |
| Gauge       | "How much right now" (can increase/decrease)                                        | Query instant value directly or use other non-monotonic functions                   | Do not use `rate()` on gauges. Example: `container_memory_usage_bytes{namespace="production"}`                    |
| Histogram   | "How long" or distribution (bucketed cumulative counters, plus `_count` and `_sum`) | Apply `rate()` to `_bucket` counters and use `histogram_quantile()` for percentiles | Example: `histogram_quantile(0.95, sum by (le) (rate(request_duration_seconds_bucket[5m])))`                      |

Key rules:

* Avoid `rate()` on gauges — use the raw gauge or appropriate functions.
* To interpret counters, always use `rate()` or `increase()`.
* For histograms, operate on the bucket counters (often with `rate()`) and use `histogram_quantile()` for percentiles.

<Frame>
  <img alt="The image describes three types of metrics: Counter, Gauge, and Histogram, each explaining their function, example, and query usage." />
</Frame>

## Labels: dimensionality by design

Labels are one of Prometheus’s most powerful features. Without labels you’d need a unique metric name for every dimension combination — that doesn’t scale. Labels let you:

* Filter subsets (e.g., by `namespace`, `pod`, `service`)
* Group and aggregate (e.g., `sum by (service)`)
* Correlate metrics across services when labels are consistent

Kubernetes injects many useful labels automatically (for example, `namespace`). Establish platform-wide labeling conventions (team, service, environment) to make cross-service queries straightforward.

## PromQL patterns you’ll use daily

PromQL can look intimidating, but most needs are covered by three patterns:

1. Instant vector — current values
2. Range vector + function — rates/changes over time
3. Aggregation — group and summarize by labels

Examples:

```promql theme={null}
