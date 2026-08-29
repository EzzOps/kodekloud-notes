# Azure DDoS protection

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Deploy-Azure-DDoS-Protection/Azure-DDoS-protection/page

Azure DDoS Protection defends Azure applications and networks from volumetric, protocol, and application attacks with automatic mitigation, telemetry, and network or per IP protection plans.

Azure DDoS Protection defends your Azure-hosted applications and network resources from volumetric, protocol, and application-layer DDoS attacks. It continuously monitors traffic, automatically applies mitigations, and integrates with Azure diagnostics and security operations so your services remain available during attack events.

Key benefits:

* Always-on monitoring and automatic mitigation using Azure’s global network capacity.
* Adaptive tuning to reduce false positives by matching detection thresholds to normal application traffic.
* Built-in analytics, telemetry, and alerting to surface attack indicators and support incident response.
* Optional access to Microsoft's Rapid Response team during large or complex events.
* Integration with Azure Firewall, Application Gateway, Network Security Groups (NSGs), and Defender for Cloud for layered protection.

<Frame>
  <img alt="The image is a flowchart illustrating Azure DDoS protection, showing the process from the customer to public IPs via a virtual network and policy generation. It highlights features like always-on monitoring, rapid response, and adaptive tuning." />
</Frame>

Most importantly, Azure DDoS Protection scales with attack volume and leverages Microsoft’s global bandwidth to absorb large traffic floods, minimizing impact to application availability.

## Protection plans and tiers

Azure offers two main DDoS Protection approaches to fit different scopes and billing models:

* DDoS Network Protection (plan-level): create a DDoS Protection plan and associate it with one or more virtual networks. This protects many resources—Virtual Machines (VMs), Virtual Machine Scale Sets (VMSS), Application Gateway, Azure Firewall, Bastion, Load Balancers, and NICs—at the network boundary.
* DDoS IP Protection (per-public-IP): enable protection per Public IP resource. Billing is per protected public IP and suited to scenarios with only a few IPs to secure.

<Frame>
  <img alt="The image is a diagram showing the Azure DDoS Network Protection tiers, illustrating the flow from the internet to a load balancer, virtual machine scale set, and associated network components like managed disks and storage accounts." />
</Frame>

<Frame>
  <img alt="The image illustrates a network diagram of Azure DDoS protection tiers featuring DDoS IP protection, showing elements like a public IP, load balancer, virtual machine scale set within a virtual network, and components like managed disks and storage accounts for diagnostic logs." />
</Frame>

## Pricing and notable differences

* Network Protection: typically a fixed monthly fee (common plan-level pricing examples are around \$2,500/month) regardless of how many resources are attached—cost-effective when protecting many resources.
* IP Protection: billed per protected Public IP address—cost-effective when you only need protection for a small number of IPs.

| Aspect           | DDoS Network Protection (Plan)                                                    | DDoS IP Protection (Per IP)                                 |
| ---------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Scope            | Protects VNets and all attached resources (LB, App Gateway, Firewall, NICs, etc.) | Protects specific Public IP resources                       |
| Billing          | Fixed monthly plan fee                                                            | Charged per protected public IP                             |
| Best for         | Large deployments with many public endpoints                                      | Small deployments or isolated public IPs                    |
| Example scenario | Protect entire VNet containing multiple apps and load balancers                   | Protect a single public-facing appliance or legacy endpoint |

> **lightbulb** Azure provides a Basic level of DDoS protection for public IPs at no extra charge. Microsoft has announced deprecation plans for certain Basic SKUs—check the official Azure DDoS Protection documentation for current status and migration guidance: [https://learn.microsoft.com/azure/ddos-protection/](https://learn.microsoft.com/azure/ddos-protection/)

## Deployment and configuration (high-level)

A typical deployment workflow for DDoS Network Protection:

1. Create a DDoS Protection plan in the Azure portal (this is the network/plan-level offering).
2. Attach the plan to one or more virtual networks (existing or new).
3. Enable telemetry and diagnostic logging to collect attack telemetry and metrics.
4. Configure alerts and action groups to notify security teams on suspicious traffic or attack events.
5. Test and monitor using controlled/simulated traffic or synthetic checks where allowed.

<Frame>
  <img alt="The image is a guide on deploying a DDoS protection plan, showing steps including creating a protection plan, enabling on VNets, configuring telemetry, setting diagnostic alerts, and testing. It includes a screenshot of a user interface from a software application related to DDoS protection." />
</Frame>

The portal provides visibility into which VNets and resources are protected under a plan, and where diagnostic logs are stored for investigation.

## Scope of protection per plan type

* Network Protection: protects the VNets you associate with the plan, covering many attached resources such as Azure Firewall, Application Gateway, Bastion, Load Balancers, VM NICs, and more.
* IP Protection: protects only the explicit Public IPs you enable (either newly created or edited existing Public IP resources).

<Frame>
  <img alt="The image is a webpage from Microsoft's site comparing features of Azure DDoS Protection tiers, showing a table with two columns for &#x22;DDoS IP Protection&#x22; and &#x22;DDoS Network Protection&#x22; alongside feature availability. A navigation menu on the left provides links to different sections and topics related to Azure DDoS Protection." />
</Frame>

## Create a DDoS Protection plan in the Azure portal

Steps to create a Network Protection plan:

* In the Azure portal search box, type “DDoS protection plans”.
* Select your subscription and resource group, choose a plan name and region (for example, East US).
* Review and accept charges, then create the plan.
* After creation, attach the plan to the virtual networks you want to protect.

<Frame>
  <img alt="The image shows the Microsoft Defender for Cloud interface in Azure, focusing on the 'Regulatory Compliance' section with a search for DDoS protection plans." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure portal screen where a user is in the process of creating a DDoS protection plan. It displays details like subscription, resource group, name, and region, with an option to create the plan." />
</Frame>

The Network Protection plan you create here is a plan-level (Network) offering, not the per-IP protection model.

<Frame>
  <img alt="The image shows a Microsoft Azure portal page for Network security, specifically focusing on DDoS Protection, with a message indicating that there are no DDoS protection plans to display. There is an option to create a new DDoS protection plan." />
</Frame>

## Creating per-IP protection

To protect an individual Public IP:

1. Go to Public IP addresses in the Azure portal.
2. Create a new Public IP resource or edit an existing one.
3. Enable DDoS protection for that Public IP to apply the per-IP protection model.
4. Note: per-IP protected addresses are billed under the IP Protection model.

<Frame>
  <img alt="The image shows a Microsoft Azure portal page where a user is creating a public IP address. The form includes fields for subscription, resource group, and region selection." />
</Frame>

<Frame>
  <img alt="The image shows a Microsoft Azure interface where a user is in the process of creating a public IP address, selecting DDoS protection options." />
</Frame>

> **warning** DDoS Protection Standard and per-IP protection can be expensive depending on scale. Evaluate whether a plan-level purchase (Network Protection) or per-IP billing is more cost-effective for your architecture. Use Azure Cost Management and tagging to estimate and monitor costs.

## Cost considerations and best practices

* Choose Network Protection when you need broad coverage across multiple VNets and many public endpoints.
* Choose Per-IP Protection when protecting a small number of Public IPs; compare aggregated per-IP fees vs. a single plan fee.
* Always enable diagnostic logs (sent to a Storage Account, Log Analytics workspace, or Event Hub) and create alerts to integrate with your incident response workflow.
* Regularly test mitigations with controlled simulations and maintain runbooks for responding to DDoS incidents.
* Combine DDoS protection with rate-limiting, Web Application Firewall (WAF), and network-level filtering for layered defense.

## Summary

Azure DDoS Protection offers flexible options to defend against large-scale volumetric attacks and targeted IP-level threats. Choose Network Protection for broad, multi-resource coverage and per-IP protection for targeted scenarios. Regardless of the model, enable telemetry, diagnostics, and alerting to maintain visibility and responsiveness during incidents.

Further reading and references:

* Azure DDoS Protection documentation: [https://learn.microsoft.com/azure/ddos-protection/](https://learn.microsoft.com/azure/ddos-protection/)
* Azure Cost Management: [https://learn.microsoft.com/azure/cost-management-billing/](https://learn.microsoft.com/azure/cost-management-billing/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/2dfc3e6d-61ae-4c3c-a71d-559cd1e302af/lesson/f9e31aed-1e1a-412c-8ffe-e0d702223643)
