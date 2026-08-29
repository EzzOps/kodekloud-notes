# Cloud VPC Connecting to other networks

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Networking/Cloud-VPC-Connecting-to-other-networks/page

Overview of Google Cloud VPC connectivity options for on-prem, VPC-to-VPC, interconnect, and multi-cloud scenarios comparing VPN, Dedicated and Partner Interconnect and peering

Welcome back. This lesson explains how a Google Cloud VPC can connect to other networks — on-premises data centers, other Google Cloud projects, or external clouds such as AWS. We cover the common connection options, how they work, trade-offs, and guidance for choosing the right solution for performance, cost, and security.

Private Service Connect (overview)

* Private Service Connect enables private consumption of Google services inside your VPC. Networks often need to communicate privately between environments; this article focuses on the main networking primitives and when to use each.

## On-premises to Google Cloud: VPN and Interconnect

Scenario: Your organization runs workloads on-premises and in Google Cloud. You need secure, private IP connectivity between your on-prem network and a Google VPC.

Common approaches:

* Cloud VPN (site-to-site IPsec)
  * Creates encrypted tunnels over the public Internet.
  * Use HA VPN for higher availability and automatic redundancy across Google edge locations.
  * Best when cost and quick setup matter or for low/medium bandwidth requirements.

* Cloud Interconnect
  * Provides private, dedicated connectivity into Google’s network.
  * Traffic enters Google’s global backbone and does not traverse the public Internet.
  * Ideal for very high throughput, lower latency, predictable performance, or strict compliance requirements.

Key distinction:

* Interconnect = private connectivity into Google’s backbone (no traversal of the public Internet).
* VPN = encrypted traversal of the public Internet (IPsec), but still provides private connectivity between on-prem and cloud resources.

## VPC-to-VPC: VPC Network Peering

If you need private connectivity between multiple VPCs across projects or regions, VPC Network Peering is a common choice.

* VPC Peering connects two VPCs directly over Google’s internal network.
* Traffic remains on Google’s backbone and is not exposed to the public Internet.
* Peering is one-to-one and non-transitive — you cannot route from VPC A to VPC C via VPC B.

<Frame>
  <img alt="A Google Cloud diagram showing VPC peering between two projects with regions, subnets, VMs, and arrows for importing/exporting routes and VPN/router connections. Left-side callouts note private IP connectivity, internal traffic (no internet exposure), and that peering is one-to-one with no transitive routing." />
</Frame>

Use VPC peering for low-latency, private communication between two VPCs when simple, direct connectivity is sufficient. For hub-and-spoke or centralized routing, consider Shared VPC, Cloud VPN with a hub, or network virtual appliances.

## Interconnect options: Dedicated vs Partner

For high-bandwidth or low-latency requirements, Cloud Interconnect is preferable to VPN. Choose between Dedicated Interconnect and Partner Interconnect depending on location, bandwidth requirements, and operational preferences.

* Dedicated Interconnect
  * A physically direct connection from your on-prem network to Google’s network at an interconnect location (colocation facility).
  * Provides very high bandwidth, low latency, and predictable performance because traffic enters Google’s backbone immediately.
  * Common for organizations that transfer large volumes of data frequently or require strict data-control guarantees.

<Frame>
  <img alt="A simple network diagram showing an on-premises data center connected via a Dedicated Interconnect to a VPC/cloud network (with an edge cache) for low-latency data transfer. Labels at the bottom highlight benefits like high bandwidth, reliability, and lower latency." />
</Frame>

* Partner Interconnect
  * Use when Google lacks a direct presence at your data center location.
  * A supported service provider (telecom or colocation partner) delivers connectivity to Google at an interconnect location.
  * Provides Layer 3 connectivity into your VPC with multiple bandwidth options and greater geographic flexibility.

## Multi-cloud and hybrid connectivity

* Multi-cloud setups (for example, connecting Google Cloud to AWS) are common. Typical approaches include:
  * VPN tunnels between clouds for encrypted IP connectivity.
  * Provider-based dedicated connectivity or partner services that link cloud backbones.
  * Hybrid designs that combine Interconnect, VPN, and peering depending on latency and throughput needs.

Choose the method based on:

* Latency and bandwidth requirements
* Cost and operational overhead
* Regulatory, compliance, or data residency constraints

## Comparison table: connectivity options

| Connection type        |                                                Use case | Pros                                                                         | Cons                                                                              |
| ---------------------- | ------------------------------------------------------: | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Cloud VPN / HA VPN     |        Site-to-site encrypted tunnels over the Internet | Quick to set up; encrypted; `HA VPN` offers regional redundancy              | Performance depends on Internet; not ideal for very high bandwidth                |
| Dedicated Interconnect |              High-throughput on-prem to Google backbone | Very high bandwidth, low latency, predictable performance                    | Requires colocation and physical setup; higher cost                               |
| Partner Interconnect   |                     Where Google has no direct presence | Flexible locations; multiple bandwidth tiers; easier onboarding via provider | Slightly higher latency than Dedicated; dependent on provider                     |
| VPC Network Peering    | Private VPC-to-VPC connectivity across projects/regions | Low-latency, private traffic on Google backbone                              | One-to-one, non-transitive; not suitable for hub-and-spoke without other controls |

## Quick exam-style question

Which connection option provides the highest bandwidth and lowest latency to your on-prem environment?

* Answer: Dedicated Interconnect.

> **lightbulb** Remember: VPC peering is non-transitive and does not allow route propagation through intermediate peers. For architectures that require centralized connectivity or transitive routing, consider alternatives such as Shared VPC, Cloud VPN in a hub-and-spoke topology, or a third-party network virtual appliance.

## Summary

Google Cloud offers multiple secure ways to connect networks:

* Cloud VPN: encrypted site-to-site tunnels over the Internet (`HA VPN` for higher availability).
* Cloud Interconnect: dedicated private connectivity (`Dedicated Interconnect` and `Partner Interconnect`) for high performance.
* VPC Network Peering: private, low-latency connectivity between VPCs (one-to-one, non-transitive).

Select the option that best balances performance, cost, and security for your workload.

## Links and references

* [Google Cloud VPN documentation](https://cloud.google.com/network-connectivity/docs/vpn)
* [Cloud Interconnect documentation](https://cloud.google.com/network-connectivity/docs/interconnect)
* [VPC Network Peering documentation](https://cloud.google.com/vpc/docs/vpc-peering)
* [AWS (Amazon Web Services)](https://aws.amazon.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/f2509a3a-1b7e-49f6-bdea-4985dc552c0e/lesson/60b3bd46-b78c-4530-b3e2-6f99782fbbee)
