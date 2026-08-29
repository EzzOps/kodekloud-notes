# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Peering-for-an-ExpressRoute-Deployment/Introduction/page

Configuring ExpressRoute peering to connect on premises networks to Azure, covering private and Microsoft peering, IP planning, BGP configuration, and route filtering for secure connectivity

Now that you know how to provision an ExpressRoute circuit and choose the correct SKUs, this lesson focuses on one of the most critical topics: configuring peering for ExpressRoute.

Peering determines how your on-premises network exchanges traffic with Azure. It directly impacts connectivity, security posture, and access to Microsoft services. Note that ExpressRoute peering is a distinct concept from peering between Azure virtual networks (VNet peering); it addresses different scenarios and operates at a different network layer.

> **lightbulb** ExpressRoute peering controls how traffic flows between your on-premises network and Azure: who advertises routes, which IP spaces are used (private vs. public), and how BGP sessions are configured. VNet peering, in contrast, links Azure virtual networks internally and does not involve your on-premises edge.

Learning objectives — what you will gain from this module:

| Topic               | Why it matters                                                                                                                                                                                                                                                                                                                                                            | Key focus areas                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Private peering     | Keeps traffic on private IP space and off the public Internet, enabling secure connectivity to Azure VNets                                                                                                                                                                                                                                                                | IP addressing and subnet planning, BGP configuration (ASN, neighbor IPs, session parameters), integrating settings with your ExpressRoute circuit |
| Microsoft peering   | Required to reach Microsoft SaaS (e.g., [Microsoft 365](https://www.microsoft.com/microsoft-365), [Dynamics 365](https://dynamics.microsoft.com/)) and certain Azure PaaS endpoints (e.g., [Azure Storage](https://learn.microsoft.com/azure/storage/), [Azure SQL](https://learn.microsoft.com/azure/azure-sql/)) that are advertised using Microsoft public IP prefixes | When private peering suffices vs. when Microsoft peering is required, public prefix advertisement, and connectivity considerations                |
| BGP route filtering | Helps you control which prefixes are accepted or advertised to limit routes propagated into your environment                                                                                                                                                                                                                                                              | Route filters for Microsoft peering, prefix selection and security, minimizing route table size and avoiding route leaks                          |

* Learn how to set up private peering — the most common configuration for connecting on-premises networks to Azure VNets — including IP planning and BGP details.
* Understand Microsoft peering and when it’s needed to reach Microsoft SaaS and certain PaaS services advertised via Microsoft public IP prefixes.
* Explore BGP route filtering to control accepted/advertised prefixes for improved security and stability across large or multi-region topologies.

<Frame>
  <img alt="The image lists learning objectives related to private and Microsoft peering for secure communication, connecting using public IP prefixes, and controlling BGP routes. It includes four numbered points on a gradient background." />
</Frame>

By the end of this module you will have a practical understanding of how ExpressRoute peering works and the exact differences between Private and Microsoft peering, enabling you to design secure, performant connectivity between your on-premises network and Azure.

Further reading and references:

* [ExpressRoute overview (Microsoft Learn)](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
* [Overview of BGP (Microsoft Learn)](https://learn.microsoft.com/azure/virtual-network/virtual-networks-bgp-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/3b13bf2e-ae4b-48f8-bc30-43e676e68d98/lesson/28f453ab-d686-4251-bc85-ea8be239869b)
