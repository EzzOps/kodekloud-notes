# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Networks-with-Site-to-Site-VPN-Connections/Introduction/page

Explains Azure site-to-site VPNs, components, configuration steps, on-prem settings, routing, and troubleshooting to establish secure IPsec IKE route-based connections between datacenters and Azure virtual networks

Welcome to the module: Connecting Networks with Site-to-Site VPN Connections.

This lesson explains what site-to-site (S2S) VPNs are, when to use them, and how to configure them end-to-end between an on‑premises network and an Azure virtual network.

Learning objectives

* Understand what a site-to-site VPN connection is and when to use it.
* Identify the high-level components in an Azure site-to-site VPN deployment.
* Follow step-by-step Azure configuration and typical on‑premises settings to establish a working S2S VPN.

***

## What is a site-to-site VPN?

A site-to-site VPN creates a secure, encrypted IP tunnel between two distinct networks—typically an on-premises datacenter and an Azure virtual network—over the public internet. Traffic that traverses this tunnel is encrypted and integrity-protected, enabling private communication across untrusted networks.

Key scenarios

* Hybrid cloud connectivity between on-premises datacenters and Azure VNets.
* Secure branch-to-branch connectivity over the internet.
* Encrypted IP-level connectivity where ExpressRoute is not required or available.

***

## High-level technical overview

Site-to-site VPNs rely on standard IPsec/IKE protocols and specific Azure resources. Below is a compact reference for the principal components and behaviors.

| Area                            |                                                                                    What it is | Typical Azure/On‑prem examples                           |
| ------------------------------- | --------------------------------------------------------------------------------------------: | -------------------------------------------------------- |
| Encryption & Protocols          |                IPsec for confidentiality and integrity; IKE for key exchange (commonly IKEv2) | `IPsec ESP`, `IKEv2`                                     |
| Azure gateway                   |         Virtual Network Gateway deployed in a dedicated `GatewaySubnet` (route-based for S2S) | Virtual Network Gateway (VPN)                            |
| Azure representation of on-prem |                      Local Network Gateway: public IP and address prefixes (optional BGP ASN) | Local Network Gateway resource                           |
| Connection object               | Links Virtual Network Gateway and Local Network Gateway; sets pre-shared key and routing type | Connection resource with `sharedKey` and `routingWeight` |
| On-premises device              |                            A compatible VPN appliance/server supporting route-based IPsec/IKE | Cisco ASA, Palo Alto, Juniper, Windows RRAS              |
| Routing                         |                      Static routes or BGP to exchange prefixes; no overlapping address spaces | BGP ASN on Local Network Gateway and on-prem router      |
| Common deployment model         |                                              Route-based VPN (uses virtual tunnel interfaces) | Preferred for Azure S2S                                  |

***

## Azure S2S VPN: Step-by-step configuration (high level)

Below is a practical sequence for configuring an Azure site-to-site VPN. Each step includes typical Azure CLI commands as examples. Replace placeholders with your values (wrap them in backticks when used in scripts or docs).

1. Create a resource group (if you don't have one):

```bash theme={null}
az group create --name `RG_NAME` --location `eastus`
```

2. Create a virtual network and subnets (include a `GatewaySubnet`):

```bash theme={null}
az network vnet create \
  --resource-group `RG_NAME` \
  --name `VNetName` \
  --address-prefix `10.1.0.0/16` \
  --subnet-name `default` \
  --subnet-prefix `10.1.0.0/24`

az network vnet subnet create \
  --resource-group `RG_NAME` \
  --vnet-name `VNetName` \
  --name `GatewaySubnet` \
  --address-prefix `10.1.255.0/27`
```

3. Create a public IP for the VPN gateway:

```bash theme={null}
az network public-ip create \
  --resource-group `RG_NAME` \
  --name `VNetGatewayIP` \
  --allocation-method Dynamic
```

4. Create the Virtual Network Gateway (this can take 20–45 minutes):

```bash theme={null}
az network vpn-gateway create \
  --resource-group `RG_NAME` \
  --name `VNetGateway` \
  --public-ip-address `VNetGatewayIP` \
  --vnet `VNetName` \
  --gateway-type Vpn \
  --sku VpnGw1 \
  --vpn-type RouteBased \
  --no-wait
```

5. Create a Local Network Gateway to represent your on-premises site:

```bash theme={null}
az network local-gateway create \
  --resource-group `RG_NAME` \
  --name `OnPremLocalGateway` \
  --gateway-ip-address `203.0.113.10` \
  --local-address-prefixes `10.10.0.0/16` \
  --asn 65010  # optional for BGP
```

6. Create the S2S connection with a pre-shared key (PSK):

```bash theme={null}
az network vpn-connection create \
  --resource-group `RG_NAME` \
  --name `S2SConnection` \
  --vnet-gateway1 `VNetGateway` \
  --local-gateway2 `OnPremLocalGateway` \
  --shared-key `yourPresharedKeyHere` \
  --enable-bgp false
```

Notes:

* For BGP-enabled connections, add the ASN/peer settings and set `--enable-bgp true`.
* A route-based VPN is the standard for Azure S2S; policy-based is limited in features.

***

## On‑premises configuration checklist

Configure your on-prem VPN device to match the Azure gateway parameters:

* Public IP: the device must have a stable public IP known to Azure.
* Pre-shared key: must match `sharedKey` used in the Azure Connection resource.
* IKE version: use IKEv2 when possible.
* Encryption & integrity algorithms: ensure compatibility (e.g., AES256/SHA256).
* Tunnel type: route-based (virtual tunnel interfaces) if using Azure route-based gateways.
* Local network prefixes: configured to advertise/route the on-prem address ranges.
* BGP: if using BGP, configure ASN and peer IPs; ensure BGP timers and MTU are compatible.

Example on-prem parameter summary:

| Parameter                  | Example                |
| -------------------------- | ---------------------- |
| On-prem public IP          | `203.0.113.10`         |
| On-prem private prefix(es) | `10.10.0.0/16`         |
| IKE version                | `IKEv2`                |
| Encryption                 | `AES256`               |
| Integrity                  | `SHA256`               |
| DH group                   | `Group 14`             |
| Tunnel mode                | `Route-based`          |
| Pre-shared key             | `yourPresharedKeyHere` |

***

## Routing considerations

* Avoid overlapping IP address spaces between Azure VNets and on-prem networks.
* Choose static routes for simple topologies or BGP for dynamic route exchange and scale.
* When using BGP, ensure both sides have unique ASNs and compatible BGP neighbors.

***

## Troubleshooting checklist

| Symptom                   | Quick checks                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Tunnel never connects     | Verify public IPs, pre-shared key, IKE/IKEv2 settings and supported algorithms. Check Azure VPN gateway provisioning status. |
| Intermittent connectivity | Check MTU, IP fragmentation, NIC or firewall timeouts, keepalives.                                                           |
| Routes not present        | Validate Local Network Gateway prefixes and BGP peer status (if using BGP).                                                  |
| Overlapping networks      | Confirm there are no overlapping prefixes; rename/readdress or use NAT if unavoidable.                                       |

<Callout icon="lightbulb">
  Configuring site-to-site VPNs is not strictly required for all certification exams, but understanding how the pieces fit together is valuable for real-world deployments and troubleshooting.
</Callout>

<Callout icon="warning">
  Do not use overlapping IP address ranges between Azure and on-premises networks—this is the most common cause of routing failures and inaccessible resources.
</Callout>

***

## Links and references

* Azure Virtual Network Gateway documentation: [https://learn.microsoft.com/azure/vpn-gateway/](https://learn.microsoft.com/azure/vpn-gateway/)
* Azure VPN Gateway troubleshooting: [https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-troubleshoot-azure-to-onprem](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-troubleshoot-azure-to-onprem)
* IPsec/IKE overview: [https://datatracker.ietf.org/doc/html/rfc7296](https://datatracker.ietf.org/doc/html/rfc7296)

Use these resources as authoritative references when designing and troubleshooting Azure site-to-site VPNs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/b93345c7-5af5-4be6-b741-18d26211f13b/lesson/be46d179-56e9-4ae8-b8dd-e55f65277347" />
</CardGroup>
