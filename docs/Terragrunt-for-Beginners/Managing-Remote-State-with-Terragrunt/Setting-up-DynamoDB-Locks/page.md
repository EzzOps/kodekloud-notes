# Setting up DynamoDB Locks

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Managing-Remote-State-with-Terragrunt/Setting-up-DynamoDB-Locks/page

This article explains how to set up DynamoDB locks using Terraform and Terragrunt for managing state file consistency in Infrastructure as Code workflows.

Implementing state locking is critical for any Infrastructure as Code (IaC) workflow. By leveraging AWS DynamoDB, Terraform and Terragrunt coordinate changes to prevent conflicting updates and ensure consistency.

<Frame>
  ![The image describes the features of Terraform/Terragrunt locks using AWS DynamoDB, highlighting state file locking, prevention of multiple user access, and the use of DynamoDB for state locking.](https://kodekloud.com/kk-media/image/upload/v1752884270/notes-assets/images/Terragrunt-for-Beginners-Setting-up-DynamoDB-Locks/terraform-terragrunt-dynamodb-locks-features.jpg)
</Frame>

Terraform and Terragrunt acquire a lock before performing any write operations on the state file. In AWS-based pipelines, DynamoDB acts as the lock manager. This setup guarantees:

* Exclusive write access to the state
* Automatic creation of the lock table (when using Terragrunt’s `remote_state`)
* Reliable, distributed coordination across teams and CI/CD environments

## Configuring `remote_state` in Terragrunt

To enable DynamoDB locking, define a `remote_state` block in your `terragrunt.hcl`. Terragrunt will create the DynamoDB table if it doesn’t already exist.

```hcl theme={null}
remote_state {
  backend = "s3"
  config = {
    bucket         = "my-terraform-state-bucket"
    key            = "envs/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "my-terraform-lock-table"
  }
}
```

<Callout icon="lightbulb">
  Terragrunt automatically provisions the DynamoDB table specified by `dynamodb_table`. You only need AWS IAM permissions for S3 and DynamoDB table creation.
</Callout>

| Backend Option  | Description                                      | Example Value                   |
| --------------- | ------------------------------------------------ | ------------------------------- |
| bucket          | S3 bucket name for state storage                 | `"my-terraform-state-bucket"`   |
| key             | Path within bucket for the `.tfstate` file       | `"envs/prod/terraform.tfstate"` |
| region          | AWS region for both S3 and DynamoDB operations   | `"us-east-1"`                   |
| encrypt         | Enable server-side encryption (SSE) for the file | `true`                          |
| dynamodb\_table | DynamoDB table name for state locking            | `"my-terraform-lock-table"`     |

## Handling Stuck Locks

If a Terraform or Terragrunt process crashes mid-run, the DynamoDB lock may remain, blocking subsequent operations. Use the force-unlock command to clear a stuck lock.

```bash theme={null}
