# Azure Resource Tags

Source: https://notes.kodekloud.com/docs/Updated-AZ-104-Microsoft-Azure-Administrator/Administer-Governance-and-Compliance/Azure-Resource-Tags/page

Guide explaining Azure resource tags, how to manage them in the portal, enforce inheritance with Azure Policy, and follow best practices for organization and cost allocation.

Tags in Azure are key-value pairs you attach to resources to provide searchable metadata for organization, governance, automation, and cost allocation. In environments with many subscriptions, resource groups, and resources, tags help you identify ownership, environment, project, and billing information quickly and consistently.

This guide explains how Azure resource tags work, how to manage them in the Azure portal, and best practices for tagging at scale.

## Why use Azure tags?

Use tags to add metadata, group cross-resource workloads, and track costs. Common scenarios include ownership, environment identification, project grouping, and cost center allocation.

| Use case         |                                                 Purpose | Example tag               |
| ---------------- | ------------------------------------------------------: | ------------------------- |
| Ownership        |                 Identify the responsible person or team | `Owner: Sam`              |
| Environment      |         Separate production, staging, and dev resources | `Environment: Production` |
| Project grouping | Group resources across resource groups or subscriptions | `Project: Apollo`         |
| Cost allocation  |            Attribute spend to finance codes or projects | `CostCenter: 1100`        |

Key points about scope and inheritance:

* Tags can be applied to subscriptions, resource groups, and individual resources.
* Billing and cost reporting are determined at the resource level—tags must be on the resource for accurate cost allocation.
* Tags do not automatically flow from a resource group or subscription to underlying resources unless you enforce that behavior (for example, through Azure Policy or supported preview features).

<Callout icon="lightbulb">
  Tip: If you prefer tagging at the resource group level for human convenience, use policy enforcement to copy or inherit those tags onto resources so billing and automation tools see them at the resource level.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;Azure Resource Tags&#x22; showing four use cases—Adding metadata, Logical grouping, Name-value pair, and Cost management—each illustrated with an Azure icon and a colored tag. A footer notes that tags don't follow inheritance by default and Azure Policy can be used to inherit tags from a resource group or subscription." />
</Frame>

## Preview features vs. production

Azure occasionally offers preview capabilities for tag inheritance. In production, rely on GA (generally available) features like Azure Policy to ensure consistent, auditable, and enforceable tag behavior.

<Callout icon="warning">
  Warning: Avoid relying on preview features in production. Prefer policy enforcement to ensure tag inheritance and governance for stable, auditable behavior.
</Callout>

## Managing tags in the Azure portal

Follow these steps to add or edit tags on individual resources from the portal:

1. Open the Azure portal and go to All resources.
2. Select a resource (for example, a virtual machine or storage account) and open the Tags pane.
3. Add name-value pairs. Example:
   * Name: `Owner` — Value: `Sam`
   * Name: `Environment` — Value: `Dev`
   * Name: `CostCenter` — Value: `1100`
4. Save to apply the tags.

The portal suggests existing tag names and values from your subscription while you type, encouraging consistent naming and reuse.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;All resources&#x22; list and the &#x22;about-rithin&#x22; storage account details, with an &#x22;Edit tags&#x22; panel open where an Environment tag value (e.g., &#x22;Dev&#x22;) is being entered. The left pane lists multiple resources and the center pane shows resource properties and services." />
</Frame>

## Filter, discover, and edit tagged resources

* Filtering: Use the filters in All resources to find resources by tag (for example, filter where `Environment` = `Dev` to show development resources).
* Tag blade: The Tags blade lists all name-value combinations used across the subscription. Clicking an entry shows resources that use that tag.
* Editing tags on a resource: Open the resource, click Edit tags, change the value or delete a tag using the trash icon, then save. Refresh the resource list or Tags view to see updates.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the overview for a virtual machine named &#x22;about-rithin-vm&#x22; with the Edit tags pane open. The tags shown include &#x22;Cost Center: 1100&#x22; and &#x22;Environment: Dev.&#x22;" />
</Frame>

## Tag listing and propagation

* The Tags blade provides a subscription-wide view of tag keys and values and enables quick navigation to tagged resources.
* You can add new keys or values directly from the Tags blade; newly added entries will appear across the portal after a refresh.
* To ensure tags exist on resources (important for billing and automation), use Azure Policy to enforce tag presence, copy tags from resource groups, or deny resource creation unless required tags are present.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Tags&#x22; blade with tag entries like &#x22;Cost Center : 1100&#x22;, &#x22;Environment : Dev&#x22;, and &#x22;Environment : Prod&#x22;. A cursor is hovering over or clicking the &#x22;Environment : Prod&#x22; tag." />
</Frame>

## Applying tags to resource groups

* Resource group tags help organization and discovery, especially for teams that think in terms of application boundaries.
* Resource group tags do not automatically propagate to underlying resources unless you deploy or enforce propagation (for example, with Azure Policy).
* For production governance, enforce tag standards and inheritance via Azure Policy to ensure consistent application across resources and accurate cost reporting.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Resource groups&#x22; view with the &#x22;about-rithin&#x22; resource group selected and a list of resources (VMs, public IP, NSG, disks, etc.) in the right-hand pane. The left navigation menu, filters, and subscription/essentials info are also visible." />
</Frame>

## Best practices for tagging

* Define a tagging taxonomy and publish it (keys, allowed values, conventions).
* Standardize on casing and separators (e.g., kebab-case or PascalCase) to avoid duplicates like `CostCenter` vs `cost-center`.
* Use a small, consistent set of keys (Owner, Environment, Project, CostCenter, Compliance) to reduce management overhead.
* Enforce mandatory tags at resource creation using Azure Policy and remediate noncompliant resources automatically where appropriate.
* Review and clean up unused tag keys periodically to keep the catalog manageable.

## Summary

* Tags are name-value pairs used to label resources for management, billing, and organization.
* For billing and automation, tags must exist on the resource level—resource group or subscription tags won’t automatically apply to resources without enforcement.
* Use Azure Policy to enforce tagging standards, automate inheritance, and maintain consistent governance at scale.

## Links and references

* [Azure Policy documentation](https://learn.microsoft.com/azure/governance/policy/)
* [Tag resources in Azure](https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources)
* [Azure cost management and billing](https://learn.microsoft.com/azure/cost-management-billing/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/df99187b-f512-443a-a64b-93af9d73c5bc/lesson/00d038ab-75ff-452a-b885-1a1324b4f015" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/az-104-microsoft-azure-administrator/module/df99187b-f512-443a-a64b-93af9d73c5bc/lesson/4b712333-ccaf-4e8b-9ff1-90288e4853e0" />
</CardGroup>
