# Distributed Denial of Service DDoS

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-Azure-DDoS-Protection/Distributed-Denial-of-Service-DDoS/page

Overview of Distributed Denial of Service attacks, their categories, botnet amplification, and layered defenses including Azure-specific protections like DDoS Protection Standard and WAF

In this lesson we’ll cover Distributed Denial of Service (DDoS) attacks: what they are, how they work, common attack categories, and practical defenses — including cloud-native patterns and Azure-specific examples. DDoS is one of the most common and disruptive threats to online services because it uses many distributed, compromised devices (a botnet) to overwhelm a target’s capacity.

At a high level:

* A DDoS attack uses many compromised devices — desktops, servers, or IoT devices — to generate large volumes or specially crafted traffic toward a single target.
* Because traffic originates from many distributed sources, it’s harder to filter and more powerful than a single-source attack.
* The impact can be exhausted network bandwidth, consumed server CPU/memory, or depleted protocol state (connection tables), preventing legitimate users from reaching the service.

## How botnets amplify impact

Infected devices in a botnet are typically controlled remotely by attackers; their owners are often unaware. When thousands of these devices simultaneously generate traffic, the aggregate load can:

* saturate upstream or on-premises network links,
* overwhelm load balancers, firewalls, or application servers,
* exhaust protocol state (for example, TCP connection tables), and
* trigger cascading failures in dependent services.

## DDoS attack categories

DDoS attacks are commonly grouped into three categories: volumetric, protocol (state-exhaustion), and application-layer (Layer 7). Each targets different resources and requires different mitigation strategies.

| Category                    |                         Target / Goal | Common vectors                                                 | Characteristics                                                   | Typical mitigation                                                              |
| --------------------------- | ------------------------------------: | -------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Volumetric                  |          Network bandwidth saturation | UDP floods, DNS/NTP amplification, IP spoofing & amplification | Very high bandwidth; aims to exhaust link capacity                | Upstream absorption/scrubbing, CDN/edge services, rate limiting                 |
| Protocol (state-exhaustion) |     Network/transport layer resources | SYN floods, fragmented packets, connection-state exhaustion    | Low-to-moderate bandwidth but exhausts connection or memory state | Network hardening, filtering, stateful inspection, SYN cookies                  |
| Application-layer (Layer 7) | Application server resources or logic | HTTP floods, slow POST / slowloris, SQLi, XSS, abusive bots    | Mimics legitimate requests; harder to distinguish from real users | Web Application Firewall (WAF), bot management, input validation, rate limiting |

### Volumetric attacks

Volumetric attacks try to saturate the target’s network link by generating huge amounts of traffic. Common examples include UDP floods and amplification attacks that leverage spoofed source IPs.

<Frame>
  <img alt="The image describes types of DDoS attacks, focusing on volumetric attacks, and explains how Azure handles them by absorbing and scrubbing fake network traffic such as UDP floods, amplification, and spoofed packets." />
</Frame>

Mitigation: volumetric attacks are typically absorbed at the network edge or by upstream scrubbing centers (CDNs, cloud DDoS protection services) that can filter and drop attack traffic before it reaches your infrastructure.

### Protocol (state-exhaustion) attacks

Protocol attacks exploit weaknesses in network and transport protocols (OSI layers 3 and 4). Examples include SYN floods, malformed or fragmented packets, and attacks designed to consume connection state in firewalls, load balancers, or servers.

<Frame>
  <img alt="The image outlines types of DDoS attacks, specifically focusing on protocol attacks, with Azure's mitigation strategies." />
</Frame>

Mitigation: tune TCP/IP stacks, enable SYN cookies, use network-level filtering and connection limits, and place stateful defenses upstream where they can drop suspicious traffic.

### Application-layer (Layer 7) attacks

Application-layer attacks target the application itself (OSI layer 7), often by mimicking valid user behavior to exhaust server-side resources or by exploiting application vulnerabilities (e.g., SQL injection, XSS).

<Frame>
  <img alt="The image is a diagram explaining types of DDoS attacks, specifically focusing on resource (application) layer attacks such as HTTP violations, SQL injection, and XSS, with defense strategies like Application Gateway WAF and DDoS protection." />
</Frame>

Mitigation: application-aware defenses are required — Web Application Firewalls (WAFs), bot management, strict input validation, authentication and authorization checks, and per-client rate limiting.

> **lightbulb** Combine network-level DDoS protection (to absorb volumetric and protocol attacks) with an application-layer WAF to block malicious requests and exploit attempts. In Azure, common implementations are `DDoS Protection Standard` together with `Application Gateway WAF` or `Azure Front Door with WAF`. See the references below for more details.

## Defenses and best practices

A layered, defense-in-depth approach is recommended for cloud-hosted applications:

* Network-level protections
  * Use cloud DDoS protection services or CDNs to absorb and scrub traffic.
  * Rate-limit and filter at the edge; apply ingress ACLs and geo-blocking when appropriate.
* Protocol-level hardening
  * Tune OS TCP/IP stacks, enable SYN cookies, and configure connection limits on load balancers and firewalls.
  * Drop obviously malformed packets or extreme anomalies early.
* Application-layer defenses
  * Deploy a WAF and tune rulesets for your application’s traffic patterns.
  * Implement robust input validation, authentication, and per-client throttling.
  * Use bot management to distinguish legitimate users from automated traffic.

Operational recommendations:

* Maintain an incident response plan and run DDoS drills.
* Monitor traffic baselines with telemetry and set alerts for sudden deviations.
* Use autoscaling where possible, but avoid scaling blindly during attacks without upstream protection — autoscaling can increase cost without addressing upstream network saturation.

## Quick reference table

| Focus                                | Example controls                                                 |
| ------------------------------------ | ---------------------------------------------------------------- |
| Absorb large-scale traffic           | `DDoS Protection Standard`, CDN, Azure Front Door                |
| Block malicious application requests | Application Gateway WAF, custom WAF rules                        |
| Reduce protocol exhaustion           | SYN cookies, connection throttling, stateful inspection          |
| Identify bots & abuse                | Bot management services, behavioral analysis                     |
| Operational readiness                | Playbooks, runbooks, monitoring, and run periodic failover tests |

## Links and references

* [Azure DDoS Protection overview](https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview)
* [Azure Application Gateway WAF overview](https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/ag-overview)
* [Azure Front Door documentation](https://learn.microsoft.com/en-us/azure/frontdoor/)
* OWASP: [Denial of Service (DoS) risks and mitigation guidance](https://owasp.org/)

Key takeaway: DDoS is best handled with multiple layers — an upstream, high-capacity protection service to absorb volumetric and protocol attacks, combined with application-layer defenses (WAF, rate-limiting, bot mitigation) to protect application logic and user experience.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/2dfc3e6d-61ae-4c3c-a71d-559cd1e302af/lesson/1354e80b-c5de-4a62-9bc8-0a63a61e4763)
