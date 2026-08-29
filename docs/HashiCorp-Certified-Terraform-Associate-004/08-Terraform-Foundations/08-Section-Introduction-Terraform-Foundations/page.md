# single-line comment
block_type "block_label" "block_label" {
  first_argument  = expression or value
  second_argument = expression or value
  third           = expression or value
}

attribute_abc = "value_1"
attribute_2   = "value_2"
```

Core concepts at a glance

| Concept               | Why it matters                                                                                                          | Example                                                                      |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Dynamic configuration | Avoid hard-coding values; reuse attributes emitted by one resource in another                                           | A VM references `aws_subnet.example.id` instead of a literal subnet ID       |
| Dependency mapping    | Terraform infers create/update/delete order from references, ensuring resources are provisioned in the correct sequence | A load balancer depends on backend instances referenced in its configuration |
| Unique identification | Each block has a resource type + local name (address) that other blocks use to reference it                             | `github_repository.production-repo` uniquely addresses that repo resource    |

<Frame>
  <img alt="The image explains resource referencing in HashiCorp Terraform, highlighting its benefits in creating dynamic configurations, automatic dependency mapping, and resource identification. It includes a diagram illustrating the flow between network configurations, firewalls, virtual machines, Kubernetes clusters, DNS records, and data lookup against cloud providers." />
</Frame>

Data sources

In addition to resources you create, Terraform can consume external data via `data` blocks. Data sources let you query existing infrastructure or provider metadata and then reference those results just like attributes from created resources.

Example use cases:

* Lookup an existing DNS forward lookup zone and use its `name` to create records.
* Query a cloud account to obtain a subnet or image ID that your resource needs.

Resource webs and dependency graphs

As configurations grow, they form a graph of interconnected blocks — `resource`, `data`, `output`, `variable`, and so on. Terraform uses these references to compute the dependency graph and to decide the correct apply/destroy ordering and what must be updated together.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Resource Referencing: The Reality of Terraform,&#x22; displaying interconnected nodes labeled as &#x22;Resource,&#x22; &#x22;Data,&#x22; &#x22;Output,&#x22; and &#x22;Variable.&#x22; It illustrates the dependencies and relationships between different elements in Terraform infrastructure, using arrows to indicate connections." />
</Frame>

HCL demo: writing Terraform files in VS Code

This demo shows practical HCL examples and recommended workflow items (like using `terraform fmt`). The focus is on writing, referencing, and formatting HCL rather than provider-specific behavior.

1. Create a file named `github.tf` in your working directory. VS Code with a Terraform extension will provide syntax highlighting and snippets for `provider` and `resource` blocks.

2. Add a provider block that references a token variable:

```hcl theme={null}
provider "github" {
  token = var.github_token
}
```

3. Define a repository resource. Each resource block is a combination of `type` and `local name` that forms the unique address used elsewhere in the configuration:

```hcl theme={null}
resource "github_repository" "production-repo" {
  name        = "prod-repo"
  description = "Repo for our production app"
  private     = true
}
```

4. Add another repository using a different local name so both resources have unique addresses:

```hcl theme={null}
resource "github_repository" "testing-repo" {
  name        = "test-repo"
  description = "Repo for our testing app"
  private     = true
}
```

<Callout icon="lightbulb">
  Every resource instance in a Terraform configuration must have a unique address: the combination of its type and its local name (for example, `github_repository.production-repo`). Reusing the same local name for two instances of the same resource type will produce a configuration error.
</Callout>

<Callout icon="warning">
  Do not hard-code sensitive values (like provider tokens) directly in `.tf` files. Use input variables, `terraform.tfvars`, or environment variables (for example, `TF_VAR_github_token`) and store secrets in a secure secrets manager or CI/CD secret store.
</Callout>

Using `terraform fmt` to format HCL

Keep code readable and consistent with `terraform fmt`. It normalizes indentation and aligns assignment operators to Terraform's canonical style.

Examples:

* Run the formatter across the working directory:

```bash theme={null}
$ terraform fmt
github.tf
test.tf
```

* If only one file required formatting, the output might be:

```bash theme={null}
$ terraform fmt
github.tf
```

Splitting resources across files

Terraform treats all `.tf` files in a directory as a single configuration. Use multiple files to organize resources logically — e.g., separate providers, networking, compute, and test resources.

Example file split:

test.tf:

```hcl theme={null}
resource "github_repository" "testing-repo" {
  name        = "test-repo"
  description = "Repo for our testing app"
  private     = true
}
```

github.tf:

```hcl theme={null}
provider "github" {
  token = var.github_token
}

resource "github_repository" "production-repo" {
  name        = "prod-repo"
  description = "Repo for our production app"
  private     = true
}
```

Running `terraform fmt` in the directory will scan and format all `.tf` files and report each file it modified.

Quick best practices

| Area         | Recommendation                                                                                |
| ------------ | --------------------------------------------------------------------------------------------- |
| Referencing  | Prefer using attributes from created `resource` or `data` blocks instead of hard-coded values |
| Secrets      | Use variables and secure secret stores — avoid committing tokens to VCS                       |
| Formatting   | Run `terraform fmt` regularly or enable automatic formatting in your editor                   |
| Organization | Group related resources into separate `.tf` files or modules for maintainability              |

Wrap-up

* Resource referencing enables dynamic, maintainable Terraform configurations by passing values between blocks rather than hard-coding.
* Terraform uses references to build a dependency graph and determine the correct provisioning order.
* Maintain consistent style with `terraform fmt`, split files for clarity, and keep secrets out of source files.

Links and references

* [Terraform Documentation](https://www.terraform.io/docs)
* [Terraform CLI — terraform fmt](https://www.terraform.io/cli/commands/fmt)
* [Terraform GitHub Provider](https://registry.terraform.io/providers/hashicorp/github/latest)
* [HCL Language Documentation](https://github.com/hashicorp/hcl)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/913661a6-d796-4eac-ad5d-1586b2b474ef" />
</CardGroup>


# Section Introduction Terraform Foundations

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Section-Introduction-Terraform-Foundations/page

Introductory guide to Terraform fundamentals, why teams use it, core concepts, common commands, workflows, state management, modules, and hands-on exam preparation

Welcome to the Terraform Foundations section.

Now that you've reviewed the [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004) exam objectives and installed Terraform and Visual Studio Code on your local machine, it's time to begin the hands-on material.

This lesson covers the core fundamentals of Terraform: what it is, why organizations adopt it, and how it improves infrastructure workflows compared with manually clicking through provider consoles or running ad-hoc CLI commands. You will learn the foundational concepts that explain how Terraform works and why it’s widely used for reproducible, automated infrastructure.

<Callout icon="lightbulb">
  This section focuses on the essential Terraform concepts you need early in your study path. If you're preparing for the HashiCorp Certified: Terraform Associate exam, these topics map closely to the exam's foundational objectives.
</Callout>

## What is Terraform?

Terraform is an open-source Infrastructure as Code (IaC) tool by HashiCorp that lets you define cloud and on-prem resources declaratively using configuration files (typically with the `.tf` extension). Terraform transforms those declarative files into an execution plan and then applies that plan to create, update, or destroy resources across multiple providers (AWS, Azure, GCP, and many others).

Key verbs you’ll use frequently:

* `terraform init` — initialize a working directory
* `terraform plan` — preview changes before applying
* `terraform apply` — execute the planned changes
* `terraform destroy` — remove managed infrastructure

## Why organizations use Terraform

Terraform introduces consistent, reproducible, and auditable infrastructure automation. Instead of manual clicks or scattered CLI scripts, Terraform gives you:

* Declarative configuration: describe desired state, not imperative steps.
* Multi-cloud and provider support: one tool for many platforms.
* Versionable configurations: treat infrastructure like code in git.
* Predictable change plans: preview changes with `terraform plan`.
* Reusable modules: encapsulate and share architecture patterns.

## Core Terraform concepts

| Concept       | Purpose                         | Example/Notes                                                 |
| ------------- | ------------------------------- | ------------------------------------------------------------- |
| Configuration | Declare resources and settings  | Files with `.tf` using HCL (HashiCorp Configuration Language) |
| Provider      | Plugin for a target platform    | `provider "aws" { region = "us-east-1" }`                     |
| Resource      | A managed infrastructure object | `resource "aws_instance" "web" { ... }`                       |
| State         | Maps config to real resources   | Stored locally or remotely (S3, Terraform Cloud)              |
| Plan/Apply    | Preview and enact changes       | `terraform plan` → `terraform apply`                          |
| Module        | Reusable configuration unit     | Local or registry-based modules for reuse                     |

<Callout icon="warning">
  Terraform state contains the authoritative mapping of resources. Protect and manage state carefully (use remote backends and locking for teams) to avoid resource drift and corruption.
</Callout>

## How Terraform improves workflows

* Automation and CI/CD: Integrate Terraform into pipelines to provision and update infrastructure automatically.
* Collaboration: Use remote state backends and workspaces to coordinate changes among teams.
* Drift detection: `terraform plan` surfaces differences between configuration and real infrastructure.
* Idempotence: Reapplying the same configuration converges the environment to the declared state.

## Common usage pattern

1. Write configuration (`*.tf` files).
2. Initialize the working directory:
   * `terraform init`
3. Validate and preview changes:
   * `terraform validate`
   * `terraform plan`
4. Apply changes:
   * `terraform apply`
5. Maintain and update through version control and CI.

## Next steps and references

* Official Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* HashiCorp Learn: [https://learn.hashicorp.com/terraform](https://learn.hashicorp.com/terraform)
* Course link (exam prep): [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004)

Suggested next hands-on exercises:

* Create a simple provider configuration and one resource.
* Initialize with `terraform init`, plan with `terraform plan`, and apply with `terraform apply`.
* Configure a remote backend (e.g., S3 with DynamoDB locking for AWS) to experiment with team workflows.

This section prepares you for deeper topics such as modules, state backends, remote operations, and workspace strategies that follow in the next lessons.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/25dc89b6-200b-4c5d-971a-2eb6d7c7abcc" />
</CardGroup>
