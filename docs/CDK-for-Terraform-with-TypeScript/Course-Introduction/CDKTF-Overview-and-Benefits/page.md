# CDKTF Overview and Benefits

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/CDKTF-Overview-and-Benefits/page

Overview of CDK for Terraform explaining benefits of using programming languages like TypeScript for type safe, reusable infrastructure definitions compatible with Terraform and OpenTofu.

This lesson provides an overview of CDK for Terraform (CDKTF), highlighting its advantages and how it combines Terraform's ecosystem with modern programming languages like TypeScript. You'll learn the core benefits, a short typed example, expected synth/deploy output, and considerations for compatibility and migration.

<Frame>
  <img alt="A presentation slide titled &#x22;CDKTF - Overview and Benefits.&#x22; It shows the AWS logo on a teal curved background with small tool icons and a KodeKloud copyright." />
</Frame>

## Why choose CDKTF?

CDKTF brings the full Terraform provider and module ecosystem together with the expressiveness of familiar programming languages. This combination provides:

* Familiar syntax and constructs (loops, conditionals, functions, classes) for defining infrastructure.
* Better logic reusability through language-level abstractions and helper functions.
* Type safety and IDE auto-completion for safer, faster development and refactoring.
* Direct compatibility with Terraform modules and engines (including OpenTofu), enabling gradual adoption.

### Key benefits at a glance

| Benefit                 | What it provides                                                       | Example/Notes                                                   |
| ----------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| Familiar language       | Use TypeScript (or other supported languages) to define infrastructure | Leverage existing TypeScript skills and libraries               |
| Strong typing           | Early detection of invalid types and improved editor support           | Prevents mistakes like assigning `"true"` to a boolean property |
| Reusability & logic     | Encapsulate patterns using classes, functions, and modules             | Compose complex stacks from reusable constructs                 |
| Terraform compatibility | Outputs Terraform configuration compatible with Terraform/OpenTofu     | Reuse existing modules without rewriting                        |

<Callout icon="lightbulb">
  Using language features and types reduces the learning curve and helps catch issues earlier — type mismatches and invalid patterns are often discovered during development instead of at apply time.
</Callout>

## Type safety example

Below is a simplified TypeScript CDKTF stack demonstrating typed properties. Note how `objectLockEnabled` is typed as a boolean. This example configures the AWS and random providers, creates a random ID, and provisions an S3 bucket using the generated value.

```typescript theme={null}
import { Construct } from "constructs";
import { TerraformStack } from "cdktf";
import { AwsProvider, S3Bucket } from "@cdktf/provider-aws";
import { RandomProvider, RandomId } from "@cdktf/provider-random";

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Configure the AWS provider
    new AwsProvider(this, "aws", {
      region: "us-east-1", // change to your preferred region
    });

    // Configure the random provider
    new RandomProvider(this, "random");

    const randomId = new RandomId(this, "random-id", {
      byteLength: 4,
    });

    // Create the S3 bucket
    new S3Bucket(this, "s3-bucket", {
      bucket: `cdktf-demo-bucket-${randomId.hex}`, // use the generated hex/id
      objectLockEnabled: true, // must be a boolean
      tags: {
        env: "dev",
      },
    });
  }
}
```

If you accidentally assign a string to a boolean-typed property, TypeScript will produce a compile-time error such as:

```text theme={null}
error TS2322: Type '"foo"' is not assignable to type 'boolean'.
```

This immediate feedback prevents invalid configurations from being synthesized or applied.

## Synth & deploy output

When you synthesize and deploy a CDKTF stack (for example, using `cdktf deploy`), the output shows Terraform-style logs for resource lifecycle operations. Example:

```bash theme={null}
cdktf-demo  random_id.random-id: Creating...
cdktf-demo  random_id.random-id: Creation complete after 0s [id=Nx4LnQ]
cdktf-demo  aws_s3_bucket.s3-bucket: Creating...
cdktf-demo  aws_s3_bucket.s3-bucket: Creation complete after 2s [id=cdktf-demo-bucket-1-371le0b9d]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

No outputs found.
```

Quick commands:

| Action                    | Command         |
| ------------------------- | --------------- |
| Deploy stack              | `cdktf deploy`  |
| Synthesize Terraform JSON | `cdktf synth`   |
| Destroy stack             | `cdktf destroy` |

## Compatibility and migration

CDKTF is designed to fit into existing Terraform workflows and to simplify adoption:

* Use existing Terraform modules directly from CDKTF — reuse proven infrastructure code without rewriting.
* CDKTF synthesizes Terraform configuration (JSON) that remains compatible with Terraform engines and OpenTofu.
* Migration tools and community guides are available to help convert HCL/Terraform projects into CDKTF constructs when needed.

Useful links and references:

* CDK for Terraform (CDKTF): [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform Documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* OpenTofu: [https://opentofu.org](https://opentofu.org)
* Terraform Provider Registry: [https://registry.terraform.io](https://registry.terraform.io)

This concludes the introduction. We reviewed infrastructure and IaC basics, explored Terraform's strengths, and introduced CDKTF as a modern approach to infrastructure as code.

What's next?

A TypeScript crash course will cover the essential TypeScript concepts required to work effectively with CDKTF.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; listing four points: 01 Understanding infrastructure and IaC, 02 Exploring Terraform and its benefits, 03 CDKTF: A modern approach to IaC, and 04 What's next?. The left side has a turquoise gradient background and the items appear on the right with colorful numbered markers." />
</Frame>

and learn all the fundamental knowledge needed.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/9770c9dd-fb0f-4b73-bc7c-448dbfabaf13" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/5de68f68-7610-468f-b775-7a004cc48117" />
</CardGroup>
