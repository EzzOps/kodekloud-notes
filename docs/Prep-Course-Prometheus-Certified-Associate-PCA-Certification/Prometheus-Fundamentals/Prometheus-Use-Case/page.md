# Example: download a particular release (replace with the latest or your desired version)
wget https://github.com[AWS_SECRET_ACCESS_KEY]/v2.37.0/prometheus-2.37.0.linux-amd64.tar.gz
```

After downloading, verify the tarball exists:

```bash theme={null}
ls -l
# Example output
# -rw-r--r-- 1 user1 user1 83782323 Jul 14 11:38 prometheus-2.37.0.linux-amd64.tar.gz
```

## 2) Extract the tarball and inspect contents

Extract the downloaded tarball:

```bash theme={null}
tar xvf prometheus-2.37.0.linux-amd64.tar.gz
```

Move into the extracted directory and list its contents:

```bash theme={null}
cd prometheus-2.37.0.linux-amd64/
ls -l
# Example output:
# drwxr-xr-x 2 user1 user1  4096 Jul 14 11:30 console_libraries
# drwxr-xr-x 2 user1 user1  4096 Jul 14 11:30 consoles
# -rw-r--r-- 1 user1 user1 11357 Jul 14 11:30 LICENSE
# -rw-r--r-- 1 user1 user1  3773 Jul 14 11:30 NOTICE
# -rwxr-xr-x 1 user1 user1 109655433 Jul 14 11:30 prometheus
# -rw-r--r-- 1 user1 user1   934 Jul 14 11:30 prometheus.yml
# -rwxr-xr-x 1 user1 user1 101469395 Jul 14 11:18 promtool
```

What each important file is for:

* `prometheus` — the Prometheus server executable.
* `prometheus.yml` — the main configuration file; defines scrape targets and jobs.
* `promtool` — CLI utility to validate configuration and assist with rule files.
* `consoles/` and `console_libraries/` — optional UI console templates.

## 3) Start the Prometheus server

From the extracted directory run:

```bash theme={null}
./prometheus
```

You should see logs indicating the server and TSDB started, the configuration file was loaded, and the HTTP server is ready. Example lines:

```bash theme={null}
ts=2022-09-02T03:25:25.910Z caller=main.go:996 level=info msg="TSDB started"
ts=2022-09-02T03:25:25.910Z caller=main.go:1177 level=info msg="Loading configuration file" filename=prometheus.yml
ts=2022-09-02T03:25:25.910Z caller=main.go:957 level=info msg="Server is ready to receive web requests."
ts=2022-09-02T03:25:25.910Z caller=manager.go:941 level=info component="rule manager" msg="Starting rule manager..."
```

<Callout icon="warning">
  If running on a remote machine, ensure port `9090` is reachable (open in firewall/security group) before connecting with a browser. Also avoid running Prometheus as root; use a dedicated user for production deployments.
</Callout>

## 4) Verify via the web UI and a simple query

Open a browser to the Prometheus web UI:

* Local: `http://localhost:9090`
* Remote: `http://<PROMETHEUS_HOST_IP>:9090`

The default web expression browser lets you execute PromQL queries. To verify Prometheus is scraping itself, run the simplest query:

```text theme={null}
up
```

You should see a result similar to:

`up{instance="localhost:9090", job="prometheus"}`

A value of `1` indicates the target is up; `0` indicates down.

## Visual: Prometheus website and download block

Here’s the Prometheus website download block where you choose the binary and version:

<Frame>
  <img alt="The image is a screenshot of the Prometheus website, featuring information about their open-source monitoring solution and a statement condemning Russia's invasion of Ukraine." />
</Frame>

And the releases page listing precompiled binaries and checksums (select the correct OS/arch and copy the link address for wget):

<Frame>
  <img alt="The image shows a download page for Prometheus, listing precompiled binaries for different operating systems and architectures. It includes versions, file sizes, and SHA256 checksums for Prometheus components like alertmanager and others." />
</Frame>

## Quick reference table

| Resource          |                                 Default / Example | Notes                                      |
| ----------------- | ------------------------------------------------: | ------------------------------------------ |
| Web UI port       |                                           `:9090` | Access via `http://<host>:9090`            |
| Config file       |                                  `prometheus.yml` | Located in the extracted directory         |
| Prometheus binary |                                    `./prometheus` | Start the server from the extracted folder |
| Promtool          |                                        `promtool` | Validate config and rules                  |
| Example PromQL    | `up{instance="localhost:9090", job="prometheus"}` | `1` = up, `0` = down                       |

## Useful links and references

* Prometheus download page: [https://prometheus.io/download/](https://prometheus.io/download/)
* Prometheus documentation (configuration & PromQL): [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Prometheus GitHub releases: [https://github.com/prometheus/prometheus/releases](https://github.com/prometheus/prometheus/releases)

Follow these steps to get a local Prometheus server running quickly. Once confirmed, you can customize `prometheus.yml` to add scrape targets and integrate Alertmanager, Grafana, or other monitoring components.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/056381b5-99b2-4e68-b7c1-d2361c9c3308" />
</CardGroup>


# Prometheus Use Case

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Use-Case/page

Overview of Prometheus production use cases including metric aggregation across sites, alerting for resource exhaustion, and correlating application metrics to identify performance thresholds.

In this lesson we cover three common Prometheus production use cases: aggregating metrics across locations, alerting on resource exhaustion, and correlating application metrics to identify performance thresholds. These examples show why Prometheus is widely adopted for monitoring and how teams typically operate it in real environments.

Start with a common scenario: multiple data centers across the country plus workloads in a cloud provider (for example, [AWS](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs)). Your goal is a single, unified view of key metrics from all locations—CPU, memory, request latency, error rates, and more.

Prometheus can collect and present this data. Typical deployment patterns include running one Prometheus instance per site or environment, then aggregating metrics with federation or centralizing them via `remote_write` to a long-term store. Prometheus also includes a built-in expression browser and graphing UI for quick exploration. For richer dashboards, teams commonly pair Prometheus with [Grafana](https://learn.kodekloud.com/user/courses/grafana-loki).

<Frame>
  <img alt="The image illustrates a network diagram with data centers (West DC, Central DC, East DC) and AWS, connected to a central dashboard displaying various graphs and charts." />
</Frame>

All of that data can be displayed on a single dashboard by scraping instrumented services or exporters at each location and aggregating results using one of the approaches below.

| Aggregation approach                      |                                                                         When to use | Key trade-offs                                                                        |
| ----------------------------------------- | ----------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------- |
| Per-site Prometheus + federation          |                       Multiple independent sites with occasional cross-site queries | Simpler isolation, lower coupling; federation can be complex for global queries       |
| Centralized remote write (`remote_write`) | Long-term storage (clickhouse, Cortex, Thanos, VictoriaMetrics) and unified queries | Enables high-availability and long retention, but adds external storage/manageability |
| Hybrid (federation + remote\_write)       |                                       Mix of local alerting and long-term analytics | Balances local resilience with centralized analytics                                  |

## Use case 2: Alerting on memory saturation

Imagine repeated outages caused by high memory usage on the MySQL host. The operations team wants alerts (email, Slack, PagerDuty) when memory usage hits 80% so they can intervene before users are affected.

Prometheus evaluates alerting rules (PromQL) and emits alerts when conditions are true. Alertmanager receives those alerts and handles deduplication, grouping, inhibition, and delivery to receivers such as email, Slack, or PagerDuty.

<Frame>
  <img alt="The image outlines a use case involving server memory issues, where the operations team wants to be notified via email when memory usage reaches 80% capacity to take proactive measures. Diagrams illustrate a process from server monitoring to email notification." />
</Frame>

A straightforward alerting rule for high memory usage:

```yaml theme={null}
groups:
- name: node.rules
  rules:
  - alert: HighMemoryUsage
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 80
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High memory usage on `{{ $labels.instance }}`"
      description: "Memory usage is above 80% for more than 5 minutes on `{{ $labels.instance }}`."
```

<Callout icon="lightbulb">
  Prometheus evaluates alerting rules; Alertmanager is responsible for routing and delivering alerts to channels (email, Slack, PagerDuty, SMS). Configure Alertmanager receivers and routing rules to control notification behavior and silence management.
</Callout>

## Use case 3: Finding the upload size where latency degrades

You’ve shipped a video upload feature and need to know the file size at which request latency begins to increase noticeably. The recommended approach:

* Instrument the application to expose upload metrics:
  * Use a histogram for request durations, e.g. `upload_request_duration_seconds_bucket`.
  * Record upload sizes as a gauge or histogram (e.g., `upload_size_bytes`).
  * Attach meaningful labels (endpoint, status\_code, instance) when appropriate.
* Scrape these metrics with Prometheus and visualize them in Grafana or the Prometheus expression browser.
* Use PromQL to correlate average upload size and latency over time.

Useful PromQL examples:

* Average upload size over the last 5 minutes (if each upload reports `upload_size_bytes` as a per-request gauge):

```promql theme={null}
avg_over_time(upload_size_bytes[5m])
```

* 95th percentile request duration over the last 5 minutes (based on a histogram named `upload_request_duration_seconds_bucket`):

```promql theme={null}
histogram_quantile(0.95, sum(rate(upload_request_duration_seconds_bucket[5m])) by (le))
```

Plot both series on a dashboard to visually identify the file-size range where latency increases. You can also create an alert that fires only when both average size and high latency occur together:

```promql theme={null}
(
  avg_over_time(upload_size_bytes[5m]) > 50 * 1024 * 1024
)
and
(
  histogram_quantile(0.95, sum(rate(upload_request_duration_seconds_bucket[5m])) by (le)) > 2
)
```

This expression becomes true when the 5-minute average upload size exceeds 50 MiB and the 95th-percentile latency exceeds 2 seconds.

<Callout icon="warning">
  When combining vector results with logical operators (for example `and`), ensure the vectors have compatible label sets. Use aggregation or vector matching (for example, `on(instance)`) to align labels so the compound expression behaves as intended.
</Callout>

## Putting it all together

Prometheus supports the full workflow for these use cases:

* Distributed collection and aggregation: run per-site Prometheus instances and consolidate with federation or `remote_write`.
* Alerting: express rules in PromQL, evaluate them in Prometheus, and manage delivery through Alertmanager.
* Instrumentation-driven observability: use histograms for latency and size, counters for counts, and gauges for instantaneous values to correlate metrics and drive data-informed decisions.

Recommended checklist for production readiness:

* Instrument services with appropriate metric types (histogram for latency, gauge for sizes, counters for totals).
* Scrape application endpoints and exporters reliably (configure scrape intervals and relabeling).
* Define and test PromQL queries in the expression browser and dashboards.
* Create alerting rules with appropriate `for` durations to avoid flapping.
* Configure Alertmanager routes and receivers for on-call workflows.
* Choose aggregation/retention strategy (federation vs `remote_write`) based on query needs and retention requirements.

Links and references

* [Prometheus documentation](https://prometheus.io/docs/)
* [Alertmanager documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [PromQL quick reference](https://prometheus.[SECRET_REDACTED]/)
* [Grafana](https://learn.kodekloud.com/user/courses/grafana-loki)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/d5b034d7-fd50-4ae1-89f0-586162a6be6e" />
</CardGroup>
