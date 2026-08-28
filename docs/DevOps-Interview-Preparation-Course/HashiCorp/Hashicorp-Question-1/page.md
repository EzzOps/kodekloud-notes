# Hashicorp Question 1

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/HashiCorp/Hashicorp-Question-1/page

This article explains how to securely manage database credentials using Terraform and HashiCorp Vault, emphasizing best practices for handling sensitive information.

When using Terraform to create databases—such as AWS RDS instances—one of the primary concerns is how to securely store sensitive credentials like database usernames and passwords. Instead of hardcoding these details in your Terraform configuration or committing them to a [GitHub repository](https://github.com), you can integrate Terraform with a secure secrets management solution like HashiCorp Vault.

<Callout icon="lightbulb">
  Always treat sensitive credentials as secrets. Exposing them in your code or through unsecured channels (e.g., email or Slack) can lead to unauthorized access and potential damage.
</Callout>

This approach allows you to reference the Vault location containing your sensitive data—without embedding the actual secrets in your Terraform code. During a `terraform apply`, Terraform connects to Vault to fetch the necessary credentials dynamically, ensuring that your database instance is created securely at runtime.

<Frame>
  ![The image explains the use of Terraform and Vault integration to manage secrets like DB usernames and passwords, emphasizing best practices for not committing these to a GitHub repository. It includes a diagram showing the process of using a Vault provider and referencing secrets via a data block in Terraform.](https://kodekloud.com/kk-media/image/upload/v1752873356/notes-assets/images/DevOps-Interview-Preparation-Course-Hashicorp-Question-1/terraform-vault-secrets-integration.jpg)
</Frame>

Below is an example Terraform configuration demonstrating this secure integration:

```hcl theme={null}
provider "vault" {
  address = "https://vault.example.com"
}

data "vault_generic_secret" "db_credentials" {
  path = "secret/data/db"
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = data.vault_generic_secret.db_credentials.data.username
  password             = data.vault_generic_secret.db_credentials.data.password
  parameter_group_name = "default.mysql5.7"
}
```

In this configuration:

* The Vault provider block specifies the address of your Vault server.
* The data block (`vault_generic_secret`) retrieves the database credentials from Vault securely.
* The `aws_db_instance` resource uses these dynamically fetched credentials at runtime to create the database instance.

If HashiCorp Vault is not an option in your environment, consider using other secure secrets management services such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/). However, it is crucial to avoid insecure storage options like using an [S3 bucket](https://aws.amazon.com/s3/) for storing sensitive data in plaintext.

<Callout icon="triangle-alert">
  Never store or expose sensitive credentials in your Terraform code or repositories. Always utilize a secure, dedicated secrets management system to prevent unauthorized access.
</Callout>

Integrating Terraform with a secure secrets management solution not only enhances your infrastructure security but also demonstrates a solid practice during technical interviews. Understanding how Terraform data blocks interact with Vault or similar services is a valuable skill in today's DevOps landscape.

This lesson has shown you how to integrate Terraform with HashiCorp Vault so that your sensitive credentials remain secure throughout your deployment process. Stay tuned for more best practices on managing infrastructure securely.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-preparation-course/module/04f41564-5032-49c6-a98f-da77606c4687/lesson/160c382d-8c49-4f34-a388-54a426ea545b" />
</CardGroup>
