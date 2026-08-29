# Multiple Resources

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/HashiCorp-Configuration-Language/Multiple-Resources/page

Explains how to define and manage multiple Azure resources with Terraform using provider declaration, resource blocks, inter-resource references, and plan apply workflow.

So far we've been working with single resources to learn Terraform syntax. Real-world infrastructure rarely consists of only one resource — applications typically require networking, storage, databases, compute, and supporting services working together.

This lesson shows how to define multiple resources in one Terraform configuration so they are managed together predictably and repeatably.

Concept overview

* A provider (for example, the AzureRM provider) is the communication layer between Terraform and a cloud platform such as Azure.
* Providers implement many resource types (virtual networks, storage accounts, SQL databases, Kubernetes clusters, etc.).
* Each resource type documents its available arguments (some required, some optional) in the Terraform provider docs: [https://registry.terraform.io/](https://registry.terraform.io/).

<Frame>
  <img alt="The image illustrates the concept of managing multiple resources using the &#x22;azurerm provider,&#x22; featuring icons for SQL and other services with associated arguments. There's also a section on the right outlining an argument reference guide for configuring these resources." />
</Frame>

Key concept: Terraform is declarative — you describe the desired state and Terraform determines the actions required to reach that state. When multiple resource blocks are present in the same configuration, Terraform analyzes references between them to determine ordering and dependencies.

Example: resource group, virtual network, storage account
Below is a concise, real-world example showing multiple resources in a single configuration. Note how resources reference one another (so values are not duplicated) and how blocks are structured.

```hcl theme={null}
provider "azurerm" {
  features {}
}
