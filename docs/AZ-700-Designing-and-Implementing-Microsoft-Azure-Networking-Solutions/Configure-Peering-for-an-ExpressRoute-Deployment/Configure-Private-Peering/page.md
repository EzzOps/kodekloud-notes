# Configure Private Peering

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Peering-for-an-ExpressRoute-Deployment/Configure-Private-Peering/page

Guide to configuring ExpressRoute private peering in Azure portal, detailing BGP /30 subnets VLAN ID ASN peer IPs MD5 and Global Reach and mirroring settings on on-prem routers

Configuring ExpressRoute private peering creates a private, high-throughput connection between your on-premises network and Azure virtual networks. This guide explains the fields you enter in the Azure portal (Private peering tab) after an ExpressRoute circuit is created and how to mirror those settings on your on-premises routers.

You can learn more about the feature on the Microsoft docs: [ExpressRoute private peering](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-howto-private-peering). To access the configuration, open the ExpressRoute circuit in the [Azure portal](https://portal.azure.com) and select the Private peering tab.

Below is an example of the portal interface and where you enter the private peering details:

<Frame>
  <img alt="The image shows a configuration interface for &#x22;Private peering&#x22; with settings related to subnets, VLAN ID, and ASN details on the right. On the left, there are labeled sections for different networking components like Non-VNet Subnets and BGP Advertising." />
</Frame>

Key configuration items — quick reference

| Field                             | What it controls                                                            | Example / Notes                                                                                                                                                                            |
| --------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Primary and secondary /30 subnets | IP addressing for the two BGP peering sessions to Microsoft                 | Each `/30` gives two usable IPs (one for your router, one for Microsoft). Must not overlap your VNets or on-prem prefixes.                                                                 |
| VLAN ID                           | Layer 2 tag for the physical/virtual link                                   | Must match the VLAN configured on your edge device and what the connectivity provider expects.                                                                                             |
| ASN (Autonomous System Number)    | Your on-prem ASN used for BGP session establishment                         | Use your assigned ASN or the provider's ASN if they manage routing.                                                                                                                        |
| BGP peer IP addresses             | IPs from the `/30` subnets used for the BGP neighbors                       | Configure the corresponding addresses on your on-prem router interfaces.                                                                                                                   |
| Route advertisement               | Which on-prem prefixes you will advertise to Azure (and receive from Azure) | Ensure intended prefixes are advertised; avoid leaking overlapping or private ranges incorrectly.                                                                                          |
| MD5 authentication (optional)     | BGP MD5 password to authenticate BGP peers                                  | Recommended for added security to prevent unauthorized BGP sessions.                                                                                                                       |
| Global Reach (optional)           | Enables Azure backbone connectivity between your on-prem sites              | See [ExpressRoute Global Reach](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-global-reach-overview) for multi-circuit connectivity across Microsoft’s global network. |

Detailed explanation of each configuration item

* Primary and secondary /30 subnets
  * Azure requires two distinct `/30` point-to-point ranges: one for the primary BGP session and one for the secondary session. Each `/30` contains exactly two usable addresses—one assigned to your on-prem router and the other to Microsoft’s edge router. Plan these subnets so they do not overlap any VNet or on-premises networks you will advertise.

* VLAN ID
  * The VLAN ID is the 802.1Q tag used on the Layer 2 segment between your edge router and Microsoft’s edge. Ensure the VLAN ID entered in the portal is the same VLAN configured on your physical or virtual on-prem interface and matches the connectivity provider’s configuration (when applicable).

* ASN (Autonomous System Number)
  * Enter the ASN that will identify your network in BGP. This can be your organization’s ASN or one provided by your connectivity provider. The ASN is used in path selection and BGP session establishment with Microsoft’s ASN.

* BGP peer IP addresses
  * The portal expects the IP addresses drawn from the `/30` subnets you defined. After you save the private peering configuration, configure those same IP addresses on your on-premises router interfaces so the BGP neighbor relationships can form.

* Route advertisement (BGP settings)
  * Configure which on-premises prefixes are advertised to Azure via ExpressRoute. Correct route advertisement ensures Azure VNets can reach your on-prem networks and allows your on-premises routers to learn Azure VNet prefixes. Verify route filtering and summarize carefully to avoid leaking unintended networks.

* MD5 hash for the BGP session (optional)
  * BGP MD5 adds an authentication layer for the BGP session. While optional, MD5 is recommended where possible to safeguard against unauthorized peers and accidental route injection. If you enable MD5, configure the same string on both the portal and your on-premises devices.

* Global Reach (optional)
  * If you operate multiple on-premises sites and want to connect them via Microsoft’s network (rather than sending traffic over the public Internet or private direct links), consider enabling ExpressRoute Global Reach. Global Reach allows traffic between your sites to transit the Microsoft backbone when multiple ExpressRoute circuits are present and enabled for Global Reach.

Step-by-step: configuring private peering in the Azure portal

1. Open your ExpressRoute circuit in the Azure portal and select the Private peering tab.
2. Enter the Primary and Secondary `/30` subnets for BGP peering.
3. Specify the VLAN ID that will be used on the Layer 2 link.
4. Enter your ASN (or the provider’s ASN if applicable).
5. Input the BGP peer IP addresses (from each `/30`).
6. Configure route advertisement settings and any prefix filters required.
7. (Optional) Enable MD5 authentication and enter the MD5 string.
8. (Optional) Enable Global Reach if you need Microsoft backbone connectivity between on-prem sites.
9. Save the configuration and coordinate with your on-prem team or provider to configure the same values on your equipment.

Final checklist before enabling private peering

* Verify the chosen `/30` subnets do not overlap any VNet or on-prem address space to be advertised.
* Confirm the VLAN ID and peer IPs exactly match your on-premises configuration.
* Coordinate and confirm the ASN with your provider or routing team.
* Decide whether to enable BGP MD5 authentication for additional session security.
* If connecting multiple sites, evaluate ExpressRoute Global Reach and follow Azure guidance for multi-circuit configurations.

<Callout icon="lightbulb">
  Make sure the configuration you enter in the Azure portal is mirrored exactly on your on-premises routers (VLAN, peer IPs, ASN, BGP timers, and optional MD5) so the BGP sessions can establish and routes are exchanged correctly.
</Callout>

Once the portal settings are applied and your on-premises devices are configured to match, private peering will establish private BGP sessions across the ExpressRoute circuit, enabling secure, low-latency connectivity between your on-premises environment and Azure VNets.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3b13bf2e-ae4b-48f8-bc30-43e676e68d98/lesson/b4e350c4-0bc8-4909-822b-752f287d815c" />
</CardGroup>
