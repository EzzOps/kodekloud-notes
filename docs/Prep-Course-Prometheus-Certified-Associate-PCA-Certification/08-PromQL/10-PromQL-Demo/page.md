# returns series that match the left condition (>1000) but do NOT appear on the right (>30000)
```

## Putting it together: quick interactive examples

Combine arithmetic, comparison, and logical operators to build targeted queries.

Example — add 50 to `node_arp_entries`:

```bash theme={null}
$ node_arp_entries
node_arp_entries{instance="node1"} 2

$ node_arp_entries + 50
{instance="node1"} 52
```

Example — filter filesystems greater than `6_000_000` bytes:

```bash theme={null}
$ node_filesystem_avail_bytes
node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efi"} 531341312
node_filesystem_avail_bytes{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/"} 1427759104
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/snapd/ns"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/user/127"} 727838720

$ node_filesystem_avail_bytes > 6000000
node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efi"} 531341312
node_filesystem_avail_bytes{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/"} 1427759104
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/snapd/ns"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/user/127"} 727838720
```

Add a second filter to exclude very large filesystems (greater than `1_000_000_000` bytes):

```bash theme={null}
$ node_filesystem_avail_bytes > 6000000 and node_filesystem_avail_bytes < 1000000000
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/snapd/ns"} 726482944
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/user/127"} 727838720
```

`or` example — values less than `6_000_000` OR greater than `10_000_000_000`:

```bash theme={null}
$ node_filesystem_avail_bytes < 6000000 or node_filesystem_avail_bytes > 10000000000
# returns series matching either condition (below the first threshold or above the second)
```

## Summary

* Arithmetic operators (`+`, `-`, `*`, `/`, `%`, `^`) perform numeric transformations and unit conversions.
* Comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`) filter series; use `bool` to emit 0/1 results for alerting.
* Operator precedence determines evaluation order; use parentheses to make expressions explicit.
* Logical set operators (`and`, `or`, `unless`) combine or subtract series sets to build complex queries.

Further reading and references:

* Prometheus PromQL documentation: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* PromQL operators and expressions: [https://prometheus.io/docs/prometheus/latest/querying/operators/](https://prometheus.io/docs/prometheus/latest/querying/operators/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/d8a05d2c-75ff-489e-b5c8-5b9de1d1156a)


# PromQL Demo

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/PromQL-Demo/page

Demonstrates PromQL label selectors, regex matching, range vectors, and modifiers like offset and at with practical examples for querying historical and point-in-time metrics.

This lesson demonstrates PromQL label selectors and modifiers with practical examples. You'll learn how to filter series by labels, use regular expressions, select historical samples with range vectors, and query past points in time using `offset` and the `@` modifier.

## Inspecting per-CPU metrics

The `node_cpu_seconds_total` metric exposes CPU time broken down by the `cpu` and `mode` labels. Use exact label matchers to select specific series.

Select all series for CPU 0:

```promql theme={null}
node_cpu_seconds_total{cpu="0"}
```

Example output (one sample per series):

```text theme={null}
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="idle"}  7045.07
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="user"}  6.52
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="system"} 5.84
...
```

Notes:

* Label values must be quoted (for example, `cpu="0"`).
* To select every CPU except zero, use the negation operator `!=`:

```promql theme={null}
node_cpu_seconds_total{cpu!="0"}
```

## Range vectors: selecting historical samples

Range vectors return all samples within a relative time window for each matching series. Append a range selector `[...]` to a vector selector.

Get the last 2 minutes of samples for CPU 0:

```promql theme={null}
node_cpu_seconds_total{cpu="0"}[2m]
```

This returns time series objects that include all samples in the last 2 minutes for each matching series.

## Combining labels for more specific selection

You can combine multiple label matchers to narrow results. For example, to select CPU 0 when the CPU is `idle`:

```promql theme={null}
node_cpu_seconds_total{cpu="0", mode="idle"}
```

Example output:

```text theme={null}
node_cpu_seconds_total{cpu="0", instance="192.168.1.168:9100", job="node", mode="idle"} 7045.07
```

## Matching with regular expressions

Use regex matchers to match label values that fit a pattern. The `=~` operator matches regex; `!~` negates it.

Match all `mountpoint` values that start with `/run` (e.g., `/run`, `/run/lock`, `/run/snapd/ns`, `/run/user/127`):

```promql theme={null}
node_filesystem_files{mountpoint=~"^/run.*"}
```

Example output:

```text theme={null}
node_filesystem_files{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run"} 888580
node_filesystem_files{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/lock"} 888580
node_filesystem_files{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/snapd/ns"} 888580
node_filesystem_files{device="tmpfs", fstype="tmpfs", instance="192.168.1.168:9100", job="node", mountpoint="/run/user/127"} 177716
```

To get everything that does not start with `/run`, use the negated regex operator:

```promql theme={null}
node_filesystem_files{mountpoint!~"^/run.*"}
```

Example output:

```text theme={null}
node_filesystem_files{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efivars"} 830688
node_filesystem_files{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/"} 830688
node_filesystem_files{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/var/snap/firefox/common/host-hunspell"} 888580
```

## Combining regex with range selectors

You can combine regex matchers with range vectors to fetch history for only those matching series.

Fetch the last 5 minutes of samples for mountpoints that do not start with `/run`:

```promql theme={null}
node_filesystem_files{mountpoint!~"^/run.*"}[5m]
```

Example output (series identifiers shown):

```text theme={null}
node_filesystem_files{device="/dev/sda2", fstype="vfat", instance="192.168.1.168:9100", job="node", mountpoint="/boot/efivars"}
node_filesystem_files{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/"}
node_filesystem_files{device="/dev/sda3", fstype="ext4", instance="192.168.1.168:9100", job="node", mountpoint="/var/snap/firefox/common/host-hunspell"}
```

## Offsets: querying past time ranges

The `offset` modifier shifts the time window of a selector into the past. It is applied after the selector (and after any range vector).

Query 5 minutes of data starting 30 minutes ago:

```promql theme={null}
node_filesystem_files{mountpoint!~"^/run.*"}[5m] offset 30m
```

This returns the 5-minute range of samples from 30 minutes ago for all matching series.

## Point-in-time queries with the @ modifier

Use the `@` modifier to evaluate a selector at a specific instant (Unix timestamp). This is useful for fetching the value at an exact time in the past.

Evaluate the series for mountpoint `/` at Unix timestamp `1620000000`:

```promql theme={null}
node_filesystem_files{mountpoint="/"} @ 1620000000
```

Tip: Use an online Unix epoch converter, such as [https://www.epochconverter.com/](https://www.epochconverter.com/), to translate a human-readable date/time into the correct Unix timestamp.

## Quick reference: label matchers and examples

|  Matcher | Meaning                        | Example                                              |
| -------: | ------------------------------ | ---------------------------------------------------- |
|      `=` | Exact match                    | `node_cpu_seconds_total{cpu="0"}`                    |
|     `!=` | Not equal                      | `node_cpu_seconds_total{cpu!="0"}`                   |
|     `=~` | Regex match                    | `node_filesystem_files{mountpoint=~"^/run.*"}`       |
|     `!~` | Negated regex                  | `node_filesystem_files{mountpoint!~"^/run.*"}`       |
|  `[...]` | Range vector (past samples)    | `node_cpu_seconds_total{cpu="0"}[2m]`                |
| `offset` | Shift selector to past         | `... [5m] offset 30m`                                |
|      `@` | Evaluate at an exact timestamp | `node_filesystem_files{mountpoint="/"} @ 1620000000` |

## Notes about dashboards and PromQL

> **lightbulb** When using dashboards like [Grafana](https://grafana.com/docs/grafana/latest/), you usually don't need to manually calculate Unix epoch timestamps or `offset` windows—Grafana translates the dashboard time range into appropriate PromQL expressions. When querying directly in Prometheus's expression browser or via the Prometheus HTTP API, you'll need to use `offset` or the `@` modifier yourself to request historical data.

## Links and references

* [Prometheus query basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* [PromQL operators and functions](https://prometheus.io/docs/prometheus/latest/querying/operators/)
* [Grafana documentation](https://grafana.com/docs/grafana/latest/)
* [Unix epoch converter](https://www.epochconverter.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/2d798c38-7b90-41ca-9fe0-a522fc3b13e6)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/d5b05228-3115-4469-8de4-678de9b42118)
