# Prometheus Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Prometheus-Basics/page

Learn to set up a monitoring stack with Prometheus, Grafana, and Alertmanager, covering architecture, data visualization, and alerting.

In this lesson, you’ll learn how to set up a complete monitoring stack with Prometheus, Grafana, and Alertmanager. We’ll cover:

1. Overview of Prometheus
2. Prometheus architecture
3. Data visualization with Grafana
4. Alerting with Prometheus and Alertmanager

***

## 1. Overview of Prometheus

Prometheus is an open-source, pull-based monitoring and alerting system designed for time series data. It excels at:

* Multi-dimensional data model: metrics are labeled with key/value pairs.
* PROMQL: a flexible query language for slicing, aggregating, and analyzing time series.
* Native TSDB: optimized on-disk format for fast storage and retrieval.
* White-box monitoring: collects internal metrics (CPU, memory, request rates, etc.) from instrumented code.

<Callout icon="lightbulb">
  Prometheus focuses strictly on metrics collection and alerting. It does not handle logs, distributed tracing, or advanced anomaly detection. Consider integrating with [Grafana Loki](https://grafana.com/oss/loki/) for logs and [Jaeger](https://www.jaegertracing.io/) for tracing.
</Callout>

***

## 2. Prometheus Architecture

Prometheus consists of several core components that work together to discover, scrape, store, and alert on metrics.

### 2.1 Service Discovery

Prometheus automatically discovers scrape targets in dynamic environments:

| Platform   | Discovery Mechanism      | Example                 |
| ---------- | ------------------------ | ----------------------- |
| Kubernetes | Kubernetes API           | `kubernetes_sd_configs` |
| AWS EC2    | EC2 API                  | `ec2_sd_configs`        |
| Consul     | HTTP API                 | `consul_sd_configs`     |
| Static     | Manually defined targets | `static_configs`        |

### 2.2 Instrumentation and Exporters

Instrumentation happens in two ways:

1. **Client libraries** for languages like Go, Python, Java, and Ruby.
2. **Exporters** for services you cannot modify.

| Exporter       | Purpose                            | GitHub/Docs                                                                                         |
| -------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| Node Exporter  | Host-level metrics (CPU, disk)     | [https://github.com/prometheus/node\_exporter](https://github.com/prometheus/node_exporter)         |
| Blackbox       | Endpoint probing (HTTP, TCP, ICMP) | [https://github.com/prometheus/blackbox\_exporter](https://github.com/prometheus/blackbox_exporter) |
| MySQL Exporter | Database server metrics            | [https://github.com/prometheus/mysqld\_exporter](https://github.com/prometheus/mysqld_exporter)     |
| JMX Exporter   | JVM application metrics            | [https://github.com/prometheus/jmx\_exporter](https://github.com/prometheus/jmx_exporter)           |

### 2.3 Scraping and Local Storage

Prometheus periodically scrapes metrics from each target defined in `prometheus.yml`. Scrapes are HTTP GET requests that return metrics in the Prometheus exposition format. The time series data is then committed to the local TSDB.

```yaml theme={null}
