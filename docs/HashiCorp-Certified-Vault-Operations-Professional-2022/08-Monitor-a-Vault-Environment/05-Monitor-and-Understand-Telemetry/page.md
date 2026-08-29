# Monitor and Understand Telemetry

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Operations-Professional-2022/Monitor-a-Vault-Environment/Monitor-and-Understand-Telemetry/page

This article focuses on monitoring Vault telemetry, audit logs, and operational logs for performance insights.

## Objective 2 Overview

In this lesson, we focus on monitoring a Vault environment. While Objective 1 emphasizes Vault configuration, Objective 2 covers:

* Monitor and understand Vault Telemetry
* Monitor and understand Vault Audit Logs
* Monitor and understand Vault Operational Logs

HashiCorp certification exams often use “understand” to mean that familiarity with core concepts is sufficient. With that in mind, let’s explore Vault telemetry: how to configure, collect, and visualize runtime metrics.

## What Is Vault Telemetry?

Vault telemetry is a set of runtime metrics that reveal how Vault performs and operates internally. Typical telemetry data includes:

* Write durations to the storage backend
* Vault’s response times for client API requests
* Node seal or initialization status

<Frame>
  ![The image is a slide explaining telemetry, describing it as the collection of runtime metrics for performance monitoring and debugging in a Vault environment. It mentions metrics aggregation every 10 seconds and sending telemetry information to aggregation solutions like DataDog or Prometheus.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878580/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Telemetry/telemetry-runtime-metrics-vault-explained.jpg)
</Frame>

Vault aggregates metrics every 10 seconds, keeps them in memory for one minute, and exposes them via a local endpoint. A telemetry agent on each Vault node usually scrapes this endpoint and ships data to an external monitoring solution such as DataDog, Prometheus, Splunk, or Grafana. These platforms enable you to build dashboards, charts, and alerts to track your Vault cluster’s health and performance.

<Callout icon="lightbulb">
  Telemetry metrics are held in-memory for only 60 seconds. Ensure your agent scrapes them at least every 10 seconds to avoid missing critical data.
</Callout>

## Supported Telemetry Providers

Configure telemetry in the `telemetry` stanza of your Vault HCL config. Vault supports multiple backends:

| Provider    | Use Case                                   | Recommended Platform |
| ----------- | ------------------------------------------ | -------------------- |
| statsite    | Simple, statsd-compatible aggregation      | Custom scripts       |
| statsd      | General metrics collection                 | Graphite, DataDog    |
| circonus    | Enterprise-grade monitoring                | Circonus             |
| dogstatsd   | DataDog-specific tags and metrics          | DataDog              |
| prometheus  | Pull-based model, native Vault integration | Prometheus           |
| stackdriver | Google Cloud monitoring                    | Google Stackdriver   |

<Frame>
  ![The image lists providers supported by Vault, including statsite, statsd, circonus, dogstatsd, prometheus, and stackdriver. It also features a Vault certification badge and a cartoon character.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878581/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Telemetry/vault-supported-providers-certification-cartoon.jpg)
</Frame>

Choose the provider that aligns with your observability stack: for example, use `dogstatsd` for DataDog and `prometheus` for Prometheus.

## Common Vault Telemetry Metrics

Vault emits a variety of metrics. Below are some key examples:

<Frame>
  ![The image is a table listing various metrics collected by Vault, with descriptions for each metric. It includes metrics like request handling duration, garbage collection pause, memory usage, and audit log request time.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878582/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Telemetry/vault-metrics-table-request-duration.jpg)
</Frame>

| Metric                            | Description                                              |
| --------------------------------- | -------------------------------------------------------- |
| vault.core.handleRequest          | Time taken to handle API requests                        |
| vault.runtime.totalGCPauseNS      | Nanoseconds spent in garbage collection (stop-the-world) |
| vault.runtime.memoryUsePercentage | Percentage of physical memory in use                     |
| vault.runtime.memoryUseTotalBytes | Total physical memory in use (bytes)                     |
| vault.audit.log.request           | Latency of sending audit log entries                     |
| vault.policy.getPolicy            | Duration to retrieve policy definitions                  |

For a comprehensive metric list, see the [Vault Telemetry documentation](https://www.vaultproject.io/docs/internals/telemetry).

## Configuring Telemetry in Vault

To enable telemetry, add a `telemetry` block to your Vault server’s HCL configuration. For example, to configure DogStatsD:

```hcl theme={null}
telemetry {
  dogstatsd_addr = "metrics.hcvop.com:8125"
  dogstatsd_tags = ["vault_env:production"]
}

seal "transit" {
  address  = "transit.hcvop.com:8200"
  key_name = "autounseal"
}
```

After updating your config, restart Vault or send a `SIGHUP` to reload the settings.

<Callout icon="triangle-alert">
  Incorrect telemetry configuration can lead to missing metrics or excessive network traffic. Always validate your HCL syntax and test connectivity to your metrics endpoint.
</Callout>

## Telemetry Workflow

A typical Vault telemetry workflow involves:

1. Vault emits runtime metrics on each node.
2. Local telemetry agent scrapes metrics (e.g., via DogStatsD or Prometheus endpoint).
3. Agent forwards data to a centralized system:
   * DataDog
   * Splunk
   * Prometheus
   * Grafana
4. Operations teams build dashboards and set up alerts based on these metrics.

<Frame>
  ![The image illustrates a telemetry workflow involving a Vault Admin configuring a Vault Server, which sends metrics upstream to an aggregation platform like DataDog, Splunk, Prometheus, or Grafana. The process includes creating dashboards and alerting for metric consumption.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878583/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Telemetry/telemetry-workflow-vault-admin-metrics.jpg)
</Frame>

Vault’s role ends at emitting and exposing metrics; the external monitoring system handles storage, visualization, and alerting.

## Sample Monitoring Dashboard

Below is an example Vault monitoring dashboard in DataDog, showing key metrics such as garbage collection pause durations, login request latency, and backend performance. This view helps you quickly assess the status and health of your Vault cluster.

<Frame>
  ![The image shows a dashboard for monitoring Vault, featuring various performance metrics, logs, and summaries. It includes graphs and data visualizations for runtime, storage backend, and token activities.](../../../../images/kodekloud.com/kk-media/image/upload/v1752878584/notes-assets/images/HashiCorp-Certified-Vault-Operations-Professional-2022-Monitor-and-Understand-Telemetry/vault-monitoring-dashboard-performance-metrics.jpg)
</Frame>

## Key Takeaways

* Telemetry provides real-time metrics about Vault’s performance and health.
* Metrics aggregation occurs every 10 seconds and is retained for 60 seconds in memory.
* Supported providers include statsite, statsd, circonus, dogstatsd, prometheus, and stackdriver.
* Monitor essential metrics: request duration, GC pause, memory usage, and audit log latency.
* On the exam, you may need to interpret or identify telemetry configurations; full hands-on setup is uncommon.

## Links and References

* [Vault Telemetry Configuration](https://www.vaultproject.io/docs/configuration/telemetry)
* [Vault Metrics](https://www.vaultproject.io/docs/internals/telemetry)
* [Vault Audit Logging](https://www.vaultproject.io/docs/audit)
* [Prometheus Documentation](https://prometheus.io/docs/)
* [DataDog Docs](https://docs.datadoghq.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-operations-professional-2022/module/36cf9665-35d2-4dbc-9ddc-fc00ca80cbd4/lesson/81ebbaf9-5f12-49df-b150-5d0c82a6493f" />
</CardGroup>
