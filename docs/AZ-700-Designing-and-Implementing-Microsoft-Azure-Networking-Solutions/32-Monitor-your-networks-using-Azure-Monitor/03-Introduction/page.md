# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Monitor-your-networks-using-Azure-Monitor/Introduction/page

Explains how Azure Monitor collects and visualizes network telemetry using Metrics Explorer and Network Insights to detect, analyze, and troubleshoot Azure network issues.

In this lesson you'll learn how Azure Monitor helps you monitor, analyze, and troubleshoot your Azure networks.

We cover how Azure Monitor collects telemetry from your resources, how to visualize that telemetry using Metrics Explorer, and how to use Network Insights to gain end-to-end visibility across your Azure network environment. As you progress you'll see how telemetry flows into Azure Monitor and how built-in tools help you detect, investigate, and resolve network issues across your deployment.

## Lesson objectives

| Objective                                             | What you'll learn                                                                                                              | Key features / terms                                                      |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Understand Azure Monitor telemetry sources            | How Azure Monitor gathers metrics, logs, and traces from Azure resources via platform metrics, diagnostic settings, and agents | `platform metrics`, `diagnostic settings`, `Azure Monitor agents`         |
| Visualize and analyze telemetry with Metrics Explorer | How to create charts, use aggregations, apply filters and dimensions, and compare real-time and historical trends              | Metrics Explorer, aggregations, filters, dimensions                       |
| Use Network Insights for network health and analytics | How to view topology, check connectivity, analyze traffic, and troubleshoot capacity or performance issues                     | Azure Monitor Network Insights, topology, connectivity, traffic analytics |

<Frame>
  <img alt="The image outlines three learning objectives related to Azure Monitor: understanding its function, using Metrics Explorer for data visualization, and exploring Network Insights for network health and analytics." />
</Frame>

Throughout this lesson we'll build on these objectives to show how telemetry—metrics, logs, and distributed traces—flows into Azure Monitor and how the built-in analysis and visualization tools help you detect, investigate, and remediate network issues across your Azure environment.

> **lightbulb** Key telemetry sources to remember: platform metrics (lightweight, near real-time), diagnostic settings (resource-level logs and metrics), and agents (VM-level logs and insights). Use the right source depending on the level of detail and retention you need.

> **warning** Be mindful of data ingestion and retention costs when enabling diagnostic settings or agent-based telemetry for many resources—plan retention and sampling that match your troubleshooting and compliance requirements.

## Links and references

* [Azure Monitor overview](https://learn.microsoft.com/azure/azure-monitor/overview)
* [Metrics Explorer documentation](https://learn.microsoft.com/azure/azure-monitor/metrics/metrics-explorer)
* [Network Insights for Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/network/overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/9dfef54c-25b7-419f-a3f9-35b473feccf9/lesson/a0bec4cb-df49-4124-b100-eb14c15c397e)
