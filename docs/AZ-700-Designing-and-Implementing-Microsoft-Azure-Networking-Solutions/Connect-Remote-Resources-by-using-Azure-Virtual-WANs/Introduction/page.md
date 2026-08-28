# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Remote-Resources-by-using-Azure-Virtual-WANs/Introduction/page

Guide to Azure Virtual WAN architecture, SKU selection, hub IP planning, cross tenant VNet connectivity, and routing controls to design and configure global hub and spoke network connectivity.

Connecting remote resources with Azure Virtual WAN

Azure Virtual WAN is a Microsoft-managed networking service that centralizes and simplifies connectivity for branch offices, remote users, and virtual networks by leveraging Microsoft's global backbone. It implements a hub-and-spoke, transit-style architecture: a managed Virtual WAN hub can terminate Site-to-Site VPN, ExpressRoute, and Point-to-Site connections, and provide global transit between multiple VNets.

This article explains how Virtual WAN works and how to plan and configure it for real-world scenarios. It is organized to help you understand the architecture, select the right SKU, design hub addressing, connect VNets across tenants, and control routing and traffic flows.

<Callout icon="lightbulb">
  Recommended prerequisites: familiarity with Azure networking concepts (VNet, subnet, Network Security Groups), Site-to-Site and Point-to-Site VPN basics, and an Azure subscription with contributor access to networking resources.
</Callout>

## Learning objectives

By the end of this article you will be able to:

* Describe Azure Virtual WAN and its hub-and-spoke transit model.
* Choose between the Basic and Standard WAN SKUs based on features and scale.
* Design IP address allocation for Virtual WAN hubs and hub services.
* Connect VNets from different Azure tenants to the same Virtual WAN hub for cross-organization or cross-team transit.
* Configure and control routing: route tables, associations, propagation, and custom labels to manage traffic flows.

| Topic                          | Outcome                                                                                                                                         |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| What is Azure Virtual WAN      | Understand hub-and-spoke transit and which connection types Virtual WAN supports (Site-to-Site, ExpressRoute, Point-to-Site, VNet connections). |
| WAN SKUs                       | Compare Basic vs Standard SKUs and pick the right SKU for scale and features.                                                                   |
| Hub IP addressing              | Learn how to assign private IP ranges to hubs to support hub services and avoid overlap with connected VNets.                                   |
| Cross-tenant VNet connectivity | Understand options and prerequisites to attach VNets from different Azure AD tenants to the same Virtual WAN hub.                               |
| Routing & control              | Learn about route tables, associations, propagation, and using labels for granular traffic control.                                             |

## What is Azure Virtual WAN?

Azure Virtual WAN provides an operationally simple, scalable way to connect distributed resources to a central transit hub that is managed by Microsoft. Key characteristics:

* Managed hub: Microsoft handles the underlying infrastructure for the hub.
* Global transit: Hubs in different regions can be used for global connectivity patterns.
* Multi-protocol termination: Supports Site-to-Site VPN, ExpressRoute, and Point-to-Site VPN from the hub.
* VNet connectivity: Connect multiple VNets to the hub for centralized routing.

Use cases include corporate branch connectivity, secure remote access for distributed workforces, multi-region VNet transit, and multi-tenant or multi-subscription network designs.

## WAN SKUs — Basic vs Standard

Choosing a WAN SKU affects scale, performance, and features. Below is a simplified comparison to help with selection.

| SKU      | Use cases                            | Key differences                                                                                    |
| -------- | ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Basic    | Small deployments or PoC             | Lower throughput, limited features; cost-effective for small-scale scenarios                       |
| Standard | Production and scale-out deployments | Higher throughput, advanced routing features, and additional resiliency and performance guarantees |

<Callout icon="warning">
  Before choosing a SKU, verify throughput and feature requirements for your expected traffic patterns (VPN tunnels, ExpressRoute, and Point-to-Site connections) and confirm SKU availability in your regions.
</Callout>

For detailed limits and pricing, consult the official Azure Virtual WAN documentation.

## IP address allocation for Virtual WAN hubs

Proper IP planning avoids overlap and enables hub services to function correctly. Best practices:

* Allocate a private, non-overlapping address range to each hub (e.g., /24 or larger) that does not conflict with connected VNets or on-premises networks.
* Reserve subnets for hub services if required by specific integrations.
* Document and enforce addressing policies across subscriptions and tenants to prevent collisions during cross-tenant VNet attachments.

## Connecting VNets across tenants

Virtual WAN supports connecting VNets from different Azure AD tenants to the same hub, which is useful for intercompany networks, multi-team boundaries, or separation of billing/subscription ownership. Key considerations:

* Permission model: subscriptions and resource groups that own the VNets must grant appropriate permissions for hub attachment.
* Peering alternatives: consider whether hub-based transit is required or if VNet peering across tenants (with proper authorization) could be simpler for your scenario.
* Security and governance: ensure RBAC, network policies, and logging are configured to meet compliance requirements.

## Routing in Azure Virtual WAN

Routing is a central function of the Virtual WAN hub. Understand these concepts:

* Route tables: Define how traffic is routed through the hub to connected resources or on-premises networks.
* Association: Route tables can be associated with specific connections or spokes to apply routing behavior.
* Propagation: Routes can be learned from on-premises or ExpressRoute and propagated to route tables.
* Labels: Custom route labels allow you to organize and prioritize routes for different traffic flows, enabling fine-grained control across multiple VNets and connections.

Practical tips:

* Use separate route tables for different traffic zones (for example, north-south external vs east-west VNet transit).
* Test route propagation and use network watcher or packet capture tools to validate expected forwarding paths.
* Document how labels and associations are applied to avoid unintended transit behavior.

## Next steps and references

* [Azure Virtual WAN Documentation](https://learn.microsoft.com/azure/virtual-wan/)
* [Azure Networking Documentation](https://learn.microsoft.com/azure/networking/)
* [Azure ExpressRoute Overview](https://learn.microsoft.com/azure/expressroute/)

This article prepares you to design and operate Virtual WAN for global connectivity. The following sections will provide step-by-step examples, configuration patterns, and routing configurations to implement the concepts introduced here.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/26572db6-1783-4efc-a13f-e3185c8ac54d/lesson/f3d9c058-0464-424f-8ae1-4c4bf376cd24" />
</CardGroup>
