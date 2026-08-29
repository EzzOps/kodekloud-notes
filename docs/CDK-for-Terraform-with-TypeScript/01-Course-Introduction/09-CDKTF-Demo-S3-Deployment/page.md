# CDKTF Demo S3 Deployment

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/CDKTF-Demo-S3-Deployment/page

Guide to deploying AWS S3 buckets using CDK for Terraform with TypeScript, including reusable constructs, provider setup, random suffixes, synth and deploy steps

This guide shows how to deploy Amazon S3 buckets using CDK for Terraform (CDKTF) with TypeScript. You'll learn how to:

* configure providers (AWS and random),
* build a reusable construct that adds an `env` tag,
* create two S3 buckets (one with a random suffix),
* synthesize and deploy using the Terraform engine.

Prerequisites: Node.js, Yarn, and basic TypeScript knowledge. For more details see the CDKTF docs and Terraform docs:

* CDKTF: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* AWS S3: [https://docs.aws.amazon.com/s3/latest/userguide/Welcome.html](https://docs.aws.amazon.com/s3/latest/userguide/Welcome.html)

## Install dependencies

Change into the CDKTF project directory and install dependencies with Yarn:

```bash theme={null}
cd cdktf/
yarn install
```

Example (trimmed) output:

```bash theme={null}
$ yarn install
> YN0000: · Yarn 4.4.1
> YN0000: · Resolution step
> YN0000: · Fetch step
> YN0000: · Link step
```

## CDKTF TypeScript example (complete)

Below is a concise, complete TypeScript example that demonstrates:

* AWS and random provider configuration
* a reusable `S3BucketWithEnvTag` construct that adds an `env` tag
* a stack creating two S3 buckets (one with a random suffix)
* app instantiation and synthesize

```typescript theme={null}
// main.ts
import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import { AwsProvider, S3Bucket } from '@cdktf/provider-aws';
import { RandomProvider, Id as RandomId } from '@cdktf/provider-random';

interface S3BucketWithEnvTagProps {
  env: 'dev' | 'prod';
  name: string;
}

class S3BucketWithEnvTag extends Construct {
  constructor(scope: Construct, id: string, { env, name }: S3BucketWithEnvTagProps) {
    super(scope, id);

    // Create the S3 bucket with tags and object lock enabled
    new S3Bucket(this, 's3-bucket', {
      bucket: name,
      objectLockEnabled: true,
      tags: {
        env: env,
      },
    });
  }
}

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Configure the AWS provider
    new AwsProvider(this, 'aws-provider', {
      region: 'us-east-1', // change to your preferred region
    });

    // Configure the random provider
    new RandomProvider(this, 'random-provider');

    // Create a random id for bucket suffix
    const randomId = new RandomId(this, 'random-id', {
      byteLength: 4,
    });

    // Create the first S3 bucket with a random suffix and object lock enabled
    new S3Bucket(this, 's3-bucket', {
      bucket: `cdktf-demo-bucket-1-${randomId.hex}`,
      objectLockEnabled: true,
    });

    // Create the second S3 bucket using the reusable construct
    new S3BucketWithEnvTag(this, 's3-bucket-with-env-tag', {
      name: `cdktf-demo-bucket-2-${randomId.hex}`,
      env: 'dev',
    });
  }
}

const app = new App();
new MyStack(app, 'cdktf-demo');
app.synth();
```

Notes about the example:

* The `S3BucketWithEnvTag` class is a reusable construct (component) that encapsulates bucket creation and tagging logic.
* The `RandomId` from the `random` provider is used to create unique bucket names to avoid collisions.
* `objectLockEnabled: true` is set in the example; ensure your bucket configuration and AWS account support object lock if you plan to use it.

## Quick reference: common commands

| Command             | Purpose                                      | Example output / notes                              |
| ------------------- | -------------------------------------------- | --------------------------------------------------- |
| `yarn install`      | Install project dependencies                 | Example trimmed output shown above                  |
| `yarn cdktf synth`  | Synthesize Terraform JSON from the CDKTF app | Produces `terraform.json` / Terraform config files  |
| `yarn cdktf deploy` | Synthesize then apply via Terraform          | Prompts to confirm apply, then provisions resources |

## Deploy with CDKTF

When ready to deploy, run:

```bash theme={null}
yarn cdktf deploy
```

You will be prompted to confirm the apply, similar to the Terraform CLI. Example (trimmed) output after a successful deploy:

```bash theme={null}
Initializing...
Synthesizing Terraform configuration...
Applying changes...

cdktf-demo  random_id.random-id: Creating...
cdktf-demo  random_id.random-id: Creation complete after 0s [id=Nx4LnQ]
cdktf-demo  aws_s3_bucket.s3-bucket: Creating...
cdktf-demo  aws_s3_bucket.s3-bucket-with-env-tag_s3-bucket_D552D986: Creating...
cdktf-demo  aws_s3_bucket.s3-bucket: Creation complete after 2s [id=cdktf-demo-bucket-1-37l1e0b9d]
cdktf-demo  aws_s3_bucket.s3-bucket-with-env-tag_s3-bucket_D552D986: Creation complete after 2s [id=cdktf-demo-bucket-2-37l1e0b9d]
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

No outputs found.
```

## What CDKTF does under the hood

* Your TypeScript code is synthesized by CDKTF into Terraform configuration (HCL/JSON).
* The generated Terraform configuration is executed by the Terraform engine and the specified providers, which create the actual cloud resources (S3 buckets in this example).

A truncated example of the synthesized Terraform JSON metadata:

```json theme={null}
{
  "backend": {
    "local": {
      "path": "/root/code/cdktf/terraform.cdktf-demo.tfstate"
    }
  },
  "required_providers": {
    "aws": {
      "source": "hashicorp/aws",
      "version": "5.76.0"
    },
    "random": {
      "source": "hashicorp/random",
      "version": "3.6.3"
    }
  }
}
```

## Resources created

| Resource                               | Purpose                                                               | Example ID / note               |
| -------------------------------------- | --------------------------------------------------------------------- | ------------------------------- |
| `random_id.random-id`                  | Generates random suffix for bucket names                              | `Nx4LnQ`                        |
| `aws_s3_bucket.s3-bucket`              | First bucket with random suffix and object lock                       | `cdktf-demo-bucket-1-37l1e0b9d` |
| `aws_s3_bucket.s3-bucket-with-env-tag` | Second bucket created via reusable construct, includes `env: dev` tag | `cdktf-demo-bucket-2-37l1e0b9d` |

After apply completes, verify the two new S3 buckets in the AWS Management Console. The second bucket will include the `env: dev` tag that the reusable construct added.

> **lightbulb** If you prefer writing infrastructure in a familiar programming language (TypeScript in this example), CDKTF lets you build reusable constructs and synthesize them into Terraform configuration that still uses the Terraform engine and provider ecosystem.

An overview of how the TypeScript → Terraform flow fits into larger multi-provider and multi-language workflows is discussed later in this article.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/143800c0-baed-4527-b647-1726fef7f375)
