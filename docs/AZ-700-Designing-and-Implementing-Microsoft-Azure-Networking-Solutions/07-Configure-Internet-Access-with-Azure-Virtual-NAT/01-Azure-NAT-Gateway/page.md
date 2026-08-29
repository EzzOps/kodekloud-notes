# Azure NAT Gateway

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Configure-Internet-Access-with-Azure-Virtual-NAT/Azure-NAT-Gateway/page

Explains Azure NAT Gateway, a managed service that centralizes scalable, secure outbound Internet access for virtual networks, preventing SNAT port exhaustion and providing predictable source IPs for whitelisting

Azure NAT Gateway

In this lesson, we cover Azure NAT Gateway — the managed Azure service that provides secure, scalable outbound Internet access for resources inside your virtual network.

Why use NAT Gateway?

If you run dozens or hundreds of virtual machines (VMs) or PaaS resources in Azure, providing reliable outbound Internet connectivity can be challenging:

* SNAT port exhaustion: With many instances sharing a limited number of source ports, outbound connections can fail when ports are exhausted.
* Security exposure: Assigning public IPs to each VM increases the attack surface.
* Unpredictable source IPs: When outbound addresses vary per VM, whitelisting and access control at external services becomes difficult.

Azure NAT Gateway centralizes outbound connectivity, so all egress traffic from associated subnets leaves through a managed, predictable set of public IP addresses — simplifying security, scaling, and whitelisting.

Architecture overview

A typical NAT Gateway deployment looks like this:

* A NAT Gateway resource is created using Standard public IP resources.
* A NAT Gateway can be associated with multiple subnets in the same virtual network.
* Each subnet can be associated with only one NAT Gateway.
* You can assign a single public IP to the NAT Gateway or a public IP prefix (a contiguous set of addresses) to provide a pool of outbound addresses.

Benefits at a glance

| Benefit                 | Description                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------- |
| Outbound simplification | Centralizes egress so you don’t need public IPs on every VM.                            |
| Managed scalability     | Azure scales NAT Gateway to prevent SNAT port exhaustion for large workloads.           |
| Predictable source IPs  | Outbound traffic appears from a fixed set of IPs, simplifying whitelisting.             |
| Improved security       | VMs remain private; only NAT Gateway public IP(s) are exposed for outbound connections. |

When to choose NAT Gateway

* Large-scale outbound workloads that require high port capacity.
* Scenarios where predictable source IPs are required for whitelisting external services.
* Cases where you want VMs or NICs to remain private (no direct public IPs).
* Any environment aiming to reduce maintenance and operational overhead for outbound connectivity.

Coexistence of inbound and outbound flows

Many applications require both inbound and outbound connectivity — for example, a web tier that receives user traffic and also calls external APIs. Azure is flow-aware: it distinguishes inbound-initiated connections (handled by Azure Load Balancer or Public IPs) from outbound-initiated connections (routed through NAT Gateway) so replies are delivered to the correct VM.

<Frame>
  <img alt="The image illustrates a network diagram showing the coexistence of inbound and outbound flows within a virtual network, featuring elements like load balancer, NAT, subnets, and VMs. It emphasizes flow awareness, simultaneous support, and correct translation handling." />
</Frame>

A couple of important notes about Load Balancer vs NAT Gateway:

* Azure Load Balancer can provide outbound connectivity in certain configurations (for example, when VMs have inbound rules), but it is not optimized as the primary mechanism for very high-scale outbound workloads. Using it for heavy egress can still lead to SNAT port exhaustion.
* NAT Gateway is purpose-built for high-scale, predictable outbound connectivity and should be used when you need guaranteed outbound capacity and stable source IP addresses.

Flow-awareness ensures Azure correctly translates and routes traffic in both directions so responses reach the appropriate VM — even when both Load Balancer and NAT Gateway are used together.

> **lightbulb** Use NAT Gateway when you need predictable, secure, and scalable outbound connectivity from subnets. It is the recommended approach to avoid SNAT port exhaustion and centralize outbound IP addresses for whitelisting.

Quick comparison

| Feature                | NAT Gateway                              | Azure Load Balancer (outbound behavior)                                  |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------ |
| Primary purpose        | High-scale, managed outbound egress      | Load balancing inbound traffic; provides limited outbound in some setups |
| SNAT port scaling      | Managed by Azure (high capacity)         | Can exhaust SNAT ports under heavy outbound load                         |
| Predictable source IPs | Yes (single IP or IP prefix)             | Less predictable unless manually configured with public IPs              |
| Typical use case       | Centralized outbound for subnets and VMs | Inbound traffic distribution and small-scale outbound scenarios          |

Useful links and references

* [Azure NAT Gateway documentation](https://learn.microsoft.com/azure/virtual-network/nat-gateway)
* [Azure Load Balancer documentation](https://learn.microsoft.com/azure/load-balancer/load-balancer-overview)
* [Azure public IP documentation](https://learn.microsoft.com/azure/virtual-network/public-ip-address)

Summary

Azure NAT Gateway is a robust, managed service that centralizes outbound Internet access for subnets, avoids SNAT port exhaustion, and provides predictable source IPs for whitelisting. It works seamlessly with inbound solutions like Azure Load Balancer to support complex application topologies.

Next steps

Now that you understand what NAT Gateway does and why it’s useful, proceed to the Azure portal or ARM/Bicep/Terraform workflows to create and associate a NAT Gateway with your virtual network subnets. For implementation details and examples, see the official Azure NAT Gateway documentation linked above.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/5fa34fd1-903f-422e-8fc1-12a89731ebb9/lesson/dcb73f54-10c8-4245-89fb-7cda6c6401cd)
