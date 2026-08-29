# Show effective routes for a network interface
az network nic show-effective-route-table --name MyNic --resource-group MyResourceGroup
```

To validate the route table associated with a subnet from the CLI:

```bash theme={null}
# Show subnet details including associated route table
az network vnet subnet show \
  --resource-group MyResourceGroup \
  --vnet-name MyVNet \
  --name MySubnet \
  --query "routeTable"
```

To list routes in a route table:

```bash theme={null}
az network route-table route list \
  --resource-group MyResourceGroup \
  --route-table-name MyRouteTable
```

Tip: Look for overlapping prefixes, unexpected next hops, and route priorities. Azure selects routes by longest-prefix match; UDRs override system routes for equal-length prefixes.

## 2) Use Azure Network Watcher to validate traffic paths

Azure Network Watcher provides tools to visualize traffic, validate hops, and find where packets are dropped.

<Frame>
  <img alt="The image is a slide titled &#x22;Diagnosing a Routing Problem,&#x22; listing two steps: &#x22;Check effective routes&#x22; and &#x22;Use Network Watcher.&#x22;" />
</Frame>

Network Watcher tools to try:

| Tool                    | Purpose                                                                                                        |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| IP Flow Verify          | Check whether traffic is allowed or denied for a 5-tuple (src/dst IP, protocol, src/dst port).                 |
| Next Hop                | Determine the next hop for traffic from a VM to a destination IP (shows which device will receive the packet). |
| Connection Troubleshoot | Test end-to-end connectivity and reveal the path between two endpoints.                                        |
| Packet capture          | Capture packets on a VM for deeper inspection and post-capture analysis.                                       |

Reference: [Azure Network Watcher documentation](https://learn.microsoft.com/azure/network-watcher/)

## 3) Verify user-defined routes (UDRs) and route table associations

UDRs let you steer traffic through firewalls, NVAs, or custom gateways for inspection, logging, or policy enforcement. Validate any custom routes for:

* Correct destination prefixes (no accidental overlaps)
* Correct next hop type and next hop IP
* Appropriate priority (UDRs override system routes when applicable)
* Proper association with the intended subnet

If a subnet isn't associated with the intended route table, Azure will apply the default/system routes instead.

> **lightbulb** Always verify route table associations on the subnet level. A mis-associated subnet will silently use system routes instead of your custom routes.

Common CLI checks to confirm associations and route contents are shown above. Use these to ensure the actual configuration matches your design.

## 4) Watch for asymmetric routing (and why it breaks inspection)

Asymmetric routing happens when outbound and return traffic follow different paths. This often breaks stateful inspection in firewalls and NVAs or causes return packets to be dropped.

How to avoid or detect asymmetric routing:

* Ensure return paths traverse the same NVA or gateway (configure symmetric routing on both sides).
* For hub-and-spoke or forced-tunneling designs, make sure spokes and the hub have consistent route tables and next hops.
* Check for SNAT, BGP path changes, or source/destination-based routing that may alter the return path unexpectedly.
* Use Network Watcher's Connection Troubleshoot and Next Hop tools to confirm both directions.

## 5) Confirm appliances, gateways, and load balancers are healthy

If you force traffic through an NVA or gateway, ensure those devices are online and functioning; otherwise you’ll see drops or blackholes.

Common quick checks

| Component               | What to check                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------- |
| NVA / VM                | Is the VM running and reachable? Test SSH/ICMP and check OS-level forwarding settings. |
| NSGs                    | Are security rules allowing management and forwarding traffic (including probes)?      |
| Load balancer / Gateway | Are health probes passing? Are backend pools configured correctly?                     |
| BGP / Peering           | Are BGP sessions established and is the expected prefix advertisement present?         |

Additional diagnostic tips

* Reproduce the failing flow and capture packet traces on the VM (packet capture) for suspicious behavior.
* Use incremental testing: validate routing on the VM/NIC, then subnet, then route tables, then NVAs/gateways.
* Keep a simple map of expected paths (e.g., source → next hop → final destination) to compare against effective routes.

## Summary checklist

* View effective routes on the VM/NIC.
* Use Network Watcher tools (IP Flow Verify, Next Hop, Connection Troubleshoot, Packet capture).
* Validate UDRs and confirm correct subnet associations.
* Check for asymmetric routing and enforce symmetric return paths where required.
* Confirm NVAs, gateways, and load balancers are healthy and reachable.

Following these steps methodically will help you diagnose and resolve most Azure routing problems. In practice, issues usually boil down to a missing, misconfigured, or conflicting route — or to a required device being offline. Verify each layer from VM to route table to appliance and you’ll typically find the root cause quickly.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3289c34c-80e6-417c-af60-54cbbcee3f01/lesson/fe507c3e-88fb-4dd0-84f9-fb573ef72042)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-Virtual-Network-Traffic-Routing/Introduction/page

Guide to Azure virtual network routing, covering built-in routes, user defined routes, forced tunneling, BGP, network virtual appliances, and troubleshooting with Network Watcher

Implementing virtual network traffic routing in Azure

In this lesson we'll break down how network traffic is routed inside Azure so you can control, understand, and optimize communication between resources—both within a virtual network (VNet) and to/from external networks.

What you’ll gain from this lesson:

* When Azure’s built-in routing is sufficient vs. when you should customize routes.
* How to create and apply User Defined Routes (UDRs) to override system routes.
* Techniques to redirect outbound internet traffic (forced tunneling) to on-premises or security appliances.
* How dynamic routing (BGP) works with Azure and how to integrate Network Virtual Appliances (NVAs) for hybrid scenarios.
* Practical troubleshooting with Network Watcher, Effective Routes, and related tools to diagnose routing problems.

> **lightbulb** This lesson assumes a basic understanding of core Azure networking concepts such as VNets, subnets, NSGs, and peering.

We’ll start with Azure’s default routing behavior and built-in system routes, then progressively introduce customization, forced tunneling, dynamic routing with BGP, and troubleshooting techniques.

## Learning objectives (expanded)

* Understand Azure’s default (system) routes and how Azure determines next hops.
* Learn when automatic routes suffice and when to apply UDRs to control traffic flow.
* Configure forced tunneling to send outbound traffic to on-premises or third-party security stacks.
* Integrate BGP for dynamic routes across VPN/ExpressRoute and NVAs.
* Use Network Watcher, Effective Routes, and packet capture to validate and troubleshoot routing.

## Key routing concepts (at-a-glance)

| Concept                            | Purpose                                                                                       | When to use                                                                  |
| ---------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| System Routes (built-in)           | Automatically created routes by Azure for intra-VNet, peering, internet, and system next hops | Default for most deployments                                                 |
| User Defined Routes (UDRs)         | Custom route tables you associate with subnets to override system routes                      | When you must force traffic through NVAs, on-prem, or apply custom next-hops |
| Forced Tunneling                   | Route outbound internet-bound traffic to on-premises or security appliances                   | Centralized egress filtering, corporate compliance                           |
| BGP (dynamic routing)              | Exchange routes between Azure and on-premises or third-party routers                          | Large-scale/hybrid networks needing automatic route exchange                 |
| Network Virtual Appliance (NVA)    | Third-party or custom VM-based routers/firewalls in a VNet                                    | Advanced filtering, DPI, or traffic inspection requirements                  |
| Network Watcher / Effective Routes | Tools to inspect how Azure actually routes traffic and to diagnose issues                     | Essential for troubleshooting and validating route precedence                |

## When to customize routing

Consider custom routing (UDRs, NVAs, BGP) when you need to:

* Enforce centralized outbound inspection (e.g., route all internet egress through a firewall).
* Route traffic between VNets or on-prem through specific NVAs for inspection, transformation, or logging.
* Implement policy-based routing for segmentation, service chaining, or gateway-specific requirements.
* Integrate dynamic routes via BGP for high availability and automatic route propagation.

## Routing precedence and behavior

Azure determines routing based on precedence rules. In general:

1. User-defined routes (UDRs) have higher priority than system routes when a UDR is associated with a subnet.
2. More specific (longer prefix) routes are preferred.
3. If no matching route is found, Azure drops the packet.

Understanding precedence avoids common mistakes like accidentally creating blackholes or bypassing inspection appliances.

## Troubleshooting routing issues

Use these tools and techniques:

* Network Watcher → IP Flow Verify to validate reachability.
* Effective Routes for a VM’s network interface or subnet to see the applied routes and next hops.
* Connection Troubleshoot and packet capture (where permitted) to verify traffic flow.
* Review NSGs and Azure Firewall/NVA rules that may be blocking traffic even when routing is correct.

## Links and references

* [Azure Virtual Network routing overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview)
* [User-defined routes (UDR) in Azure](https://learn.microsoft.com/azure/virtual-network/udr-overview)
* [Azure BGP routing and ExpressRoute](https://learn.microsoft.com/azure/expressroute/expressroute-routing)
* [Network Watcher overview and tools](https://learn.microsoft.com/azure/network-watcher/network-watcher-monitoring-overview)

We’ll begin with Azure’s default routing behavior and built-in system routes.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3289c34c-80e6-417c-af60-54cbbcee3f01/lesson/459e7654-dde2-4630-b666-4010f8b2501f)
