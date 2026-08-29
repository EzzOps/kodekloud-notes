# Choose the Right ExpressRoute Circuit and Billing Model

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-an-ExpressRoute-deployment/Choose-the-Right-ExpressRoute-Circuit-and-Billing-Model/page

Guide to selecting Azure ExpressRoute circuits, billing models, bandwidth, resiliency, and SKUs with pricing considerations and portal configuration steps for reliable private connectivity between on-premises and Azure

Choosing the correct ExpressRoute circuit, billing model, and supporting options (bandwidth, resiliency, SKU) is a key design decision. The right combination ensures predictable costs, sufficient throughput, and the regional or global connectivity your workloads require. This guide breaks down the selection process and highlights practical configuration steps in the Azure portal.

## Quick overview

* Billing model: Metered vs Unlimited — choose based on expected egress volume.
* Bandwidth: Provision for current needs and anticipated growth; ExpressRoute Direct supports very large capacities.
* Resiliency: Multiple peering locations and circuits reduce risk of outage.
* SKU: Standard vs Premium — Premium required for global connectivity and higher route limits.
* Physical connectivity: Your connectivity provider provisions the handoff to Microsoft Edge routers.

## Billing models: Metered vs Unlimited

* Unlimited Data: Fixed monthly fee covering all data transfer across the ExpressRoute connection. Best for sustained, high-volume traffic between Azure and on-premises.
* Metered Data: Lower monthly base charge with outbound (egress from Azure to on-premises) billed per GB. Suitable for small sites or scenarios with minimal outbound traffic.

| Billing Model  |                 Best for | Pros                                          | Cons                                       |
| -------------- | -----------------------: | --------------------------------------------- | ------------------------------------------ |
| Unlimited Data | High, predictable egress | Predictable monthly cost; no per-GB surprises | Higher base cost for low-volume use        |
| Metered Data   |     Low outbound traffic | Lower base cost                               | Egress charges can add up with heavy usage |

> **lightbulb** If you expect minimal outbound traffic, choose the metered plan to save on monthly fees. For steady, high-volume transfers, Unlimited keeps costs predictable and avoids unpredictable egress costs.

## Bandwidth selection and capacity planning

* Start with the capacity you need today and factor in 12–24 month growth estimates.
* ExpressRoute circuits commonly start at 50 Mbps and scale up; ExpressRoute Direct supports very large port speeds (10 Gbps, 100 Gbps options depending on provider).
* Provisioning too small risks congestion; provisioning too large wastes budget. When in doubt, size conservatively and plan for scale-up.

## Scalability and gateway considerations

* You can often increase ExpressRoute circuit bandwidth without network downtime, but this may require coordination with your connectivity provider and the exchange.
* Changing the virtual network gateway SKU (or performing a downgrade) can require redeploying or recreating the gateway and may cause a brief outage.

> **warning** Scaling down a gateway or changing its SKU can cause a brief outage. Schedule maintenance windows for downgrades and any action that requires gateway redeployment.

<Frame>
  <img alt="The image is about choosing the right ExpressRoute circuit and billing model, highlighting aspects such as billing options, bandwidth selection, scalability, pricing factors, and premium add-ons. It includes an icon of a lock with directional arrows and a note about gateway size adjustments." />
</Frame>

## Pricing factors to review

Pricing varies by region, resiliency, and billing model. Key variables that influence monthly cost:

* Billing model (metered vs unlimited)
* Port speed (bandwidth)
* Region / peering location
* Resiliency and availability options
* Premium SKU (adds charge when used)

Always validate current pricing in the Azure Pricing Calculator: [https://azure.microsoft.com/en-us/pricing/calculator/](https://azure.microsoft.com/en-us/pricing/calculator/)

<Frame>
  <img alt="The image is about choosing the right ExpressRoute circuit and billing model, featuring a list of factors such as billing options, bandwidth selection, scalability, pricing factors, and a premium add-on against a map with location markers." />
</Frame>

## When to choose the Premium SKU

Choose Premium when you need:

* Global connectivity across multiple Azure regions (connectivity beyond the local region).
* Higher route limits and larger scale than the Standard SKU provides.

Premium expands route counts and region reach, making it the correct choice for multi-region architectures and large enterprise networks.

<Frame>
  <img alt="The image is a diagram outlining factors for choosing the right ExpressRoute circuit and billing model, including options like billing, bandwidth, scalability, pricing, and a premium add-on. It highlights &#x22;Global Connectivity&#x22; on the right side." />
</Frame>

## Portal walkthrough — where to create ExpressRoute resources

In the Azure portal you work with two main resource types for an ExpressRoute deployment:

1. Virtual Network Gateway — this is the gateway resource (same family used by VPN gateway) where the ExpressRoute circuit terminates. When creating it:
   * Create it in the same region as the virtual network it will serve.
   * Choose gateway type: ExpressRoute.
   * Select gateway SKU appropriate for throughput and features (Standard, HighPerformance, UltraPerformance, or GW1/GW2/GW3).
2. ExpressRoute Circuit — this resource holds circuit metadata:
   * Select subscription and resource group.
   * Choose port speed, peering location, provider (or ExpressRoute Direct), resiliency, billing model, and SKU (Standard vs Premium).

Recommended links:

* ExpressRoute overview: [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction)
* Virtual network gateway: [https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-gateway](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-gateway)

<Frame>
  <img alt="The image shows the Microsoft Azure portal dashboard, displaying various Azure services icons and a list of resources with their types and last viewed dates." />
</Frame>

## Creating the virtual network gateway (key steps)

* Ensure the gateway is in the same region as the VNet.
* Select gateway type = ExpressRoute.
* Choose the correct gateway SKU for the required throughput and features.
* The ExpressRoute circuit will terminate on this gateway to provide connectivity to VNets.

## Creating the ExpressRoute circuit (key steps and resiliency options)

* Set subscription and resource group.
* Choose peering location and provider (or ExpressRoute Direct).
* Select port/bandwidth and billing model.
* Decide resiliency level:
  * Maximum resiliency: two circuits across two different locations (strongest protection).
  * High resiliency: two peering locations for greater availability.
  * Standard resiliency: two links within a single peering location.

<Frame>
  <img alt="The image shows a Microsoft Azure interface for creating an ExpressRoute. It includes options for selecting a subscription, resource group, and resiliency settings." />
</Frame>

## Provider involvement and the physical handoff

* After provisioning the ExpressRoute circuit resource, your connectivity provider provisions the physical layer from your site to the provider edge.
* The provider installs the physical circuit to the selected peering location and hands off to Microsoft Edge routers.
* Microsoft connects the Edge routers to your ExpressRoute gateway in Azure, which becomes the termination point for your circuit and enables connectivity to configured VNets.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for creating an ExpressRoute, with a diagram illustrating two ExpressRoute circuits connecting an on-premises network to Microsoft Enterprise Edges." />
</Frame>

## Decision checklist

* Estimate monthly egress volume → choose Metered or Unlimited.
* Select initial port speed and plan for growth (document expected ramp).
* Decide if you need Premium for global reach or higher route counts.
* Choose resiliency level based on SLA and budget.
* Coordinate with connectivity provider for the physical installation and peering location.
* Validate costs in the Azure Pricing Calculator.

Resources and further reading:

* Azure ExpressRoute documentation: [https://learn.microsoft.com/en-us/azure/expressroute/](https://learn.microsoft.com/en-us/azure/expressroute/)
* Azure Pricing Calculator: [https://azure.microsoft.com/en-us/pricing/calculator/](https://azure.microsoft.com/en-us/pricing/calculator/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/8f99eebf-f145-491c-be3f-007ba6971986/lesson/93959f95-c7b8-4aaa-b37e-2a507215ef1c)
