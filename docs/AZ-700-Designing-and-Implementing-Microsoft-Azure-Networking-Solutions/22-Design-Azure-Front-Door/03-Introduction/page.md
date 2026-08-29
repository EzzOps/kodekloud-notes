# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Azure-Front-Door/Introduction/page

Guide to designing and configuring Azure Front Door for global Layer 7 routing, load balancing, security, SKUs, backend pools, health probes, TLS, and deployment best practices.

Designing Azure Front Door

If your application requires a global entry point with Layer 7 (HTTP/HTTPS) capabilities, Azure Front Door is the appropriate service. Unlike Application Gateway, which is a regional Layer 7 service, Front Door offers global load balancing, edge routing, and additional performance and security features delivered from Microsoft's global points-of-presence (POPs).

> **lightbulb** Azure Front Door provides a global, scalable entry point for your applications—combining load balancing, application acceleration, and security features on Microsoft's global network.

This lesson/article will walk you step-by-step through Azure Front Door: what it does, how to choose the right SKU, how to design routing and backend pools, how to configure health probes, and how to secure traffic end-to-end.

## Learning objectives (what you'll learn)

1. Understand the role and advantages of Azure Front Door as a global Layer 7 entry point.
2. Compare the Standard and Premium SKUs to choose the right option for your scenario.
3. Deploy Azure Front Door using Quick (wizard) and Custom (full configuration) creation flows.
4. Configure routing rules, path-based routing, host/header matches, and secure redirection (e.g., HTTP → HTTPS).
5. Define backend endpoints, origin types, backend pools, and host header settings.
6. Configure health probes for reliable failover and availability.
7. Apply SSL/TLS certificates and enable secure end-to-end connections.

***

## What Front Door provides (high level)

* Global load balancing and edge routing using Microsoft's POPs for improved latency and availability.
* Layer 7 intelligent routing: path-based, header-based, and priority/fallback routing.
* Performance features: caching at the edge, TLS termination at POPs, and connection optimizations.
* Security features: TLS termination, Web Application Firewall (WAF) integration, bot protection, and advanced policy controls (Premium).

***

## Comparing SKUs

Use the table below to quickly compare core differences between the Standard and Premium SKUs. Choose Standard for common global load balancing and acceleration needs; choose Premium when you require advanced security controls and deeper integration with private origins.

| Feature / Capability                 |                Standard SKU |                                                 Premium SKU |
| ------------------------------------ | --------------------------: | ----------------------------------------------------------: |
| Global HTTP(s) load balancing        |                           ✓ |                                                           ✓ |
| Edge caching & acceleration          |                           ✓ |                                                           ✓ |
| Managed TLS certificates             |                           ✓ |                                                           ✓ |
| Web Application Firewall (WAF)       |                   Basic WAF |                                     Advanced WAF & policies |
| Advanced security controls           |                           — |                                                           ✓ |
| Integration with private backends    |                     Limited |            Enhanced (private link & private origin support) |
| Advanced routing and transform rules |                       Basic |                        Enhanced rule options and transforms |
| Recommended for                      | Most public-facing web apps | Enterprise security, private backends, complex policy needs |

***

## Deployment approaches

Decide between a quick setup for simple use cases and a custom setup for production-ready, complex architectures.

| Approach                          |                    When to use | What you configure                                                                                     |
| --------------------------------- | -----------------------------: | ------------------------------------------------------------------------------------------------------ |
| Quick creation (wizard)           |       Rapid prototyping, demos | Basic frontend host, single backend pool, default routing                                              |
| Custom creation (full experience) | Production, complex topologies | Multiple frontend hosts, multiple routing rules, caching, WAF policies, custom probes, origin settings |

Quick creation is ideal to validate concepts quickly; custom creation gives you control over frontend hosts, detailed routing, probe tuning, and policy applications recommended for production.

***

## Routing, redirects, and request transforms

Routing rules determine how Front Door matches and forwards requests. Common patterns:

* Path-based routing: route `/api/*` to API backends and `/static/*` to CDN-backed storage.
* Header-based matches: route based on `Host`, `User-Agent`, or custom headers.
* Priority & fallback: primary backend with one or more fallback pools when the primary is unhealthy.
* Redirect rules: enforce `HTTP → HTTPS`, canonical hostnames, or legacy path redirects.
* Rewrite rules: rewrite request/response headers, or modify URLs/paths before forwarding to the origin.

Best practices:

* Use redirect rules to enforce HTTPS and canonical hostnames for SEO and user experience.
* Use rewrite rules only when backends require a specific host header or path format.

***

## Backends and origin types

Front Door supports a variety of origin types. Typical origins include:

* Azure App Service
* Azure Storage static websites
* Public IP addresses
* Virtual machines
* Kubernetes ingress controllers
* External hostnames and third-party origins

Backend pools group origins and define:

* Load balancing settings (priority, weight, session affinity)
* Health probe settings (protocol, path, interval)
* Host header behavior (use incoming host, custom host header, or override with origin hostname)

Example origin decision flow:

* Public static assets → Azure Storage static website or CDN
* API endpoints → App Service or Kubernetes ingress
* Private/internal services → Premium SKU with private origin support

***

## Health probes

Health probes are essential for automated failover and availability. Configure probes to match the health-check endpoints implemented by your application.

Probe settings to tune:

* Protocol: `HTTP` or `HTTPS`
* Path: e.g., `/healthz` or `/status`
* Interval: probe frequency (seconds)
* Timeout: how long to wait for a response
* Unhealthy threshold: number of consecutive failures before marking origin unhealthy
* Healthy threshold: number of successes to mark origin healthy again

Table: probe configuration example

| Parameter           | Example value | Notes                                                               |
| ------------------- | ------------: | ------------------------------------------------------------------- |
| Protocol            |       `HTTPS` | Use HTTPS when backend supports TLS for end-to-end encryption       |
| Path                |    `/healthz` | Implement a lightweight endpoint that returns 200 for healthy state |
| Interval            |         `30s` | Balance probe sensitivity vs. request overhead                      |
| Timeout             |          `5s` | Avoid long-running probes that delay failover                       |
| Unhealthy threshold |           `3` | Three consecutive failures -> mark unhealthy                        |

Tune probes so that transient errors don’t cause unnecessary failovers but failures are detected quickly enough for good availability.

***

## SSL/TLS and secure end-to-end

Front Door supports TLS termination at the edge and secure connections to backends.

Key options:

* Edge TLS termination: Azure-managed certificates (auto-renewed) or bring-your-own certificate.
* End-to-end TLS: Front Door communicates with your origins over HTTPS; you can set a custom host header if the backend needs a specific hostname.
* TLS policy: select allowed TLS versions and cipher suites to meet compliance and security posture.

Best practices:

* Use Azure-managed certificates for most public endpoints to simplify lifecycle management.
* For sensitive workloads or private origins, enable end-to-end TLS and validate backend certificates.
* Review allowed TLS versions and disable older, unsafe versions (e.g., TLS 1.0/1.1).

***

## Recommended design checklist

* Choose SKU based on security and private-origin needs (Standard vs Premium).
* Define frontend hosts (custom domains) and attach managed certificates.
* Create backend pools with multiple origins and appropriate health probes.
* Implement routing rules: path-based, header-based, and priority/fallback policies.
* Configure caching and compression at the edge for static content.
* Apply WAF rules and bot protections as required.
* Monitor metrics and logs (Front Door logs, WAF logs, Application Insights) to detect anomalies.

***

## Links and references

* Azure Front Door overview: [https://learn.microsoft.com/azure/frontdoor/front-door-overview](https://learn.microsoft.com/azure/frontdoor/front-door-overview)
* Front Door Standard/Premium documentation: [https://learn.microsoft.com/azure/frontdoor/front-door-sku-comparison](https://learn.microsoft.com/azure/frontdoor/front-door-sku-comparison)
* Azure Web Application Firewall (WAF): [https://learn.microsoft.com/azure/web-application-firewall/](https://learn.microsoft.com/azure/web-application-firewall/)
* TLS best practices: [https://learn.microsoft.com/security/zero-trust/overview](https://learn.microsoft.com/security/zero-trust/overview)
* Azure managed certificates: [https://learn.microsoft.com/azure/frontdoor/front-door-managed-certificates](https://learn.microsoft.com/azure/frontdoor/front-door-managed-certificates)

This lesson will expand each section with step-by-step guidance, configuration examples, and deployment patterns to help you design and operate a resilient, secure Azure Front Door architecture.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/705deb1d-f387-4bab-9642-e9838d1a0c4c/lesson/3d690cdd-4622-4078-9997-f1449d476617)
