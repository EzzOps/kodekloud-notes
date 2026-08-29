# Use cases for Azure Traffic Manager

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-Traffic-Manager/Use-cases-for-Azure-Traffic-Manager/page

Azure Traffic Manager use cases and operation for DNS-based traffic routing, health probes, failover, performance routing, maintenance handling, and hybrid cloud endpoint support

Azure Traffic Manager is a global DNS-based traffic director and the entry point for distributed applications. It operates at the DNS layer to direct user requests to the best endpoint for availability, performance, or compliance.

Consider a deployment with an app running in East US and another in West Europe. Traffic Manager sits above these endpoints and load-balances DNS responses so client requests go to the most appropriate endpoint. If the primary endpoint (East US) becomes unhealthy according to Traffic Manager’s health probe, Traffic Manager stops returning that endpoint in DNS answers and instead directs clients to the secondary (failover) endpoint (West Europe). This enables automatic failover without manual intervention. Keep in mind that DNS caching and the configured TTL affect how quickly clients observe the change: shorter TTLs produce faster failover but increase DNS query volume.

Traffic Manager can also use performance-based routing to steer users to the closest or lowest-latency region automatically — for example, routing European users to West Europe and U.S. users to East US to optimize latency and user experience.

For planned maintenance or upgrades, you can disable an endpoint in the Traffic Manager profile (or let health probes mark it unavailable). Traffic Manager will stop returning it in DNS responses and route user traffic to remaining healthy endpoints. After maintenance completes, re-enable the endpoint and it will rejoin the rotation — no DNS record changes required.

Traffic Manager is not limited to Azure-managed resources. It can direct traffic to external endpoints (on-premises or other clouds such as AWS or GCP) as long as the endpoint has a public DNS name, making Traffic Manager useful for hybrid-cloud and migration scenarios.

You can combine routing methods across nested or multiple Traffic Manager profiles to implement advanced traffic strategies — for example, weighted routing for A/B testing, priority (failover) for active-passive disaster recovery, or geographic routing for data residency and compliance.

<Frame>
  <img alt="The image is a diagram illustrating Azure Traffic Manager use cases, showing a TM profile managing two endpoints for increased application availability, improved performance, and service maintenance without downtime." />
</Frame>

Health probes will flag an endpoint as unavailable during maintenance or when it becomes unhealthy. When that happens, Traffic Manager stops returning that endpoint in DNS responses and client traffic is redirected to backup endpoints. Once maintenance is complete and you re-enable the endpoint, it rejoins the rotation automatically.

Traffic Manager supports a variety of routing methods. You select one routing method per Traffic Manager profile, but you can combine multiple methods across nested or separate profiles to achieve complex behaviors.

<Frame>
  <img alt="The image illustrates Azure Traffic Manager use cases, showing a diagram of primary and failover endpoints with various application service plans in East US and West Europe, highlighting benefits like increased availability and improved performance." />
</Frame>

Routing methods overview

| Routing method      |                      When to use it | Typical scenario                                                 |
| ------------------- | ----------------------------------: | ---------------------------------------------------------------- |
| Priority (Failover) |        Primary → secondary failover | Active-passive DR: send traffic to primary unless it’s unhealthy |
| Performance         |              Lowest-latency routing | Route users to the closest/fastest region automatically          |
| Weighted            |    Traffic distribution experiments | A/B testing or gradual rollouts across endpoints                 |
| Geographic          | Data residency or geo-based content | Route users by region to comply with laws or localize content    |
| MultiValue / Subnet |                    Advanced control | Return multiple healthy endpoints or route by client IP subnet   |

How Traffic Manager works

Traffic Manager is a DNS-level service — it does not sit in the data path. When a client resolves a hostname (for example, `www.kodekloud.com`), the resolver chain (client resolver or a recursive resolver such as Google DNS) issues a DNS query that eventually reaches the Traffic Manager profile. Traffic Manager evaluates endpoint health with probes and applies the configured routing method to select the best endpoint.

Traffic Manager typically returns a DNS response that points the recursive resolver (and ultimately the client) to the chosen endpoint, often as a CNAME record such as `kodekloudeu.cloudapp.net`. The recursive resolver caches that response according to the DNS TTL, and the client then connects directly to the selected endpoint. Because application traffic flows directly between client and endpoint, Traffic Manager does not introduce a data-plane hop or bandwidth bottleneck — it participates only in the control plane via DNS responses.

<Frame>
  <img alt="The image is a diagram showing how a Traffic Manager works, detailing the interaction between a user, browser, DNS service, Microsoft Azure, and various applications like web apps and virtual machines." />
</Frame>

> **lightbulb** Traffic Manager performs DNS-based routing only — it does not proxy or forward application traffic. Design your failover and maintenance plans around DNS TTL and caching behavior to ensure expected recovery times.

> **warning** DNS caching by clients and intermediate resolvers can delay failover. Use appropriately low TTLs to shorten propagation time, but balance this against increased DNS query traffic and potential cost.

Links and references

* [Demystifying DNS](https://learn.kodekloud.com/user/courses/demystifying-dns)
* [AWS For Beginners with Hands-On Labs](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs)
* [GCP Cloud Digital Leader Certification](https://learn.kodekloud.com/user/courses/gcp-cloud-digital-leader-certification)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/38ad64e6-12ba-4187-955b-c2e4522be498/lesson/d4f1cb65-a22c-4558-b5a0-22df1c2b81a4)
