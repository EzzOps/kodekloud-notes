# Learn the Basics of HashiCorp Configuration Language HCL

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Learn-the-Basics-of-HashiCorp-Configuration-Language-HCL/page

Introduction to HashiCorp Configuration Language explaining HCL syntax, structure, Terraform usage, resource and data blocks, style recommendations, and basic workflow for authoring infrastructure-as-code

Welcome to this focused introduction to HashiCorp Configuration Language (HCL). This lesson explains what HCL is, why Terraform uses it, and how to author clear, maintainable infrastructure-as-code using HCL.

HCL is a purpose-built, declarative language designed to express infrastructure intent in a readable and approachable way. It strikes a balance between simplicity and expressive power so both beginners and experienced engineers can read, write, and maintain Terraform configurations. By the end of this lesson you should be comfortable reading, authoring, and organizing basic HCL files for Terraform.

HCL is declarative: you describe the desired end state (for example, “a VPC with CIDR 10.0.0.0/16”) and Terraform determines how to create or update resources to match that state. Think of it like ordering a dish at a restaurant — you specify the final result, not every step required to cook it.

<Frame>
  <img alt="The image provides an overview of HashiCorp Configuration Language (HCL), highlighting its features such as being a declarative language, easy to read and write, and serving as Terraform’s primary interface." />
</Frame>

## HCL structure and basic syntax

HCL configurations are organized into blocks that group related configuration items. Each block has:

* A block type (for example, `resource`, `data`, `variable`, `output`)
* One or more labels (for example, a resource type and an instance name)
* A body containing arguments and optionally nested blocks

Comments are supported and useful for documenting intent:

* Single-line comments: `#` or `//`
* Multi-line (block) comments: `/* ... */`

Attributes are name/value pairs inside blocks that configure resources or data sources.

Example annotated HCL:

```hcl theme={null}
