# Steps to create a CPU alert in Azure Portal:
1. Go to Azure Monitor > Alerts  
2. Click New alert rule  
3. Select target resource (VM or App Service)  
4. Under Condition, choose "CPU Percentage"  
5. Set threshold (e.g., CPU > 80% for 5 minutes)  
6. Define an action group for notifications  
7. Review and create
```

By proactively tracking CPU trends, you can right-size VMs or refactor code before performance degrades.

***

## Memory Utilization

Memory utilization shows how much RAM your applications consume. Excessive memory usage can trigger slowdowns or out-of-memory errors.

<Frame>
  ![The image illustrates memory utilization issues, showing slow performance with a warning symbol and an application crash with an error message.](https://kodekloud.com/kk-media/image/upload/v1752867299/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/memory-utilization-issues-performance-warning.jpg)
</Frame>

### How to Monitor Memory

1. In Azure Portal, navigate to **Azure Metrics**.
2. Select your target resource (e.g., VM, Web App).
3. Add the **Memory Usage** metric to a chart.
4. Configure an alert on critical thresholds.

<Frame>
  ![The image is a flowchart illustrating a practical example of memory monitoring in three steps: navigating Azure metrics, selecting a relevant resource, and choosing a memory usage metric.](https://kodekloud.com/kk-media/image/upload/v1752867299/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/memory-monitoring-flowchart-azure-metrics.jpg)
</Frame>

Review memory usage graphs over time to uncover leaks or inefficient allocation:

<Frame>
  ![The image shows a memory monitoring graph with available memory data over time, highlighting average, 5th, and 10th percentile values. It emphasizes identifying trends and spikes in memory consumption.](https://kodekloud.com/kk-media/image/upload/v1752867300/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/memory-monitoring-graph-trends-spikes.jpg)
</Frame>

**Remediation Tips:**

* Optimize code to release unused memory
* Scale up the VM or App Service plan if needed

***

## Disk Performance

Disk performance metrics gauge how efficiently your storage layer handles read/write operations—vital for data-intensive workloads.

<Frame>
  ![The image illustrates disk performance, showing a diagram of data being read from and written to a storage disk, with accompanying text explaining the concept.](https://kodekloud.com/kk-media/image/upload/v1752867301/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/disk-performance-data-read-write-diagram.jpg)
</Frame>

### Key Disk Metrics

| Metric     | Description                            |
| ---------- | -------------------------------------- |
| IOPS       | Input/Output Operations per Second     |
| Latency    | Time taken for each read/write request |
| Throughput | Volume of data transferred per second  |

<Frame>
  ![The image is a diagram titled "Disk Performance" featuring three colored boxes labeled "Input/Output Operations per Second (IOPS)," "Latency," and "Throughput."](https://kodekloud.com/kk-media/image/upload/v1752867302/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/disk-performance-iops-latency-throughput.jpg)
</Frame>

<Frame>
  ![The image is a diagram titled "Disk Performance," showing three components: Input/Output Operations per Second (IOPS), Latency, and Throughput, with a note that throughput measures the amount of data transferred per second.](https://kodekloud.com/kk-media/image/upload/v1752867303/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/disk-performance-iops-latency-throughput-2.jpg)
</Frame>

Poor disk performance manifests as slow file operations and timeouts:

<Frame>
  ![The image illustrates a decline in disk performance, represented by a downward graph and arrows, with a label indicating "Poor disk performance."](https://kodekloud.com/kk-media/image/upload/v1752867304/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/poor-disk-performance-decline-graph.jpg)
</Frame>

<Frame>
  ![The image is a diagram about disk performance, highlighting issues like slow response times and increased latency, which impact user experience.](https://kodekloud.com/kk-media/image/upload/v1752867305/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/disk-performance-latency-response-times-diagram.jpg)
</Frame>

### Monitoring Disk Performance

* Enable metrics for IOPS, latency, and throughput on your storage account or managed disk.
* Use Azure Monitor and Azure Storage Metrics to chart and alert.
* Set thresholds (e.g., latency > 20 ms) to trigger notifications.

<Frame>
  ![The image is a diagram illustrating disk performance monitoring using Azure Monitor and Azure Storage Metrics to track IOPS, latency, and throughput.](https://kodekloud.com/kk-media/image/upload/v1752867306/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/disk-performance-monitoring-azure-diagram.jpg)
</Frame>

**Remediation Strategies:**

* Upgrade to Premium or Ultra disks
* Use striping and caching for high-throughput scenarios
* Implement an in-memory or CDN cache for hot data

***

## Network Performance

Network performance determines how swiftly and reliably data travels across your Azure resources and to end users.

Key metrics:

* **Bandwidth**: Maximum data transfer rate
* **Latency**: Round-trip time between endpoints
* **Packet Loss**: Percentage of dropped packets

Poor network health can cause application delays, timeouts, and degraded user satisfaction.

### Monitoring with Azure Network Watcher

1. Enable **Network Watcher** in your subscription.
2. Use **Connection Monitor** to assess latency and packet loss.
3. Review bandwidth usage on each virtual NIC.

<Frame>
  ![The image illustrates a practical example of network performance monitoring using Azure Network Watcher, focusing on bandwidth, latency, and packet loss.](https://kodekloud.com/kk-media/image/upload/v1752867307/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/azure-network-watcher-performance-monitoring.jpg)
</Frame>

Azure Network Watcher’s **Network Performance Monitor** provides end-to-end visibility:

<Frame>
  ![The image is a slide titled "Practical Example of Network Performance Monitoring," showing a diagram of network issues and listing corrective actions: optimizing network configurations, increasing bandwidth, and implementing QoS policies.](https://kodekloud.com/kk-media/image/upload/v1752867308/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/network-performance-monitoring-diagram.jpg)
</Frame>

**Remediation Tips:**

* Optimize routing, peering, and gateway configurations
* Increase bandwidth allocation for high-traffic workloads
* Apply QoS policies to prioritize mission-critical packets

***

## Benefits and Common Challenges

Proactive monitoring helps you:

* Detect issues before they impact users
* Optimize resource allocation and reduce costs
* Maintain consistent performance under load

However, you may encounter:

* Alert fatigue from too many notifications
* Difficulty selecting the most relevant metrics
* Balancing performance improvements with budget constraints

<Frame>
  ![The image is a diagram titled "Common Challenges," highlighting three issues: managing alert fatigue, identifying relevant metrics, and balancing performance and cost.](https://kodekloud.com/kk-media/image/upload/v1752867309/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Inspect-infrastructure-performance-indicators-including-CPU-memory-disk-and-network/common-challenges-alert-fatigue-metrics.jpg)
</Frame>

***

## References

* [Azure Monitor documentation](https://docs.microsoft.com/azure/azure-monitor/)
* [Azure Metrics in Azure Portal](https://docs.microsoft.com/azure/azure-monitor/essentials/metrics)
* [Azure Network Watcher overview](https://docs.microsoft.com/azure/network-watcher/)
* [AZ-400 Exam Guide](https://docs.microsoft.com/learn/certifications/exams/az-400)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/473876ba-f35b-4ae7-a361-3fc9572e593d/lesson/14a3b0ef-81f0-42d4-ad18-699cd8b90cea" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Analyze-Metrics/Introduction/page

Learn to analyze Azure metrics, monitor infrastructure performance, and leverage telemetry data for optimizing resource health and application performance.

In this lesson, you’ll learn how to analyze metrics for the AZ-400 exam by inspecting Azure infrastructure performance and leveraging telemetry data. Effective monitoring helps you optimize resource health, detect issues early, and ensure your applications run smoothly.

By the end of this tutorial, you'll be able to:

* Track critical infrastructure metrics (CPU, memory, disk, network)
* Configure Azure monitoring services and alerts
* Analyze usage and application performance telemetry
* Build custom dashboards and follow best practices for Azure performance management

***

Understanding core infrastructure metrics lets you proactively manage Azure resources and avoid bottlenecks.

## Key Metrics Overview

| Metric             | Definition                              | Azure Monitor Metric Name | Typical Threshold  |
| ------------------ | --------------------------------------- | ------------------------- | ------------------ |
| CPU Usage          | Percentage of CPU capacity in use       | Percentage CPU            | 70%                |
| Memory Utilization | Ratio of committed vs. available memory | Available Memory          | 80%                |
| Disk I/O           | Read/write operations per second        | Disk Read/Write Ops/Sec   | Varies by workload |
| Network Throughput | Inbound/outbound bytes per second       | Network In/Out Bytes      | Varies by workload |

<Frame>
  ![The image is a slide titled "Inspecting Infrastructure Performance Indicators, Including CPU, Memory, Disk, and Network," listing four key metrics: Understanding Key Metrics for Azure Performance Management, CPU Performance, Memory Utilization, and Disk Performance.](https://kodekloud.com/kk-media/image/upload/v1752867318/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/infrastructure-performance-indicators-metrics.jpg)
</Frame>

<Callout icon="lightbulb">
  Import these metrics into Azure Monitor to visualize trends, set alerts, and automate scaling actions.
</Callout>

## Practical Monitoring Scenarios

* **Scenario 1:** Scale out a compute cluster when CPU usage exceeds 75% for 5 minutes
* **Scenario 2:** Trigger an alert on sustained disk latency spikes in a database VM
* **Scenario 3:** Throttle network-intensive workloads to prevent bandwidth saturation

<Frame>
  ![The image is a slide titled "Inspecting Infrastructure Performance Indicators, Including CPU, Memory, Disk, and Network," listing three points: practical examples of performance monitoring, benefits of proactive performance, and common challenges.](https://kodekloud.com/kk-media/image/upload/v1752867319/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/infrastructure-performance-indicators-monitoring.jpg)
</Frame>

### Benefits & Challenges

| Benefit                          | Challenge                                 |
| -------------------------------- | ----------------------------------------- |
| Early issue detection            | Alert fatigue if thresholds too strict    |
| Optimized resource utilization   | Data overload without proper filtering    |
| Reduced downtime and faster MTTR | Misconfigured alerts can mask real issues |

***

Telemetry data provides deeper insights into application usage and performance.

<Frame>
  ![The image is a slide titled "Analyzing Metrics by Using Collected Telemetry, Including Usage and Application Performance," listing four topics related to Azure: introduction to telemetry, key services, monitoring services, and configuring alerts.](https://kodekloud.com/kk-media/image/upload/v1752867320/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/analyzing-metrics-telemetry-azure-slide.jpg)
</Frame>

## Configuring Alerts

1. Navigate to **Azure Monitor > Alerts**
2. Create an **Alert Rule** for a selected metric
3. Define **Action Groups** to notify, log, or trigger automation

<Callout icon="triangle-alert">
  Avoid setting excessive alert rules. Prioritize critical metrics to reduce noise and ensure timely response.
</Callout>

## Building Custom Dashboards

* Pin metric charts from multiple resources
* Use **Workbooks** for interactive reports
* Share dashboards with your team via Azure Portal

***

Monitor end-to-end application health by analyzing real usage metrics, dependencies, and response times.

<Frame>
  ![The image is a slide titled "Analyzing Metrics by Using Collected Telemetry, Including Usage and Application Performance," listing topics like monitoring application performance, analyzing usage metrics, custom dashboards in Azure Monitor, and best practices.](https://kodekloud.com/kk-media/image/upload/v1752867322/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Introduction/analyzing-metrics-telemetry-application-performance.jpg)
</Frame>

## Best Practices

* Enable **Application Insights** for distributed tracing
* Define **Failure Anomalies** to catch performance regressions
* Leverage **Live Metrics Stream** during load testing
* Tag resources consistently for grouped telemetry analysis

***

* [Azure Monitor Overview](https://docs.microsoft.com/azure/azure-monitor/overview)
* [Application Insights Documentation](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
* [Configure Azure Alert Rules](https://docs.microsoft.com/azure/azure-monitor/alerts/alerts-unified)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/473876ba-f35b-4ae7-a361-3fc9572e593d/lesson/09ccd487-b457-4d05-a6b9-5152368c62a1" />
</CardGroup>
