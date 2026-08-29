# Deploying CloudFormation Templates

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/AWS-CloudFormation-Introduction/Deploying-CloudFormation-Templates/page

Overview of deploying AWS CloudFormation templates using console, CLI, and CI/CD with recommended practices and examples

In this lesson we cover the most common ways to deploy AWS CloudFormation templates (YAML or JSON). Whether you prefer a visual, manual workflow or a fully automated CI/CD pipeline, CloudFormation supports patterns for development, testing, and production deployments. Below we summarize the options, show concise CLI examples, and outline recommended practices for automation and permissions.

## Deployment approaches at a glance

* Manual (visual): AWS Management Console and Infrastructure Composer — good for exploration, quick edits, and one-off stack creation.
* CLI (scriptable): aws cloudformation deploy / create-stack / update-stack — ideal for reproducible deployments and automation scripts.
* CI/CD (fully automated): AWS CodePipeline or external CI systems — recommended for continuous delivery from version control.

## Manual methods (Console and Infrastructure Composer)

* AWS Management Console: Upload a CloudFormation template in the CloudFormation console and create a stack. The console guides you through selecting parameters, tags, and required capabilities, then provisions resources.
* Infrastructure Composer: Import a template to visually edit resources or build a template from scratch, then deploy it using CloudFormation.

Typical console/Composer flow:

1. Author or modify the template (YAML/JSON).
2. Upload the template or point CloudFormation to an S3 URL.
3. Create the stack and provide parameters, tags, and any required capabilities.
4. CloudFormation provisions the resources defined in the template.

## Automated methods (CLI)

Using the AWS CLI is fast, repeatable, and integrates into scripts and pipelines. Two common CLI patterns:

* High-level (recommended for many workflows): aws cloudformation deploy — handles create-or-update automatically and is simpler for typical use cases.
* Low-level explicit operations: aws cloudformation create-stack and aws cloudformation update-stack — use when you need explicit control.

Example: deploy a local template file using aws cloudformation deploy

```bash theme={null}
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-stack \
  --capabilities CAPABILITY_NAMED_IAM
```

Example: create a stack with parameters using aws cloudformation create-stack

```bash theme={null}
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=Environment,ParameterValue=production
```

Notes on CLI usage:

* aws cloudformation deploy performs create-or-update (idempotent behavior) and can simplify deployments when you track templates in version control.
* aws cloudformation create-stack explicitly creates a new stack; use aws cloudformation update-stack for existing stacks.
* When templates create or modify IAM resources (roles, policies), include capability flags such as CAPABILITY\_IAM or CAPABILITY\_NAMED\_IAM. If your template uses CloudFormation macros that expand at processing time, include CAPABILITY\_AUTO\_EXPAND.

<Callout icon="lightbulb">
  Always supply the correct CAPABILITY\_\* flags for templates that create or modify IAM resources. Also ensure the IAM principal running the CLI has permissions to create/update the resources referenced in your template.
</Callout>

## CI/CD with CodePipeline (recommended for automated delivery)

For continuous delivery, integrate CloudFormation with CodePipeline (or another CI/CD system). Typical pipeline pattern:

1. Store templates and application code in a source repo (CodeCommit, GitHub, etc.).
2. CodePipeline (or your CI system) detects changes and triggers the pipeline.
3. Optional build/test stages (CodeBuild, unit tests, integration tests).
4. A CloudFormation deploy action creates or updates stacks (can deploy nested stacks or change sets).

<Frame>
  <img alt="A slide titled &#x22;Deploying CloudFormation Templates&#x22; showing an automated method that integrates AWS CloudFormation with AWS CodePipeline. It depicts the two services connecting and automatically deploying CloudFormation templates." />
</Frame>

## Comparison table

| Method                  | Best for                                      | Key commands / examples                                       |
| ----------------------- | --------------------------------------------- | ------------------------------------------------------------- |
| Manual Console          | Visual editing, one-off stacks, demos         | Upload template in AWS CloudFormation Console                 |
| Infrastructure Composer | Visual authoring and iterative editing        | Export to template → deploy via Console/CLI                   |
| CLI (scriptable)        | Repeatable automation, local CI scripts       | `aws cloudformation deploy` / `create-stack` / `update-stack` |
| CI/CD (CodePipeline)    | Fully automated delivery from version control | Integrate CloudFormation action into pipeline stages          |

## Best practices

* Keep templates in version control (Git); treat templates as code.
* Parameterize environment-specific values and avoid hard-coding credentials.
* Use change sets or aws cloudformation deploy to preview changes for production stacks.
* Manage IAM privileges carefully: least-privilege for the principal that runs deployments.
* Use nested stacks or modular templates for large deployments to improve maintainability.

## Links and references

* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for multi-cloud orchestration patterns)

Summary

* Manual: Use the CloudFormation console or Infrastructure Composer for visual editing and ad-hoc stack creation.
* CLI: Use `aws cloudformation deploy`, `create-stack`, or `update-stack` for scripted, repeatable deployments.
* CI/CD: Use CodePipeline (or other CI systems) to automatically deploy CloudFormation templates from version control for continuous delivery.

These routes cover deployments from exploratory manual edits to fully automated CI/CD workflows—pick the pattern that fits your development lifecycle and governance needs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2ec6349c-f14b-48d2-8049-b313938d561e/lesson/57f917d7-0fb1-4aa3-a198-c4d098d765ee" />
</CardGroup>
