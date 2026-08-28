# DNS resolution shows the Traffic Manager CNAME to the selected App Service FQDN
nslookup az700-atm-kodekloud.trafficmanager.net
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
az700-atm-kodekloud.trafficmanager.net    canonical name = app-az700-tm-southeastasia.azurewebsites.net.
app-az700-tm-southeastasia.azurewebsites.net    canonical name = waws-prod-sg1-031.sip.azurewebsites.windows.net.
waws-prod-sg1-031.sip.azurewebsites.windows.net  canonical name = waws-prod-sg1-031.southeastasia.cloudapp.azure.com.
Name:    waws-prod-sg1-031.southeastasia.cloudapp.azure.com
Address: 20.188.98.74
```

* If you change your network location (for example, via VPN), Traffic Manager may resolve to a different App Service according to the routing method:

```bash theme={null}
nslookup az700-atm-kodekloud.trafficmanager.net
Server:         162.252.172.57
Address:        162.252.172.57#53

Non-authoritative answer:
az700-atm-kodekloud.trafficmanager.net    canonical name = app-az700-tm-eastus.azurewebsites.net.
app-az700-tm-eastus.azurewebsites.net     canonical name = waws-prod-blu-047.sip.azurewebsites.windows.net.
waws-prod-blu-047.sip.azurewebsites.windows.net canonical name = waws-prod-blu-047.eastus.cloudapp.azure.com.
Name:    waws-prod-blu-047.eastus.cloudapp.azure.com
Address: 40.117.154.240
```

* Test an App Service response by setting the Host header to an App Service hostname returned by DNS:

```bash theme={null}
curl "http://az700-atm-kodekloud.trafficmanager.net" -H "Host: app-az700-tm-eastus.azurewebsites.net"
```

If successful, the App Service HTML page will be returned. Example trimmed response body:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
  <title>Traffic Manager Demo - Southeast Asia</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; padding-top: 20vh; }
    .region { font-size: 1.5em; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; display: inline-block; margin-top: 20px; }
    .info { margin-top: 30px; font-size: 1.1em; opacity: 0.9; }
  </style>
</head>
<body>
  <h1>Happy Learning from Southeast Asia</h1>
  <div class="region">Region: Southeast Asia</div>
  <div class="info">
    <p>App Service: app-az700-tm-southeastasia</p>
    <p>Location: southeastasia</p>
  </div>
</body>
</html>
```

Tip: On Windows, clear the local DNS cache before testing:

```bat theme={null}
ipconfig /flushdns
```

## Quick reference

| Topic           | Key points                                                                                    |
| --------------- | --------------------------------------------------------------------------------------------- |
| Endpoint types  | Azure, External, Nested                                                                       |
| Routing methods | Performance, Priority, Weighted, Geographic, Multivalue, Subnet                               |
| Health probes   | Configure protocol, port, path, expected codes, interval/timeout                              |
| Host header     | Use a custom domain or set the Host header for tests to avoid 404s                            |
| Diagnostics     | Use `nslookup` to inspect CNAME chains and `curl` with `-H "Host: ..."` to validate responses |

<Frame>
  <img alt="The image shows the Azure Traffic Manager interface, with navigation options and a section for adding endpoints. It describes the service as a DNS-based traffic load balancer for distributing traffic with high availability." />
</Frame>

Summary

* Azure Traffic Manager is a DNS-based routing service for distributing client requests across multiple endpoints.
* Choose the right routing method and endpoint types for your architecture (Azure, external, nested).
* Configure health probes carefully to match your application’s health endpoints.
* Use a custom domain (CNAME to `your-profile.trafficmanager.net`) and add that custom domain to your App Services for production.
* For testing, use `nslookup`, `curl` with a custom Host header, and flush local DNS caches as needed.

I hope this clarifies Traffic Manager configuration. Next, we’ll continue with the following topic.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/38ad64e6-12ba-4187-955b-c2e4522be498/lesson/586559a8-2585-4722-8248-5bc7b85ba028" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Azure-Traffic-Manager/Introduction/page

Overview of Azure Traffic Manager, a DNS-based traffic load balancer for global routing, failover, performance, and endpoint health management

In this lesson you'll learn how Azure Traffic Manager works, when to use it, and which features help deliver globally available and performant applications. Traffic Manager is a DNS-based traffic load balancer that directs client requests to the best available endpoint using DNS resolution and built-in health checks. It’s ideal for multi-region deployments and globally distributed users where DNS-level control, failover, and latency-based routing are required.

What you'll learn:

* Common scenarios where Traffic Manager improves availability and performance (global failover, performance optimization, compliance-based routing).
* How DNS resolution and health probes determine where traffic goes.
* The routing methods Traffic Manager supports and when to use each.
* Types of endpoints Traffic Manager manages.
* Key configuration steps and operational controls, including probe tuning and DNS considerations.
* When to choose Traffic Manager vs. application-layer load balancers (e.g., Azure Front Door or Application Gateway).

<Callout icon="lightbulb">
  Traffic Manager operates at the DNS layer, not the HTTP/HTTPS request layer. For application-layer features such as SSL termination, path-based routing, or a Web Application Firewall (WAF), consider Azure Front Door or Application Gateway instead.
</Callout>

***

## How Traffic Manager Works (high level)

Traffic Manager uses DNS queries to return the DNS name of the endpoint that should serve the request. It evaluates endpoints’ health and the selected routing method when answering DNS queries:

* Client resolves your application’s Traffic Manager profile DNS name (e.g., `myapp.trafficmanager.net`).
* Traffic Manager evaluates endpoint health via configured probes (HTTP/HTTPS/TCP).
* Based on routing method and probe results, Traffic Manager returns the DNS record that points the client to an endpoint (or a nested profile).
* Because Traffic Manager operates at the DNS layer, the client then connects directly to the endpoint returned by DNS.

Key consequences:

* Failover and routing decisions are fast in DNS responses but subject to client DNS caching and TTL.
* Traffic Manager does not terminate or proxy traffic; it only guides clients to endpoints.

***

## When to Use Traffic Manager

Common use cases:

* Global failover / disaster recovery (priority routing).
* Performance optimization for globally distributed users (latency/performance routing).
* Gradual rollouts and traffic distribution (weighted routing).
* Data sovereignty or localization (geographic routing).
* Combining multiple Traffic Manager profiles for hierarchical routing (nested profiles).

Use Traffic Manager when you need DNS-level control across regions. Use application-layer services (Front Door, Application Gateway) when you require features like SSL offload, path-based routing, or WAF.

***

## Routing Methods

| Routing method        |                                              Primary purpose | When to choose                                              |
| --------------------- | -----------------------------------------------------------: | ----------------------------------------------------------- |
| Priority              | Global failover with a primary endpoint and backup endpoints | Disaster recovery, active/passive deployments               |
| Weighted              |                Distribute traffic by weight across endpoints | Gradual rollouts, A/B testing, traffic shaping              |
| Performance (latency) |                   Route users to the lowest-latency endpoint | Optimize user experience across regions                     |
| Geographic            |                        Route users based on client geography | Data residency, content localization, regulatory compliance |
| Multivalue            |           Return multiple healthy endpoints in DNS responses | Clients can choose among multiple endpoints (limited use)   |
| Subnet                |                   Map client IP ranges to specific endpoints | Route specific client subnets to dedicated endpoints        |

Examples (CLI):

* Create a profile (Priority):

```bash theme={null}
az network traffic-manager profile create \
  --name my-tm-profile \
  --resource-group my-rg \
  --routing-method Priority \
  --unique-dns-name myapp
```

* Add an endpoint:

```bash theme={null}
az network traffic-manager endpoint create \
  --name my-endpoint \
  --profile-name my-tm-profile \
  --resource-group my-rg \
  --type azureEndpoints \
  --target-resource-id "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/my-rg/providers/Microsoft.Web/sites/myapp" \
  --priority 1
```

Note: Wrap placeholders such as `<SUBSCRIPTION_ID>` in backticks when copying these commands.

***

## Endpoint Types

| Endpoint type      |                                                                  Description | Typical use                                                    |
| ------------------ | ---------------------------------------------------------------------------: | -------------------------------------------------------------- |
| Azure endpoints    | Azure-hosted services (App Service, VM, Cloud Service, public Load Balancer) | Best for Azure-native services reachable via public DNS/IP     |
| External endpoints |                     Endpoints outside Azure (on-prem, other cloud providers) | Hybrid or multi-cloud deployments                              |
| Nested profiles    |                                  Traffic Manager profile used as an endpoint | Hierarchical traffic management and advanced failover patterns |

<Callout icon="warning">
  Traffic Manager requires endpoints to be publicly addressable by DNS or IP. Internal-only/private load balancers are not directly supported as endpoints.
</Callout>

***

## Health Checks and Probe Configuration

Traffic Manager uses configurable probes to determine endpoint health. Configure probes to match your application’s behavior to avoid false positives/negatives.

Probe configuration options:

* Protocol: `HTTP`, `HTTPS`, or `TCP`.
* Path: For `HTTP/HTTPS`, the probe path (e.g., `/health`).
* Interval: Time between probes (seconds).
* Timeout: How long to wait for probe response (seconds).
* Tolerated failures: Number of consecutive failures before marking an endpoint unhealthy.

Recommended probe tuning:

* Point probes at a lightweight, stable health endpoint (e.g., `/healthz`).
* For global failover, prefer shorter intervals and conservative tolerated failures to fail over quickly but avoid transient flaps.
* For performance-based routing, ensure probes truly reflect end-user experience (latency vs application readiness).

Example (CLI) to set a probe:

```bash theme={null}
az network traffic-manager profile update \
  --name my-tm-profile \
  --resource-group my-rg \
  --status Enabled \
  --interval 30 \
  --timeout 10 \
  --max-failures 3 \
  --protocol HTTP \
  --path /healthz
```

***

## DNS Considerations

Because Traffic Manager is DNS-based, DNS behavior affects routing and failover:

* TTL (time-to-live) controls how long clients cache DNS answers. Shorter TTLs make failover faster but increase DNS query volume.
* DNS caching by resolvers and clients can delay failover beyond Traffic Manager decisions.
* Use an appropriate TTL for your SLA and expected failover speed; common values are 30–300 seconds depending on trade-offs.

Best practices:

* Balance TTL and TTL-driven costs: very low TTLs increase DNS traffic.
* Consider nested profiles to create complex routing with clearer DNS names and TTL strategies.
* Monitor DNS resolution times from representative regions to validate behavior.

***

## Configuration Checklist (Portal and CLI)

1. Create a Traffic Manager profile.
   * Choose a unique DNS name (e.g., `myapp.trafficmanager.net`).
   * Select a routing method.
2. Add endpoints (Azure, External, or Nested).
3. Configure probes to validate endpoint health.
4. Set TTL and DNS retry strategies that meet your failover SLAs.
5. Test failover scenarios by simulating endpoint failures and verifying DNS resolution behavior.
6. Monitor — use Azure Monitor and Traffic Manager metrics to track endpoint health and DNS query patterns.

Azure Portal steps (summary):

* Navigate to Traffic Manager profiles > + Create.
* Provide subscription, resource group, profile name, and routing method.
* After creation, select Endpoints > + Add to register endpoints.
* Configure Monitoring settings (protocol, path, interval, timeout).

***

## Limitations and When to Choose Other Services

* Traffic Manager only operates at DNS level (no TLS termination, no application-layer routing).
* Client DNS caching can delay failover; application-layer services provide faster, proxy-based failover.
* For SSL offload, path-based routing, WAF, or edge caching, use Azure Front Door or Application Gateway.

Use Traffic Manager when:

* You need simple, scalable DNS-based routing across regions.
* Your endpoints can be publicly resolved and handled by clients directly.

Use Front Door/Application Gateway when:

* You need advanced HTTP features (SSL termination, path-based routing, WAF).
* You require edge caching, rewrite, or full proxy behavior.

***

## Examples and Scenarios

* Global active/passive: Use Priority routing with primary endpoint priority=1 and backups priority=2,3...
* Blue/green or canary releases: Use Weighted routing and adjust weights to shift traffic gradually.
* Low-latency region selection: Use Performance routing to direct users to the lowest-latency endpoint.
* Regulatory compliance by region: Use Geographic routing to bind users to local endpoints.

***

## Links and References

* [Azure Traffic Manager documentation](https://learn.microsoft.com/azure/traffic-manager/)
* [Azure CLI Traffic Manager commands](https://learn.microsoft.com/cli/azure/network/traffic-manager)
* [Azure Front Door vs. Traffic Manager](https://learn.microsoft.com/azure/frontdoor/front-door-traffic-manager-comparison)

***

If you'd like, I can add step-by-step portal screenshots, a sample ARM template for a Traffic Manager profile, or a reference checklist for probe tuning tailored to your application. Which would you prefer?

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/38ad64e6-12ba-4187-955b-c2e4522be498/lesson/30fd15a3-2a12-4c63-b6d3-f299c95a7173" />
</CardGroup>
