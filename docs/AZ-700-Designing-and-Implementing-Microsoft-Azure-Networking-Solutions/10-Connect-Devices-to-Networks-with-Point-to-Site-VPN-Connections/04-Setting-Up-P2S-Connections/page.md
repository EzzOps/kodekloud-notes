# Setting Up P2S Connections

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Devices-to-Networks-with-Point-to-Site-VPN-Connections/Setting-Up-P2S-Connections/page

Step-by-step guide to configure Azure Point-to-Site VPN connections, covering VNets, VPN gateway setup, authentication, tunnel protocols, client profile import, and hub and spoke gateway transit.

This guide walks through configuring Point-to-Site (P2S) VPN connections in Azure. The end-to-end process is:

1. Create or reuse a virtual network (VNet) and subnets.
2. Ensure you have a `GatewaySubnet`.
3. Create (or reuse) the VPN gateway.
4. Configure the Point-to-site settings on the VPN gateway.
5. Download and install the VPN client/profile on client devices.

You can reuse an existing VPN gateway that was deployed for Site-to-Site (S2S) — a separate gateway is not required just for P2S. After configuring P2S, download the client profile and import it into the Azure VPN Client or another supported client to connect.

<Frame>
  <img alt="The image illustrates a step-by-step process for setting up site-to-site connections using Azure, starting from creating VNets and subnets to installing a VPN profile on a device." />
</Frame>

Design considerations

* Client address pool: choose a subnet that does not overlap with on-prem or peered VNets.
* Authentication method: certificate-based, Azure Active Directory (Entra ID), or RADIUS.
* Tunnel protocols: OpenVPN, IKEv2, and/or SSTP depending on client support.
* Routing: whether to advertise custom routes or rely on default system routes.

> **lightbulb** You can use certificate-based authentication, [Azure Active Directory (Entra ID)](https://learn.microsoft.com/en-us/azure/active-directory/), or RADIUS for P2S. Choose the method that fits your security requirements. Make sure the client address pool is large enough and does not overlap your on-prem or hub/spoke address spaces.

Step-by-step: configure P2S in the Azure portal

1. Open the VPN gateway resource and select the "Point-to-site configuration" blade.
2. Define the client address pool, select tunnel types, and choose an authentication method.
3. (Optional) Add custom routes to advertise to clients.
4. Save and wait for the configuration to apply (this can take a few minutes).

<Frame>
  <img alt="The image provides instructions for configuring Point-to-Site VPN authentication methods in Microsoft Azure, showing option menus and highlighting steps like navigating to settings and setting the address pool." />
</Frame>

Common configuration values (examples)

* Address pool example: `172.17.0.0/24` — make sure this range has enough IPs for simultaneous clients and doesn't overlap other networks.
* Tunnel types: `OpenVPN`, `IKEv2`, `SSTP` (enable one or more).
* Authentication: `Certificate`, `Azure Active Directory (Entra ID)`, `RADIUS`.

Table: P2S configuration options

|        Setting | Purpose                          | Example / Notes                                |
| -------------: | -------------------------------- | ---------------------------------------------- |
|   Address pool | IPs assigned to P2S clients      | `172.17.0.0/24`                                |
|   Tunnel types | Protocols clients use to connect | `OpenVPN`, `IKEv2`, `SSTP`                     |
| Authentication | How clients authenticate         | `Certificate`, `Azure AD (Entra ID)`, `RADIUS` |
|  Custom routes | Routes advertised to clients     | `10.91.0.0/16` (spoke network)                 |

Azure AD (Entra ID) authentication specifics

If you choose Azure AD as the authentication method for OpenVPN, you must provide tenant and application values in the portal:

* Tenant login URL: for example, `https://login.microsoftonline.com/your-tenant-id`
* Audience and issuer values: obtained from the Microsoft documentation and the Azure AD app registration

Follow the Microsoft guidance for OpenVPN + Azure AD integration: [https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication](https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication)

<Frame>
  <img alt="The image shows a webpage from Microsoft's documentation, detailing how to authorize the Azure VPN application, with various sections and clickable links for different deployment locations." />
</Frame>

Authorize the Azure VPN application for your tenant:

1. Click the link in the documentation and sign in as an admin if required.
2. Consent to the Azure VPN application.
3. Copy the Tenant ID and the audience/issuer values into the portal's P2S fields.

<Frame>
  <img alt="The image shows a Microsoft Azure configuration page for setting up a Point-to-Site VPN with Azure Active Directory authentication. There are details about configuring tenant, audience, and issuer values in the Azure VPN gateway setup." />
</Frame>

Apply and validate

* Save the P2S configuration and wait for it to apply.
* After the setting is applied, download the client profile ZIP from the portal.
* Extract the profile (XML or configuration file) and import it into the Azure VPN Client or your supported VPN client.

<Frame>
  <img alt="The image shows a Microsoft Azure portal with the &#x22;Point-to-site configuration&#x22; settings for a virtual network gateway, detailing options such as tunnel type and Azure Active Directory authentication." />
</Frame>

Import and connect (Azure VPN Client)

1. Open the Azure VPN Client.
2. Use Import to load the profile XML/configuration from the ZIP.
3. The app auto-populates connection properties — click Connect.
4. Authenticate using your chosen method (certificates, Azure AD prompt, or RADIUS credentials).

After connecting the client receives an IP from the address pool (e.g., `172.17.0.2`) and learns the VPN routes advertised by Azure.

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen for configuring a point-to-site VPN, alongside an Azure VPN Client window displaying the connection properties." />
</Frame>

Hub-and-spoke and gateway transit

If your hub VNet hosts the VPN gateway and you want P2S clients to reach spoke VNets, enable gateway transit on the VNet peerings:

1. On the hub --> spoke peering: enable "Allow gateway transit".
2. On the spoke --> hub peering: enable "Use remote gateways".

After enabling gateway transit, disconnect and reconnect your VPN client so it can refresh and receive the new route advertisements. The client route list will then include the peered VNets (for example, `10.91.0.0/16`).

> **warning** Ensure peered VNets' address spaces do not overlap with the P2S client address pool. Overlapping address spaces will prevent proper routing for P2S clients.

<Frame>
  <img alt="The image shows a Microsoft Azure portal with settings for virtual network peering, alongside an Azure VPN Client window displaying connection properties and VPN routes." />
</Frame>

Verify access to internal resources

Once P2S is connected and gateway transit is enabled, you should be able to access private resources in a spoke VNet using their private IP addresses. For example, you can reach an internal web application hosted on a Linux VM in the spoke VNet.

<Frame>
  <img alt="The image shows a Microsoft Azure portal displaying details of a virtual machine named &#x22;vm-az700-p2s-spoke-app-01,&#x22; which is running on Linux (Ubuntu 22.04) with specific subscription and network configuration details." />
</Frame>

Quick checklist before you finish

* Address pool chosen and non-overlapping (`e.g., 172.17.0.0/24`).
* Tunnel protocol(s) enabled for client compatibility.
* Authentication configured and validated (certs, Azure AD, or RADIUS).
* Client profile downloaded, imported, and tested.
* Gateway transit configured if hub-spoke access is required.

References

* Azure VPN Client: [https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-client-v2-windows](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-client-v2-windows)
* OpenVPN + Azure AD integration: [https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication](https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-authentication)

This completes the P2S VPN gateway setup and validation steps.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c5df2cec-e98a-4e4f-ad3a-e20fe745164e/lesson/dba5363c-6d0d-4532-a060-927ca12a0ade)
