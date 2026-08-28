# Summary

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Configure-Monitoring-for-a-DevOps-Environment/Summary/page

This guide covers continuous monitoring in Azure using Azure Monitor, Log Analytics, and Azure Insights for optimal performance and issue resolution.

## Introduction

Continuous monitoring is critical for detecting and resolving issues before they impact end users. In this guide, you’ll learn how to leverage Azure Monitor, Log Analytics, and Azure Insights to achieve end-to-end observability, ensure high availability, and maintain optimal performance in your cloud environment.

***

## Azure Monitor Overview

Azure Monitor provides a unified platform to collect, analyze, and act on telemetry from:

* Applications
* Infrastructure
* Networking

<Callout icon="lightbulb">
  By consolidating metrics and logs across your Azure resources, Azure Monitor helps you identify performance bottlenecks, diagnose failures, and automate remediation.
</Callout>

### Key Capabilities

* **Telemetry Collection**: Automatically gather metrics and logs from Azure resources and custom sources.
* **Analysis & Visualization**: Use built-in charts, dashboards, and workbooks for insights.
* **Automation & Integration**: Connect with Logic Apps, Functions, and DevOps tools for incident response.

### Integrations

Azure Monitor seamlessly integrates with:

* **Azure DevOps** for pipeline telemetry
* **GitHub Actions** for CI/CD observability
* **Third-party tools** via REST API or Azure Event Hubs

***

## Azure Log Analytics

Log Analytics is the analytics engine behind Azure Monitor logs. It enables you to store, query, and visualize large volumes of operational data using Kusto Query Language (KQL).

### Getting Started

1. **Create a Workspace**
   ```azurecli theme={null}
   az monitor log-analytics workspace create \
     --resource-group MyResourceGroup \
     --workspace-name MyLogWorkspace \
     --location eastus
   ```
2. **Ingest Data**: Connect VMs, containers, and platform resources to the workspace.
3. **Run KQL Queries**: Filter, correlate, and visualize your data.

### Example KQL Query

```kusto theme={null}
// Top 5 VMs by CPU usage in the last hour
Perf
| where TimeGenerated > ago(1h) and CounterName == "% Processor Time"
| summarize AvgCPU = avg(CounterValue) by Computer
| top 5 by AvgCPU desc
```

<Callout icon="lightbulb">
  Use `render` operators (e.g., `render timechart`) in KQL to quickly visualize trends directly in the Log Analytics query pane.
</Callout>

***

## Configuring Azure Monitor Alerts

Define alerts to proactively notify your team when metrics cross thresholds. Here’s how to create a high-CPU alert:

```azurecli theme={null}
az monitor metrics alert create \
  --name HighCpuAlert \
  --resource-group MyResourceGroup \
  --scopes /subscriptions/00000000-0000-0000-0000-000000000000/[AWS_SECRET_ACCESS_KEY]/Microsoft.Compute/virtualMachines/MyVM \
  --condition "avg Percentage CPU > 80" \
  --evaluation-frequency 5m \
  --window-size 5m \
  --action-group MyActionGroup
```

***

## Azure Insights: Deep Dives by Resource Type

Azure Insights extends Azure Monitor to provide specialized monitoring for different resource families.

| Insight Type    | Description                                                                     |
| --------------- | ------------------------------------------------------------------------------- |
| **Application** | End-to-end web app monitoring with performance, usage, and failure telemetry.   |
| **VM**          | Health and performance insights for VMs and VM Scale Sets.                      |
| **Container**   | Visibility into AKS/ACI workloads, including container metrics and logs.        |
| **Storage**     | Observability for Blob, Table, Queue, and File storage services.                |
| **Network**     | Network Watcher tools for connectivity checks, traffic analytics, and topology. |

***

## Best Practices

* Tag resources consistently to filter metrics and logs by environment, team, or application.
* Centralize logs in a single Log Analytics workspace when feasible.
* Automate alert actions with Logic Apps or Azure Functions for faster incident response.
* Regularly review dashboards and alerts to adjust thresholds as your environment scales.

***

## Conclusion

By implementing a robust continuous-monitoring strategy in Azure—combining Azure Monitor, Log Analytics, and specialized Insights—you can maintain high performance, maximize uptime, and quickly respond to incidents. Start by setting up your Log Analytics workspace, authoring KQL queries, and creating proactive alerts, then expand into resource-specific Insights for comprehensive observability.

***

## Links and References

* [Azure Monitor Documentation](https://learn.microsoft.com/azure/azure-monitor/)
* [Log Analytics and KQL](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
* [Azure Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview)
* [Azure Network Watcher](https://learn.microsoft.com/azure/network-watcher/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/7e7ab3a7-8b66-40ef-9f77-1988e32b786d/lesson/37acebb3-918f-4cde-a9ed-4a4e2c7ef073" />
</CardGroup>
