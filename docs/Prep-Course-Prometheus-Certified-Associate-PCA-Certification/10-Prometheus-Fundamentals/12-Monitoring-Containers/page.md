# HELP node_disk_discard_time_seconds_total This is the total number of seconds spent by all discards.
# TYPE node_disk_discard_time_seconds_total counter
node_disk_discard_time_seconds_total{device="sda"} 0
node_disk_discard_time_seconds_total{device="sr0"} 0
```

> **lightbulb** Including `# HELP` and `# TYPE` in your exporters makes metrics easier to understand and reduces ambiguity when other engineers query or consume them.

## Metric types

Prometheus defines four primary metric types. Here’s a concise reference you can use when designing instrumentation.

| Type      | Description                                                                                                                                                         | Typical use cases                                          | Example                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| Counter   | Cumulative metric that only increases (or resets on restart).                                                                                                       | Total requests, error counts, job executions.              | `node_cpu_seconds_total{cpu="0",mode="idle"} 258277.86` |
| Gauge     | Value that can go up and down.                                                                                                                                      | Current memory usage, temperature, concurrent connections. | `process_resident_memory_bytes 1.23e+07`                |
| Histogram | Observations grouped into configurable cumulative buckets; also exports a `_count` and `_sum`. Useful for aggregating distributions across instances.               | Response time distributions, payload sizes.                | `http_request_duration_seconds_bucket{le="0.5"} 240`    |
| Summary   | Tracks event counts, sum, and client-side computed quantiles (percentiles). Quantiles are computed per-instance and cannot be aggregated reliably across instances. | Latency percentiles on a single instance.                  | `http_request_duration_seconds{quantile="0.5"} 0.12`    |

Histograms collect counts for bucket boundaries (buckets are cumulative). For example, with buckets 0.2s, 0.5s, 1s you get counts of requests that completed in less than 0.2s, less than 0.5s (including those under 0.2s), and less than 1s (including those under 0.5s):

<Frame>
  <img alt="The image is an infographic about histograms, displaying response time and request size metrics along with a bar chart illustrating response time buckets." />
</Frame>

Summaries report quantiles directly (for example 20%, 50%, 80%) and are calculated on the client side. Because quantiles in summaries are per-instance they are not directly aggregatable across multiple instances the way histogram bucket counts are.

<Frame>
  <img alt="The image is a summary slide comparing histogram-like data tracking, showing percentiles for response time and request size, with a bar chart illustrating response time percentiles." />
</Frame>

## Metric names and labels

Metric names should be descriptive and follow Prometheus naming conventions: ASCII letters, numbers, underscores, and colons. Avoid colons in custom metrics — they are typically reserved for recording rules.

Labels are key/value pairs that further qualify a metric and let you slice and group metrics by attributes such as `path`, `method`, or `instance`. Label names may include ASCII letters, numbers, and underscores.

Why labels are useful — a brief example:

A naive approach would create separate metrics per endpoint:

```text theme={null}
requests_auth_total
requests_user_total
requests_cart_total
```

This approach makes it hard to compute totals without knowing each metric name. A better approach uses a single metric with a `path` label:

```text theme={null}
requests_total{path="/auth"}  123
requests_total{path="/user"}  456
requests_total{path="/cart"}  78
```

You can then compute totals or grouped sums with PromQL:

```promql theme={null}
sum(requests_total)
sum(requests_total) by (path)
```

Add other labels as needed (for example `method="GET"`). Each unique combination of label keys and values creates a distinct time series.

<Frame>
  <img alt="The image illustrates a comparison of two methods for calculating total API requests in an e-commerce app, highlighting the difficulty of calculating total requests across all paths versus summing requests using a specific method with labeled paths." />
</Frame>

Internally, Prometheus stores the metric name as a label called `__name__`. Example:

```text theme={null}
node_cpu_seconds_total{cpu="0"} = {__name__="node_cpu_seconds_total", cpu="0"}
```

Labels that begin and end with double underscores (for example `__name__`) are internal to Prometheus.

Prometheus also automatically assigns two labels to every scraped metric:

* `instance` — the target address that was scraped.
* `job` — the scrape job name from your Prometheus configuration.

Example scrape job in `prometheus.yml`:

```yaml theme={null}
scrape_configs:
  - job_name: "node"
    scheme: https
    basic_auth:
      username: prometheus
      password: password
    static_configs:
      - targets:
          - "192.168.1.168:9100"
```

> **warning** Avoid high-cardinality labels (for example, user IDs, session IDs, or highly variable full request paths). Every distinct label value combination creates a new time series, which can quickly exhaust memory and storage in Prometheus.

## Quick references and further reading

* Prometheus data model and time series: [Prometheus concepts — data model](https://prometheus.io/docs/concepts/data_model/)
* Node Exporter guide: [Node Exporter](https://prometheus.io/docs/guides/node-exporter/)
* Convert Unix timestamps: [Epoch Converter](https://www.epochconverter.com/)

Keep these practical rules in mind:

* Use meaningful metric names.
* Favor labels over separate metric names when the distinguishing characteristic is a dimension (e.g., `path`, `method`).
* Choose histograms if you need to aggregate distributions across instances; use summaries for per-instance quantiles when aggregation across instances is not required.
* Design labels to keep cardinality manageable.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/4a67d30f-a156-41e2-8718-30942784652e)


# Monitoring Containers

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Monitoring-Containers/page

Guide to monitoring Docker and containers with Prometheus using Docker Engine metrics and cAdvisor for per container resource visibility, setup, scraping, and troubleshooting

We previously configured Prometheus to collect metrics from Linux hosts. This guide extends that setup to containerized environments. You can collect two complementary metric sets:

* Docker Engine metrics — metrics about the Docker daemon/engine itself.
* Per-container metrics — detailed container-level CPU, memory, filesystem, and process information exposed by cAdvisor.

Collecting both provides full-stack observability: engine-level health and per-container resource usage.

<Frame>
  <img alt="The image is an illustration of container metrics, showing how metrics can be scraped from containerized environments using Docker Engine and cAdvisor. It includes visual elements of servers, containers, and a monitoring icon." />
</Frame>

## 1. Enable Docker Engine metrics

Docker can expose runtime metrics directly from the daemon. This is useful for monitoring the Docker engine itself (daemon CPU, errors, image/operation counts, etc.), and is configured on the host running Docker.

Create or edit `/etc/docker/daemon.json` and add the metrics address and enable experimental features:

```json theme={null}
{
  "metrics-addr": "127.0.0.1:9323",
  "experimental": true
}
```

> **lightbulb** Exposing Docker metrics via the daemon is an experimental feature. Use it for testing or in environments where experimental features are acceptable.

Restart Docker and verify the metrics endpoint is reachable:

```bash theme={null}
