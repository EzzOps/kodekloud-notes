# Configure the AWS provider
provider "aws" {
  region = "us-east-1"
}

# Random ID to ensure unique bucket name
resource "random_id" "bucket_id" {
  byte_length = 4
}

# Create an S3 bucket
resource "aws_s3_bucket" "tf-demo-bucket-1" {
  bucket              = "tf-demo-bucket-1-${random_id.bucket_id.hex}"
  object_lock_enabled = true
}

module "s3_bucket" {
  source = "./modules/s3_bucket_with_env_tag"
  env    = "dev"
  name   = "tf-demo-bucket-2-${random_id.bucket_id.hex}" # Ensure unique bucket name
}
```

Key points:

* `provider "aws"` sets the AWS region.
* `random_id.bucket_id` provides a short hex suffix so bucket names are globally unique.
* `object_lock_enabled = true` enables S3 Object Lock at bucket creation (see important notes below).
* The `module` block reuses `modules/s3_bucket_with_env_tag` and passes `env` and `name` inputs.

## Module: modules/s3\_bucket\_with\_env\_tag

modules/s3\_bucket\_with\_env\_tag/main.tf:

```hcl theme={null}
resource "aws_s3_bucket" "tf-demo-bucket-2" {
  bucket              = var.name
  object_lock_enabled = true
  tags = {
    env = var.env
  }
}
```

modules/s3\_bucket\_with\_env\_tag/variables.tf:

```hcl theme={null}
variable "env" {
  description = "Environment tag for the bucket"
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.env)
    error_message = "The env variable must be either 'dev' or 'prod'."
  }
}

variable "name" {
  description = "The name of the bucket"
  type        = string
}
```

This module:

* Creates a bucket with the provided `name`.
* Enables object lock on creation.
* Applies an `env` tag set to the supplied `env` value (validated to be either `dev` or `prod`).

<Callout icon="lightbulb">
  Important: Amazon S3 requires versioning to be enabled on a bucket to use Object Lock. In Terraform you should add a `versioning` block inside the bucket resource when enabling object lock:

  ```hcl theme={null}
  resource "aws_s3_bucket" "example" {
    bucket              = "example-bucket"
    object_lock_enabled = true

    versioning {
      enabled = true
    }
  }
  ```
</Callout>

## Notes and caveats

* Object Lock must be enabled at bucket creation and cannot be disabled later. Plan accordingly for retention and compliance.
* Using a `random_id` or other unique suffix avoids global name collisions for S3 buckets.
* The `env` tag applied by the module helps with cost allocation and filtering in the AWS console.

<Callout icon="warning">
  Buckets created with object lock enabled are configured at creation time and cannot have object lock disabled later. Ensure you understand retention and compliance requirements before enabling this feature.
</Callout>

## What resources will be created?

| Resource Type            | Purpose                                              | Example / Notes                                |
| ------------------------ | ---------------------------------------------------- | ---------------------------------------------- |
| `aws_s3_bucket`          | First bucket created directly in root `main.tf`      | `tf-demo-bucket-1-<random hex>`                |
| `aws_s3_bucket` (module) | Second bucket created via module with `env` tag      | `tf-demo-bucket-2-<random hex>`                |
| `random_id`              | Generates a short unique suffix for bucket names     | `random_id.bucket_id.hex`                      |
| Module inputs            | Reusable configuration for bucket name and `env` tag | `env = "dev"`, `name = "tf-demo-bucket-2-..."` |

## Deploying the Terraform configuration

1. Change into the Terraform directory and initialize:

```bash theme={null}
cd tf
terraform init
```

2. Apply the configuration:

```bash theme={null}
terraform apply
```

Terraform will present a plan and prompt for confirmation:

```text theme={null}
Plan: 3 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

Enter a value:
```

Type `yes` to proceed. After the apply finishes, refresh the S3 console to confirm that the buckets exist and include the random ID suffix.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing a green success banner for creating the bucket &#x22;console-demo-bucket-2-1234&#x22; and the &#x22;General purpose buckets&#x22; list. The table shows two buckets with their names, AWS region (US East N. Virginia) and creation dates." />
</Frame>

If you inspect the second bucket's Properties, you should see the `env` tag set to `dev` (as passed into the module) and the default encryption and MFA delete settings.

<Frame>
  <img alt="Screenshot of an AWS S3 bucket settings page. It shows a tag &#x22;env: dev&#x22;, default server-side encryption using Amazon S3 managed keys (SSE‑S3), and MFA delete disabled." />
</Frame>

## Summary

This example demonstrates infrastructure-as-code with Terraform:

* Declarative HCL creates reproducible AWS S3 resources.
* Modules encapsulate reusable patterns (here, a bucket with an `env` tag).
* Use `random_id` or other uniqueness strategies for globally unique S3 names.
* Remember to enable `versioning` whenever you enable `object_lock_enabled`.

## Links and references

* [Terraform Documentation: AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [Amazon S3 Object Lock Overview](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html)
* [Terraform: Modules](https://developer.hashicorp.com/terraform/language/modules)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/4ab4bc08-1cd8-4221-a974-a6b0700c1318" />
</CardGroup>


# Terraform Overview Benefits and Limitations

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Terraform-Overview-Benefits-and-Limitations/page

Overview of Terraform, highlighting benefits like reproducibility, automation, modularity, and limitations such as HCL learning curve, limited type safety, and comparison with CDK for Terraform.

In this lesson we cover Terraform — what it does, why teams adopt it, and where it can fall short. Expect clear examples and a short comparison with language-based alternatives like CDK for Terraform (CDKTF).

## Benefits

* Consistency and reproducibility\
  Infrastructure is defined as code, so deployments are consistent and predictable across environments (dev, staging, prod). This reduces configuration drift and makes rollbacks easier.
* Automation and efficiency\
  A single CLI command can provision, update, or tear down resources across multiple providers (AWS, Azure, GCP, etc.), removing manual UI steps and human error.
* Version control and collaboration\
  Store Terraform code in Git to track changes, review changes via pull requests, and collaborate across teams with auditable history.
* Modularity and reusability\
  Break configurations into modules (e.g., an S3 bucket module that accepts an `environment` variable) to reuse patterns across accounts and environments and simplify complex architectures.

<Frame>
  <img alt="A presentation slide titled &#x22;Automating Cloud Deployments With This Code&#x22; shows four colorful numbered panels. They list benefits: consistency and reproducibility; automation and efficiency; version control and collaboration; and modularity and reusability." />
</Frame>

For example, an S3 bucket module that accepts an environment variable can be reused in multiple environments, simplifying management of larger architectures.

## Limitations

* Learning curve for HCL\
  HashiCorp Configuration Language (HCL) is declarative and focused on infrastructure. Developers used to imperative languages (TypeScript, Python) will need time to learn HCL idioms and patterns.
* Limited programming flexibility\
  HCL is not a general-purpose language: it lacks constructs such as classes, custom user-defined functions, and rich control flow. While built-in functions and expressions exist, representing complex logic can become verbose or awkward.
* Type safety and validation\
  HCL provides limited compile-time type checking and editor autocompletion compared with typed languages. Many issues only surface at `terraform validate` or `terraform apply`, not directly in the editor.

Below is a concrete example that demonstrates the type-safety limitation. In this Terraform resource, `object_lock_enabled` expects a boolean, but the configuration sets a string value `"foo"`:

```hcl theme={null}
resource "aws_s3_bucket" "tf-demo-bucket-2" {
  bucket              = var.name
  object_lock_enabled = "foo"
  tags = {
    env = var.env
  }
}
```

If you run `terraform validate` (or `terraform apply`), Terraform will report a type error:

```bash theme={null}
$ terraform validate
Error: Incorrect attribute value

  on modules/s3_bucket_with_env_tag/main.tf line 3, in resource "aws_s3_bucket" "tf-demo-bucket-2":
   3:   object_lock_enabled = "foo"

Inappropriate value for attribute "object_lock_enabled": a bool is required.
```

The error appears only when running Terraform commands; many editors won't flag the problem unless you install additional language integrations or linters.

Fixing the value to a boolean resolves the error:

```hcl theme={null}
resource "aws_s3_bucket" "tf-demo-bucket-2" {
  bucket              = var.name
  object_lock_enabled = true
  tags = {
    env = var.env
  }
}
```

After correcting the type, `terraform validate` and `terraform apply` will succeed:

```bash theme={null}
$ terraform apply
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

CDK for Terraform (CDKTF) uses familiar programming languages to provide stronger type safety, richer abstractions, and improved editor experiences when authoring infrastructure-as-code.

<Callout icon="lightbulb">
  Type safety and improved editor tooling are primary motivations for using CDKTF or other language-based IaC approaches. These trade-offs and benefits are explored when adopting language-based IaC solutions.
</Callout>

## Quick comparison: Benefits vs Limitations

| Aspect               | Benefits                                   | Limitations                                               |
| -------------------- | ------------------------------------------ | --------------------------------------------------------- |
| Predictability       | Consistent deployments across environments | Requires discipline for state management and locking      |
| Speed                | Automate provisioning across providers     | Debugging complex HCL logic can be slower                 |
| Collaboration        | Git-based workflows, reviews, and history  | HCL learning curve for developers                         |
| Developer experience | Reusable modules and community providers   | Limited type safety vs typed languages (e.g., TypeScript) |

## References

* Terraform: [https://www.terraform.io/](https://www.terraform.io/)
* HCL language: [https://github.com/hashicorp/hcl](https://github.com/hashicorp/hcl)
* CDK for Terraform (CDKTF): [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)

This overview should help you weigh Terraform's strengths (repeatability, automation, modularity) against its trade-offs (HCL learning curve, reduced programming flexibility, and weaker type safety). Use this when deciding whether plain Terraform or a language-based approach like CDKTF best fits your team.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/66707a98-1e37-458d-acc4-9e05b1f8063f" />
</CardGroup>
