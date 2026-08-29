# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Introduction/page

Explains Prometheus alerting using PromQL, alert rule structure, lifecycle states, and Alertmanager's role in grouping routing and delivering notifications.

In this lesson we'll cover Prometheus alerting: how to define alerting conditions with PromQL, how Prometheus generates alerts, and how Alertmanager handles routing and notifications. Alerting is critical for production systems — it ensures teams are notified of issues (disk full, node down, high latency) even when nobody is actively watching dashboards.

<Frame>
  <img alt="The image illustrates a system alert scenario, showing server icons with a &#x22;Low disk space&#x22; alert, and a sleeping administrator with the text suggesting a need for alert mechanisms when problems occur." />
</Frame>

Prometheus alerting works by evaluating PromQL expressions. When an expression returns one or more vectors, Prometheus generates an alert instance for each matching timeseries.

Example: alert when a filesystem has less than 1000 bytes available:

```promql theme={null}
node_filesystem_avail_bytes < 1000
```

If this query returns a vector such as:

```promql theme={null}
node_filesystem_avail_bytes{device="tmpfs", instance="node1", mountpoint="/run/lock"} 547
```

Prometheus creates one alert instance for that filesystem (because it has only 547 bytes available). If the query returns multiple vectors, each matching timeseries becomes a separate alert instance:

```promql theme={null}
