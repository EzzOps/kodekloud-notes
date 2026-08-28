# Configure DNS Settings Inside a VNet

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Name-Resolution-for-Azure-Virtual-Network/Configure-DNS-Settings-Inside-a-VNet/page

Guide to configuring Azure VNet DNS using Private DNS zones, virtual network links, DNS servers and forwarding, with security, hub and spoke patterns, and testing examples

Configuring DNS inside an Azure virtual network (VNet) is essential for enterprise and hybrid environments that require custom name resolution. This guide shows recommended architectures, Azure Private DNS zone usage, and step‑by‑step examples to get a simple test environment running.

At a high level, the diagram below illustrates two Azure VNets (VNet1 and VNet2), each hosting VMs and a DNS server, plus an on‑premises DNS. DNS queries from on‑premises and between VNets can be forwarded to the appropriate DNS server or to Azure's platform resolver at `168.63.129.16` when required.

<Frame>
  <img alt="The image depicts a network diagram for configuring DNS settings inside a virtual network (VNet), illustrating DNS queries flow between on-premises, DNS servers, and virtual machines across two VNets. It includes recommendations for secure DNS setup, such as enabling recursive resolution and securing the DNS server from the internet." />
</Frame>

Key takeaways from the architecture diagram:

* Each VNet can host its own DNS server (for example `10.1.0.4` in VNet1 and `10.2.0.4` in VNet2). VMs inside that VNet point to the local DNS server for resolution.
* If a DNS server cannot resolve a name locally, it forwards queries across peering/site‑to‑site/ExpressRoute links or to Azure's platform DNS resolver at `168.63.129.16` if configured.
* Ensure appropriate firewall/NSG rules for DNS (UDP/TCP port `53`) and that recursive resolution or forwarders are configured.
* Do not expose internal DNS servers directly to the public internet; always place them behind network controls.

<Callout icon="lightbulb">
  Design your DNS for recursive resolution using forwarders or direct recursion. Use hub‑and‑spoke or centralized DNS patterns: place DNS servers in a hub VNet and have spokes forward queries (via peering or conditional forwarders). Link the Private DNS zone to the hub instead of linking every spoke directly.
</Callout>

Essentials for a working custom DNS deployment

* DNS servers must have records or forwarders for all relevant zones (private zones, conditional forwarders).
* Allow UDP/TCP port `53` between clients, DNS servers, and across networks where resolution must traverse.
* Secure internal DNS servers with NSGs, firewalls, or private endpoints — do not publish them to the public internet.

DNS traffic and port summary:

| Protocol | Port | Use case                                                                 |
| -------- | ---- | ------------------------------------------------------------------------ |
| UDP      | `53` | Standard DNS queries and responses (most lookups)                        |
| TCP      | `53` | Zone transfers, large responses and fallbacks                            |
| —        | —    | Ensure NSGs and firewalls permit both directions where DNS must traverse |

<Callout icon="warning">
  Do not publish internal DNS servers directly to the internet. Restrict access using NSGs, firewalls, or private connectivity and use Azure platform DNS (`168.63.129.16`) where appropriate.
</Callout>

Walkthrough: create a simple test environment
This walkthrough creates a minimal foundation: resource group, two VNets with subnets, and an example public IP. Extend this to add NICs and VMs as needed.

PowerShell example to create resource group, two VNets and subnets:

```powershell theme={null}
