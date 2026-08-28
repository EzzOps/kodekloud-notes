# ExpressRoute SKUs

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-an-ExpressRoute-deployment/ExpressRoute-SKUs/page

Guide to Azure ExpressRoute SKUs, explaining circuit types, port models, billing options, geographic reach, routing limits, and choosing appropriate circuit and gateway SKUs for deployments

In this lesson we explain Azure ExpressRoute SKUs: what they are, why they matter, and how to choose the right one for your deployment.

## What is an ExpressRoute circuit?

An ExpressRoute circuit is a dedicated private network connection between your on‑premises environment and Microsoft Azure. It bypasses the public Internet to provide improved security, predictable latency, and higher reliability. When you provision a circuit, you establish private connectivity between your edge routers and Microsoft’s edge infrastructure.

## Port types and connection models

When creating an ExpressRoute circuit you first choose a port type and a connection model:

* Provider model — The most common approach. You connect through a Microsoft‑approved service provider (an ExpressRoute partner) that provisions and manages the physical connectivity between your location and Microsoft’s network.
* ExpressRoute Direct — You connect directly to Microsoft’s edge locations (often via a colocation facility). This model is used when you need very high bandwidth and direct control over the physical handoff.

If you select the provider model, pick a service provider from Microsoft’s list of partners. If you use Direct, you effectively act as your own provider for the physical handoff.

## Circuit SKU overview

Circuit SKUs control geographic reach and routing limits for the physical connection. Choose the SKU that matches your reach and scale requirements.

| SKU      | Geographic reach                                                                                                            | Typical use case                                                                           |
| -------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Local    | Connectivity limited to Azure regions within the same metropolitan area or metro region (local peering)                     | Small or local deployments that do not require cross-region reach                          |
| Standard | Access to all Azure regions within a geopolitical boundary or “market” (for example, all of Europe or all of North America) | Enterprises with workloads distributed across a single geography                           |
| Premium  | Global connectivity to Azure regions worldwide; higher route limits and larger numbers of VNet connections                  | Large, global, or very high-scale hybrid environments requiring many routes and VNet links |

<Frame>
  <img alt="The image shows a configuration screen for selecting ExpressRoute SKUs in Azure, with options for port type, SKU type, billing model, and more. The premium SKU is highlighted, indicating support for over 4,000 routes and more than 10 virtual networks, enabling global connectivity." />
</Frame>

## Billing model

When provisioning a circuit you’ll also choose a billing model:

* Metered — You are billed for data that traverses the ExpressRoute circuit. Often lower base cost; suitable when traffic is variable and egress patterns are predictable.
* Unlimited — Fixed monthly price covering an agreed data volume; useful when you expect consistent high-volume traffic.

Select the billing model based on traffic patterns and cost predictability requirements.

## Circuit SKU vs Gateway SKU

It’s important to distinguish between the circuit SKU and the gateway SKU:

| Resource                                              | What it represents                                                                     | What it controls                                                                  |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| ExpressRoute circuit SKU (Local / Standard / Premium) | The physical/private link and its reach                                                | Geographic reach, route limits, and circuit-level capabilities                    |
| Gateway SKU (e.g., ErGw1/ErGw2, VpnGw1/VpnGw2)        | An Azure resource deployed in a virtual network to terminate connectivity to a circuit | Gateway throughput, features, and performance for connecting VNets to the circuit |

<Callout icon="lightbulb">
  Remember: an ExpressRoute "circuit" is the physical/private connection to Microsoft, and the "gateway" is an Azure resource that connects your VNets to that circuit. Circuit SKUs control reach and route limits; gateway SKUs control gateway throughput and features.
</Callout>

## Choosing the right SKU — practical guidance

* Start with your geographic reach:
  * Local if all workloads are within a single metro.
  * Standard if you need access across a single geopolitical market.
  * Premium if you need global Azure region reach.
* Consider scale (route count and number of VNets):
  * Larger hybrid networks and many VNets typically require Premium.
* Factor in throughput and features:
  * Circuit SKUs don’t change gateway throughput — size your gateway SKU separately.
* Review cost model:
  * If traffic volume is predictable and high, consider Unlimited billing.
  * If traffic is sporadic, Metered may be more cost-effective.

## Quick checklist

* Decide port/connection model: Provider vs ExpressRoute Direct.
* Select the circuit SKU (Local, Standard, Premium) based on reach and route/VNet needs.
* Choose the billing model (metered vs unlimited) aligned to traffic patterns.
* Deploy and size the appropriate gateway SKU for VNet connectivity and throughput.

## Links and references

* [Azure ExpressRoute documentation](https://learn.microsoft.com/azure/expressroute)
* [ExpressRoute Direct overview](https://learn.microsoft.com/azure/expressroute/expressroute-direct)
* [Azure VPN and ExpressRoute gateway SKUs](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpngateways)

This guidance will help you design ExpressRoute deployments that meet both connectivity and scale requirements for secure, predictable hybrid networking.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/8f99eebf-f145-491c-be3f-007ba6971986/lesson/8b52b41c-744b-461f-97ff-3f24091ad6bc" />
</CardGroup>
