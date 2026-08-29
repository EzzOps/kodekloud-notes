# Why Secrets in Terraform Are Risky

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Why-Secrets-in-Terraform-Are-Risky/page

Explains risks of storing secrets in Terraform, where secrets leak, and practical controls to protect state, logs, version control, and plan artifacts.

Welcome back.

We're starting a focused and highly practical section: securing your Terraform configurations and handling secrets safely during development and deployment. This topic appears repeatedly in production environments and in certification material like the [Terraform Associate Certification: HashiCorp Certified](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified). Mismanaging secrets can cause real security incidents—exposed credentials, compromised services, or worse.

In this article we'll explain why storing secrets in Terraform is tricky, where those secrets typically surface, and what controls you should apply to protect them.

## The common mistake

A common pattern: you create a resource that needs a password (for example, a database), so you put that password into a Terraform variable and continue. It seems convenient, but that value will often appear in multiple places across your Terraform workflow—and frequently as plain text. Treating Terraform variables like a secret vault is a mistake.

## Terraform state and why secrets appear

Terraform persists a complete representation of the infrastructure it manages. "Complete" includes resource attributes that are necessary for lifecycle operations and drift detection—sensitive values such as passwords, API keys, and connection strings included.

By default Terraform state is serialized as JSON (plain text). If you use a shared backend (remote state), anyone with access to the backend can potentially read those secrets. CI/CD systems can also capture Terraform output or provider error messages in logs, which may expose sensitive values.

Warning: Terraform stores secrets in state by design to perform its management tasks. The correct approach is to protect state and other exposure points, not to expect Terraform to avoid storing needed attributes.

## Example state snippet

Below is a representative excerpt from a local Terraform state file showing how a database password can appear in multiple places:

```json theme={null}
{
  "version": 4,
  "terraform_version": "...",
  "serial": "...",
  "lineage": "...",
  "outputs": {
    "database_password_output": {
      "value": "MySuperSecretPassword123!",
      "type": "string",
      "sensitive": true
    }
  },
  "resources": [
    {
      "mode": "managed",
      "type": "aws_db_instance",
      "name": "main",
      "provider": "...",
      "instances": [
        {
          "schema_version": "...",
          "attributes": {
            "password": "MySuperSecretPassword123!",
            "other_attributes": "..."
          }
        }
      ]
    }
  ]
}
```

## Where secrets can end up

Secrets in a Terraform workflow commonly surface in four places. The table below summarizes each exposure point and why it is risky:

| Exposure point        |                                                                      Why it's risky | Typical examples                                  |
| --------------------- | ----------------------------------------------------------------------------------: | ------------------------------------------------- |
| State files           |                  State contains full resource attributes in JSON, including secrets | `terraform.tfstate`, remote backend state         |
| Logs & console output | `terraform plan`, `terraform apply`, provider errors, and CI logs can reveal values | Terminal output, CI job logs                      |
| Version control       |            Committed `.tfvars` or hard-coded credentials become part of Git history | `terraform.tfvars`, inline secrets in `.tf` files |
| Plan artifacts        |          Saved `terraform plan` files and similar artifacts include proposed values | CI artifacts, stored plans                        |

<Frame>
  <img alt="The image is an infographic titled &#x22;Where Sensitive Data Can End Up,&#x22; highlighting four areas: state files, logs & console, version control, and plan files, with specific examples under each category." />
</Frame>

## Multiple exposure points require layered protections

Because secrets may appear in state, logs, version control, and artifact storage, apply defenses in depth:

* Protect state
  * Use secure remote backends that support encryption at rest and strong access controls.
  * Enable backend locking where available to prevent concurrent writes.
  * Limit who and what (CI jobs, agents) can access the state backend.
* Avoid leaking secrets in logs and CI
  * Use `sensitive = true` for variables and outputs to reduce accidental CLI exposure (note: this does not prevent secrets from being stored in state).
  * Sanitize provider outputs and minimize verbose logging in CI.
  * Treat CI logs as sensitive artifacts and rotate tokens/keys used in CI.
* Keep secrets out of version control
  * Never commit `terraform.tfvars` with real secrets or hard-code credentials in `.tf` files.
  * Use pre-commit hooks and secret-scanning tools to detect accidental commits.
* Manage plan artifacts carefully
  * Avoid storing plans with sensitive values in long-lived or public artifact repositories.
  * If you must store artifacts, ensure they are encrypted and access is restricted.

## What this section will cover

In the upcoming lessons we will present specific, practical techniques to reduce the exposure of secrets across Terraform workflows:

* Using sensitive variables and environment variables to prevent casual CLI exposure and to reduce the chance of committing credentials. Keep in mind that marking a variable as `sensitive` will not stop Terraform from persisting its value in state if the provider requires it.
* Encrypting and protecting state backends, enforcing least privilege, and configuring backend access controls.
* Leveraging provider-specific features that can avoid writing secrets into state when providers offer them (for example, providers that return ephemeral credentials or avoid storing generated secrets).
* Integrating external secrets managers (for example, learn more in the [Vault Associate Certification course](https://learn.kodekloud.com/user/courses/labs-hashicorp-certified-vault-associate-certification)) so sensitive values are retrieved dynamically and not committed to Terraform state. We'll also cover workflow design to avoid persisting fetched secrets in state if that’s not acceptable for your security posture.

By the end of this section you'll understand how to secure secrets across your Terraform workflow—knowledge that’s useful in real-world environments and relevant for the [Terraform Associate Certification: HashiCorp Certified](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified).

> **lightbulb** Understand where secrets will appear in your workflow first; then apply protections to each layer (state, logs, VCS, and artifacts).

Let's proceed to the solutions and protections in the next lessons.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/0420bd59-917f-4dde-85a9-40a8261efe0b)
