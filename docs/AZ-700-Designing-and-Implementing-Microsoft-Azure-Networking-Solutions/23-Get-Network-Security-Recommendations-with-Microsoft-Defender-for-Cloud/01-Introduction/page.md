# From the same VM after enabling the storage account to allow only the selected VNet/subnet
kodekloude@vm-service-endpoints:~$ curl https://sanavidm.blob.core.windows.net/data/gl2.jpeg
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output `FILE`"
Warning: to save to a file.
kodekloude@vm-service-endpoints:~$
```

This confirms the Storage account sees the request as coming from your VNet/subnet and that traffic stays on Microsoft’s internal network.

## Implementation notes and caveats

* Enabling a service endpoint injects system routes and configures Azure’s internal routing so traffic to the supported service is routed over the Microsoft backbone instead of the public internet.
* DNS resolution for the service FQDN still returns a Microsoft public IP. The VM uses its private IP to connect, but the destination IP is a Microsoft-owned public IP; on-premises clients will still see a public endpoint unless you supplement with NAT/DNS or more advanced routing.
* Service endpoints authorize a VNet/subnet identity to the service — you do not authorize individual VM private IPs.
* For strict private connectivity (FQDN resolves to a private IP within your VNet) and full private-to-private resolution, use Azure Private Endpoint (Private Link). Private Endpoints assign private IPs in your VNet and integrate with private DNS.

## Quick comparison

| Feature                                        | Service Endpoint | Private Endpoint (Private Link)  |
| ---------------------------------------------- | ---------------- | -------------------------------- |
| Traffic stays on Microsoft backbone            | Yes              | Yes                              |
| Service FQDN resolves to public IP             | Yes              | No — resolves to private IP      |
| Requires subnet/VNet authorization             | Yes              | Yes — plus private IP assignment |
| Best for strict private access and private DNS | No               | Yes                              |

Service endpoints are a simple and effective way to secure PaaS access from VNets. For scenarios that require full private addressing and private DNS resolution, prefer Private Endpoint.

## Links and references

* [Azure Virtual Network service endpoints overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)
* [Azure Storage network security (service endpoints)](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security?tabs=azure-portal#service-endpoints)
* [Azure Private Link / Private Endpoint overview](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/eaba2742-d4a4-4233-8056-b3eaec8692a5/lesson/5a426397-3c8b-4ae7-98a8-53b0dc0f0aef)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Get-Network-Security-Recommendations-with-Microsoft-Defender-for-Cloud/Introduction/page

How Microsoft Defender for Cloud evaluates and improves Azure virtual network security with recommendations, benchmarks, monitoring, incident investigation, and remediation guidance.

Get network security recommendations with Microsoft Defender for Cloud.

This lesson explains how Defender for Cloud evaluates and protects your Azure virtual networks and connected cloud resources. You will learn the recommended security controls, the baselines and benchmarks Defender for Cloud applies, and how to monitor, investigate, and respond to network-related security findings.

Topics covered:

* Microsoft's recommended best practices for network security.
* Security baselines and benchmarks applied by Defender for Cloud to evaluate your environment.
* How Defender for Cloud helps identify compliance gaps and map findings to regulatory standards.
* Methods to monitor, investigate, and respond to security alerts and recommendations that Defender for Cloud generates.

By the end of this lesson you will understand how Defender for Cloud assesses network security posture, surfaces actionable recommendations, and supports continuous monitoring and incident response.

> **lightbulb** Tip: To follow along, ensure you have Reader access to a subscription or resource group with Defender for Cloud enabled. For recommendation remediation, contributor-level permissions are typically required.

## What you will learn (at a glance)

| Topic                                  | What you'll learn                                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Recommended network security practices | How to design and harden Azure virtual networks, NSGs, and network appliances per Microsoft guidance                |
| Security baselines & benchmarks        | Which baselines (for example, CIS, Azure Security Benchmark) Defender for Cloud uses and how it evaluates resources |
| Compliance mapping                     | How Defender for Cloud maps findings to regulatory standards and identifies compliance gaps                         |
| Alerts, monitoring & response          | How to monitor network alerts, investigate incidents, and use built-in or custom playbooks for response             |

## Why this matters

Defender for Cloud continuously assesses your network configuration and traffic controls to surface misconfigurations, unprotected exposures, or deviations from recommended baselines. Addressing these recommendations reduces attack surface, improves compliance, and helps prevent lateral movement and data exposure.

> **warning** Important: Some network security recommendations require configuration changes that may impact traffic flow. Always validate changes in a staging environment and test connectivity after applying rule or route updates.

## High-level workflow

1. Defender for Cloud collects configuration and telemetry from your subscription and resources.
2. It evaluates resources against built-in security controls and chosen benchmarks.
3. Recommendations and alerts are generated, prioritized by severity and exposure.
4. You investigate findings using the portal, logs, and integrated threat intelligence.
5. Apply remediations manually or with automated playbooks and track progress.

## Resources and next steps

* Microsoft Defender for Cloud overview: [https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction)
* Azure Networking concepts: [https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)
* Azure Security Benchmark: [https://learn.microsoft.com/azure/security/benchmark/](https://learn.microsoft.com/azure/security/benchmark/)
* CIS Benchmarks for Azure: [https://www.cisecurity.org/benchmark/azure/](https://www.cisecurity.org/benchmark/azure/)

By the end of this lesson you will be prepared to use Defender for Cloud to assess network security posture, act on prioritized recommendations, and implement continuous monitoring and incident response processes.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/f4902d6f-4431-423f-91f8-1fa582bb6d5b/lesson/f87a4342-af5a-4f58-a396-88307da36b2e)
