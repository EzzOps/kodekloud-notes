# Calling Modules with the Module Block

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Modules/Calling-Modules-with-the-Module-Block/page

Explains Terraform module blocks for calling reusable modules to organize, reuse, and version infrastructure code, with examples, attributes, reuse patterns, and best practices.

Welcome to this lesson on the `module` block in Terraform.

This article is a concise, practical introduction to modules and how the `module` block helps you organize reusable infrastructure as code. Modules let you group related resources into composable building blocks so you can reuse, version, and share tested infrastructure patterns across projects and teams.

## What is a Terraform module?

A Terraform module is a collection of resources, variables, and outputs that together implement a logical piece of infrastructure (for example: networking, databases, or a Kubernetes cluster). You call a module using a `module` block from another configuration to instantiate that set of resources with specific input values.

Modules reduce duplication and make infrastructure easier to manage:

* Reusability: Share standard patterns across teams.
* Maintainability: Break large configurations into smaller, focused pieces.
* Consistency: Versioned modules enforce tested configurations.

When managing multiple applications that require similar resources (databases, networks, load balancers, etc.), modules let you avoid copying resource definitions into each configuration. Instead, each application references reusable modules and passes inputs to customize them.

<Frame>
  <img alt="The image illustrates Terraform building blocks for a marketing application, showing modules like TLS Certificate, Load Balancer, Message Queuing, Kubernetes Cluster, and Database Cluster. These modules are connected to module blocks within the application setup." />
</Frame>

For example, a marketing application can call a module that provisions a TLS certificate, a load balancer, and a Kubernetes cluster. The module encapsulates the necessary resources and exposes variables to customize values such as certificate names or cluster sizes.

Another example: a GenAI service for a customer website can reuse the same modules—add `module` blocks, pass the required inputs, and avoid duplicating resource definitions.

<Frame>
  <img alt="The image illustrates the concept of Terraform building blocks, showing a connection between a marketing application and a GenAI service through various modules like TLS certificate, load balancer, message queuing, Kubernetes cluster, and database cluster." />
</Frame>

## How the module block works

The `module` block calls a module source and injects it into your current configuration. You provide inputs (variables) to configure the module and the module returns outputs that other parts of your configuration can use.

Common use cases:

* Reusing a network module across multiple environments with different CIDR blocks.
* Sharing a standardized database cluster setup across several applications.
* Composing modules together to form complex architectures without repeating low-level resource definitions.

<Frame>
  <img alt="The image is a promotional graphic for HashiCorp Terraform, featuring a hand holding a purple block. The text describes the &#x22;Module Block&#x22; feature, explaining how it helps organize Terraform configurations." />
</Frame>

## Example: Using a VPC module from the Terraform Registry

Below is a typical example using a popular AWS VPC module from the Terraform Registry. Instead of creating many networking resources directly, you call a tested module and pass the values you need.

```hcl theme={null}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "4.0.1"

  name           = var.vpc_name
  cidr           = var.vpc_cidr_block

  azs            = ["us-west-2a", "us-west-2b"]
  private_subnets = ["10.0.1.0/24"]
  public_subnets  = ["10.0.101.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}
```

How to read this example:

* `source` — Where the module code lives (a Registry module in this case).
* `version` — Pins a specific module release to ensure reproducible runs.
* Inputs such as `name`, `cidr`, and the subnet lists correspond to variables declared inside the module and let you customize its behavior.

## Common module block attributes

| Attribute          | Purpose                                                                                                 | Example                         |
| ------------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `source`           | Location of the module code. Can be a Registry address, Git URL, local path, or other supported source. | `terraform-aws-modules/vpc/aws` |
| `version`          | (Registry modules) Pin the module version to ensure reproducible deployments.                           | `"4.0.1"`                       |
| inputs (arguments) | Values you pass to module variables to configure the module.                                            | `name = var.vpc_name`           |
| outputs            | Values the module exports so other resources can consume them.                                          | `module.vpc.public_subnets`     |

## Reuse patterns

* Call the same module multiple times with different arguments to create multiple instances (e.g., separate VPCs for different environments).
* Use `for_each` or `count` with module blocks to dynamically create multiple module instances when supported (Terraform 0.13+ supports loop over modules).
* Version pin modules and review changes before upgrading to avoid surprises in production.

## Best practices

* Keep module interfaces small and stable: expose only the variables and outputs needed.
* Pin module versions and test upgrades in a staging environment.
* Publish commonly used modules to a private module registry or the Terraform Registry for easy discovery and reuse.
* Document module inputs, outputs, and behavior so other teams can consume them correctly.

> **lightbulb** Pinning a module version ensures reproducible deployments. Test new module versions deliberately — do not rely on automatically pulling the latest release.

## Quick reference and further reading

* Terraform Modules documentation: [https://www.terraform.io/docs/language/modules/index.html](https://www.terraform.io/docs/language/modules/index.html)
* Terraform Registry (modules): [https://registry.terraform.io/](https://registry.terraform.io/)
* Best practices for reusable modules: [https://www.terraform.io/docs/language/modules/develop/index.html](https://www.terraform.io/docs/language/modules/develop/index.html)

By organizing your infrastructure into modules, you improve maintainability, consistency, and team productivity—enabling infrastructure-as-code patterns that scale across projects.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/7a9b9328-bd7d-4cb0-99f2-2ac166f272a7/lesson/35b3ebdb-6412-45a4-8f62-28afa6637f7c)
