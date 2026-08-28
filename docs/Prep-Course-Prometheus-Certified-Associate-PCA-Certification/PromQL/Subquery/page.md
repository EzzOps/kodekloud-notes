# Subquery

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Subquery/page

Explains Prometheus subqueries, syntax and examples for evaluating instant queries over time windows so range aggregations can operate.

Suppose you have a gauge metric and you want to know its maximum value over the past ten minutes. Prometheus provides the `max_over_time` function for exactly that:

```PromQL theme={null}
max_over_time(node_filesystem_avail_bytes[10m])
```

That works fine for gauges. But what if you have a counter metric and you want the maximum *rate* over the past ten minutes? A naïve attempt might look like this:

```PromQL theme={null}
max_over_time(rate(http_requests_total[10m]))
```

This will fail because `rate(...)` returns an instant vector while `max_over_time` expects a range vector. Also remember: in `rate(metric[10m])`, the `10m` is the sample range for the `rate()` calculation (how Prometheus computes the rate), not how far back to query data for aggregation.

This is where subqueries solve the problem.

<Callout icon="lightbulb">
  Use subqueries when you need to take an instant-expression (for example, `rate(...)`) and evaluate that expression across a historical time window at a given resolution so that range-based aggregation functions (like `max_over_time`, `min_over_time`, etc.) can operate on a range vector.
</Callout>

## Subquery syntax

A Prometheus subquery wraps an instant query and appends a bracketed range and step (resolution). Optionally, you can add an `offset`.

```PromQL theme={null}
<instant_query> [<range>:<resolution>] [offset <duration>]
```

* `<instant_query>`: any instant-vector expression (e.g., `rate(...)`, `irate(...)`, or any metric selector).
* `<range>`: how far back to collect data for the subquery (the time window).
* `<resolution>`: step between samples returned by the subquery (the query step).

Example: compute the maximum rate of `http_requests_total` over the last 5 minutes, where `rate()` uses a 1 minute sample range and the subquery samples every 30 seconds:

```PromQL theme={null}
max_over_time(rate(http_requests_total[1m])[5m:30s])
```

* The inner `[1m]` tells `rate()` how to group samples for each instant.
* The outer `[5m:30s]` tells Prometheus to evaluate the instant expression for the previous 5 minutes at 30-second intervals, returning a range vector that `max_over_time` can consume.

## Quick comparison: instant vs range vectors

| Vector type    | Represents                                       | Typical use                                                                              |
| -------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Instant vector | A single value per series at one timestamp       | `rate(...)`, `irate(...)`, metric selectors without `[range]`                            |
| Range vector   | Multiple samples per series across a time window | `max_over_time(...)`, `avg_over_time(...)`, or subquery results like `rate(...)[5m:30s]` |

## Examples

1. Trying to nest `rate(...)` directly inside `max_over_time(...)` (invalid):

```PromQL theme={null}
