# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/ExpressRoute-Advanced-Features/Introduction/page

Explains Azure ExpressRoute advanced features like Global Reach and FastPath to enable private multi-region connectivity, improve performance, and design resilient hybrid networks.

Advanced ExpressRoute capabilities for private, high-performance Azure networking

With the core ExpressRoute setup complete, you can extend connectivity with advanced features that optimize performance, improve resiliency, and enable private global networks. This article explains how to:

* Link multiple ExpressRoute circuits across regions
* Use ExpressRoute Global Reach to interconnect circuits and create private global connectivity
* Apply FastPath to improve traffic performance between on-premises networks and VNets
* Decide when cross-circuit connections are appropriate for your architecture

These capabilities are particularly relevant for multinational enterprises, regulatory or data-residency requirements, resiliency and business continuity, and for optimizing data paths for globally distributed or latency-sensitive applications.

<Frame>
  <img alt="The image outlines four learning objectives related to ExpressRoute, including linking circuits across regions, leveraging Global Reach, configuring circuits, and improving network performance with FastPath." />
</Frame>

FastPath is an optimization that lowers latency and increases throughput by allowing data packets to bypass the slower forwarding path inside the ExpressRoute virtual network gateway and travel on a more direct route over Azure's backbone. It benefits data-intensive workloads—such as SAP, database migrations, and analytics pipelines—where every millisecond and megabit helps improve application performance.

After reading this article you will understand when and how to apply Global Reach and FastPath to meet performance, resiliency, and operational requirements for your Azure connectivity.

<Callout icon="lightbulb">
  FastPath and Global Reach are complementary: Global Reach connects separate ExpressRoute circuits to create private end-to-end connectivity across regions, while FastPath optimizes the local traffic path between an ExpressRoute circuit and virtual machines inside a VNet.
</Callout>

## Why connect ExpressRoute circuits?

Linking circuits or enabling Global Reach makes sense in scenarios such as:

* Multinational or multi-region deployments that require a private backbone between offices and Azure
* Data residency or compliance where traffic must remain on private links and not traverse the public internet
* Resiliency and high availability through diverse physical paths and cross-region redundancy
* Performance optimization for globally distributed applications that benefit from shorter, predictable network paths
* Consolidated hybrid network architectures for cost and operational simplicity

## High-level overview: ExpressRoute Global Reach

ExpressRoute Global Reach enables private connectivity between two or more ExpressRoute circuits. By bridging circuits over the Azure backbone you can create a private, Microsoft-managed WAN connecting on-premises sites in different regions without traversing the internet.

Key points:

* Global Reach links circuits at the ExpressRoute gateway level to form private paths between customer sites.
* Traffic between linked circuits remains on Microsoft's backbone; it does not traverse the public internet.
* Useful for creating private global topologies (hub-and-spoke, full mesh) across regions or service providers.

High-level steps to enable Global Reach:

1. Ensure each ExpressRoute circuit is provisioned and approved.
2. Configure peering and authorize the circuits for Global Reach in the Azure portal (or via ARM/PowerShell/CLI).
3. Map the desired connectivity: which circuits and on-prem subnets should be reachable across the private backbone.
4. Validate routing and BGP advertisements to ensure correct paths.

## FastPath: accelerate VNet-to-ExpressRoute traffic

FastPath reduces latency and increases throughput by bypassing the gateway's general-purpose packet forwarding plane and using a streamlined path for data-plane traffic between the ExpressRoute circuit and VM NICs in the VNet.

When to enable FastPath:

* High-throughput, low-latency application requirements (e.g., SAP, database replication, large-scale migrations)
* Large east–west data transfers where gateway forwarding introduces measurable latency or throughput limits

Considerations:

* FastPath applies to traffic between ExpressRoute and virtual machines in the same VNet or peered VNets (depending on gateway and peering configuration).
* Not all gateway SKUs or configurations support FastPath—validate SKU compatibility and required gateway features before enabling.
* FastPath optimizes data-plane forwarding; control-plane and BGP remain unchanged.

## Feature comparison

| Feature                   | Purpose                                                    | When to use                                                               |
| ------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| ExpressRoute circuit      | Private connection from on-premises to Azure               | Basic hybrid connectivity for a single site or region                     |
| ExpressRoute Global Reach | Connect multiple ExpressRoute circuits over Azure backbone | Private, multi-region WAN between on-premises sites and regions           |
| FastPath                  | Optimize data path between ExpressRoute and VMs            | Latency-sensitive or high-throughput workloads (e.g., SAP, DB migrations) |

## Key design considerations

* Routing and BGP: Plan BGP communities, prefixes, and route priorities to avoid asymmetric routing or unexpected path selection.
* Security and compliance: Ensure private paths meet regulatory controls and logging/auditing requirements.
* Resiliency: Use diverse physical connections and multiple circuits/locations to avoid single points of failure.
* Cost and operational overhead: Global Reach reduces internet transit but may add circuit and configuration complexity—balance cost against the benefits.
* Gateway SKUs: Verify gateway SKU compatibility for Global Reach and FastPath and scale gateway resources for expected throughput.

## Links and references

* [Azure ExpressRoute documentation](https://learn.microsoft.com/azure/expressroute/)
* [ExpressRoute Global Reach overview](https://learn.microsoft.com/azure/expressroute/expressroute-global-reach)
* [ExpressRoute FastPath overview](https://learn.microsoft.com/azure/expressroute/expressroute-fastpath)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/580264b2-4667-4ffc-a0f8-6d6592e1560e/lesson/b2c477a8-ee63-4bd9-b129-3031eeeebc75" />
</CardGroup>
