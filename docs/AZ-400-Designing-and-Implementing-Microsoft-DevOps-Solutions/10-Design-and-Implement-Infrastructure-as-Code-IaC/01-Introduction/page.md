# Sign in
az login

# Compile a Bicep file to ARM JSON (optional)
az bicep build --file ./main.bicep

# Create a resource group
az group create --name myResourceGroup --location eastus

# Deploy the Bicep file to a resource group
az deployment group create --resource-group myResourceGroup --template-file ./azuredeploy.bicep --parameters storageAccountType=Standard_GRS
```

Visual Studio Code integration

* Use VS Code with the Bicep extension for IntelliSense, syntax highlighting, and snippets.
* The extension enables validation, quick fixes, and direct deployment capabilities when signed into your Azure account.
* For a streamlined authoring experience, enable the Bicep extension and configure the Azure Account extension to authenticate from the editor.

<Frame>
  <img alt="A presentation slide titled &#x22;Deploying With Bicep in Visual Studio Code&#x22; showing three colored feature cards labeled 01 IntelliSense, 02 Code snippets, and 03 Direct deployment capabilities with icons. The slide includes a © Copyright KodeKloud notice in the corner." />
</Frame>

Deploying from Azure Cloud Shell

* Upload your .bicep file to the [Cloud Shell](https://learn.microsoft.com/azure/cloud-shell/overview) using drag-and-drop or the Cloud Shell upload options.
* Use the same az group create and az deployment group create commands in Cloud Shell for zero-local-setup deployments.

```bash theme={null}
az group create --name ExampleGroup --location "Your Location"
az deployment group create --resource-group ExampleGroup --template-file azuredeploy.bicep --parameters storageAccountType=Standard_GRS
```

Azure Automanage Machine Configuration
[Azure Automanage](https://learn.microsoft.com/azure/automanage/) Machine Configuration automates VM configuration and applies recommended best practices and security guidelines to supported virtual machines. Automanage simplifies operational management across VM fleets by ensuring consistent configuration, patching, and policy enforcement.

<Frame>
  <img alt="A presentation slide titled &#x22;Azure Automanage Machine Configuration Extension.&#x22; It shows two rounded colored boxes labeled &#x22;01 Best Practices&#x22; and &#x22;02 Security Guidelines.&#x22;" />
</Frame>

Closing notes

* Bicep improves authoring productivity and maintainability compared to raw ARM JSON while remaining fully compatible with Azure's resource model.
* Start small: convert simple ARM templates into Bicep, validate locally, and adopt modules for repeated patterns as your IaC footprint grows.
* Use CI/CD pipelines to compile and validate Bicep artifacts, and follow security best practices to protect credentials and secrets.

Links and references

* [Bicep Overview (Microsoft Learn)](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview)
* [Bicep Install Guide](https://learn.microsoft.com/azure/azure-resource-manager/bicep/install?tabs=azure-cli)
* [ARM templates overview](https://learn.microsoft.com/azure/azure-resource-manager/templates/overview)
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/?view=azure-cli-latest)
* [Azure Key Vault documentation](https://learn.microsoft.com/azure/key-vault/general/overview)
* [Azure Cloud Shell overview](https://learn.microsoft.com/azure/cloud-shell/overview)
* [Azure Automanage documentation](https://learn.microsoft.com/azure/automanage/)

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/75eafabe-1911-4a4e-a7fb-277f6aa6e2d0/lesson/cb59c871-c341-4dbd-94f6-02ef1f601474)


# Introduction

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Infrastructure-as-Code-IaC/Introduction/page

Learn to design and implement Infrastructure as Code solutions for Azure, covering configuration management, Desired State Configuration, IaC strategy, and deployment environments.

In this lesson, you’ll learn how to design and implement Infrastructure as Code (IaC) solutions for Azure. We’ll cover:

1. **Configuration Management**\
   – Definition and core concepts\
   – Key benefits in Azure\
   – Overview of Azure configuration management tools and best practices

2. **Desired State Configuration (DSC)**\
   – Azure Automation State Configuration\
   – Azure Resource Manager (ARM) and Bicep\
   – Azure Automanage Machine Configuration

3. **Building Your IaC Strategy**\
   – Fundamental IaC principles\
   – Leveraging source control for infrastructure definitions\
   – Automating testing and deployment pipelines

4. **Azure Deployment Environments**\
   – Understanding on-demand, self-service infrastructure\
   – Comparing blue-green, canary, and rolling deployment strategies\
   – Configuring Azure DevOps for automated provisioning\
   – Monitoring and maintaining deployment environments

Let’s dive into each of these topics step by step.

***

## 1. Configuration Management in Azure

Configuration management ensures that your application infrastructure remains consistent, secure, and compliant. By defining your environment as code, you can:

* Prevent configuration drift
* Enforce security standards
* Automate patching and updates
* Scale environments reliably

### Key Azure Configuration Management Tools

| Tool                                   | Purpose                                     | Documentation                                                                                     |
| -------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Azure Automation State Configuration   | DSC-based configuration at scale            | [Learn more](https://docs.microsoft.com/azure/automation/automation-state-configuration/overview) |
| Azure Resource Manager (ARM)           | Declarative templates for resource delivery | [Learn more](https://docs.microsoft.com/azure/azure-resource-manager/templates/overview)          |
| Bicep                                  | Domain-specific language for ARM templates  | [Learn more](https://docs.microsoft.com/azure/azure-resource-manager/bicep/overview)              |
| Azure Automanage Machine Configuration | Automated OS and VM guest configuration     | [Learn more](https://docs.microsoft.com/azure/automanage/automanage-overview)                     |

> **lightbulb** Choosing the right configuration management tool depends on your organization’s scale, existing skill set, and compliance requirements.

***

## 2. Desired State Configuration (DSC)

Desired State Configuration (DSC) is a PowerShell-based platform that enables you to declaratively define and maintain system configurations.

* **Azure Automation State Configuration**: Host DSC pull servers in Azure to manage Windows and Linux machines.
* **ARM & Bicep**: Use ARM templates or Bicep files to define the desired state of Azure resources.
* **Azure Automanage Machine Configuration**: Simplify VM configuration with managed services that automatically apply best practices.

***

## 3. Developing an IaC Strategy

A solid IaC strategy encompasses:

1. **Core Concepts**\
   – Declarative vs. imperative approaches\
   – Idempotency and immutability
2. **Source Control Integration**\
   – Storing templates in Git repositories\
   – Branching strategies (e.g., GitFlow, trunk-based development)
3. **Pipeline Automation**\
   – Unit testing templates (e.g., [ARM-TTK](https://github.com/Azure/arm-template-toolkit))\
   – Continuous Integration/Continuous Deployment (CI/CD) workflows in Azure DevOps or GitHub Actions

> **triangle-alert** Always validate your templates in a non-production environment before promoting to production to avoid unintended resource changes.

***

## 4. Designing Azure Deployment Environments

When architecting deployment environments in Azure, consider:

* **Environment Types**: Development, testing, staging, production

* **Deployment Strategies**:
  | Strategy   | Description                                 | Use Case                         |
  | ---------- | ------------------------------------------- | -------------------------------- |
  | Blue-Green | Two identical environments, switch traffic  | Zero-downtime deployments        |
  | Canary     | Incremental rollout to a subset of users    | Mitigate risk for new features   |
  | Rolling    | Update small sets of instances sequentially | Controlled, progressive upgrades |

* **Self-Service Provisioning**: Configure Azure DevOps pipelines and templates to allow teams to spin up environments on demand.

* **Monitoring & Maintenance**: Use Azure Monitor, Application Insights, and Policy for ongoing health checks and compliance.

***

## Next Steps

Now that you have an overview of Azure IaC concepts and tools, we’ll begin our deep dive into configuration management technologies. In the following section, we’ll define configuration management in detail and demonstrate how to get started with Azure Automation State Configuration.

- [Watch Video](https://learn.kodekloud.com/user/courses/az-400/module/75eafabe-1911-4a4e-a7fb-277f6aa6e2d0/lesson/bda4079b-c9c1-4a2d-be15-5aa8140c2c85)
