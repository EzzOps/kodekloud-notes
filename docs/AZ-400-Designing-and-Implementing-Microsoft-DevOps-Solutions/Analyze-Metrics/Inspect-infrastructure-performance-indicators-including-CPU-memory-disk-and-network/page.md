# Inspect infrastructure performance indicators including CPU memory disk and network

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Analyze-Metrics/Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/page

This guide explains how to monitor critical performance metrics in Azure, including CPU, memory, disk, and network indicators.

In this guide, you’ll discover how to monitor four critical performance metrics in Azure:

| Metric  | Why It Matters                                                | Azure Tools                                        |
| ------- | ------------------------------------------------------------- | -------------------------------------------------- |
| CPU     | Measures compute load and identifies processing bottlenecks   | Azure Monitor, Azure Metrics                       |
| Memory  | Tracks RAM consumption to prevent slowdowns and crashes       | Azure Monitor, Azure Metrics                       |
| Disk    | Monitors IOPS, latency, and throughput for data operations    | Azure Storage Metrics, Azure Monitor               |
| Network | Analyzes bandwidth, latency, and packet loss for connectivity | Azure Network Watcher, Network Performance Monitor |

Understanding these indicators is essential for maintaining optimal performance, minimizing downtime, and preparing for the AZ-400 exam. By keeping an eye on these metrics, you’ll ensure a smooth user experience while optimizing costs.

<Frame>
  ![The image is an infographic titled "Infrastructure Performance Indicators," highlighting four key performance indicators (KPIs): CPU usage, memory utilization, disk performance, and network activity.](https://kodekloud.com/kk-media/image/upload/v1752867295/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/infrastructure-performance-indicators-infographic.jpg)
</Frame>

***

## CPU Performance

CPU performance reflects the percentage of processing capacity your workloads consume. Sustained high CPU can lead to slow response times and application failures.

<Frame>
  ![The image illustrates CPU performance, highlighting that it is typically expressed as a percentage of total available CPU capacity.](https://kodekloud.com/kk-media/image/upload/v1752867295/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/cpu-performance-capacity-percentage-illustration.jpg)
</Frame>

Use Azure Monitor and Azure Metrics to collect real-time and historical CPU data:

<Frame>
  ![The image lists tools for monitoring CPU usage in Azure, specifically Azure Monitor and Azure Metrics.](https://kodekloud.com/kk-media/image/upload/v1752867296/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/azure-monitor-cpu-usage-tools.jpg)
</Frame>

High CPU usage often signals a busy application or a resource-intensive process. If it remains above 80% for extended periods, you may experience:

* Slow response times
* Increased processing latency
* Application crashes

<Frame>
  ![The image illustrates the impact of high CPU usage, showing slow performance with a warning symbol and an application crash with an error message.](https://kodekloud.com/kk-media/image/upload/v1752867297/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/high-cpu-usage-performance-warning-crash.jpg)
</Frame>

### Practical Example: Alerting on CPU Spikes

```shell theme={null}
