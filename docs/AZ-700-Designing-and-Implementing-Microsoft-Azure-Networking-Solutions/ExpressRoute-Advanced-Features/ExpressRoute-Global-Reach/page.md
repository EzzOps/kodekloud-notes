# Example pattern (availability of flags varies by az version)
az network express-route connection update \
  --name <connection-name> \
  --resource-group <rg> \
  --express-route-gateway-bypass true
```

PowerShell example:

```powershell theme={null}
$connection = Get-AzVirtualNetworkGatewayConnection -Name "labConnection" -ResourceGroupName "lab-rg"
$connection.ExpressRouteGatewayBypass = $True
Set-AzVirtualNetworkGatewayConnection -VirtualNetworkGatewayConnection $connection
```

Note: CLI flag names and PowerShell property names may change with newer modules; always confirm with the latest Azure CLI / Az PowerShell reference.

<Callout icon="warning">
  Enabling FastPath changes the data plane for qualified traffic. Validate routing, perform staged testing, and confirm compatibility of gateway SKUs and connected appliances before enabling in production to avoid unintended traffic disruptions.
</Callout>

## Validation and operational tips

* After enabling FastPath, generate representative traffic and measure latency and throughput against baseline results.
* Monitor gateway metrics to confirm reduced processing load.
* Confirm control-plane operations (route updates, connection state) continue to function via the gateway.
* If issues appear, roll back the setting and re-run validation tests in a staging environment.

## References

* Azure ExpressRoute FastPath overview: [https://learn.microsoft.com/en-us/azure/expressroute/expressroute-fastpath-overview](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-fastpath-overview)

This concludes the ExpressRoute FastPath overview — enabling it can significantly improve data-plane performance when prerequisites and supported SKUs are validated.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/580264b2-4667-4ffc-a0f8-6d6592e1560e/lesson/341dd7fd-82b4-41ff-aa7d-adab930ca2f1" />
</CardGroup>


# ExpressRoute Global Reach

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/ExpressRoute-Advanced-Features/ExpressRoute-Global-Reach/page

Describes Azure ExpressRoute Global Reach enabling private cross-region WAN overlay over Microsoft backbone to connect on-premises sites and Azure regions securely with lower latency

[ExpressRoute Global Reach](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-global-reach) is a capability in Azure ExpressRoute that lets you link multiple ExpressRoute circuits to form a privately routed, cross-region WAN overlay over the Microsoft backbone. This enables you to unify on-premises sites and Azure regions into a single private network fabric without hairpinning traffic over the public Internet.

With Global Reach, traffic between your branch offices can traverse the Microsoft Global Network for improved predictability, lower latency, and stronger security compared to traversing the open Internet.

<Frame>
  <img alt="The image illustrates a network diagram showing cross-region connectivity to link multiple ExpressRoutes between the US West and UK South regions, with connections to locations in Silicon Valley, San Francisco, and London. It highlights features like geopolitical region access and global reach across premises." />
</Frame>

Key capabilities and scenarios

* Private WAN overlay: Connect two or more ExpressRoute circuits to create a private path between on-premises sites across regions.
* Carrier-agnostic interconnect: Use different local carriers at each site; traffic still flows over Microsoft’s backbone.
* Cross-region reach: With the appropriate SKU and region support, you can connect sites across continents without routing over the public Internet.
* ExpressRoute Direct option: For high-throughput, low-latency needs, consider [ExpressRoute Direct](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-direct) which offers dedicated physical ports (such as 10 Gbps or 100 Gbps) to the Microsoft network.

Real-world example

* Two ExpressRoute circuits—one in Tokyo and one in Silicon Valley—can be linked through Global Reach to create a private, global path between offices in those cities. As long as the ExpressRoute SKUs and regional availability support the link, all traffic will stay on the Microsoft Global Network.

SKU and regional considerations

| SKU       | Scope / Reach                                               | Typical use case                                                        |
| --------- | ----------------------------------------------------------- | ----------------------------------------------------------------------- |
| `Premium` | Global: access to all Azure regions and higher route limits | Cross-continental connectivity, large enterprise WANs                   |
| `Local`   | Metro / same-region only                                    | Localized connectivity, cost-sensitive or strictly regional deployments |

<Callout icon="lightbulb">
  Check regional availability: ExpressRoute Global Reach and some SKUs are not supported in every Azure region. Verify current [Microsoft documentation](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-global-reach) and regional availability before designing your topology.
</Callout>

<Frame>
  <img alt="The image shows a network diagram illustrating ExpressRoute's global reach, connecting multiple local service providers in Tokyo, Hong Kong, and the US to the Microsoft Global Network." />
</Frame>

How Global Reach works (brief)

* Each ExpressRoute circuit has private peering configured to exchange routes between your on-premises routers and the Microsoft fabric.
* When you link circuits using Global Reach, Microsoft injects route connectivity across those circuits so on-premises sites behind different circuits can exchange traffic over the Microsoft backbone.
* Optionally, you can configure a shared key when linking circuits for additional authentication during setup.

Configuration overview (Azure portal)

1. Open the ExpressRoute circuit you want to enable Global Reach on.
2. Verify private peering is correctly configured (ASN, peering subnets, VLAN IDs and BGP settings).
3. Click Add Global Reach on the circuit blade.
4. Select the peer circuit to link (for example, the circuit in the remote office/region). If available, enter a shared key for the connection.
5. Ensure the routing and peering configuration on the peer circuit matches expected parameters.
6. Repeat Add Global Reach for each pair of circuits you want to interconnect.
7. Save and confirm changes; Azure will establish the internal connectivity so traffic flows over the Microsoft Global Network.

<Frame>
  <img alt="The image shows the configuration interface for setting up ExpressRoute Global Reach, including settings for private peering and global reach options." />
</Frame>

Operational and design considerations

* Routing: Ensure route filters, BGP communities, and route limits are planned—Premium SKUs increase route capacity.
* Latency and path selection: Although traffic stays on Microsoft’s backbone, design for optimal paths and regional proximity where possible.
* Security and compliance: Global Reach avoids the public Internet, which aids security and compliance, but verify any regional/legal constraints (geopolitical boundaries).
* Interoperability: Because Global Reach is carrier-agnostic, you can use different service providers at each site; just ensure local connectivity to the ExpressRoute co-location is configured.

Summary

ExpressRoute Global Reach enables enterprises to:

* Build a private global WAN overlay between on-premises sites using the Microsoft Global Network.
* Avoid routing inter-site traffic over the public Internet for better security, predictability, and performance.
* Use different local carriers while maintaining a centralized private connectivity fabric.
* Extend connectivity across regions when using the Premium SKU—confirm region support and SKU capabilities before implementation.

Further reading and references

* [ExpressRoute Global Reach documentation](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-global-reach)
* [ExpressRoute Direct documentation](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-direct)
* [Azure ExpressRoute overview](https://learn.microsoft.com/en-us/azure/expressroute/)

Next, we'll examine another feature.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/580264b2-4667-4ffc-a0f8-6d6592e1560e/lesson/63575090-3921-440d-bbb1-bc03b7d63f04" />
</CardGroup>
