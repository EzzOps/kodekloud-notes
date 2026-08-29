# CDKTF Development Best Practices

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Conclusion/CDKTF-Development-Best-Practices/page

Practical best practices for CDK for Terraform covering when to import modules versus write constructs, incremental migration from Terraform, examples, design guidance, and learning resources

This final lesson summarizes practical best practices for CDK for Terraform (CDKTF). We'll revisit key concepts, show examples for when to import Terraform modules versus writing CDKTF constructs, outline an incremental migration workflow for existing Terraform projects, and point to further learning resources.

## Should you import a module or write a CDKTF construct?

There are three common approaches when implementing reusable infrastructure components:

* Reuse a published Terraform module from the Terraform Registry.
* Import a local Terraform module (from another repo or a local path).
* Re-implement the logic as a CDKTF construct in TypeScript (or your chosen language) using provider bindings.

Use the option that best matches your trade-offs: speed vs. customization vs. long-term maintainability.

<Callout icon="lightbulb">
  Tip: Start by importing modules to move quickly. When a component requires frequent changes or language-level abstractions, gradually rewrite it as a CDKTF construct.
</Callout>

## Example: S3 bucket implemented as a CDKTF construct

Below is a concise CDKTF construct example that creates an S3 bucket and tags it with an `env` tag. This TypeScript construct demonstrates a language-level abstraction you might prefer when you want a stable, reusable building block in your codebase.

```typescript theme={null}
// s3-bucket-with-env-tag.ts
import { Construct } from 'constructs';
import { s3Bucket } from '@cdktf/provider-aws';

interface S3BucketWithEnvTagProps {
  env: 'dev' | 'prod';
  name: string;
}

export class S3BucketWithEnvTag extends Construct {
  constructor(scope: Construct, id: string, { env, name }: S3BucketWithEnvTagProps) {
    super(scope, id);

    // Create the S3 bucket
    new s3Bucket.S3Bucket(this, 's3-bucket', {
      bucket: name,
      objectLockEnabled: true,
      tags: {
        env: env,
      },
    });
  }
}
```

You can either:

* Re-implement that logic as a CDKTF construct (above),
* Import a published Terraform module from the registry, or
* Import a local Terraform module.

## Import a local Terraform module using cdktf.json

To import a local module and have CDKTF generate bindings for it, add the module to your `cdktf.json` using a relative or absolute `source`. Example:

```json theme={null}
{
  "language": "typescript",
  "app": "npx ts-node main.ts",
  "projectId": "244e6594-8fee-4789-9b66-45ed8e1b1f28",
  "sendCrashReports": "false",
  "terraformProviders": [],
  "terraformModules": [
    {
      "name": "s3_bucket_with_env_tag",
      "source": "/root/code/tf/modules/s3_bucket_with_env_tag"
    }
  ],
  "context": {}
}
```

After updating `cdktf.json`:

```bash theme={null}
yarn install
yarn cdktf get
```

CDKTF will generate module bindings under `.gen`, allowing you to import and use the module like any construct.

## Using the generated module from TypeScript

Once generated, import the module and use it in your stack similarly to native constructs:

```typescript theme={null}
import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import { provider, s3Bucket } from '@cdktf/provider-aws';
import * as random from '@cdktf/provider-random';
import * as S3BucketWithEnvTag from './.gen/modules/modules/s3_bucket_with_env_tag';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Configure the random provider
    new random.provider.RandomProvider(this, 'random-provider');

    const randomId = new random.id.Id(this, 'random-id', {
      byteLength: 4,
    });

    // Create the S3 bucket (direct provider binding)
    new s3Bucket.S3Bucket(this, 's3-bucket', {
      bucket: `cdktf-demo-bucket-1-${randomId.hex}`,
      objectLockEnabled: true,
    });

    // Use the generated module construct
    new S3BucketWithEnvTag.S3BucketWithEnvTag(this, 's3-bucket-with-env-tag', {
      name: `cdktf-demo-bucket-2-${randomId.hex}`,
      env: 'dev',
    });
  }
}
```

## Decision guidance: import module vs write a construct

Use this table to choose the best approach for your component:

| Option                             |                                     Best for | When to prefer                                              |
| ---------------------------------- | -------------------------------------------: | ----------------------------------------------------------- |
| Import Terraform module (registry) |          Rapid delivery of stable components | The module exists, is well-maintained, and you need speed   |
| Import local Terraform module      |         Reuse shared infra code across repos | You already have tested modules within your org             |
| Write CDKTF construct              | Language-level APIs and fine-grained control | You want TypeScript abstractions or expect frequent changes |

## Using CDKTF in an existing Terraform project (incremental migration)

You can migrate existing Terraform projects into CDKTF incrementally. Typical workflow:

1. Create a new folder and initialize a CDKTF project.
2. Install the CDKTF CLI and run `cdktf init`, choosing "Start from an existing Terraform project" when prompted.

Example session (abbreviated):

```bash theme={null}
