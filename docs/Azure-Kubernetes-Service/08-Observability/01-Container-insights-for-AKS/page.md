# Container insights for AKS

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Observability/Container-insights-for-AKS/page

This article explains how to use Container Insights for Azure Kubernetes Service to monitor and optimize containerized workloads.

Azure Monitor is Microsoft’s native solution for collecting and analyzing metrics and logs from applications, infrastructure, and Azure services. With Container Insights for Azure Kubernetes Service (AKS), you gain end-to-end visibility into your containerized workloads—helping you troubleshoot performance issues, improve availability, and optimize resource utilization.

![The image is a diagram of Azure Monitor, illustrating its components and processes, including data collection, insights, visualization, analysis, and response. It shows how data from applications, infrastructure, Azure platform, and custom sources is processed and utilized.](https://kodekloud.com/kk-media/image/upload/v1752869500/notes-assets/images/Azure-Kubernetes-Service-Container-insights-for-AKS/azure-monitor-diagram-components-processes.jpg)

It delivers:

* Real-time metrics and logs
* Interactive dashboards and workbooks
* Alerting and diagnostic capabilities

## What Is Container Insights?

Container Insights is an Azure Monitor feature built specifically for AKS clusters. It collects performance and health data across your nodes and containers, allowing you to:

* Detect resource hotspots
* Trace application failures
* Set up proactive alerts

Container Insights aggregates two primary data types:

| Data Type | Description                              | Examples                                          |
| --------- | ---------------------------------------- | ------------------------------------------------- |
| Metrics   | Numerical values over time               | CPU usage, memory consumption, network I/O        |
| Logs      | Structured or unstructured event records | Container logs, system events, application traces |

Metrics power visualizations and alerts, while logs are stored in a Log Analytics workspace for ad-hoc querying and root-cause analysis.

![The image is a diagram illustrating the process of container insights, showing how data from containers, Azure Kubernetes Service, and operating systems is collected and processed through metrics and logs for visualization, analysis, and response. It includes components like workbooks, metric explorer, log analytics, and alerts.](https://kodekloud.com/kk-media/image/upload/v1752869502/notes-assets/images/Azure-Kubernetes-Service-Container-insights-for-AKS/container-insights-diagram-azure-kubernetes.jpg)

## Azure Monitoring Agent Architecture

Enabling the monitoring add-on on AKS deploys two Azure Monitoring Agents (AMA):

| Agent Type     | Deployment Method     | Role                                |
| -------------- | --------------------- | ----------------------------------- |
| AMA ReplicaSet | ReplicaSet (1 pod)    | Cluster-level failover for metrics  |
| AMA DaemonSet  | DaemonSet (all nodes) | Node-level metrics & log collection |

Both agents send data to a dedicated Log Analytics workspace for storage and analysis.

## Demo: Create an AKS Cluster with Container Insights

Follow these steps in the Azure portal to spin up an AKS cluster with Container Insights:

1. Navigate to **Create Kubernetes cluster**.
2. Under the **Integration** tab, enable **Container Insights**.
3. (Optional) Enable **Managed Prometheus** and **Managed Grafana**.
4. For this demo, toggle **Alerting** *Off*.
5. Review and **Create**.

![The image shows a configuration page for creating a Kubernetes cluster, with options for enabling container insights, managed Prometheus, managed Grafana, and alerting settings.](https://kodekloud.com/kk-media/image/upload/v1752869503/notes-assets/images/Azure-Kubernetes-Service-Container-insights-for-AKS/kubernetes-cluster-configuration-page.jpg)

Once deployment finishes, open your AKS resource and select **Monitoring > Container Insights**.

## Exploring Cluster Metrics

The Container Insights dashboard provides a high-level overview of your AKS environment:

* Total node count
* CPU and memory utilization over time
* Active pod count

![The image shows a dashboard from KodeKloud-AKS Insights, displaying metrics for node CPU and memory utilization, node count, and active pod count over a six-hour period. The graphs indicate recent increases in CPU and memory usage.](https://kodekloud.com/kk-media/image/upload/v1752869505/notes-assets/images/Azure-Kubernetes-Service-Container-insights-for-AKS/kodekloud-aks-insights-dashboard-metrics.jpg)

## Generating Load with a Stress Test

To observe real-time metric changes, create CPU load in a test namespace:

```bash theme={null}
