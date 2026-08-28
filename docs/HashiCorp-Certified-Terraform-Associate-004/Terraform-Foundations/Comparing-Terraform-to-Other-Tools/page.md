# Terraform
terraform.tfstate
terraform.tfstate.backup
.terraform/
.terraform.lock.hcl
*.tfvars
```

Working at scale: environments, projects, and modules

* Most organizations manage multiple environments (for example: `dev`, `staging`, `prod`) and several projects or components.
* Rather than a single monolithic working directory, create a top-level `terraform/` folder and separate environments and projects into subdirectories.

Common directory pattern:

* `repo/terraform/<project>/prod/` — contains `main.tf`, `variables.tf`, `outputs.tf`, and its own state.
* `repo/terraform/<project>/dev/` — separate working directory and state for development.
* Each subdirectory is an independent Terraform working directory with its own backend configuration and lifecycle.

Benefits:

* Reduced blast radius: operations in `dev` cannot accidentally modify `prod` because they use separate state files (local or remote).
* Clear boundaries make it easier to adopt reusable modules: extract repeated infrastructure into `modules/` and call them from environment working directories.

When using remote backends (recommended for collaboration), configure the backend per working directory to store state remotely (for example: S3 with DynamoDB for locking, or Terraform Cloud). Remote state helps with team collaboration, locking, and recovery.

<Frame>
  <img alt="The image illustrates a Git-based workflow for HashiCorp Terraform, showing push and pull actions with a repository leading to various environment directories, each containing Terraform files like main.tf, variables.tf, and outputs.tf." />
</Frame>

Wrapping up — best practices checklist

* Use multiple `.tf` files in a single working directory to organize by concern: variables, resources, outputs, and providers.
* Adopt conventional filenames (`main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`, `terraform.tfvars`) for consistency across teams.
* Keep each environment or project in its own working directory with separate state to minimize risks.
* Protect state files and lock files via `.gitignore` and prefer remote backends (S3, Azure Storage, Google Cloud Storage, or Terraform Cloud) for collaboration and state locking.
* Avoid committing secrets; use environment variables, secret managers, or secure backend integrations.

Further reading and references

* [Terraform Documentation — Configuration Language](https://www.terraform.io/docs/language/index.html)
* [Terraform Backend Configuration](https://www.terraform.[AWS_SECRET_ACCESS_KEY].html)
* [Best Practices for Terraform State](https://developer.hashicorp.com/terraform/tutorials/state/local-state)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/98cbbcea-8b12-451b-9c24-ab45c948c292/lesson/091341c0-56b9-4172-b563-d327f1263aef" />
</CardGroup>


# Comparing Terraform to Other Tools

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Foundations/Comparing-Terraform-to-Other-Tools/page

Explains Terraform versus cloud-native and config management tools, highlighting differences, use cases, and when to combine provisioning with in-VM configuration

This guide clears up common confusions about Terraform and how it compares to other tools in the infrastructure and configuration-management ecosystem. Understanding these differences helps you choose the right tool(s) for provisioning, management, and in-VM configuration—especially in single-cloud vs multi-cloud environments.

## IaC tools vs configuration-management tools (diagram overview)

On the left side of the diagram are tools that share Terraform’s core goal: provisioning and managing cloud infrastructure.

* CloudFormation and Bicep are cloud-native, declarative IaC systems tightly integrated with a single cloud provider (AWS and Azure respectively). They give deep provider-specific features and often get new provider functionality sooner.
* Pulumi is cloud-agnostic like Terraform but exposes general-purpose programming languages (TypeScript, Python, Go, etc.) to define infrastructure, which can appeal to developer-centric teams.
* Terraform is cloud-agnostic and focuses on declarative HCL to provide a consistent experience across many providers, making it a common choice for multi-cloud strategies.

Many organizations adopting multi-cloud prefer a cloud-agnostic IaC layer (Terraform or Pulumi) so teams don’t need to learn and maintain distinct native IaC solutions for each cloud.

<Frame>
  <img alt="The image is a comparison between Terraform and other tools, divided into &#x22;Infrastructure as Code Tools&#x22; (AWS CloudFormation, Azure Bicep, Pulumi) and &#x22;Configuration Management Tools&#x22; (Ansible, Chef, Puppet), highlighting their features and uses." />
</Frame>

On the right side of the diagram are tools that solve a different set of problems—usually complementary to Terraform.

* Ansible, Chef, Puppet, and SaltStack are configuration management systems focused on in-VM tasks: installing packages, templating and distributing configuration files, managing OS services, and enforcing runtime desired state.
* These tools typically run inside provisioned instances (or via agentless connections) and are best suited for application configuration, ongoing drift correction, and orchestration of software deployment.

## Typical pattern: combine provisioning with configuration

A common and recommended separation of concerns is:

* Provision infrastructure resources with Terraform (or another IaC tool): VMs, networking, load balancers, managed databases, and cloud-managed services.
* Configure software and runtime behavior inside those instances with configuration-management tools or boot-time mechanisms (Ansible, Chef, Puppet, SaltStack, `cloud-init`, baked images, or container orchestration).

This division keeps lifecycle management distinct from in-guest configuration and lets each tool do what it does best.

## Quick comparison table

| Category                                |                                                                                                                                                                                     Examples | Primary use                                                                   | Strengths                                                     |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Infrastructure as Code (cloud-specific) |                                                                                                  [CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation), Azure Bicep | Declarative provisioning within a single cloud                                | Deep provider integration, fast access to provider features   |
| Infrastructure as Code (cloud-agnostic) |                                                                                                              Terraform, [Pulumi](https://learn.kodekloud.com/user/courses/pulumi-essentials) | Multi-cloud provisioning and resource management                              | Portability across providers, consistent workflows            |
| Configuration management                | [Ansible](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course), [Chef](https://www.chef.io/), [Puppet](https://puppet.com/), [SaltStack](https://saltproject.io/) | Package installs, config files, service management, runtime state enforcement | In-VM orchestration, drift remediation, rich templating       |
| Bootstrapping / cloud-init              |                                                                                                                                                                                 `cloud-init` | Instance initialization and first-boot tasks                                  | Lightweight, runs at VM boot, commonly used for initial setup |

<Callout icon="lightbulb">
  Terraform is primarily for infrastructure provisioning. CloudFormation and Bicep are cloud-specific with deep provider integration. Configuration-management tools (Ansible, Chef, Puppet, SaltStack) handle in-VM software and runtime configuration. Pulumi is another cloud-agnostic IaC option that uses general-purpose programming languages and offers a different developer experience.
</Callout>

## How to choose

* Use cloud-native IaC (CloudFormation/Bicep) when you need the deepest, earliest access to provider-specific features and you operate mainly within one cloud.
* Use Terraform or Pulumi when you require consistent multi-cloud workflows and a provider-agnostic model.
* Use configuration management tools (or `cloud-init`) where you need agent-based/agentless in-VM configuration, application deployment, or ongoing state enforcement.
* In many environments, a combined approach yields the best balance: Terraform (or Pulumi) to provision cloud resources and a configuration system to install and manage software inside instances.

## Links and references

* [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
* [Pulumi Essentials](https://learn.kodekloud.com/user/courses/pulumi-essentials)
* [Learn Ansible Basics - Beginners Course](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)
* [Chef](https://www.chef.io/)
* [Puppet](https://puppet.com/)
* [SaltStack](https://saltproject.io/)
* `cloud-init` — [https://cloud-init.io/](https://cloud-init.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/be082b2a-db28-4bed-84e4-233393a3aafa/lesson/e350b625-1d02-40db-acfc-fb0eaeadde7a" />
</CardGroup>
