# Retrieve the LOCK ID from the error output, then run:
terragrunt force-unlock LOCK_ID --terragrunt-non-interactive
```

<Callout icon="triangle-alert">
  Forcing an unlock can lead to concurrent modifications if another process is still running. Always verify no other operations are active before using `force-unlock`.
</Callout>

## Benefits of DynamoDB State Locking

| Benefit                     | Description                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| Single-Writer Enforcement   | Prevents multiple users or CI jobs from applying at the same time             |
| Automated Table Management  | Terragrunt creates and manages the DynamoDB lock table, reducing manual steps |
| Robust CI/CD Integration    | Locks persist across distributed pipelines, ensuring consistent state access  |
| Safe Recovery from Failures | `force-unlock` provides a backdoor to unblock state operations                |

By combining Terraform, Terragrunt, Amazon S3, and DynamoDB locks, teams can focus on building infrastructure rather than wrestling with state conflicts.

## Links and References

* [Terraform Remote State](https://www.terraform.io/language/state/remote)
* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [AWS DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondb/)
* [Managing Locks with S3 and DynamoDB](https://www.terraform.io/docs/cloud/run/lock.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/2eef056a-8494-4e5d-acf0-25b04fad55c4/lesson/216870e3-4bb2-4c54-97bf-c65306283363" />
</CardGroup>


# Demo of Lab 4

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Attributes/Demo-of-Lab-4/page

This article guides configuring Terragrunt to deploy and manage an AWS VPC module with best practices for security and efficiency.

Welcome to Lab 4. In this lesson, you’ll configure Terragrunt to deploy and manage an AWS VPC module. You have access to an AWS account—follow the steps below to set up credentials, initialize modules, enforce safeguards, and customize Terragrunt settings for a robust infrastructure workflow.

<Callout icon="lightbulb">
  Keep your AWS credentials secure. You can retrieve them with:

  ```bash theme={null}
  show creds
  ```

  Or log in via the provided link using your username and password. Consider opening a second terminal tab to streamline copy-and-paste.
</Callout>

***

## 1. Configure the VPC Module

In `Terraform stack/VPC/terragrunt.hcl`, reference the remote AWS VPC module (v5.8.1) from the Terraform Registry:

```hcl theme={null}
terraform {
  source  = "registry.terraform.io/terraform-aws-modules/vpc/aws"
  version = "5.8.1"
}

inputs = {
  name = "KodeKloud VPC"
  cidr = "10.64.0.0/16"
}
```

Initialize and review the plan:

```bash theme={null}
cd "Terraform stack/VPC"
terragrunt init
terragrunt plan
```

You should see **4 to add**. If everything checks out, continue to the next section.

***

## 2. Configure a Custom Terragrunt Cache

Terragrunt can cache downloaded modules locally to speed up repeated runs. Add a top-level `download_dir` in your root `terragrunt.hcl`:

```hcl theme={null}
download_dir = "/full/path/to/Terraform stack/.terragrunt_config"

terraform {
  source  = "registry.terraform.io/terraform-aws-modules/vpc/aws"
  version = "5.8.1"
}

remote_state {
  backend = "local"
  config  = {}
}

inputs = {
  name = "KodeKloud VPC"
  cidr = "10.64.0.0/16"
}
```

Re-initialize and verify the cache directory:

```bash theme={null}
terragrunt init
ls "Terraform stack/.terragrunt_config"
```

Then plan and apply:

```bash theme={null}
terragrunt plan
terragrunt apply
```

After confirming the apply, check the AWS Console under **VPC** to see your new VPC.

***

## 3. Prevent Accidental Destruction

Protect critical resources by adding a `prevent_destroy` lifecycle rule:

```hcl theme={null}
lifecycle {
  prevent_destroy = true
}
```

Re‐apply and test destruction:

```bash theme={null}
terragrunt apply
terragrunt destroy
```

Terragrunt will refuse to destroy due to the `prevent_destroy` setting.

<Callout icon="triangle-alert">
  If you need to remove the resource later, you must first remove or comment out the `prevent_destroy` block.
</Callout>

***

## 4. Use a Specific IAM Role

All Terragrunt operations should assume the `KodeKloudTerragruntRole` role. Retrieve your AWS account ID:

```bash theme={null}
aws sts get-caller-identity --output text --query Account
```

Then add the role ARN to `terragrunt.hcl`:

```hcl theme={null}
iam_role = "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/KodeKloudTerragruntRole"
```

Verify the role is in use:

```bash theme={null}
terragrunt plan
```

***

## 5. Specify a Custom Terraform Binary & Version

Use the Terraform 1.82 binary packaged in this stack:

```hcl theme={null}
terraform_binary             = "/full/path/to/Terraform stack/terraform_1.82/terraform"
terraform_version_constraint = "1.82"
```

Re‐run:

```bash theme={null}
terragrunt init
terragrunt plan
```

***

## 6. Enforce a Terragrunt Version Constraint

Require Terragrunt in the `>= 0.34.0, < 0.40.0` range:

```hcl theme={null}
terragrunt_version_constraint = ">= 0.34.0, < 0.40.0"
```

If you encounter a compatibility error (e.g., on version 0.58.8), update to include your version:

```hcl theme={null}
terragrunt_version_constraint = ">= 0.34.0, <= 0.59"
```

Then re‐plan:

```bash theme={null}
terragrunt plan
```

***

## 7. Configure Retryable Errors

Handle transient network or locking issues by specifying retry patterns:

```hcl theme={null}
retryable_errors = [
  "Error locking state:.*",
  "no such host",
  "request timed out"
]
```

Run:

```bash theme={null}
terragrunt plan
terragrunt apply
```

Terragrunt will retry on matching errors automatically.

***

## Terragrunt Settings at a Glance

| Setting                         | Purpose                                 | Example                                              |
| ------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| terraform.source                | Module source                           | `"registry.terraform.io/.../vpc/aws"`                |
| download\_dir                   | Cache directory for modules             | `"/path/to/.terragrunt_config"`                      |
| lifecycle.prevent\_destroy      | Prevent critical-resource deletion      | `prevent_destroy = true`                             |
| iam\_role                       | Specifies assumed IAM role              | `"arn:aws:iam::123456789012:role/...TerragruntRole"` |
| terraform\_binary               | Custom Terraform CLI path               | `"/path/to/terraform_1.82/terraform"`                |
| terraform\_version\_constraint  | Lock Terraform to a specific version    | `"1.82"`                                             |
| terragrunt\_version\_constraint | Lock Terragrunt to a version range      | `">= 0.34.0, <= 0.59"`                               |
| retryable\_errors               | Patterns that trigger automatic retries | `["Error locking state:.*", "no such host"]`         |

***

## Links and References

* [Terraform AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws)
* [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
* [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
* [AWS IAM Roles Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

That completes **Lab 4**. Thank you for following along!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/1a2a45b4-e7d1-4af2-a897-7ebf83a4350e/lesson/85edd206-4f62-45a0-9a1e-b392827e2847" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/1a2a45b4-e7d1-4af2-a897-7ebf83a4350e/lesson/6e9c7bbd-209c-4ab0-a0dc-410eb3c2af6b" />
</CardGroup>
