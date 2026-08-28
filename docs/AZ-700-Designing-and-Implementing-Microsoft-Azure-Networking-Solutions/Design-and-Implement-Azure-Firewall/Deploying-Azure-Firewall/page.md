# Deploying Azure Firewall

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Firewall/Deploying-Azure-Firewall/page

Guides deploying Azure Firewall in hub and spoke networks, configuring SKUs, subnets, forced tunneling, routing, and comparing capabilities with Network Security Groups

In this lesson you'll learn how to deploy Azure Firewall from the Azure portal, how it fits into a hub‑and‑spoke topology, and when to choose Azure Firewall vs Network Security Groups (NSGs). Before you begin, make sure you have an Azure subscription and an existing resource group to host the firewall.

1. Select the target subscription and the resource group where the firewall will be created.
2. Complete the firewall creation form (name, region, SKU, VNet, address space, public IP, etc.) and deploy.

<Frame>
  <img alt="The image shows a guide for deploying an Azure Firewall, highlighting six steps on the left and a &#x22;Create a firewall&#x22; form on the right. The form includes details like name, region, SKU, virtual network, and address space settings." />
</Frame>

Deployment checklist — portal fields and considerations:

* Firewall name and Azure region.
* SKU selection: Basic, Standard, or Premium (choose based on features required such as TLS inspection and IDPS).
* Management mode: attach a Firewall Policy (recommended) or use legacy rules.
* Virtual network: select the VNet that will host the firewall (typically a hub VNet).
* Address space and a dedicated subnet named `AzureFirewallSubnet` (details below).
* Public IP assignment: required for DNAT (inbound) and SNAT (outbound) translations as needed.
* Optional forced tunneling configuration if you need to forward outbound traffic to on‑premises appliances using UDRs or Azure Firewall Manager.

<Callout icon="lightbulb">
  The firewall must be deployed in a dedicated subnet named exactly `AzureFirewallSubnet`. Ensure the subnet is sized appropriately (typically a /26 or larger) to accommodate firewall scaling and features.
</Callout>

<Callout icon="warning">
  Forced tunneling redirects outbound traffic to on‑premises systems and can affect failover, latency, and routing complexity. Validate route priorities and next hops (UDRs) before enabling in production.
</Callout>

When to use forced tunneling

* Use forced tunneling when you must inspect or route all outbound traffic through on‑premises firewalls or centralized inspection points.
* Implement forced tunneling via user‑defined routes (UDRs) in spoke route tables or centrally using Azure Firewall Manager to automate route distribution.

Hub‑and‑spoke topology (centralized inspection)
The hub‑and‑spoke model places shared services—including Azure Firewall—into a central hub VNet. Application workloads reside in spoke VNets that peer with the hub. Traffic destined for the internet, other spokes, or on‑premises can be routed through the hub for inspection and policy enforcement.

<Frame>
  <img alt="The image illustrates a Hub-Spoke network topology for deploying Azure Firewall, featuring components like Azure Bastion, Azure Monitor, VPN Gateway, and multiple virtual machines within network diagrams." />
</Frame>

How this architecture works (high level):

* Azure Firewall runs in the hub VNet and acts as the centralized inspection and policy enforcement point.
* Spoke VNets peer with the hub. Spoke UDRs send internet and cross‑spoke traffic to the firewall's private IP with next hop set to `Virtual Appliance`. The firewall inspects and forwards traffic according to configured rules and policies.
* On‑premises connectivity (VPN Gateway or ExpressRoute) terminates in the hub so on‑premises traffic can also be inspected by the firewall.
* Scaling or adding spokes typically requires only peering and UDR updates—no reconfiguration of the firewall core.

Testing tip: For validation, you can route traffic from spokes to a packet‑capture VM (via UDR) to observe flow and behavior. In production, replace the test VM with Azure Firewall for centralized, application‑aware protection.

Azure Firewall vs NSG — feature comparison
Both NSGs and Azure Firewall filter traffic, but they operate at different layers and serve different purposes. Use the table below to choose the right tool for each requirement.

| Feature / Use Case                     |                                                       Azure Firewall |                                  Network Security Group (NSG) |
| -------------------------------------- | -------------------------------------------------------------------: | ------------------------------------------------------------: |
| Protocol & port filtering              |             Yes — supports TCP, UDP, and application‑aware filtering |              Yes — TCP, UDP, and Any (ICMP handled via `Any`) |
| Application / FQDN filtering (Layer 7) |                                Yes — application rules and FQDN tags |                                                            No |
| Centralized policy & management        |                        Yes — Firewall Policy, Azure Firewall Manager |                   No — NSGs are applied at subnet / NIC scope |
| SNAT (outbound NAT)                    |                                                                  Yes |                                                            No |
| DNAT (inbound NAT)                     |                                                                  Yes |                                                            No |
| Service tags support                   |                                                                  Yes |                                                           Yes |
| Logging & telemetry                    | Rich firewall telemetry: application rules, threats, FQDN resolution |                             Basic flow logs via NSG Flow Logs |
| Typical use case                       |  Centralized, application‑aware inspection, NAT, threat intelligence | Lightweight, high‑performance subnet/NIC-level access control |

Useful links and references

* Azure Firewall documentation: [https://learn.microsoft.com/azure/firewall](https://learn.microsoft.com/azure/firewall)
* Network Security Groups (NSG) documentation: [https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
* Azure Firewall Manager and forced tunneling: [https://learn.microsoft.com/azure/firewall-manager](https://learn.microsoft.com/azure/firewall-manager)

<Frame>
  <img alt="The image compares Azure Firewall and NSGs in terms of protocol-based traffic filtering, service tags support, application FQDN tags support, integration with Azure Monitor, and SNAT/DNAT support, indicating capabilities with checkmarks." />
</Frame>

Summary and recommended best practices

* Deploy Azure Firewall into a hub VNet using a dedicated `AzureFirewallSubnet`.
* Choose the SKU (Basic, Standard, Premium) based on required features (TLS inspection, IDPS, etc.) and attach a Firewall Policy whenever possible for centralized management.
* Route spoke outbound and cross‑spoke traffic to the firewall via UDRs with next hop type `Virtual Appliance` to ensure inspection.
* Use NSGs to provide fast, distributed packet‑level filtering at the subnet/NIC level; use Azure Firewall for centralized, application‑aware filtering, NAT, and advanced logging.
* Test routing and policy behavior in a non‑production environment before enabling forced tunneling or complex route designs.

Next steps

* Review the Azure Firewall quickstart guides and portal walkthroughs: [https://learn.microsoft.com/azure/firewall/quick-start](https://learn.microsoft.com/azure/firewall/quick-start)
* Plan your hub address space and size `AzureFirewallSubnet` to at least `/26` to allow for scale and resilience.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c48f6bd6-195c-4405-9c9f-614ed7beb371/lesson/6351f535-6682-4f74-909d-037eeda846b9" />
</CardGroup>
