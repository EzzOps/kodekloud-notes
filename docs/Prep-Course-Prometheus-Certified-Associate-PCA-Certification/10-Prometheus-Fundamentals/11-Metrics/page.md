# Metrics

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Metrics/page

Explains Prometheus metrics structure, time series, metric types, labels and metadata with guidance on instrumentation and avoiding high cardinality

In this lesson we’ll explain how Prometheus metrics are structured, how time series are formed, and how to interpret different metric types. You’ll learn how labels and metric names work, the meaning of `# HELP` and `# TYPE` metadata, and practical guidance for avoiding high-cardinality issues.

A Prometheus metric has three main parts:

* a descriptive name,
* a set of labels (key/value pairs),
* and a numeric value recorded at a specific time.

The text exposition format looks like:

```text theme={null}
<metric_name>{<label_1="value_1">,<label_N="value_N">} <metric_value>
```

Example from the Node Exporter:

```text theme={null}
node_cpu_seconds_total{cpu="0",mode="idle"} 258277.86
```

This indicates that CPU 0 has accumulated 258,277.86 seconds in the "idle" state. If a machine has multiple CPUs, the same metric appears multiple times with different `cpu` labels:

```text theme={null}
node_cpu_seconds_total{cpu="0",mode="idle"} 258277.86
node_cpu_seconds_total{cpu="1",mode="idle"} 427262.54
node_cpu_seconds_total{cpu="2",mode="idle"} 283288.12
node_cpu_seconds_total{cpu="3",mode="idle"} 258202.33
```

Each unique metric name + label set identifies a separate stream of timestamped values (a time series).

When Prometheus scrapes a target it records the sample timestamp (by default the scrape time) as a Unix timestamp (seconds since the epoch) for samples without an explicit timestamp. For example:

```text theme={null}
1668215300
```

You can convert Unix timestamps using any Unix timestamp converter; dashboards typically render these in local time zones automatically.

Stored samples therefore include a value plus a timestamp, e.g.:

```text theme={null}
node_cpu_seconds_total{cpu="0",mode="idle"} 258277.86 1668215300
```

<Frame>
  <img alt="The image is a diagram titled &#x22;Counter,&#x22; highlighting metrics like &#x22;Total # requests,&#x22; &#x22;Total # Exceptions,&#x22; and &#x22;Total # of job executions,&#x22; showing how these numbers can only increase." />
</Frame>

## Time series

A "time series" in Prometheus is a stream of timestamped values that share the same metric name and identical label sets (same keys and values). In other words: metric name + labels = time series.

Examples:

```text theme={null}
node_filesystem_files{device="sda2", instance="server1"}
node_filesystem_files{device="sda3", instance="server1"}
node_filesystem_files{device="sda2", instance="server2"}
node_filesystem_files{device="sda3", instance="server2"}

node_cpu_seconds_total{cpu="0", instance="server1"}
node_cpu_seconds_total{cpu="1", instance="server1"}
node_cpu_seconds_total{cpu="0", instance="server2"}
node_cpu_seconds_total{cpu="1", instance="server2"}
```

Although there are only two metric names above, the different label combinations produce eight distinct time series. As Prometheus scrapes these targets periodically (for example every 15 or 30 seconds), it appends new timestamped values to each time series.

## Metric metadata: HELP and TYPE

Prometheus text exposition may include two helpful metadata comments per metric:

* `# HELP` — a short human-readable description of the metric.
* `# TYPE` — the metric type (`counter`, `gauge`, `histogram`, `summary`).

Example:

```text theme={null}
