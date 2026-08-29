# Point to Site Authentication Methods

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Devices-to-Networks-with-Point-to-Site-VPN-Connections/Point-to-Site-Authentication-Methods/page

Overview of point-to-site VPN authentication methods, comparing certificate-based, Microsoft Entra ID, and Active Directory RADIUS approaches with deployment steps, benefits, and trade-offs.

Point-to-site (P2S) VPNs let individual devices connect securely to a virtual network. Choosing the right P2S authentication method affects security, manageability, and user experience. This article explains the most common approaches—certificate-based authentication, Microsoft Entra ID authentication, and Active Directory domain authentication via RADIUS—provides deployment steps, and compares trade-offs to help you pick the right option.

## Overview

* Certificate-based authentication: Strong device identity using client certificates signed by a trusted root CA.
* Microsoft Entra ID authentication: Cloud-native user authentication with MFA and Conditional Access integration.
* Active Directory domain authentication (RADIUS): Reuse on-premises AD credentials, ideal for hybrid environments.

<Frame>
  <img alt="The image is a diagram outlining point-to-site authentication methods, showing a network setup involving Azure VPN, on-premises VPN, and integration with a RADIUS server for AD domain authentication." />
</Frame>

## 1) Certificate-based authentication

Certificate-based authentication requires each client device to present a valid client certificate during the VPN handshake. The certificate must be issued (signed) by a root certificate authority (CA) that the VPN gateway trusts.

Typical deployment steps:

1. Generate or obtain a root CA certificate (enterprise PKI or a public CA).
2. Upload the public root certificate to the Azure VPN configuration so the gateway trusts client certificates signed by that root.
3. Issue client certificates signed by the root CA and install them on devices that require VPN access.

Benefits:

* Strong device-level trust and reduced reliance on user passwords.
* Works well when you control the endpoint devices (e.g., corporate-owned laptops).

Operational considerations:

* Certificate issuance, revocation, and lifecycle management add operational overhead.
* Secure storage and distribution of private keys are critical.

> **warning** If client certificate private keys are not properly protected, device compromise can allow unauthorized VPN access. Use hardware-backed keystores or HSMs where possible and maintain a clear revocation process.

## 2) Microsoft Entra ID authentication

Microsoft Entra ID (formerly Azure AD) provides a modern, user-centric authentication flow for P2S VPNs. Users sign in with their Entra ID credentials, enabling integration with Conditional Access, multi-factor authentication (MFA), and centralized identity policies.

Key benefits:

* Integrates with Conditional Access and MFA for stronger, policy-driven security.
* Familiar user experience: sign in with work accounts.
* Centralized administration through Entra ID.

Note about protocol support:

> **lightbulb** Entra ID authentication for P2S is supported for specific VPN client protocol(s). Confirm current protocol compatibility in Azure documentation before deploying Entra ID for your P2S configuration.

Why choose Entra ID:

* Best for cloud-first organizations that want to leverage the identity platform for access controls.
* Lightweight for end users compared to certificate distribution.

## 3) Active Directory domain authentication (via RADIUS)

Active Directory domain authentication uses on-premises AD credentials and a RADIUS server (for example, Microsoft Network Policy Server or third-party RADIUS) to validate user logins.

Authentication flow:

1. VPN gateway forwards user credentials to the configured RADIUS server.
2. The RADIUS server validates credentials against Active Directory Domain Services.
3. RADIUS returns accept/deny to the VPN gateway, which grants or denies the session.

Benefits:

* Reuses existing AD usernames and passwords and existing network access policies.
* Ideal for hybrid setups where on-prem authentication must remain authoritative.

Operational considerations:

* Requires a highly available RADIUS infrastructure and secure connectivity between Azure and your RADIUS servers.
* Consider latency and reachability when RADIUS servers are on-premises.

## Comparison table

| Method             | Best for                  | Pros                                                           | Cons                                                     | Notes                                                         |
| ------------------ | ------------------------- | -------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Certificate-based  | Corporate-managed devices | Strong device identity; credential-less connection             | Operational overhead for issuing/revoking certificates   | Use when you control endpoints and need device-level trust    |
| Microsoft Entra ID | Cloud-first organizations | Integrates with MFA & Conditional Access; centralized policies | Requires supported VPN protocol and Entra ID integration | Check Azure docs for protocol support and client requirements |
| AD domain (RADIUS) | Hybrid environments       | Reuse AD credentials and policies                              | Requires RADIUS infrastructure and secure connectivity   | Good when your environment depends on on-prem AD              |

## Recommended selection guidance

* Choose certificate-based authentication if device identity and credential-less access are primary goals and you can operate certificate lifecycle processes.
* Choose Microsoft Entra ID when you want cloud-native authentication, MFA, and Conditional Access applied to VPN sessions.
* Choose AD domain authentication via RADIUS to reuse on-prem credentials and align VPN access with existing AD policies in hybrid deployments.

## Further resources

* Azure VPN P2S documentation: [https://learn.microsoft.com/azure/vpn-gateway/point-to-site-overview](https://learn.microsoft.com/azure/vpn-gateway/point-to-site-overview)
* Microsoft Entra ID (Azure AD) documentation: [https://learn.microsoft.com/azure/active-directory/](https://learn.microsoft.com/azure/active-directory/)
* Network Policy Server (NPS) and RADIUS guidance: [https://learn.microsoft.com/windows-server/networking/technologies/nps/nps-top](https://learn.microsoft.com/windows-server/networking/technologies/nps/nps-top)

This concludes the overview of point-to-site authentication methods.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c5df2cec-e98a-4e4f-ad3a-e20fe745164e/lesson/e9e72e51-f89d-4598-8462-48872b1edf5c)
