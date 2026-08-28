# Azure Firewall Manager policies

Source: https://notes.kodekloud.com/docs/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Working-with-Azure-Firewall-Manager/Azure-Firewall-Manager-policies/page

Guide to centralizing and automating Azure Firewall policies across subscriptions, regions, and virtual hubs, explaining policy models, management options, associations, and providing CLI and Bicep examples.

Learn how Azure Firewall Manager policies centralize and scale Azure Firewall configuration across subscriptions, regions, and virtual hubs. This guide explains the policy model, management options, association patterns, and includes practical CLI and Bicep examples to help you create and deploy Firewall Policies consistently.

## What is Azure Firewall Manager?

Azure Firewall Manager is a centralized management service that sits above individual Azure Firewall instances and virtual hubs. It enables administrators to create, distribute, and manage Firewall Policies across many firewalls and environments, ensuring consistent security controls and simplified operations at scale.

Key capabilities:

* Centralized policy authoring and distribution
* Support for cross-subscription and cross-region assignments
* Layered/global + local policy model for baseline controls with environment-specific overrides
* Multiple management interfaces for automation and integration

## Flexible policy management

Firewall Policies can be created and managed through several Microsoft tooling options, allowing you to pick the approach that fits your automation and operational model:

* Azure Portal — visual authoring and quick edits.
* REST API — integrate with automation pipelines.
* ARM / Bicep templates — infrastructure-as-code deployments.
* Azure PowerShell — scriptable automation for PowerShell users.
* Azure CLI — scriptable automation for Bash and CI systems.

<Frame>
  <img alt="The image illustrates &#x22;Flexible Policy Management&#x22; for Azure Firewall Manager, showing management options like Azure Portal, REST API, Templates, Azure PowerShell, and CLI." />
</Frame>

Management options at a glance:

|        Interface | Use case                                           | Example                                                                                        |
| ---------------: | -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
|     Azure Portal | Manual authoring, review, and ad-hoc updates       | Use the Firewall Manager blade to create policies                                              |
|         REST API | Integrate with external systems or custom tooling  | [https://docs.microsoft.com/rest/api/firewall/](https://docs.microsoft.com/rest/api/firewall/) |
|      ARM / Bicep | Declarative, repeatable infrastructure deployments | Bicep example below                                                                            |
| Azure PowerShell | PowerShell-centric automation and runbooks         | `New-AzFirewallPolicy -Name "MyPolicy" -ResourceGroupName "RG"`                                |
|        Azure CLI | Shell scripts and CI/CD pipelines                  | `az network firewall policy create --name MyPolicy --resource-group RG --location eastus`      |

Example: Create a Firewall Policy with Azure CLI

```bash theme={null}
az network firewall policy create \
  --name MyFirewallPolicy \
  --resource-group myResourceGroup \
  --location eastus \
  --tags "env=prod" "owner=security"
```

Example: Basic Bicep snippet to create a Firewall Policy

```bicep theme={null}
resource fwPolicy 'Microsoft.Network/firewallPolicies@2021-08-01' = {
  name: 'myFirewallPolicy'
  location: 'eastus'
  properties: {
    threatIntelMode: 'Alert'
  }
}
```

## Association with multiple hubs or VNets

A single Firewall Policy can be associated with multiple Azure Firewall instances or virtual hubs (vHubs). When attached, the policy governs the firewall's behavior for the deployment (for example, traffic filtering, NAT, application rules, TLS inspection settings, and logging). This helps avoid duplicated rules across environments and reduces configuration drift.

Common association patterns:

* One policy applied to multiple production hubs for uniform controls.
* One global policy + per-hub local policies for exceptions and additional rules.
* Dedicated policies per environment when isolation is required.

## Cross-subscription and cross-regional support

Firewall Policies can be applied to firewall resources across subscriptions and regions. Azure Firewall Manager supports centralized policy assignment, but this requires proper RBAC and management scope configuration so the management account has rights over target resources.

<Callout icon="warning">
  Ensure your management/service account has the necessary RBAC permissions and management group or subscription scopes when assigning policies across subscriptions. Lack of appropriate access will prevent policy assignment and lifecycle management.
</Callout>

## Layered (global) vs local policy model

A recommended deployment pattern is layered policies:

* Global (baseline) policy: defined by central security teams to ensure organization-wide controls (allow/deny lists, logging, threat intelligence).
* Local policy: defined by regional or application teams to add environment-specific rules or exceptions.

This layered approach balances centralized governance with local flexibility. The diagram below shows how a global policy can be pushed to many hubs while specific hubs may also combine global and local policies as needed.

<Frame>
  <img alt="The image is a diagram illustrating Azure Firewall Manager's cross-subscription and regional support, showing connections between different network hubs: &#x22;Prod Hub Vwan,&#x22; &#x22;Staging Hub VNET,&#x22; and &#x22;Dev Hub VNET,&#x22; all utilizing global policies." />
</Frame>

<Callout icon="lightbulb">
  Use a global policy to enforce organization-wide controls (for example, deny lists, allow lists, and logging). Apply local policies for environment-specific exceptions or additional rules.
</Callout>

## How to create, attach, and verify Firewall Policies

Below are practical examples to help you create a policy and attach it to an Azure Firewall or vHub.

1. Create a Firewall Policy (Azure CLI)

```bash theme={null}
az network firewall policy create \
  --name GlobalPolicy \
  --resource-group infra-rg \
  --location eastus
```

2. Attach a Firewall Policy to an Azure Firewall (Azure CLI)

```bash theme={null}
az network firewall update \
  --name MyAzureFirewall \
  --resource-group prod-rg \
  --firewall-policy /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/infra-rg/providers/Microsoft.Network/firewallPolicies/GlobalPolicy
```

3. Bicep example: create a firewall and attach a policy

```bicep theme={null}
resource fwPolicy 'Microsoft.Network/firewallPolicies@2021-08-01' existing = {
  name: 'GlobalPolicy'
}

resource firewall 'Microsoft.Network/azureFirewalls@2021-08-01' = {
  name: 'myAzureFirewall'
  location: 'eastus'
  properties: {
    sku: {
      name: 'AZFW_VNet'
      tier: 'Standard'
    }
    firewallPolicy: {
      id: fwPolicy.id
    }
  }
}
```

4. Verify the association (Azure CLI)

```bash theme={null}
az network firewall show \
  --name MyAzureFirewall \
  --resource-group prod-rg \
  --query "firewallPolicy.id" \
  --output tsv
```

## Policy design checklist

* Define global baseline rules for all hubs (logging, threat intel, deny lists).
* Use local policies sparingly for necessary exceptions.
* Automate policy creation and assignment using Bicep/ARM or CLI in CI/CD pipelines.
* Validate RBAC and management scopes before assigning cross-subscription policies.
* Test policy impact in staging before applying to production.

## Links and references

* [Azure Firewall Manager overview](https://learn.microsoft.com/azure/firewall-manager/)
* [Firewall Policy documentation](https://learn.microsoft.com/azure/firewall/policy-overview)
* [Azure CLI networking commands](https://learn.microsoft.com/cli/azure/network)

Now that you understand Azure Firewall Manager policy concepts, management options, and deployment patterns, you can design a layered policy framework and automate policy distribution across your organization.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-700-designing-and-implementing-microsoft-azure-networking-solutions/module/51f1c934-1aa2-45ea-8c2a-791e6dd8e948/lesson/a1775cd1-1555-4f4b-b9fb-0b0ab46705ea" />
</CardGroup>
