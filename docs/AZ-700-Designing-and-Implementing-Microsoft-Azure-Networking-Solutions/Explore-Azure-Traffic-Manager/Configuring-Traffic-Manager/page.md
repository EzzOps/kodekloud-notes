# Configuring Traffic Manager

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-Traffic-Manager/Configuring-Traffic-Manager/page

Guide to configuring Azure Traffic Manager including endpoint types, nested profiles, health probes, routing methods, DNS behavior, custom domains, and diagnostic validation

This guide explains how to configure Azure Traffic Manager, step by step. You’ll learn about endpoint types, nested profiles, probe configuration, DNS behavior, and how to validate routing using diagnostics tools. Keywords: Azure Traffic Manager, routing methods, endpoints, health probes, custom domain, DNS-based load balancing.

Traffic Manager uses a parent Traffic Manager profile that references multiple endpoints. Endpoints can be:

* Azure endpoints — services running in your Azure subscription (App Services, Cloud Services, Public IPs).
* External endpoints — services outside Azure (on-premises or other clouds), referenced by IP (IPv4/IPv6) or FQDN.
* Nested endpoints — references to other Traffic Manager profiles (useful for hierarchical routing and large-scale deployments).

<Callout icon="lightbulb">
  Azure Traffic Manager is DNS-based: it returns one or more IPs/FQDNs to the client according to the selected routing method (performance, priority, weighted, geographic, multivalue, subnet).
</Callout>

<Frame>
  <img alt="The image is a diagram illustrating external endpoints in a traffic manager setup, showing a parent profile with regional nodes and endpoint distribution including failed and trial endpoints." />
</Frame>

## Nested profiles

Nested profiles let the parent profile reference other Traffic Manager profiles. The parent profile has its routing method (for example, latency), and each nested profile can use a different routing method (for example, priority). Use nested profiles to aggregate regions or implement conditional failover across multiple child profiles.

<Frame>
  <img alt="The image is a diagram illustrating nested endpoints in a traffic manager setup, showing the relationship between parent and child profiles across different regions like West US, West Europe, and East Asia. It explains traffic routing, including conditions for failed endpoints and advanced routing configurations for complex deployments." />
</Frame>

Important note on nested profiles:

* The `min child endpoints` option enforces how many healthy child endpoints must exist before the nested profile accepts traffic. For example, if `min child endpoints = 2`, the nested profile will only be considered healthy when at least two child endpoints are healthy. If the primary endpoint fails and the nested profile does not meet its minimum healthy child requirement, Traffic Manager will not route traffic to that nested profile.

## Portal workflow — create and configure a Traffic Manager profile

Follow these steps in the Azure portal to create a Traffic Manager profile and prepare endpoints.

1. Create a Traffic Manager profile
   * Choose a globally unique name — this forms the FQDN: `your-profile-name.trafficmanager.net`.
   * Select a routing method:
     * Performance, Weighted, Priority, Geographic, Multivalue, Subnet
     * Notes:
       * Performance/Weighted/Priority/Geographic typically return a single endpoint per DNS response.
       * Multivalue can return multiple healthy endpoints in one response.
       * Subnet maps client source subnets to specific endpoints.
   * Choose the subscription and resource group. (Traffic Manager is a global resource; the region you pick is only for metadata/storage.)
   * Click Create to deploy the profile.

2. Configure probes and endpoint health checks
   * Under the profile's Configuration tab, set:
     * Protocol: `HTTP`, `HTTPS`, or `TCP`
     * Port: probe port (e.g., `80` or `443`)
     * Path: probe path (e.g., `/health` or `/`)
     * Optional headers and expected status codes
     * Probe interval, tolerated failures, probe timeout
   * These probe settings tell Traffic Manager how to determine endpoint health.

Example of common probe settings:

| Setting               | Purpose                                         | Example       |
| --------------------- | ----------------------------------------------- | ------------- |
| Protocol              | Transport for probe checks                      | `HTTP`        |
| Port                  | Destination port for probe                      | `80`          |
| Path                  | URL path used by HTTP(S) probes                 | `/health`     |
| Expected status codes | Defines which HTTP codes are considered healthy | `200`         |
| Interval / Timeout    | Frequency and response timeout for checks       | `30s` / `10s` |

<Frame>
  <img alt="The image displays a configuration screen for a Traffic Manager profile, highlighting the &#x22;Configuration&#x22; tab with options like routing method, DNS time to live, and protocol settings. It instructs users to navigate to this tab to manage the Traffic Manager endpoints." />
</Frame>

3. Add endpoints
   * Azure endpoint: choose target resource type (App Service, Cloud Service, Public IP) and select the resource.
   * External endpoint: enter the FQDN or IP address of the non-Azure service.
   * Nested endpoint: reference another Traffic Manager profile.
   * Example portal flow: Add → Azure endpoint → Name (e.g., `EUS`) → Target App Service in East US → enable health checks. Do not select “Always serve traffic” unless you intentionally want to bypass health probes.

<Frame>
  <img alt="The image shows a Microsoft Azure dashboard with details of an app service named &#x22;app-az700-tm-eastus.&#x22; It provides information like the resource group, status, location, and subscription details." />
</Frame>

After adding additional App Service endpoints (for example, Southeast Asia and West Europe), Traffic Manager will probe each endpoint and show status in the portal.

<Frame>
  <img alt="The image shows a Microsoft Azure portal interface displaying three endpoints under a Traffic Manager profile, with their status and locations listed." />
</Frame>

## Host header behavior and App Service integration

When clients access the Traffic Manager FQDN, understand the Host header implications:

* Browsers set the Host header to the domain requested. For example, when requesting `your-profile.trafficmanager.net`, the Host header will be `your-profile.trafficmanager.net`.
* App Service requires the Host header to match one of its configured hostnames (e.g., `*.azurewebsites.net` or a custom domain you mapped). If it does not match, the App Service will return a 404.

<Frame>
  <img alt="The image shows a &#x22;404 Web Site not found&#x22; error message on a blue background, with technical details in the browser's developer tools highlighting a failed GET request." />
</Frame>

Production best practice:

* Use a custom domain (for example, `www.kodekloud.com`) and map it to Traffic Manager.
  * In DNS: create a CNAME record from `www.kodekloud.com` to `your-profile.trafficmanager.net`.
  * In each App Service: add the custom domain so the App Service accepts requests with `Host: www.kodekloud.com`. This avoids 404s due to host header mismatch.

<Callout icon="warning">
  Accessing the Traffic Manager endpoint directly (without a custom domain mapped to App Service) will result in a mismatched Host header and likely a 404. For realistic testing, map a custom domain or explicitly set the Host header in your test requests.
</Callout>

## Diagnostics — DNS resolution and request testing

To validate Traffic Manager behavior and which endpoint is returned, use `nslookup` and `curl`.

* Observe the CNAME chain returned by DNS for the Traffic Manager profile:

```bash theme={null}
