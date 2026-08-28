# Cloud VPC IP Addresses and Subnets

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-VPC-IP-Addresses-and-Subnets/page

Overview of Google Cloud VPCs, IP addressing and subnets, public versus private networking, Cloud NAT, firewall rules, and CIDR planning best practices for scalable and secure deployments.

Hey everyone — welcome back.

In this lesson we cover a fundamental piece of every cloud deployment: the Virtual Private Cloud (VPC). We’ll start with the big picture and then drill into how IP addressing and subnets work so you clearly understand how resources are identified and how they communicate on Google Cloud Platform (GCP).

Big picture: the VPC network

* The VPC is the virtual, isolated network that hosts your GCP resources.
* It defines IP ranges, subnets, firewall policies, and routing behavior.
* The VPC construct itself is global in GCP; subnets you create are regional.

Below is a simplified diagram illustrating a VPC with regional subnets and instances:

<Frame>
  <img alt="A simplified Google Cloud VPC diagram showing Internet traffic entering a Cloud Network and being routed to two regions (us-west1 and us-east1) with three subnets labeled 10.240.0.0/24, 192.168.1.0/24, and 10.2.0.0/16. Each subnet contains Compute Engine instances." />
</Frame>

Core concepts and definitions

What is a VPC?

* A Virtual Private Cloud (VPC) is your private virtual network in GCP.
* It provides centralized control over IP address ranges, subnets, firewall rules, and routing.
* The VPC itself is global; subnets are created per region and span all zones within that region.

IP addresses in a VPC

* Private (internal) IPs: Non-internet-routable addresses used for internal communication inside the VPC. Common ranges: `10.x.x.x`, `172.16.x.x–172.31.x.x`, `192.168.x.x`.
* External (public) IPs: Internet-routable addresses assigned to resources when direct inbound/outbound internet access is required (ephemeral or static). Instances without external IPs can still initiate outbound connections by using Cloud NAT.

Subnets and CIDR notation

* A subnet is a regional slice of your VPC’s IP address space, defined by a primary CIDR range (for example `10.0.1.0/24`).
* CIDR notation `a.b.c.d/nn` indicates the network prefix length; the `/nn` determines how many addresses are available.
* In GCP, subnets are regional and span all zones in the chosen region. This simplifies IP planning across availability zones and increases resilience.

Why use subnets?

* Segment resources by function, security posture, or environment (for example, `web`, `app`, `db`).
* Apply different firewall rules and routing for different groups of resources.
* Simplify IP management and future scaling.

Public vs. private subnets (conceptual in GCP)

* Public subnet: Instances have external IPs and routes to the internet gateway; used for load balancers, public-facing VMs, etc.
* Private subnet: Instances only have internal IPs and no external IPs; use Cloud NAT for outbound-only internet access (OS updates, package installs) while preventing inbound internet traffic.

Quick reference table

| Topic               |                                  Description | Example / Notes                             |
| ------------------- | -------------------------------------------: | ------------------------------------------- |
| VPC                 |                Global virtual network in GCP | Create and manage at the project level      |
| Subnet              |             Regional CIDR block within a VPC | `10.0.1.0/24` (spans all zones in a region) |
| Private IP          |                        Internal-only address | `10.128.0.5`                                |
| External IP         |                    Internet-routable address | `34.68.194.64` (ephemeral or static)        |
| Cloud NAT           | Outbound-only internet for private instances | Use NAT for instances without external IPs  |
| Secondary IP ranges |                 Additional CIDRs on a subnet | Useful for GKE Pod IPs or managed services  |

Important networking details for GCP

* Internet access: An instance needs an external IP to receive direct inbound traffic from the internet. Outbound egress from an instance with an external IP is available via the default route to the internet gateway.
* Cloud NAT: Provides controlled outbound-only internet connectivity for instances without external IPs.
* Secondary IP ranges: Attach secondary CIDR ranges to subnets for alias IPs, GKE clusters, or services that require additional address space.
* Firewall rules: GCP firewall rules are stateful and apply at the VPC level. Use them to explicitly allow or deny traffic to instances based on IP, protocols, and ports.

Best practices and planning

<Callout icon="lightbulb">
  Tip: Plan your CIDR ranges and subnet layout before deploying resources. Reserve address space for growth, separate environments (prod/stage/dev), and avoid overlapping ranges across projects and on-prem networks.
</Callout>

<Callout icon="warning">
  Warning: Avoid overlapping CIDR ranges between VPCs or with your on-prem networks unless you use advanced routing or NAT solutions. Overlaps complicate peering and VPN connectivity.
</Callout>

Quick recap

* VPC = your controllable network in GCP (global construct).
* Subnet = regional CIDR block used to organize IPs and resources.
* Private IPs are used for internal communication; external IPs enable internet-routable communication.
* Use Cloud NAT to permit outbound-only internet for private instances without exposing them to inbound traffic.

Further reading and references

* [GCP VPC documentation](https://cloud.google.com/vpc/docs)
* [Cloud NAT overview](https://cloud.google.com/nat/docs/overview)
* [VPC subnetworks in GCP](https://cloud.google.com/vpc/docs/subnets)

That’s the essential theory for VPCs, IP addressing, and subnets in GCP. A hands-on demo will show creating a VPC and subnets, configuring CIDR ranges, applying firewall rules, and setting up Cloud NAT. Speak with you soon.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/7e130de4-4123-496e-b876-68d577f8ab6a" />
</CardGroup>
