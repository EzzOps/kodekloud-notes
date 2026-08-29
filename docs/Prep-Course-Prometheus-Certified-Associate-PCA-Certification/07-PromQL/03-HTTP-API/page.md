# Raw metric (instant vector)
node_cpu_seconds_total
# => {cpu="0", mode="idle"}   115.12
# => {cpu="0", mode="irq"}    87.4482
# Apply ceil()
ceil(node_cpu_seconds_total)
# => {cpu="0", mode="idle"}   116
# => {cpu="0", mode="irq"}    88
# Apply floor()
floor(node_cpu_seconds_total)
# => {cpu="0", mode="idle"}   115
# => {cpu="0", mode="irq"}    87
# Example using abs() with an arithmetic expression
# This computes the absolute value of (1 - sample).
abs(1 - node_cpu_seconds_total)
# => {cpu="0", mode="idle"}   114.12    # abs(1 - 115.12)
# => {cpu="0", mode="irq"}    86.4482   # abs(1 - 87.4482)
# => {cpu="0", mode="steal"}  43.245    # abs(1 - 44.245)
```

## Date and time functions

Prometheus exposes functions to extract parts of the current evaluation time. These are useful for calendar-aware calculations, scheduling logic in queries, or tagging alerts with time components.

Key functions:

* `time()` — current Unix time in seconds (float).
* `minute()`, `hour()`, `day_of_week()`, `day_of_month()`, `days_in_month()`, `month()`, `year()` — return the specified component of the current evaluation timestamp.

Example (if evaluation time is Thursday, September 22, 2022 at 15:07):

```plaintext theme={null}
Expression         => result
---------------------------
minute()           => 07
hour()             => 15
day_of_week()      => 4
day_of_month()     => 22
days_in_month()    => 30
month()            => 09
year()             => 2022
```

## Converting between scalars and vectors

* `scalar(v)` — Converts an instant vector `v` containing exactly one sample into a scalar value. If `v` contains more than one element, the result is `NaN`.
* `vector(s)` — Converts a scalar `s` into an instant vector containing a single sample (useful for combining scalar thresholds with vector operations).

Use these when you need to mix scalar math or constants with vector expressions.

## Sorting

Sort instant vectors by the sample values.

* `sort(v)` — ascending order.
* `sort_desc(v)` — descending order.

Example:

```bash theme={null}
# Sorted ascending
sort(node_filesystem_avail_bytes)
# => node_filesystem_avail_bytes{device="gvfsd-fuse", fstype="fuse.gvfsd-fuse", instance="node1"} 0
# => node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1"} 5238784
# => node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="node1"} 531341312
# => node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1"} 725422080
# => node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1"} 726319104
# Sorted descending
sort_desc(node_filesystem_avail_bytes)
# => highest values first...
```

## Presence checks: absent / present (and their \_over\_time variants)

These functions help detect missing series or whether a series has samples inside a specified range.

* `absent(v)` — If `v` contains any elements, returns an empty vector. If no elements exist, returns a single-element vector with the value `1` and the labels taken from the expression.
* `absent_over_time(v[range])` — Returns `1` for each series that has no samples inside the specified range; returns nothing if at least one sample exists.
* `present_over_time(v[range])` — Returns `1` for each series that has at least one sample in the range; otherwise returns nothing for that series.

Examples:

```bash theme={null}
# If the series exists at least once in the given range:
present_over_time(node_filesystem_avail_bytes[5m])
# If the series has no samples in the range:
absent_over_time(node_memory_Active_bytes[1h])
# => {}
```

From the Prometheus docs (behavior illustrations):

```bash theme={null}
absent(nonexistent{job="myjob"})
absent(nonexistent{job="myjob", instance=".*"})
absent(sum(nonexistent{job="myjob"}))
# => {}
```

<Callout icon="lightbulb">
  Refer to the Prometheus documentation under [Querying → Functions](https://prometheus.io/docs/prometheus/latest/querying/functions/) for a complete list of functions and their exact semantics.
</Callout>

<Frame>
  <img alt="The image shows a webpage from the Prometheus documentation, specifically detailing the usage of the delta() function in querying. It features a menu on the left, content in the center, and a list of functions on the right." />
</Frame>

There are many more functions (`delta`, `deriv`, `exp`, etc.). The names tend to be descriptive; trying examples in the Prometheus console is an effective way to learn them.

## Counters and rate calculations

Counters are monotonically increasing metrics (e.g., bytes sent, requests served). Plotting the raw counter typically shows a continuously rising line, which is often not as useful as the rate of change.

<Frame>
  <img alt="The image displays a graph showing a steadily increasing counter metric over time. Accompanying text explains that such plots show expected increases over time." />
</Frame>

Prometheus provides two primary functions to convert counters to per-second rates:

* `rate(v[range])` — computes the average per-second rate of increase across the provided time range. It uses the first and last sample of the range (accounting for counter resets).
* `irate(v[range])` — computes an instant rate using only the last two samples in the range (i.e., slope between the most recent samples).

<Frame>
  <img alt="The image contains a line graph illustrating fluctuations over time and text discussing the rate of change of a counter metric using rate() and irate() functions." />
</Frame>

How `rate()` works (conceptual):

* `rate(http_errors[1m])` divides the series into overlapping 1-minute windows for each evaluation.
* If the scrape interval is 15s, each 1-minute window typically contains 4 samples.
* For each window, `rate()` computes (last\_sample - first\_sample) / window\_seconds, yielding a per-second average across the window.

Numeric illustration (one 1-minute window):

```plaintext theme={null}
samples in window: 1.2, 2.3, 3.1, 3.3
first = 1.2, last = 3.3
difference = 3.3 - 1.2 = 2.1
rate = 2.1 / 60 = 0.035 (per second)
```

How `irate()` differs:

* `irate(http_errors[1m])` still evaluates over the 1-minute range, but uses the last two samples within that window.
* Rate is (last - second\_last) / time\_difference\_between\_these\_two\_samples (often equal to the scrape interval, e.g., 15s).

Example usage:

```bash theme={null}
# Instant rate using the last two samples in each window
irate(http_errors[1m])
# => calculated as (last - second_last) / scrape_interval_seconds
```

Practical differences and guidance:

|          Function | Behavior                                   | Best use                                                    |
| ----------------: | ------------------------------------------ | ----------------------------------------------------------- |
|  `rate(v[range])` | Averages across the entire range           | Stable, recommended for alerting and slow-moving counters   |
| `irate(v[range])` | Instant slope between the last two samples | More responsive; useful for graphing very volatile counters |

<Frame>
  <img alt="The image is a screenshot comparing &#x22;rate&#x22; and &#x22;irate&#x22;, which explains that &#x22;rate&#x22; looks at the first and last data points within a range and is effectively an average rate over the range." />
</Frame>

Tips when using `rate()` / `irate()`:

* Ensure the chosen range contains enough samples. With a 15s scrape interval, `1m` yields \~4 samples; more samples improve stability.
* When aggregating across series, compute the rate first, then aggregate. This preserves correct counter-reset handling per series.

Correct pattern:

```bash theme={null}
# Compute per-second rate per series first, then aggregate across series
sum without(code, handler) (rate(http_requests_total[24h]))
```

## Example: network transmit bytes

A raw counter such as `node_network_transmit_bytes_total` shows cumulative bytes transmitted per interface. The web UI helps explore series and labels.

<Frame>
  <img alt="The image shows the Prometheus web interface with a query being typed in the search bar, displaying autocomplete suggestions for network device statistics." />
</Frame>

Viewing the raw counter over time shows a steady increase:

<Frame>
  <img alt="The image shows a Prometheus dashboard displaying a graph of network transmission bytes over time. A hover-over tooltip provides details of the network interface and the specific timestamped data point." />
</Frame>

To convert the counter into throughput (bytes per second), compute the per-second rate:

```bash theme={null}
# Per-second transmit rate averaged across a 1m window
rate(node_network_transmit_bytes_total[1m])
```

This query returns the average bytes-per-second for each interface over the selected window—more meaningful for bandwidth and throughput alerts.

## Summary and references

* PromQL offers many functions across categories: math, time/date, sorting, presence checks, conversions, and counter-rate computations.
* Use `rate()` for stable averages (preferred for alerting), and `irate()` for instant slopes (preferred for responsive graphs).
* Always compute rates per series before aggregation to properly handle resets.
* For a complete list and exact semantics, see the Prometheus docs: [https://prometheus.io/docs/prometheus/latest/querying/functions/](https://prometheus.io/docs/prometheus/latest/querying/functions/)

Additional resources:

* [Prometheus Querying (official docs)](https://prometheus.io/docs/prometheus/latest/querying/functions/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/6254635d-a3cb-472d-861a-2e3d699b0751" />
</CardGroup>


# HTTP API

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/HTTP-API/page

Explains Prometheus HTTP API usage including instant and range PromQL queries, endpoints, parameters, examples, and curl usage for automation and integrations.

Prometheus exposes an HTTP API to run PromQL queries and to retrieve server metadata — for example, alerting rules, configuration, and service discovery information. This API is ideal for automation, integrations, or third-party tools like [Grafana](https://grafana.com) when the web UI isn't suitable.

Below are concise examples for instant queries (current value), instant queries at a specific timestamp, and range queries (time series across an interval) using the Prometheus HTTP API.

## Quick reference: endpoints and parameters

| Endpoint                   | Purpose                                           | Required form data                          |
| -------------------------- | ------------------------------------------------- | ------------------------------------------- |
| `POST /api/v1/query`       | Instant query (single point in time)              | `query` (PromQL expression)                 |
| `POST /api/v1/query`       | Instant query at a specific time                  | `query`, `time` (Unix timestamp or RFC3339) |
| `POST /api/v1/query_range` | Range query (multiple samples across an interval) | `query`, `start`, `end`, `step`             |

Example parameter formats:

* `query` — e.g. `node_cpu_seconds_total{job="node"}` (wrap label selectors in double quotes)
* `time`, `start`, `end` — Unix timestamp (seconds, optional fractional part) or RFC3339
* `step` — resolution in seconds (e.g. `15`)

<Callout icon="lightbulb">
  The `/api/v1/query` endpoint performs an instant query (value at a single point in time). For multi-point time series over a time range, use `/api/v1/query_range`.
</Callout>

<Callout icon="warning">
  When using `curl --data` on the shell, wrap the entire value in single quotes and use double quotes inside PromQL label selectors to avoid quoting conflicts. Example: `--data 'query=node_cpu_seconds_total{job="node"}'`.
</Callout>

## Instant query (current value)

To evaluate an instant query, POST to `/api/v1/query` with form-encoded data. Include the `query` parameter containing a PromQL expression.

Example: request the `node_arp_entries` metric for a specific instance:

```bash theme={null}
curl 'http://localhost:9090/api/v1/query' --data 'query=node_arp_entries{instance="192.168.1.168:9100"}'
```

If your Prometheus server is remote, replace `http://localhost:9090` with the appropriate host (for example, `http://<prometheus-host>:9090`).

Example: query CPU seconds total for targets with `job="node"`, and pretty-print with [`jq`](https://stedolan.github.io/jq/):

```bash theme={null}
curl 'http://localhost:9090/api/v1/query' --data 'query=node_cpu_seconds_total{job="node"}' | jq
```

Example response (truncated):

```json theme={null}
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "node_cpu_seconds_total",
          "cpu": "0",
          "instance": "192.168.1.168:9100",
          "job": "node",
          "mode": "idle"
        },
        "value": [
          1670382765.652,
          "502077.09"
        ]
      },
      {
        "metric": {
          "__name__": "node_cpu_seconds_total",
          "cpu": "1",
          "instance": "192.168.1.168:9100",
          "job": "node",
          "mode": "idle"
        },
        "value": [
          1670382765.652,
          "502077.09"
        ]
      }
    ]
  }
}
```

Anything available in the web UI can be retrieved via the API by issuing the appropriate PromQL query.

## Instant query at a specific time

To evaluate an instant query at a historical timestamp, add the `time` form parameter (Unix timestamp with optional fractional seconds). Prometheus evaluates the expression as of that timestamp.

Example: get `node_memory_Active_bytes` at a specific timestamp and pretty-print with `jq`:

```bash theme={null}
curl 'http://localhost:9090/api/v1/query' \
  --data 'query=node_memory_Active_bytes{job="node"}' \
  --data 'time=1670380680.132' | jq
```

Example response:

```json theme={null}
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "node_memory_Active_bytes",
          "instance": "192.168.1.168:9100",
          "job": "node"
        },
        "value": [
          1670380680.132,
          "1369653248"
        ]
      }
    ]
  }
}
```

The sample timestamp in the response matches the `time` you provided.

## Range query (values over a time interval)

To fetch metric values across an interval (multiple time points), use `POST /api/v1/query_range`. Required form parameters:

* `query` — PromQL expression (often a metric name or function).
* `start` — start time (Unix timestamp or RFC3339).
* `end` — end time (Unix timestamp or RFC3339).
* `step` — resolution step (in seconds; e.g., `15`).

Example: fetch `node_memory_Active_bytes` for the 10 minutes ending at `1670380680.132` with a 15-second step:

```bash theme={null}
curl 'http://localhost:9090/api/v1/query_range' \
  --data 'query=node_memory_Active_bytes{job="node"}' \
  --data 'start=1670380080.132' \
  --data 'end=1670380680.132' \
  --data 'step=15' | jq
```

The `query_range` response returns a `matrix` result: each matched series includes a sequence of `[timestamp, value]` pairs.

Important distinction:

* Using a range-vector selector inside an instant query (for example, `rate(node_cpu_seconds_total[5m])`) is valid with `/api/v1/query`: the function is evaluated over the specified range ending at the instant (or `time`) you provide.
* To retrieve multiple samples across time (the actual metric values at each scrape within a range), use `/api/v1/query_range`.

## Examples: common usage patterns

| Use case                         | Example query                                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Instant metric value for a `job` | `node_cpu_seconds_total{job="node"}`                                                                              |
| Instant rate over last 5 minutes | `rate(node_cpu_seconds_total[5m])`                                                                                |
| Range query to chart a metric    | Query via `POST /api/v1/query_range` with `start`, `end`, `step` and `query=node_memory_Active_bytes{job="node"}` |

## Summary

* Use `POST /api/v1/query` with `--data 'query=...'` for instant evaluations.
* Add `--data 'time=...'` to evaluate an instant query at a specific timestamp.
* Use `POST /api/v1/query_range` with `start`, `end`, and `step` to retrieve metric values across a time interval.
* When using shell `curl`, wrap the entire `--data` value in single quotes and use double quotes inside PromQL label selectors to avoid quoting conflicts.

## Links and references

* [Prometheus HTTP API documentation](https://prometheus.io/docs/prometheus/latest/querying/api/)
* [PromQL language overview](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [Grafana](https://grafana.com)
* [`jq` — Command-line JSON processor](https://stedolan.github.io/jq/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/c301bb9e-206d-4152-8858-3f9ae213cae2" />
</CardGroup>
