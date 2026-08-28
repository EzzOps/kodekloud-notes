# Create a Front Door in the Azure portal

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Azure-Front-Door/Create-a-Front-Door-in-the-Azure-portal/page

Guide to creating and configuring Azure Front Door via the Azure portal, covering deployment paths, SKU selection, endpoint naming, origin configuration, routing, caching, and security

Create an Azure Front Door instance from the Azure portal. This walkthrough explains the portal experience and highlights the key decisions you'll make during deployment: deployment path, SKU selection, endpoint naming, and origin (backend) configuration. Follow the Custom Create path when you need precise control over routing, caching, and security; use Quick Create for a fast, sensible-default deployment.

When you begin in the portal, you’ll see a comparison of Azure Front Door and related CDN options and two primary deployment paths:

* Quick Create: Fast deployment with sensible defaults for backend pools, routing, and caching.
* Custom Create: Full control over backend pools, routing rules, caching, rewrite rules, health probes, and security (WAF policies, IP restrictions, Private Link).

Next you must pick the SKU: Standard or Premium. Choose Standard for most global load-balancing and performance scenarios (global Layer 7 routing, caching, TLS termination, optional compression). Choose Premium when you need advanced security and enterprise features—richer Web Application Firewall (WAF) capabilities, Private Link integration, and additional controls for regulated or security-sensitive workloads.

You will also be asked to provide a globally unique name for your Front Door endpoint. This name becomes part of the public DNS for the default Front Door hostname (for example, `your-frontdoor-name.azurefd.net`). Pick a concise, descriptive name that reflects the application and environment.

<Frame>
  <img alt="The image provides instructions for creating a Front Door in the Azure portal, detailing steps such as choosing a deployment method, selecting an SKU, and entering a unique endpoint name. It also compares Azure Front Door offerings, including a choice between Quick Create and Custom Create options." />
</Frame>

Pick a concise, descriptive name for the endpoint (for example, `myapp-prod`) so the default endpoint would be:

```text theme={null}
https://myapp-prod.azurefd.net
```

<Callout icon="lightbulb">
  The portal validates the endpoint name for global uniqueness. If you plan to use a custom domain (for example, `www.contoso.com`), map it to the Front Door endpoint later and enable managed certificates or bring your own TLS certificate.
</Callout>

After choosing a name, define the backend(s) (origins) that Front Door will route traffic to. Supported origin types include:

* Azure App Service (Web Apps)
* Azure Storage (static website hosting)
* Azure Application Gateway
* Virtual machines or VM scale sets (public IPs)
* Any external origin reachable over HTTP/HTTPS

Use the following settings when configuring each origin (typical):

* Origin hostname
* Port (80/443 by default)
* Origin host header (override when needed)
* Weight (for load balancing across origins)
* Health probe settings (probe path, interval, and match criteria)

Table: Origin types and typical use cases

| Origin type         | Typical use case                                                 |
| ------------------- | ---------------------------------------------------------------- |
| Azure App Service   | Dynamic web apps and APIs hosted in App Service                  |
| Azure Storage       | Static websites and assets (HTML, JS, images)                    |
| Application Gateway | Internal app gateway for WAF/Layer 7 within Azure                |
| VMs / VM scale sets | Custom workloads, legacy apps with public IPs                    |
| External origins    | Third-party services or on-premises endpoints exposed over HTTPS |

In Custom Create you can also configure backend pools, routing rules, caching policies, request/response rewrite rules, and security settings such as Web Application Firewall (WAF) policies and IP restrictions.

<Frame>
  <img alt="The image explains how to create a Front Door in the Azure portal, detailing the steps for selecting a deployment method, SKU, endpoint name, and origin type. It also includes a comparison of offerings and quick create options." />
</Frame>

When you finalize deployment, Azure provisions Front Door resources and configures global anycast entry points automatically. Quick Create applies defaults so you can be running quickly; Custom Create lets you fine-tune every aspect—use it when you need specific routing logic, advanced security, or custom caching and rewrite rules.

This walkthrough demonstrates the Custom Create path to show how to fine-tune backend pools, routing rules, and security settings.

Links and references

* [Azure Front Door documentation](https://learn.microsoft.com/azure/frontdoor/)
* [Create and configure Azure Front Door (portal)](https://learn.microsoft.com/azure/frontdoor/quickstart-create-front-door)
* [Azure Front Door Security and WAF guidance](https://learn.microsoft.com/azure/frontdoor/front-door-waf-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/705deb1d-f387-4bab-9642-e9838d1a0c4c/lesson/04505329-38ec-4c47-b93c-dda5d36a09eb" />
</CardGroup>
