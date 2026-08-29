# Point to Site Protocols

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Connect-Devices-to-Networks-with-Point-to-Site-VPN-Connections/Point-to-Site-Protocols/page

Overview of Azure Point-to-Site VPN protocols OpenVPN, SSTP, and IKEv2 with guidance on selecting based on client platforms, network restrictions, and connectivity requirements

In this lesson we break down the VPN protocols supported by Azure for Point-to-Site (P2S) connections. Azure supports multiple P2S protocols so you can accommodate varied client platforms, network restrictions, and security requirements—choosing the right protocol helps ensure connectivity, performance, and compliance.

## OpenVPN

OpenVPN is a widely used open-source VPN protocol available on Windows, macOS, Linux, Android, and iOS. It relies on TLS for authentication and can run over either UDP or TCP, giving you flexibility for performance and firewall traversal. OpenVPN supports modern cipher suites and strong encryption, making it a solid choice for organizations with stringent security needs.

Typical steps when using OpenVPN with Azure P2S:

* Enable OpenVPN protocol support on the Azure VPN Gateway.
* Generate and distribute the VPN client configuration (Azure can provide a client package).
* Configure the VPN client address pool so connected devices receive private IP addresses from your virtual network.

Useful links:

* OpenVPN project: [https://openvpn.net/](https://openvpn.net/)
* Azure P2S documentation: [https://learn.microsoft.com/azure/vpn-gateway/point-to-site-about](https://learn.microsoft.com/azure/vpn-gateway/point-to-site-about)

## SSTP (Secure Socket Tunneling Protocol)

SSTP is a Microsoft-developed VPN protocol with native support on Windows clients. It tunnels VPN traffic over TLS on TCP port `443` (HTTPS), which helps it traverse firewalls and web proxies that block non‑HTTPS traffic.

Because SSTP uses standard HTTPS/TLS semantics, it is often the most reliable fallback for users connecting from highly restrictive networks or environments that block other VPN ports. Native Windows support also minimizes client setup for Windows users.

<Frame>
  <img alt="The image illustrates the Point-to-Site (P2S) Protocols, focusing on the Secure Socket Tunneling Protocol (SSTP) with a diagram showing the VPN gateway, client addresses, and supported operating systems." />
</Frame>

This makes SSTP a practical choice for remote users behind corporate firewalls or web proxies where other VPN protocols may fail.

## IKEv2 (Internet Key Exchange v2)

IKEv2 is a modern, standards-based VPN protocol that negotiates security associations and encryption keys. It is valued for speed, stability, and mobility features:

* Mobility and multihoming (MOBIKE) let clients maintain or re‑establish sessions when switching networks (for example, Wi‑Fi → cellular).
* Uses UDP port `500` for IKE and UDP port `4500` when NAT traversal (NAT‑T) is required.
* Provides fast reconnects and resilient behavior on unstable networks.

IKEv2 is especially well suited for mobile users or scenarios where connection continuity and quick recovery are critical.

<Frame>
  <img alt="The image is a diagram explaining the Point-to-Site IKEv2 VPN with a VPN Gateway, showing different VPN client addresses and their associated devices and platforms." />
</Frame>

## Protocol comparison

| Protocol | Transport         |              Default ports | Platform support                                     | Best use case                                             |
| -------- | ----------------- | -------------------------: | ---------------------------------------------------- | --------------------------------------------------------- |
| OpenVPN  | UDP or TCP (TLS)  | `UDP`/`TCP` (configurable) | Cross‑platform (Windows, macOS, Linux, iOS, Android) | Broad device support and strict security requirements     |
| SSTP     | TCP (TLS)         |                  `TCP 443` | Native Windows; limited on other platforms           | Windows-only or extremely restrictive networks/firewalls  |
| IKEv2    | UDP (IKE / NAT‑T) |      `UDP 500`, `UDP 4500` | Strong on modern OSes and mobile platforms           | Mobile/roaming users needing fast reconnect and stability |

## Summary

Azure supports OpenVPN, SSTP, and IKEv2 for Point-to-Site VPNs. Choose based on client platforms, network restrictions, and the connectivity behavior you need:

* OpenVPN: best cross‑platform support and strong security; flexible transport (`UDP` or `TCP`).
* SSTP: native Windows support and excellent firewall/proxy traversal via `TCP 443`.
* IKEv2: optimal for mobile/roaming users due to MOBIKE and fast reconnection.

> **lightbulb** Select the protocol that aligns with your client OS footprint and network constraints. Use OpenVPN for broad device coverage, SSTP for Windows environments with strict proxies/firewalls, and IKEv2 for mobile and unstable-network scenarios.

Links and references

* Azure VPN Gateway (Point-to-Site): [https://learn.microsoft.com/azure/vpn-gateway/point-to-site-about](https://learn.microsoft.com/azure/vpn-gateway/point-to-site-about)
* OpenVPN: [https://openvpn.net/](https://openvpn.net/)
* IKEv2 overview and MOBIKE: [https://tools.ietf.org/html/rfc5723](https://tools.ietf.org/html/rfc5723)

Next steps

* Review your client OS mix and network constraints.
* Pilot the preferred protocol with a subset of users.
* Verify gateway configuration, client address pool, and required ports are available through your network perimeter.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c5df2cec-e98a-4e4f-ad3a-e20fe745164e/lesson/8dd53173-744e-42e1-ac15-3357597cc8f5)
