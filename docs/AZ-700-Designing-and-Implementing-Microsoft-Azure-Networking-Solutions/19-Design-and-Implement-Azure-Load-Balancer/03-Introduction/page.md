# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Load-Balancer/Introduction/page

Guide to designing, deploying, and operating Azure Load Balancer solutions including types, SKUs, zones, gateway routing, probes, and NAT

In this lesson you’ll learn how to design, deploy, and operate Azure Load Balancer solutions that deliver scalability, resilience, and high availability for cloud applications.

By the end of this lesson you will be able to:

* Differentiate public (internet-facing) and internal (private) Azure Load Balancers, and select the right type for your architecture.
* Route traffic through Network Virtual Appliances (NVAs) using Gateway Load Balancer to enable deep packet inspection, advanced firewalling, or integration with third‑party appliances.
* Understand how Azure Load Balancers operate across multiple Availability Zones to survive zone-level failures and maximize uptime.
* Compare the Standard and Basic SKUs of Azure Load Balancer to determine the best fit for performance, scale, and security requirements.

<Frame>
  <img alt="The image lists learning objectives related to load balancers, including differentiating between types, routing traffic, understanding operations in availability zones, and comparing SKUs." />
</Frame>

This lesson also provides step-by-step, hands-on guidance in the Azure portal so you can practice deploying and configuring the components that support production-grade load balancing:

* Create an Azure Load Balancer and the supporting resources it requires.
* Associate backend pools with Virtual Machines (VMs) or Virtual Machine Scale Sets (VMSS) to enable horizontal scaling.
* Define load-balancing rules to control how incoming connections are distributed across backend endpoints.
* Configure session persistence (sticky sessions) for stateful applications that require client affinity.
* Create health probes to monitor backend instance availability and ensure traffic is only directed to healthy endpoints.
* Define outbound NAT rules so backend resources can initiate outbound connections to the internet when necessary.

<Frame>
  <img alt="The image lists two learning objectives: configuring probes to monitor backend instances and configuring outbound NAT rules for backend traffic." />
</Frame>

> **lightbulb** This lesson combines conceptual design with hands-on portal walkthroughs. Follow the portal exercises to practice creating backend pools, probes, and outbound NAT rules. For deeper reference, see the [Azure Load Balancer documentation](https://learn.microsoft.com/azure/load-balancer/).

Quick SKU comparison

| SKU      | Best for                                                              | Key differences                                                                                       |
| -------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Standard | Production workloads requiring high availability, security, and scale | Supports zone redundancy, more backend instances, and integration with Network Security Groups (NSGs) |
| Basic    | Small or non-critical workloads, test/dev environments                | Simpler feature set, no zone redundancy, limited scalability and security features                    |

> **warning** Choose the SKU that matches your availability, scale, and security needs. Standard SKU is recommended for production deployments due to zone-redundancy and advanced networking support.

Together, these topics and hands-on steps form a practical foundation for designing, deploying, and operating Azure Load Balancers in production environments. For further reading and examples, consult the [Azure Load Balancer Overview](https://learn.microsoft.com/azure/load-balancer/overview) and the [Gateway Load Balancer documentation](https://learn.microsoft.com/azure/load-balancer/standard-load-balancer-overview).

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6d9c06ee-9a3e-4b7a-be2f-6bb8314af6a2/lesson/e8095c1b-9718-4f36-bcd6-d5f38759dfb0)
