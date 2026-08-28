# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-VPN-Gateway/Introduction/page

Guidance for planning, deploying, configuring, and troubleshooting Azure VPN Gateway connectivity including subnet, SKUs, routing, security, verification, and high availability.

Design and implement an Azure VPN Gateway

This lesson walks through planning, deploying, and troubleshooting Azure VPN Gateway connectivity. Follow the sequence below to ensure a robust, secure, and highly available VPN deployment.

Core objectives

* Plan gateway scope and capacity.
* Create the required GatewaySubnet.
* Configure addressing, routing, and security.
* Choose the appropriate gateway type and SKU.
* Configure the Local Network Gateway and on-premises device.
* Deploy the VPN connection and validate end-to-end connectivity.
* Troubleshoot and design for resiliency.

Planning checklist

* Identify which resources need connectivity: on-premises networks, other VNets, or individual clients.
* Estimate expected throughput and number of tunnels.
* Define required security posture: encryption, authentication (PSK vs certificates), and isolation.
* Establish availability and resiliency requirements: zone-redundant SKUs, active-active, or hybrid failover.

<Frame>
  <img alt="The image lists four learning objectives related to VPN gateways, including planning, creating a subnet, configuration requirements, and types of VPN gateways. It's titled &#x22;Learning Objectives&#x22; with a gradient background on the left." />
</Frame>

GatewaySubnet: required and specific

Create a dedicated subnet named `GatewaySubnet` inside the VNet that will host the VPN Gateway. Azure enforces the name and expects adequate IP space for the chosen SKU and number of tunnels. Typically a `/27` or larger is recommended for production; smaller sizes may limit functionality.

Example: create GatewaySubnet with Azure CLI

```bash theme={null}
az network vnet subnet create \
  --resource-group MyResourceGroup \
  --vnet-name MyVNet \
  --name GatewaySubnet \
  --address-prefixes 10.1.255.0/27
```

Configuration requirements

* Address spaces: ensure no overlap with on-premises networks. Plan routing and address prefixes for all connected sites.
* Routing: decide between Azure system routes and custom route tables; plan how to propagate BGP routes if using dynamic routing.
* NSGs and firewalls: GatewaySubnet should not contain NSG rules that block gateway traffic (UDP 500/4500, ESP, IKE, etc.). Place segmentation and inspection perimeters away from GatewaySubnet.

<Callout icon="warning">
  Avoid applying restrictive Network Security Group (NSG) rules directly to `GatewaySubnet`. Doing so can block required VPN and management traffic and prevent gateway deployment or tunnel establishment.
</Callout>

VPN gateway types and when to use them

| Gateway type                                      | When to use                                           | Key notes                                              |
| ------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| Route-based (VNet-to-VNet, Site-to-Site with BGP) | Dynamic routing, multiple remote subnets, BGP support | Supports active-active, BGP, and modern scenarios      |
| Policy-based (static IPsec)                       | Simple site-to-site with fixed IPSEC policies         | Limited scalability and no BGP; used for older devices |

Choosing a SKU and generation

Select a SKU that matches your throughput, number of tunnels, and feature requirements (BGP, active-active, zone redundancy). Common SKUs: `VpnGw1`, `VpnGw2`, `VpnGw3`, and the Basic/older families. Always reference the Azure VPN Gateway SKUs documentation for detailed limits and pricing.

Local Network Gateway and on-premises device

A Local Network Gateway is an Azure resource that represents the remote VPN endpoint. It typically contains:

* The public IP address of the on-premises VPN device.
* The address prefixes (on-premises subnets) advertised to Azure.

Configure the on-premises device to match:

* IKE/IKEv2 and IPsec parameters (encryption, hashing).
* Authentication method (pre-shared key or certificates).
* Route advertisement (static routes or BGP).

Creating the VPN connection

Select the connection type:

* Site-to-Site (IPsec) for traditional on-premises to Azure links.
* VNet-to-VNet for peering VNets via VPN gateway.
* Point-to-Site (S2C) for individual clients.

Example: check connection status with Azure CLI

```bash theme={null}
az network vpn-connection show \
  --resource-group MyResourceGroup \
  --name MyVpnConnection \
  --query "connectionStatus"
```

<Frame>
  <img alt="The image lists learning objectives related to VPN configuration, including choosing a gateway SKU, creating a network gateway, configuring a VPN device, and creating a VPN connection." />
</Frame>

Verification and troubleshooting

Use these steps and tools to validate and troubleshoot the VPN:

* Azure portal: Monitor VPN Gateway -> Connections for tunnel status.
* Azure Network Watcher: use VPN diagnostics, packet capture, and topology.
* Logs and metrics: review gateway logs, connection metrics, and IKE/IPsec counters.
* Routing validation: confirm on-premises and Azure route tables and BGP advertisements.
* End-to-end tests: ping, traceroute, and application-level checks from both ends.

Useful CLI examples

```bash theme={null}
