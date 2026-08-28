# Choosing a Load Balancer Type

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Load-Balancer/Choosing-a-Load-Balancer-Type/page

Guide to selecting Azure load balancer types, Gateway Load Balancer for NVAs, and choosing Basic versus Standard SKUs based on scale, security, and availability

Selecting the right Azure load balancer is a foundational decision for any cloud network architecture. This guide explains the main Azure load balancer types, when to use each, and how to choose between the Basic and Standard SKUs based on scale, resiliency, security, and availability needs.

What you’ll learn:

* The difference between Public and Internal Load Balancers
* When to use the Gateway Load Balancer for NVAs
* Key differences between Basic and Standard SKUs and recommended scenarios

## Load balancer types: Public vs Internal

* Public Load Balancer — Receives traffic from the Internet via a public IP address and distributes incoming requests to backend virtual machines. Use this for workloads that must be reachable from outside your Azure virtual network (for example, public web applications).
* Internal Load Balancer — Distributes traffic only within a private virtual network. Use this to balance traffic for internal application tiers or services that must remain private.

<Frame>
  <img alt="The image illustrates the architecture of choosing a load balancer type, showing the use of public and internal load balancers in a virtual network with web and business tier subnets. It explains the roles of each load balancer type in handling traffic." />
</Frame>

The diagram shows a common tiered application architecture: internet traffic is terminated at the public load balancer in the web tier, while internal calls (API requests, database traffic) are handled by an internal load balancer in the business tier. Separating public and internal load balancing reduces exposure, improves security posture, and enables you to tune performance for each tier independently.

## Gateway Load Balancer (for NVAs)

A specialized option is the Gateway Load Balancer. It enables transparent, high-throughput integration with third-party network virtual appliances (NVAs), such as firewalls, IDS/IPS, and other security devices.

Learn more: [https://learn.microsoft.com/en-us/azure/load-balancer/gateway-load-balancer-overview](https://learn.microsoft.com/en-us/azure/load-balancer/gateway-load-balancer-overview)

<Frame>
  <img alt="The image is a diagram illustrating a Gateway Load Balancer setup, showing the flow of unfiltered and filtered web traffic between customer applications, virtual networks, and network virtual appliances (NVAs)." />
</Frame>

How Gateway Load Balancer works (summary):

* Unfiltered internet traffic is directed to the Gateway Load Balancer frontend IP.
* Traffic is encapsulated and forwarded to NVAs for inspection and filtering.
* NVAs apply policies, then forward filtered traffic to the application backend.
* Supports chaining of multiple NVAs for complex inspection pipelines.

Key components:

* Frontend IP — receives incoming traffic.
* Load-balancing rules — determine distribution of packets to backends.
* Backend pools — typically composed of NVAs for Gateway LB deployments.
* Tunnel interfaces — provide connectivity and encapsulation to NVAs.
* Chaining — route traffic sequentially through multiple NVAs for layered inspection.

When you need transparent inspection, throughput, and high availability for security appliances, Gateway Load Balancer provides a scalable solution.

## Load Balancer SKUs: Basic vs Standard

Azure Load Balancer is available in two SKUs: Basic and Standard. Choose the SKU that aligns with your scale, resiliency, and security requirements.

<Frame>
  <img alt="The image is a comparison table between Basic and Standard SKUs for load balancers, highlighting features such as backend pool size, health probes, and availability zones. There are also instance configuration options on the right side." />
</Frame>

Use the table below to compare the most relevant SKU differences at a glance.

| Feature                |                                    Basic SKU |                                               Standard SKU |
| ---------------------- | -------------------------------------------: | ---------------------------------------------------------: |
| Backend pool size      | Up to 300 IP configurations per backend pool |                              Up to 5,000 backend instances |
| Health probes          |                                    TCP, HTTP |                     TCP, HTTP, HTTPS (advanced monitoring) |
| Availability zones     |                  No zone-redundant frontends |                Supports zonal and zone-redundant frontends |
| Inbound/outbound flows |          Primarily inbound; limited outbound |               Full inbound and flexible outbound scenarios |
| Security posture       |   Less restrictive by default; NSGs optional |   Secure by default — inbound blocked unless NSG allows it |
| SLA                    |                                       No SLA |                     99.99% SLA in supported configurations |
| Recommended use        |           Development, simple test scenarios | Production workloads requiring scale and high availability |

Additional considerations:

* Standard SKU is recommended for production workloads requiring high availability, zone redundancy, and stricter security controls.
* Basic SKU may be acceptable for small, non-critical environments where its limitations are understood and tolerated.

## Choosing the right combination

Decide based on these criteria:

* Exposure: Public vs Internal load balancer depending on whether the service must be accessible from the Internet.
* Security needs: Use Standard SKU and NSGs for stricter default posture; consider Gateway LB if you require NVAs for deep packet inspection.
* Scale and availability: For large-scale or SLA-bound services, prefer Standard SKU with zone redundancy.
* Global vs regional routing: If you need global load balancing, evaluate Azure Front Door or Traffic Manager alongside regional load balancers.

Recommended resources:

* Azure Load Balancer overview: [https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview](https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview)
* Gateway Load Balancer: [https://learn.microsoft.com/en-us/azure/load-balancer/gateway-load-balancer-overview](https://learn.microsoft.com/en-us/azure/load-balancer/gateway-load-balancer-overview)
* Network Security Groups (NSGs): [https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
* Azure Front Door: [https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview](https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview)
* Traffic Manager: [https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview](https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview)

<Callout icon="lightbulb">
  For production workloads that require high availability, zone redundancy, and stricter security controls, prefer the Standard SKU. Use Basic only for simple, non-critical scenarios where its limits are acceptable.
</Callout>

Now that you understand public vs internal load balancers, the Gateway Load Balancer pattern for NVAs, and the Basic vs Standard SKUs, you can select and configure the Azure load balancer that best meets your application’s performance, security, and availability requirements.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/6d9c06ee-9a3e-4b7a-be2f-6bb8314af6a2/lesson/76f6d7c1-6dab-4e30-8de3-ba79ea4c6091" />
</CardGroup>
