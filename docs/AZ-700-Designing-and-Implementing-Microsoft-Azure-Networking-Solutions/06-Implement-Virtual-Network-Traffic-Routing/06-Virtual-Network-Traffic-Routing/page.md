# Virtual Network Traffic Routing

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-Virtual-Network-Traffic-Routing/Virtual-Network-Traffic-Routing/page

Guide to Azure virtual network routing, inspecting effective routes on NICs, and using user-defined routes and network virtual appliances to control traffic and outbound behavior

Virtual network traffic routing

Understanding how Azure routes traffic inside a virtual network is essential for designing secure, reliable connectivity between your resources and to the internet. This guide explains the routing layers, how to inspect the routes that apply to a network interface (NIC), and practical tips for using user-defined routes (UDRs) and network virtual appliances (NVAs).

How to inspect routes

* In the Azure portal, open the VM's network interface and view the Effective routes blade. This shows the exact routes applied to the NIC—similar to running the `route` command on a Windows or Linux VM—and includes the route source (system, default, or custom) and the next hop.
* Use the Effective routes view when troubleshooting connectivity to confirm which route will be used for a given destination.
* For automation or scripting scenarios, you can also inspect route tables and associations via the Azure CLI or REST API. See References below for official docs.

Routing layers in Azure

1. System routes

* Azure automatically creates system routes for every subnet in a virtual network. These built-in routes establish baseline connectivity for:
  * routing between subnets in the same virtual network (intra-VNet),
  * routing to the internet for public outbound access,
  * routing across peered virtual networks.
* System routes are managed by Azure and require no manual configuration. For example, after creating a virtual network peering, traffic flows between the peered VNets without adding any routes because system routes already cover that connectivity.

2. Default routes

* Default routes are implemented as part of the system routes and cover common scenarios so resources work out of the box. A typical default sends traffic for all destinations outside the VNet to the internet via the `0.0.0.0/0` route.
* Defaults provide sensible behavior initially; use UDRs if you need to change outbound behavior (for instance, route internet-bound traffic through an NVA).

3. Custom routes (User-defined routes, UDRs)

* Create custom routes in a route table and associate the table to one or more subnets to override or extend system/default routing.
* Common use case: send all internet-bound traffic through a firewall/NVA for inspection by creating a UDR with next hop type `Virtual appliance` pointing to the NVA’s IP.
* Azure uses longest-prefix match to pick the route that applies. A more specific (longer) prefix wins. If two routes share the same prefix length, a user-defined route takes precedence over system routes—so carefully design UDRs to avoid unintended routing behavior.

Table: Route types at a glance

| Route type          | Managed by           | Typical purpose                                         | Example                                      |
| ------------------- | -------------------- | ------------------------------------------------------- | -------------------------------------------- |
| System routes       | Azure platform       | Baseline intra-VNet, VNet-peering, and internet routing | Built-in intra-VNet routes                   |
| Default routes      | Azure (system route) | Generic outbound to internet (`0.0.0.0/0`)              | `0.0.0.0/0 → Internet`                       |
| Custom routes (UDR) | You (route table)    | Override or redirect traffic to NVAs/firewalls          | `10.0.0.0/16 → Virtual appliance (10.0.0.4)` |

Common next hop types

| Next hop type       | When to use                  | Example                                   |
| ------------------- | ---------------------------- | ----------------------------------------- |
| `VirtualNetwork`    | Intra-VNet routing           | Traffic to other subnets in the same VNet |
| `Internet`          | Public outbound access       | `0.0.0.0/0` directed to internet          |
| `Virtual appliance` | Send traffic to NVA/firewall | Next hop IP = firewall private IP         |
| `None`              | Blackhole a network          | Used to drop traffic intentionally        |

<Frame>
  <img alt="The image shows a screenshot of a network interface's effective routes in a virtual network traffic routing setup, along with explanations of system, default, and custom routes." />
</Frame>

> **lightbulb** To change routing for a subnet, create or update a route table with the desired routes and associate it with the subnet. Then use the Effective routes blade on a VM's network interface to verify which routes are in effect—system, default, and any user-defined routes.

Practical notes and best practices

* Route tables are applied at the subnet level; NICs inherit their subnet’s associated route table.
* Use the Effective routes blade to confirm the result of longest-prefix matching and UDR precedence.
* When routing through an NVA, ensure the NVA has the required inbound/outbound rules and that Azure NSGs do not block required traffic.
* Limit UDR scope to only the subnets that need custom routing to reduce risk of widespread misconfiguration.

> **warning** Misconfigured user-defined routes can disrupt connectivity (including access to Azure services or the internet). Test changes in a controlled environment and verify with the Effective routes blade before applying in production.

Additional details to keep in mind

* Azure selects the route based on the most specific prefix that matches the destination (longest-prefix match).
* If two routes have the same prefix length, a user-defined route takes precedence over a system route.
* Common next hop types include `VirtualNetwork`, `Internet`, and `Virtual appliance`. Use `Virtual appliance` to direct traffic to NVAs/firewalls for inspection or filtering.
* When using NVAs, ensure IP forwarding is enabled on the subnet/NIC if required by the NVA vendor.

Summary
Azure's layered routing model consists of system routes (baseline connectivity), default system routes (common outbound/intra-VNet cases), and custom user-defined routes for explicit control. Use route tables to implement UDRs, validate behavior with the Effective routes blade in the portal, and follow best practices to avoid unintended service disruptions.

Links and references

* [Azure route tables and user-defined routes](https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview)
* [View effective routes on a network interface in the Azure portal](https://learn.microsoft.com/azure/virtual-network/virtual-networks-effective-routes-overview)
* [Azure network virtual appliances (NVAs) guidance](https://learn.microsoft.com/azure/virtual-network/nva-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3289c34c-80e6-417c-af60-54cbbcee3f01/lesson/b9b1f6a5-a050-42d8-a964-f3b70bed90d9)
