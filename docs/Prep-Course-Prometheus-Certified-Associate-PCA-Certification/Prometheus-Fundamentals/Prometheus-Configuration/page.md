# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",handler="/api"} 1027

# HELP cpu_seconds_total Total user and system CPU time spent in seconds
# TYPE cpu_seconds_total counter
cpu_seconds_total{cpu="0"} 12345.67
```

Metric types and when to use them

| Metric type | Purpose                                                    | Typical use cases                            |
| ----------- | ---------------------------------------------------------- | -------------------------------------------- |
| Counter     | Monotonically increasing value; only increases (or resets) | Total requests served: `http_requests_total` |
| Gauge       | Value that can go up or down                               | Current memory usage or temperature          |
| Histogram   | Buckets observations and counts/sums for quantiles         | Request latency distributions                |
| Summary     | Client-side quantiles and counts over sliding time windows | Percentile latency at the client side        |

Prometheus components at a glance

| Component         | Role                                                     | Notes / Links                                                                     |
| ----------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Prometheus server | Scrapes targets and stores metrics in the TSDB           | Query with PromQL                                                                 |
| Alertmanager      | Receives alerts from Prometheus and routes notifications | See [Alertmanager docs](https://prometheus.io/docs/alerting/latest/alertmanager/) |
| Exporters         | Translate non-Prometheus data into metrics               | Examples: `node_exporter`, `blackbox_exporter`                                    |
| Pushgateway       | Accepts push metrics for short-lived jobs                | Not intended for service metrics                                                  |

A few additional technical notes

* Service discovery: Prometheus supports multiple discovery mechanisms (Kubernetes, Consul, EC2, DNS) so targets can be discovered dynamically.
* Alerting rules: Define rules in Prometheus to evaluate conditions and send alerts to Alertmanager for notification and silencing.
* Retention and remote storage: Prometheus' local TSDB is optimized for recent data. For long-term retention, use compatible remote storage backends via `remote_write`/`remote_read`.
* Choosing metric types: Use counters for totals, gauges for instantaneous values, histograms/summaries for latency distributions.

Background and further reading
Prometheus originated at SoundCloud and joined the Cloud Native Computing Foundation (CNCF) in 2016. It is implemented primarily in Go. For full documentation, client libraries, and exporter examples, see the official Prometheus docs: `https://prometheus.io/docs/`.

Links and references

* [Prometheus querying basics (PromQL)](https://prometheus.[SECRET_REDACTED]/)
* [Grafana](https://grafana.com/)
* [node\_exporter](https://github.com/prometheus/node_exporter)
* [blackbox\_exporter](https://github.com/prometheus/blackbox_exporter)
* [Pushgateway](https://github.com/prometheus/pushgateway)
* [Prometheus documentation](https://prometheus.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/72d69aea-73bd-4d4c-b112-fafe324761d5" />
</CardGroup>


# Prometheus Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Configuration/page

How to configure Prometheus scrape jobs and global settings, examples, authentication, reloading, and verifying targets in the UI

Once Prometheus is installed and one or more hosts are exposing metrics, you must configure Prometheus so it knows which targets to scrape. Prometheus uses a pull model: the server is explicitly configured to retrieve metrics from targets. These settings live in the Prometheus YAML configuration file (commonly `/etc/prometheus/prometheus.yml`).

Example minimal Prometheus config:

```yaml theme={null}
