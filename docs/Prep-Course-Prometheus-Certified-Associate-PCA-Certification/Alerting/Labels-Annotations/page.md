# First query result
node_filesystem_avail_bytes{device="tmpfs", instance="node1", mountpoint="/run/lock"} 547

# A broader query returning two results
node_filesystem_avail_bytes < 2000
# returns:
node_filesystem_avail_bytes{device="tmpfs", instance="node1", mountpoint="/run/lock"} 547
node_filesystem_avail_bytes{device="/dev/sda2", instance="node1", mountpoint="/"} 1228
```

The second query produces two results, so Prometheus would produce two alert instances — one per filesystem.

<Callout icon="lightbulb">
  Prometheus evaluates alert expressions and generates alert instances, but it does not deliver notifications (email, SMS, Slack). That responsibility belongs to Alertmanager, which receives alerts from Prometheus and handles deduplication, grouping, silencing, and routing to external channels.
</Callout>

<Frame>
  <img alt="The image illustrates the alerting process in Prometheus, showing that Prometheus triggers alerts but does not send notifications, which are handled by a separate process called Alertmanager. The diagram includes arrows showing alerts being managed by Alertmanager and distributed to users via platforms like Gmail, Slack, and another messaging service." />
</Frame>

## Alert rules and rule files

Alert rules are defined in the same rule format as recording rules. The main difference is the presence of the `alert` key for alerting rules, while recording rules use `record`. Both rule types can live in the same rule group.

Example rule group containing a recording rule and an alert:

```yaml theme={null}
groups:
  - name: node
    interval: 15s
    rules:
      - record: node_memory_memFree_percent
        expr: 100 * node_memory_MemFree_bytes{job="node"} / node_memory_MemTotal_bytes{job="node"}
      - alert: LowMemory
        expr: node_memory_memFree_percent < 20
        for: 3m
```

In this example:

* `node_memory_memFree_percent` is a recording rule used to precompute a metric.
* `LowMemory` is an alert that fires when `node_memory_memFree_percent < 20` has held true for 3 minutes.

Another common alert is detecting targets that are down. The `up` metric returns 0 for unreachable targets:

```yaml theme={null}
groups:
  - name: node
    rules:
      - alert: NodeDown
        expr: up{job="node"} == 0
        for: 5m
```

The `for` clause delays the alert transition to firing until the expression has been true for the given duration. This prevents alerts from firing on transient scrape failures or brief network blips.

<Callout icon="warning">
  Use `for` to avoid false positives for sustained conditions (e.g., sustained high CPU). For extremely urgent conditions (e.g., data corruption, loss of control plane) keep `for` short or omit it to allow faster notifications.
</Callout>

## Example alerts file

Prometheus reads rule files (commonly placed under `/etc/prometheus/rules.yml` or a rules directory). Example snippet:

```yaml theme={null}
groups:
  - name: node
    rules:
      - alert: LowMemory
        expr: node_memory_memFree_percent{job="node"} < 20
        for: 3m
      - alert: NodeDown
        expr: up{job="node"} == 0
        for: 3m
```

When you open the Alerts tab in the Prometheus UI you'll see these alerts and their current states.

## Alert lifecycle and states

Prometheus alerts go through three states:

| State    | Description                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------- |
| Inactive | The expression returns no results (condition not present).                                                |
| Pending  | The expression returned results but the `for` duration has not yet elapsed; alert is awaiting transition. |
| Firing   | The expression has been true for at least the `for` duration; Prometheus sends the alert to Alertmanager. |

## Quick reference: alert rule fields

| Field         | Purpose                                                   | Example                                        |
| ------------- | --------------------------------------------------------- | ---------------------------------------------- |
| `alert`       | Name of the alert                                         | `LowMemory`                                    |
| `expr`        | PromQL expression that defines the alert condition        | `node_memory_memFree_percent{job="node"} < 20` |
| `for`         | Delay before alert becomes `firing`                       | `3m`                                           |
| `labels`      | Add or override labels for the alert instance             | `severity: "critical"`                         |
| `annotations` | Human-readable information shown in UIs and notifications | `summary: "Node memory low"`                   |

## Putting it together: Prometheus + Alertmanager

* Prometheus evaluates alerting rules and creates alert instances when expressions match timeseries.
* Prometheus sends alerts to one or more Alertmanager instances.
* Alertmanager handles deduplication, grouping, silencing, and routing notifications to integrations such as email, Slack, PagerDuty, or webhooks.
* A single Alertmanager can receive alerts from multiple Prometheus servers across environments.

This separation of concerns creates a reliable alerting pipeline: Prometheus for evaluation, Alertmanager for delivery and routing.

## Links and references

* [Prometheus Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
* [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/91532f0e-a56b-46c5-88fe-57e3ad48b1d4" />
</CardGroup>


# Labels Annotations

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Labels-Annotations/page

Explains Prometheus alert labels versus annotations and best practices for routing, grouping, and human readable notification content

Labels and annotations are two distinct parts of a Prometheus alert definition. Use labels to identify, group, and route alerts in Alertmanager. Use annotations to attach human-readable details (descriptions, runbooks, links) that appear in notifications.

## Labels

Labels are key/value pairs that become part of an alert's identity. Alertmanager uses labels for routing, grouping, deduplication, and inhibition. To assign labels to an alert, include a `labels` block in the rule and add the relevant key/value pairs.

Example — adding severity labels to rule definitions:

```yaml theme={null}
groups:
  - name: node
    rules:
      - alert: NodeDown
        expr: up{job="node"} == 0
        labels:
          severity: warning
      - alert: MultipleNodesDown
        expr: avg_without(instance)(up{job="node"}) <= 0.5
        labels:
          severity: critical
```

<Callout icon="lightbulb">
  Labels affect alert identity, deduplication, grouping, and routing in Alertmanager. Use them for any matching or routing logic.
</Callout>

## Annotations

Annotations are intended for human-readable information included in notifications. They do not change an alert’s identity and therefore cannot be used for routing or matching in Alertmanager. Typical uses are descriptions, runbook links, and diagnostic hints.

Annotations support templating using the Go template language. When writing templates, reference alert fields via the `alert` object. Because MDX and other processors can misinterpret template braces, always wrap template expressions in inline code or fenced code blocks.

Common template fields:

* `{{ .Labels }}` — the full labels map
* `{{ .Labels.instance }}` — the `instance` label value
* `{{ .Value }}` — the firing sample value (the metric value that caused the alert to fire)

Example — using an annotation to provide a human-readable description:

```yaml theme={null}
groups:
  - name: node
    rules:
      - alert: node_filesystem_free_percent
        expr: 100 * node_filesystem_free_bytes{job="node"} / node_filesystem_size_bytes{job="node"} < 70
        annotations:
          description: "filesystem {{ .Labels.device }} on {{ .Labels.instance }} is low on space, current available space is {{ .Value }}"
```

When this alert fires the `description` will be rendered with concrete values, for example:
filesystem `/dev/sda3` on `10.0.0.5:9100` is low on space, current available space is `20.40345`.

<Callout icon="warning">
  Remember: use `{{ .Labels }}` (capital L) and `{{ .Value }}` (capital V) in templates. Labels are used by Alertmanager for routing; annotations are only for notification content and will not affect routing or matching.
</Callout>

## Labels vs Annotations — Quick Comparison

|     Concept | Purpose                                                                                          | Example                                                                     |
| ----------: | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
|      Labels | Used for alert identity, routing, grouping, deduplication in Alertmanager                        | `severity: critical`                                                        |
| Annotations | Human-readable notification content (descriptions, runbooks, links); templated with Go templates | `description: "disk {{ .Labels.device }} on {{ .Labels.instance }} is low"` |

## Best Practices

* Keep labels stable and meaningful (e.g., `severity`, `team`, `service`) so routing rules remain predictable.
* Avoid putting large or frequently-changing text in labels — use annotations for verbose or dynamic content.
* Template annotations to include contextual details (`instance`, `device`, metric value) so notifications are actionable.
* Test templates with sample alerts to ensure correct rendering and escaping.

## Links and References

* [Alertmanager — Prometheus Alerting](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [Prometheus Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
* [Go text/template package](https://pkg.go.dev/text/template)
* [MDX Documentation](https://mdxjs.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/49dae37b-171f-416f-a715-28a083b2b436" />
</CardGroup>
