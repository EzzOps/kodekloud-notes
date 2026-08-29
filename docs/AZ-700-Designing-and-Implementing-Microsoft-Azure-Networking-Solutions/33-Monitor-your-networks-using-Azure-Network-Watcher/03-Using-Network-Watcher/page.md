# Using Network Watcher

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Monitor-your-networks-using-Azure-Network-Watcher/Using-Network-Watcher/page

Guide to using Azure Network Watcher tools for monitoring, diagnosing, and troubleshooting network connectivity, NSG evaluations, packet captures, flow logs, and traffic analytics.

In this lesson we’ll review the core tools available in Azure Network Watcher, explain how each helps monitor and diagnose network issues, and show where to find them in the Azure portal. The content preserves the original diagram sequence and focuses on concise, actionable guidance for troubleshooting and observability.

## What Network Watcher gives you at a glance

Azure Network Watcher provides region-scoped diagnostics and monitoring features to help you visualize topology, validate connectivity, inspect NSG rule evaluation, capture packets, and analyze traffic patterns. Use the tools together to accelerate root-cause analysis across Azure and hybrid environments.

## Topology

Topology produces a visual map of a VNet (interfaces, VMs, subnets, NSGs and their associations), showing resource dependencies and how things connect. This is especially helpful in complex environments when you need to confirm NIC-to-VM mappings, subnet placement, and NSG attachments.

<Frame>
  <img alt="The image displays a network topology diagram with interconnected nodes labeled as VMs and network security groups, alongside a menu with options for visual representation, resource associations, relationship mapping, and regional instance." />
</Frame>

> **lightbulb** Topology is regional. Deploy or enable Network Watcher in the same Azure region as the VNet you want to visualize.

## Connection Monitor

Connection Monitor performs active connectivity checks between endpoints (for example VM-to-VM or on-premises-to-Azure). It measures latency, success/failure, and other telemetry and persists results in Azure Monitor (Metrics, Alerts, and Log Analytics) so you can track trends and create alerts.

<Frame>
  <img alt="The image is a diagram illustrating Azure's Connection Monitor 2.0, showing the flow between Azure VMs, non-Azure hosts, endpoints, and data storage in Azure Monitor. It highlights features like connectivity checks, latency comparison, end-to-end visibility, and data storage." />
</Frame>

## IP Flow Verify

IP Flow Verify simulates a single packet (TCP/UDP, inbound/outbound) for a VM and reports whether NSG rules would allow or deny it. Provide source/destination IPs and ports to determine which NSG rule (and its priority) made the decision.

<Frame>
  <img alt="The image shows a user interface for a network diagnostic tool labeled &#x22;IP Flow Verify,&#x22; displaying packet details with IP addresses and ports, with an indication that access is denied due to a security rule." />
</Frame>

## NSG diagnostics

NSG diagnostics lists inherited and explicit rules applied to NICs and subnets and explains the evaluation order. It’s ideal for resolving rule conflicts, confirming priorities, and understanding why traffic was allowed or denied.

<Frame>
  <img alt="The image shows an NSG (Network Security Group) diagnostics interface with options for rule troubleshooting, effective rules identification, traffic analysis, and resolution guidance. It includes a form for checking rule details, indicating an inbound traffic status as denied." />
</Frame>

## VPN Troubleshoot

VPN Troubleshoot validates site-to-site and point-to-site VPN paths and confirms the next hop for VPN traffic. It detects incorrect or unexpected routes caused by User-Defined Routes (UDR) or system routes and works across hybrid links.

<Frame>
  <img alt="The image shows a VPN troubleshooting interface with options for subscription, resource group, and location, displaying the status of resources. Below are buttons for route path identification, troubleshooting, misconfiguration detection, and hybrid scenario support." />
</Frame>

## Packet capture

Packet capture collects raw packet data to or from a VM. You can filter by VM, protocol, IP, or port and store captures in an Azure Storage account or on the VM. Use this when investigating latency spikes, dropped connections, or suspicious traffic.

<Frame>
  <img alt="The image shows a user interface for setting up a packet capture, with options for subscription, resource group, target virtual machine, and storage settings. There are buttons for different configuration areas such as network traffic recording, flexible targeting, storage options, and problem diagnosis." />
</Frame>

## Connection Troubleshoot

Connection Troubleshoot runs an end-to-end connectivity test between two endpoints, showing every hop and isolating failures caused by NSGs, UDRs, or firewalls. It visualizes the path and highlights where packets are blocked or delayed.

<Frame>
  <img alt="The image displays a &#x22;Connection Troubleshoot&#x22; interface with options including &#x22;End-to-End Connectivity Testing,&#x22; &#x22;Hop-by-Hop Analysis,&#x22; &#x22;Path Visualization,&#x22; and &#x22;Proactive Issue Detection,&#x22; along with a form for configuring network settings." />
</Frame>

## Flow Logs

Flow Logs capture NSG traffic records (source/destination IPs, ports, and allow/deny actions). Logs are stored in Azure Storage and can be forwarded to Log Analytics or SIEM tools for deeper analysis, retention, and correlation with other telemetry.

<Frame>
  <img alt="The image displays a flow logs interface for network security groups, showing a list with details like resource type, status, and location. It includes options for NSG traffic logging, detailed flow data, log storage, and analytics support." />
</Frame>

## Traffic Analytics

Traffic Analytics ingests flow logs via Log Analytics and visualizes traffic patterns, hotspots, blocked flows, and potential malicious attempts. It provides centralized dashboards and cross-region insights for trending and anomaly detection.

<Frame>
  <img alt="The image shows a dashboard for Traffic Analytics, highlighting features like NSG flow logs, log analytics integration, visual dashboards, workspace storage, and centralized monitoring. A graph displays inbound and outbound network traffic data, along with analytics of Azure regions, networks, and subnets." />
</Frame>

***

## Portal walkthrough — quick demos

The Network Watcher tools live in the Network Watcher blade in the Azure portal. Below are practical steps and what to expect in the UI for several common diagnostics.

### IP Flow Verify (portal steps)

1. Search for **Network Watcher** in the Azure portal.
2. Choose **IP Flow Verify** from the left-hand tools.
3. Select the VM and its NIC, choose protocol (TCP/UDP) and direction (inbound/outbound).
4. Enter local and remote IP addresses and ports, then run the test.\
   Network Watcher will report whether the packet would be allowed and which NSG rule matched.

<Frame>
  <img alt="The image shows a Microsoft Azure Network Watcher interface for IP flow verification, indicating that access is allowed for the specified inbound connection." />
</Frame>

Try an unauthorized port (for example TCP 8080) to see IP Flow Verify return **Access denied** and identify the blocking rule.

<Frame>
  <img alt="The image shows a Microsoft Azure &#x22;IP flow verify&#x22; tool interface with inputs for local and remote IP addresses and ports. The results section indicates &#x22;Access denied&#x22; due to a security rule labeled &#x22;DenyAllInBound.&#x22;" />
</Frame>

### NSG diagnostics (portal steps)

* Select **NSG diagnostics**, pick a VM and simulate traffic (protocol, direction, source IP, destination port).
* The tool runs a simulated evaluation and shows whether traffic would be allowed or denied and which rule matched (including priority and action).

<Frame>
  <img alt="The image shows the Microsoft Azure portal, specifically the Network Watcher NSG diagnostics page, displaying a denied inbound traffic result for specified IP addresses and port. It includes sections for source type, destination IP, and other diagnostic parameters." />
</Frame>

Click **View details** to see the rule evaluation order and the matching rule that caused the allow/deny decision.

<Frame>
  <img alt="The image shows an Azure Network Security Group (NSG) diagnostic screen detailing security rules for a virtual machine service. The rules indicate a denied action due to a &#x22;DenyAllInBound&#x22; rule applied." />
</Frame>

### Next hop

* Use the **Next Hop** tool to determine which route a VM uses for a destination IP (example: `8.8.8.8`).
* The result indicates next hop type (Internet, VirtualAppliance, VirtualNetworkGateway, VnetLocal, None) and whether a UDR or system route is used.

<Frame>
  <img alt="The image shows the Microsoft Azure Network Watcher interface, focusing on the &#x22;Next hop&#x22; tool, which helps specify a target virtual machine and destination IP to view the next network hop. The form includes fields for subscription, resource group, virtual machine, network interface, and IP addresses." />
</Frame>

### Connection Troubleshoot (demo)

Connection Troubleshoot aggregates multiple checks (connectivity, NSG diagnostics, Next Hop, port scan). Provide the VM, destination (URI/FQDN/IP), protocol version, and port (for example `443`), then run the test. The report shows reachability, probe counts, failures, average/max latency, and provides a hop-by-hop path with diagnostics.

<Frame>
  <img alt="The image shows the &#x22;Network Watcher | Connection Troubleshoot&#x22; page in the Microsoft Azure portal, where users can specify connection settings and diagnostics for troubleshooting network connections. The interface includes options for destination, probe settings, and connection diagnostic tests." />
</Frame>

The test summary includes overall reachability and a “See details” link to view per-hop diagnostics. In the sample run, the target was reachable with 66 probes, 0 failures, average latency 2 ms and max 7 ms.

<Frame>
  <img alt="The image shows the Microsoft Azure portal with a &#x22;Connectivity details&#x22; section displaying network connection statuses as &#x22;Healthy&#x22; for two endpoints. The interface includes options for running diagnostic tests and viewing additional information." />
</Frame>

### Flow Logs and Topology in the portal

* Use **Flow Logs** to enable NSG logging (allowed and denied flows). Store logs in Azure Storage and forward to Log Analytics or SIEM for retention and correlation.
* Use **Topology** to zoom into VNets and inspect VMs, NICs, NSG attachments, private endpoints, and IP configurations for quick verification of associations.

<Frame>
  <img alt="The image shows a network topology diagram in the Azure Network Watcher tool, displaying various virtual network connections and endpoints. The interface includes sections for monitoring, diagnostics, and topology mapping." />
</Frame>

### Connection Monitor & Traffic Analytics (portal)

* Use **Connection Monitor** to create continuous monitors for critical endpoints and push metrics to Azure Monitor.
* **Traffic Analytics** consumes NSG flow logs via Log Analytics to present dashboards, identify hotspots and blocked flows, and detect anomalies across regions.

<Frame>
  <img alt="The image shows the Microsoft Azure portal's Traffic Analytics page under Network Watcher, featuring options to monitor network traffic with a descriptive section and an infographic." />
</Frame>

***

## Tools quick reference

| Tool                    | Purpose                                                | Portal location / Output                                         |
| ----------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- |
| Topology                | Visualize VNets, NICs, NSGs, and associations          | Network Watcher → Topology                                       |
| Connection Monitor      | Continuous endpoint monitoring (latency, availability) | Network Watcher → Connection Monitor (Azure Monitor integration) |
| IP Flow Verify          | Simulate single packet through NSGs                    | Network Watcher → IP Flow Verify                                 |
| NSG diagnostics         | Detailed rule evaluation and priority matching         | Network Watcher → NSG diagnostics                                |
| Next Hop                | Determine route used to reach destination              | Network Watcher → Next hop                                       |
| Connection Troubleshoot | End-to-end path, hop-by-hop diagnostics                | Network Watcher → Connection Troubleshoot                        |
| Packet capture          | Collect raw packets for analysis                       | Network Watcher → Packet capture (stores to Storage/VM)          |
| Flow Logs               | Record allowed/denied NSG flows                        | Network Watcher → Flow Logs (Storage / Log Analytics)            |
| Traffic Analytics       | Analyze flow logs, dashboards and trends               | Log Analytics → Traffic Analytics                                |

***

## Conclusion

Azure Network Watcher is a comprehensive toolkit for visibility and troubleshooting across Azure and hybrid networks. Combine topology, connection tests, NSG evaluation, packet captures, flow logs, and analytics to speed root-cause analysis and maintain reliable, secure network operations.

For further reading:

* [Azure Network Watcher documentation](https://learn.microsoft.com/azure/network-watcher)
* [Monitor networks with Network Watcher — tutorials and best practices](https://learn.microsoft.com/azure/network-watcher/network-watcher-monitoring-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/31b3db0e-2227-4279-9b25-73af54822819/lesson/4eec4a0f-2ed3-4fd7-a8ba-eb6917d47b66)
