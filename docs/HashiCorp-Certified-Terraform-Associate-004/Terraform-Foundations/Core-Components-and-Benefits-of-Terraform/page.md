# Core Components and Benefits of Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Core-Components-and-Benefits-of-Terraform/page

Overview of Terraform core components and benefits, explaining core, providers, resources, state, and modules for building reusable, predictable infrastructure and team collaboration

In this lesson, we'll break down the fundamental components that make Terraform a reliable, infrastructure-as-code (IaC) tool. Understanding these building blocks — Terraform Core, Providers, Resources, State, and Modules — helps you design predictable, repeatable infrastructure and collaborate safely across teams.

* Terraform Core
* Providers
* Resources
* State
* Modules

## Terraform Core

Terraform Core is the CLI binary that reads and interprets your Terraform configuration files (`.tf`). When you run `terraform init`, `terraform plan`, or `terraform apply`, you are interacting with Terraform Core. Its responsibilities include:

* Parsing configuration files and building a dependency graph.
* Comparing your declared configuration against the current state.
* Determining a plan of changes and orchestrating provider API calls to create, update, or destroy resources.

Terraform Core is provider-agnostic: it defines the workflow and execution model while delegating resource-specific operations to providers.

## Providers

Providers are plugins that extend Terraform Core with the logic to manage resources on a particular platform (AWS, Azure, Google Cloud, GitHub, etc.). Providers implement the mappings between Terraform resource declarations and platform API calls.

A minimal provider block:

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}
```

Notes about providers:

* Version pin providers to ensure reproducible behavior.
* Providers may require credentials and specific configuration (environment variables, shared configs, or explicit blocks).
* Provider plugins are installed during `terraform init`.

## Resources

Resources are the primary declarations that describe the infrastructure objects Terraform will manage — compute instances, networks, databases, DNS records, and more. Each resource block contains arguments (inputs) and exposes attributes (outputs) that can be referenced elsewhere.

Example resource:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "example-web"
  }
}
```

Key resource concepts:

* Attributes such as IDs and computed values are stored in state and can be referenced using interpolation.
* Lifecycle meta-arguments (`create_before_destroy`, `prevent_destroy`) control how Terraform updates resources.
* Resource dependencies are inferred from references; explicit `depends_on` can enforce ordering when needed.

## State

Terraform state is the authoritative record of what Terraform manages in the real world. It maps resources in your configuration to real-world objects, stores metadata (IDs, attributes), and enables Terraform to compute incremental diffs.

State enables:

* Mapping real resources to configuration.
* Accurate planning and targeted updates.
* Sensitive metadata persistence (resource IDs, ARNs, endpoints).

Remote state and locking are critical for team workflows. Example S3 backend with DynamoDB locking:

```hcl theme={null}
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "project-name/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
  }
}
```

<Callout icon="lightbulb">
  Remote state backends enable team collaboration, state locking, and recovery. Use them for shared environments to avoid state conflicts and accidental overwrites.
</Callout>

<Callout icon="warning">
  Terraform state can contain sensitive information (secrets, IDs, endpoints). Use encrypted storage, restrict access, and avoid committing state files to source control.
</Callout>

## Modules

Modules are reusable, composable packages of Terraform configuration — the primary method to encapsulate and share common infrastructure patterns. Think of modules as functions or libraries for infrastructure.

Calling a module:

```hcl theme={null}
module "vpc" {
  source = "git::https://example.com/terraform-modules.git//vpc"
  cidr   = "10.0.0.0/16"
  region = "us-east-1"
}
```

Module best practices:

* Keep modules focused and opinionated.
* Expose inputs (`variables`) and outputs (`outputs`) for composability.
* Version and publish modules (Terraform Registry, Git tags) for stability.

<Frame>
  <img alt="The image is a diagram of Terraform's core components, including Terraform Core, Providers, Resources, State, and Modules, with brief descriptions of each." />
</Frame>

## Component Overview

* Terraform Core: Orchestrates the execution model and dependency graph.
* Providers: Implement API interactions for specific platforms.
* Resources: Declare the desired infrastructure objects.
* State: Records the current status and metadata of managed resources.
* Modules: Package reusable configuration patterns.

## Summary Table

| Component      | Role                                                          | Example                                                             |
| -------------- | ------------------------------------------------------------- | ------------------------------------------------------------------- |
| Terraform Core | Execution engine; builds dependency graph and applies changes | CLI commands: `terraform init`, `terraform plan`, `terraform apply` |
| Provider       | Translates resources to API calls for a platform              | `provider "aws" { region = "us-east-1" }`                           |
| Resource       | Declares infrastructure objects to manage                     | `resource "aws_instance" "web" { ... }`                             |
| State          | Persists mapping and metadata of managed resources            | `backend "s3" { ... }`                                              |
| Module         | Reusable configuration package                                | `module "vpc" { source = ".../vpc" }`                               |

## Next steps and further reading

* Try creating a small configuration that includes a provider, a resource, and remote state.
* Explore Modules to reduce duplication and enforce standards across projects.

## Links and References

* Terraform documentation: [https://developer.hashicorp.com/terraform/](https://developer.hashicorp.com/terraform/)
* S3 backend: [https://developer.hashicorp.[AWS_SECRET_ACCESS_KEY]/s3](https://developer.hashicorp.[AWS_SECRET_ACCESS_KEY]/s3)
* Terraform Registry: [https://registry.terraform.io/](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/d8ecb318-0b84-4541-91cc-fae07ce9b3ed" />
</CardGroup>
