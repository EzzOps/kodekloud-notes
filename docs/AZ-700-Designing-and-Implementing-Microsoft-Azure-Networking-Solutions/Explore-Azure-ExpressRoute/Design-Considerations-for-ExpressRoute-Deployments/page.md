# Design Considerations for ExpressRoute Deployments

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-ExpressRoute/Design-Considerations-for-ExpressRoute-Deployments/page

Designing Azure ExpressRoute deployments covering gateway and circuit selection, peering and routing, redundancy and high availability, connection models, and BFD for rapid failure detection

Azure ExpressRoute is a private, dedicated connection between your on-premises networks and Microsoft Azure. When designing an ExpressRoute deployment, prioritize capacity, resiliency, routing, and operational model to meet business SLAs. This guide walks through the key design choices in order, helping you build a scalable, highly available, and cost-effective ExpressRoute architecture.

Start by selecting the ExpressRoute Gateway SKU. Choose a gateway SKU based on expected throughput, whether you require [Availability Zones](https://learn.microsoft.com/azure/availability-zones/) for resilience, and how many connections you plan to support. Consider SKU limits (throughput, route scale) and zone support when making this choice.

<Frame>
  <img alt="The image is a diagram outlining Azure ExpressRoute design considerations, focusing on gateway SKU selection with aspects like circuit SKU and bandwidth, routing configuration, redundancy and high availability, and connection model choice." />
</Frame>

Larger environments or critical applications often require higher gateway SKUs to support greater bandwidth and advanced features. Decide between a metered or unlimited data plan and select the appropriate circuit bandwidth—ExpressRoute circuits range from 50 Mbps up to 100 Gbps. Typical scenarios:

* Small-to-medium businesses: start with lower bandwidth (for example, 200 Mbps) and plan for scale.
* Enterprises / heavy-data workloads: choose higher-capacity circuits and higher gateway SKUs to meet throughput and SLA needs.

<Frame>
  <img alt="The image is a design considerations chart for Azure ExpressRoute, focusing on gateway SKU selection, circuit SKU and bandwidth, routing configuration, redundancy and high availability, and connection model choice. It highlights throughput, availability zones, and connection scale for ExpressRoute Gateway SKUs." />
</Frame>

Circuit SKU and bandwidth are central to capacity planning. Match your chosen gateway SKU with the circuit bandwidth to satisfy throughput, growth, and SLA requirements. Consider burst requirements, typical utilization, and headroom for future growth.

<Frame>
  <img alt="The image outlines design considerations for Azure ExpressRoute, highlighting areas like Circuit SKU and Bandwidth. It includes options for data plans, required bandwidth ranging from 50 MBPS to 100 GBPS, and other configuration choices." />
</Frame>

Routing configuration: plan which peering option(s) you need and how traffic will flow across ExpressRoute. The main peering types are:

* Private peering — for connectivity to Azure Virtual Networks and private Azure services. See: [Private peering](https://learn.microsoft.com/azure/expressroute/expressroute-peering)
* Microsoft peering — for connectivity to Microsoft public services (for example, Microsoft 365 and some Azure PaaS services) that require public IP connectivity. See: [Microsoft peering](https://learn.microsoft.com/azure/expressroute/expressroute-peering)

Decide whether you need private peering, Microsoft peering, or both based on workloads, compliance, and traffic patterns. Also define route filters and prefix advertisement policies to control which routes are exchanged.

<Frame>
  <img alt="The image outlines design considerations for Azure ExpressRoute, highlighting aspects like gateway SKU selection, routing configuration, and peering options. The highlighted item is &#x22;Routing Configuration.&#x22;" />
</Frame>

Redundancy and high availability are essential. Plan for physical path diversity, redundant provider connectivity, and resilient on-premises design:

* Use dual connections from your site to Microsoft via diverse path providers or diverse provider edges.
* Deploy redundant ExpressRoute Gateways in different [Availability Zones](https://learn.microsoft.com/azure/availability-zones/) where supported by the chosen SKU for zone-level isolation.
* Ensure redundant on-prem routers and links to avoid single points of failure.
* Consider multi-site topologies and failover testing to validate your operational recovery objectives.

<Frame>
  <img alt="The image displays a slide titled &#x22;Azure ExpressRoute – Design Considerations,&#x22; listing factors like gateway SKU selection, circuit SKU and bandwidth, routing configuration, redundancy and high availability, and connection model choice. It focuses on the highlighted item &#x22;Redundancy and High Availability.&#x22;" />
</Frame>

Connection model choice: select the connection model that best fits your organization—options include co-location (via an exchange provider), point-to-point Ethernet, IP VPN, or [ExpressRoute Direct](https://learn.microsoft.com/azure/expressroute/expressroute-direct). Evaluate:

* Site locations and proximity to exchange points
* Available service providers and lead times
* Required capacities (current and future)
* Operational responsibilities (who manages physical cross-connects, monitoring, and troubleshooting)

Bringing these elements together—SKU, circuit, peering, redundancy, and connection model—lets you design a resilient, high-performing ExpressRoute deployment that aligns with your business requirements.

<Callout icon="lightbulb">
  When designing ExpressRoute, align gateway SKU, circuit bandwidth, peering types, and redundancy to meet your application's availability, throughput, and security goals. Validate failover scenarios and confirm provider diversity during planning and testing.
</Callout>

BFD — Bidirectional Forwarding Detection (BFD)

Bidirectional Forwarding Detection (BFD) is a lightweight protocol that accelerates failure detection on forwarding paths between peers. Implementing BFD with ExpressRoute reduces detection times compared to routing-protocol timers alone, improving failover speed and reducing service interruption.

* BFD typically reduces failure detection from multiple seconds to under one second, enabling faster failover for critical workloads.
* BFD is supported on ExpressRoute private peering and enabled on Microsoft's edge routers by default. Your on-premises routers must support and be configured for BFD to gain full benefit.

To maximize reliability:

* Enable and configure BFD on each on-prem edge router participating in ExpressRoute private peering.
* Associate BFD sessions with the BGP adjacency so BFD events trigger immediate BGP reactions.
* Test primary and backup paths and tune BFD timers to meet your recovery time objectives.

<Frame>
  <img alt="The image illustrates Bidirectional Forwarding Detection (BFD) with ExpressRoute Peering, comparing failure detection times with and without BFD and explaining configuration steps on Microsoft and partner/customer edges." />
</Frame>

<Callout icon="lightbulb">
  BFD is enabled by default on Microsoft's edge routers, but you must configure it on your on-premises equipment. Proper BFD configuration and testing is a best practice for mission-critical workloads that require minimal failover time.
</Callout>

Summary checklist

| Design Factor           | Key Questions                                            | Recommendation                                                                     |
| ----------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Gateway SKU             | What throughput and zone resiliency do you need?         | Choose SKU based on throughput, route scale, and zone support.                     |
| Circuit SKU & Bandwidth | What are current and projected bandwidth needs?          | Pick bandwidth with headroom; consider metered vs unlimited plans.                 |
| Peering Types           | Do you need private, Microsoft, or both peerings?        | Map peering to workloads (VNet vs public Microsoft services).                      |
| Redundancy              | Are there diverse physical paths and multiple providers? | Use dual/provider-diverse connections and zonal gateway redundancy.                |
| Connection Model        | Which provisioning model suits locations and providers?  | Select co-location, point-to-point, IP VPN, or ExpressRoute Direct as appropriate. |
| BFD & BGP               | How fast must failures be detected and rerouted?         | Enable BFD on on-prem routers and tie it to BGP for sub-second failover.           |

Links and references

* [Azure ExpressRoute peering](https://learn.microsoft.com/azure/expressroute/expressroute-peering)
* [ExpressRoute Direct](https://learn.microsoft.com/azure/expressroute/expressroute-direct)
* [Availability Zones](https://learn.microsoft.com/azure/availability-zones/)
* BFD: RFC 5880 — [https://datatracker.ietf.org/doc/html/rfc5880](https://datatracker.ietf.org/doc/html/rfc5880)
* BGP: RFC 4271 — [https://datatracker.ietf.org/doc/html/rfc4271](https://datatracker.ietf.org/doc/html/rfc4271)

By following these considerations—selecting the right gateway and circuit combinations, planning peering and redundancy, and implementing BFD for fast failure detection—you can build a robust ExpressRoute deployment ready for enterprise production workloads.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c1bf6def-e7d7-42de-8511-07397f2eaff9/lesson/45f22903-788f-4bdd-befa-f58f1d570ed6" />
</CardGroup>
