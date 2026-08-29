# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-ExpressRoute/Introduction/page

Overview of Azure ExpressRoute private connectivity, design considerations, peering types, redundancy, BFD failover, and security options for planning enterprise-grade network connections to Azure

Welcome. This lesson explains Azure ExpressRoute — Microsoft Azure’s private, high-throughput connectivity option for linking on-premises networks (or colocation facilities) directly to Azure datacenters. ExpressRoute delivers predictable performance, private routing (BGP-based), and SLA-backed availability, and is commonly used where security, compliance, or performance requirements make the public internet unsuitable.

> **warning** This module does not include a live lab. ExpressRoute deployments typically involve carrier or connectivity partners and physical cross‑connects, which can incur significant lead time and cost. Use the diagrams and configuration snippets here to plan real deployments with your networking team and your chosen service provider.

> **lightbulb** This lesson focuses on conceptual design, operational considerations, and example configurations for Azure ExpressRoute. Treat the diagrams and snippets as planning references—validate all production designs with your network provider and Azure support teams.

Learning objectives for this module

* Understand ExpressRoute’s value: private/global connectivity, predictable performance, and SLA guarantees.
* Identify when ExpressRoute is preferred over Internet VPNs — e.g., strict security, compliance, or high throughput needs.
* Learn peering types (private peering, Microsoft peering) and how each influences routing, IP addressing, and network design.
* Plan for capacity, redundancy, and vendor engagement with connectivity providers.
* Learn how BFD (Bidirectional Forwarding Detection) reduces failover detection time and improves resiliency.
* Review encryption and data confidentiality options for provider links (for example, MACsec on metro/physical links where supported).

<Frame>
  <img alt="The image outlines four learning objectives related to ExpressRoute, highlighting its global connectivity benefits, reasons for use, connection methods, and planning considerations." />
</Frame>

Throughout this article we’ll describe core ExpressRoute concepts, typical deployment patterns, and configuration examples you can adapt. Because ExpressRoute spans cloud and physical provider networks, the content emphasizes design decisions and operational considerations rather than step‑by‑step lab exercises.

Key topics covered

| Topic                                   | Why it matters                                                      | Example / Outcome                                                                                            |
| --------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| ExpressRoute circuit models & providers | Guides procurement and circuit attachment choices                   | Choose between co-located metro, exchange-based, or provider-managed models                                  |
| Peering types and routing implications  | Determines how Azure services and customer networks exchange routes | Private peering for VNet connectivity; Microsoft peering for platform services (subject to routing policies) |
| Redundancy & high-availability patterns | Ensures resilient connectivity and SLA alignment                    | Dual circuits, diverse physical paths, and active/active routing                                             |
| BFD for faster failover detection       | Lowers convergence time during link/device faults                   | BFD complements BGP to detect failures in sub-second intervals                                               |
| Traffic security across provider links  | Addresses data confidentiality across the metro/provider network    | MACsec on physical links where supported; application-layer encryption otherwise                             |

<Frame>
  <img alt="The image outlines learning objectives related to improving failover detection with BFD and securing ExpressRoute using MACsec encryption technologies." />
</Frame>

What follows in this guide

* Conceptual diagrams that show common topologies (single-circuit, dual-circuit, exchange-based peering).
* Routing and peering comparisons (BGP attributes, prefix advertisement limits, and advertisement scopes).
* High-availability patterns (redundant circuits, diverse physical routes, and co‑located recovery).
* Operational topics: monitoring, BFD deployment, MACsec applicability, and engagement with connectivity providers.
* Practical configuration snippets for BGP/BFD and example verification steps to validate route propagation and failover behavior.

Links and references

* [Azure ExpressRoute overview](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
* [ExpressRoute circuit and peering documentation](https://learn.microsoft.com/azure/expressroute/expressroute-peering-overview)
* [BFD overview (RFC)](https://datatracker.ietf.org/doc/html/rfc5880)
* [MACsec technology overview](https://www.ieee.org/conferences_events/conferences/sas/index.html) (vendor and provider support varies — consult your connectivity provider)

Use the diagrams and examples in this lesson as a foundation for planning and validating an ExpressRoute deployment in collaboration with your network operations and connectivity provider teams.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c1bf6def-e7d7-42de-8511-07397f2eaff9/lesson/0a6209a8-8a79-41c5-b843-dc991f1335cb)
