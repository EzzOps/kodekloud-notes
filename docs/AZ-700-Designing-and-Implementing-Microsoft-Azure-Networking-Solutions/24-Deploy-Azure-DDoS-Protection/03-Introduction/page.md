# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-Azure-DDoS-Protection/Introduction/page

Guide to Azure DDoS Protection explaining attack types, Basic versus Standard tiers, key features, and steps to enable and monitor Standard protection for virtual networks and public resources.

Welcome to the lesson on deploying [Azure DDoS Protection](https://learn.microsoft.com/azure/ddos-protection/).

This lesson explains why DDoS protection is critical in cloud environments, how Azure detects and mitigates DDoS attacks, and the practical steps to keep your services resilient. You’ll get a concise overview of attack types, Azure’s protection tiers, and the actions required to enable the Standard protection tier across your resources.

What you'll learn in this lesson:

* What a DDoS attack is, why it is dangerous, and how it can disrupt cloud applications.
* The common categories of DDoS attacks—volumetric, protocol, and resource (or application)-level attacks—so you can recognize different threat patterns.
* The differences between Azure DDoS Protection tiers (Basic and Standard) and how to choose the right tier for your environment.
* Key features of Azure DDoS Protection such as adaptive tuning, real-time telemetry, mitigation reporting, and integration with other Azure services.
* The high-level steps required to create and associate a DDoS Protection plan with your Azure virtual networks and public-facing resources.

> **lightbulb** Azure provides Basic DDoS protection at no additional cost for all public IPs. The Standard tier is a paid offering that includes advanced mitigation, telemetry, and per-resource protection that you can enable by creating a DDoS Protection plan.

## Why DDoS protection matters in the cloud

Distributed Denial of Service (DDoS) attacks aim to make services unavailable by overwhelming networks, protocols, or application resources. In cloud environments, DDoS attacks can cause:

* Service outages or degraded performance for customers.
* Increased resource consumption and unexpected costs from autoscaling.
* Cascading failures in dependent services and loss of availability SLAs.

Azure DDoS Protection helps you reduce these risks by automatically detecting and mitigating attacks at the network edge, delivering mitigation actions and telemetry so you can respond and adapt quickly.

## Attack categories at a glance

| Attack Category        | What it targets                        | Common examples                                | Impact                                                         |
| ---------------------- | -------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| Volumetric             | Network bandwidth                      | UDP floods, amplification attacks (NTP, DNS)   | Saturates link capacity, prevents legitimate traffic           |
| Protocol               | Network/transport layer resources      | SYN floods, fragmented packet attacks          | Exhausts network devices, firewalls, load balancers            |
| Resource / Application | Application logic or server CPU/memory | Slow HTTP (R.U.D.Y), high-CPU request patterns | Slows or crashes application servers, degrades user experience |

Understanding these categories helps you prioritize protections and detect patterns faster.

## Azure DDoS Protection: Basic vs Standard

| Tier     | Coverage                         | Key features                                                                                                                                   |
| -------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic    | Included for all public IPs      | Automatic network-layer protection for common volumetric attacks                                                                               |
| Standard | Paid offering (per subscription) | Adaptive tuning per virtual network, attack telemetry, mitigation reports, integration with `Azure Monitor` and `Microsoft Defender for Cloud` |

Standard is designed for production workloads that require tailored protection and visibility into attack telemetry. Use Standard when you need actionable diagnostics, custom mitigation tuning, and integration with Azure security and monitoring tools.

## Key features of Azure DDoS Protection Standard

* Adaptive tuning: Reduces false positives by learning normal traffic patterns for your protected resources.
* Real-time telemetry: Attack metrics and mitigation events surfaced to Azure Monitor and diagnostic logs.
* Mitigation reporting: Post-attack analysis and reports to help refine defensive posture.
* Integration: Works with Network Watcher, Azure Monitor, and Microsoft Defender for Cloud to centralize alerts and response.

## High-level steps to enable Azure DDoS Protection Standard

1. Create a DDoS Protection plan in your subscription.
   * See: [https://learn.microsoft.com/azure/ddos-protection/ddos-protection-plan-overview](https://learn.microsoft.com/azure/ddos-protection/ddos-protection-plan-overview)
2. Associate one or more virtual networks to the protection plan.
   * See: [https://learn.microsoft.com/azure/virtual-network/](https://learn.microsoft.com/azure/virtual-network/)
3. Ensure the resources you want protected use public IPs within those virtual networks (public-facing endpoints are the primary DDoS vectors).
   * See: [https://learn.microsoft.com/azure/virtual-network/public-ip-addresses](https://learn.microsoft.com/azure/virtual-network/public-ip-addresses)
4. Configure alerting and telemetry via Azure Monitor and Network Watcher to capture mitigation events, metrics, and flow logs.
   * See: [https://learn.microsoft.com/azure/azure-monitor/](https://learn.microsoft.com/azure/azure-monitor/) and [https://learn.microsoft.com/azure/network-watcher/](https://learn.microsoft.com/azure/network-watcher/)
5. After any incident, review attack analytics and mitigation reports to refine rules, autoscaling policies, and runbooks.

## Planning and operational considerations

* Coverage scope: DDoS Protection Standard protects resources in associated virtual networks. Public IPs outside those networks are not covered.
* Cost vs risk: Evaluate expected traffic patterns and business impact to decide whether Standard’s telemetry and mitigation justify the cost.
* Monitoring and automation: Integrate mitigation alerts with incident response playbooks (Azure Alerts, Logic Apps, or SIEM tools) to automate containment and remediation.
* Testing and drills: Periodically run resilience tests (in controlled conditions) to validate monitoring, scaling, and mitigation workflows.

## Links and references

* [Azure DDoS Protection overview](https://learn.microsoft.com/azure/ddos-protection/)
* [DDoS Protection plan overview](https://learn.microsoft.com/azure/ddos-protection/ddos-protection-plan-overview)
* [Azure Virtual Network documentation](https://learn.microsoft.com/azure/virtual-network/)
* [Public IP addresses in Azure](https://learn.microsoft.com/azure/virtual-network/public-ip-addresses)
* [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/)
* [Network Watcher](https://learn.microsoft.com/azure/network-watcher/)
* [Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/)

This lesson will expand on each of these topics and walk through configuration examples, monitoring guidance, and incident response best practices for deploying DDoS protection in Azure.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/2dfc3e6d-61ae-4c3c-a71d-559cd1e302af/lesson/aa6e8602-e98b-421d-9f74-9f4739da087d)
