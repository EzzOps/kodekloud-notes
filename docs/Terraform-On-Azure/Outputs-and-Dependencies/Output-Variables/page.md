# Output Variables

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Outputs-and-Dependencies/Output-Variables/page

Explains Terraform output variables and how to expose runtime values like IPs, IDs, and sensitive data for automation and workflows

In this lesson we explain Terraform output variables — the mechanism Terraform uses to expose useful runtime information after resources are created.

An output answers a simple question: How do I get values out of Terraform after `apply`?

Common use cases for outputs:

* Expose values only known after creation (for example, IP addresses or resource IDs).
* Display operational information such as public IPs, URLs, or connection strings.
* Pass values to other modules, scripts, or CI/CD pipelines to enable further automation and orchestration.

<Frame>
  <img alt="The image is an infographic explaining output variables, focusing on their roles in exposing values, displaying resource details, and enabling further processing in Terraform." />
</Frame>

## Example resources

We’ll use a minimal example: an Azure resource group and an Azure public IP. The `ip_address` attribute is assigned by Azure only after the resource is created — which is exactly why outputs are useful.

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "output-demo-rg"
  location = "East US"
}

resource "azurerm_public_ip" "public_ip" {
  name                = "demo-public-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Basic"
}
```

## Output block structure

An `output` block provides a name and a `value`, and may optionally include a `description`, `sensitive`, and other arguments. The `value` is normally a reference to a resource attribute — not a hard-coded literal.

General form:

```hcl theme={null}
output "<name>" {
  value       = <expression>
  description = "<optional description>"
  # other optional arguments ...
}
```

Example — expose the public IP address assigned by Azure:

```hcl theme={null}
output "public_ip_address" {
  description = "The public IP address of the deployed resource"
  value       = azurerm_public_ip.public_ip.ip_address
}
```

This value is evaluated after `apply` because `ip_address` is assigned dynamically by Azure.

## Where to put outputs

Terraform will load outputs from any `.tf` file in the current working directory (for example, `main.tf`). As a best practice, keep outputs in a dedicated `outputs.tf` file for clarity and easier maintenance.

Example showing both locations are valid:

```hcl theme={null}
