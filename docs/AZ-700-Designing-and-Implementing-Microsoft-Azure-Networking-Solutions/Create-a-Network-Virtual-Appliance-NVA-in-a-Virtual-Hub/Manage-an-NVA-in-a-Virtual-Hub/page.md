# Manage an NVA in a Virtual Hub

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Create-a-Network-Virtual-Appliance-NVA-in-a-Virtual-Hub/Manage-an-NVA-in-a-Virtual-Hub/page

Guidance for selecting, deploying, integrating, and operating Network Virtual Appliances in an Azure Virtual Hub, including marketplace deployment, hub routing integration, resource organization, sizing, and monitoring.

This lesson explains how to manage a Network Virtual Appliance (NVA) in an Azure Virtual Hub and outlines the high-level steps to plan, deploy, and operate an appliance integrated with hub routing.

Overview

* A Network Virtual Appliance (NVA) provides virtualized network functions such as firewalls, routing, SD‑WAN, or packet inspection.
* When used with an Azure Virtual Hub (part of Virtual WAN), NVAs can be deployed from the Azure Marketplace and integrated into the hub’s routing so traffic is steered through them for inspection, routing, or policy enforcement.
* The following sections walk through selecting an NVA, deploying it from the Marketplace, how Azure integrates it into the hub, and how resources are organized in your subscription.

Key steps

1. Select the NVA offer
2. Deploy the NVA from Marketplace
3. Azure provisions and integrates the NVA into your Virtual Hub
4. Organize and manage the resulting resources in your subscription

Step 1 — Select the NVA offer

* Search the Azure Marketplace for NVAs that match your functional and non‑functional requirements (for example: firewall, advanced routing, SD‑WAN, IDS/IPS).
* Evaluate each offer for:
  * Feature set required (L3/L4 routing, L7 inspection, high‑availability models)
  * Supported deployment modes (single NIC, multi‑NIC, inline/hub integration)
  * Throughput and performance claims
  * Licensing model (BYOL, pay-as-you-go, subscription)
* Consider vendor documentation and reference architectures to ensure the appliance supports the Virtual Hub integration pattern you need.

Step 2 — Deploy the NVA from Marketplace

* Marketplace NVAs are typically shipped as managed applications or publisher offerings. During deployment you will configure:
  * Virtual machine size (CPU, memory)
  * Instance count (number of VM instances or scale units)
  * Aggregate capacity/throughput and licensing options
  * Networking settings to attach the appliance into the Virtual Hub
* Capacity and scaling characteristics are vendor-specific; consult the appliance vendor documentation to map your expected traffic to the appropriate instance size and count.

<Callout icon="lightbulb">
  Capacity, throughput, and licensing vary by vendor. Confirm vendor performance and high-availability guidance to size instance types and counts for your expected traffic patterns.
</Callout>

Step 3 — Azure provisions and integrates the NVA into your hub

* After submitting deployment settings, Azure will provision VM instances and any required networking resources inside the selected Virtual Hub (or a managed resource group controlled by the publisher).
* The deployed NVA instances are integrated into the hub’s routing and connectivity. Integration typically includes:
  * Route table entries or hub routing policies to steer traffic through the NVA
  * Network interfaces attached to the hub or associated subnets
  * Health probes or load‑balancing indicators (vendor-dependent) for HA and traffic distribution

Step 4 — Resource organization in your subscription

* Marketplace deployments commonly split resources between publisher-managed and customer-managed resource groups to clarify management and support boundaries.

| Resource group type     | Purpose                                                                               | Examples                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Managed Resource Group  | Publisher- or Azure-managed resources deployed as part of the Marketplace application | `VM instances`, `publisher-managed NICs`, `load balancer components`           |
| Customer Resource Group | Resources you own and manage for configuration and integration                        | Hub configuration artifacts, routing policy objects, custom automation scripts |

* Keeping resources in separate groups simplifies lifecycle operations, billing, and support handoffs between the appliance publisher and your operations team.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Managing an NVA in a Virtual Hub,&#x22; outlining the process from choosing an NVA offer to deployment and subscription in Azure services. It includes steps like selecting deployment settings and managing resource groups." />
</Frame>

Operational checklist

* Validate vendor capacity with representative traffic tests or vendor sizing tools.
* Decide on HA pattern: active/active, active/passive, or vendor-specific clustering.
* Configure hub route policies to steer required traffic to the NVA.
* Implement monitoring and alerting for instance health and throughput.
* Maintain a clear separation of publisher-managed vs. customer-managed resources for upgrades and troubleshooting.

References and further reading

* Azure Virtual WAN: [https://learn.microsoft.com/azure/virtual-wan/](https://learn.microsoft.com/azure/virtual-wan/)
* Azure Marketplace: [https://azuremarketplace.microsoft.com/](https://azuremarketplace.microsoft.com/)
* Vendor-specific NVA documentation (check the Marketplace offer listing for links)

By following these steps you ensure your NVAs are deployed consistently, operate within expected capacity limits, and are integrated into your Virtual Hub routing fabric—reducing manual configuration and simplifying ongoing operations. Detailed deployment steps for a specific NVA and Virtual Hub integration are provided in the vendor and Azure Virtual WAN documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/e948f42e-2daf-4044-94be-e714418a6dbf/lesson/af6df5e0-5698-458a-8536-f2165c047205" />
</CardGroup>
