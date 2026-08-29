# Read the secret from AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_pass" {
  secret_id = "production/database/password"
}

# Use it in your resource
resource "aws_db_instance" "main" {
  identifier     = "mydb"
  engine         = "postgres"
  instance_class = "db.t3.micro"
  username       = "admin"
  # Secret is fetched at plan/apply time
  password       = data.aws_secretsmanager_secret_version.db_pass.secret_string
}
```

Operational notes for this pattern

* The secret value is not present in your `.tf` or `.tfvars` files—only the reference to Secrets Manager is.
* Terraform (or the CI runner executing Terraform) must have IAM permissions to read the secret.
* The secret value will typically be written to Terraform state after resource creation. Protect state using encrypted, access-controlled backends (for example, S3 + KMS with restricted IAM).
* The same concept applies to other platforms: use the Azure Key Vault, Google Secret Manager, or Vault data sources. Syntax differs, but the core idea—read at plan/apply and reference in resources—remains the same.

Advanced Vault patterns

* HashiCorp Vault supports dynamic credentials, leasing, and short-lived secrets—features that increase security for production workloads. Consider Vault when you need dynamic secrets or granular programmatic control.

Protection Quick Reference

Below is a concise comparison of three techniques for protecting secrets during provisioning: sensitive variables, environment variables, and external secret sources.

| Technique                |        Protects console logs/output |                                      Protects Terraform state |              Protects Git commits | Recommended use                                                                          |
| ------------------------ | ----------------------------------: | ------------------------------------------------------------: | --------------------------------: | ---------------------------------------------------------------------------------------- |
| Sensitive variables      |                  Yes (hides output) |                                    No (can still be in state) | Yes (reduces accidental exposure) | Use `sensitive = true` for variables/outputs to reduce accidental prints                 |
| Environment variables    | Partially (depends on process logs) | No (values passed to Terraform can still be written to state) |  Yes (keeps secrets out of files) | Use `TF_VAR_*` or `AWS_*` env vars for local dev and CI injection                        |
| External secret managers |   Yes (prevents embedding in files) |                           No (state may still contain values) |         Yes (secrets not in repo) | Use AWS Secrets Manager, Vault, Azure Key Vault, or Google Secret Manager for production |

Key recommendations (defense in depth)

* Store secrets in an external secrets manager for centralized lifecycle management and rotation.
* Inject secrets into the Terraform runtime via environment variables when appropriate (keeps secrets out of files).
* Mark variables and outputs as `sensitive = true` to avoid exposing values in logs and console output.
* Protect Terraform state with a remote backend, encryption (for example, KMS), and least-privilege IAM roles; assume secrets may appear in state.

<Callout icon="warning">
  Even when you read secrets from an external manager, the secret values may end up in Terraform state. Make sure your state backend is encrypted and access is restricted (for example, use a remote backend with KMS encryption and least-privilege IAM).
</Callout>

<Frame>
  <img alt="The image is a &#x22;Protection Quick Reference&#x22; table comparing techniques for protecting logs/output, state, and Git commits, highlighting sensitive variables, environment variables, and external sources. It includes recommendations for using environment variables, storing secrets externally, and using sensitive variables to hide output." />
</Frame>

Wrapping up

This guide covered how to protect secrets when provisioning infrastructure with Terraform:

* Protect inputs with `sensitive` variables.
* Keep secrets out of version control by using environment variables for injection.
* Use an external secrets manager for production-grade security and centralized rotation.
* Secure your Terraform state—encrypt it, restrict access, and minimize sensitive data stored in it.

Further reading and references

* [Terraform documentation](https://www.terraform.io/docs)
* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
* [HashiCorp Vault](https://www.vaultproject.io/)
* [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)
* [Google Secret Manager](https://cloud.google.com/secret-manager)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/6692aa5c-6e6f-4e94-8c89-ba37927f2894" />
</CardGroup>


# Securing State Files

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Securing-State-Files/page

Guidance on securing Terraform state files using remote backends, encryption, access controls, state locking, auditing, and safe migration to prevent secret exposure.

In this lesson we shift focus from protecting secrets in your configuration (sensitive variables, environment variables, and external secret stores) to the place where those secrets ultimately reside: the Terraform state file.

Terraform state contains the complete configuration for every resource it manages, including attributes required to create and manage infrastructure — and sensitive values such as database passwords, API keys, private keys, and TLS certificates. Because state is plain JSON by default, any user who can read the file can access those secrets.

<Callout icon="lightbulb">
  Terraform state files often include secrets. Treat state as a sensitive artifact: secure where it’s stored, who can access it, and how it’s audited.
</Callout>

Example state snippet (JSON) showing sensitive values stored in plain text:

```json theme={null}
{
  "version": 4,
  "terraform_version": "1.5.0",
  "serial": 1,
  "lineage": "abcd1234-ef56-7890-abcd-ef1234567890",
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
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "password": "MySuperSecretPassword123!"
          }
        }
      ]
    }
  ]
}
```

<Callout icon="warning">
  Do not commit Terraform state files to version control. They commonly contain secrets and other sensitive infrastructure data.
</Callout>

Why local state is risky

* Local state is stored on a developer workstation unencrypted unless you encrypt your disk.
* It’s easy to accidentally commit `terraform.tfstate` to Git.
* Sharing local state via email or chat is insecure.
* Local state provides no built-in access control, role-based permissions, or audit logging.

Why remote state is safer

* Centralized storage prevents long-term state residency on developer machines.
* Backends commonly support encryption at rest (SSE-S3, SSE-KMS, Azure Storage encryption, GCS encryption).
* Access is managed via IAM/RBAC, allowing fine-grained permissions for read/write/list operations.
* Audit logging (e.g., CloudTrail) records who accessed state and when.
* State locking prevents concurrent modifications that could corrupt state.

Comparison: Local vs Remote State

| Feature            |                  Local State | Remote State (recommended)                              |
| ------------------ | ---------------------------: | ------------------------------------------------------- |
| Encryption at rest |   Depends on disk encryption | Typically supported (SSE-S3, SSE-KMS, provider-managed) |
| Access control     | File system permissions only | IAM / RBAC controls via backend                         |
| Audit logging      |                         None | Provider logs (e.g., CloudTrail, audit records)         |
| State locking      |                Not available | Supported by many backends (DynamoDB, etc.)             |
| Team collaboration |       Risky / manual sharing | Centralized, safe collaboration                         |

For production workloads, always use a remote backend with encryption and locking enabled. Local state is acceptable only for learning or single-developer experiments.

How to configure encrypted remote state (example: Amazon S3)

Below is an S3 backend configuration that stores state in an S3 bucket and uses DynamoDB for locking. Put this in a Terraform configuration file (e.g., `backend.tf`).

```hcl theme={null}
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"         # state locking table
    encrypt        = true                      # SSE-S3 (AES-256) server-side encryption
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abcd-efgh-ijkl" # SSE-KMS (recommended)
  }
}
```

Notes on encryption and locking:

* `encrypt = true` enables S3 server-side encryption with AES-256 (SSE-S3).
* Specifying a `kms_key_id` causes S3 to use AWS KMS (SSE-KMS). SSE-KMS is recommended because it provides additional access controls and audit trails for decryption.
* Use `dynamodb_table` to enable state locking, which prevents concurrent `terraform apply` runs from corrupting state.
* In production prefer SSE-KMS over SSE-S3 for better access control and auditing.

Migrating existing local state to a remote backend

You can switch to a remote backend at any time. If a backend block is added to a project that already has local state, running `terraform init` will prompt you to migrate the existing local state to the remote backend. This makes migration safe and non-disruptive.

Layered security for state files

Apply defense-in-depth when protecting state. Typical layers include:

1. Encryption at rest (SSE-S3 or SSE-KMS).
2. State locking to prevent concurrent changes.
3. Fine-grained IAM/RBAC policies to restrict access.
4. Audit logging (CloudTrail or provider logs) to track access and changes.

Each layer complements the others: if one control is misconfigured, additional layers still protect your secrets.

State file security checklist

| Requirement                 | Why it matters                              | Example / Action                                         |
| --------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| Remote state for production | Centralized control and safer collaboration | Use S3, Azure Storage, or GCS backend                    |
| Encryption at rest          | Prevents plaintext secrets on storage       | Enable SSE-KMS or SSE-S3 (`encrypt = true`)              |
| Fine-grained access control | Limits who can read/write state             | Use IAM roles, policies, or RBAC                         |
| State locking               | Prevents concurrent writes and corruption   | Configure DynamoDB (`dynamodb_table`) or backend locking |
| Audit logging               | Trace access and detect misuse              | Enable CloudTrail, provider audit logs                   |

<Frame>
  <img alt="The image displays a &#x22;State File Security Checklist&#x22; with four items: remote state use for production, encryption at rest, access controls, and state locking, all checked off. A note emphasizes the importance of protecting state files containing secrets." />
</Frame>

Conclusion

Terraform state files will contain secrets — this is unavoidable. Your responsibility is to secure the storage and access to state. Follow the checklist: use a remote backend, enable encryption (prefer KMS), implement access controls, enable state locking, and keep audit logging enabled. Provider-specific features (for example, write-only provider arguments) can add an extra layer of protection.

Links and references

* [Terraform Remote State](https://www.terraform.io/docs/state/index.html)
* [S3 Backend for Terraform](https://www.terraform.io/docs/backends/types/s3.html)
* [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
* [DynamoDB for State Locking](https://www.terraform.io/docs/backends/types/s3.html#dynamodb-table)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/937ac82e-4dee-466c-92aa-9a731752424e/lesson/d01bf993-41e6-4d77-90a5-2a6797ce3668" />
</CardGroup>
