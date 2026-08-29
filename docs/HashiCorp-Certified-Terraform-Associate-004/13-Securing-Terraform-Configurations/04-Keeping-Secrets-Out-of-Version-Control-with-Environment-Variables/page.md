# Keeping Secrets Out of Version Control with Environment Variables

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Keeping-Secrets-Out-of-Version-Control-with-Environment-Variables/page

Explains using environment variables and CI/CD secret stores to avoid committing secrets in Terraform and outlines protecting Terraform state and sensitive variables

Storing secrets directly in Terraform files is a common security mistake — one that’s easy to make and costly to remediate. This guide explains why committing secrets is risky, how environment variables mitigate most of that risk, and what gaps remain (notably Terraform state).

Why this matters: once credentials are committed, they persist in Git history unless you rewrite it — a difficult, risky process for shared repositories. If automated scanners find credentials, you’ll likely need to rotate secrets, revoke API keys, and investigate potential exposure.

> **warning** Never commit secrets into version control. If you do, treat those credentials as compromised and rotate them immediately.

Typical bad example (do not commit this):

```hcl theme={null}
db_password = "MyS3cr3tP@ssw0rd!"
db_username = "admin"
api_key = "sk-abc123xyz789"
```

Use environment variables instead

Rather than writing secrets to disk, set them in your local shell or inject them at runtime from your CI/CD system. Terraform automatically maps environment variables named `TF_VAR_<variable_name>` to input variables in your configuration.

Local shell example:

```bash theme={null}
export TF_VAR_db_password="MyP@ssw0rd!"
export TF_VAR_api_key="sk-abc123xyz"
terraform apply
```

In your Terraform code, declare variables normally and mark sensitive variables with `sensitive = true`. Do not set a `default` for secrets you expect to supply at runtime:

```hcl theme={null}
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

Why environment variables help

* Secrets aren’t stored as files on disk; they live only in memory for the shell session or CI job.
* They can’t accidentally be committed to Git, removing the most common leakage vector.
* CI/CD systems (GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.) provide encrypted secret management and inject secrets as environment variables at runtime.
* Marking variables with `sensitive = true` gives additional protection by hiding values in Terraform outputs and logs.

Quick comparison

| Concern                        | Local environment variables | CI/CD secrets                     | Terraform state                        |
| ------------------------------ | --------------------------- | --------------------------------- | -------------------------------------- |
| Risk of being committed to Git | Low                         | Low (encrypted at rest)           | High — state can contain secrets       |
| Storage location               | Memory of shell session     | CI provider’s encrypted store     | State file (remote or local)           |
| Rotation / access control      | Manual                      | Managed by provider (recommended) | Requires state handling best practices |

<Frame>
  <img alt="The image highlights the benefits of using environment variables, such as never being stored in files, never committed to Git, being perfect for CI/CD pipelines, and working with sensitive data. It notes that they do not keep secrets out of state." />
</Frame>

Using environment variables in CI/CD

Store secrets in your CI/CD provider’s secrets store and inject them at runtime. Example GitHub Actions workflow that references repository secrets and maps them to `TF_VAR_*` environment variables:

```yaml theme={null}
name: Terraform Apply
on: [push]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Terraform Apply
        env:
          TF_VAR_db_password: ${{ secrets.DB_PASSWORD }}
          TF_VAR_api_key: ${{ secrets.API_KEY }}
        run: |
          terraform init
          terraform apply --auto-approve
```

GitHub Secrets (and similar features in other CI systems) are encrypted at rest and only decrypted for the running job. CI systems also attempt to redact secrets from logs if they are printed accidentally.

> **lightbulb** For production, store secrets in your CI/CD system or a managed secrets store (for example, AWS Secrets Manager or HashiCorp Vault) and inject them as environment variables at runtime.

State is a separate problem

Environment variables prevent accidental commits, but they do not prevent secrets from being recorded in Terraform state. When Terraform creates resources that include secrets (for example, a database user or API key), those secret values can end up in state files. Protect Terraform state by:

* Using remote/state locking backends (e.g., Terraform Cloud, S3 with DynamoDB locking).
* Enabling encryption at rest for the backend.
* Limiting who can read the state.
* Avoiding placing secrets in resource arguments where possible — use external secret sources.

Summary — checklist

* Do not store secrets in Terraform variable files tracked by Git.
* Use environment variables (`TF_VAR_*`) locally and inject secrets via CI/CD.
* Mark sensitive variables with `sensitive = true`.
* Protect Terraform state separately (remote backend, encryption, access control).
* Consider external secret managers (Vault, AWS Secrets Manager, etc.) to avoid ever storing secrets in Terraform configurations or state.

Links and references

* Terraform input variables: [https://www.terraform.io/docs/language/values/variables.html](https://www.terraform.io/docs/language/values/variables.html)
* GitHub Actions secrets: [https://docs.github.com/en/actions/security-guides/encrypted-secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* AWS Secrets Manager: [https://aws.amazon.com/secrets-manager/](https://aws.amazon.com/secrets-manager/)
* HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/5dd4f27c-a1b4-4068-9de3-190c4e9c9f94)
