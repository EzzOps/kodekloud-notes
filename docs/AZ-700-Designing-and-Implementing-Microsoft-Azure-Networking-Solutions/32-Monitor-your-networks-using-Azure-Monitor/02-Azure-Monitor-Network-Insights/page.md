# Azure Monitor Network Insights

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Monitor-your-networks-using-Azure-Monitor/Azure-Monitor-Network-Insights/page

Overview of Azure Monitor Network Insights for centralized monitoring, diagnostics, traffic analytics, and troubleshooting of Azure networking resources to manage health, connectivity, and performance.

Azure Monitor Network Insights centralizes visibility into the health, performance, and connectivity of your Azure networking estate. Instead of visiting multiple blades, Network Insights provides a single, consolidated view that surfaces health indicators, telemetry, and diagnostics for resources such as virtual networks, subnets, firewalls, VPNs, and ExpressRoute circuits.

Key benefits:

* Unified network health dashboard with per-resource health states (Available, Degraded, Unavailable).
* Deep traffic visibility via Traffic Analytics (top talkers, flow patterns, bandwidth usage).
* Integrated troubleshooting with Network Watcher tools such as Connection Monitor and Packet Capture.
* Proactive alerting for critical network failures.

<Frame>
  <img alt="The image shows a network monitoring interface with sections for network health, alerts, and various network components such as firewalls and VPN connections. A side menu highlights options like &#x22;Health and Alerts&#x22; and &#x22;Traffic Analytics.&#x22;" />
</Frame>

## What Network Insights monitors

Network Insights consolidates health, connectivity status, and performance metrics across network resources. Instead of manually aggregating logs, you get structured views and drill-downs that speed up root-cause analysis.

Highlights:

* Health rollups and per-resource health indicators.
* Telemetry for throughput, packet drops, and latency.
* Traffic Analytics and NSG flow log integration for traffic pattern analysis.
* Diagnostics links to Packet Capture, Connection Monitor, and other Network Watcher tools.

## Traffic Analytics

Traffic Analytics (built on Network Watcher) provides actionable insights into traffic flows and capacity planning:

* Identify top talkers, application-level traffic patterns, and bandwidth hotspots.
* Detect asymmetric routing, unexpected spikes, or potential throughput bottlenecks.
* Use Traffic Analytics to prioritize remediation and plan scaling or routing changes.

From Network Insights you can drill into a specific resource (for example, a VPN connection) to see packet drops, tunnel health, latency, and other contextual metrics—replacing manual log parsing with an interactive experience.

Troubleshooting workflows integrate with Network Watcher diagnostics such as Connection Monitor (end-to-end path checks) and Packet Capture (for packet-level investigation). These tools help isolate causes like misconfigured NSGs, routing issues, or upstream ExpressRoute interruptions.

> **lightbulb** To use Traffic Analytics and many Network Watcher features you may need to enable `Network Watcher` in the target region and enable diagnostic settings (for example, NSG Flow Logs). Ensure you have the required permissions and that diagnostic settings are configured for the resources you wish to monitor.

## Exploring Network Insights in the Azure portal

The Azure portal surfaces Network Insights under Azure Monitor > Insights > Networks. The layout is consistent across subscriptions; demo subscriptions may show limited telemetry but the interface remains the same.

Steps to navigate:

1. Open Azure Monitor in the portal and select Insights.
2. Choose Networks (expand the Insights menu if it’s not visible).
3. Browse the inventory of networking components (NICs, NSGs, private endpoints, public IPs, VNets, gateways).
4. Select a resource to open its blade and view metrics, health, and diagnostic links.

<Frame>
  <img alt="The image shows the Microsoft Azure Monitor overview dashboard, displaying options like &#x22;Application Insights,&#x22; &#x22;Container Insights,&#x22; and &#x22;VM Insights,&#x22; along with monitoring and diagnostic tools such as &#x22;Metrics,&#x22; &#x22;Alerts,&#x22; and &#x22;Logs.&#x22;" />
</Frame>

Inside the Networks view you’ll see alerts, an inventory of resources, and quick actions in the left pane. Selecting a specific network interface reveals standard metrics like bytes sent/received and packet counts—useful for baseline monitoring and swift anomaly detection.

<Frame>
  <img alt="The image shows a Microsoft Azure interface focusing on network resources, displaying network interfaces, security groups, and private endpoints along with their health status and alerts. There are no active alerts, and the network activity is shown with bytes sent and received." />
</Frame>

Many resource blades include a workbook icon. Opening the workbook launches prebuilt visualizations and contextual telemetry so you can analyze activity without manually configuring Metrics Explorer.

<Frame>
  <img alt="The image shows a Microsoft Azure interface displaying network metrics graphs for packets sent and received over time. The graphs indicate activity in bytes sent and received, with an observable increase around noon." />
</Frame>

If you use connectivity services (VPN Gateway, ExpressRoute), Network Insights integrates with Connection Monitor to show end-to-end connectivity and path diagnostics. For NSGs, Insights indicates whether flow logs and Traffic Analytics are enabled and surfaces related alerts—helpful when assessing telemetry coverage and configuration.

## Resource overview and typical metrics

| Resource Type                | What Network Insights shows                                       | Typical metrics / indicators                           |
| ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| Application Gateway          | Health state, throughput, failed requests, WAF alerts             | `Backend health`, `TotalRequests`, `FailedRequests`    |
| VPN Gateway / VPN connection | Tunnel health, latency, packet drops                              | `TunnelStatus`, `BytesTransferred`, `IKE/IpSec status` |
| Load Balancer                | Health of backend pool members, SNAT usage                        | `DipAvailability`, `SNATConnections`                   |
| ExpressRoute circuit         | Circuit status, peering metrics, latency                          | `ProvisioningState`, `IngressBytes`, `EgressBytes`     |
| Network Interface (NIC)      | Traffic, packet counts, connection health                         | `BytesSent`, `BytesReceived`, `PacketDrops`            |
| Network Security Group (NSG) | Flow log status, Traffic Analytics coverage, denied/allowed flows | `NSGFlowLogEnabled` (diagnostic)                       |

## Best practices

* Enable Network Watcher in each region where you have resources to capture regional diagnostics.
* Turn on NSG Flow Logs and send them to a Log Analytics workspace to enable Traffic Analytics.
* Configure proactive alerts for critical thresholds and health-state changes.
* Use workbooks and prebuilt visualizations for faster root-cause analysis and recurring reporting.

## Links and references

* Azure Monitor documentation: [https://learn.microsoft.com/azure/azure-monitor/](https://learn.microsoft.com/azure/azure-monitor/)
* Network Watcher overview: [https://learn.microsoft.com/azure/network-watcher/](https://learn.microsoft.com/azure/network-watcher/)
* Traffic Analytics overview: [https://learn.microsoft.com/azure/network-watcher/traffic-analytics](https://learn.microsoft.com/azure/network-watcher/traffic-analytics)

With that, we will move on to the last topic.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/9dfef54c-25b7-419f-a3f9-35b473feccf9/lesson/de739e38-a197-4584-b3a2-0a573e383027)
