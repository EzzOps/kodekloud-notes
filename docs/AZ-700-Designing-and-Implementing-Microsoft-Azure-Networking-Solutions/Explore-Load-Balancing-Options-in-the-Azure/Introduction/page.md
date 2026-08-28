# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Explore-Load-Balancing-Options-in-the-Azure/Introduction/page

Overview of Azure load balancing options and guidance to choose between regional and global solutions for high availability, performance, and traffic distribution across Azure services.

Welcome to this module on Azure load balancing.

In this lesson we'll explore Azure's load balancing portfolio and how each option helps you achieve high availability, fault tolerance, and optimal application performance. You will learn how Azure distributes network traffic across multiple resources—ensuring reliability and consistent performance as demand changes.

By the end of this module, you will meet three clear learning objectives:

* Grasp the core load balancing concepts: how a load balancer acts as a traffic cop by distributing incoming requests to backend resources to maintain reliability and performance.
* Differentiate Azure's main load balancing solutions: Azure Load Balancer (Layer 4), Application Gateway (Layer 7), Traffic Manager (DNS-based global routing), and Azure Front Door (global HTTP load balancing and acceleration).
* Choose the right service for your application based on traffic type, availability goals, latency requirements, and architecture constraints.

<Frame>
  <img alt="The image outlines learning objectives related to Azure's load balancing solutions, including understanding load balancer functions, different Azure solutions, and choosing appropriate services based on specific needs." />
</Frame>

Use this module to build practical guidance for designing resilient, performant network architectures on Azure. We’ll start with the foundational concepts behind load balancing and then examine Azure Load Balancer before progressing to higher-layer and global routing solutions.

<Callout icon="lightbulb">
  Tip: When evaluating which Azure load balancing service to use, first identify your traffic type (TCP/UDP vs. HTTP/HTTPS), whether you need global vs. regional routing, and whether you require application-layer features like WAF or URL-based routing.
</Callout>

Quick comparison — at a glance:

| Service             | OSI Layer             | Primary Use Case                                             | Key features                                                        |
| ------------------- | --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------- |
| Azure Load Balancer | Layer 4 (Transport)   | High-throughput, low-latency TCP/UDP traffic within a region | Public/private IP, health probes, cross-zone HA                     |
| Application Gateway | Layer 7 (Application) | HTTP(S) routing with advanced features                       | URL-based routing, session affinity, Web Application Firewall (WAF) |
| Traffic Manager     | DNS-based (Global)    | Geo-distribution and failover across regions                 | DNS routing methods: priority, performance, weighted                |
| Azure Front Door    | Layer 7 (Global HTTP) | Global HTTP(S) load balancing and acceleration               | Anycast, SSL termination, CDN-like caching, WAF integration         |

Links and references

* Azure Load Balancer: [https://learn.microsoft.com/azure/load-balancer/](https://learn.microsoft.com/azure/load-balancer/)
* Azure Application Gateway: [https://learn.microsoft.com/azure/application-gateway/](https://learn.microsoft.com/azure/application-gateway/)
* Azure Traffic Manager: [https://learn.microsoft.com/azure/traffic-manager/](https://learn.microsoft.com/azure/traffic-manager/)
* Azure Front Door: [https://learn.microsoft.com/azure/frontdoor/](https://learn.microsoft.com/azure/frontdoor/)

Let's proceed by examining each learning objective in detail, starting with core load balancing concepts and the Azure Load Balancer.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/a231ef6d-9e0c-4c9d-81dd-d3ea9de8d42f/lesson/8b4580a6-a941-4dd8-acf0-2e1f6187c203" />
</CardGroup>
