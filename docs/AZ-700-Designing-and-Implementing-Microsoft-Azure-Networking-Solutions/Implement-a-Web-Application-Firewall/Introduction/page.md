# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Implement-a-Web-Application-Firewall/Introduction/page

Guide to designing and implementing Azure Web Application Firewall including deployment options, rule management, tuning, and integration with Azure Front Door for global protection.

This lesson explains how to design and implement a Web Application Firewall (WAF) on Azure. It focuses on practical configuration, rule management, and integration patterns so you can protect web applications from common threats while minimizing false positives.

By the end of this article you'll understand:

* What a WAF is and which attacks it defends against (for example, SQL injection, cross-site scripting, and other [OWASP Top 10](https://owasp.org/www-project-top-ten/) threats).
* WAF operating modes: detection (logging/monitoring) versus prevention (blocking malicious requests).
* Rules and rule groups: the difference between managed/default rule sets and custom rules, and when to use each.
* How to integrate WAF with Azure Front Door to provide centralized edge protection for globally distributed applications.

A WAF inspects HTTP/HTTPS traffic destined for your application and applies rule logic to identify and mitigate malicious requests. In Azure, you typically configure WAF to operate in one of two modes:

* Detection mode: logs suspicious or malicious traffic for analysis without impacting user traffic.
* Prevention mode: actively blocks requests that match configured rules to stop attacks immediately.

<Callout icon="lightbulb">
  Use detection mode when you first enable a WAF or when you’re tuning rules. Switch to prevention only after you’ve validated rule behavior to avoid unintended blocking.
</Callout>

## Rules and rule groups

WAF rules are organized into rule groups. Azure provides managed rule sets—such as the OWASP Core Rule Set—that block many common attack patterns out of the box. Managed rule sets give broad coverage quickly; however, they can require tuning to prevent false positives for your specific application.

Custom rules let you target organization-specific threats by combining match conditions (IP address, geographic location, request URI, headers, query string, rate thresholds) with actions (Allow, Block, or Log) and a priority. You can also define rate-limiting rules to throttle abusive clients.

Common custom-rule examples:

* Block requests from specific countries or IP ranges.
* Block or rate-limit requests to a specific path (for example, repeated requests to a login endpoint).
* Block requests that exceed a configured request size or contain suspicious headers.

<Frame>
  <img alt="The image lists learning objectives related to understanding and operating Web Application Firewalls (WAF), including their modes, rules, and custom rule creation. It has a gradient background and step numbers." />
</Frame>

## Azure WAF deployment options

Azure supports multiple WAF deployment models. Each option has trade-offs for global reach, latency, and the feature set available:

| Deployment option                |                                                             Best for | Notes / links                                                                                                                                                                                                              |
| -------------------------------- | -------------------------------------------------------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WAF on Azure Application Gateway | Azure-hosted applications needing Layer 7 protection within a region | Ideal for regional PaaS/IaaS backends. See Azure Application Gateway WAF docs: [https://docs.microsoft.com/azure/application-gateway/waf-overview](https://docs.microsoft.com/azure/application-gateway/waf-overview)      |
| WAF on Azure Front Door          |             Global, low-latency edge protection for distributed apps | Applies policies at the edge to protect multiple backends and reduce latency. See Azure Front Door WAF: [https://docs.microsoft.com/azure/frontdoor/waf-overview](https://docs.microsoft.com/azure/frontdoor/waf-overview) |
| WAF capabilities in Azure CDN    |                               Static content and CDN edge protection | Some CDN SKUs include basic WAF features; useful for protecting cached content and reducing origin load. See Azure CDN docs: [https://docs.microsoft.com/azure/cdn/](https://docs.microsoft.com/azure/cdn/)                |

When to choose each:

* Use Application Gateway WAF when you require deep integration with Azure VNets, private backends, or per-region routing.
* Use Azure Front Door WAF to protect globally distributed apps and apply centralized security rules at the edge.
* Use CDN-integrated WAF when you primarily serve static assets and want basic edge-level request filtering.

## Tuning, testing, and best practices

* Start in detection mode to collect logs and analyze rule hits before enabling prevention. Review false positive events and add exclusions or custom rules as needed.
* Apply rate-limiting rules for high-risk endpoints (e.g., authentication or API endpoints) to mitigate brute-force and scraping attacks.
* Combine managed rules with targeted custom rules rather than wholesale disabling managed rule groups. Disable only the specific rules that cause false positives.
* Use prioritized custom rules to allow trusted traffic that would otherwise be blocked by managed rules (for example, internal health probes).
* Integrate WAF logs with Azure Monitor, Log Analytics, or SIEM for alerting and incident response.

## What this article covers

This article walks through how to choose the right WAF deployment for your scenario, tune managed rule sets, and implement common custom rules to address application-specific threats. It also demonstrates integrating Azure WAF with Azure Front Door for centralized, global protection.

## Links and references

* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* Azure WAF on Application Gateway: [https://docs.microsoft.com/azure/application-gateway/waf-overview](https://docs.microsoft.com/azure/application-gateway/waf-overview)
* Azure Front Door WAF: [https://docs.microsoft.com/azure/frontdoor/waf-overview](https://docs.microsoft.com/azure/frontdoor/waf-overview)
* Azure CDN documentation: [https://docs.microsoft.com/azure/cdn/](https://docs.microsoft.com/azure/cdn/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/4339a7c9-9465-4ca0-ba30-4ee56ed54bf1/lesson/1893f8c6-e845-437a-a3f8-2cee0e64db09" />
</CardGroup>
