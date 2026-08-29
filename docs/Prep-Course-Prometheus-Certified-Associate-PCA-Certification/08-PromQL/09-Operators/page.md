# Five days ago
node_memory_Active_bytes{instance="node1"} offset 5d

# Two weeks ago
node_memory_Active_bytes{instance="node1"} offset 2w

# One and a half hours ago (two equivalent forms)
node_memory_Active_bytes{instance="node1"} offset 90m
node_memory_Active_bytes{instance="node1"} offset 1h30m
```

## @ — anchor to an exact timestamp

To evaluate a metric at an exact point in time, use the `@` modifier with a Unix timestamp (seconds since the epoch). This returns the sample closest to that timestamp:

<Frame>
  <img alt="The image is a slide titled &#x22;Offset Modifier,&#x22; explaining how to use the &#x22;@&#x22; modifier to navigate to a specific point in time, with a green label highlighting &#x22;@ modifier.&#x22;" />
</Frame>

```promql theme={null}
# Value at a specific Unix timestamp
node_memory_Active_bytes{instance="node1"} @1663265188
```

Note: Unix timestamps used with `@` are in seconds. Many tools can convert a human-readable time into the Unix epoch if needed.

## Combining @ and offset

You can combine `@` and `offset`. When both are present, the `@` timestamp serves as the anchor point and `offset` shifts relative to that anchor. The order of `@` and `offset` does not matter — both forms are equivalent:

```promql theme={null}
node_memory_Active_bytes{instance="node1"} @1663265188 offset 5m
node_memory_Active_bytes{instance="node1"} offset 5m @1663265188
```

Both queries return the metric value five minutes before the specified timestamp (for example, if the timestamp corresponds to 06:06, the returned value is from 06:01).

> **lightbulb** You can use `offset` and `@` with instantaneous vectors (single-value queries) or with range vectors (time windows). The `@` timestamp anchors the evaluation, and `offset` shifts that anchored timestamp or window.

## Range vectors with anchors and offsets

Range vectors use square brackets to request a window of samples, for example `[2m]`. By default, `[2m]` refers to the most recent two minutes. When combined with `@` and/or `offset`, the range vector is anchored and shifted accordingly:

```promql theme={null}
# Two minutes of data anchored at the timestamp (e.g., covering 06:04–06:06 if the timestamp is 06:06)
node_memory_Active_bytes{instance="node1"}[2m] @1663265188

# Two minutes of data anchored at the timestamp, then offset 10 minutes earlier
node_memory_Active_bytes{instance="node1"}[2m] @1663265188 offset 10m
```

These modifiers let you precisely inspect historical values and sample windows — useful for incident postmortems, trend analysis, and retroactive debugging.

## Additional resources

* Prometheus PromQL documentation: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
* PromQL examples and timestamp usage: [https://prometheus.io/docs/prometheus/latest/querying/expression/](https://prometheus.io/docs/prometheus/latest/querying/expression/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/b4de09eb-de60-4a9d-a193-b6f74f9889a3/lesson/79b04571-939c-45cb-adf9-7e273e92da79)


# Operators

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/PromQL/Operators/page

Guide to PromQL operators covering arithmetic, comparisons, bool modifier, precedence, and logical set operators with examples for building Prometheus queries and alerting rules

This lesson dives into PromQL operators — how to perform arithmetic, compare and filter series, combine expressions using logical set operators, and understand operator precedence. These concepts are essential for crafting precise Prometheus queries and reliable alerting rules.

## Arithmetic operators

Arithmetic operators perform numeric operations on instant vectors or scalars: addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), modulo (`%`), and power (`^`).

<Frame>
  <img alt="The image lists arithmetic operators along with their descriptions, providing basic math functions such as addition, subtraction, multiplication, division, modulo, and power." />
</Frame>

Operator quick reference:

| Operator | Meaning                |
| -------- | ---------------------- |
| `+`      | Addition               |
| `-`      | Subtraction            |
| `*`      | Multiplication         |
| `/`      | Division               |
| `%`      | Modulo (remainder)     |
| `^`      | Exponentiation (power) |

Example — convert bytes to kibibytes (KiB). `node_memory_active_bytes` reports memory in bytes; divide by `1024` to convert to KiB:

```bash theme={null}
$ node_memory_active_bytes{instance="node1"}
node_memory_active_bytes{instance="node1", job="node"} 2204815360

$ node_memory_active_bytes{instance="node1"} / 1024
{instance="node1", job="node"} 2153168
```

> **warning** Arithmetic on a metric produces a computed vector — the result does not preserve the original metric name. The result contains the same labels but no original metric identifier. This is expected PromQL behavior.

> **lightbulb** Dividing by `1000` converts to decimal kilobytes (kB); dividing by `1024` converts to kibibytes (KiB). Choose based on the unit system you want.

## Comparison operators

Comparison operators filter or compare metric values: `==`, `!=`, `>`, `<`, `>=`, `<=`.

<Frame>
  <img alt="The image displays a table of comparison operators with their descriptions, including equal, not equal, greater than, less than, greater or equal, and less or equal." />
</Frame>

Comparison operator examples:

| Operator | Use case              |
| -------- | --------------------- |
| `==`     | Equal to              |
| `!=`     | Not equal             |
| `>`      | Greater than          |
| `<`      | Less than             |
| `>=`     | Greater than or equal |
| `<=`     | Less than or equal    |

Example — filter network flags greater than `100`:

```bash theme={null}
$ node_network_flags
node_network_flags{device="enp0s3", instance="node1", job="node"} 5000
node_network_flags{device="enp0s3", instance="node2", job="node"} 4800
node_network_flags{device="lo", instance="node1", job="node"} 77
node_network_flags{device="lo", instance="node2", job="node"} 84

$ node_network_flags > 100
node_network_flags{device="enp0s3", instance="node1", job="node"} 5000
node_network_flags{device="enp0s3", instance="node2", job="node"} 4800
```

## The `bool` modifier

The `bool` modifier changes a comparison from a filter (dropping non-matching series) into a 0/1 indicator for each input series. This is especially useful for alerting rules where you need an on/off numeric signal rather than a filtered set.

Example — check which filesystems have less than `1000` bytes available:

```bash theme={null}
$ node_filesystem_avail_bytes
node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="node1", mountpoint="/boot/efi"} 53371
node_filesystem_avail_bytes{device="/dev/sda3", fstype="ext4", instance="node1", mountpoint="/"} 18771
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run"} 421
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run/lock"} 80012
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run/snapd/ns"} 872

$ node_filesystem_avail_bytes < bool 1000
node_filesystem_avail_bytes{device="/dev/sda2", fstype="vfat", instance="node1", mountpoint="/boot/efi"} 0
node_filesystem_avail_bytes{device="/dev/sda3", fstype="ext4", instance="node1", mountpoint="/"} 0
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run"} 1
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run/lock"} 0
node_filesystem_avail_bytes{device="tmpfs", fstype="tmpfs", instance="node1", mountpoint="/run/snapd/ns"} 1
```

A `1` indicates the comparison evaluated to true; `0` indicates false. Use these boolean vectors directly in alert expressions or downstream calculations.

## Operator precedence

PromQL evaluates expressions according to operator precedence. Higher-precedence operators are evaluated before lower-precedence ones. Operators on the same precedence level are left-associative (evaluated left-to-right), except exponentiation (`^`) which is right-associative.

<Frame>
  <img alt="The image explains the precedence order of binary operators in PromQL, listing them from highest to lowest, with additional information on operator associativity." />
</Frame>

Examples:

* `2 * 3 % 2` is evaluated as `(2 * 3) % 2` (left-to-right).
* `2 ^ 3 ^ 2` is evaluated as `2 ^ (3 ^ 2)` (right-to-left).

Always use parentheses when in doubt to make your intent explicit and avoid surprises.

## Logical operators: or, and, unless

PromQL provides three set-level logical operators that operate on series sets: `or`, `and`, and `unless`.

<Frame>
  <img alt="The image lists PromQL's three logical operators: OR, AND, and UNLESS, each with a colored checkmark." />
</Frame>

Behavior overview:

| Operator | Description                                                                      |
| -------- | -------------------------------------------------------------------------------- |
| `and`    | Intersection: returns series present in both left and right vectors.             |
| `or`     | Union: returns series present in either left or right vector.                    |
| `unless` | Set difference: returns series from the left that do not match any on the right. |

Examples

* Return filesystems with available bytes greater than `1000` and less than `3000` (intersection):

```bash theme={null}
$ node_filesystem_avail_bytes
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/"} 53371
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/var"} 1771
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/etc"} 421
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/home"} 2872

$ node_filesystem_avail_bytes > 1000 and node_filesystem_avail_bytes < 3000
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/var"} 1771
```

* Union: filesystems with available bytes less than `500` or greater than `70000`:

```bash theme={null}
$ node_filesystem_avail_bytes
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/home"} 53371
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/var"} 18771
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/etc"} 421
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/opt"} 80012

$ node_filesystem_avail_bytes < 500 or node_filesystem_avail_bytes > 70000
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/etc"} 421
node_filesystem_avail_bytes{instance="node1", job="node", mountpoint="/opt"} 80012
```

* `unless` (left set difference): return series greater than `1000` unless they are greater than `30000`:

```bash theme={null}
$ node_filesystem_avail_bytes > 1000 unless node_filesystem_avail_bytes > 30000
