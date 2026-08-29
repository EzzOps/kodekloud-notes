# environments/prod/main.tf
module "custom_vpc" {
  source       = "../../modules/custom_vpc"
  cidr_block   = var.vpc_cidr
  environment  = "prod"
}
```

***

## Community Modules

Community modules are shared on public registries and maintained by the broader Terraform user base. They offer:

* **Rapid Development**\
  Address common patterns—VPC, IAM roles, load balancers—without reinventing the wheel.

* **Collective Expertise**\
  Leverage bug fixes and improvements contributed by many users.

* **Continuous Updates**\
  Popular modules receive frequent enhancements and support for new provider features.

### When to Choose Community Modules

* Your use case aligns with widely adopted infrastructure patterns.
* You want to reduce development and maintenance overhead.
* You’re comfortable with community-driven versioning and updates.

### Example: Consuming a Community Module

```hcl theme={null}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.10.0"
  name    = "my-vpc"
  cidr    = "10.0.0.0/16"
}
```

***

## Comparison Table

| Criteria          | Custom Modules               | Community Modules              |
| ----------------- | ---------------------------- | ------------------------------ |
| Control           | 100% custom architecture     | Constrained by upstream design |
| Development Speed | Longer due to bespoke design | Fast—plug & play               |
| Maintenance       | On your team                 | Shared across community        |
| Compliance        | Fully customizable           | Audit required before adoption |
| Update Cadence    | Scheduled by your team       | Depends on module author       |

***

## Hybrid Module Approach

For many projects, a hybrid strategy is ideal:

1. **Leverage Community Modules** for standard components (e.g., networking, compute, storage).
2. **Wrap or Extend** those modules to enforce naming conventions, tagging policies, or security guardrails.
3. **Develop Custom Modules** only for truly unique business logic or specialized integrations.

```hcl theme={null}
module "secure_vpc" {
  source = "git::https://github.com/your-org/terraform-aws-vpc-wrapper.git?ref=v1.2.0"
  # Wraps the upstream VPC module with your policies
}
```

***

## Key Considerations

* **Security & Compliance**

<Callout icon="lightbulb">
  Always review third-party module code for hidden risks before deploying to production.
</Callout>

* **Version Locking**

<Callout icon="triangle-alert">
  Pin module versions to avoid unexpected breaking changes:

  ```hcl theme={null}
  module "vpc" {
    source  = "terraform-aws-modules/vpc/aws"
    version = "3.10.0"
  }
  ```
</Callout>

* **Documentation & Support**\
  Verify that community modules are well-documented and actively maintained.

* **Team Expertise**\
  Assess your team’s Terraform skills to gauge how much custom work you can sustain.

***

## Conclusion

Choosing between Custom and Community modules isn’t an all-or-nothing decision. By understanding the strengths and limitations of each, you can craft a Terraform module strategy that accelerates development, enforces best practices, and adapts to your project’s unique needs.

***

## References

* [Terraform Registry](https://registry.terraform.io/)
* [Terraform Modules Overview](https://www.terraform.io/docs/modules/index.html)
* [Terraform Best Practices](https://learn.hashicorp.com/terraform/modules)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/209205f7-ed08-47c5-a92a-84f7794a093a" />
</CardGroup>


# Demo Creating Your Own Module From Scratch

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Demo-Creating-Your-Own-Module-From-Scratch/page

This tutorial teaches how to build a reusable Terraform module for an AWS S3 bucket and consume it with Terragrunt.

In this tutorial, you’ll learn how to build a reusable Terraform module for an AWS S3 bucket and then consume it with Terragrunt. You’ll get hands-on experience with:

1. Directory structure
2. Writing module files (`main.tf`, `variables.tf`, `outputs.tf`)
3. Referencing the module in Terragrunt
4. Initializing, planning, and applying changes
5. Verifying the S3 bucket

***

## 1. Directory Structure

Organize your project by creating a dedicated module folder:

```bash theme={null}
mkdir -p modules/s3
cd modules/s3
touch main.tf variables.tf outputs.tf
```

Your workspace should resemble:

```HCL theme={null}
.
├── modules
│   └── s3
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── terragrunt.hcl
```

| File         | Purpose             | Description                                    |
| ------------ | ------------------- | ---------------------------------------------- |
| main.tf      | Resource definition | Defines the `aws_s3_bucket` resource           |
| variables.tf | Input variables     | Declares variables like `bucket_name`          |
| outputs.tf   | Outputs             | Exposes attributes such as bucket name and ARN |

***

## 2. Writing the S3 Module

### main.tf

Create the S3 bucket using the `bucket_name` variable:

```hcl theme={null}
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}
```

### variables.tf

Declare the bucket name as a required input:

```hcl theme={null}
variable "bucket_name" {
  type        = string
  description = "Unique name for the S3 bucket"
}
```

<Callout icon="triangle-alert">
  S3 bucket names must be globally unique and comply with AWS naming rules.\
  Avoid uppercase letters and underscores.
</Callout>

### outputs.tf

Expose both the bucket name and ARN:

```hcl theme={null}
output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.this.arn
}
```

***

## 3. Consuming the Module with Terragrunt

In your root or environment-specific folder, configure Terragrunt to source the S3 module:

```hcl theme={null}
