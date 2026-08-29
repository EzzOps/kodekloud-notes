# ExpressRoute Connectivity Models

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-ExpressRoute/ExpressRoute-Connectivity-Models/page

Explains Azure ExpressRoute connectivity models, trade-offs, and scenarios for choosing cloud exchange, point to point, any to any MPLS, or ExpressRoute Direct for private enterprise connections

This article explains the primary connectivity models for Azure ExpressRoute, how they differ, and typical scenarios for choosing each. Use this as a quick reference when designing hybrid or cloud-first network architectures that require private, high-throughput, and predictable connectivity to Microsoft Azure.

## Overview

ExpressRoute provides private connectivity between your on-premises networks and Microsoft Azure. There are four common connectivity models:

* Cloud exchange co-location
* Point-to-point Ethernet
* Any-to-any (IP VPN / provider-managed MPLS)
* ExpressRoute Direct (direct connection into Microsoft’s backbone)

Each model has trade-offs in cost, control, bandwidth, latency, and operational complexity. Read the short model descriptions below and use the comparison table to match a model to your requirements.

## Service provider models

These models rely on an ExpressRoute connectivity provider to bridge your on-premises network to Azure.

### Cloud exchange co-location

In the cloud exchange co-location model, you colocate equipment in the same facility (an exchange or data-hub) as the ExpressRoute provider. You run a short physical cross-connect from your rack to the provider’s equipment, and the provider on-ramps you into Azure.

Example: Your company keeps critical systems in a London colocation facility that hosts an ExpressRoute provider. You establish a cross-connect from your rack to the provider’s port, and the provider carries the traffic to Microsoft Azure. This option is ideal for latency-sensitive workloads and organizations already colocated with providers (common in finance and HPC).

### Point-to-point Ethernet connection

Point-to-point Ethernet gives you a dedicated, private circuit from your datacenter to an ExpressRoute provider. Conceptually it’s a private cable (physical or logical) from your location to the provider, who then provides access to Azure.

Example: A hospital requiring strict compliance and predictable throughput contracts a telecom to run a dedicated link from its datacenter to the provider’s network. This model is simple, secure, and provides reliable performance—useful for regulated industries and critical systems.

### Any-to-any (IP VPN / provider-managed MPLS)

Any-to-any (commonly called IP VPN or provider MPLS) uses a provider-managed WAN to connect multiple branch offices and data centers to Azure. The provider extends connectivity from each site over their WAN and integrates it with ExpressRoute.

Example: A multinational retailer uses its WAN provider to connect dozens of stores and offices to Azure through a single ExpressRoute integration point, reducing the need for separate physical connections at each site and simplifying management.

## Direct model

ExpressRoute Direct lets you connect directly to Microsoft’s global network at an ExpressRoute Direct location without an intermediary provider. This is the highest-control option and can offer very high speeds (up to 100 Gbps) for demanding, latency-sensitive enterprises.

<Frame>
  <img alt="The image illustrates ExpressRoute connectivity models for Microsoft Azure, including service provider and direct models, with different connection types like cloud exchange, point-to-point Ethernet, and any-to-any (IPVPN)." />
</Frame>

Example: A global bank needing large bandwidth, full routing control, and the strictest security might provision a physical cross-connect at an ExpressRoute Direct site and obtain multi-10/100 Gbps connectivity into Microsoft’s backbone. ExpressRoute Direct is robust and performant but typically more expensive and operationally involved.

> **lightbulb** ExpressRoute Direct is preferred when you need maximum bandwidth and control (e.g., high-frequency trading, global backups, large-scale migrations). For many organizations, service-provider models offer a simpler, lower-cost path with sufficient performance.

## Comparison table

| Model                      |                                                                                         Description | Best for                                           | Example                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------: | -------------------------------------------------- | ------------------------------------------------------------------- |
| Cloud exchange co-location | Colocate equipment in a facility that hosts the ExpressRoute provider and use a short cross-connect | Low latency, colocated sites, finance/HPC          | `Rack in a London colo cross-connects to provider`                  |
| Point-to-point Ethernet    |                                              Dedicated private circuit from your site to a provider | Predictable performance, regulated environments    | `Dedicated line from hospital to provider`                          |
| Any-to-any (IP VPN / MPLS) |                                      Provider-managed WAN integrates multiple sites to ExpressRoute | Multi-site organizations with many branches        | `Retail chain connects stores through provider WAN`                 |
| ExpressRoute Direct        |                                Direct physical connection into Microsoft’s network (up to 100 Gbps) | Very high bandwidth, maximum control and isolation | `Global bank with direct cross-connect at ExpressRoute Direct site` |

## Choosing the right model

Consider these factors when selecting a model:

* Bandwidth needs: choose ExpressRoute Direct for multi-10/100 Gbps; provider models for lower throughput.
* Latency and performance predictability: colocation and direct connections typically minimize latency.
* Regulatory and compliance: dedicated circuits or direct connections often simplify proof-of-control and auditing.
* Operational overhead: provider-managed MPLS reduces hardware and per-site complexity for many branches.
* Cost: Direct connections and colocation typically cost more upfront and require more operational effort than provider-managed options.

> **warning** Consider contractual SLAs, carrier redundancy, and regulatory requirements before choosing a model. ExpressRoute costs and operational responsibilities vary widely between provider-managed setups and ExpressRoute Direct.

## Links and references

* Azure ExpressRoute documentation: [https://learn.microsoft.com/azure/expressroute](https://learn.microsoft.com/azure/expressroute)
* Designing Azure network connectivity: [https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/](https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/)
* ExpressRoute Direct overview: [https://learn.microsoft.com/azure/expressroute/expressroute-direct](https://learn.microsoft.com/azure/expressroute/expressroute-direct)

Now that you understand the connectivity models and trade-offs, map your performance, security, and operational requirements to the model that best fits your environment.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c1bf6def-e7d7-42de-8511-07397f2eaff9/lesson/30bc8bd7-9906-4c87-9be4-798622262188)
