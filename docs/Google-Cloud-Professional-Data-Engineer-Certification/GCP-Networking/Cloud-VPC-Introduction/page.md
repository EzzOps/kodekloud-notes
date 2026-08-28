# Cloud VPC Introduction

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-VPC-Introduction/page

Introduction to Cloud VPC explaining logical isolation, IP addressing, subnets, routing, firewall control, connectivity options, and best practices for designing secure cloud networks.

Welcome back. In this lesson you'll learn what a Cloud VPC (Virtual Private Cloud) is, why it matters, and how it maps to real-world networking concepts you already know.

Put simply, a Cloud VPC is your private, logically isolated network inside a cloud provider’s global infrastructure. It’s where your virtual machines, storage, and cloud services live. With a VPC you control IP addressing, subnet layout, firewall policies, routing, and how your resources connect to each other and the public internet.

<Frame>
  <img alt="A slide titled &#x22;Cloud VPC&#x22; showing a cloud icon above a dashed circle containing a small building illustration with server and database icons connected to it. The graphic sits on a light blue background with a © Copyright KodeKloud note." />
</Frame>

Why VPCs matter (quick overview)

* Logical isolation: VPCs provide a secure “bubble” for your cloud resources, separated from other customers’ networks.
* Network control: Define IP ranges, subnets, routing tables, and security (firewall) rules.
* Flexible connectivity: Connect VPCs to each other or on-premises networks using peering, VPNs, or dedicated interconnects.
* Compliance and segmentation: Use subnets and firewall rules to isolate environments (production, staging, dev).

VPC analogy — “apartment building” (helps visualize responsibilities)

* The cloud provider is the building owner/manager: they run the physical datacenter, network backbone, and managed platform services.
* Your VPC is your apartment: you design the layout, pick which rooms (subnets) you use, and control who can enter (firewall rules).
* Tenants are separate customers: activities inside one tenant’s apartment don’t affect other tenants unless explicitly connected.

<Frame>
  <img alt="An illustration of a residential apartment building with four labeled tenant units (Tenant 01–04). Lines connect each unit to a top area showing shared services—Shared Security, Shared Water, and Shared Electricity—representing multi-tenant VPCs." />
</Frame>

Mapping the analogy to technical concepts

| Concept                  |                                                 Cloud equivalent | What you control                                                |
| ------------------------ | ---------------------------------------------------------------: | --------------------------------------------------------------- |
| Building / Owner         | Cloud provider infrastructure (data center, physical networking) | Nothing — provider-managed (physical security, power, backbone) |
| Apartment / Tenant space |                                            VPC (virtual network) | IP addressing, subnets, routing, firewall/security rules        |
| Rooms                    |                                                          Subnets | IP range allocation, resource placement (zones/regions)         |
| Doors & locks            |                                 Firewall rules / Security groups | Allow/block traffic to/from resources                           |
| Hallways & elevators     |                                Routing, load balancers, gateways | How traffic flows between subnets, VPCs, and the internet       |
| Inter-apt connections    |                                   VPC peering, VPN, Interconnect | Explicitly configured cross-VPC or on-prem connectivity         |

Key clarifications and best practices

* Shared responsibility: The provider secures and operates the physical layer; you are responsible for network design, segmentation, and access controls inside your VPC.
* Isolation: VPCs are isolated at the network level. No cross-VPC access occurs unless you configure VPC peering, a VPN, or a dedicated interconnect.
* Segmentation: Use subnets and IP ranges to separate environments and control communication with routing and firewall rules.
* Naming and IP planning: Plan CIDR ranges and subnet sizes early to avoid overlapping address spaces when you later peer VPCs or connect to on-prem networks.

<Callout icon="lightbulb">
  VPCs give you network-level isolation and control. The provider secures and operates the physical infrastructure, while you design IP addressing, subnets, firewall policies, and routing for your workloads.
</Callout>

Common connectivity options (one-line descriptions)

* VPC Peering — Private, non-transitive connection between two VPCs for low-latency internal traffic.
* VPN — Encrypted tunnel for secure connectivity between a VPC and on-premises networks or other clouds.
* Interconnect / Direct Connect — Dedicated, high-throughput private link between your network and the cloud provider.
* Shared VPC / Transit Gateway / Hub-and-spoke — Centralized models for managing many VPCs at scale.

Further reading and references

* [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
* [Google Cloud VPC Overview](https://cloud.google.com/vpc/docs/vpc)
* [Azure Virtual Network (VNet) Overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)

That’s it for this lesson — next, we’ll dive deeper into subnets, routing tables, and firewall rules so you can design a secure and scalable VPC topology. See you in the next video.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/3994c380-4923-4971-ad8b-5c9b0e92fa29" />
</CardGroup>
