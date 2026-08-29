# VM-level configurations
vsphere_network = "10.0.5.0/24"
vm_image        = "image-x3f83j2sv3"

# Application configurations
enable_logging  = true

# Cloud account configurations
subscription_id = "abcd-1234-cc"
```

Tips for `.tfvars`:

* Group variables by intent (network, VM, app, cloud account) and add comments for clarity.
* Use environment-specific files (`dev.tfvars`, `staging.tfvars`, `prod.tfvars`) and pass the one you need at runtime.
* Exclude `.tfvars` files from version control if they contain secrets (use `.gitignore`), or store non-secret environment defaults in the repo.
* Use `terraform.tfvars` or `*.auto.tfvars` for values you want Terraform to pick up automatically in the current working directory.

Explicitly using a `.tfvars` file:

```bash theme={null}
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"
```

## 4) Command-line flags (-var / -var-file)

Command-line flags provide the highest-priority overrides and are ideal for ephemeral changes, testing, or CI steps that must force a specific value.

<Frame>
  <img alt="The image is a slide titled &#x22;Command Line Flags,&#x22; explaining how to pass variable values directly from the command line using -var=&#x22;key=value&#x22;. It features branding for HashiCorp Terraform." />
</Frame>

Examples:

```bash theme={null}
terraform plan -var="enable_logging=true"
terraform apply -var="region=us-west-2" -var="vm_image=image-x3f83j2sv3"
```

Notes:

* CLI `-var` overrides `.tfvars`, environment variables, and defaults.
* Use `-var-file` on the command line to provide a tfvars file that differs from the auto-loaded files.
* Avoid using `-var` for routine production config because command-line flags are not persisted in files and can be harder to audit.

## Precedence: which source wins?

Terraform resolves variables using a strict order of precedence. When a variable is set in multiple places, the highest-priority source takes effect.

Precedence from highest to lowest:

1. Command-line flags (`-var` and `-var-file` specified on the CLI)
2. Environment variables (`TF_VAR_` prefixed)
3. Terraform variable files (auto-loaded `terraform.tfvars`, `*.auto.tfvars`, and other `*.tfvars` when passed)
4. Variable block `default` values

<Frame>
  <img alt="The image explains the order of precedence in Terraform for resolving variable values, with a hierarchy from command line flags to variable block defaults. It highlights flexibility for values, clear override rules, and adaptability across environments." />
</Frame>

Practical examples:

* If a variable has a `default` and you set it in `dev.tfvars`, the `dev.tfvars` value wins over the `default`.
* If you then set the same variable using `TF_VAR_VARNAME`, the environment variable overrides `dev.tfvars`.
* Finally, providing `-var="VAR=value"` on the CLI will override the environment variable and all other sources.

### Quick reference table for precedence

| Priority    | Source                | How to apply                                                      |
| ----------- | --------------------- | ----------------------------------------------------------------- |
| 1 (highest) | Command-line flags    | `terraform apply -var="key=value"` or `-var-file="file.tfvars"`   |
| 2           | Environment variables | `export TF_VAR_key="value"` or pipeline secrets                   |
| 3           | `.tfvars` files       | `terraform.tfvars`, `*.auto.tfvars`, or `-var-file="file.tfvars"` |
| 4 (lowest)  | `variable` defaults   | `variable "key" { default = "value" }`                            |

## Summary and best practices

* Defaults: Use for safe, non-sensitive baselines and documentation.
* Environment variables: Use for secrets and CI/CD-injected values.
* `.tfvars` files: Use to group environment-specific settings; avoid committing secrets unless stripped.
* Command-line flags: Use for ad-hoc overrides and testing; remember these are highest precedence.
* Always follow the precedence rules above to avoid unexpected overrides during runs.

References and further reading:

* Terraform CLI docs: [https://www.terraform.io/docs/cli](https://www.terraform.io/docs/cli)
* Variable configuration: [https://www.terraform.io/docs/language/values/variables.html](https://www.terraform.io/docs/language/values/variables.html)

Understanding these variable assignment methods and their precedence ensures predictable Terraform behavior and helps you design secure, maintainable infrastructure configurations.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/33831f76-25e8-43e2-97e6-55e37b463fe9)


# Connecting to Cloud Platforms with Provider Blocks

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/Connecting-to-Cloud-Platforms-with-Provider-Blocks/page

Explains Terraform provider blocks, their configuration, authentication, version pinning, initialization, and best practices for securely connecting Terraform to cloud platforms and services

Welcome to this lesson on the provider block in Terraform.

Provider blocks are the bridge between Terraform Core and the APIs of the platforms you manage. Terraform Core handles state, planning, and graphing, but it relies on providers — separate plugins — to perform platform-specific API calls and authentication.

Terraform Core reads your configuration, constructs the resource graph, and creates execution plans. Providers implement the platform logic and authentication so Terraform can create, update, and delete resources on your behalf.

<Frame>
  <img alt="The image illustrates Terraform providers, including various cloud platforms and other services, connected to Terraform. Examples include AWS, Azure, Kubernetes, Google Cloud, Infoblox, and GitHub." />
</Frame>

In a typical architecture diagram, cloud platforms (AWS, Azure, Google Cloud, Kubernetes, etc.) appear on one side while other services (GitHub, DNS providers, monitoring systems) appear on the other. Providers encapsulate all platform-specific behavior so Terraform Core can remain focused on orchestration.

<Frame>
  <img alt="The image illustrates Terraform providers, showing its core connected to various cloud platforms (such as Kubernetes, AWS, Azure, Google Cloud) and other services (like Infoblox and GitHub)." />
</Frame>

Because providers are independent plugins, Terraform stays modular: provider authors maintain platform APIs and Terraform Core manages lifecycle and orchestration.

## What a provider block does

A provider block (written in HCL like the rest of your Terraform) specifies how Terraform authenticates to and communicates with a platform. Typical configuration options include:

* Endpoints and regions
* Authentication credentials or identity sources
* API version or feature toggles
* Provider-specific behavior and defaults

Where to put provider blocks: Many teams use a `providers.tf` file for clarity, but Terraform reads any `*.tf` file in the working directory. File placement is a convention, not a requirement.

## Provider block structure and examples

* The syntax is `provider "<name>" { ... }`. The provider label must match the provider name registered in the Terraform Registry (for example: `aws`, `azurerm`, `github`).
* Each provider exposes its own arguments — consult the provider’s Registry page for exact options.

Example: AWS provider (using a named profile)

```hcl theme={null}
provider "aws" {
  region  = "us-east-2"
  profile = "prd-workload"
}
```

Example: Azure Resource Manager provider (the Azure provider requires an empty `features {}` block; authentication fields shown as placeholders)

```hcl theme={null}
provider "azurerm" {
  features {}

  tenant_id       = "tenant-id"
  subscription_id = "sub-id"
  client_id       = "client-id"
  client_secret   = "client-secret"
}
```

These examples show explicit credentials only for clarity. In production, avoid embedding secrets in Terraform files — use environment variables, shared credential files, IAM roles/instance profiles, managed identities, Vault, or other secret stores.

> **lightbulb** Use secure secret management and the principle of least privilege. Avoid storing credentials or secrets directly in `.tf` files or version control.

## Pinning provider versions (recommended)

Providers evolve independently from Terraform Core. To ensure consistent, reproducible deployments and to avoid unexpected breaking changes, pin provider versions with the `required_providers` block inside `terraform {}`.

Example: pinning AWS and Azure providers

```hcl theme={null}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

## Authentication methods by provider

Different providers support different authentication mechanisms. The table below summarizes common approaches and recommended best practices.

| Provider           | Common authentication methods                                           | Best practice                                                                        |
| ------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| AWS                | access key/secret, shared credentials file, instance profile / IAM role | Prefer IAM roles (instance profiles) or environment credentials; use least privilege |
| Azure              | service principal (client\_id/client\_secret), managed identity         | Use managed identity where possible; rotate service principals regularly             |
| Google Cloud (GCP) | service account keys, workload identity                                 | Use workload identity or short-lived tokens instead of long-lived keys               |
| GitHub             | personal access tokens (PAT), OAuth apps                                | Use fine-scoped tokens and rotate regularly                                          |

Treat provider credentials as highly sensitive: store them in secret stores, rotate them, and grant only the permissions Terraform requires.

> **warning** Never commit credentials, client secrets, or service account keys into version control. Doing so risks accidental exposure.

## Provider lifecycle and initialization

When you run `terraform init`, Terraform performs the following provider-related steps:

* Reads provider requirements from your configuration (`required_providers`).
* Checks local cache for provider binaries; if missing, downloads required provider plugins from the Terraform Registry (`https://registry.terraform.io`).
* Verifies downloads using cryptographic checksums and installs plugins locally.
* Initializes providers with the configuration you provided.

This ensures team members use the same provider versions and that providers are securely downloaded and verified.

## Using multiple provider configurations

A single provider configuration can manage many resource types for that platform (for example, one `aws` provider can manage compute, storage, networking, and databases). You only need one provider block per account/region/scope.

If you must target multiple accounts, regions, or scopes, create multiple provider configurations and use `alias` to reference them in resources. Example flow:

* Define the default provider for the main account.
* Define an aliased provider for the secondary account or other region.
* Reference the aliased provider from resources with `provider = aws.secondary`.

## Where to find providers and documentation

Primary sources:

* Terraform Registry: [https://registry.terraform.io](https://registry.terraform.io) — provider pages include resource types, arguments, data sources, authentication examples, and change logs.
* Provider GitHub repositories — useful for release notes, issues, and deep dives.
* Official cloud provider docs for platform-specific details.

Useful links and references:

* [Terraform Registry](https://registry.terraform.io)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [AWS Identity and Access Management](https://docs.aws.amazon.com/iam/latest/UserGuide/)

## Summary

* Provider blocks configure how Terraform talks to platform APIs (regions, endpoints, credentials, features).
* Providers are independent plugins — pin versions with `required_providers` to keep deployments stable.
* Never store secrets in `.tf` files; use secret management and least privilege.
* Run `terraform init` to download and initialize providers; Terraform verifies provider binaries automatically.
* Consult the Terraform Registry for provider documentation, examples, and versioning information.

This concludes the deep dive into provider blocks. A hands-on lab is recommended to practice writing provider blocks and creating resources using those providers. In the next sections we'll build on this foundation and create actual resources with these providers.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/91a8fdbc-765e-4003-abb5-13ff438f6f74)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/66544cee-f367-4cc5-9cb3-a816a71550b7)
