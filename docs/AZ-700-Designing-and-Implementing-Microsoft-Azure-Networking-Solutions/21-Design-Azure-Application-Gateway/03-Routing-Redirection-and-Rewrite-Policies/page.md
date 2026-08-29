# Routing Redirection and Rewrite Policies

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-Azure-Application-Gateway/Routing-Redirection-and-Rewrite-Policies/page

Practical guide to Azure Application Gateway routing, URL redirection, rewrite policies and a portal walkthrough for path based routing and backend configuration

This article explains how Azure Application Gateway handles three core responsibilities for web front-ends: request routing, URL redirection, and rewrite policies. These features help you build secure, scalable, and high-performance application delivery in Azure.

> **lightbulb** This guide focuses on practical configuration patterns—basic vs path-based routing, common redirection scenarios, and rewrite rules—plus a step-by-step Azure Portal walkthrough to create an Application Gateway that routes /api and /images paths to separate backend pools.

## 1. Request routing rules

Routing rules determine how incoming HTTP(S) requests are mapped to backend pools. Every routing rule must be associated with a listener (the listener accepts traffic on a specific protocol, port, and hostname) and HTTP settings.

Two primary rule types:

| Rule type          | When to use                                        | Behavior / Example                                                                              |
| ------------------ | -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Basic              | Single backend for all traffic matching a listener | All traffic on the listener goes to one backend pool (simplest setup)                           |
| Path-based routing | Multiple backends depending on request URL path    | Route `/api/*` → API backend, `/images/*` → Image backend; the most specific path match applies |

Path-based routing selects the most specific matching path pattern for a request. When designing path patterns, be deliberate about ordering and specificity—within a single routing rule, the gateway applies the first matching pattern.

<Frame>
  <img alt="The image shows a diagram of &#x22;Application Gateway Request Routing Rules,&#x22; detailing rule types as basic and path-based, with a menu highlighting associated backend pools." />
</Frame>

Path-based routing is especially useful to separate workloads (for example, static assets vs APIs), enabling independent scaling, deployment, and optimization for each service.

<Frame>
  <img alt="The image illustrates configuring URL path-based routing, showing how requests to specific URL paths are directed to designated backend server pools via an application gateway. It includes examples, such as requests to &#x22;/images/&#x22; directed to an Image Server Pool and &#x22;/video/&#x22; to a Video Server Pool." />
</Frame>

Benefits of path-based routing:

* Scalability: scale image servers independently from APIs.
* Performance: route static content to optimized servers or CDN frontends.
* Operational separation: different teams can own different backends.

## 2. URL Redirection

Redirection rules forward clients to different URLs or protocols based on conditions. Common scenarios include upgrading HTTP to HTTPS and migrating or consolidating endpoints.

Redirection types:

* Global redirection: redirect all requests from one listener to another (typical HTTP → HTTPS).
* Path-based redirection: redirect only requests that match certain paths (for example, `/cart/*`).
* Redirect to external site: send traffic to an external URL (configured with a dedicated redirect setting).

Supported HTTP redirect status codes:

| Status code | Meaning                               |
| ----------- | ------------------------------------- |
| 301         | Permanent redirect                    |
| 302         | Temporary redirect (Found)            |
| 303         | See Other                             |
| 307         | Temporary Redirect (preserves method) |

<Frame>
  <img alt="The image illustrates configuring redirection in an application gateway, highlighting global redirection, which directs traffic from one listener to another, usually for HTTP to HTTPS redirection. It includes a sidebar with different redirection options." />
</Frame>

<Frame>
  <img alt="The image shows a configuration interface for path-based redirection, used to set up URL redirection for specific paths like &#x22;/cart/*&#x22;." />
</Frame>

<Frame>
  <img alt="The image shows a menu for configuring redirection options with a focus on &#x22;Redirect to External Site,&#x22; and a diagram indicating how redirection works." />
</Frame>

<Frame>
  <img alt="The image shows a configuration interface for redirection types, with options like global and path-based redirection, and various HTTP status codes such as 301, 302, 303, and 307." />
</Frame>

When to choose which redirect code:

* Use 301 for permanent URL changes (search engines update indexes).
* Use 302/307 for temporary redirection (clients should continue to request the original URL later).
* Use 307 instead of 302 when you must preserve the original HTTP method (e.g., POST).

## 3. Rewrite policies

Rewrite rules let you modify HTTP requests/responses that flow through Application Gateway:

* Add, remove, or modify request and response headers (useful for security headers, or injecting tracing headers).
* Change URL path or query string values.
* Re-evaluate path-based routing after rewriting the path (re-route).

Rewrite sets are created independently and then associated with routing rules. You can add conditions so a rewrite only applies when specific criteria are met (for example, a header value or path pattern).

<Frame>
  <img alt="The image shows a tutorial on configuring rewrite policies with buttons for adding, deleting, and organizing rewrite rules in a rule set. It includes options like Request Routing Rule Association, Rewrite Condition, and Rewrite Type." />
</Frame>

Example rewrite use cases:

* Add `Strict-Transport-Security` header to responses.
* Strip internal path prefixes (`/internal-api/*` → `/api/*`) and then re-route.
* Inject A/B test headers for specific user cohorts.

## 4. Portal walkthrough: create an Application Gateway with path-based routing

This walkthrough demonstrates creating an Application Gateway in the Azure Portal that routes `/api` requests to an API backend and `/images` requests to an image backend.

Start from your Resource Group (example: `rg-az700-appgw`) that contains your backend virtual machines.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface focused on resource groups, specifically displaying details for the resource group &#x22;rg-az700-appgw&#x22; with its various management and configuration options." />
</Frame>

Step-by-step summary:

1. Create Application Gateway resource:
   * Name: e.g., `AZ70001`
   * Region: match the VMs
   * Tier: `Standard_v2` (choose `WAF_v2` if you need a managed Web Application Firewall)
   * Scale: choose instance count or enable autoscaling
   * IP type: IPv4 or dual-stack as required

<Frame>
  <img alt="The image shows a Microsoft Azure portal page for creating an application gateway. It includes fields for project and instance details, such as subscription, resource group, gateway name, region, tier, and IP address type." />
</Frame>

2. Configure the Application Gateway subnet:
   * Application Gateway requires a dedicated subnet, typically named `ApplicationGatewaySubnet`.
   * Choose an address range sized for your expected scale (e.g., `/27` if not using autoscaling).

<Frame>
  <img alt="The image shows a screenshot of the Microsoft Azure portal, specifically the &#x22;Add a subnet&#x22; page, where configuration details for a new subnet in a virtual network are being set. There are options for configuring IPv4 address space, with fields for subnet name, address range, and size." />
</Frame>

3. Frontend configuration:
   * Create or select a public IP (e.g., `AppGateway-AZ700-PIP`) for internet-facing access, or configure private frontend IP for internal scenarios.

4. Create backend pools:
   * Example names: `AppGW-AZ-700-BEP-API` and `AppGW-AZ-700-BEP-IMG`.
   * Targets: virtual machines, VMSS, NICs, IP addresses, or FQDNs.

5. Configure listeners and HTTP settings:
   * Listener: protocol (HTTP/HTTPS), port (e.g., 80 or 443), and hostname.
   * HTTP settings: backend port, protocol, cookie-based affinity (session stickiness), and health probe association.

6. Add path-based routing rules:
   * Example path mappings:
     | Path pattern | Backend pool           | HTTP setting          |
     | ------------ | ---------------------- | --------------------- |
     | `/api/*`     | `AppGW-AZ-700-BEP-API` | API HTTP settings     |
     | `/images/*`  | `AppGW-AZ-700-BEP-IMG` | IMG HTTP settings     |
     | default      | default backend        | default HTTP settings |

When adding a path-based rule, bind each pattern to the appropriate backend target and HTTP setting; define a default backend for unmatched paths.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface for creating an application gateway, specifically on the configuration step, where a user is adding a path and setting backend options." />
</Frame>

7. Review and create. Deployment may take several minutes.

<Frame>
  <img alt="The image shows a Microsoft Azure interface for creating an application gateway, displaying basic settings like subscription, resource group, and region." />
</Frame>

After deployment completes, open the Application Gateway resource from your Resource Group.

<Frame>
  <img alt="The image shows the Microsoft Azure portal screen indicating that a deployment for &#x22;Microsoft.ApplicationGateway&#x22; is complete, with options to view details and navigate to the resource group." />
</Frame>

## 5. Post-deployment management

In the Application Gateway blade you can view and manage:

* Web Application Firewall (if enabled)
* Backend pools
* Backend HTTP settings
* Frontend IP configurations
* Private link and SSL settings
* Listeners
* Rules (basic & path-based)
* Rewrite sets
* Health probes

If you did not create a custom health probe during initial configuration, add one and associate it with the HTTP settings to gain precise control over health checks.

<Frame>
  <img alt="This image shows the &#x22;Add health probe&#x22; configuration screen on the Microsoft Azure portal, where settings such as protocol, host, path, and intervals can be defined for an application gateway." />
</Frame>

Link backend targets to your pools (select VMs, IPs, or FQDN). After saving, the backend pool displays configured targets and their IPs.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface for editing a backend pool, where you can configure target types and targets, such as virtual machines and IP addresses." />
</Frame>

Updates to configuration may take a short time to propagate. Portal notifications show deployment progress and status.

<Frame>
  <img alt="The image shows the Microsoft Azure portal, specifically the &#x22;Backend pools&#x22; section of an application gateway. There are notifications on the right, indicating deployment progress and other recent activities." />
</Frame>

Once running, copy the Application Gateway public IP and test in a browser. Requests should be routed according to your path rules (for example, `/api` returns API responses).

<Frame>
  <img alt="The image shows a green screen with a message indicating &#x22;API Endpoint Active&#x22; along with server information and a note about the API backend path." />
</Frame>

Load distribution is typically round-robin across backend instances. Enable cookie-based affinity in HTTP settings if you require session persistence (sticky sessions).

If you see 404s on a path, verify:

* Path mappings in the routing rule.
* Backend content (for example, `index.html` exists in the images folder).
* Health probe results and logs.

<Frame>
  <img alt="The image shows a configuration screen for creating a routing rule in the Microsoft Azure portal. It includes options for setting up backend targets, listener settings, and path-based routing rules." />
</Frame>

## 6. Configuring rewrite rules in the portal

Create a rewrite set, add ordered rewrite rules with conditions and actions (modify headers, paths, queries), and then associate the rewrite set with the appropriate routing rule.

<Frame>
  <img alt="The image shows the Microsoft Azure portal interface for creating a rewrite set. It includes fields for naming the rewrite rule and setting a rule sequence." />
</Frame>

## 7. Health checks and backend health

Application Gateway exposes backend health status showing each instance, probe response codes (for example `200 OK`), and failing backends for troubleshooting. If you need custom health behavior, create and associate custom probes.

<Frame>
  <img alt="The image shows the &#x22;Backend health&#x22; status page of an Azure Application Gateway, indicating all backend servers are healthy, with each receiving a 200 status code." />
</Frame>

> **lightbulb** If you need more control over health checks, create and associate custom health probes with the HTTP settings. Custom probes let you define host, path, interval, and success thresholds.

## Quick reference

| Component     | Purpose                                                                   |
| ------------- | ------------------------------------------------------------------------- |
| Listener      | Accepts incoming traffic on a protocol, port, and optionally hostname     |
| Routing rule  | Binds a listener to backend pools and HTTP settings (basic or path-based) |
| Backend pool  | Group of targets (VMs, VMSS, IPs, FQDN) serving requests                  |
| HTTP settings | Configure backend port, protocol, affinity, and health probe              |
| Rewrite set   | Collection of rewrite rules to alter headers, paths, or queries           |
| Health probe  | Checks backend health (default or custom)                                 |

## Links and references

* Azure Application Gateway documentation: [https://learn.microsoft.com/azure/application-gateway/](https://learn.microsoft.com/azure/application-gateway/)
* Application Gateway configuration samples and how-to guides: [https://learn.microsoft.com/azure/application-gateway/configuration-overview](https://learn.microsoft.com/azure/application-gateway/configuration-overview)

This covers the core concepts of Application Gateway request routing, redirection types, rewrite policies, and a practical portal walkthrough for path-based routing.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/50c3966d-1fc5-45b0-8339-5c8be2ce49c3/lesson/d1ad4748-374b-4944-9ae8-5751399cb742)
