# Certification Details

Source: https://notes.kodekloud.com/docs/Updated-AZ-104-Microsoft-Azure-Administrator/Introduction/Certification-Details/page

Overview of AZ-104 exam objectives and key study topics for managing Azure identities, governance, storage, compute, networking, monitoring, backups, and troubleshooting

This lesson summarizes the AZ-104: Microsoft Azure Administrator exam objectives and shows the core topics to study. The AZ-104 tests skills required to manage Azure identities, governance, storage, compute, networking, and monitoring.

There are five main domains in the exam:

* Manage identities and governance
* Implement and manage storage
* Deploy and manage Azure compute resources
* Implement and maintain virtual networking
* Monitor and maintain Azure resources

Below is a quick overview followed by a deeper look at each domain and recommended topics to study.

<Frame>
  <img alt="A presentation slide titled &#x22;AZ-104 Certification: Topics.&#x22; It shows five colored boxes listing exam domains: manage identities and governance; implement and manage storage; deploy and manage Azure compute resources; implement and maintain virtual networking; and monitor and maintain Azure resources." />
</Frame>

Summary table of domains and focus areas

| Domain                                    | Exam weight | Core topics to study                                                                                                                    |
| ----------------------------------------- | ----------: | --------------------------------------------------------------------------------------------------------------------------------------- |
| Manage identities and governance          |      20–25% | Microsoft Entra ID (Azure AD), RBAC, policies, subscriptions, management groups, ARM templates, CLI/PowerShell resource management      |
| Implement and manage storage              |      15–20% | Storage account types, replication, access control, blob/files/queues/tables, lifecycle management                                      |
| Deploy and manage compute resources       |      20–25% | Azure VMs (provisioning, sizing, extensions), PaaS compute (App Service, Container Instances, Container Apps), basic container concepts |
| Implement and maintain virtual networking |      15–20% | vNets, subnets, NSGs, peering, VPN Gateway, load balancers, UDRs, routing                                                               |
| Monitor and maintain resources            |      10–15% | Azure Backup, Site Recovery, Azure Monitor, Log Analytics, diagnostic settings, alerts and metrics                                      |

Manage Azure Identities and Governance (20–25%)

This domain tests identity management, governance, and resource administration. Key study items:

* Microsoft Entra ID (formerly Azure AD): users, groups, service principals, managed identities.
* Authentication and conditional access basics.
* Role-Based Access Control (RBAC): built-in & custom roles, assignments and effective permissions.
* Governance constructs: management groups, subscriptions, resource groups, Azure Policy (definition/assignment).
* Resource deployment and automation: ARM templates, Bicep (if applicable), Azure CLI, and Azure PowerShell for provisioning and role assignments.
* Troubleshooting identity and access issues.

<Frame>
  <img alt="A slide titled &#x22;AZ-104 Certification: Topics&#x22; highlighting &#x22;Manage Azure identities and governance (20–25%)&#x22; with subitems (Administer Identity, Administer Governance and Compliance, Administer Azure Resources). To the right are colored boxes listing other domains: Implement and manage storage; Deploy and manage Azure compute resources; Implement and maintain virtual networking; Monitor and maintain Azure resources." />
</Frame>

Implement and Manage Storage (15–20%)

Focus on managing Azure Storage services:

* Storage account types and tiers (Standard/Premium, hot/cool/archive).
* Data replication options (LRS, GRS, RA-GRS, ZRS) and choosing based on availability and recovery needs.
* Access control: shared keys, SAS tokens, Azure AD integration.
* Data management: lifecycle policies, soft delete, immutable blobs, file shares.

Deploy and Manage Azure Compute Resources (20–25%)

Understand compute options and administration:

* Virtual Machines: deployment, sizes, extensions (e.g., custom script, VM Agent), managed disks, availability sets/zones, backups and updates.
* PaaS compute: App Service plans and app deployment, Azure Container Instances, Container Apps and how they differ from AKS.
* Containers and orchestration: basic container concepts and when to choose PaaS vs container services.

Note: Azure Kubernetes Service (AKS) is a deeper, specialized topic. It is useful to understand at a high level but is not a primary focus of the AZ-104 objectives. For a dedicated AKS course, see the linked resource below.

Implement and Maintain Virtual Networking (15–20%)

This domain covers network design, connectivity, and traffic management:

* Virtual networks, subnets, and network security groups (NSGs).
* Private connectivity: Virtual Network Peering and VPN Gateway for inter-site connectivity.
* Traffic management: Azure Load Balancer, Application Gateway (high level), route tables, and user-defined routes (UDRs).
* Network troubleshooting basics and service endpoints/private endpoints.

<Frame>
  <img alt="A slide titled &#x22;AZ-104 Certification: Topics&#x22; highlighting the central topic &#x22;Implement and manage virtual networking (15–20%)&#x22; with subitems for administering virtual networking, intersite connectivity, and network traffic. Four colored boxes on the right list other domains: manage Azure identities and governance, implement and manage storage, deploy/manage Azure compute resources, and monitor/maintain Azure resources." />
</Frame>

Monitor and Maintain Azure Resources (10–15%)

This domain focuses on monitoring, backup, and recovery:

* Azure Backup: backup policies, recovery points, and restore operations.
* Azure Site Recovery (ASR) basics for disaster recovery scenarios.
* Azure Monitor: collecting metrics, logs, and configuring diagnostic settings.
* Log Analytics and Kusto Query Language (KQL) basics for querying logs.
* Setting up alerts (metric and log alerts) and automated actions.

<Frame>
  <img alt="A presentation slide titled &#x22;AZ-104 Certification: Topics&#x22; highlighting &#x22;Monitor and maintain Azure resources (10–15%)&#x22; with subitems &#x22;Administer Data Protection&#x22; and &#x22;Administer Monitoring.&#x22; To the right are four colored boxes listing other domains: Manage Azure identities and governance; Implement and manage storage; Deploy and manage Azure compute resources; and Implement and maintain virtual networking." />
</Frame>

Service name changes and official resources

* Microsoft Entra ID is the new name for Azure AD. This is a rebranding; functionality remains consistent, though some product pages and learning content may reference the new name.
* Always verify current exam objectives and platform terminology on official Microsoft pages.

<Callout icon="lightbulb">
  For up-to-date exam objectives and guided learning paths, rely on official sources such as Microsoft Learn and the Azure documentation. Combine hands-on practice (deploying VMs, setting up RBAC, configuring networks, and using Azure Monitor) with study modules to reinforce practical skills.
</Callout>

Links and references

* [Microsoft Learn](https://learn.microsoft.com/learn/) — official learning paths and modules for AZ-104.
* [Azure documentation](https://learn.microsoft.com/azure/) — product docs, how-tos, and architecture guidance.
* [Azure Kubernetes Service (AKS) course example](https://learn.kodekloud.com/user/courses/azure-kubernetes-service) — additional AKS-focused content if you want to dive deeper into container orchestration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/edb6b82d-2942-45b9-89e9-33fbe75528c2/lesson/71f11178-1751-4192-9bd1-e82c83f18146" />
</CardGroup>
