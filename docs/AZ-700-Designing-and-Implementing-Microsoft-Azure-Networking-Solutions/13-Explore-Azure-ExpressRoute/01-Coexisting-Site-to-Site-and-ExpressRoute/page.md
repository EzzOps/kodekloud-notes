# Create peering from VNetA to VNetB
az network vnet peering create \
  --name VNetA-to-VNetB \
  --resource-group rg-a \
  --vnet-name VNetA \
  --remote-vnet /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/rg-b/providers/Microsoft.Network/virtualNetworks/VNetB \
  --allow-vnet-access true

# Create peering from VNetB to VNetA (reciprocal)
az network vnet peering create \
  --name VNetB-to-VNetA \
  --resource-group rg-b \
  --vnet-name VNetB \
  --remote-vnet /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/rg-a/providers/Microsoft.Network/virtualNetworks/VNetA \
  --allow-vnet-access true
```

Note: For `AllowGatewayTransit` and `UseRemoteGateways`, you must set these appropriately on the hub and spoke peerings and deploy a gateway in the hub's `GatewaySubnet`.

## Hub-spoke architecture, NVAs, and gateway transit

A common design pattern is hub-spoke, where the hub VNet hosts shared services (for example, an NVA, firewall, VPN gateway, or ExpressRoute). Spokes peer with the hub to consume those shared services.

NVAs and forwarding

* Because peering is non-transitive, to route traffic from Spoke A to Spoke B via an NVA in the hub:
  * Configure user-defined routes (UDRs) in the spokes to direct the relevant traffic to the hub NVA.
  * Enable `AllowForwardedTraffic` on the peering(s) if the NVA will forward traffic across peered VNets.
  * Ensure the NVA’s routing and Network Security Groups (NSGs) allow and forward the traffic to the intended destination.

Gateway transit

* To centralize an on-premises VPN or ExpressRoute gateway in the hub (saving cost and simplifying management):
  * On the hub peering, enable `AllowGatewayTransit`.
  * On the spoke peering(s), enable `UseRemoteGateways`.
  * The hub must have a VPN or ExpressRoute gateway deployed in its `GatewaySubnet`.
* Centralizing gateways requires careful capacity, routing, and security planning; monitor throughput and failover behavior.

<Frame>
  <img alt="The image is a diagram illustrating the implementation of VNet peering between three virtual networks (VNet A, HUB VNet, and VNet B) with labels indicating gateway transit, remote gateway usage, and peering connections. It includes elements like subnets, NVA, VPN gateway, and UDR." />
</Frame>

## Address space requirements

* Peered VNets must have non-overlapping IP address ranges. If address spaces overlap, the peering cannot be created.
* Plan address spaces during design to avoid collisions and to accommodate future growth and cross-region expansion.

> **lightbulb** Plan IP addressing and peering settings (`AllowForwardedTraffic`, `AllowGatewayTransit`, `UseRemoteGateways`) before implementation. Early planning prevents routing surprises in hub-spoke and NVA scenarios.

## Troubleshooting checklist

* Confirm address spaces do not overlap.
* Verify peering status is "Connected" in both VNets.
* Check `AllowVirtualNetworkAccess`, `AllowForwardedTraffic`, and gateway settings on both sides.
* Validate UDRs and NSGs to ensure traffic is routed and permitted as expected.
* For cross-tenant peering, ensure the required role assignments and authorizations are in place.

## Summary and next steps

VNet peering provides private, high-performance connectivity across VNets using the Microsoft backbone. It supports cross-subscription and cross-tenant peering and enables hub-spoke topologies with NVAs and centralized gateways when properly configured. Remember:

* Peering is non-transitive—explicit peering or NVAs + routing are required for multi-hop connectivity.
* VNets must have non-overlapping address spaces.
* Plan peering flags and routing before deployment.

Next steps:

* Follow the Azure portal walkthrough or the Azure CLI examples to create peering in your subscription.
* Review related concepts: Virtual Network, Network Security Groups, User-Defined Routes (UDRs), and Azure VPN/ExpressRoute gateways.

Links and references

* [Azure Virtual Network peering overview](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering)
* [Designing a hub-spoke topology in Azure](https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/hub-spoke)
* [Azure CLI: az network vnet peering](https://learn.microsoft.com/cli/azure/network/vnet/peering)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/788bfe49-db39-491a-82d2-847c85bbcceb/lesson/516e8e6d-67c6-49e8-9b91-ada86b2f2a3d)


# Coexisting Site to Site and ExpressRoute

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-ExpressRoute/Coexisting-Site-to-Site-and-ExpressRoute/page

Designing an Azure VNet that uses both ExpressRoute for high throughput private connectivity and VPN site-to-site for encrypted backup and branch connections with BGP failover

In this lesson we cover how to design an Azure virtual network (VNet) that concurrently uses both ExpressRoute and site-to-site (S2S) VPN connectivity. This hybrid pattern is common for organizations that require high throughput private connectivity to a primary datacenter while also supporting encrypted IPsec tunnels for remote offices, branch sites, or failover paths.

At a high level:

* The VNet contains two separate virtual network gateway resources in the GatewaySubnet: an ExpressRoute gateway for private peering and a VPN gateway for IPsec S2S (and optionally point-to-site) connections.
* ExpressRoute provides private, high-throughput connectivity to the main on-premises datacenter.
* The VPN gateway provides encrypted IPsec tunnels (and requires a public IP address for the gateway resource) for headquarters backup links and smaller branches that do not have ExpressRoute.

<Frame>
  <img alt="The image illustrates a dual gateway setup for a network, showcasing connections between a virtual network (VNET1) and on-premises locations using ExpressRoute and IPsec VPN tunnels. It details the setup of ExpressRoute and VPN gateways for connectivity between different sites." />
</Frame>

Implementation summary

* Deploy two distinct virtual network gateways in the same VNet (within the GatewaySubnet): one virtual network gateway configured for ExpressRoute and one for VPN. Each gateway supports only its corresponding connection type, so separation is required.
* Configure BGP and route preference attributes so the desired path (ExpressRoute vs VPN) is selected under normal conditions and so failover behavior occurs as intended.

> **lightbulb** Each gateway must be created and configured for its respective purpose—ExpressRoute for private peering and the VPN gateway for IPsec-based site-to-site or point-to-site connections. They can coexist on the same VNet but are deployed as separate gateway resources.

Why use both (benefits)

* Resiliency and business continuity: Use the VPN gateway as a failover for ExpressRoute when the private circuit is impacted (provider outage or maintenance). Proper routing/BGP configuration is required to ensure seamless failover.
* Flexibility: Connect smaller branches and remote workers over S2S or P2S VPN while keeping critical datacenter traffic on high-throughput ExpressRoute links.
* Geographical diversity: Use ExpressRoute for main datacenter capacity and VPN for geographically dispersed or temporary sites.

Gateway types at a glance

| Gateway Type          | Primary use case                                                  | Notes / Example                                                                                          |
| --------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| ExpressRoute gateway  | Private, high-throughput connectivity to on-premises datacenter   | Requires ExpressRoute circuit and private peering; does not require an Azure public IP like VPN gateways |
| VPN gateway (S2S/P2S) | Encrypted IPsec/IKE tunnels for remote sites or clients           | Requires a public IP for the gateway; supports IPsec S2S and point-to-site connections                   |
| Both coexisting       | Hybrid designs needing both high throughput and branch/remote VPN | Deploy both gateway resources in the same GatewaySubnet and manage routing preferences via BGP           |

Resiliency and failover considerations

* Routing and BGP: Use BGP route attributes (AS path, local preference, MED) to prefer ExpressRoute routes under normal operation and to allow the VPN route to take over during ExpressRoute disruption.
* Route advertisement: Ensure on-premises networks advertise the correct prefixes to both ExpressRoute and the VPN peer so Azure receives multiple paths and can switch when necessary.
* Health detection: Combine Azure routing with monitoring and automation to detect ExpressRoute failures and validate VPN path readiness.
* Bandwidth and cost: Remember the VPN path may have throughput and pricing differences compared to ExpressRoute; verify SKUs and throughput requirements.

<Frame>
  <img alt="The image illustrates a secure failover network architecture featuring an ExpressRoute Gateway and VPN connections between a virtual network in East US and on-premises sites. It includes IPsec/IKE S2S VPN tunnels for secure connectivity and specific IP addresses for network components." />
</Frame>

Common deployment checklist

* Create the GatewaySubnet in the VNet (correct size for gateways).
* Provision an ExpressRoute gateway and associate with your ExpressRoute circuit and private peering configuration.
* Provision a VPN gateway (choose an appropriate SKU for required throughput).
* Configure VPN S2S connections and/or point-to-site configurations for remote users.
* Enable BGP on both ExpressRoute and VPN gateways and configure route preferences for failover logic.
* Test failover: simulate ExpressRoute outage and validate traffic fails over to VPN, and fails back when ExpressRoute is restored.

Use cases and design notes

* Use ExpressRoute for primary datacenter connectivity (low latency, high throughput).
* Use VPN S2S as backup/failover for ExpressRoute or to connect smaller branches.
* Use point-to-site VPN for remote worker access if needed.
* Consider security, compliance, and routing policies when routing traffic across dual gateways.

<Frame>
  <img alt="The image is a network design diagram showing connections between a virtual network (VNET1) in East US and on-premises locations, using ExpressRoute and IPsec VPN tunnels. The design highlights aspects of high availability and geographical diversity." />
</Frame>

Configuration example snippets (Azure CLI)

* Create a GatewaySubnet:

```bash theme={null}
az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name GatewaySubnet \
  --address-prefixes 10.0.255.0/27
```

* Create a VPN gateway (example):

```bash theme={null}
az network vnet-gateway create \
  --resource-group myRG \
  --name myVpnGateway \
  --vnet myVNet \
  --public-ip-address myVpnGatewayPIP \
  --gateway-type Vpn \
  --vpn-type RouteBased \
  --sku VpnGw2
```

* Create an ExpressRoute gateway (example):

```bash theme={null}
az network vnet-gateway create \
  --resource-group myRG \
  --name myERGateway \
  --vnet myVNet \
  --gateway-type ExpressRoute \
  --sku ErGw2AZ
```

> **warning** Be mindful of gateway SKUs, throughput limits, and costs. Some SKUs do not support parallel VPN and ExpressRoute features or may impose throughput constraints—validate SKU capabilities before deploying to production.

Further reading and references

* [Azure ExpressRoute overview](https://learn.microsoft.com/azure/expressroute/overview)
* [Configure a VPN gateway](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-howto-site-to-site-resource-manager-portal)
* [Virtual network gateway SKUs and limits](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpngateways)

This article covered the architecture, benefits, and deployment considerations for running ExpressRoute and site-to-site VPN in the same Azure VNet, including high-level configuration, failover behavior, and practical deployment steps.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c1bf6def-e7d7-42de-8511-07397f2eaff9/lesson/efd89b55-edd0-4e70-9d26-3948a34c876a)
