# random_pet.additional_pet will be created
+ resource "random_pet" "additional_pet" {
    + id        = (known after apply)
    + length    = 3
    + separator = "-"
}

# random_pet.example must be replaced
-/+ resource "random_pet" "example" {
    ~ id     = "smashing-mutt" -> (known after apply)
    ~ length = 2 -> 3 # forces replacement
    # (1 unchanged attribute hidden)
}

# vault_generic_secret.example_kv will be updated in-place
~ resource "vault_generic_secret" "example_kv" {
    ~ data_json = (sensitive value)
      id        = "secret/example1"
    # (4 unchanged attributes hidden)
}

# vault_generic_secret.example_secret will be destroyed
# (because vault_generic_secret.example_secret is not in configuration)
- resource "vault_generic_secret" "example_secret" {
    - data                  = (sensitive value) -> null
    - data_json             = (sensitive value) -> null
    - delete_all_versions   = false -> null
    - disable_read          = false -> null
    - id                    = "secret/example" -> null
    - path                  = "secret/example" -> null
}

Plan: 2 to add, 1 to change, 2 to destroy.
```

Legend: what the resource action symbols mean

| Symbol | Meaning                             | Notes                                                                                     |
| ------ | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `+`    | Create                              | Attributes that are not known until apply are shown as `(known after apply)`              |
| `~`    | Update in-place                     | The provider supports changing the resource without destroying it                         |
| `-`    | Destroy                             | Resource will be removed because it is no longer in configuration                         |
| `-/+`  | Destroy and then create replacement | Change cannot be done in-place; the plan will show which attribute `# forces replacement` |

In the example above:

* `random_pet.additional_pet` is marked `+` (a new resource).
* `random_pet.example` is marked `-/+` because changing `length` from `2` to `3` forces replacement; Terraform annotates the attribute with `# forces replacement`.
* `vault_generic_secret.example_kv` is updated in-place; sensitive values are shown as `(sensitive value)` to avoid leaking secrets.
* `vault_generic_secret.example_secret` is scheduled for destruction since it was removed from the configuration; its attributes are shown as being removed (set to `null`).

<Frame>
  <img alt="The image is an informational graphic about &#x22;terraform plan,&#x22; explaining its function to generate an execution plan for resource changes and highlighting its importance for conducting dry-runs to prevent unintended changes." />
</Frame>

Provider refresh details

* By default, `terraform plan` refreshes state from providers to ensure the plan reflects the current world. This makes the plan accurate for most use cases.
* If you need to avoid provider queries (for example, to reduce API calls during ad-hoc checks), you can pass `-refresh=false`, but this may cause the plan to be based on stale information.

> **warning** Using `-refresh=false` can produce misleading plans because Terraform will not reconcile state with the provider. Use it cautiously and avoid it in production workflows where accuracy matters.

Saving plans and reproducible execution
Saving a plan to a file is useful for reviews, approvals, and CI/CD workflows. A saved plan captures the exact actions Terraform will take; applying the saved plan later executes those actions without recalculating them.

Quick commands

| Command                      | Purpose                               | Example                             |
| ---------------------------- | ------------------------------------- | ----------------------------------- |
| `terraform plan`             | Preview changes                       | `terraform plan`                    |
| `terraform plan -out=<file>` | Save a plan to a file for later apply | `terraform plan -out=myplan.tfplan` |
| `terraform apply <file>`     | Apply a saved plan file (no re-plan)  | `terraform apply myplan.tfplan`     |

Example workflow

```bash theme={null}
$ terraform plan -out=myplan.tfplan
<plan output>
<plan file created>

$ terraform apply myplan.tfplan
```

When you run `terraform apply myplan.tfplan`, Terraform skips the planning phase and executes the saved plan exactly as recorded. This ensures determinism and is ideal for audit trails and automated approvals.

Summary and best practices

* Treat `terraform plan` as a dry-run: it refreshes state, calculates the delta, and displays actions with clear symbols.
* Always review the plan before applying, especially in production environments.
* Use `terraform plan -out=FILE` to produce a saved, deterministic plan that can be reviewed and applied later.
* Be mindful of sensitive values: Terraform hides them in plan output.
* Pay attention to `-/+` replacement annotations so you understand when resources will be destroyed and recreated.

Links and references

* [Terraform CLI docs](https://www.terraform.io/cli)
* [Terraform State](https://www.terraform.io/language/state)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/7f9b99d1-8db6-4e09-b1e9-10e21e56ac7c)


# Terraform Validate

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Terraform-Validate/page

Explains terraform validate, an offline local syntax and schema check for Terraform configurations that requires terraform init and does not call provider APIs.

In this lesson we cover `terraform validate` — the Terraform CLI command that performs a local, offline check of your configuration files to catch syntax and structural errors before you run slower, provider-interacting commands.

What `terraform validate` does

* Checks HCL syntax across your configuration files.
* Validates structural correctness of blocks (resources, modules, providers).
* Verifies required arguments and attribute types against provider schemas (when initialized).
* Confirms referenced variables and outputs are declared.

What `terraform validate` does NOT do

* Make API calls to cloud providers or external services.
* Confirm provider-side resources exist (for example, whether an AMI ID is valid).
* Check cloud permissions or runtime environment constraints.
* Guarantee an apply will succeed.

> **lightbulb** `terraform validate` performs an offline schema-aware validation of your configs. It relies on provider schemas downloaded during `terraform init`, but it does not make any provider API calls, so provider-side problems (missing AMIs, permissions, quotas) will not be detected here.

Example resource snippet (what `terraform validate` inspects for syntax and attribute correctness):

```hcl theme={null}
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name = "example"
  }
}
```

Because validation is offline, it will not detect provider-level issues such as:

* Whether the referenced AMI actually exists.
* Whether you have permissions to create the resource.
* Whether the resource already exists in the provider.

Those problems are detected later by `terraform plan` and `terraform apply`, which interact with provider APIs.

> **warning** You must run `terraform init` before `terraform validate`. Initialization downloads provider plugins and schemas that `validate` uses. Running `validate` without first initializing the working directory will fail and prompt you to run `terraform init`.

Where `terraform validate` fits in a typical Terraform workflow

| Step       | Command              | Purpose                                                                       |
| ---------- | -------------------- | ----------------------------------------------------------------------------- |
| Initialize | `terraform init`     | Download providers, modules, and schema required for validation and planning. |
| Validate   | `terraform validate` | Fast, local syntax and schema check.                                          |
| Plan       | `terraform plan`     | Evaluate changes against provider state; makes API calls.                     |
| Apply      | `terraform apply`    | Apply changes to your infrastructure.                                         |
| Destroy    | `terraform destroy`  | Remove infrastructure created by Terraform.                                   |

Example command sequence

```bash theme={null}
terraform init
terraform validate
terraform plan
terraform apply
terraform destroy
```

Best practices and tips

* Use `terraform validate` as a quick pre-commit or CI check to catch syntax/regression issues before running expensive plans.
* Combine `terraform validate` with `terraform fmt -check` in CI to ensure consistent formatting and valid syntax.
* Remember that `validate` is not a substitute for `terraform plan` — always review the plan before applying.

Exam tip

* For the Terraform Associate exam and practical use, remember: `terraform validate` is an offline syntax/structure check and requires `terraform init` to have been run in the working directory.

Links and references

* [Terraform CLI Docs — validate](https://www.terraform.io/cli/commands/validate)
* [Terraform Init](https://www.terraform.io/cli/commands/init)
* [Terraform Plan](https://www.terraform.io/cli/commands/plan)
* [HashiCorp Certified: Terraform Associate](https://learn.hashicorp.com/collections/terraform/terraform-associate)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/84faaf55-4299-4f18-a2ff-77a55feb1b90)
