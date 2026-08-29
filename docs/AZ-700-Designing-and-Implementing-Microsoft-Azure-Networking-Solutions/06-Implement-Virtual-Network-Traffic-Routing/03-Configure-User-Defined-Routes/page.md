# Configure User Defined Routes

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-Virtual-Network-Traffic-Routing/Configure-User-Defined-Routes/page

Configuring Azure user-defined routes to direct subnet traffic through network virtual appliances for inspection and security, including deployment, verification, and best practices.

Control traffic flow inside an Azure virtual network by creating custom routing rules. User-defined routes (UDRs) let you override Azure system routes and direct traffic between subnets, VNets, and network appliances (for example, a firewall or network virtual appliance — NVA).

On the left side of the diagram below you can see a virtual network split into subnets (front-end, back-end, and DMZ). A virtual appliance (commonly a firewall or NVA) is placed in the DMZ. Traffic from the front-end subnet is routed through the DMZ to the back-end. The route table controls exactly how this traffic is forwarded.

<Frame>
  <img alt="The image illustrates a virtual network traffic routing setup, showing a network diagram with subnets and a routing table, alongside a form for creating a route table." />
</Frame>

To create UDRs you build an Azure route table, add routes that match the destination prefix (single IP, CIDR, or service tag), and associate the route table with a subnet. When a packet leaving the subnet matches a user-defined route, Azure forwards it to the specified next hop instead of following the default system path.

The portal UI for creating a route table is shown on the right side of the diagram: you select subscription, resource group, name, and whether to propagate gateway routes. In most cases keep gateway route propagation enabled unless you have a specific reason to disable it.

When adding a route you specify:

* Route name
* Destination address prefix (single IP, CIDR such as a subnet, or a service tag)
* Next hop type (for NVAs choose `VirtualAppliance`)
* Next hop IP address (the appliance private IP)

This redirects traffic to the appliance for inspection or filtering instead of sending it directly to the destination.

Below is the portal dialog for associating a route table to a subnet — associating a route table to a subnet activates the UDR for that subnet.

<Frame>
  <img alt="The image shows a setup guide for creating a custom route and associating a route table to a subnet in a network configuration context, with fields for route name, destination type, and next hop details." />
</Frame>

Summary: UDRs override Azure system routes and force traffic through NVAs or firewalls when needed — useful for enhanced security, packet inspection, or non-default traffic flows. When we cover Azure Firewall, UDRs will be used to steer traffic through the firewall.

This lesson/demo deploys a simple topology and validates how UDRs force traffic to an NVA (a Linux VM with IP forwarding enabled). The topology contains two spoke VNets (East US and West US) peered to a central hub VNet that hosts the NVA.

Infrastructure overview

|        Component | Role / Private IP                                                       |
| ---------------: | ----------------------------------------------------------------------- |
| Spoke East US VM | `vm-az700-udr-spoke-eus-01` — 10.50.1.4                                 |
| Spoke West US VM | `vm-az700-udr-spoke-wus-01` — 10.60.1.4                                 |
|       Hub NVA VM | `vm-az700-udr-hub-01` — 10.70.1.4 (Linux VM with IP forwarding enabled) |
|     VNet peering | Spokes peered with hub (peering configured to allow forwarded traffic)  |

The demo can be deployed with PowerShell. The snippets below highlight variable declarations, public IPs, NSGs, NIC creation (with IP forwarding enabled on the NVA NIC), and VM configuration. This example is for lab/demo use only.

```powershell theme={null}
