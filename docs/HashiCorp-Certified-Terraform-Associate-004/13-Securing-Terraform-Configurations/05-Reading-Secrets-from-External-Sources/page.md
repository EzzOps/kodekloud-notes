# Reading Secrets from External Sources

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Securing-Terraform-Configurations/Reading-Secrets-from-External-Sources/page

Best practices for retrieving and protecting secrets in Terraform by using external secret managers, marking variables sensitive, injecting via environment variables, and securing Terraform state

Instead of embedding secrets directly in your Terraform code, store them in a dedicated secrets manager such as AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, or Google Secret Manager. These services are purpose-built for secret lifecycle management—rotation, access logging, and encryption at rest—so let them handle secrets and have Terraform retrieve values at runtime.

High-level workflow: Terraform fetches secrets from your secrets manager during plan/apply and then uses those secret values when creating or updating infrastructure.

<Frame>
  <img alt="The image demonstrates a best practice for Terraform, which involves not storing secrets directly in Terraform files. It suggests retrieving secrets before building infrastructure with various cloud providers like AWS, Azure, and Google Cloud." />
</Frame>

Benefits of using an external secrets manager

* Purpose-built controls: rotation, access logging, and encryption at rest are provided by the secrets manager.
* Centralized rotation and access control: rotate a secret once and all consumers read the updated value; manage access with IAM/RBAC.
* Reduced exposure in code: secrets are not hard-coded in `.tf` or `.tfvars` files (note: secrets may still end up in state).
* Single source of truth: Terraform, applications, and monitoring systems can all read the same centrally managed secret.

<Frame>
  <img alt="The image advises not to store secrets in Terraform and suggests using dedicated tools to manage secrets, showing a workflow for retrieving secrets and building infrastructure with AWS, Azure, and Google Cloud." />
</Frame>

How it works in Terraform (AWS Secrets Manager example)

Use a provider-specific data source to read the secret value at plan/apply time and reference that data in your resources. This avoids hard-coding secret values in your repository while letting Terraform inject them when it creates or updates infrastructure.

```hcl theme={null}
