# Configuring Peering

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Enable-Cross-VNet-Connectivity/Configuring-Peering/page

Guide to configuring Azure virtual network peering, including peering options, Private DNS setup, lab steps for cross‑VNet private connectivity, testing, and best practices

Configuring peering between two Azure virtual networks (VNets) enables private, low-latency communication between resources across VNets without exposing traffic to the public internet. This guide explains the key peering options, shows a short lab that demonstrates name resolution plus private connectivity between two Linux VMs in separate VNets/regions, and provides sample commands you can reuse.

## Key peering settings

When creating a VNet peering, you typically choose from these options:

| Setting                                            | What it does                                                                                                  | When to enable                                                                                 |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Virtual Network Access                             | Allows resources in one VNet to directly reach resources in the peered VNet (e.g., ping, SSH, TCP/UDP).       | Always enable when you need direct connectivity between VNets.                                 |
| Forwarded Traffic                                  | Permits traffic that was routed/inspected by an NVA or firewall in one VNet to continue into the peered VNet. | Enable for hub-and-spoke topologies where inspection or routing via a central NVA is required. |
| Gateway / Route Server Access (Use remote gateway) | Lets a VNet use a VPN gateway or route server deployed in the peered VNet (gateway transit).                  | Use when you want to share a single VPN/ExpressRoute gateway across VNets to save cost.        |

Peering is configured per VNet—if you want bidirectional traffic, create the peering from both sides and enable the appropriate options.

> **lightbulb** Peering is non-transitive by default. To support forwarded traffic or gateway transit, ensure the correct options are enabled on both sides of the peering and that your routing/NVA policies permit transit.

<Frame>
  <img alt="The image shows a virtual network peering configuration interface, with options for setting peering connections and access permissions, alongside labeled sections like &#x22;Virtual Network Access,&#x22; &#x22;Forwarded Traffic,&#x22; &#x22;Gateway/Route Server Access,&#x22; and &#x22;Peering Direction.&#x22;" />
</Frame>

In the Azure portal the peering UI surfaces these toggles explicitly so you only grant what your topology requires.

## Lab overview

This lab demonstrates private DNS name resolution and peering-based connectivity between VNets in different regions:

* Two Linux VMs are deployed in separate VNets and regions (East US and West US).
* A Private DNS zone is created and linked to both VNets so VMs are auto-registered with A records and resolve by private name.
* Initially DNS resolution succeeds but traffic between VNets is blocked. After creating peering (configured on both VNets), connectivity via private IPs is validated (ping / SSH).

## Create NICs, VMs, and a Private DNS zone (PowerShell snippet)

The following PowerShell excerpt shows the key steps to create NICs, VM configurations, deploy VMs, and create/link a Private DNS zone. Variables such as `$resourceGroup`, `$locationWUS`, `$locationEUS`, `$subnetObj1`, `$subnetObj2`, `$pip1`, `$pip2`, and credentials are assumed to be defined earlier in your script.

```powershell theme={null}
