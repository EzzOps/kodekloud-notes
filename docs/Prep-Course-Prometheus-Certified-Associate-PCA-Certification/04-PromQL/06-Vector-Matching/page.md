# This will fail: rate() returns an instant vector, but max_over_time expects a range vector
max_over_time(rate(http_requests_total[10m]))
```

2. Correct approach using a subquery:

```PromQL theme={null}
# Compute the max rate over the last 5 minutes, with rate() grouped by 1m and subquery sampled every 30s
max_over_time(rate(http_requests_total[1m])[5m:30s])
```

3. Visualizing how a subquery returns samples:

```PromQL theme={null}
# Subquery example: evaluate rate(node_cpu_seconds_total[1m]) over the last 2 minutes at 10s resolution
rate(node_cpu_seconds_total[1m])[2m:10s]

# Example returned samples (timestamps shown):
0.991777777804683 @ 1664226130
0.991777777804683 @ 1664226140
0.991333333304358 @ 1664226150
0.991111111113807 @ 1664226160
0.991111111113807 @ 1664226170
0.991555555528651 @ 1664226180
0.9895555555561764 @ 1664226190
0.9895555555561764 @ 1664226200
0.989333333337472 @ 1664226210
0.989333333337472 @ 1664226220
0.991111111113807 @ 1664226230
```

In the example above:

* The `1m` inside `rate()` is the sample range used by `rate` for each evaluated instant.
* The outer `[2m:10s]` asks Prometheus to evaluate that `rate(...)` expression across the past 2 minutes at 10-second intervals, producing a range vector.

> **warning** Be careful with very small `resolution` values (the subquery step). High-resolution subqueries can be expensive and may increase query latency and Prometheus load. Choose a resolution appropriate for the precision you need.

## Practical example: network transmit bytes

Let's use a real metric: `node_network_transmit_bytes_total` (total transmitted bytes on a network interface). To get the current transmission rate:

```PromQL theme={null}
rate(node_network_transmit_bytes_total[1m])
```

That yields the current rate per interface (an instant vector), for example:

```Prometheus theme={null}
{device="enp0s3", instance="192.168.1.168:9100", job="node"} 1556.911111111111
{device="enp0s3", instance="192.168.1.168:9200", job="node"} 1567.6
{device="lo", instance="192.168.1.168:9100", job="node"} 0
{device="lo", instance="192.168.1.168:9200", job="node"} 0
```

<Frame>
  <img alt="The image shows the Prometheus query interface in a web browser, where various network-related metrics are listed with prefixes, such as &#x22;node_network,&#x22; and a search bar is used to filter them." />
</Frame>

To find the highest rate over the past 5 hours, use a subquery so `max_over_time` receives a range vector:

```PromQL theme={null}
max_over_time(rate(node_network_transmit_bytes_total[1m])[5h:30s])
```

* Inner `[1m]` is the `rate()` sample range (how `rate` computes an instant rate).
* Outer `[5h:30s]` requests the last 5 hours of the `rate(...)` values sampled every 30 seconds.
* `max_over_time(...)` then returns the maximum of those sampled rate values.

If you remove `max_over_time` and just run the subquery:

```promql theme={null}
rate(node_network_transmit_bytes_total[1m])[1h:30s]
```

Prometheus will return a series of sampled points for the last hour at 30-second intervals, which you can inspect or aggregate further.

## When to use subqueries

* Converting an instant-vector expression into a range vector for range aggregations (e.g., `max_over_time`, `avg_over_time`).
* Evaluating rate-like expressions historically at a chosen resolution without using recording rules.
* Performing windowed calculations over computed instant values.

## References

* [Prometheus Querying Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [Prometheus Subqueries](https://prometheus.io/docs/prometheus/latest/querying/basics/#subqueries)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/023a6dfb-e64f-4184-976a-b010d9127fd5)


# Vector Matching

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Vector-Matching/page

Describes PromQL vector matching and modifiers like on ignoring group_left and group_right to control label based pairing and many-to-one or one-to-many arithmetic

In this lesson we cover vector matching in PromQL—how Prometheus pairs elements from two instant vectors when performing element-wise arithmetic and how to control that matching using label selectors and grouping modifiers.

## Element-wise operations between vectors

PromQL can operate on two instant vectors element-wise. For example, to compute the percentage of free space per filesystem, divide available bytes by total size and multiply by 100:

```text theme={null}
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/home"} 512
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/var"} 484
node_filesystem_size_bytes{instance="node1", job="node", mountpoint="/home"} 1024
node_filesystem_size_bytes{instance="node1", job="node", mountpoint="/var"} 2048
```

Query:

```promql theme={null}
node_filesystem_avail_bytes / node_filesystem_size_bytes * 100
```

This divides each left-hand sample by the corresponding right-hand sample and multiplies by 100 to yield a percentage.

### Label-matching rule (exact by default)

By default, PromQL only pairs two samples when their complete set of labels and values are identical. The matching process checks every label on the left sample and tries to find a sample on the right with the exact same label names and values.

> **lightbulb** All labels on the two vectors must match exactly unless you use `on(...)` or `ignoring(...)` to control which labels are used for matching.

If labels differ (or one sample has an extra label), they will not match:

```text theme={null}
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/home"} 512
node_filesystem_size_bytes{instance="node2", job="node", mountpoint="/home"} 1024
```

Because `instance` differs, these samples will not pair.

## Controlling which labels are used for matching

Use `on(...)` to list the label names to match on, or `ignoring(...)` to exclude certain labels from the matching. This is vital when one metric has additional label dimensions that should not prevent matching.

Example: compute the percentage of `500` errors per HTTP method when error metrics include a `code` label, but request metrics do not.

Input metrics:

```text theme={null}
http_errors{method="get", code="500"} 40
http_errors{method="get", code="404"} 77
http_errors{method="put", code="501"} 23
http_errors{method="post", code="500"} 61
http_errors{method="post", code="404"} 42

http_requests{method="get"} 421
http_requests{method="del"} 288
http_requests{method="post"} 372
```

Options to match by `method`:

* Ignore the `code` label on the errors side:

```promql theme={null}
http_errors{code="500"} / ignoring(code) http_requests
```

* Or explicitly match on `method`:

```promql theme={null}
http_errors{code="500"} / on(method) http_requests
```

Only methods present on both sides will appear. In this dataset, `put` (only in `http_errors`) and `del` (only in `http_requests`) will be dropped from the output.

You can list multiple labels in `on(...)`:

```promql theme={null}
http_errors / on(method, instance) http_requests
```

## Example: match on CPU but ignore mode

When metrics include different operational modes but you only want to match by CPU:

vector1:

```text theme={null}
{cpu="0", mode="idle"} 4
{cpu="1", mode="iowait"} 7
{cpu="2", mode="user"} 2
```

vector2:

```text theme={null}
{cpu="1", mode="steal"} 4
{cpu="2", mode="user"} 7
{cpu="0", mode="idle"} 2
```

Use `on(cpu)` or `ignoring(mode)` to match samples by `cpu` only.

<Frame>
  <img alt="This image illustrates vector matching keywords using two vectors, showing how elements are matched and summed based on specified labels like &#x22;cpu&#x22; and &#x22;mode.&#x22;" />
</Frame>

## Matching modes: one-to-one, many-to-one, one-to-many

* One-to-one (default): each element on the left matches at most one element on the right.
* Many-to-one / one-to-many: when multiple samples on one side match a single sample on the other side, you must explicitly allow this with `group_left()` or `group_right()`.

When PromQL detects multiple matches for a single sample without an explicit grouping modifier, it returns an error: "multiple matches for labels".

Example (many-to-one): error counts per `path` and `error` vs. total requests per `path`.

Input:

```text theme={null}
http_errors:
{error="400", path="/cats"} 2
{error="500", path="/cats"} 5
{error="400", path="/dogs"} 1
{error="500", path="/dogs"} 7

http_requests:
{path="/cats"} 14
{path="/dogs"} 20
```

A naive query:

```promql theme={null}
http_errors / on(path) http_requests
```

returns an error due to multiple `http_errors` entries for each `path`. Tell PromQL that the left-hand side may have multiple entries matching a single right-hand entry with `group_left()`:

```promql theme={null}
http_errors / on(path) group_left() http_requests
```

`group_left()` preserves the extra labels from the left-hand side (for example `error`) in the output.

<Frame>
  <img alt="The image explains the Many-To-One matching concept in PromQL, where each element on the &#x22;one&#x22; side can match with multiple elements on the &#x22;many&#x22; side, using an example of HTTP errors and requests. It demonstrates how group_left is used to match elements from the right side with multiple elements from the left side based on the path." />
</Frame>

Use `group_right()` when the right-hand side may have multiple matching samples per single left-hand sample (one-to-many in the opposite direction). The `group_*()` modifier may be used with or without a label list; providing a label list preserves those labels from the many side in the result.

## Prometheus UI example: filesystem availability percentage

Each filesystem time series commonly includes labels like `device`, `fstype`, `instance`, `job`, and `mountpoint`. When the label sets align exactly between `node_filesystem_avail_bytes` and `node_filesystem_size_bytes`, dividing them yields the percentage available for that timeseries:

```text theme={null}
node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efi"} 531341312
node_filesystem_size_bytes{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efi"} 536834048
...
```

If labels match perfectly, this query will return the expected percentage per filesystem.

<Frame>
  <img alt="The image shows a Prometheus web interface displaying queries for filesystem metrics, specifically node_filesystem_avail_bytes and node_filesystem_size_bytes, with data in a tabular format." />
</Frame>

If labels do not match (for example one metric has an extra `error` label), the division returns no results unless you control matching with `on(...)`, `ignoring(...)`, and—if multiple matches occur—`group_left()` or `group_right()`.

<Frame>
  <img alt="The image shows a Prometheus web interface displaying query results for file system usage metrics, including the percentage of available bytes and specific device details. It includes tables with metric names, device instances, and mount points." />
</Frame>

### Example: HTTP errors vs. HTTP requests totals

When `http_errors_total` includes an `error` label and `http_requests_total` does not:

```text theme={null}
http_errors_total{error="400", instance="192.168.1.168:8000", job="api", path="/cars"} 13
http_errors_total{error="500", instance="192.168.1.168:8000", job="api", path="/cars"} 32
http_requests_total{instance="192.168.1.168:8000", job="api", path="/cars"} 100
```

A direct division will yield nothing because label sets differ. Exclude `error` from matching:

```promql theme={null}
http_errors_total / ignoring(error) http_requests_total
```

If multiple `http_errors_total` samples (different `error` values) match a single `http_requests_total` sample, use `group_left()` to explicitly allow many-to-one matching and retain the `error` label in results:

```promql theme={null}
http_errors_total / ignoring(error) group_left() http_requests_total
```

<Frame>
  <img alt="The image shows a Prometheus monitoring dashboard displaying file system metrics and HTTP requests with data in a tabular format. It includes queries for file system usage and HTTP error totals." />
</Frame>

## Matching modes at a glance

| Matching mode        | Description                                                                                         | Example                        |
| -------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------ |
| One-to-one (default) | Each sample on the left matches at most one on the right. Requires identical label sets and values. | `A / B`                        |
| Many-to-one          | Multiple samples on the left match a single sample on the right. Must use `group_left()`.           | `A / on(path) group_left() B`  |
| One-to-many          | Multiple samples on the right match a single sample on the left. Must use `group_right()`.          | `A / on(path) group_right() B` |

Note: In the table, `A` and `B` represent vectors; any label selectors like `{path="/cats"}` should be written as PromQL expressions in queries.

## Practical tips and links

* Always inspect the label sets of the two vectors (`label_join`, `label_replace`, or the Prometheus UI) before combining them to avoid silent drops or errors.
* Use `on(...)` to restrict matching to specific key labels, and `ignoring(...)` to exclude irrelevant labels.
* When allowing multiple matches, choose `group_left()` or `group_right()` according to which side holds the extra label dimensions you want to preserve.
* To explicitly keep only select labels from the many side, supply them to `group_left(<labels...>)` or `group_right(<labels...>)`.

Further reading:

* [PromQL: Binary Operators and Vector Matching](https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching)
* [Prometheus Documentation](https://prometheus.io/docs/)

Summary

* PromQL defaults to strict one-to-one label matching.
* Use `on(...)` / `ignoring(...)` to control which labels are considered for matching.
* Use `group_left()` / `group_right()` to explicitly allow many-to-one or one-to-many matches and to preserve labels from the many side when needed.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/d8df097a-4cbf-40fc-9f95-89490c4e15e3)
