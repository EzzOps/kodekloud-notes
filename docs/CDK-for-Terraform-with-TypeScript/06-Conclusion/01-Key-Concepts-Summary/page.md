# create a project folder and initialize
mkdir cdktf2
cd cdktf2

# install the CDKTF CLI if not installed
npm i -g cdktf-cli

# initialize a new TypeScript CDKTF project
cdktf init
# follow interactive prompts:
# - Terraform Cloud State Management? No
# - Template? TypeScript
# - Project name? cdktf2
# - Start from existing Terraform project? Yes
# - Enter the path to the existing Terraform project
# - Select providers used in the project (e.g., aws, random)
```

CDKTF will scan your Terraform configuration, import providers/modules, and generate TypeScript code. Expect to clean up a few items: duplicate imports, missing provider declarations, and any provider-specific nuances.

> **warning** The conversion tool is a strong starting point but not a full one-click migration. For larger projects, plan time to resolve generated import issues and to refactor modules into idiomatic CDKTF constructs where needed.

### Example generated TypeScript (from conversion)

A converted `main.ts` may include generated provider and module bindings like this:

```typescript theme={null}
import { Construct } from 'constructs';
import { App, LocalBackend, TerraformStack } from 'cdktf';
import { AwsProvider } from './.gen/providers/aws/provider';
import { S3Bucket } from './.gen/providers/aws/s3-bucket';
import { Id } from './.gen/providers/random/id';
import * as S3BucketWithEnvTag from './.gen/modules/modules/s3_bucket_with_env_tag';
import { RandomProvider } from '@cdktf/provider-random/lib/provider';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new LocalBackend(this, {
      path: 'terraform.tfstate',
    });

    new AwsProvider(this, 'aws', {
      region: 'us-east-1',
    });

    new RandomProvider(this, 'random');

    const bucketId = new Id(this, 'bucket_id', {
      byteLength: 4,
    });

    new S3BucketWithEnvTag.S3BucketWithEnvTag(this, 's3_bucket', {
      env: 'dev',
      name: `tf-demo-bucket-2-${bucketId.hex}`,
    });

    new S3Bucket(this, 'tf-demo-bucket-1', {
      bucket: `tf-demo-bucket-1-${bucketId.hex}`,
      objectLockEnabled: true,
    });
  }
}
```

After adjustments:

```bash theme={null}
# install dependencies
yarn install

# synth / deploy
yarn cdktf synth
yarn cdktf deploy
```

## Design guidance: constructs and stacks

* Constructs
  * Encapsulate a single responsibility (e.g., "S3 bucket with logging" or "API with backend Lambda").
  * Keep public props minimal and stable.
  * Group resources by deployment/ownership and dependency boundaries.
  * Avoid embedding business logic that changes frequently into a low-level construct.

* Stacks
  * A stack should represent a deployable business unit (for example: API, frontend, database tier).
  * Deploy stacks independently when you need separate lifecycle, teams, or scaling.
  * Design stacks to match your deployment and ownership boundaries.

## Further learning and resources

* CDKTF docs — Language-specific guidance and examples: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform Registry — Reusable Terraform modules: [https://registry.terraform.io/](https://registry.terraform.io/)
* CDKTF community discussions and forum posts — practical patterns and troubleshooting

<Frame>
  <img alt="A webpage showing the &#x22;CDK for Terraform&#x22; documentation with a site navigation sidebar and content about the Cloud Development Kit. A privacy settings/cookie consent pop-up is overlaid on the left side of the screen." />
</Frame>

Other recommended resources:

* [CDKTF documentation](https://developer.hashicorp.com/terraform/cdktf) (TypeScript examples included)
* Community forums and GitHub discussions for real-world patterns
* Build hands-on projects — practical experience is the best teacher

## Summary

* Use imported Terraform modules to move quickly for stable, well-maintained components.
* Prefer CDKTF constructs when you need TypeScript-first abstractions or expect frequent changes.
* Use the CDKTF conversion tooling to speed migration from Terraform, then incrementally refactor generated code.
* Design constructs to have a single responsibility and design stacks around deployable business functionality.

Thank you — I hope this lesson clarified CDKTF best practices and helps you build maintainable Infrastructure as Code.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/14cadb71-0522-4f61-8015-24e11e133123/lesson/a18b319f-7dd6-4f80-9422-84d000d2f78a)


# Key Concepts Summary

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Conclusion/Key-Concepts-Summary/page

Final course recap on using TypeScript with CDK for Terraform to build reusable, maintainable AWS infrastructure as code, covering projects, constructs, state management, and best practices.

This final module pulls together the core ideas from the course and describes practical strategies for turning those ideas into a maintainable, reusable infrastructure-as-code (IaC) codebase. Below is a concise, well-structured recap of what we covered and guidance for applying it in real projects.

## Course recap — what we covered

We started with fundamentals of infrastructure and Infrastructure as Code (IaC), then introduced CDK for Terraform (CDKTF) and the benefits it brings:

* Use familiar programming constructs (TypeScript) to generate Terraform configuration.
* Improve maintainability, testability, and reusability of infrastructure code.
* Leverage Terraform providers and the Terraform ecosystem while using higher-level abstractions.

Then we completed three hands-on projects that built on each other.

* Project 1 — TypeScript fundamentals: variables, types, classes, literals, functions, and other core language features.

<Frame>
  <img alt="A recap slide showing TypeScript concepts on the left, Terraform in the middle, and AWS infrastructure components on the right. It visually maps TypeScript → Terraform → AWS services like S3, Lambda, DynamoDB and API Gateway." />
</Frame>

* Project 2 — CDKTF basics: create a local CDKTF project, synthesize Terraform configuration with the CDKTF CLI, and explore stacks, outputs, and the CDKTF construct model.
* Project 3 — Real AWS deployments: provisioned S3, API Gateway, DynamoDB, Lambda, and IAM. The final deliverable was a reusable, deployable API that returns a random name from a configurable list.

## What you have achieved

* Understand core IaC concepts and why CDKTF is a strong choice for teams using TypeScript.
* Apply TypeScript to bring structure and type safety to your infrastructure code.
* Learn CDKTF fundamentals for synthesizing Terraform and organizing infrastructure with constructs and stacks.
* Build and deploy real-world AWS infrastructure (Lambda, IAM, S3, API Gateway, DynamoDB).
* Organize code using constructs and follow best practices for reusability and maintainability.

<Frame>
  <img alt="A vertical four-step timeline titled &#x22;What you have achieved&#x22; showing learning milestones. It lists goals like understanding IaC and CDKTF, learning TypeScript and CDKTF fundamentals, and building/deploying real-world infrastructure with brief bullet points." />
</Frame>

## Quick project summary (at-a-glance)

| Project   | Focus                   | Outcome                                                                            |
| --------- | ----------------------- | ---------------------------------------------------------------------------------- |
| Project 1 | TypeScript fundamentals | Solid grounding in TypeScript syntax and patterns used to author CDKTF constructs  |
| Project 2 | CDKTF & local stacks    | Local CDKTF project, synthesis to Terraform, stacks, outputs, and CLI workflows    |
| Project 3 | AWS resource deployment | Reusable infra: S3, Lambda, API Gateway, DynamoDB, IAM — end-to-end deployable API |

## Putting it all together — the tower analogy

Think of your infrastructure codebase as a tower of bricks. Each layer is a level of abstraction and responsibility. When adding new functionality, ask if it should be a new brick (separate module/construct) or part of an existing one.

Layers (from foundation to top):

| Layer            | Purpose                                   | Examples                                                             |
| ---------------- | ----------------------------------------- | -------------------------------------------------------------------- |
| Foundation       | Providers and state backend configuration | Provider blocks, backend (S3/DynamoDB locking), remote state         |
| Reused modules   | Stable, shared building blocks            | Modules from the `Terraform Registry` or organization-shared modules |
| Constructs       | Reusable CDKTF constructs you author      | High-level components that compose providers and modules             |
| Stacks & outputs | Final deployable units                    | Per-environment stacks, outputs such as API URLs and ARNs            |

When deciding to split functionality, evaluate:

* Who will use the component?
* How will they use it (API/props and expected defaults)?
* What should be the default behavior vs. what should be overridable?

Design constructs with sensible defaults (for quick onboarding) but allow clear overrides (for flexibility). For example, our Lambda construct created a role and reasonable defaults, while letting callers override runtime settings such as timeout or memory.

> **lightbulb** Design constructs with clear defaults and override points: defaults help users get started quickly; configurable properties make the construct reusable across teams and environments.

## Practical design guidelines and best practices

* Prefer existing, reliable modules when they meet your needs — don’t rebuild what already works. See the Terraform Registry for vetted modules.
* Build custom constructs when requirements are unique or when you need organization-specific conventions.
* Define clear input/output contracts for constructs to make composition predictable.
* Keep stacks thin: a stack should represent a deployable unit (e.g., one environment or service).
* Use environment-aware configuration (workspaces, per-environment variables, or parameterized stacks) to avoid duplication.
* Version and document your constructs so teams can adopt them without guessing defaults.

## Checklist — deciding to create a new construct or module

* Will more than one team or project reuse this functionality?
* Does the functionality represent a coherent unit of infrastructure (e.g., “serverless API” or “shared networking”)?
* Can you design a simple, stable API for configuration and sensible defaults?
  If you answered yes to these, a reusable construct/module is justified.

## State, backends, and collaboration — important considerations

> **warning** Always plan your state and backend strategy before collaborating. Remote state, locking, and consistent provider configuration are essential for team workflows and safe deployments.

Key recommendations:

* Use a remote backend (S3 + DynamoDB locking for AWS) in team environments.
* Keep provider and backend configuration in a stable foundation layer to avoid accidental drift.
* Use CI/CD to run synth and apply workflows consistently; restrict who can apply production changes.

## Recommended next steps

* Continue practicing by extracting a construct from an existing stack and publishing it internally.
* Explore the Terraform Registry for modules you can adopt or adapt.
* Start a small catalog of organization-approved constructs with documentation and examples.
* Automate synthesis (CDKTF) and Terraform applies via CI/CD to standardize deployments.
* Read the CDKTF docs and Terraform provider docs to deepen provider-specific knowledge:
  * CDKTF: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
  * Terraform core: [https://www.terraform.io](https://www.terraform.io)
  * Terraform Registry: [https://registry.terraform.io](https://registry.terraform.io)
  * TypeScript: [https://www.typescriptlang.org](https://www.typescriptlang.org)

## Summary

We revisited the course’s core concepts and provided practical strategies to apply them: design reusable constructs, prefer proven modules, and plan state/backends for collaboration. These practices will help you scale infrastructure code across teams and projects while preserving clarity, safety, and reusability.

The final module will provide suggested next steps and resources to continue your IaC journey.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/14cadb71-0522-4f61-8015-24e11e133123/lesson/fee657ac-eddb-419d-b057-9f2ebb6446c4)
