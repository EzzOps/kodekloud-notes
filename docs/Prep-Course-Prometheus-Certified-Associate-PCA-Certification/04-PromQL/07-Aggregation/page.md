# Aggregation

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Aggregation/page

Explains Prometheus aggregation operators and using by and without to group or exclude labels with examples and practical tips

Aggregation operators in Prometheus let you reduce an instant vector into a new instant vector by combining several time series into one (or fewer) values. Common use cases include computing the sum, min, max, average, or count across a set of time series.

This guide explains:

* What aggregation operators do
* How to group results using `by(...)`
* How to exclude labels using `without(...)`
* Practical examples with `http_requests` and `node_cpu_seconds_total`

See also: [Prometheus Aggregation Operators](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators)

## Aggregation operators overview

Aggregation operators operate across all series in an instant vector by default. The most common are:

| Operator  | Description                             | Example                |
| --------- | --------------------------------------- | ---------------------- |
| `sum()`   | Sum of all matching series              | `sum(http_requests)`   |
| `max()`   | Maximum value among all matching series | `max(http_requests)`   |
| `min()`   | Minimum value among all matching series | `min(http_requests)`   |
| `avg()`   | Average of all matching series          | `avg(http_requests)`   |
| `count()` | Count of series in the vector           | `count(http_requests)` |

> **lightbulb** Aggregation reduces multiple time series into fewer series. If you need to retain distinctions (e.g., per path or per instance), use `by(...)` to group by label(s) before aggregation.

## Basic examples: sum, max, avg

Given the following `http_requests` instant vector:

```text theme={null}
$ http_requests
http_requests{method="get", path="/auth"} 3
http_requests{method="post", path="/auth"} 1
http_requests{method="get", path="/user"} 4
http_requests{method="post", path="/user"} 8
http_requests{method="post", path="/upload"} 2
http_requests{method="get", path="/tasks"} 4
http_requests{method="put", path="/tasks"} 6
http_requests{method="post", path="/tasks"} 1
http_requests{method="get", path="/admin"} 3
http_requests{method="post", path="/admin"} 9
```

* Sum across all series:

```text theme={null}
$ sum(http_requests)
{} 41  // 3+1+4+8+2+4+6+1+3+9
```

* Max across all series:

```text theme={null}
$ max(http_requests)
{} 9
```

* Average across all series:

```text theme={null}
$ avg(http_requests)
{} 4.1
```

By default these operations aggregate over every distinct time series in the instant vector (i.e., every combination of labels).

## Grouping with `by(...)`

Use `by(<label1>, <label2>, ...)` to keep the specified labels and aggregate across all others. This is how you "group by" a label.

Example: sum by path

```text theme={null}
$ sum by(path) (http_requests)
{path="/auth"} 4   // 3+1
{path="/user"} 12  // 4+8
{path="/upload"} 2 // 2
{path="/tasks"} 11 // 4+6+1
{path="/admin"} 12 // 3+9
```

This groups the results by the `path` label and sums all series that share the same path.

Example: sum by method

```text theme={null}
$ sum by(method) (http_requests)
{method="get"} 14   // 3+4+4+3
{method="post"} 21  // 1+8+2+1+9
{method="put"} 6    // 6
```

You can pass multiple labels to `by(...)` to aggregate by combinations (e.g., `by(instance, method)`).

## Excluding labels with `without(...)`

`without(...)` is the inverse of `by(...)`. It aggregates across all labels except the ones listed. Use it when you want to drop specific labels and collapse across the rest.

Example:

```text theme={null}
$ http_requests
http_requests{method="get", path="/auth", instance="node1"} 3
http_requests{method="post", path="/auth", instance="node1"} 1
http_requests{method="get", path="/tasks", instance="node1"} 4
http_requests{method="put", path="/tasks", instance="node1"} 6
http_requests{method="post", path="/tasks", instance="node1"} 1
http_requests{method="get", path="/auth", instance="node2"} 13
http_requests{method="post", path="/node2"} 11
http_requests{method="put", path="/tasks", instance="node2"} 16
http_requests{method="post", path="/tasks", instance="node2"} 11
```

If you want to aggregate all series while preserving `instance` and `method` labels, you can do:

```text theme={null}
$ sum without(path) (http_requests)
{instance="node1", method="get"} 7   // 3+4
{instance="node1", method="post"} 2  // 1+1
{instance="node1", method="put"} 6   // 6
{instance="node2", method="get"} 27  // 13+14
{instance="node2", method="post"} 71 // 11+18+12+11+19
{instance="node2", method="put"} 22  // 11+11
```

This is equivalent to `sum by(instance, method) (http_requests)`.

> **warning** Be careful: aggregation removes labels not listed in `by(...)` (or not excluded by `without(...)`). If those labels are important for identifying series, include them in `by(...)`.

## Real-world: node\_cpu\_seconds\_total examples

Consider `node_cpu_seconds_total`, which typically has labels like `cpu`, `instance`, `mode`, and `job`. If you run:

```text theme={null}
sum(node_cpu_seconds_total)
```

Prometheus will return a single value summing across all instances, CPUs, and modes — usually not what you want for per-node visibility.

Example excerpt of raw time series:

```text theme={null}
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="iowait"} 13084.27
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="idle"} 2.65
...
node_cpu_seconds_total{cpu="1", instance="192.168.1.168:9100", job="node", mode="system"} 31.88
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9200", job="node", mode="system"} 35.4
...
```

If you want the total CPU seconds per instance (i.e., per target), group by `instance`:

```text theme={null}
sum by(instance)(node_cpu_seconds_total)
```

This returns one summed value per `instance`, aggregating across `cpu` and `mode`.

If you want per-instance and per-CPU totals, group by both:

```text theme={null}
sum by(instance, cpu)(node_cpu_seconds_total)
```

That yields values like:

* instance A, cpu 0
* instance A, cpu 1
* instance B, cpu 0
* instance B, cpu 1

If you prefer to exclude `cpu` and `mode` and aggregate everything else, use `without(...)`. For example, to aggregate into per-instance totals via `without`:

```text theme={null}
sum without(cpu, mode) (node_cpu_seconds_total)
```

This drops `cpu` and `mode` from the result, leaving the aggregation keyed by the remaining labels (e.g., `instance` and `job`).

## Quick tips

* Use `by(...)` to preserve the labels you care about.
* Use `without(...)` to drop specific labels and aggregate across the rest.
* Aggregation dramatically changes the dimensionality of your data — including or excluding labels will affect alerting and dashboarding logic.
* When building dashboards, prefer aggregations that match the level of granularity you want to visualize (per-instance, per-pod, per-cluster, etc.).

## Links and references

* [Prometheus Querying: Aggregation Operators](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators)
* [Prometheus Documentation](https://prometheus.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/8f09a977-27de-4d40-8fe7-25a679d03eae)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/0a0d5663-1e6c-4108-b228-b49fbe9d02ab)
