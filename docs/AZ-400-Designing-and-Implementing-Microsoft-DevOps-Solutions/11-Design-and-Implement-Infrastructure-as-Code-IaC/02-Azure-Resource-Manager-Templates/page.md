# Compile the configuration to a local folder
ScheduledTaskDaily -OutputPath "$env:Temp\DSC"
```

<Callout icon="lightbulb">
  Ensure you include `StartBoundary` and `RepeatDuration` when you need the schedule to span a specific time window.
</Callout>

1. In the portal, go to **State Configuration (DSC)** > **Configurations**.
2. Click **Add**, upload the compiled `.mof` file from `"$env:Temp\DSC"`.
3. Confirm and **Save**.

<Frame>
  ![The image shows a screenshot of the Azure portal, specifically the Azure Automation State Configuration (DSC) section, with options for managing configurations and a highlighted example of creating a scheduled task.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867694/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-portal-automation-dsc-screenshot.jpg)
</Frame>

Compile status will appear in **Configuration Versions**.

<Frame>
  ![The image shows a screenshot of the Azure Automation State Configuration interface, highlighting the "Compile" option for a specific configuration. It includes details like resource group, location, and subscription information.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867695/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-state-configuration-screenshot-2.jpg)
</Frame>

***

## Step 4: Assign the Configuration to the VM

Apply the new DSC configuration to your node:

1. Under **State Configuration (DSC)** > **Nodes**, select your VM.
2. Click **Assign Node Configuration**.
3. Choose the `ScheduledTaskDaily` configuration version and **OK**.

<Frame>
  ![The image shows a screenshot of the Azure Automation State Configuration interface, specifically the "Assign Node Configuration" section, with a list of resources and services on the left sidebar.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867697/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Automation-State-Configuration/azure-automation-state-configuration-screenshot-3.jpg)
</Frame>

* The node will show **Noncompliant** until DSC applies your settings.
* After successful application, it returns to **Compliant**, indicating the scheduled task is in place.

***

## Links and References

* [Azure Automation DSC Overview](https://docs.microsoft.com/azure/automation/automation-dsc-overview)
* [PowerShell ScheduledTask DSC Resource](https://docs.microsoft.com/powershell/module/psdesiredstateconfiguration/scheduledtask)
* [Az.Automation PowerShell Module](https://www.powershellgallery.com/packages/Az.Automation)
* [Azure Virtual Machine Agent](https://docs.microsoft.com/azure/virtual-machines/extensions/agent-windows)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/75eafabe-1911-4a4e-a7fb-277f6aa6e2d0/lesson/9c20a5b5-9c80-40ab-846e-1a6559323ca3" />
</CardGroup>


# Azure Resource Manager Templates

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Infrastructure-as-Code-IaC/Azure-Resource-Manager-Templates/page

Use Azure Resource Manager templates to define cloud infrastructure as code, enabling repeatable, auditable, and automated deployments in Azure.

Use Azure Resource Manager (ARM) templates to define your cloud infrastructure as code (IaC), enabling repeatable, auditable, and automated deployments. Once authored in JSON, you can version, share, and deploy these templates to build consistent Azure environments.

<Frame>
  ![The image is an introduction to Azure Resource Manager Templates, showing a flowchart with three stages: ARM Template Creation, Automated Deployment, and Configured Resources.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867698/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/azure-resource-manager-templates-flowchart.jpg)
</Frame>

## Why Use ARM Templates?

ARM templates offer several advantages over manual provisioning:

| Benefit              | Description                                                   | Example                                                 |
| -------------------- | ------------------------------------------------------------- | ------------------------------------------------------- |
| Template Reuse       | Shareable across teams and projects                           | Use the same network template in dev, test, and prod    |
| Auditable Infra      | JSON files double as documentation for compliance             | Source control history shows every configuration change |
| Modular Architecture | Break large deployments into smaller, maintainable components | Separate templates for networking, storage, and compute |

<Frame>
  ![The image is an introduction slide for Azure Resource Manager Templates, highlighting two features: "Template reuse" and "Auditable infrastructure."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867699/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/azure-resource-manager-templates-introduction.jpg)
</Frame>

## Core Structure of an ARM Template

Every ARM template follows a consistent structure with four main sections:

* **parameters**: Define inputs to customize deployments.
* **variables**: Store reusable values or expressions.
* **resources**: Declare Azure resources to create or update.
* **outputs**: Return information after deployment for chaining or debugging.

<Frame>
  ![The image outlines the key components of ARM Templates, which include Parameters, Variables, Resources, and Outputs, each represented in a colored box.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867700/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/arm-templates-key-components-diagram.jpg)
</Frame>

Minimal ARM template example:

```json theme={null}
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {},
  "variables": {},
  "resources": [],
  "outputs": {}
}
```

## Managing Resource Dependencies

To avoid deployment errors—such as creating a VM before its storage account—you can use the `dependsOn` property. ARM ensures resources deploy in the correct order.

<Frame>
  ![The image is a slide titled "Managing Dependencies in ARM Templates," highlighting two points: ensuring correct deployment sequence and preventing errors and deployment failures. It includes icons representing these concepts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867700/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/managing-dependencies-arm-templates-slide.jpg)
</Frame>

```json theme={null}
{
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "name": "mystorageaccount",
      "apiVersion": "2021-04-01",
      "location": "eastus"
    },
    {
      "type": "Microsoft.Compute/virtualMachines",
      "name": "myVM",
      "apiVersion": "2021-07-01",
      "location": "eastus",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts', 'mystorageaccount')]"
      ],
      "properties": {
        // VM configuration here
      }
    }
  ]
}
```

<Frame>
  ![The image illustrates managing dependencies in ARM templates, showing a dependency between a storage account and a virtual machine.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867701/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/arm-templates-dependency-management-diagram.jpg)
</Frame>

## Secure Secret Management

Never embed secrets (passwords, API keys) directly in your templates. Instead, store them in [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/overview) and reference them at deployment time.

<Frame>
  ![The image compares insecure and secure methods of handling secrets in ARM templates, highlighting the use of hardcoding versus Azure Key Vault.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867702/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/secure-insecure-secrets-arm-templates.jpg)
</Frame>

<Callout icon="triangle-alert">
  Avoid hardcoding secrets in your JSON. Use `[reference()]` or `[listSecrets()]` to fetch values from Key Vault at runtime.
</Callout>

## Modular Template Organization

Organize large deployments by splitting templates into specialized files. Use a main template to link sub-templates for networking, storage, compute, and more:

<Frame>
  ![The image is a diagram showing the organization of ARM templates, with a "Main ARM Template" linking to a "Networking Template."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867703/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/arm-templates-organization-diagram.jpg)
</Frame>

This approach improves maintainability and streamlines complex setups.

## Azure Resource Manager Architecture

Azure Resource Manager is the control plane that validates, orchestrates, and enforces your desired state. You interact with ARM via the portal, CLI, PowerShell, or REST API.

<Frame>
  ![The image is a diagram illustrating the interaction between users and Azure Resource Manager, showing options to create, update, and delete resources.](../../../../images/kodekloud.com/kk-media/image/upload/v1752867704/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/azure-resource-manager-user-interaction-diagram.jpg)
</Frame>

ARM templates map directly to this architecture, providing `Deploy` and `Manage` functions for your resources:

<Frame>
  ![The image is a diagram showing the relationship between an ARM Template and its functions, "Deploy" and "Manage," in the context of Azure Resource Manager and DSC. It highlights that ARM Templates are essential for implementing DSC by defining "infrastructure as code."](../../../../images/kodekloud.com/kk-media/image/upload/v1752867705/notes-assets/images/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions-Azure-Resource-Manager-Templates/arm-template-functions-diagram-azure.jpg)
</Frame>

## Integrating DSC with ARM Templates

PowerShell Desired State Configuration (DSC) ensures each VM meets your specified state. Use the DSC extension in your ARM template to apply configurations at provisioning:

```json theme={null}
{
  "extensionProfile": {
    "extensions": [
      {
        "name": "DSCExtension",
        "properties": {
          "publisher": "Microsoft.PowerShell",
          "type": "DSC",
          "typeHandlerVersion": "2.9",
          "autoUpgradeMinorVersion": true,
          "settings": {
            "configuration": {
              "url": "https://example.com/MyDscConfiguration.zip",
              "script": "ConfigureFirewall.ps1",
              "function": "ConfigureFirewall"
            },
            "configurationArguments": {
              "nodeName": "Localhost"
            }
          },
          "protectedSettings": {
            "configurationUrlSasToken": "sasTokenValue"
          }
        }
      }
    ]
  }
}
```

DSC resources—such as `WindowsFeature` for IIS or `xWebsite` for site configuration—complement ARM templates by enforcing OS-level and application settings.

***

Bicep is a domain-specific language (DSL) that streamlines ARM template authoring by providing concise syntax and rich tooling support.

## Links and References

* [Azure Resource Manager Overview](https://learn.microsoft.com/azure/azure-resource-manager/management/overview)
* [Deploy resources with ARM templates](https://learn.microsoft.com/azure/azure-resource-manager/templates/overview)
* [Azure Key Vault Documentation](https://learn.microsoft.com/azure/key-vault/)
* [PowerShell DSC Extension](https://learn.microsoft.com/azure/virtual-machines/extensions/dsc-overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/az-400/module/75eafabe-1911-4a4e-a7fb-277f6aa6e2d0/lesson/801f312e-a143-4476-a43c-69d0ce437d8c" />
</CardGroup>
