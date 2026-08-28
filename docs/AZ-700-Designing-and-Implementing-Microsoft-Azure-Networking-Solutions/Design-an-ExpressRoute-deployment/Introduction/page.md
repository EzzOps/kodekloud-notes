# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-an-ExpressRoute-deployment/Introduction/page

Guide to designing Azure ExpressRoute deployments, choosing service tiers, peering locations, circuit billing and bandwidth to optimize latency, reach, redundancy, cost, and routing.

Welcome to this lesson on designing an Azure ExpressRoute deployment.

This guide helps you plan and choose the right ExpressRoute configuration for reliable, high-performance private connectivity between your on‑premises networks and Azure. It focuses on three core design decisions:

* Understand the ExpressRoute service tiers — Local, Standard, and Premium — and how their reach and capabilities differ. Choosing the correct tier ensures your circuit can reach the required Microsoft peering prefixes and services.
* Choose the best peering location. Selecting an appropriate peering location minimizes latency and improves application performance by placing connectivity closer to your workloads or users.
* Select the right circuit type and billing model. ExpressRoute supports both metered and unlimited data plans and a range of bandwidth options; picking the correct combination balances cost and capacity for your traffic patterns.

Throughout this lesson you will learn what each option means, when to prefer one over another, and the key design considerations to match ExpressRoute choices to your network and compliance requirements.

<Callout icon="lightbulb">
  Use this guide to align ExpressRoute selections with application requirements (latency, throughput, regional reach) rather than defaulting to the largest or cheapest option. Early design decisions significantly affect cost and connectivity options.
</Callout>

## 1. ExpressRoute service tiers — Local, Standard, Premium

Choosing the right service tier determines which Azure regions and Microsoft peering prefixes your circuit can access. Below is a compact comparison to help you evaluate reach and common use cases.

| Tier     | Regional reach                             | Microsoft peering reach                           | Typical use case                                                      | Notes                                                                                     |
| -------- | ------------------------------------------ | ------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Local    | Single metro/region                        | Limited to the local region                       | Traffic confined to one region, lower cost                            | Ideal when workloads and users are co-located                                             |
| Standard | Regional (multiple metros within a region) | Access to Microsoft public services in the region | Regional deployments requiring connectivity across a single geography | Most common mid-tier choice                                                               |
| Premium  | Global                                     | Broad reach to Microsoft prefixes across regions  | Global deployments with multi-region services and peering needs       | Required if you need connectivity to many global Microsoft services or extra route limits |

When to choose each tier:

* Local: low-latency single-region needs and cost optimization.
* Standard: regional redundancy and broader service access.
* Premium: multi-region or global Microsoft peering reach and larger route limits.

<Callout icon="warning">
  Selecting the wrong tier can limit reachable services and prefixes. Upgrading/downgrading tiers may require provisioning a new circuit or involve additional configuration — plan accordingly.
</Callout>

## 2. Choosing the best peering location

Peering location choice impacts latency, cost, and resiliency. Pick locations that minimize hops between your users/workloads and Azure, and that provide the required physical connectivity (e.g., your colocation provider has presence there).

Key factors to evaluate:

* Latency: choose the closest available ExpressRoute peering location to your primary workloads or user population.
* Physical connectivity options: ensure your provider supports cross-connects or partner circuits at the chosen location.
* Redundancy: prefer multiple peering locations across different metros for failover and reduced maintenance windows.
* Cost & transit: transit pricing and cross-connect fees can vary by location.

Consider this quick decision checklist:

1. Map workload locations and Azure region requirements.
2. Identify available ExpressRoute peering locations that serve those regions.
3. Validate provider presence and pricing at each peering location.
4. Design for redundancy: at least two peering locations for production-critical services.

## 3. Circuit types and billing models

ExpressRoute offers different billing and bandwidth options. Understanding metered vs unlimited and available bandwidth sizes helps you balance cost and capacity.

| Billing model | How it charges                                          | Best for                                         | Considerations                                                  |
| ------------- | ------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| Metered       | You pay for outbound data transfer (ingress often free) | Low average monthly egress, unpredictable bursts | Good when traffic is small or highly variable                   |
| Unlimited     | Fixed monthly fee for unlimited data                    | High or predictable high-volume traffic          | Better for heavy and stable data loads despite higher base cost |

Bandwidth and sizing:

* ExpressRoute circuits come in multiple bandwidths (for example 50 Mbps, 100 Mbps, 1 Gbps, 10 Gbps — confirm current SKUs with your provider).
* Choose a bandwidth that supports peak application demand plus headroom for growth and failover events.

Billing decision tips:

* Estimate monthly egress volumes and compare cost of metered vs unlimited.
* For bursty workloads with low average traffic, metered may be cheaper.
* For consistent high-volume replication or data transfer, unlimited can be more cost-effective.

## 4. Design checklist and decision flow

Use this step-by-step flow when planning an ExpressRoute deployment:

1. Inventory requirements
   * Which Azure regions and services must be reachable?
   * Expected monthly egress/ingress volumes and peak throughput.
   * Latency and jitter tolerances for key applications.
2. Select tier
   * If you require global Microsoft peering or higher route limits -> Premium.
   * For most region-bound needs -> Standard.
   * For single-metro, cost-sensitive needs -> Local.
3. Choose peering locations
   * Prioritize lowest-latency locations that your connectivity provider supports.
   * Design for at least two peering locations for production.
4. Choose circuit bandwidth and billing
   * Model costs for metered vs unlimited based on traffic estimates.
   * Select bandwidth to handle peak and failover scenarios.
5. Plan routing and security
   * Decide peering types to use (Private, Microsoft/Service peering).
   * Plan BGP communities, route filters, and prefix advertisement policy.
6. Validate operational readiness
   * Confirm provider SLAs, monitoring, and support options.
   * Test failover scenarios and measure latency after provisioning.

Example decision:

* Global data replication between regions + multiple Microsoft services required -> Premium tier, two peering locations in distinct metros, unlimited plan with 1 Gbps circuit (or higher) based on measured throughput.

## 5. Additional design considerations

* BGP and route limits: confirm route counts for your chosen tier (Premium often provides higher route limits).
* Security: control prefix advertisement and use route filters for Microsoft peering.
* Redundancy: use dual circuits across diverse metros and multiple service providers if possible.
* Compliance and data sovereignty: ensure regional reach aligns with data residency requirements.
* Monitoring and observability: enable network monitoring and collect baseline latency/throughput metrics.

## Links and references

* [Azure ExpressRoute overview](https://learn.microsoft.com/azure/expressroute/)
* [ExpressRoute FAQ and pricing](https://azure.microsoft.com/pricing/details/expressroute/)
* [Microsoft peering overview and routing](https://learn.microsoft.com/azure/expressroute/expressroute-routing)

Use these resources to verify current SKU names, bandwidth options, pricing, and any recent changes to peering models or route limits.

<Callout icon="lightbulb">
  Checklist for a quick review: Confirm required region reach, pick a tier that covers those regions, choose lowest-latency peering locations available through your provider, and evaluate metered vs unlimited based on projected egress.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/8f99eebf-f145-491c-be3f-007ba6971986/lesson/aa2d172c-6606-454c-b174-5431357b52fa" />
</CardGroup>
