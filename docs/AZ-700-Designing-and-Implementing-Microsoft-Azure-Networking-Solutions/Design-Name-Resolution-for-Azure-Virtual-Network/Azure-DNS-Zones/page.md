# Azure DNS Zones

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Name-Resolution-for-Azure-Virtual-Network/Azure-DNS-Zones/page

Guide to creating and managing Azure public and private DNS zones, delegating name servers, and adding record sets.

In this lesson/article we move from basic DNS concepts into Azure-specific DNS management.

A DNS zone in Azure is a container that holds DNS records for a specific domain. For example, if you own `echovisa.com`, the DNS zone stores all records related to that domain — A records for web servers, MX for mail, TXT for verification, and so on. You can manage DNS zones across different Azure subscriptions, which helps when an organization splits environments or teams across subscriptions.

Each DNS zone you create in Azure is assigned a unique set of name servers. These name servers are how you delegate DNS responsibility for the domain to Azure, and they prevent conflicts when multiple DNS services exist for the same domain.

<Frame>
  <img alt="The image is a screenshot showing the Azure DNS Zones interface, specifically the &#x22;Create DNS zone&#x22; page, with project and instance details. Key features like DNS zone containers and reuse across subscriptions are highlighted on the right." />
</Frame>

When you create a DNS zone in Azure and delegate your domain's name servers to those Azure name servers, Azure becomes authoritative for DNS queries for that domain.

You can purchase domains directly from Azure ([App Service Domains](https://learn.microsoft.com/en-us/azure/app-service/manage-custom-domains/purchase-domain)), or you can buy domains from registrars such as [GoDaddy](https://www.godaddy.com) or [Namecheap](https://www.namecheap.com). If you bought the domain from a registrar, your domain will initially use the registrar’s name servers. To make Azure authoritative, you update (delegate) the domain at your registrar by replacing those registrar name servers with the Azure DNS name servers provided when you create the zone.

DNS delegation is simply handing control of a portion of the DNS namespace (for example, `echovisa.com`) to another DNS service (Azure DNS). The delegation process is:

1. Create a zone in Azure. Azure provides a set of name servers for the zone.
2. At your domain registrar, edit the domain’s name server records and replace them with the Azure-provided name servers.
3. Wait for DNS propagation. After delegation propagates, queries for your domain resolve via Azure DNS.

<Frame>
  <img alt="The image shows a form for creating a DNS zone in Azure, with sections for project and instance details, and instructions for DNS delegation, including steps on copying Azure name servers and updating registrar settings." />
</Frame>

## Record sets

Within a DNS zone you add record sets. A record set groups DNS records of the same name and type. For example, a record set named `www` of type A can hold one or more A records (multiple A records are commonly used for basic load distribution).

Azure DNS supports standard record types: A, AAAA, CNAME, MX, NS, TXT, PTR, SRV, and more. Azure prevents duplicate records within the same record set to avoid conflicts. The input fields in the portal change depending on the record type you choose — for example, A records require IPv4 addresses; CNAME records require a canonical name target.

<Frame>
  <img alt="The image shows a form for adding a DNS record set, including fields for name, type, alias record set, TTL, and IP address. A sidebar note explains that a record set groups DNS records of the same type and name within a zone." />
</Frame>

## Demonstration: Create a zone in the portal

To create a public DNS zone in the Azure portal:

* Search for “DNS zones” (do not select Private DNS zones if you want a public zone).
* Click Create.
* Choose a subscription and resource group, and enter the zone name (for example, `echovisa.com`).
* Optionally upload a zone file if you have many records to import.
* Review + create.

<Frame>
  <img alt="The image shows a Microsoft Azure DNS management interface with no DNS zones displayed, featuring options to create a new zone or learn more." />
</Frame>

After the zone is created, open it. You will see the SOA (Start of Authority) and NS (name server) record sets. Azure provides four global name servers for redundancy. You can add custom records under Record sets.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface for creating a DNS zone, where users can upload a DNS zone file or copy their DNS zone details. The interface includes navigation tabs and buttons for progressing through the setup process." />
</Frame>

Example: add a record `az700.echovisa.com` as an A record with IP `1.1.1.1`. Click Add and the record will exist in the Azure DNS zone.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface where a DNS record set for &#x22;echovisa.com&#x22; is being managed. The DNS Management tab is open, displaying options to add a new A (IPv4 Address) record set." />
</Frame>

If you run a normal DNS lookup from your workstation immediately after creating the record, you may still see responses from your registrar’s name servers (for example, GoDaddy) because public DNS is still delegated to the registrar’s name servers. Example lookup that queries the default resolver (your ISP or local DNS cache):

```bash theme={null}
nslookup az700.echovisa.com
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
Name:   az700.echovisa.com
Address: 13.248.169.48
Name:   az700.echovisa.com
Address: 76.223.54.146
```

Those responses are coming from the registrar’s DNS servers, not Azure. To verify Azure's record directly, set the nslookup server to one of the Azure-provided name servers (copy a server name from the Azure portal) and query again:

```bash theme={null}
nslookup
> server ns1-09.azure-dns.com.
Default server:  ns1-09.azure-dns.com.
Address:        13.107.236.9#53
> az700.echovisa.com
Server:     ns1-09.azure-dns.com.
Address:    13.107.236.9#53

Name:   az700.echovisa.com
Address: 1.1.1.1
```

This demonstrates that the record exists in Azure, but the global DNS system still points to your registrar's name servers until you update them. You cannot practically configure every resolver in the world to query the Azure name servers directly — instead you delegate the domain at the registrar.

<Frame>
  <img alt="This image shows a screenshot of the MXToolbox SuperTool webpage displaying the DNS lookup results for &#x22;echovisa.com,&#x22; including IP addresses and TTL information." />
</Frame>

## Performing delegation at the registrar (example: [GoDaddy](https://www.godaddy.com))

To make Azure authoritative for `echovisa.com`:

1. Copy the four Azure name servers from the Azure DNS zone overview.
2. Log in to your domain registrar (e.g., [GoDaddy](https://www.godaddy.com)), open the domain's DNS or name server settings, and replace the existing name servers with the Azure name servers.
   * Note: Azure name servers are often shown with a trailing dot (e.g., `ns1-09.azure-dns.com.`). Some registrars reject the trailing dot — remove the trailing dot if required by the registrar.
3. Save the changes and wait for propagation. This can take minutes to hours depending on registrar and DNS caches.

<Frame>
  <img alt="The image shows a browser window with a GoDaddy interface for editing nameservers, indicating an error with invalid TLDs and requesting correct format input." />
</Frame>

After updating the registrar name servers, you can verify public resolution using a public DNS lookup tool (for example, [MXToolbox](https://mxtoolbox.com)) or by performing a normal nslookup from your machine. Once the registrar switch propagates, public queries for `echovisa.com` will be answered by Azure's DNS servers and will return the records you configured in Azure.

<Callout icon="lightbulb">
  Changing the name servers at your registrar is what enables public delegation to Azure. Creating a zone in Azure alone does not make Azure authoritative until you update the registrar settings and propagation completes.
</Callout>

## Adding real records and TTL

To point a hostname to a public IP, create an A record with the IPv4 address. For example, add `web.echovisa.com` with the public IP of a VM. TTL (Time To Live) controls how long resolvers cache the record. A TTL of 3600 is one hour — within that time, caches return the cached value and will not re-query authoritative servers until the TTL expires.

<Frame>
  <img alt="The image shows a Microsoft Azure DNS management interface where a user is adding a DNS record set for the domain echovisa.com. Various DNS record types, such as A, AAAA, CNAME, and MX, are listed for selection." />
</Frame>

After adding the A record and after delegation completes, public lookups will resolve to the IP you configured in Azure. You can confirm with public lookup tools or a standard nslookup from your machine (no special server selection required once delegation is in place).

<Frame>
  <img alt="The image shows a Microsoft Azure DNS management page for the domain &#x22;echovisa.com,&#x22; displaying details of DNS record sets like NS and SOA records." />
</Frame>

Once delegation is complete, you manage all DNS records for the domain from the Azure DNS zone — you no longer need to edit DNS records at the registrar.

## Internal-only (private) domains

If you need DNS records that are accessible only within an Azure virtual network or your private network, use private DNS zones in Azure. Private DNS zones provide name resolution for resources inside the networks you link to the zone and are not visible on the public internet. Do not confuse public DNS zones with private DNS zones; they serve different use cases.

If you want to troubleshoot caching while testing changes, clear local DNS cache on your machine (e.g., `ipconfig /flushdns` on Windows) or lower the TTL temporarily to accelerate propagation.

***

This covers creating Azure DNS zones, record sets, and how and why to delegate your registrar's name servers to Azure so the world queries Azure for your domain.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c82c47ed-c3b3-4aa2-ac47-d0ee418e9797/lesson/430319c4-fb92-4a6a-b963-ffc94e5bec29" />
</CardGroup>
