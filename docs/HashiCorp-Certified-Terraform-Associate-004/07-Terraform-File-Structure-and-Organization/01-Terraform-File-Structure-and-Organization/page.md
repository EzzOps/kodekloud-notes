# Terraform File Structure and Organization

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-File-Structure-and-Organization/Terraform-File-Structure-and-Organization/page

Organizing Terraform files, state, environments, and best practices for collaboration, secrets management, and reusable modules.

Hey everyone — welcome back.

This lesson explains how to structure Terraform configurations for clarity, reuse, and safe collaboration. Whether you work with a single `.tf` file or a multi-directory layout for multiple environments, organizing files consistently will make day-to-day operations and long-term maintenance much easier. Below we walk through Terraform block types, recommended filenames, state handling, environment separation patterns, and best practices for secrets and version control.

When authoring Terraform, you declare different block types inside `.tf` files to describe the infrastructure you want to deploy. Application or infrastructure teams state requirements (for example: an S3 bucket, a VM, or a Kubernetes cluster), and Terraform converts those requirements into configuration blocks.

Common Terraform block types:

* `variable` — declare inputs to the configuration.
* `resource` — describe real-world infrastructure objects to create and manage.
* `output` — expose values after deployment (for use by people, other configurations, or orchestration).
* `provider` — configure the provider plugins (e.g., AWS, GCP, Azure, Kubernetes).

Terraform loads any file with the `.tf` extension in the working directory when you run `terraform plan`, `terraform apply`, or other commands, and it merges them into a single configuration at runtime.

<Frame>
  <img alt="The image is a diagram showing infrastructure requirements and their corresponding configuration in a Terraform configuration file. It includes elements like an S3 bucket, virtual machine, and Kubernetes cluster mapped to various Terraform constructs such as variables and resources." />
</Frame>

Why split files?

* A single large `.tf` file becomes brittle and hard to review.
* Logical separation improves readability, team ownership, and reuse.
* Terraform treats all `.tf` files in the directory as one configuration, so cross-file references (for example, referencing a resource defined in another file) work automatically.

A typical strategy is to group related blocks in separate files by concern:

* `variables.tf` — input variable declarations
* `network.tf` — network-related resources (VPCs, subnets, firewalls)
* `kubernetes.tf` — Kubernetes resources or provider configuration for clusters
* `outputs.tf` — outputs to expose information after apply

Because Terraform merges files in the working directory, you don't need special imports or wiring to reference a resource defined in a different file.

<Frame>
  <img alt="The image illustrates how Terraform processes files in a working directory, detailing a sequence involving variables, resources, and outputs." />
</Frame>

Recommended, practical file layout

* Using conventional filenames increases predictability across teams.
* Below is a concise reference you can adopt as a starting point.

| File               | Purpose                                                      | Example / Notes                                                                           |
| ------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `main.tf`          | Primary configuration: networks, clusters, compute resources | Put core `resource` and `module` blocks here                                              |
| `variables.tf`     | Declare input variables                                      | Use `variable "env" {}` declarations                                                      |
| `outputs.tf`       | Expose outputs after apply                                   | Use `output "bucket_name" {}` blocks                                                      |
| `providers.tf`     | Provider configuration and provider blocks                   | Examples: `provider "aws" { region = "us-east-1" }`                                       |
| `terraform.tfvars` | Assign values to variables (auto-loaded)                     | Use for non-sensitive environment defaults; Terraform loads this automatically if present |

Notes on using `terraform.tfvars` and per-environment tfvars:

* You can create environment-specific files like `prod.tfvars` and pass them with `-var-file=prod.tfvars`.
* Do not store secrets in plaintext in `.tfvars` files that are committed to version control.

<Frame>
  <img alt="The image lists common Terraform files with their purposes: main.tf for infrastructure components, variables.tf for variable definitions, outputs.tf for output blocks, providers.tf for provider configurations, and terraform.tfvars for variable values." />
</Frame>

Terraform runtime and state files
Terraform also creates and updates several files to track its operations. These are not part of your source configuration and generally should not be manually edited:

* `terraform.tfstate` — the current state file recording managed infrastructure.
* `terraform.tfstate.backup` — prior state backup created before updates.
* `.terraform.lock.hcl` — dependency lock file for provider versions.
* `.terraform/` — directory storing downloaded provider plugins and modules.

Because state often contains resource IDs, IP addresses, and sometimes sensitive attributes, treat state as sensitive data.

<Frame>
  <img alt="The image describes two Terraform files: terraform.tfstate, which stores the state, and terraform.tfstate.backup, which is a backup of the previous state file. It also shows a directory listing with various Terraform-related files." />
</Frame>

<Callout icon="lightbulb">
  Always add `terraform.tfstate`, `terraform.tfstate.backup`, `.terraform/`, and `.terraform.lock.hcl` to your repository's `.gitignore`. This prevents accidentally committing sensitive or environment-specific data into version control.
</Callout>

<Callout icon="warning">
  Do not store secrets (API keys, passwords, private keys) in plaintext inside `.tfvars` or Terraform files. Use environment variables, a secret manager (e.g., AWS Secrets Manager, HashiCorp Vault), or remote backends with proper access controls instead.
</Callout>

Example .gitignore snippet

```text theme={null}
