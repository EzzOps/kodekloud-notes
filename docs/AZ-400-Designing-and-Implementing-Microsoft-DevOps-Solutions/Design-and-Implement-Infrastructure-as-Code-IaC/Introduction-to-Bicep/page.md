# Introduction to Bicep

Source: https://notes.kodekloud.com/docs/AZ-400-Designing-and-Implementing-Microsoft-DevOps-Solutions/Design-and-Implement-Infrastructure-as-Code-IaC/Introduction-to-Bicep/page

Overview of Microsoft Bicep language for declaring and deploying Azure resources, covering syntax, examples, installation, authoring best practices, and deployment workflows

Welcome to this lesson on [Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview) — Microsoft’s concise domain-specific language (DSL) for declaring and managing Azure resources. Bicep delivers a cleaner, more maintainable authoring experience than raw [ARM template JSON](https://learn.microsoft.com/azure/azure-resource-manager/templates/overview) while producing the same ARM artifacts that Azure consumes. Use Bicep to improve readability, modularity, and maintainability of your Infrastructure as Code (IaC).

<Frame>
  <img alt="A presentation slide titled &#x22;Bicep – Introduction&#x22; with a centered blue hexagon Bicep logo. The text says Bicep is a Microsoft domain-specific language that simplifies declaring Azure resources compared to traditional ARM templates." />
</Frame>

How Bicep works:

* Author readable .bicep files with declarative resource definitions.
* Bicep compiles (either implicitly during deployment or explicitly with the Bicep CLI) to ARM template JSON that Azure understands.
* This approach gives you concise syntax and full ARM compatibility for deployment scenarios and tooling.

Key benefits:

* Simpler, more readable syntax compared to raw ARM JSON.
* Native support for modularity and reuse through modules.
* Less boilerplate and easier maintenance for growing templates.

Example: simple storage account in Bicep

```bicep theme={null}
@description('Specifies the location for resources.')
param location string = 'eastus'

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: 'mystorageaccountname'
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Premium_LRS'
  }
}
```

Installation options

* The [Azure CLI](https://learn.microsoft.com/cli/azure/?view=azure-cli-latest) bundles Bicep support, so many users do not need a separate binary.
* You can also install or update Bicep directly on each OS via the standalone binary or package managers. See the official installation guide: [https://learn.microsoft.com/azure/azure-resource-manager/bicep/install?tabs=azure-cli](https://learn.microsoft.com/azure/azure-resource-manager/bicep/install?tabs=azure-cli)

<Callout icon="lightbulb">
  If you have a recent Azure CLI installation, the az bicep commands are available without a separate binary. Run az bicep version to confirm availability.
</Callout>

Common platform install examples

PowerShell (Windows):

```powershell theme={null}
Set-ExecutionPolicy Bypass -Scope Process -Force; iwr -useb https://aka.ms/installbicep | iex
```

Linux (standalone binary example):

```bash theme={null}
curl -Lo bicep https://github.[AWS_SECRET_ACCESS_KEY]/bicep-linux-x64
chmod +x ./bicep
sudo mv ./bicep /usr/local/bin/bicep
```

macOS (Homebrew example):

```bash theme={null}
brew tap azure/bicep
brew install bicep
```

Core Bicep language building blocks

| Building Block | Purpose                                                  | When to use                                                              |
| -------------- | -------------------------------------------------------- | ------------------------------------------------------------------------ |
| Parameter      | Input supplied at deployment time                        | Make templates flexible and reusable across environments                 |
| Variable       | Reusable expressions or computed values                  | Avoid repeating logic and improve readability                            |
| Resource       | Declaration of Azure resources with type and API version | All infrastructure is declared as resources                              |
| Module         | Encapsulated Bicep file used as a child template         | Reuse and compose complex deployments                                    |
| Output         | Values returned after deployment                         | Expose IDs, endpoints, connection strings for scripts or other templates |

Authoring best practices

* Use parameters and variables to keep templates configurable across environments (dev/prod).
* Group related resources and extract repeatable patterns into modules.
* Use resource loops and conditions to minimize duplicated code.
* Leverage built-in functions for string manipulation, resource IDs, and array handling.
* Secure secrets using [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/overview) rather than embedding them in templates.

<Frame>
  <img alt="A colorful slide titled &#x22;Authoring With Bicep&#x22; showing five numbered tips for effective Azure Bicep scripting. The tips cover naming conventions, validating/previewing templates, implementing outputs, handling dependencies, and secure handling of sensitive data." />
</Frame>

More practical authoring tips:

* Adopt consistent naming conventions for resources, parameters, and modules.
* Validate and preview templates before deployment using the deployment what-if and validate operations.
* Emit outputs for important resource IDs, connection strings, and endpoints for downstream automation.
* Model resource dependencies explicitly (dependsOn or implicit references) to ensure correct provisioning order.
* Avoid storing secrets in code—use Key Vault references or secure parameter inputs.

<Callout icon="warning">
  Never commit secrets or credentials to source control. Use Key Vault references, Azure AD-backed service principals, or secure parameter files for sensitive values.
</Callout>

Deploying Bicep with Azure CLI
High-level deployment workflow:

1. Install and sign in with the [Azure CLI](https://learn.microsoft.com/cli/azure/?view=azure-cli-latest).
2. Optionally compile a .bicep file to ARM JSON using az bicep build for debugging or CI scenarios.
3. Create or choose an existing resource group.
4. Deploy the Bicep file with az deployment group create (or use subscription/management group scope as needed).

<Frame>
  <img alt="A presentation slide titled &#x22;Authoring With Bicep&#x22; with the subtitle &#x22;Process of Deploying a Bicep File Using Azure CLI.&#x22; It shows two colorful panels labeled &#x22;01 Install Azure CLI&#x22; and &#x22;02 Install Bicep CLI&#x22; with short notes about installing each." />
</Frame>

Useful CLI commands

|                                                                   Command | Purpose                                 |
| ------------------------------------------------------------------------: | --------------------------------------- |
|                                                                  az login | Authenticate to Azure                   |
|                                             az bicep build --file \<file> | Compile .bicep to ARM JSON (optional)   |
|                            az group create --name \<rg> --location \<loc> | Create a resource group                 |
| az deployment group create --resource-group \<rg> --template-file \<file> | Deploy a Bicep file to a resource group |

Example CLI steps:

```bash theme={null}
