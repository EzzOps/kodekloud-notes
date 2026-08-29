# Working with Virtual WAN

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Remote-Resources-by-using-Azure-Virtual-WANs/Working-with-Virtual-WAN/page

Guide to deploying and managing Azure Virtual WAN, covering cross tenant VNet attachments, routing concepts, point to site VPN setup, hub configuration, and operational best practices.

In this lesson we explore how Azure Virtual WAN operates in practical deployments and how to connect cross-tenant VNets to a Virtual WAN hub. You’ll learn the key routing concepts, how to set up point-to-site (User VPN) connectivity, and best practices for managing route propagation and hub attachments.

Azure Virtual WAN enables centralized routing and consistent security controls across VNets that may belong to different tenants, subscriptions, or teams. It removes much of the manual configuration required by traditional hub-and-spoke designs and provides built-in support for VPN, ExpressRoute, and point-to-site client connectivity.

To connect a VNet from another tenant you need at least Contributor access on that VNet. Create a hub connection and provide the resource ID of the target VNet — it can be from another tenant. This simplifies cross-organization connectivity without complex peering or duplicated networking resources.

> **lightbulb** To connect a cross-tenant VNet you must have the appropriate permissions (typically Contributor) on the target VNet. Verify RBAC before attempting to create the hub connection.

<Frame>
  <img alt="The image illustrates a setup for connecting cross-tenant VNets to a Virtual WAN Hub, featuring components like Virtual Machine (VM), VNet, and Virtual WAN. It includes key points such as shared virtual WAN hub, VNet permissions, hub connection setup, and centralized management." />
</Frame>

This shared-hub model is useful for central IT teams, mergers and acquisitions, managed-service architectures, and any scenario that benefits from centralized governance.

## Routing in Azure Virtual WAN

Virtual WAN hubs use route tables to control traffic flow between VNets, branch VPN sites, and other attachments. Understanding association, propagation, and labels is crucial to designing predictable traffic flows.

Key concepts:

* Association — When a connection (VNet, VPN site, ExpressRoute) is associated with a route table, traffic originating from that connection is evaluated against the table’s routes.
* Propagation — Connections can propagate their prefixes into route tables, allowing other attachments to learn those routes (for example, an on-prem VPN site propagating routes to VNets).
* Labels — Labels (e.g., `Default`, `Internet`, `None`) allow grouping propagation behavior for multiple attachments, avoiding per-connection route configuration.
* Custom route policies — Define granular policies for complex topologies (hub-and-spoke, full mesh, or split tunneling) to control which routes are advertised and accepted.

<Frame>
  <img alt="The image illustrates a virtual hub routing setup, showing connections between VNet1, VNet2, a hub, and on-premises networks, with a route table listing destinations and next hops. Custom route policies such as hub-and-spoke, full mesh, and split tunneling are also mentioned." />
</Frame>

Example: routing with multiple VNets and a VPN gateway\
When VNets and an on-premises VPN gateway are attached to a Virtual WAN hub, each attachment can be associated with a specific route table (for instance, the default table). You combine association and propagation to control which networks learn which prefixes and how traffic is forwarded through the hub. For example, you can prevent two spokes from directly exchanging routes by restricting propagation or by associating them with separate route tables.

## Virtual WAN vs Traditional Hub-and-Spoke

Below is a concise comparison to help you choose the right design for your needs.

| Feature              | Azure Virtual WAN                                             | Traditional Hub-and-Spoke                                        |
| -------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------- |
| Management           | Managed service with automated routing and scaling            | Manual configuration of route tables, gateways, and peering      |
| Connectivity         | Integrated site-to-site VPN, point-to-site, and ExpressRoute  | Configure each connectivity method separately                    |
| Routing              | Centralized route tables, propagation, labels, route policies | Manual route distribution or through NVAs and BGP                |
| Cross-tenant support | Native cross-tenant VNet attachments                          | Requires complex peering and cross-tenant permissions            |
| Performance & scale  | Optimized over Azure backbone, scales with managed hub        | Depends on peering topology, gateway placement, and NVAs         |
| Deployment speed     | Fast via Portal/ARM/CLI templates                             | Slower — more manual linking and configuration                   |
| NVA/BGP              | Supports Azure Route Server integration and NVAs              | Often requires NVAs with manual BGP configuration                |
| Cost model           | Pay-per-connection + data transfer via managed hub            | Costs across individual resources (gateways, firewalls, peering) |
| Best fit             | Global, multi-branch, multi-tenant environments               | Small deployments or when extreme customization is required      |

Note: If your environment requires bespoke packet inspection or custom vendor appliances with specific routing logic, a traditional hub-and-spoke with NVAs may provide finer-grained control at the expense of operational overhead.

## Portal walkthrough — Create Virtual WAN, Hub, and Point-to-Site

This section summarizes the steps in the Azure portal to create a Virtual WAN, deploy a virtual hub (with gateway), and configure a point-to-site User VPN.

1. Create a Virtual WAN resource:
   * In the Azure portal, go to Create > Virtual WAN.
   * Fill in basics: subscription, resource group, and location.
   * Most configuration is done at the hub level, so WAN-level settings are minimal.

2. Create a virtual hub:
   * From the Virtual WAN blade, click New hub.
   * You can deploy a hub with a gateway; expect longer deployment time when a gateway is included.
   * Add a Point-to-site (User VPN) configuration inline, or create it separately and attach later.

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen for creating a virtual hub, specifically focusing on the &#x22;Point to site&#x22; connection settings. Options for VPN gateway, gateway scale units, and routing preference are displayed." />
</Frame>

3. Create a User VPN configuration (Point-to-site):
   * From the Virtual WAN blade, go to User VPN configuration -> Create.
   * Select tunnel type (e.g., OpenVPN®) and choose an authentication method such as Azure AD.
   * If you choose Azure AD authentication, you must supply Audience, Issuer, and Tenant ID. See Microsoft docs for correct values.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for creating a new User VPN configuration, displaying fields for project and instance details. Users can select subscription, resource group, name, and tunnel type for the VPN configuration." />
</Frame>

Use the Microsoft documentation for Azure AD/OpenID Connect values:

* OpenVPN Azure AD authentication: [https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication](https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication)

<Frame>
  <img alt="The image displays a webpage from Microsoft Azure documentation, providing instructions on configuring Azure VPN Client settings, including details about Tenant, Audience, and Issuer values for Microsoft Entra ID." />
</Frame>

After adding the authentication details (Audience, Issuer, Tenant ID), validate and create the User VPN configuration.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface where a new User VPN configuration is being created, specifically under the &#x22;Azure Active Directory&#x22; tab." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for creating a new User VPN configuration, with validation passed and details for Azure Active Directory and other settings before finalizing the creation." />
</Frame>

Once the User VPN configuration is created, attach it to the virtual hub. Monitor deployment progress in the portal and then manage attachments and routing once the hub is active.

<Frame>
  <img alt="The image shows the Microsoft Azure portal displaying a User VPN configurations page for a virtual WAN. A notification indicates a successful addition of a User VPN configuration." />
</Frame>

### Hub creation settings and capacity

When creating the hub you must specify:

* Region (hub deployment region)
* Hub private address range (for example `10.140.0.0/24`)
* Virtual hub capacity (gateway scale units / infrastructure routing units)
* Routing preference (for example `VPN`)

Routing units and gateway capacity determine throughput and client support. For example, a single gateway scale unit supports roughly 500 P2S clients (verify current limits in Microsoft docs).

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen where a user is creating a virtual hub, filling in details such as region, name, hub private address space, virtual hub capacity, and hub routing preference." />
</Frame>

If you select a gateway (to enable P2S, S2S, or ExpressRoute), deployment time increases and the portal shows an estimate.

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen for creating a virtual hub, with details about the hub's configuration and a notification about the creation process duration." />
</Frame>

After deployment finishes, the portal shows the VirtualHubDeployment completion and you can open the hub resource to continue configuration.

<Frame>
  <img alt="The image shows an overview page in the Microsoft Azure portal indicating that a deployment named &#x22;VirtualHubDeployment&#x22; is complete, along with details such as subscription and resource group." />
</Frame>

## Adding virtual network connections (spokes)

From the Virtual WAN blade you create virtual network connections to attach VNets as spokes. When adding a connection you can:

* Select the target VNet (spoke)
* Choose a route table association
* Configure propagation (which route tables should receive propagated routes)
* Assign labels for grouping and easier management

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface, displaying an overview of a Virtual WAN named &#x22;vwan-az700-eus,&#x22; with details such as resource group, location, and status. A world map with a virtual hub location marked is visible at the bottom." />
</Frame>

Use the Add connection form to create spokes (for example Spoke A in West US, Spoke B in East US) and pick whether to propagate routes and which route table to associate.

<Frame>
  <img alt="The image shows a Microsoft Azure interface for adding a virtual network connection within a Virtual WAN configuration. Various fields such as subscription, resource group, and virtual network are filled in the &#x22;Add connection&#x22; form." />
</Frame>

## Managing routes, diagnostics, and point-to-site clients

From the hub resource you can:

* Inspect route maps and routing intent
* View BGP peers and route tables
* Validate which routes are propagated and associated
* Download point-to-site client profiles and monitor VPN metrics

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface focused on the &#x22;User VPN (Point to site)&#x22; section, displaying details such as gateway scale units, configuration options, and charts for VPN route count and bandwidth usage." />
</Frame>

### Download and use the VPN profile

Generate and download the VPN profile for the User VPN configuration. The profile contains client configuration files (for example, XML for the Azure VPN Client or OpenVPN profiles). Import the profile into the Azure VPN Client (or your OpenVPN client), then authenticate to connect.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a virtual WAN user VPN configuration, with a pop-up window open for the Azure VPN Client settings. There's a form for establishing a VPN connection with options for server validation and client authentication." />
</Frame>

After connecting with your chosen auth method (Azure AD, certificate, etc.), verify that propagated routes and spokes are visible in the client’s routing table and that you can reach internal resources by their private IP addresses.

<Frame>
  <img alt="The image shows the Microsoft Azure portal with details of a virtual network named &#x22;vnet-az700-vwan-wus&#x22; and a VPN client window displaying connection properties and status logs." />
</Frame>

## Validation: access resources across VNets

With the VPN connected and VNets attached to the hub, clients should be able to access internal VMs and services using private IP addresses. Confirm:

* Route tables are associated/propagated as expected
* Security groups and NSGs allow the required traffic
* Any NVAs or firewall policies are permitting the flows

## Summary

Azure Virtual WAN provides a managed, scalable solution for global, multi-branch, and cross-tenant connectivity. Use central route tables, association/propagation, labels, and custom route policies to control route distribution and traffic flow. For highly customized network functions or specialized third-party appliances, a traditional hub-and-spoke design may still be appropriate, but expect additional configuration and operational overhead.

Further reading:

* Azure Virtual WAN documentation: [https://learn.microsoft.com/azure/virtual-wan](https://learn.microsoft.com/azure/virtual-wan)
* OpenVPN + Azure AD authentication: [https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication](https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication)
* Virtual WAN limits and throughput: [https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-limits](https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-limits)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/26572db6-1783-4efc-a13f-e3185c8ac54d/lesson/60bd001d-a6e8-47b2-b5a4-1fe78638695b)
