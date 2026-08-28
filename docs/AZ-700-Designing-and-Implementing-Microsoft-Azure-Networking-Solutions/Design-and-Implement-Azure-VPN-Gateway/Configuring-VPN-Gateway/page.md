# Configuring VPN Gateway

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-VPN-Gateway/Configuring-VPN-Gateway/page

Guide to planning and deploying an Azure VPN gateway, covering GatewaySubnet requirements, gateway creation options, portal steps, and a hub-spoke lab for P2S and S2S testing.

Welcome. In this lesson you will learn how to plan and deploy an Azure VPN gateway. This guide covers the required subnet, gateway creation options, portal steps, and a small lab script example to build a hub-spoke topology for testing point-to-site (P2S) or site-to-site (S2S) connections.

At a high level, the sequence is:

1. Create a dedicated subnet named exactly `GatewaySubnet` inside the virtual network where the gateway will be deployed.
2. Deploy the VPN gateway resource into that virtual network.
3. Configure the connection type you need (site-to-site or point-to-site) and any additional settings such as BGP or active-active mode.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Configuring VPN Gateway&#x22; depicting two steps: &#x22;Create Gateway Subnet&#x22; and &#x22;Create VPN Gateway.&#x22;" />
</Frame>

Key differences by connection type:

* Site-to-site (S2S): Create a Local Network Gateway to represent the on-premises address space and public IP, then create a Connection between the Azure VPN gateway and the Local Network Gateway.
* Point-to-site (P2S): Configure client address pools, authentication method (certificate or Azure AD), and VPN client configuration.

Detailed S2S and P2S setup (tunnel parameters, device configuration, and client packages) are outside the scope of this lesson. Treat this guide as the core steps to prepare and create the VPN gateway.

## Start with the GatewaySubnet

The VPN gateway must be placed in a subnet named exactly `GatewaySubnet`. Azure requires this exact name to allocate and configure the gateway resources. Keep this subnet dedicated to the gateway—do not deploy other workloads in it.

GatewaySubnet guidelines:

| Property  | Recommendation                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------- |
| Name      | `GatewaySubnet` (exact match)                                                                                          |
| Size      | At least a `/27` (Microsoft recommends this for scaling and multiple gateway instances)                                |
| NSG / UDR | Do not apply Network Security Groups (NSGs) or User-Defined Routes (UDRs) to this subnet; Azure manages required rules |
| Use       | Dedicated to the VPN gateway only                                                                                      |

<Callout icon="lightbulb">
  Always name the subnet exactly `GatewaySubnet`. If the name is different, Azure cannot place the gateway and creation will fail.
</Callout>

<Frame>
  <img alt="The image provides instructions for creating a Gateway Subnet for a VPN gateway, highlighting subnet naming, purpose, size, and configuration requirements. It includes a form for adding a subnet with fields for name, address range, and related settings." />
</Frame>

## Creating the VPN gateway — options and considerations

When you create the VPN gateway resource, choose options based on your topology, throughput, and feature requirements:

| Option          | Notes / Recommendation                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| VPN type        | Use `Route-based` unless you require legacy `Policy-based` VPNs. Route-based supports dynamic routing (BGP) and modern scenarios.                                              |
| SKU             | Gateway SKUs (e.g., `VpnGw1`, `VpnGw2`, `VpnGw3`, etc.) determine throughput, maximum tunnels, and available features. Choose according to expected load and connection count. |
| Virtual network | The gateway must be created in the VNet that contains the `GatewaySubnet`.                                                                                                     |
| Public IP       | Assign a public IP to the gateway; this is the internet endpoint for S2S tunnels or P2S clients.                                                                               |
| BGP             | Enable BGP if you need dynamic route exchange between on-premises and Azure.                                                                                                   |
| Active-active   | Enable for high-availability scenarios requiring two simultaneous external IP addresses; requires matching on-premises configuration.                                          |

Notes:

* If you plan to use Azure Route Server, the VPN must be route-based. See Azure Route Server docs for integration details.
* SKU selection affects available features (for example, BGP and active-active support vary by SKU). Reference the Azure VPN Gateway SKUs documentation when choosing.

<Frame>
  <img alt="The image is a guide for creating a VPN gateway, detailing aspects such as VPN type, SKU impact, VNet association, and public IP requirements, alongside a virtual network gateway creation form." />
</Frame>

## Provisioning time and deployment plan

Provisioning a virtual network gateway can take time. Plan accordingly.

<Callout icon="warning">
  Creating a virtual network gateway can take up to 45 minutes. Do not retry or change configuration mid-provisioning—this can cause failures or require cleanup.
</Callout>

Tips:

* Start gateway creation during a maintenance window.
* Avoid cancelling and recreating mid-deploy; repeated attempts may require support and cleanup.
* Monitor the Deployment in the resource group for progress and failure details.

## Summary of the core steps

To deploy a VPN gateway:

* Plan the hub VNet address space and reserve a `GatewaySubnet`.
* Create `GatewaySubnet` with at least a `/27` prefix and keep it dedicated.
* Deploy the VPN gateway into the VNet containing the `GatewaySubnet`.
* Select appropriate VPN type (route-based), SKU, and public IP configuration.
* Allow provisioning time; after creation, configure S2S or P2S connections.

## Practical lab example (hub-spoke topology with PowerShell)

This example creates a hub VNet (for the VPN gateway), a spoke VNet (for workloads), and a test VM in the spoke. The hub will host the gateway and be peered to the spoke to enable gateway transit.

Corrected PowerShell snippet (note: use single quotes for plaintext password to avoid variable expansion):

```powershell theme={null}
