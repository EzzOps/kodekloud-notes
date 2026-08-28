# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Azure-Application-Gateway/Introduction/page

Overview of designing and deploying Azure Application Gateway, covering components, traffic flow, SKUs, WAF, TLS strategies, high availability, monitoring, and production planning.

Welcome to this lesson on designing Azure Application Gateway.

Azure Application Gateway is Microsoft’s Layer 7 (application layer) load balancer that provides advanced routing and security for HTTP/HTTPS traffic. In this lesson you’ll learn the core concepts, how request traffic flows through the gateway, how to choose the right SKU, and key planning considerations for production deployments.

<Callout icon="lightbulb">
  This lesson focuses on conceptual and architectural aspects of Azure Application Gateway. Practical examples and configuration steps will be covered in later sections.
</Callout>

Learning objectives

* Understand core Application Gateway capabilities: SSL offloading, end-to-end TLS, path-based routing, host-based routing, and integration with Azure Web Application Firewall (WAF).
* Learn the traffic lifecycle inside Application Gateway: listeners, rules, HTTP settings, backend pools, and health probes — and how they work together to process user requests.
* Compare and choose the appropriate SKU (Standard, Standard\_v2, WAF, WAF\_v2) by evaluating scale, features, performance, and security trade-offs.
* Plan for production: high availability, autoscaling, network topology, TLS/certificate strategies, monitoring, and integration with other Azure networking services.

By the end of this lesson, you should be able to make informed decisions about when and how to use Azure Application Gateway in your solutions.

## Core concepts and primary components

Understand these components and how they fit together when designing solutions with Application Gateway:

| Component                      | Purpose                                                                          | Example / Notes                                       |
| ------------------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Listener                       | Accepts incoming client connections (IP + port + protocol)                       | HTTP/HTTPS listener on port 80/443                    |
| Rule                           | Maps a listener to a backend pool and HTTP settings (basic or path-based)        | Path-based rule: `/images/*` routes to `img-backend`  |
| Backend pool                   | Set of backend targets (VMs, scale sets, IPs, FQDNs, or App Service)             | `my-app-backend` with two VMSS instances              |
| HTTP settings                  | Connection behavior to backend (protocol, port, cookie-based affinity, timeouts) | Offload TLS at gateway or use end-to-end TLS          |
| Health probe                   | Monitors backend health and drives routing decisions                             | Custom probe path `/health` with 200 response         |
| Web Application Firewall (WAF) | Protects web apps from common attacks (OWASP rules)                              | WAF\_v2 supports autoscaling and improved performance |

<Callout icon="lightbulb">
  Tip: Use path-based routing and host-based routing to reduce the number of public IPs and consolidate multiple sites behind a single Application Gateway.
</Callout>

## How traffic flows through Application Gateway (end-to-end)

A clear step-by-step view of request processing helps with design and troubleshooting:

1. DNS resolves the public IP or FQDN of the Application Gateway.
2. The client initiates an HTTP/HTTPS request to the gateway IP/FQDN.
3. Listener on the gateway accepts the connection (binds to IP, port, protocol).
4. Listener matches a rule (basic or path-based) that decides which backend pool to use.
5. HTTP settings define how the gateway connects to the backend (protocol, port, affinity, timeout).
6. Gateway performs a health probe against backend targets; only healthy targets receive traffic.
7. If WAF is enabled, the request is inspected against WAF rules before being forwarded.
8. Gateway forwards the request to a chosen backend target and relays the backend response to the client.

Example: path-based routing decision (conceptual)

```text theme={null}
Client: GET https://www.contoso.com/images/logo.png
Listener: HTTPS on port 443
Rule: Path-based /images/* -> backend pool 'image-servers'
HTTP settings: Use HTTP to backend on port 8080 (TLS offloaded at gateway)
```

## Choosing the right SKU: Standard vs Standard\_v2 vs WAF vs WAF\_v2

Key differences include autoscaling, performance, feature parity, and pricing. Consider workload patterns, required features (e.g., WAF), and operational model (manual vs autoscale).

| SKU          | Autoscaling         | WAF Support | Common use cases                                                |
| ------------ | ------------------- | ----------- | --------------------------------------------------------------- |
| Standard     | No (manual scaling) | No          | Simple L7 load balancing, dev/test                              |
| Standard\_v2 | Yes (autoscale)     | No          | Production apps needing autoscale and faster provisioning       |
| WAF          | No (manual scaling) | Yes         | Apps requiring web protection (manual scaling)                  |
| WAF\_v2      | Yes (autoscale)     | Yes         | Production secured apps with autoscaling and improved telemetry |

When to choose WAF\_v2:

* You need managed WAF protections (OWASP rules, custom rules).
* You want autoscaling, faster updates, and improved performance telemetry.
* You require zone-redundant, highly available architecture.

Useful reference: [Azure Application Gateway pricing and SKUs](https://learn.microsoft.com/azure/application-gateway/).

## Real-world deployment considerations

* High availability and redundancy
  * Deploy across availability zones (when supported) and use multiple backend instances.
  * Consider Standard\_v2/WAF\_v2 for built-in autoscaling and zone redundancy.
* Network topology
  * Application Gateway must be deployed in a virtual network subnet dedicated to the gateway.
  * Integrate with Azure Front Door or Azure CDN for global traffic routing or static content distribution.
* TLS and certificate management
  * Decide whether to offload TLS at the gateway (simpler) or use end-to-end TLS for strict security.
  * Use Key Vault to centrally manage certificates and integrate with automation.
* Health probes and resiliency
  * Configure custom probes and sensitivity settings to avoid routing to unhealthy instances.
* Security and WAF tuning
  * Use a staged approach to WAF rules: Detection mode first, then Prevention after tuning.
  * Monitor false positives and create custom rules when needed.
* Monitoring and logging
  * Enable diagnostics logging, metrics, and Azure Monitor alerts for latency, throughput, and WAF events.
  * Centralize logs with Log Analytics or SIEM for analysis.
* Cost and scaling patterns
  * Evaluate traffic patterns; autoscaling (v2 SKUs) reduces operational overhead for variable traffic loads.

## Quick conceptual example: HTTP setting JSON (illustrative)

This is a conceptual example showing settings you configure for backend communication. Actual deployment uses ARM templates, Azure CLI, or the portal and will include more properties.

```json theme={null}
{
  "name": "appGatewayBackendHttpSettings",
  "port": 8080,
  "protocol": "Http",
  "cookieBasedAffinity": "Disabled",
  "pickHostNameFromBackendAddress": false,
  "probe": {
    "name": "appGatewayProbe"
  }
}
```

## Summary

Azure Application Gateway is a powerful Layer 7 load balancer providing advanced routing, TLS handling, and optional WAF protections. Use Standard\_v2 or WAF\_v2 for production scenarios where autoscaling, improved performance, and managed security are required. Design thoughtfully around listeners, rules, backend pools, and HTTP settings, and plan for HA, monitoring, and certificate management.

## Links and references

* [Azure Application Gateway documentation](https://learn.microsoft.com/azure/application-gateway/)
* [Azure Web Application Firewall (WAF)](https://learn.microsoft.com/azure/web-application-firewall/)
* [Azure networking architecture center](https://learn.microsoft.com/azure/architecture/)
* [Azure Monitor for Application Gateway metrics and diagnostics](https://learn.microsoft.com/azure/application-gateway/application-gateway-diagnostics)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/50c3966d-1fc5-45b0-8339-5c8be2ce49c3/lesson/c5d13f9d-ea45-446f-8ab5-69381a17852a" />
</CardGroup>
