# Protecting Secrets in Your Configuration

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Protecting-Secrets-in-Your-Configuration/page

Strategies to prevent secret leakage in Terraform configurations using sensitive variables, environment injection, and external secret managers while securing state and access

Secrets can leak in many unexpected places: Terraform plan/apply output, CI logs, local files, and even your version control history. This guide walks through three complementary, pragmatic techniques to reduce exposure risk. Use them together across development and production environments.

We’ll cover:

* Sensitive variables — quick wins that hide values from CLI output and logs.
* Environment variables — keep secrets out of your repository and `.tfvars`.
* External secret stores — the recommended approach for production.

Start with the fastest improvements, then move toward more robust secret management.

## Why this matters

Terraform often stores resource attributes (including secrets) in the state. Even when values are redacted from CLI output, the state may still contain plaintext secrets. Treat your state like any other sensitive datastore: use remote backends with encryption and strict access control.

## Overview: techniques at a glance

| Technique                                                      | What it protects                                       | Typical use                               | Limitations                                                                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Sensitive variables                                            | Prevents values from appearing in CLI output and logs  | Development and quick wins in any project | Does not prevent values from being saved to state                                                                           |
| Environment variables (`TF_VAR_<name>` and provider creds)     | Keeps secrets out of `.tf` and `.tfvars` files and VCS | Local dev and CI with secret injection    | Secrets read by Terraform may still be written to state                                                                     |
| External secret stores (Vault, AWS Secrets Manager, Key Vault) | Centralized secrets, rotation, ACLs, audit logs        | Production and audited systems            | If Terraform reads secrets and writes plaintext into resources, state can still contain them; prefer secret references/ARNs |

## 1) Sensitive variables

Marking variables and outputs as `sensitive` tells Terraform to redact those values from CLI output and logs. This is the fastest, lowest-effort change that reduces accidental exposure.

Example variable definition (`variables.tf`):

```hcl theme={null}
variable "db_password" {
  description = "The database password"
  type        = string
  sensitive   = true
}
```

Using the variable in a resource (`main.tf`):

```hcl theme={null}
resource "aws_db_instance" "db" {
  identifier     = "my-db"
  instance_class = "db.t3.micro"
  engine         = "mysql"
  username       = "app_user"

  # Reference the sensitive variable normally
  password = var.db_password

  # ...other settings...
}
```

Output marked sensitive (`outputs.tf`):

```hcl theme={null}
output "db_password" {
  value     = var.db_password
  sensitive = true
}
```

<Callout icon="warning">
  Marking variables or outputs as `sensitive` hides them from CLI output and logs but does not remove values from the Terraform state. Always secure your state (use a remote backend with encryption and access controls).
</Callout>

## 2) Environment variables

Environment variables let you inject secrets without writing them into `.tf` or `.tfvars`, preventing accidental commits.

* Use the `TF_VAR_<name>` convention to set input variables from the environment.
* Provider credentials (for example `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `VAULT_TOKEN`) are commonly passed via environment variables and are supported by most providers.

Example (Linux/macOS):

```bash theme={null}
export TF_VAR_db_password="s3cr3t!"
terraform plan
terraform apply
```

Best practices for environment variables:

* Prefer CI/CD secret stores or OS-level secret managers to inject variables for automated runs.
* Avoid passing secrets via `terraform apply -var 'db_password=...'` if process-list exposure is a concern.
* Use ephemeral shells and short-lived credentials where possible.
* Remember: if Terraform writes the secret to a resource attribute, the value may still be captured in state.

Useful references:

* [Terraform variables — environment variables](https://developer.hashicorp.com/terraform/language/values/variables#environment-variables)

## 3) External secret stores (recommended for production)

For production systems, use a dedicated secrets manager for centralized secret lifecycle management, auditing, and rotation. Options include HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, and Google Secret Manager.

Two common patterns:

* Read secret values at apply time and pass them into resources (convenient but may store plaintext in state).
* Configure resources with secret references/IDs (preferred) so Terraform only stores identifiers (ARNs/IDs) instead of plaintext secrets.

Examples

* AWS Secrets Manager (reading the secret at apply-time):

```hcl theme={null}
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "my-db-password"
}

resource "aws_db_instance" "db" {
  identifier     = "my-db"
  instance_class = "db.t3.micro"
  engine         = "mysql"
  username       = "app_user"

  # Injects plaintext secret read at apply-time
  password = data.aws_secretsmanager_secret_version.db.secret_string
}
```

* HashiCorp Vault (Vault provider data source):

```hcl theme={null}
provider "vault" {
  address = "https://vault.example.com"
  # Authenticate via environment variables like VAULT_TOKEN
}

data "vault_kv_secret_v2" "db" {
  mount = "secret"
  name  = "prod/db"
}

resource "aws_db_instance" "db" {
  identifier     = "my-db"
  instance_class = "db.t3.micro"
  engine         = "mysql"
  username       = "app_user"

  password = data.vault_kv_secret_v2.db.data["password"]
}
```

Important considerations when using secret stores:

* If Terraform reads a secret and writes the plaintext into a resource attribute, the plaintext can end up in state. To avoid this, prefer APIs that accept secret references (for example, pass a Secrets Manager ARN or Key Vault secret reference).
* Design infrastructure to use secret references/IDs where possible so Terraform stores only identifiers.
* Enforce least privilege, short-lived credentials, rotation policies, and audit logging on your secret manager.
* Secure any provider tokens used to read secrets (store them in CI secret stores or encrypted environment variables).

## Recommended practices (short checklist)

| Action                                           | Why                                                            |
| ------------------------------------------------ | -------------------------------------------------------------- |
| Mark inputs/outputs as `sensitive`               | Avoid accidental printing in CLI output and logs               |
| Use `TF_VAR_` or CI secret injection             | Keep secrets out of `.tf` and `.tfvars` and out of VCS         |
| Prefer secret references (ARNs/IDs) in resources | Prevents plaintext secrets from being stored in state          |
| Use external secret managers for production      | Centralized control, rotation, auditing                        |
| Secure remote state backend                      | Encrypt state at rest and enforce ACLs                         |
| Avoid passing secrets on the CLI                 | Command-line arguments can be visible to other processes/users |

## Quick reference: do's and don'ts

* Do: mark inputs/outputs as `sensitive` to reduce accidental exposure in logs.
* Do: inject secrets via environment variables or CI/CD secret stores rather than committing them.
* Do: use external secret managers in production and prefer passing secret references (ARNs/IDs) to resources.
* Do: secure your Terraform state with a remote backend, encryption, and strict access controls.
* Don’t: hardcode secrets in `.tf` or `.tfvars` that are committed to version control.
* Don’t: pass secrets on the `terraform` command line if process-list leakage is a concern.
* Don’t: assume `sensitive` prevents secrets from being stored in state—treat state as sensitive.

<Callout icon="lightbulb">
  Best practice summary:

  * Use `sensitive` for variables and outputs to avoid CLI leaks.
  * Prefer environment variable injection for development and CI.
  * Use a secrets manager for production and pass secret references (ARNs/IDs) when possible.
  * Always protect and monitor your Terraform state backend.
</Callout>

## Closing

These three approaches are complementary. In real projects you’ll often:

1. Mark variables and outputs `sensitive` to reduce accidental exposure.
2. Use environment variables or CI secret injection for development and automated pipelines.
3. Rely on a dedicated secret manager in production—prefer secret references so Terraform does not store plaintext secrets in state.

Always treat your Terraform state as a sensitive asset: encrypt it, restrict access, and audit read permissions. For deeper reading, consult the official Terraform docs on variables, state, and remote backends:

* [Terraform variables](https://developer.hashicorp.com/terraform/language/values/variables)
* [Terraform state and remote backends](https://developer.hashicorp.com/terraform/language/state/remote)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/3d61e668-8dff-4336-8b5e-029e8b5520ab" />
</CardGroup>
