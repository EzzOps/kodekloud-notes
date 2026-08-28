# Create network interfaces
$nic1 = New-AzNetworkInterface -Name $nicName1 -ResourceGroupName $resourceGroup -Location $locationWUS -Subnet $subnetObj1 -PublicIpAddress $pip1
$nic2 = New-AzNetworkInterface -Name $nicName2 -ResourceGroupName $resourceGroup -Location $locationEUS -Subnet $subnetObj2 -PublicIpAddress $pip2

Write-Host "Building VM configurations" -ForegroundColor Cyan
$vmConfig1 = New-AzVMConfig -VMName $vmName1 -VMSize "Standard_B1s" |
    Set-AzVMOperatingSystem -Linux -ComputerName $vmName1 -Credential $credential |
    Set-AzVMSourceImage -PublisherName $imagePublisher -Offer $imageOffer -Skus $imageSku -Version $imageVersion |
    Add-AzVMNetworkInterface -Id $nic1.Id

$vmConfig2 = New-AzVMConfig -VMName $vmName2 -VMSize "Standard_B1s" |
    Set-AzVMOperatingSystem -Linux -ComputerName $vmName2 -Credential $credential |
    Set-AzVMSourceImage -PublisherName $imagePublisher -Offer $imageOffer -Skus $imageSku -Version $imageVersion |
    Add-AzVMNetworkInterface -Id $nic2.Id

Write-Host "Creating VMs (this can take several minutes)" -ForegroundColor Cyan
New-AzVM -ResourceGroupName $resourceGroup -Location $locationWUS -VM $vmConfig1 | Out-Null
New-AzVM -ResourceGroupName $resourceGroup -Location $locationEUS -VM $vmConfig2 | Out-Null

# Private DNS Zone 
Write-Host "Creating Private DNS zone $privateDnsZoneName" -ForegroundColor Cyan
$dnsZone = New-AzPrivateDnsZone -Name $privateDnsZoneName -ResourceGroup $resourceGroup

Write-Host "Linking VMs to Private DNS zone with auto-registration" -ForegroundColor Cyan
New-AzPrivateDnsVirtualNetworkLink -ZoneName $privateDnsZoneName -ResourceGroupName $resourceGroup -Name $linkNameEUS -VirtualNetworkId $vnet1.Id -EnableAutoRegistration
New-AzPrivateDnsVirtualNetworkLink -ZoneName $privateDnsZoneName -ResourceGroupName $resourceGroup -Name $linkNameWUS -VirtualNetworkId $vnet2.Id -EnableAutoRegistration

Write-Host "Deployment complete." -ForegroundColor Green
Write-Host "VM 1 Public IP:" (Get-AzPublicIpAddress -Name $ipName -ResourceGroupName $resourceGroup).IpAddress
Write-Host "VM 2 Public IP:" (Get-AzPublicIpAddress -Name $ipName2 -ResourceGroupName $resourceGroup).IpAddress
```

After deployment you should see both VMs in the portal.

<Frame>
  <img alt="The image shows the Azure portal interface displaying a list of virtual machines within the &#x22;Compute infrastructure&#x22; section. There are two running Linux virtual machines listed, each with distinct locations and public IP addresses." />
</Frame>

To add peering you can also browse to **Virtual networks** in the portal and choose one of the VNets where you want to add a peering.

<Frame>
  <img alt="The image shows the Microsoft Azure portal displaying a list of virtual networks with details like name, resource group, location, and subscription. It includes options to create, manage, refresh, and filter virtual networks." />
</Frame>

## Check Private DNS registration

When the Private DNS zone is linked to both VNets with auto-registration enabled, each VM is automatically created as an A record in the zone.

<Frame>
  <img alt="The image shows an Azure portal interface displaying DNS zone settings for &#x22;az700peering.com,&#x22; including record sets with details like type, TTL, and values." />
</Frame>

From your workstation, SSH into one VM using its public IP and validate DNS resolution from within that VM. Example session (simplified):

```bash theme={null}
# SSH to the West US VM public IP (example)
ssh kodekloud@40.121.254.127

# On the VM, check DNS resolution for the East US VM
nslookup vm-az700-eus-01.az700peering.com
# Non-authoritative answer:
# Name: vm-az700-eus-01.az700peering.com
# Attempt to ping the private IP (will fail before peering is enabled)
ping vm-az700-eus-01.az700peering.com
# PING ... (10.10.1.4) ...
# --- vm-az700-eus-01.az700peering.com ping statistics ---
# 398 packets transmitted, 0 received, 100% packet loss
```

<Callout icon="warning">
  DNS resolution via a Private DNS zone does not guarantee connectivity. Private name resolution can succeed while traffic is blocked until you establish the VNet peering and enable Virtual Network Access on both sides.
</Callout>

## Configure VNet peering in the Azure portal

1. Open one of the virtual networks (for example, the East US VNet).
2. Select **Peering** and click **Add peering**.
3. On the Add peering page, select the remote virtual network and set the peering options:
   * Allow virtual network access (basic connectivity),
   * Allow forwarded traffic (hub-and-spoke / NVA scenarios),
   * Use remote gateway (gateway transit) if you want to reuse the gateway in the remote VNet.
4. Repeat on the remote VNet to establish bidirectional peering if required.

<Frame>
  <img alt="The image is a screenshot of the Microsoft Azure portal, displaying the overview section of a virtual network named &#x22;vnet-az700-peering-eus&#x22;. It includes details such as resource group, location, and various capabilities like DDoS protection and Azure Firewall." />
</Frame>

The form shows a local vs remote summary and exposes toggles for the three main options described above.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for adding virtual network peering. It includes options for selecting resource manager settings and configuring remote virtual network peering settings." />
</Frame>

Create the peering from both VNets if you require bidirectional traffic. When the peering state shows "Connected", you can re-run connectivity tests.

## Test connectivity after peering

After enabling peering (with Virtual Network Access allowed on both sides), ping/SSH across private addresses should succeed.

Example ping output after peering was enabled:

```plaintext theme={null}
# From East US VM, ping West US VM private name
PING vm-az700-peering-wus-01.az700peering.com (10.40.1.4) 56(84) bytes of data.
64 bytes from 10.40.1.4: icmp_seq=99 ttl=64 time=72.9 ms
64 bytes from 10.40.1.4: icmp_seq=100 ttl=64 time=72.4 ms
... (additional replies)
--- vm-az700-peering-wus-01.az700peering.com ping statistics ---
113 packets transmitted, 33 received, 70.80% packet loss, time 113949ms
rtt min/avg/max/mdev = 71.888/72.476/73.552/0.347 ms
```

Note: Depending on your environment there may be some packet loss or latency. The important change is that you now receive replies (where previously you saw 100% packet loss).

SSH over the peered private network:

```bash theme={null}
# From East US VM:
ssh vm-az700-peering-wus-01.az700peering.com
# Accept host key and provide password as prompted:
# Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
# Warning: Permanently added 'vm-az700-peering-wus-01.az700peering.com' (ED25519) to the list of known hosts.
# vm's password: <enter password>
# You should be logged in to the West US VM over the peered private network
```

## Conclusion and best practices

* VNet peering provides private connectivity between VNets using Azure's backbone and should be configured on both sides for full bidirectional flows.
* Enable forwarded traffic and gateway transit only when your architecture requires inspection, centralized routing, or gateway reuse.
* Always verify both name resolution (Private DNS) and actual traffic flow (ping/SSH) when validating a peering setup.
* Review network security group (NSG) and firewall rules if connectivity is blocked despite peering being in place.

Quick reminder: SSH into a VM using its public IP from your local host when needed:

```bash theme={null}
ssh kodekloud@40.121.254.127
```

## Links and references

* [Azure Virtual Network Peering documentation](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview)
* [Azure Private DNS documentation](https://learn.microsoft.com/azure/dns/private-dns-overview)
* [Azure VPN Gateway documentation](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/788bfe49-db39-491a-82d2-847c85bbcceb/lesson/d98d481d-d4e1-4411-a1a2-f43f96d26056" />
</CardGroup>


# Hub Spoke Architecture

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Enable-Cross-VNet-Connectivity/Hub-Spoke-Architecture/page

Overview of Azure hub-spoke network architecture centralizing shared services in a hub VNet with spoke VNets, covering peering, gateway transit, security, routing and operational guidance

Hub-Spoke Architecture is a common and proven network topology in Azure for centralising shared services while isolating workloads. This guide explains why organisations adopt it, how it works, and why it is often compared to an international airport hub.

## Concept and analogy

* Hub: A central VNet that hosts shared, centrally managed services such as VPN/ExpressRoute gateways, firewalls (Azure Firewall or NVAs), DNS, and other common infrastructure. Think of the hub as an international airport terminal where all inbound and outbound traffic is processed and inspected.
* Spokes: Individual VNets for workloads (production, test, dev, team environments). Spokes peer with the hub to consume shared services. By default, spokes do not peer directly with each other unless explicitly configured.

Centralising shared network services in a hub:

* Simplifies security and policy enforcement.
* Reduces duplication of expensive appliances (gateways, firewalls) per spoke.
* Provides a single point for monitoring, logging, and egress control.

<Frame>
  <img alt="The image illustrates a &#x22;Hub-Spoke Architecture&#x22; for a network setup using Azure VPN, showing connections between spokes, hubs, on-premises sites, other VNets, and VPN clients." />
</Frame>

## Gateway transit (shared gateway) and peering

* Hub-to-spoke connectivity is typically implemented with VNet peering, which uses the Azure backbone to provide high-bandwidth, low-latency private links.
* When spokes must use the hub's gateway for outbound connectivity (to on-premises or the Internet), enable gateway transit:
  * Set `AllowGatewayTransit` on the hub side of the peering.
  * Set `UseRemoteGateways` on each spoke peering.
* Enabling gateway transit lets spokes share a single VPN or ExpressRoute gateway in the hub instead of deploying individual gateway appliances in every spoke.

<Callout icon="lightbulb">
  To use the hub VPN/ExpressRoute gateway from spoke VNets, set `AllowGatewayTransit` on the hub peering and `UseRemoteGateways` on each spoke peering. This is required for gateway transit to work.
</Callout>

## Connections and centralisation

The hub commonly provides centralised connectivity to:

* On-premises datacenters via VPN or ExpressRoute.
* Other Azure VNets (including hub-to-hub or partner VNets).
* Remote VPN clients for administrative or user access.

Centralising these connections and security functions in the hub:

* Creates a single place to apply NSGs, Azure Firewall rules, routing, monitoring, and diagnostics.
* Avoids deploying and managing duplicate gateway appliances and firewalls for each spoke.

## One gateway only

In most hub-spoke designs, a single central VPN/ExpressRoute gateway in the hub is sufficient. This mirrors the airport analogy: spokes leverage the hub's international runway rather than building one each.

Be aware that deploying or resizing a VPN gateway is an operational activity that can take significant time (often \~40–45 minutes depending on SKU and region). Plan gateway changes and automation accordingly to avoid unexpected delays.

## VNet peering vs VPN gateway — concise comparison

Choosing between VNet peering and VPN gateways depends on performance, encryption requirements, cost, and topology. The following table summarises the key differences and typical use cases.

| Feature              |                                                   VNet peering | VPN gateway                                                                    |
| -------------------- | -------------------------------------------------------------: | ------------------------------------------------------------------------------ |
| Speed & latency      |            Very low latency; high throughput on Azure backbone | Higher latency due to encryption and tunnelling                                |
| Encryption & privacy |                 Private within Azure; not encrypted by default | Encrypted end-to-end using IPsec/IKE                                           |
| Cost                 |           Generally lower; charges typically for data transfer | Higher; pay for gateway SKU and tunnel/egress usage                            |
| Cross-region support |                        Global peering available across regions | Supports cross-region tunnels, but different performance profile               |
| Transitivity         |                     Non-transitive — peering is point-to-point | Can be transitive if traffic is routed via a central gateway (gateway transit) |
| Setup complexity     |                                                Simple and fast | More complex: gateway deployment, tunnels, routing; changes take time          |
| Typical use case     | Internal Azure workloads needing high performance and low cost | Hybrid connectivity (Azure-on‑prem), encrypted tunnels, or cross-cloud links   |

## Operational guidance

* Topology: Use a star topology where each spoke peers directly with the hub. This keeps routing clear and centralises policy enforcement.
* Default: VNet peering is the recommended default for internal Azure connectivity due to cost and performance.
* Use a central hub gateway when you need:
  * Encrypted tunnels to on-premises or third-party clouds,
  * Regulatory compliance that requires encryption or dedicated inspection,
  * Centralised egress and traffic inspection via a hub firewall or NVA.
* Hybrid approach: It’s common to peer all spokes to the hub for internal traffic while letting the hub provide centralized gateway transit for hybrid connectivity.

## Quick checklist (implementation)

* Design hub VNet with sufficient address space for gateway and shared services.
* Peer each spoke to the hub; avoid full mesh peering between spokes unless required.
* If using gateway transit:
  * Configure `AllowGatewayTransit` on the hub peering.
  * Configure `UseRemoteGateways` on each spoke peering.
* Centralise logging and monitoring in the hub (Network Watcher, NSG flow logs, Azure Firewall logs).
* Test routing and failover scenarios; account for gateway deployment and update times.

## Summary

Hub-spoke architecture centralises shared network services in a hub VNet while keeping workload VNets isolated as spokes. It simplifies security, reduces cost and operational overhead, and scales well as your Azure footprint grows. Use VNet peering for high-performance internal Azure traffic; use VPN/ExpressRoute gateways when encrypted hybrid connectivity or centralised inspection is required.

## Links and references

* [Azure hub-spoke architecture reference](https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/hub-spoke)
* [VNet peering overview](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview)
* [About Azure VPN Gateway](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpngateways)

<Frame>
  <img alt="The image is a comparison table between VNet Peering and VPN Gateway, highlighting differences in speed, encryption, cost, cross-region support, transitivity, setup complexity, and use case." />
</Frame>

This concludes the lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/788bfe49-db39-491a-82d2-847c85bbcceb/lesson/cf5ccf4f-c613-4096-8e13-70acaa8e2fa4" />
</CardGroup>
