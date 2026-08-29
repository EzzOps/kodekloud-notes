# variables.tf
variable "cidr_block" {
  type        = string
  description = "The IPv4 CIDR block for the VPC"
  default     = "192.168.0.0/16"
}

variable "vpc_name" {
  type        = string
  description = "Name tag for the VPC"
  default     = "my-terraform-vpc"
}
```

Note: The VPC module’s default CIDR is `10.0.0.0/16`; changing `cidr_block` to `192.168.0.0/16` demonstrates overriding a module default.

For more inputs including tags, route tables, and subnet options see the module inputs:

<Frame>
  <img alt="The image shows a webpage from the Terraform AWS modules registry, detailing inputs for a Virtual Private Cloud (VPC) module, including default settings for IP configurations and tags." />
</Frame>

## Add the VPC module (main.tf)

Add a module block in `main.tf` that references the Registry source and wires the root variables into the module inputs:

```hcl theme={null}
# main.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.19.0"

  name = var.vpc_name
  cidr = var.cidr_block
}
```

## Provider configuration (providers.tf)

Declare the required provider constraint and configure the AWS provider. Credentials are supplied via environment variables or other supported credential providers.

```hcl theme={null}
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Credentials: use environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
}
```

<Callout icon="warning">
  Ensure your AWS credentials are available before running Terraform commands. You can export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`, or use the AWS CLI credential store.
</Callout>

## Initialize the working directory

Open a terminal, confirm your credentials, then run:

```bash theme={null}
terraform init
```

This downloads providers and any referenced modules. Example important output:

```bash theme={null}
Downloading registry.terraform.io/terraform-aws-modules/vpc/aws 5.19.0 for vpc...
- vpc in .terraform/modules/vpc
Initializing provider plugins...
- Finding hashicorp/aws versions matching "5.89.0"
- Installing hashicorp/aws v5.89.0...
- Installed hashicorp/aws v5.89.0 (signed by HashiCorp)

Terraform has created a lockfile .terraform.lock.hcl to record the provider selections it made above.
```

After init, Terraform will have downloaded the VPC module into `.terraform/modules/vpc` and installed the AWS provider plugin.

<Callout icon="lightbulb">
  Run [`terraform init`](https://developer.hashicorp.com/terraform/cli/commands/init) after adding or changing module sources so Terraform can download required modules and providers.
</Callout>

## Plan and apply the VPC

Plan to preview the resources the module will create. Depending on inputs and defaults the VPC module may create a VPC, route tables, a default security group, network ACLs, and subnets.

```bash theme={null}
terraform plan
# Example summary:
# Plan: 4 to add, 0 to change, 0 to destroy.
```

Apply the plan:

```bash theme={null}
terraform apply
# Confirm with 'yes' when prompted
```

Example (truncated) apply output:

```plaintext theme={null}
module.vpc.aws_default_route_table.default[0]: Creation complete [id=rtb-xxxxxxxx]
module.vpc.aws_default_network_acl.this[0]: Creation complete [id=acl-xxxxxxxx]
module.vpc.aws_default_security_group.this[0]: Creation complete [id=sg-xxxxxxxx]
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
```

Inspect the state:

```bash theme={null}
terraform state list
# module.vpc.aws_default_network_acl.this[0]
# module.vpc.aws_default_route_table.default[0]
# module.vpc.aws_default_security_group.this[0]
# module.vpc.aws_vpc.this[0]
```

Confirm in the AWS Console (VPCs) that the VPC exists and the CIDR matches the value you provided (`192.168.0.0/16` in this example): [https://console.aws.amazon.com/vpc/home](https://console.aws.amazon.com/vpc/home)

<Frame>
  <img alt="The image shows an AWS VPC console displaying a list of Virtual Private Clouds (VPCs), with selected details for one VPC named &#x22;my-terraform-vpc&#x22; highlighted, indicating it is available." />
</Frame>

## Export the VPC ID from the module (outputs.tf)

To use the VPC ID elsewhere, expose the module output at the root level by adding an output:

```hcl theme={null}
# outputs.tf
output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "The ID of the VPC created by the vpc module"
}
```

The VPC module documents its outputs on the Registry; copy the exact output name (here `vpc_id`) from the module page.

<Frame>
  <img alt="The image shows a webpage from the Terraform AWS modules registry, specifically detailing various output parameters related to VPC modules, such as outpost subnets and private route IDs." />
</Frame>

Apply again (adding an output does not create AWS resources):

```bash theme={null}
terraform apply
# Confirm with 'yes'
```

Example outputs:

```plaintext theme={null}
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
Outputs:
vpc_id = "vpc-0c11fbe634c8a9edf"
```

## Use the VPC ID input for another module (security group)

Now consume that exported VPC ID in a security group module (`terraform-aws-modules/security-group/aws`). The security group module expects `vpc_id` among its inputs.

Append the following to `main.tf`:

```hcl theme={null}
module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  vpc_id = module.vpc.vpc_id
  name   = "my-cool-security-group"
}
```

This module supports many ingress/egress inputs such as `egress_rules`, `egress_ipv6_cidr_blocks`, `ingress_rules`, etc. We only pass the required `vpc_id` and a `name` in this example.

<Frame>
  <img alt="The image displays a section of the Terraform AWS security group documentation, listing egress rule inputs with descriptions and default values. It includes terms like egress_ipv6_cidr_blocks, egress_prefix_list_ids, and egress_rules." />
</Frame>

Because this is a new external module, re-run:

```bash theme={null}
terraform init
```

Then:

```bash theme={null}
terraform plan
terraform apply
# Confirm with 'yes'
```

Example apply output:

```plaintext theme={null}
module.security_group.aws_security_group.this_name_prefix[0]: Creation complete after 2s [id=sg-078db811ad40027cd]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Verify in the AWS Console under EC2 → Security Groups that `my-cool-security-group` exists and is attached to the same VPC.

## Export the security group ID (append to outputs.tf)

To expose the created security group ID from the module, add an output in `outputs.tf`:

```hcl theme={null}
# outputs.tf (append)
output "sg_id" {
  value       = module.security_group.security_group_id
  description = "The ID of the security group created by the security group module"
}
```

Apply one more time (outputs only):

```bash theme={null}
terraform apply
# Confirm with 'yes'
```

Example resulting outputs:

```plaintext theme={null}
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
Outputs:
sg_id  = "sg-078db811ad40027cd"
vpc_id = "vpc-0c11fbe634c8a9edf"
```

## Quick command reference

| Command                | Purpose                                                         |
| ---------------------- | --------------------------------------------------------------- |
| `terraform init`       | Download providers and modules referenced by your configuration |
| `terraform plan`       | Preview changes Terraform will make                             |
| `terraform apply`      | Apply the planned changes to create/update resources            |
| `terraform state list` | Inspect tracked resources in the state file                     |

## Summary

* The Terraform Registry hosts thousands of reusable modules. Inspect module READMEs for inputs and outputs before consumption.
* Call child modules in the root module with `module "<name>" { source = "..." }` and pass values via module inputs.
* Modules can export outputs you reference as `module.<MODULE_NAME>.<output_name>`; those values can be passed into other modules.
* Always run `terraform init` whenever you add or change external module sources so Terraform downloads the modules and providers.

Use Registry modules to compose infrastructure quickly—delegate resource details to tested modules and wire them together with clear inputs and outputs.

## Links and references

* Terraform Registry — [https://registry.terraform.io](https://registry.terraform.io)
* terraform-aws-modules/vpc/aws — [https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)
* terraform-aws-modules/security-group/aws — [https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws/latest](https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws/latest)
* AWS provider documentation — [https://registry.terraform.io/providers/hashicorp/aws/latest](https://registry.terraform.io/providers/hashicorp/aws/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/7a9b9328-bd7d-4cb0-99f2-2ac166f272a7/lesson/c3fa64d8-e20e-43f3-8b1f-a7e52ed25978" />
</CardGroup>


# Introduction to Modules

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Modules/Introduction-to-Modules/page

Explains Terraform modules including structure, usage, sources, versioning and benefits for building reusable, consistent, maintainable infrastructure

Welcome to the Introduction to Terraform Modules.

This lesson explains how Terraform modules let you package related infrastructure-as-code into reusable, logical components. Organizing configurations into modules reduces repetition, enforces consistency across environments, and makes it easier to share well‑tested patterns across teams.

We’ll cover core concepts including module structure, usage, sources, and versioning so you can build, consume, and maintain reusable Terraform modules. Let’s dive into why modules are essential for scalable, maintainable infrastructure.

## What is a module?

A module is a container for related Terraform resources that are commonly used together — for example, the resources that make up a subnet, a VPC, or an application stack. Modules are the recommended way to package and reuse configurations.

When you run Terraform, the configuration in the working directory is the root (or parent) module. Any other module called from the root module is a child (reusable) module. Using modules helps encapsulate complexity and standardize patterns.

<Callout icon="lightbulb">
  The root module is the directory where you run Terraform commands. Child modules live in other directories, remote registries, or version control and are referenced via `module` blocks.
</Callout>

## Benefits of using modules

Using modules delivers several operational and organizational advantages:

* Improved organization: Break large configurations into smaller, easier-to-reason units.
* Easier collaboration: Publish vetted modules to a registry or shared repo so teams consume standardized building blocks.
* Consistent patterns: Centralize naming, tagging, sizing, and security controls in modules to enforce best practices.

<Frame>
  <img alt="The image explains modules as containers for related resources, highlighting their benefits: improved organization, easier collaboration, and consistent patterns." />
</Frame>

When platform or security teams review and approve modules, your organization can ensure deployments follow standards without each consumer needing to implement the same checks.

## Modules as building blocks

Instead of placing many resource blocks (TLS certificate, load balancer, message queue, Kubernetes cluster, database, etc.) into a single configuration, define each piece once as a module and reuse it across multiple root modules.

For example:

* A Marketing Application might reference the TLS and Load Balancer modules.
* A GenAI service might reference those plus GPU-backed cluster and specialized queue modules.

Root modules declare only the modules they need and configure them via inputs. This makes code DRY (Don’t Repeat Yourself), easier to test, and simpler to maintain.

<Frame>
  <img alt="The image illustrates Terraform building blocks, showing the connection between modules such as TLS Certificate and Load Balancer and applications like Marketing Application and GenAI Service." />
</Frame>

## What does a module look like?

A module is simply a directory containing standard Terraform files. The most common layout is:

* `main.tf` — resources and core configuration
* `variables.tf` — input variables the module accepts
* `outputs.tf` — outputs the module exposes to callers
* (optional) `versions.tf` — provider and Terraform version constraints
* (optional) `examples/` — example usage to help consumers

Example filesystem layout:

```text theme={null}
modules/
  tls/
    main.tf
    variables.tf
    outputs.tf
  load_balancer/
    main.tf
    variables.tf
    outputs.tf
```

Common module file types and purpose

| File           | Purpose                                 | Example                                                                     |
| -------------- | --------------------------------------- | --------------------------------------------------------------------------- |
| `main.tf`      | Define resources and composition        | `resource "aws_acm_certificate" "example" { ... }`                          |
| `variables.tf` | Declare input variables and defaults    | `hcl variable "domain_name" { type = string } `                             |
| `outputs.tf`   | Expose values to calling module         | `hcl output "certificate_arn" { value = aws_acm_certificate.example.arn } ` |
| `versions.tf`  | Lock Terraform and provider versions    | `hcl terraform { required_version = ">= 1.0.0" } `                          |
| `examples/`    | Example root module demonstrating usage | `examples/complete/main.tf`                                                 |

Example: calling a local child module from a root module

```hcl theme={null}
module "tls" {
  source = "./modules/tls"

  domain_name = "example.com"
  cert_tags   = {
    environment = "prod"
  }
}
```

Minimal `variables.tf` inside the module:

```hcl theme={null}
variable "domain_name" {
  type        = string
  description = "Domain name for the TLS certificate"
}

variable "cert_tags" {
  type        = map(string)
  description = "Tags to apply to the certificate"
  default     = {}
}
```

Minimal `outputs.tf` inside the module:

```hcl theme={null}
output "certificate_arn" {
  description = "The ARN of the TLS certificate"
  value       = aws_acm_certificate.example.arn
}
```

## Module sources and versioning

Modules can be sourced from several places: local paths, Git repositories, Terraform Registry, or other VCS. Always prefer versioned sources for reproducible builds when pulling remote modules.

Examples of module sources

| Source type    | Example                                                                                             |
| -------------- | --------------------------------------------------------------------------------------------------- |
| Local path     | `source = "./modules/network"`                                                                      |
| Git (with ref) | `source = "git::https://github.com/example-org/terraform-modules.git//modules/postgres?ref=v1.2.0"` |
| Registry       | `source = "app.terraform.io/example-org/mysql/aws"`                                                 |
| Archive URL    | `source = "https://example.com/terraform-modules.tar.gz"`                                           |

When referencing remote modules, pin to a specific tag, branch, or commit using `?ref=` to avoid accidental changes.

## Declaring and using module blocks

To reuse a module, declare a `module` block in your root module and set the `source` and any required inputs. The root module receives outputs from the child module as attributes.

Example with multiple modules:

```hcl theme={null}
module "network" {
  source = "./modules/network"
  vpc_cidr = "10.0.0.0/16"
}

module "db" {
  source = "git::https://github.com/example-org/terraform-modules.git//modules/postgres?ref=v1.2.0"
  db_name      = "appdb"
  instance_tier = "db.t3.medium"
}
```

Best practices for module authorship

* Keep modules focused and single-purpose.
* Use clear, descriptive variable names and document defaults.
* Provide outputs that callers need without exposing internal resource IDs unnecessarily.
* Include examples and tests (e.g., Terratest or Kitchen-Terraform) where feasible.
* Apply provider and Terraform version constraints in `versions.tf`.
* Use semantic versioning and tag releases for remote modules.

## Summary

Modules are the primary mechanism in Terraform for packaging, sharing, and enforcing infrastructure patterns. Use them to:

* Reduce duplication
* Improve maintainability
* Standardize security and operational controls

By organizing infrastructure as reusable modules and versioning them responsibly, teams gain scalability and governance while keeping root modules concise and readable.

## Links and References

* [Terraform Documentation: Modules](https://www.terraform.io/language/modules)
* [Terraform Registry](https://registry.terraform.io/)
* [Terraform CLI: Module Sources](https://www.terraform.io/language/modules/sources)
* [Semantic Versioning](https://semver.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/7a9b9328-bd7d-4cb0-99f2-2ac166f272a7/lesson/d7e308d3-d224-426f-a4a8-019b2f68b4b5" />
</CardGroup>
