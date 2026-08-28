# Create peering from vnet-a to vnet-b
az network vnet peering create \
  --name vnetA-to-vnetB \
  --resource-group rgA \
  --vnet-name vnetA \
  --remote-vnet /subscriptions/<subB>/resourceGroups/rgB/providers/Microsoft.Network/virtualNetworks/vnetB \
  --allow-vnet-access true

# Create peering from vnet-b to vnet-a
az network vnet peering create \
  --name vnetB-to-vnetA \
  --resource-group rgB \
  --vnet-name vnetB \
  --remote-vnet /subscriptions/<subA>/resourceGroups/rgA/providers/Microsoft.Network/virtualNetworks/vnetA \
  --allow-vnet-access true \
  --allow-forwarded-traffic true \
  --use-remote-gateways false
```

Replace placeholders such as `<subA>`, `<subB>`, `rgA`, `rgB`, `vnetA`, and `vnetB` with your actual values.

## Shared gateway (hub-and-spoke) scenario

If multiple VNets need to reach on-premises networks using a single gateway, configure a hub VNet with the gateway and have spoke VNets peer with the hub:

* On the hub VNet peering settings: enable Allow gateway transit.
* On each spoke VNet peering settings: enable Use remote gateways.
* Ensure only the hub has the gateway configured (spokes should not also have gateways when using remote gateway).

Benefits: reduced cost (single gateway), centralized connectivity, simplified routing and on-premises network management.

## Best practices and considerations

* Use regional peering for low-latency intra-region traffic; use global peering for cross-region needs.
* Monitor peering metrics and VNet traffic for cost and performance—cross-region data transfer may incur charges.
* Use NSGs and route tables to control traffic flows even after peering is established.
* Remember that peering can't be applied to VNets with overlapping IP ranges.

## Quick reference links

* [Azure Virtual Network Peering documentation](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering)
* [Azure CLI network commands](https://learn.microsoft.com/cli/azure/network)
* [Designing hub-spoke topology in Azure](https://learn.microsoft.com/azure/architecture/reference-architectures/vnet/vnet-hub-spoke)

So let’s start with how to link virtual networks—using the Azure Portal, Azure CLI, or PowerShell—to establish private, high-performance communication between your VNets.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/788bfe49-db39-491a-82d2-847c85bbcceb/lesson/96a31727-209a-484e-887c-91ea333fcc85" />
</CardGroup>


# VNet Peering

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Enable-Cross-VNet-Connectivity/VNet-Peering/page

Explains Azure VNet peering, features, configuration flags, regional and global modes, hub-spoke topologies with NVAs and gateway transit, addressing, routing, and troubleshooting.

Azure Virtual Network (VNet) peering connects separate VNets so resources (for example, virtual machines) communicate privately using their private IP addresses. Peering uses the Microsoft backbone network, providing low-latency, high-bandwidth connectivity without traversing the public internet. This enables secure, fast communication that preserves the native network experience.

What you'll learn in this article:

* When to use VNet peering (regional vs. global)
* Key features and configuration flags
* How peering fits into common topologies such as hub-spoke with NVAs and gateway transit
* Addressing and routing considerations

## Types of VNet peering

VNet peering supports two modes:

| Peering type          | Scope                        | Use case                                                                                                                |
| --------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Regional VNet peering | Within the same Azure region | Low-latency communication between VNets in a single region (e.g., for microservice separation or environment isolation) |
| Global VNet peering   | Across Azure regions         | Connect VNets across regions for geo-redundancy, multi-region services, or cross-region migrations                      |

<Frame>
  <img alt="The image depicts types of VNet peering, showing Global VNet Peering between VNet1 in Region 1 and VNet2 in Region 2, and Regional VNet Peering between VNet2 and VNet3 within Region 2." />
</Frame>

This flexibility lets you design either regional or global topologies depending on requirements such as latency, data residency, or redundancy.

## Key features

1. Data path

* Traffic between peered VNets flows directly over the Microsoft backbone network; it does not transit the public internet. This improves both performance and security.

2. Cross-subscription and cross-tenant support

* You can peer VNets across subscriptions and Azure Active Directory tenants (with the correct authorization). This is useful for multi-account organizations or when consolidating services across business units.

3. Peering controls and configuration flags

* Each peering has several important configuration options you should plan for when designing your network.

| Flag                        | Default | Description                                                                      | Typical use                                                |
| --------------------------- | ------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `AllowVirtualNetworkAccess` | true    | Enables traffic between the two VNets.                                           | Default connectivity between peered VNets.                 |
| `AllowForwardedTraffic`     | false   | Allows forwarded traffic from an NVA in the peered VNet to reach the local VNet. | Required for hub NVAs forwarding transit traffic.          |
| `AllowGatewayTransit`       | false   | Allows a peered VNet to advertise its gateway to other VNets.                    | Enable on the hub VNet to allow spokes to use its gateway. |
| `UseRemoteGateways`         | false   | Lets a VNet use the gateway of a peered VNet.                                    | Enable on spokes when centralizing gateway in the hub.     |

4. Non-transitive connectivity

* VNet peering is non-transitive. If VNet A is peered to VNet B, and VNet B is peered to VNet C, A does not have automatic connectivity to C. You must peer A↔C directly or forward traffic explicitly using an NVA and appropriate routing.

<Callout icon="warning">
  Peering is non-transitive by design. If you expect hub-to-spoke transit, configure user-defined routes and allow forwarded traffic where necessary. Assuming transitive connectivity without explicit configuration can break traffic flows.
</Callout>

<Frame>
  <img alt="The image illustrates VNet Peering features, showing a diagram with global and regional peering connections between virtual networks (VNet1, VNet2, VNet3) across two regions. It highlights features such as data path, multi-tenant support, and non-transitivity." />
</Frame>

## Example: Create VNet peering (Azure CLI)

Here is a concise example that creates peering between two VNets using the Azure CLI. Adjust names, resource groups, and locations to your environment.

```bash theme={null}
