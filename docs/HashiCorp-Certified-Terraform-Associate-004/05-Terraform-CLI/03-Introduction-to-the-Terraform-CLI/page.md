# problematic output
output "random_pet_name" {
  value = random_pet.id
}
```

Validation error message:

```bash theme={null}
$ terraform validate
Error: Reference to undeclared resource

  on main.tf line 8, in output "random_pet_name":
  value = random_pet.id

A managed resource "random_pet" "id" has not been declared in the root module.
```

Fix by referencing the declared instance label:

```hcl theme={null}
output "random_pet_name" {
  value = random_pet.name.id
}
```

## 6) Create an execution plan

Use `terraform plan` to preview changes without applying them.

```bash theme={null}
$ terraform plan
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # random_pet.name will be created
  + resource "random_pet" "name" {
      + id        = (known after apply)
      + length    = 2
      + separator = "-"
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + random_pet_name = (known after apply)
```

Save a plan to a file with `-out` so you can apply exactly that plan later:

```bash theme={null}
$ terraform plan -out=bryan
Plan: 1 to add, 0 to change, 0 to destroy.

Saved the plan to: bryan
To perform exactly these actions, run the following command to apply:
  terraform apply "bryan"
```

## 7) Apply the configuration

`terraform apply` runs a planning step and then prompts to confirm the changes. Add `-auto-approve` to skip interactive confirmation (use carefully in automation).

Interactive apply:

```bash theme={null}
$ terraform apply
# Terraform will prompt "Do you want to perform these actions?" — type "yes" to proceed.
```

Non-interactive apply:

```bash theme={null}
$ terraform apply -auto-approve
```

Example apply output:

```plaintext theme={null}
random_pet.name: Creating...
random_pet.name: Creation complete after 0s [id=better-caribou]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:
random_pet_name = "better-caribou"
```

## 8) Update configuration: replacement vs. in-place update

Changing certain attributes may force a resource replacement depending on the provider and resource type. For example, changing `length`:

```hcl theme={null}
resource "random_pet" "name" {
  length = 3
}
```

`terraform plan` may show a replacement:

```plaintext theme={null}
Terraform will perform the following actions:

  # random_pet.name must be replaced
-/+ resource "random_pet" "name" {
    id     = "better-caribou" -> (known after apply)
    length = 2 -> 3 # forces replacement
    # (1 unchanged attribute hidden)
  }

Plan: 1 to add, 0 to change, 1 to destroy.

Changes to Outputs:
  ~ random_pet_name = "better-caribou" -> (known after apply)
```

Apply the replacement (example with auto-approve):

```bash theme={null}
$ terraform apply -auto-approve
```

Sample replacement output:

```plaintext theme={null}
random_pet.name: Destroying... [id=better-caribou]
random_pet.name: Destruction complete after 0s
random_pet.name: Creating...
random_pet.name: Creation complete after 0s [id=painfully-rich-mongrel]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.

Outputs:
random_pet_name = "painfully-rich-mongrel"
```

Note: whether an attribute change forces replacement depends on the provider and resource.

## 9) Inspect the state

Terraform stores a state file (by default `terraform.tfstate`) that records managed resources and outputs.

Example state fragment:

```json theme={null}
{
  "version": 4,
  "terraform_version": "1.10.5",
  "serial": 5,
  "lineage": "8072588f-d48c-1b42-13df2b07cae7",
  "outputs": {
    "random_pet_name": {
      "value": "painfully-rich-mongrel",
      "type": "string"
    }
  }
}
```

List resources tracked in state:

```bash theme={null}
$ terraform state list
random_pet.name
```

## 10) Manage multiple resources

Every resource instance requires a unique label:

```hcl theme={null}
resource "random_pet" "bryans_pet" {
  length = 3
}

resource "random_pet" "name" {
  length = 3
}
```

After `terraform apply`:

```bash theme={null}
$ terraform state list
random_pet.bryans_pet
random_pet.name
```

## 11) Destroy resources

`terraform destroy` plans and prompts to destroy all managed resources in the configuration.

Interactive:

```bash theme={null}
$ terraform destroy
# Terraform will prompt: "Do you really want to destroy all resources? ... Only 'yes' will be accepted to confirm."
```

Non-interactive:

```bash theme={null}
$ terraform destroy --auto-approve
```

Example destroy output:

```plaintext theme={null}
random_pet.name: Destroying... [id=heavily-happy-narwhal]
random_pet.name: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

Common typo to avoid: `terraform destory` (incorrect). Use `terraform destroy`.

<Callout icon="warning">
  Be careful with `-auto-approve` or `--auto-approve` flags on `apply` and `destroy`. They bypass interactive confirmation and can cause destructive changes if used accidentally.
</Callout>

## Quick reference — common Terraform CLI commands

| Command                        | Purpose                                           | Example / Notes                                           |
| ------------------------------ | ------------------------------------------------- | --------------------------------------------------------- |
| `terraform version`            | Show Terraform version                            | `terraform version`                                       |
| `terraform fmt`                | Format HCL files                                  | `terraform fmt`                                           |
| `terraform init`               | Initialize working directory & download providers | `terraform init`                                          |
| `terraform validate`           | Validate configuration syntax and semantics       | `terraform validate`                                      |
| `terraform plan`               | Preview changes                                   | `terraform plan`                                          |
| `terraform plan -out=FILENAME` | Save a plan to a file to apply later              | `terraform plan -out=bryan`                               |
| `terraform apply`              | Apply changes (prompts for confirmation)          | `terraform apply` or `terraform apply -auto-approve`      |
| `terraform state list`         | List resources tracked in state                   | `terraform state list`                                    |
| `terraform destroy`            | Destroy all managed resources                     | `terraform destroy` or `terraform destroy --auto-approve` |

## Summary

This lesson demonstrated a simple end-to-end Terraform workflow with the `random` provider: create a configuration, format and validate it, initialize providers, plan and apply changes, inspect state, and destroy resources. The same CLI workflow applies to cloud providers; expect provider-specific behavior and longer apply/destroy durations when interacting with remote APIs.

## Links and references

* [Terraform CLI documentation](https://www.terraform.io/docs/cli/index.html)
* [random provider — HashiCorp Registry](https://registry.terraform.io/providers/hashicorp/random/latest)
* [Visual Studio Code](https://code.visualstudio.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/35cbc795-57ed-4af7-88c8-c9323af9294d/lesson/0e35f910-b353-4b57-b16f-1afa236e6024" />
</CardGroup>


# Introduction to the Terraform CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-CLI/Introduction-to-the-Terraform-CLI/page

Overview of Terraform CLI command structure, workflow, common subcommands, environment variables, and best practices for managing infrastructure as code

The Terraform CLI is the primary interface for managing infrastructure as code with Terraform. It provides a consistent command structure across cloud providers and on-premises environments, so the same commands and workflow apply whether you're deploying to AWS, Azure, GCP, or elsewhere. This predictability helps teams collaborate and automate infrastructure reliably.

A typical command pattern is:

```bash theme={null}
terraform <command> [options]
```

Once you learn the CLI conventions, you can apply them across every Terraform project.

## Command structure and examples

Commands are invoked with the base keyword `terraform` followed by a subcommand and optional flags or parameters:

```bash theme={null}
terraform <subcommand> [options or flags]
```

Example:

```bash theme={null}
terraform plan -out=planfile
```

* `terraform` — invokes the Terraform CLI.
* `plan` — subcommand that generates an execution plan.
* `-out=planfile` — optional flag that saves the plan for later use with `apply`.

Use this structure to compose commands for initialization, validation, planning, applying, and destruction.

## Terraform workflow mapped to CLI commands

Terraform’s recommended workflow maps directly to CLI subcommands. Follow these steps to develop, test, and manage infrastructure safely.

| Step              | Purpose                                                                  | CLI Examples                                         |
| ----------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| Write             | Create infrastructure definitions in HCL (`.tf` files).                  | `# Edit .tf files`                                   |
| Format & Validate | Ensure readable, valid configuration.                                    | `terraform fmt`<br />`terraform validate`            |
| Init              | Initialize the working directory: download providers, configure backend. | `terraform init`                                     |
| Plan              | Preview proposed changes before applying.                                | `terraform plan`<br />`terraform plan -out=planfile` |
| Apply             | Provision or modify resources described in configuration.                | `terraform apply`<br />`terraform apply planfile`    |
| Destroy           | Tear down managed resources.                                             | `terraform destroy`                                  |

Canonical sequence of commands:

```bash theme={null}
terraform fmt
terraform init
terraform validate
terraform plan
terraform apply
