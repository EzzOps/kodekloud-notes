# Variables
$resourceGroup = "rg-az700-private-dns"
$locationEUS = "eastus"
$locationWUS = "westus"
$username = "kodakloud"
$password = "@dm1nP@ssW0rd"

# VM 1 (East US)
$vmName1 = "vm-az700-eus-01"
$netName1 = "vnet-az700-eus"
$subnetName1 = "subnet-az700-eus"
$ipName1 = "ip-az700-eus"
$nicName1 = "nic-az700-eus"
$addressPrefix1 = "10.10.0.0/16"
$subnetPrefix1 = "10.10.1.0/24"

# VM 2 (West US)
$vmName2 = "vm-az700-wus-01"
$netName2 = "vnet-az700-wus"
$subnetName2 = "subnet-az700-wus"
$ipName2 = "ip-az700-wus"
$nicName2 = "nic-az700-wus"
$addressPrefix2 = "10.20.0.0/16"
$subnetPrefix2 = "10.20.1.0/24"

# Create Resource Group
New-AzResourceGroup -Name $resourceGroup -Location $locationEUS

# Create Subnet configurations
$subnet1 = New-AzVirtualNetworkSubnetConfig -Name $subnetName1 -AddressPrefix $subnetPrefix1
$subnet2 = New-AzVirtualNetworkSubnetConfig -Name $subnetName2 -AddressPrefix $subnetPrefix2

# Create VNets
New-AzVirtualNetwork -Name $netName1 -ResourceGroupName $resourceGroup -Location $locationEUS -AddressPrefix $addressPrefix1 -Subnet $subnet1
New-AzVirtualNetwork -Name $netName2 -ResourceGroupName $resourceGroup -Location $locationWUS -AddressPrefix $addressPrefix2 -Subnet $subnet2

# Create a Public IP (example)
New-AzPublicIpAddress -Name $ipName1 -ResourceGroupName $resourceGroup -Location $locationEUS -AllocationMethod Static
```

Create a Private DNS zone

* In the Azure portal go to Private DNS zones and create a new zone (example: `kodekloudint.com`) in a resource group such as `RG-AZ700-PRIV-DNS-01`. Private DNS zones are global resources; the resource group location stores metadata only.

<Frame>
  <img alt="The image shows the &#x22;Review + Create&#x22; page for setting up a Private DNS Zone on the Microsoft Azure portal. It includes details like subscription, resource group, and DNS zone information." />
</Frame>

Linking VNets to the Private DNS zone
By default a private DNS zone is not linked to any virtual networks. To make a VNet resolve names in that zone, add a virtual network link.

* A Virtual Network Link tells Azure that the zone (for example `kodekloudint.com`) will be used for name resolution by that VNet.
* Enable "Auto registration" so that new VMs in the linked VNet automatically register host A records into the private zone.

In the portal, add a Virtual Network Link, select the target VNet, and enable auto‑registration as required.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface for adding a virtual network link, with options to configure virtual network details and enable auto registration." />
</Frame>

After you create a virtual network link, the linked VNet can resolve records in the private DNS zone. Initially a private zone includes SOA and NS records only; with auto‑registration enabled, VM host A records appear automatically.

<Frame>
  <img alt="The image shows a Microsoft Azure portal displaying the &#x22;Virtual Network Links&#x22; section for the domain &#x22;kodekloudint.com,&#x22; with a notification about creating a virtual network link." />
</Frame>

Add manual record sets (optional)
You can manually add records to a Private DNS zone — for example, an A record `web.kodekloudint.com` pointing to `192.168.10.10`.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface, specifically the &#x22;Recordsets&#x22; section for a DNS zone, where a new A record is being added with an IP address of 192.168.10.10." />
</Frame>

Over time you will see record types such as SOA, NS, manually created A records, and auto‑registered VM records listed in the zone.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface displaying DNS records for a private DNS zone, where various record sets are listed with their types, TTL, and values." />
</Frame>

Testing from VMs

* If a VM is in a VNet linked to the private DNS zone, `nslookup` on the VM should return records from that zone.
* If a VM is in a VNet that is not linked, lookups for the private names will return `NXDOMAIN`.

Example: SSH to the East US VM (which has its VNet linked) and resolve the manually created `web.kodekloudint.com` record:

```bash theme={null}
ssh kodekloud@172.174.2.101
# On the remote VM:
kodekloud@vm-az700-eus-01:~$ nslookup web.kodekloudint.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   web.kodekloudint.com
Address: 192.168.10.10
```

From the West US VM (before linking its VNet), the same lookup returns `NXDOMAIN`:

```bash theme={null}
ssh kodekloud@20.253.255.34
# On the remote VM:
kodekloud@vm-az700-wus-01:~$ nslookup web.kodekloudint.com
Server:         127.0.0.53
Address:        127.0.0.53#53

** server can't find web.kodekloudint.com: NXDOMAIN
```

To fix that, add a Virtual Network Link for the West US VNet (enable auto‑registration if desired). After linking, the West US VM can resolve the East US VM's auto‑registered record:

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying a private DNS zone overview for &#x22;kodeloudint.com&#x22; with details like resource groups, subscriptions, and virtual network links. A notification indicates the successful creation of a virtual network link." />
</Frame>

Example after linking:

```bash theme={null}
# On West US VM after linking its VNet to the private DNS zone:
kodekloud@vm-az700-wus-01:~$ nslookup vm-az700-eus-01.kodekloudint.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   vm-az700-eus-01.kodekloudint.com
Address: 10.10.1.4

# The name resolves, but connectivity depends on VNet connectivity (peering, VPN, etc.)
kodekloud@vm-az700-wus-01:~$ ping vm-az700-eus-01.kodekloudint.com
PING vm-az700-eus-01.kodekloudint.com (10.10.1.4) 56(84) bytes of data.
```

Important: name resolution does not guarantee reachability. If VNets are isolated (no peering, no VPN/ExpressRoute), DNS will resolve names but network traffic will not flow. To enable traffic, establish VNet peering or appropriate private connectivity.

Summary and recommended practices

* Use Azure Private DNS zones for private name resolution and link VNets with Virtual Network Links.
* Enable auto‑registration for dynamic VM record creation in linked VNets.
* For complex environments, use hub‑and‑spoke DNS placement and conditional forwarders to on‑premises DNS to avoid linking every spoke VNet to a zone.
* Secure your DNS servers and network access; do not expose internal DNS servers to the internet.
* Combine DNS configuration with proper network connectivity (peering, VPN, ExpressRoute) to provide both resolution and reachability.

Links and references

* Azure Private DNS zones: [https://learn.microsoft.com/azure/dns/private-dns-overview](https://learn.microsoft.com/azure/dns/private-dns-overview)
* Azure DNS recursive resolver: [https://learn.microsoft.com/azure/dns/dns-resolver-overview](https://learn.microsoft.com/azure/dns/dns-resolver-overview)
* VNet peering: [https://learn.microsoft.com/azure/virtual-network/virtual-network-peering](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering)

For further examples on conditional forwarders and DNS forwarding between Azure and on‑premises, see the Azure DNS documentation and design guidance above.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c82c47ed-c3b3-4aa2-ac47-d0ee418e9797/lesson/f98db398-5f4d-418c-93b4-74ab9b6a5690)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Name-Resolution-for-Azure-Virtual-Network/Introduction/page

Overview of Azure VNet name resolution and DNS management including Azure resolver, Private DNS zones, custom DNS, DNS delegation, and best practices for secure multi VNet connectivity

Welcome to the lesson on name resolution in Azure Virtual Networks. This module explains how DNS works in Azure for both public and private scenarios and shows how to customize resolution for secure, reliable connectivity across resources and VNets.

What you'll learn:

* How Azure-provided name resolution differs from custom DNS servers and services.
* How to create and manage DNS zones and records (A records, CNAMEs, etc.) to map names to Azure resources.
* How to configure Azure Private DNS zones for secure, internal name resolution across virtual networks.
* When and how to implement DNS delegation to split DNS management or delegate subdomain authority.
* Best practices for name resolution and DNS customization within Virtual Networks (VNets).

Learning outcomes mapped to examples and tasks:

| Outcome                                  | Example / Task                                                                          |
| ---------------------------------------- | --------------------------------------------------------------------------------------- |
| Distinguish Azure DNS vs custom DNS      | Understand Azure Recursive Resolver and when to deploy custom DNS servers or forwarders |
| Create and manage DNS zones              | Create a Public or Private DNS zone in the Azure portal; add `A` and `CNAME` records    |
| Configure Private DNS zones across VNets | Link a Private DNS zone to one or more VNets for name resolution across subscriptions   |
| Implement DNS delegation                 | Delegate a subdomain to another DNS zone or on-premises DNS using NS records            |
| Apply best practices                     | Use conditional forwarding, split-horizon DNS, and secure DNS zone management           |

<Frame>
  <img alt="The image lists four learning objectives related to Azure, including domain name resolution, DNS configuration, DNS delegation, and best practices for private zones and DNS customization within VNets." />
</Frame>

This lesson covers how Azure automatically assigns DNS settings to virtual machines and platform services in a VNet, how the Azure recursive resolver handles internal lookups, and how to override or extend that behavior with custom DNS or Private DNS zones. You will see common deployment patterns that enable discovery across multiple VNets and subscriptions while maintaining security boundaries.

> **lightbulb** Note: Azure’s platform DNS resolver is available to VMs and PaaS services in a VNet and simplifies internal name resolution. When you need advanced control—such as custom forwarders, conditional forwarding, split-horizon DNS, or integration with on-premises DNS—you can configure your own DNS servers or use Azure Private DNS zones. See the Azure DNS documentation for details.

We conclude the lesson with a real configuration example and a concise summary of recommended practices so you can design name resolution that is predictable, secure, and easy to manage across teams and environments.

Links and references

* [Azure DNS documentation](https://learn.microsoft.com/azure/dns/)
* [Azure Private DNS overview](https://learn.microsoft.com/azure/dns/private-dns-overview)
* [Name resolution for VMs and role instances in Azure VNets](https://learn.microsoft.com/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances)
* [Delegating domain or subdomain to Azure DNS](https://learn.microsoft.com/azure/dns/dns-delegate-domain-subdomain)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c82c47ed-c3b3-4aa2-ac47-d0ee418e9797/lesson/8a998b92-e2c6-4c4b-bfc8-49c7f300cdc8)
