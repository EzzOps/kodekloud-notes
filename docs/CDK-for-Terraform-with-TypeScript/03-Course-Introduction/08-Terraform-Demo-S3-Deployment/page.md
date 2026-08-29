# run the TypeScript example
pwd
/root/code

ts-node app.ts
# Output:
# The total price is: 100
```

## Example shell commands you’ll see in labs

These are representative commands used to show working directories and run local tasks:

```bash theme={null}
pwd
/root/code

cd ~
```

## Additional Resources and References

* Official CDK for Terraform docs: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform docs: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* TypeScript Handbook: [https://www.typescriptlang.org/docs/handbook/intro.html](https://www.typescriptlang.org/docs/handbook/intro.html)
* AWS Documentation: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)

If you’re ready to build, scale, and automate cloud resources effectively with TypeScript and CDKTF, you’re in the right place. Join the forums, ask questions, and practice the labs — hands-on experience is the fastest way to master CDKTF.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/5cb4cc76-073f-4897-b4dc-4a5d91597ff5" />
</CardGroup>


# Terraform Demo S3 Deployment

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Terraform-Demo-S3-Deployment/page

Demo repository showing how to deploy AWS S3 buckets with Terraform using a reusable module, random unique names, and object lock considerations

This lesson walks through deploying S3 buckets with Terraform. The repository includes a root configuration that configures the AWS provider, generates a short random ID for unique bucket names, creates one bucket directly, and uses a reusable module for a second bucket. The same Terraform code creates reproducible cloud resources using HashiCorp Configuration Language (HCL).

## Repository layout (highlight)

* Root `main.tf` — provider, `random_id`, one `aws_s3_bucket` resource, and a module call.
* `modules/s3_bucket_with_env_tag/` — a simple module that creates a bucket and applies an `env` tag.
* Terraform state and plan artifacts are created when you run `terraform init` and `terraform apply`.

## Root configuration (abbreviated)

Root `main.tf`:

```hcl theme={null}
