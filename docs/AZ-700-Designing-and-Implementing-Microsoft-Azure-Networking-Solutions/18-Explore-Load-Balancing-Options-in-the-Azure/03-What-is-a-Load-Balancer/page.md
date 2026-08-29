# What is a Load Balancer

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Load-Balancing-Options-in-the-Azure/What-is-a-Load-Balancer/page

Describes a load balancer and how it distributes incoming traffic across backend servers to improve availability, scalability, fault tolerance, and application performance.

A load balancer is a core network component that automatically distributes incoming client requests across multiple backend resources—such as virtual machines or servers—to avoid overloading any single resource and to eliminate single points of failure. Properly implemented load balancing improves availability, reliability, and application performance.

Below we first look at a traditional setup without a load balancer.

The DNS record for `www.kodekloud.com` resolves to a single public IP. All users are routed to one backend server. If that server fails or becomes overloaded, users experience downtime or degraded performance because there is no backup or traffic management.

Now we introduce a load balancer.

`www.kodekloud.com` still resolves to a public IP address, but that IP is attached to a load balancer. The load balancer sits in front of a pool of backend servers and distributes incoming requests among them. If one server goes down, the load balancer redirects traffic to the remaining healthy servers. To do this reliably, the load balancer continuously monitors the health of each backend using health probes.

<Frame>
  <img alt="The image illustrates a load balancer setup, showing the flow from a DNS to a user, then through a public IP to a load balancer, which distributes traffic to multiple server instances." />
</Frame>

How it works (simplified flow)

1. DNS lookup: `www.kodekloud.com` resolves to a public IP.
2. Client sends requests to that public IP, which belongs to the load balancer.
3. Load balancer receives requests and forwards them to a backend pool of servers.
4. Health probes run at intervals to evaluate backend instance health.
5. If an instance is unhealthy, the load balancer excludes it until it recovers.

> **lightbulb** Health probes are critical: they ensure traffic is only routed to healthy backends. Configure probe frequency, timeout, and health criteria to match your application’s responsiveness and availability requirements.

Key benefits of using a load balancer

| Benefit              | Description                                               | Example use case                                        |
| -------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| High availability    | Automatically reroutes traffic away from failed instances | Keep web apps online during VM failures                 |
| Scalability          | Distributes load to support more concurrent users         | Scale out backend pool during peak traffic              |
| Fault isolation      | Limits impact of a failing instance                       | Maintenance or unplanned outages don't affect all users |
| Improved performance | Evenly spreads requests so no single server is overloaded | Maintain low response times under load                  |

In summary, a load balancer is a smart traffic manager for your application. It reliably routes requests across multiple backends, prevents single points of failure, and enables scalable, highly available architectures—whether in Microsoft Azure or other cloud environments.

Next steps: explore different types of load balancers (layer 4 vs. layer 7), managed cloud offerings (e.g., Azure Load Balancer, Azure Application Gateway), and configuration patterns for session persistence, SSL termination, and autoscaling.

Links and references

* [Azure Load Balancer documentation](https://learn.microsoft.com/azure/load-balancer/load-balancer-overview)
* [Introduction to load balancing (Cloudflare)](https://www.cloudflare.com/learning/ddos/glossary/load-balancing/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/a231ef6d-9e0c-4c9d-81dd-d3ea9de8d42f/lesson/27c45670-a501-4719-aea3-6d192bb400b5)
