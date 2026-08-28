# Introduction

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Design-and-Implement-Azure-Firewall/Introduction/page

Design and implement Azure Firewall providing centralized stateful network and application protection, rule processing, deployment guidance, and hub and spoke enforcement in Azure.

Design and implement Azure Firewall.

Azure Firewall is a cloud-native, stateful firewall-as-a-service that protects Azure virtual networks by providing centralized, policy-driven network and application-level protection. It inspects and logs traffic, offers high availability by default, and integrates with Azure monitoring and policy services to deliver a scalable enforcement point for enterprise network architectures.

Below are the learning objectives for this lesson. We'll:

* Understand the core capabilities of Azure Firewall, including stateful traffic inspection, built-in high availability, and integration with Azure Monitor, Azure Policy, and diagnostic logging.
* Learn how Azure Firewall evaluates and applies NAT rules, network rules, and application rules to control, filter, and translate traffic.
* Explore deployment options and step-by-step configuration of Azure Firewall using the Azure portal ([Azure portal](https://portal.azure.com)) and automation approaches.
* See how Azure Firewall functions as a central security enforcement point in hub-and-spoke network topologies, including traffic flow patterns and route considerations.
* Clarify differences between Azure Firewall and other Azure network controls (Network Security Groups, Azure DDoS Protection, Application Gateway) to determine the appropriate use case for each.

<Frame>
  <img alt="The image outlines learning objectives related to Azure Firewall, including its capabilities, processing of NAT and network rules, setup, and use in network design. It features a colorful design with numbered points." />
</Frame>

## Learning outcomes (at a glance)

| Objective                      | What you'll learn / achieve                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| Core capabilities              | How stateful inspection, scaling, and built-in HA work; integration with Azure Monitor and logging. |
| Rule processing                | How NAT rules, network rules, and application rules are evaluated and the order of precedence.      |
| Deployment & configuration     | Portal walkthrough, recommended resource group and VNet patterns, and automation considerations.    |
| Hub-spoke enforcement          | How to centralize traffic inspection in hub-and-spoke topologies and manage user-defined routes.    |
| Comparison with other controls | When to use Azure Firewall vs. NSGs, Application Gateway, or other Azure network services.          |

<Callout icon="lightbulb">
  Tip: Use Azure Firewall as the centralized enforcement layer for outbound and east-west traffic in hub-and-spoke topologies, and pair it with NSGs for per-subnet micro-segmentation to achieve layered defense.
</Callout>

## Links and references

* Azure portal: [https://portal.azure.com](https://portal.azure.com)
* Azure Firewall overview: [https://learn.microsoft.com/azure/firewall](https://learn.microsoft.com/azure/firewall)
* Azure networking concepts: [https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/virtual-network-hub-spoke](https://learn.microsoft.com/azure/architecture/reference-architectures/hybrid-networking/virtual-network-hub-spoke)

<Callout icon="warning">
  Warning: Azure Firewall is billed based on deployment SKU and processed data; review pricing and service limits before production deployment. See the Azure Firewall pricing and limits documentation for details.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/c48f6bd6-195c-4405-9c9f-614ed7beb371/lesson/173fca1a-c4a3-4d18-8f90-0738c0471de5" />
</CardGroup>
