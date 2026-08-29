# Replace the URL below with the exact URL you copied for your chosen version/arch
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz

tar xvf node_exporter-1.3.1.linux-amd64.tar.gz
cd node_exporter-1.3.1.linux-amd64
./node_exporter
```

When Node Exporter starts successfully, it logs the enabled collectors and the listening address. By default it listens on port 9100.

Example log output:

```plaintext theme={null}
level=info ts=2022-09-05T16:51:59.947Z caller=node_exporter.go:199 msg="Listening on" address=:9100
level=info ts=2022-09-05T16:51:59.947Z caller=tls_config.go:195 msg="TLS is disabled." http2=false
```

Verify the metrics endpoint is responding:

```bash theme={null}
curl localhost:9100/metrics
```

Example snippet of the metrics output:

```plaintext theme={null}
# TYPE node_timex_tick_seconds gauge
node_timex_tick_seconds 0.01
# HELP node_udp_queues Number of allocated memory in the kernel for UDP datagrams in bytes.
# TYPE node_udp_queues gauge
node_udp_queues{ip="v4",queue="rx"} 1
node_udp_queues{ip="v4",queue="tx"} 0
node_udp_queues{ip="v6",queue="rx"} 0
node_udp_queues{ip="v6",queue="tx"} 0
# HELP node_uname_info Labeled system information as provided by the uname system call.
# TYPE node_uname_info gauge
node_uname_info{domainname="(none)",machine="x86_64",nodename="user2",release="5.15.0-52-generic",sysname="Linux",version="#58-Ubuntu SMP Thu Oct 13 08:03:55 UTC 2022"} 1
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 0.148576e+06
```

The metrics endpoint includes many metrics collected by Node Exporter (CPU, memory, network, disk, kernel stats, etc.). Prometheus can scrape this endpoint to ingest those metrics.

If you prefer to pick the artifact from the website UI, right-click the specific Node Exporter artifact on the Prometheus download page and copy its link address, then use `wget` with that URL.

<Frame>
  <img alt="The image shows a list of downloadable software packages for &#x22;node_exporter,&#x22; &#x22;promlens,&#x22; &#x22;pushgateway,&#x22; and &#x22;statsd_exporter,&#x22; including details such as version, OS, architecture, size, and SHA256 checksum." />
</Frame>

> **warning** Exposing the metrics endpoint publicly can leak system details. Restrict access with a firewall, network ACLs, or run Node Exporter behind a VPN. Consider removing or protecting sensitive metrics if necessary.

## Add Node Exporter to Prometheus scrape targets

After Node Exporter is running and reachable on port 9100, add the host as a scrape target in your `prometheus.yml` under `scrape_configs`. Example:

```yaml theme={null}
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['my-host.example.com:9100']
```

You can also view the metrics in a browser at `http://<host>:9100/metrics` for a human-readable listing.

## Useful commands and tips

| Task                     | Command / Example                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Download release         | `wget https://github.com/prometheus/node_exporter/releases/download/<VERSION>/node_exporter-<VERSION>.linux-amd64.tar.gz` |
| Extract archive          | `tar xvf node_exporter-<VERSION>.linux-amd64.tar.gz`                                                                      |
| Run directly             | `./node_exporter`                                                                                                         |
| Verify metrics endpoint  | `curl localhost:9100/metrics`                                                                                             |
| Add to Prometheus        | Edit `prometheus.yml` and add a `scrape_configs` entry as shown above                                                     |
| Verify Prometheus target | Visit `http://<prometheus-host>:9090/targets`                                                                             |

## Running Node Exporter as a service (optional)

To run Node Exporter continuously, create a systemd unit (or equivalent init script) that starts the `node_exporter` binary at boot. Ensure the service runs with least privileges and that metrics access is restricted as needed.

## Links and references

* Prometheus Downloads: [https://prometheus.io/download/](https://prometheus.io/download/)
* Node Exporter GitHub releases: [https://github.com/prometheus/node\_exporter/releases](https://github.com/prometheus/node_exporter/releases)
* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/ee3d2e8d-dead-4416-9124-c1da510fa630)


# Prometheus Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Architecture/page

Overview of Prometheus monitoring architecture and ecosystem, covering server components, exporters, client libraries, pull versus push models, service discovery, Alertmanager, Pushgateway, PromQL and Grafana.

This lesson explains the Prometheus architecture, its core components, and how the wider Prometheus ecosystem fits together.

Prometheus server (the Prometheus core) is built from three primary components:

| Component                       | Responsibility                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------- |
| Data retrieval worker (scraper) | Periodically polls targets’ `\`/metrics\`\` endpoints and collects metrics.                 |
| Time series database (TSDB)     | Stores scraped metrics as time-series data optimized for high write volume and compression. |
| HTTP server / query layer       | Exposes the Prometheus HTTP API and UI for queries (PromQL) and visualization.              |

The scraper discovers and polls targets, the TSDB persists the collected metrics, and the HTTP/query layer lets you query and visualize stored metrics using `PromQL`.

Prometheus is more than a single server — it’s an ecosystem of exporters, client libraries, discovery mechanisms, alerting integrations, and visualization tools that interact to provide full monitoring and alerting capabilities.

<Frame>
  <img alt="The image is a diagram depicting the Prometheus architecture, showing components like exporters, Pushgateway, service discovery, Alertmanager, and how they interact with each other and external services." />
</Frame>

Exporter processes

Most systems and applications do not expose Prometheus-formatted metrics by default on a `\`/metrics\`\` endpoint. Exporters are lightweight processes that:

* Collect internal metrics from an application or system.
* Convert those metrics into Prometheus’ exposition format.
* Expose the metrics on an HTTP endpoint (typically `\`/metrics\`\`) so Prometheus can scrape them.

Exporters can run alongside the instrumented application (sidecars), be deployed per host (node/host exporters), or run centrally depending on your architecture and requirements.

<Frame>
  <img alt="The image illustrates how exporters collect and expose metrics from systems in a format that Prometheus expects, due to targets not listening on the /metrics endpoint by default. It includes a diagram showing the flow from services through exporters to Prometheus using HTTP requests." />
</Frame>

Native exporters

There are many official and community exporters for common software and infrastructure. These reduce the need to instrument systems yourself.

| Exporter           | Typical use case                                |
| ------------------ | ----------------------------------------------- |
| `node_exporter`    | Linux host metrics (CPU, memory, disk, network) |
| `windows_exporter` | Windows server metrics                          |
| `mysqld_exporter`  | MySQL/MariaDB metrics                           |
| `apache_exporter`  | Apache HTTP Server metrics                      |
| `haproxy_exporter` | HAProxy metrics                                 |

These exporters let you collect OS- and application-level metrics without changing the target’s code.

<Frame>
  <img alt="The image lists several native exporters for Prometheus, including Node exporters (Linux servers), Windows, MySQL, Apache, and HAProxy." />
</Frame>

Client libraries

For domain-specific metrics (error counts, request latencies, job durations, custom counters/gauges/histograms), embed a Prometheus client library in your application. Official and community libraries are available for many languages:

* Go, Java, Python, Ruby, Rust (official or widely used libraries).
* Third-party libraries for additional languages and frameworks.

Instrumenting your application lets it expose business or application-level metrics directly on `\`/metrics\`\` to be scraped by Prometheus.

<Frame>
  <img alt="The image is about monitoring application metrics using Prometheus client libraries, which support languages like Go, Java, Python, Ruby, and Rust. It mentions tracking errors, request latency, and job execution time." />
</Frame>

Pull vs push model

Prometheus primarily uses a pull-based model:

* The Prometheus server initiates HTTP requests to targets’ `\`/metrics\`\` endpoints on a schedule.
* Prometheus must therefore know which targets to monitor (via static config or service discovery).
* Pull models make it straightforward to detect failed scrapes (i.e., target is down) and to maintain a canonical list of targets.

Other monitoring systems also use pull-based approaches (for example, Zabbix, Nagios).

<Frame>
  <img alt="The image illustrates Prometheus's pull-based model for monitoring, showing its interaction with targets and noting other similar solutions like Zabbix and Nagios." />
</Frame>

Push-based systems

Push-based monitoring has targets send metrics directly to a central collector. Examples and use cases include:

* Graphite, OpenTSDB (typical push-capable setups).
* Logstash or custom metric collectors that accept pushed metrics/events.

Use push when the target cannot be reliably scraped (e.g., firewalled, behind NAT, or extremely short-lived jobs).

<Frame>
  <img alt="The image illustrates a &#x22;Push Based Model&#x22; for monitoring, where targets send metric data to a server. It mentions systems like Logstash, Graphite, and OpenTSDB." />
</Frame>

Benefits of pull-based monitoring

* Clear detection of target availability: failed scrape vs intentionally removed target.
* Prevents uncontrolled inbound connections from newly online devices that could overwhelm a central server.
* Maintains a centralized source of truth for monitored targets (static config + service discovery).

<Frame>
  <img alt="The image lists benefits of using a pull-based system, highlighting ease in detecting downtime, avoiding server overload, and maintaining a definitive monitoring list." />
</Frame>

When to use push

* Push is appropriate for short-lived, ephemeral jobs (batch jobs, short-lived containers) that terminate before a scrape can occur.
* Prometheus itself is designed for numeric metrics; it’s not an event or log ingestion system.

For ephemeral jobs, Prometheus provides the Pushgateway: a buffer that accepts pushed metrics from short-lived jobs and exposes those metrics so Prometheus can scrape them later.

> **lightbulb** Use the Pushgateway only when a job cannot be scraped directly (for example, very short-lived batch jobs). Prefer direct instrumentation or exporters for long-lived services.

> **warning** The Pushgateway is intended for ephemeral or batch jobs only. It is not a general-purpose replacement for exporters or for instrumenting long-lived services.

Service discovery

Static target lists work for small environments, but dynamic infrastructures (Kubernetes, cloud auto-scaling, Consul, etc.) require automatic discovery. Prometheus supports many service discovery mechanisms to keep its target list current:

* Kubernetes service discovery
* AWS/EC2 discovery
* Consul, Docker, Azure, GCE, and more

These integrations let Prometheus automatically update targets as services and instances are created or destroyed.

Service discovery references:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Amazon EC2](https://aws.amazon.com/ec2/)
* [HashiCorp Consul](https://www.consul.io/)

Alerting and notifications

* Prometheus can evaluate alerting rules and generate alerts based on `PromQL` expressions.
* However, Prometheus does not handle notification delivery (email, Slack, PagerDuty, etc.) itself.

Alertmanager is the component that receives alerts from Prometheus and manages:

* Deduplication and grouping of similar alerts.
* Routing alerts to appropriate receivers.
* Notification delivery via email, Slack, PagerDuty, webhooks, and other integrations.

Visualization and querying

* Query Prometheus directly using `PromQL` via the HTTP API or the built-in Prometheus UI.
* For richer dashboards, use Grafana to visualize Prometheus metrics. (Grafana is commonly paired with Prometheus; Loki is used for log aggregation and can complement Prometheus-based monitoring.)

Common resources:

* Prometheus HTTP API / PromQL docs
* Grafana for dashboards and visualizations

Summary: core components and where they fit

| Component         | Purpose                                                                       |
| ----------------- | ----------------------------------------------------------------------------- |
| Prometheus server | Scrapes metrics, stores them in TSDB, exposes API/UI for queries              |
| Exporters         | Translate non-Prometheus metrics into the exposition format (`\`/metrics\`\`) |
| Client libraries  | Instrument applications to expose custom, domain-specific metrics             |
| Pushgateway       | Temporary buffer for short-lived job metrics (ephemeral use only)             |
| Service discovery | Keeps the scrape target list up-to-date in dynamic environments               |
| Alertmanager      | Handles alert routing, grouping, and notification delivery                    |
| Visualization     | Grafana (dashboards) + Prometheus (PromQL) for queries and exploration        |

Links and references

* [Prometheus documentation](https://prometheus.io/docs/)
* [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [Grafana – official site](https://grafana.com/)
* Courses referenced (examples):
  * [Kubernetes for the Absolute Beginners - Hands-on Tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)
  * [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
  * [HashiCorp Certified: Consul Associate Certification](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/ee6ba486-2f01-4d05-9bfc-7a261add2766)
