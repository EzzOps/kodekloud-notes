# Hiding Secrets with Sensitive Variables and Outputs

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Hiding-Secrets-with-Sensitive-Variables-and-Outputs/page

Explains using Terraform sensitive variables and outputs to redact secrets in CLI output, and recommends secure state handling and secret management practices

This guide explains a common secret-exposure problem in Terraform, demonstrates the vulnerability, and shows how to fix it using `sensitive = true`. It also clarifies what sensitivity protects and what it does not, and provides best practices for secure secret management.

## Problem

If you pass a secret (e.g., an RDS password) into Terraform as a plain string variable, Terraform will interpolate it into resources — and `terraform plan` will print the secret in the plan output. That output can end up in CI logs, terminal history, screenshots, or other stored artifacts.

Vulnerable example:

```hcl theme={null}
variable "db_password" {
  description = "Database password"
  type        = string
}

resource "aws_db_instance" "main" {
  identifier      = "mydb"
  engine          = "postgres"
  instance_class  = "db.t3.micro"
  username        = "admin"
  password        = var.db_password
}
```

When you run `terraform plan`, the secret can appear in plaintext:

```bash theme={null}
$ terraform plan

Terraform will perform the following actions:
