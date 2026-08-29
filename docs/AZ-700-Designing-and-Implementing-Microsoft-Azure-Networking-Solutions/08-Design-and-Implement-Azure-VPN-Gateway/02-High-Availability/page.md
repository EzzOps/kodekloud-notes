# -------------------------------------------------------------------------------
$resourceGroup = "rg-az700-p2s"
$locationHub = "eastus"
$locationSpoke = "eastus" # Keep same region for simplicity

# Hub VNet
$hubVnetName = "vnet-az700-p2s-hub"
$hubAddressSpace = "10.90.0.0/24" # Single /24 as requested (no subnets yet)

# Spoke VNet
$spokeVnetName = "vnet-az700-p2s-spoke"
$spokeAddressSpace = "10.91.0.0/16"
$spokeSubnetName = "subnet-az700-p2s-spoke-app"
$spokeSubnetPrefix = "10.91.1.0/24"

# VM in Spoke (private only)
$vmName = "vm-az700-p2s-spoke-app-01"
$nicName = "nic-az700-p2s-spoke-app-01"
$nsgName = "nsg-az700-p2s-spoke-app"

$username = "kodekloud"
$passwordPlain = 'adminP$5w0rd'
$securePassword = ConvertTo-SecureString $passwordPlain -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)
```

What this script does:

* Creates resource group, hub and spoke VNets.
* Creates a VM in the spoke (private-only).
* The intended next steps (not shown) would be: create `GatewaySubnet` in the hub, deploy the VPN gateway into the hub, peer the hub and spoke VNets, and enable gateway transit so the spoke VM can route traffic via the hub gateway (for P2S or S2S testing).

## Creating a VPN gateway from the Azure portal

Steps (concise):

1. Search for "Virtual network gateways" and click Create.
2. Choose subscription and resource group.
3. Enter gateway name (e.g., `VPN-GW-AZ700`) and region (must match the VNet region).
4. Gateway type: `VPN`.
5. VPN type: `Route-based`.
6. SKU: choose appropriate SKU (e.g., `VpnGw1` for lab/testing).
7. Virtual network: select the hub VNet that contains `GatewaySubnet`. If you haven't created `GatewaySubnet`, the portal can propose creating one, but it may allocate a large CIDR—manual creation is preferable.
8. Public IP address: create a new public IP resource.
9. Active-active: enable only if you have matching on-premises dual-IP configuration.
10. BGP: enable if you require route-based dynamic routing.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface where a user is configuring settings to create a virtual network gateway." />
</Frame>

If you did not create the `GatewaySubnet` manually, the portal can create it for you. To avoid unintentionally large allocations, create the subnet in advance and use a `/27` (or larger) so you preserve space for other hub services.

### Walkthrough: add GatewaySubnet manually

1. Go to the hub virtual network in the portal.
2. Open Subnets -> Add.
3. For the subnet name enter `GatewaySubnet` (or choose Purpose = GatewaySubnet to set the name automatically).
4. Assign an address range (for example a `/27` like `10.90.0.32/27` depending on your addressing).
5. Save the subnet.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface where a user is adding a new subnet to a virtual network. Various configuration options are displayed, including IP address spaces for both IPv4 and IPv6." />
</Frame>

Once `GatewaySubnet` exists, go back to Virtual Network Gateways -> Create and select the hub VNet. The portal will automatically select `GatewaySubnet`. Configure the remaining options (public IP, active-active, BGP, key vault for certificate auth if needed) and click Create.

<Frame>
  <img alt="The image shows the &#x22;Create virtual network gateway&#x22; page on Microsoft Azure, displaying configuration details for a VPN gateway. The validation has passed, and options for basic settings like subscription, region, and gateway type are listed." />
</Frame>

After clicking Create the deployment enters the provisioning phase; monitor the resource group deployment. Expect up to \~45 minutes for completion.

## Next steps after gateway provisioning

* For S2S: create a Local Network Gateway representing the on-premises public IP and address spaces, then create a Connection between the Azure VPN gateway and the Local Network Gateway. Configure on-premises device with matching shared key and tunnel parameters.
* For P2S: configure client address pool, authentication (certificates or Azure AD), and generate/download VPN client profiles for end users.
* For BGP/Route Server integration: enable route-based VPN, set device and ASN values, and configure BGP peering as needed. Refer to the [Azure Route Server documentation](https://learn.microsoft.com/en-us/azure/route-server/) for integration details.
* Test connectivity from on-premises devices and VPN clients to verify routes and access to Azure workloads.

References:

* [Virtual network gateways overview - Azure](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpngateways)
* [Azure VPN Gateway SKUs](https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpngateway#vpn-gateway-skus)
* [Configure point-to-site connections - Azure VPN Gateway](https://learn.microsoft.com/azure/vpn-gateway/point-to-site-about)

This lesson covered the planning and core steps required to deploy an Azure VPN gateway and prepare for S2S/P2S connections.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f28862d8-b736-4ae4-9003-0efa45de8cd9/lesson/e6037e1f-fc88-44e4-9ef9-9540525d9652)


# High Availability

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-VPN-Gateway/High-Availability/page

Explains Azure VPN Gateway high availability options including zone‑redundant, active‑standby and active‑active configurations, deployment considerations and design tips to ensure resilient VPN connectivity.

This lesson explains high-availability options for Azure Virtual Network Gateways and how to design resilient VPN connectivity between Azure and on-premises environments. You’ll learn about zone-redundant deployments, the default active‑standby configuration, and the active‑active configuration — plus practical deployment considerations to avoid single points of failure.

Azure supports zone-redundant virtual network gateways that distribute gateway instances across multiple Availability Zones within a region. In a zone-redundant deployment, if one Availability Zone experiences an outage, an instance in another zone can continue to handle traffic so connections remain available.

<Frame>
  <img alt="The image illustrates a zone-redundant deployment architecture for virtual networks, showing network gateways, instances, virtual machines (VM) across multiple availability zones, and the flow of ingress and egress traffic." />
</Frame>

## Default: Active‑Standby

By default, Azure Virtual Network Gateways use an active‑standby arrangement:

* Two gateway instances are provisioned for redundancy.
* One instance is active and handles traffic.
* The other instance remains in standby, ready to take over if the active instance fails.

When the active instance fails, the standby instance takes over quickly, minimizing downtime. This default configuration provides a simple, reliable high-availability model for most scenarios.

> **lightbulb** Keep in mind: “default” does not mean a single instance — Azure maintains two gateway instances even in active‑standby mode to enable fast failover.

## Active‑Active for higher throughput and resiliency

Active‑active configuration runs both gateway instances actively handling connections and forwarding traffic at the same time. This increases aggregate throughput and improves resiliency by allowing traffic to be balanced across both instances.

<Frame>
  <img alt="The image illustrates high availability options for VPN connections, showing &#x22;Active/Standby&#x22; and &#x22;Active/Active&#x22; configurations with Azure VPN Gateways and on-premise VPN setups." />
</Frame>

## Quick comparison

| High‑availability option |                                             Description | Pros                                   | Cons                                                            | Typical use case                               |
| ------------------------ | ------------------------------------------------------: | -------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------- |
| Zone‑redundant           | Gateway instances distributed across Availability Zones | Protects against zonal outages         | Requires region with AZ support                                 | Regional resiliency for production workloads   |
| Active‑standby (default) |                        One active, one standby instance | Simple failover, minimal configuration | Only one instance handles traffic at a time                     | Most VNet-to-VNet or site-to-site deployments  |
| Active‑active            |                  Both instances active and load traffic | Higher throughput, better resilience   | Requires supported SKU, multiple public IPs, on‑prem redundancy | High-performance, mission‑critical VPN tunnels |

## Deployment considerations for active‑active

* Use a gateway SKU and configuration that support active‑active. See the Azure VPN Gateway documentation for supported SKUs and features: [https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways).
* Active‑active requires multiple public IP addresses so each gateway instance is reachable independently.
* Your on‑premises topology must be resilient to take full advantage of Azure-side redundancy:
  * Ideally have two on‑prem VPN devices (or virtual appliances) so each on‑prem device can establish tunnels to both Azure gateway instances.
  * Typical topology: Gateway1 ↔ OnPrem1, Gateway1 ↔ OnPrem2, Gateway2 ↔ OnPrem1, Gateway2 ↔ OnPrem2.
* Running active‑active in Azure while keeping a single on‑premises VPN device introduces a single point of failure on premises and negates much of the cloud-side redundancy.

> **warning** Important: Active‑active increases resiliency only when both sides of the connection are designed for redundancy. Verify gateway SKU support and provision multiple public IP addresses and on‑prem devices before relying on active‑active for production SLAs.

## Design tips

* Align redundancy goals between cloud and on‑premises: match the number of independent VPN devices and networks you have on‑premises to the redundancy you implement in Azure.
* If you need zonal protection, prefer zone‑redundant gateways in regions that support Availability Zones.
* For throughput-sensitive workloads, evaluate active‑active SKUs and ensure your on‑prem devices support multiple tunnels and load distribution.
* Test failover behavior and routing asymmetry — verify that routes and BGP (if used) are correctly configured to avoid traffic blackholing during failover.

## References

* Azure VPN Gateway overview and SKUs: [https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways)

With these patterns and considerations, you can design VPN connectivity that meets your availability and performance requirements for mission‑critical applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f28862d8-b736-4ae4-9003-0efa45de8cd9/lesson/4a9d85fc-c11f-452b-af39-b10f76f6b0e5)
