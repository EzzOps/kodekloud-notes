# Traffic Routing Methods

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-Traffic-Manager/Traffic-Routing-Methods/page

Overview of Azure Traffic Manager routing methods and best practices for DNS-based Priority, Weighted, Performance, and Geographic endpoint routing and health-based failover.

This guide describes the routing methods available in Azure Traffic Manager and how each method influences DNS responses to direct users to the most appropriate endpoint. All Traffic Manager decisions occur at the DNS layer: Traffic Manager returns the endpoint IP to the DNS resolver, and client traffic flows directly to that endpoint (Traffic Manager does not proxy user traffic).

> **lightbulb** Azure Traffic Manager performs DNS-based routing and uses health probes to exclude unhealthy endpoints from answers. Because routing happens at DNS, clients connect directly to the selected endpoint — Traffic Manager only influences DNS responses.

## Priority (Failover)

Use case: Active-passive failover and disaster recovery.

Flow summary:

* A client requests a URL (browser or service).
* The client’s resolver (ISP or public DNS) queries Azure Traffic Manager for the domain.
* Traffic Manager evaluates endpoints by configured priority (lowest number = highest priority).
* Health probes continuously check endpoint health.
* Traffic Manager returns the highest-priority endpoint that is healthy.
* The resolver returns that endpoint IP to the client, and the client connects directly.

Example endpoint priorities:

* Primary — Priority 1
* Failover A — Priority 2
* Failover B — Priority 3

Behavior: If Primary is unhealthy, Traffic Manager returns Failover A (Priority 2). If both Primary and Failover A are unhealthy, it returns Failover B. This implements a straightforward active-passive failover pattern ideal for defined recovery tiers.

<Frame>
  <img alt="The image illustrates the priority-based traffic routing method in Microsoft's Azure Traffic Manager, depicting the flow from the user to endpoints based on status and priority. It includes a table with endpoint priorities and their statuses, with primary degraded and failovers online." />
</Frame>

## Weighted

Use case: Gradual rollouts, A/B tests, canary releases, and controlled traffic distribution.

Flow summary:

* The client’s resolver queries Traffic Manager.
* Traffic Manager considers only healthy endpoints that have configured weights.
* Each endpoint is selected probabilistically based on its weight value.
* The selected endpoint’s IP is returned to the resolver; the client connects directly.

Example weights:

* West A — weight 5
* Region B — weight 50

Behavior: An endpoint with weight 50 receives a proportionally larger share of DNS responses than one with weight 5. Health probes ensure unhealthy endpoints are excluded from distribution.

<Frame>
  <img alt="The image is a flowchart illustrating the weighted traffic routing method in Microsoft Azure Traffic Manager, showing how user requests are routed based on weights assigned to different endpoints with their status." />
</Frame>

## Performance

Use case: Route clients to the lowest-latency endpoint for improved responsiveness.

Flow summary:

* The resolver forwards the DNS query to Traffic Manager.
* Traffic Manager uses the source IP of the DNS query and an internal latency table to map the query to the closest endpoint.
* Unhealthy endpoints are filtered by health probes.
* The lowest-latency healthy endpoint is returned to the resolver; the client connects directly.

Example:

* Source IP `89.17.0.16` maps to West US (15 ms). If West US is healthy, that endpoint is returned. If it is unhealthy, Traffic Manager selects the next lowest-latency healthy endpoint (e.g., North Europe at 17 ms).

Behavior: Performance routing optimizes for minimal latency from the client’s location and is suited to globally distributed services where response time is critical.

<Frame>
  <img alt="The image illustrates the performance-based traffic routing method in Microsoft Azure, showing how a user request is managed by the Traffic Manager using latency data to determine the closest available endpoint." />
</Frame>

## Geographic

Use case: Enforce data residency, comply with regional regulations, serve localized content or language.

Flow summary:

* The resolver sends the DNS query to Traffic Manager.
* Traffic Manager determines the geographic region of the resolver’s source IP.
* It maps that geography to a configured endpoint or a nested Traffic Manager profile.
* The assigned endpoint or nested profile is returned to the resolver.
* The client is directed to the region-specific endpoint.

Example mapping:

* Endpoint 1 — Germany
* Nested profile — Mexico and Asia
* Endpoint 2 — Rest of world

Behavior: Queries from Germany return Endpoint 1. Queries from Asia return the nested profile (which then resolves to endpoints in that nested profile). Requests from unmapped regions fall back to a default endpoint. Geographic routing is useful for compliance (data locality), localized user experience, or directing users to region-specific services.

<Frame>
  <img alt="The image illustrates a geographic traffic routing method using Microsoft Azure's Traffic Manager, detailing how user requests are directed to endpoints based on their geographic region through a DNS service." />
</Frame>

## Quick Comparison

| Routing Method      |                           Primary Goal | Typical Use Cases                                       |
| ------------------- | -------------------------------------: | ------------------------------------------------------- |
| Priority (Failover) |   High availability via active-passive | Disaster recovery, single primary with hot/warm backups |
| Weighted            |        Controlled traffic distribution | Canary releases, A/B testing, gradual rollouts          |
| Performance         |             Lowest latency for clients | Global applications that need best response times       |
| Geographic          | Region-specific routing and compliance | Data residency, localized content, language selection   |

## Best practices and considerations

* Health probes: Configure appropriate probe endpoints and frequency to quickly detect failures without causing false positives.
* DNS TTL: DNS caching affects how quickly clients switch endpoints after a change. Use shorter `TTL` for rapid failover, but consider increased DNS query volume.
* Monitoring: Combine Traffic Manager metrics with application telemetry to validate endpoint health and routing behavior.
* Nested profiles: Use nested profiles in Geographic routing to simplify mappings for large regions.

> **warning** Remember: DNS caching and resolver behavior can delay failover. Even after Traffic Manager changes DNS answers, clients may keep using cached records until the TTL expires. Plan probe intervals and TTL values to balance failover speed and DNS query load.

## Summary

* Azure Traffic Manager makes DNS-level routing decisions using routing methods: Priority, Weighted, Performance, and Geographic.
* Health probes exclude unhealthy endpoints from DNS responses to improve reliability.
* Clients always connect directly to the chosen endpoint — Traffic Manager does not proxy user traffic.
* Choose the routing method that matches your goals:
  * Priority for active-passive failover,
  * Weighted for staged rollouts or experiments,
  * Performance for latency optimization,
  * Geographic for regulatory or localization needs.

## Links and references

* Azure Traffic Manager documentation: [https://learn.microsoft.com/azure/traffic-manager/](https://learn.microsoft.com/azure/traffic-manager/)
* Routing policy concepts and examples: [https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods](https://learn.microsoft.com/azure/traffic-manager/traffic-manager-routing-methods)
* DNS TTL and caching: [https://tools.ietf.org/html/rfc1035](https://tools.ietf.org/html/rfc1035)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/38ad64e6-12ba-4187-955b-c2e4522be498/lesson/0891ec92-c30d-4253-b9d6-0768c6d4b091)
