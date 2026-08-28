# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Troubleshooting-ExpressRoute-Connections/Introduction/page

Troubleshooting Azure ExpressRoute connectivity and performance by validating circuit provisioning, peerings, BGP sessions, Layer 2 mappings, and measuring latency, jitter, throughput, and packet loss

Troubleshooting Azure ExpressRoute connections

In this lesson you'll learn the practical steps, checks, and tools to diagnose and resolve connectivity and performance issues with Azure ExpressRoute circuits. The guidance focuses on validating circuit provisioning, verifying peerings and routing, confirming Layer 2 mappings, and isolating performance bottlenecks so you can restore reliable connectivity between on-premises networks and Azure.

What you'll learn:

* How to confirm an ExpressRoute circuit is provisioned and in the correct state using the Azure Portal or Azure CLI.
* How to validate Azure Private and Microsoft peerings and common misconfigurations that break connectivity. (Public peering has been retired.)
* How to use ARP and Layer 2 checks to confirm MAC/IP mappings between on-premises equipment and Azure.
* How to identify and mitigate network performance issues that affect ExpressRoute.

| Objective                      | Why it matters                                               | Example verification                                                                        |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Circuit provisioning           | Ensures the circuit is created and enabled with the provider | `az network express-route show --name <circuit-name> --resource-group <rg>`                 |
| Peerings (Private & Microsoft) | Misconfigurations here commonly block routes                 | `az network express-route peering list --circuit-name <circuit-name> --resource-group <rg>` |
| Layer 2 ARP checks             | Confirms correct MAC \<> IP mappings and L2 behavior         | `show arp` (on-prem router/switch)                                                          |
| Performance troubleshooting    | Detects throughput, latency, jitter or packet loss issues    | `ping`, `traceroute`, BGP counters, SNMP/flow telemetry                                     |

<Callout icon="lightbulb">
  This lesson assumes familiarity with ExpressRoute concepts (circuits, peerings, BGP) and access to the Azure subscription where the ExpressRoute circuit is deployed. Recommended tools: the [Azure Portal](https://portal.azure.com), the [Azure CLI](https://learn.microsoft.com/cli/azure/?view=azure-cli-latest), and on‑premises network tools (router/switch `show arp`, BGP show commands, `ping`, `traceroute`, and packet captures).
</Callout>

Quick Azure CLI commands

* Show ExpressRoute circuit details:

```bash theme={null}
az network express-route show \
  --name <circuit-name> \
  --resource-group <resource-group>
```

* List peerings for a circuit:

```bash theme={null}
az network express-route peering list \
  --circuit-name <circuit-name> \
  --resource-group <resource-group>
```

* Show a specific peering (e.g., AzurePrivate):

```bash theme={null}
az network express-route peering show \
  --circuit-name <circuit-name> \
  --resource-group <resource-group> \
  --name AzurePrivatePeering
```

Troubleshooting checklist

1. Circuit state: Confirm the ExpressRoute circuit is provisioned and in the expected status in the Portal or via CLI.
2. Provider/Service Key: Verify the service key (SCK) and provider status if working with a connectivity partner.
3. Peerings: Validate that Azure Private and Microsoft peerings exist, are enabled, and have correct IP addresses and VLAN IDs.
4. BGP: Confirm BGP session establishment, route advertisement, and route acceptance on both sides. Check BGP state and prefix lists.
5. Layer 2: Use ARP entries and MAC tables on on‑prem switches to confirm correct mapping to the ExpressRoute VLAN.
6. Performance: Measure latency, jitter, throughput, and packet loss. Compare to SLA targets and baseline telemetry.
7. Escalation: If the issue appears on the provider side, gather configuration snippets, packet captures, and BGP logs before contacting the connectivity provider or Microsoft support.

Links and references

* [Azure ExpressRoute overview](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
* [Azure CLI reference: express-route](https://learn.microsoft.com/cli/azure/network/express-route)
* [BGP and routing with ExpressRoute](https://learn.microsoft.com/azure/expressroute/expressroute-routing)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6190597d-0e7a-4ffd-ac5d-afe70f482a27/lesson/5da8147c-83a6-4356-a7d5-50160d03d8e6" />
</CardGroup>
