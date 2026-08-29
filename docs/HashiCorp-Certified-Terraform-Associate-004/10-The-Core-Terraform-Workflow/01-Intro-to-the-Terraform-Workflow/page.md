# root module variables (variables.tf)
variable "environment" {
  type    = string
  default = "prod"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "project" {
  type    = string
  default = "myapp"
}

# child module variables (variables.tf)
variable "env" {
  type = string
}

variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "az_count" {
  type    = number
  default = 2
}
```

Because each module has an isolated scope, the child module does not automatically see `environment` or `region` from the root, and the root does not automatically see `cidr_block` or `az_count` from the child. This behavior is intentional: modules act like black-box functions that only observe inputs you provide.

<Frame>
  <img alt="The image illustrates the concept of variable isolation between a Root Module and a Child Module, separated by a boundary that blocks variable exchange." />
</Frame>

Note: Modules behave like functions — they only see the inputs you explicitly provide to them.

<Callout icon="lightbulb">
  Modules have isolated scopes. You must explicitly pass values between modules; variables are not shared implicitly.
</Callout>

Passing values into a child module (module block)

To provide values to a child module, set arguments in the `module` block of the calling (root) module. Each argument corresponds to a declared input variable in the child module.

Example — passing a root variable into a child module:

```hcl theme={null}
# root module - main.tf
module "child" {
  source = "./modules/child"

  # pass root module variable value into the child module's `env` variable
  env = var.environment
}
```

What you can pass into a module

* Root variables: `var.<NAME>` (e.g., `var.environment`)
* Resource attributes: `aws_vpc.example.id`
* Another module's outputs: `module.network.subnet_ids[0]`
* Hard-coded literals: `"us-west-2"`, `42`, `true`

Quick reference table

| Value type         | Example                        |
| ------------------ | ------------------------------ |
| Root variable      | `var.environment`              |
| Resource attribute | `aws_vpc.example.id`           |
| Module output      | `module.network.subnet_ids[0]` |
| Literal            | `"us-west-2"`                  |

Example from the Registry (root calling an external VPC module):

```hcl theme={null}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "4.0.1"

  name               = var.vpc_name
  cidr               = var.vpc_cidr_block
  azs                = ["us-west-2a", "us-west-2b"]
  private_subnets    = ["10.0.1.0/24"]
  public_subnets     = ["10.0.101.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}
```

Defaults and overrides

* Child-module variables can include defaults (for example, `az_count = 2`). If the caller doesn't pass a value, the child uses that default.
* Well-designed modules provide sensible defaults while permitting callers to override behavior via input variables.

Outputting data from a child module back to the root

A child module exposes internal values to its caller by defining `output` blocks. The root (or another calling module) can then read those outputs via `module.<NAME>.<OUTPUT>`.

Example — child module outputs:

```hcl theme={null}
# child module - outputs.tf
output "subnet_one" {
  value = aws_subnet.subnet1.id
}

output "subnet_two" {
  value = aws_subnet.subnet2.id
}

output "subnet_three" {
  value = aws_subnet.subnet3.id
}
```

Using the child module output in the root module:

```hcl theme={null}
# root module - main.tf
resource "aws_instance" "web" {
  subnet_id = module.network.subnet_one
  # ...
}
```

Passing outputs into another module:

```hcl theme={null}
module "webserver" {
  source    = "./modules/webserver"
  subnet_id = module.network.subnet_one
}
```

<Frame>
  <img alt="The image illustrates the concept of outputting data from a child module back to a root module, with a focus on resource management in a network context. It highlights how subnets are output from the child module to the root module, and notes that the root module does not have default access to the child module's data." />
</Frame>

Summary

* Variables are scoped to the module where they are declared.
* To provide input to a child module, pass values in the `module` block of the calling module.
* To expose values from a child module to its caller, create `output` blocks in the child and reference them via `module.<NAME>.<OUTPUT>`.
* Values passed between modules can be root variables, resource attributes, other module outputs, or literals — ensure the receiving module declares the corresponding input variable.

Links and references

* [Terraform Modules Overview](https://www.terraform.io/language/modules)
* [Terraform Input Variables](https://www.terraform.io/language/values/variables)
* [Terraform Output Values](https://www.terraform.io/language/values/outputs)
* [Terraform Registry](https://registry.terraform.io/)
* [HashiCorp Certified: Terraform Associate training (KodeKloud)](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/7a9b9328-bd7d-4cb0-99f2-2ac166f272a7/lesson/629e1af0-5117-4c95-a064-281840d4f417" />
</CardGroup>


# Intro to the Terraform Workflow

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Intro-to-the-Terraform-Workflow/page

Overview of Terraform's core Write Plan Apply workflow, including init, planning, applying, HCL configuration, best practices, and common commands.

HashiCorp’s canonical Terraform workflow is simple and consistent: three core stages that apply whether you’re managing a single VM or a multi-cloud environment. Understanding this flow is essential for reliable infrastructure as code.

The stages are:

* Write — declare the infrastructure you want using configuration files (HCL).
* Plan — preview what Terraform will change by comparing your configuration to the current state.
* Apply — execute those changes to create or update real infrastructure, with Terraform resolving resource dependencies automatically.

Write → Plan → Apply — that’s the canonical workflow. These steps interact in practice and are supported by a required initialization step before planning or applying.

<Frame>
  <img alt="The image illustrates the official Terraform workflow with three steps: Write, Plan, and Apply, accompanied by purple arrows and text descriptions." />
</Frame>

When you run terraform apply, Terraform performs the operations needed to make real infrastructure match the declared desired state. Terraform automatically respects resource dependencies. For example, if a database resource must exist before a web server, Terraform will create the database first — you don’t need to orchestrate that manually.

Before plan or apply can run, Terraform needs to be initialized.

terraform init downloads provider plugins and any referenced modules into the working directory. If your configuration targets AWS, Terraform fetches the AWS provider; for Azure, the Azure provider; and so on. Running `terraform init` is a required setup step for each new project directory and whenever you add or change provider/module blocks.

<Callout icon="lightbulb">
  Always run `terraform init` when you start working in a new Terraform project or after adding new provider/module references. Without initialization, `terraform plan` and `terraform apply` will fail.
</Callout>

<Frame>
  <img alt="The image outlines the Terraform workflow, featuring four steps: Writing Configuration (HCL), Initializing, Planning, and Applying." />
</Frame>

Day-to-day workflow (practical sequence)

1. Write your configuration files (.tf) in HCL to declare the desired state.
2. Initialize the directory: run `terraform init`.
3. Preview changes: run `terraform plan`.
4. Apply changes: run `terraform apply`.

Common Terraform commands

```bash theme={null}
