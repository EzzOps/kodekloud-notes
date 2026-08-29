# Demo Using Modules from the Terraform Registry

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Modules/Demo-Using-Modules-from-the-Terraform-Registry/page

Guide on using Terraform Registry modules to provision an AWS VPC and security group, exporting and passing module outputs between modules.

Welcome — in this hands-on lesson you'll learn how to consume reusable modules from the [Terraform Registry](https://registry.terraform.io). We'll:

* Provision an AWS VPC using the community module `terraform-aws-modules/vpc/aws`.
* Export the VPC ID from that module to the root module.
* Pass the VPC ID into a security group module (`terraform-aws-modules/security-group/aws`) so the security group is created in the same VPC.
* Do all of this without writing any low-level `aws_*` resource blocks in the root module.

Project layout — create these files in a new directory:

| File           | Purpose                                                              |
| -------------- | -------------------------------------------------------------------- |
| `main.tf`      | Module blocks that call registry modules (VPC, security group)       |
| `variables.tf` | Root-module variable declarations and defaults                       |
| `providers.tf` | Provider configuration (AWS provider, required provider constraints) |
| `outputs.tf`   | Root-module outputs that expose child-module outputs                 |

<Frame>
  <img alt="The image shows a Visual Studio Code window with a Terraform project open, displaying files like main.tf, variables.tf, and providers.tf. The editor area is open with a suggestion prompt visible." />
</Frame>

## Browse the Terraform Registry

The Terraform Registry hosts both providers and modules. Modules are reusable collections of Terraform configuration (typically `main.tf`, `variables.tf`, and `outputs.tf`) published by the community or organizations. Search the Registry for provider-specific modules (AWS, Azure, GCP, etc.) and review each module’s README to find inputs, outputs, and usage examples.

Below is an example page showing many AWS community modules (EKS, Lambda, KMS, and more).

<Frame>
  <img alt="The image displays a webpage from the Terraform Registry showcasing various Terraform AWS modules, such as those for EKS, security groups, Lambda, and KMS. Each module listing includes the name, description, and usage statistics." />
</Frame>

For this demo we’ll use the popular module: `terraform-aws-modules/vpc/aws`. It exposes many optional inputs and useful outputs.

## Inspect the VPC module README, inputs, and outputs

Registry modules usually document their inputs (variables) and outputs clearly in the README. Many inputs are optional and provide sensible defaults — you only need to override the values you want to change.

<Frame>
  <img alt="The image shows a webpage from the Terraform AWS Modules registry, specifically detailing optional inputs for an AWS VPC module. It includes descriptions and default values for variables like amazon_side_asn and azs." />
</Frame>

## Define variables (variables.tf)

Create `variables.tf` and declare the root-module variables you’ll pass into the VPC module. In this example we provide a CIDR block and a VPC name, both with defaults.

```hcl theme={null}
