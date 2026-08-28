# Resource Imports Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CFN-init-and-Resource-Imports/Resource-Imports-Overview/page

How to import existing AWS resources into CloudFormation stacks to manage them without recreating them.

This guide explains how to import existing AWS resources into an AWS CloudFormation stack so you can manage them with CloudFormation without recreating them. Resource imports let you adopt resources that were created outside of CloudFormation and bring them under stack management so future updates and lifecycle changes are handled by CloudFormation.

<Frame>
  <img alt="A slide titled &#x22;Resource Imports – Overview&#x22; showing an icon for Resource Imports and AWS resource icons (server, S3 bucket, database) being imported into an AWS CloudFormation stack. The caption explains this lets you manage and update resources that were created outside CloudFormation using the stack's template." />
</Frame>

Overview

Resource imports require you to explicitly declare the existing resource(s) in your stack template, provide the correct physical identifiers during the import operation, and then execute a change set that adopts the resources into the stack. The import process does not replace or recreate the physical resource — CloudFormation takes ownership of the existing resource and begins managing it.

High-level import flow

1. Identify the resource(s) you want to adopt into CloudFormation (for example, an S3 bucket, RDS instance, or EC2 instance).
2. Update your CloudFormation template to include a resource declaration with the correct AWS::ResourceType and any properties CloudFormation requires for import.
3. Create a change set (or use the CloudFormation console import workflow) and map each template resource to the existing physical resource by providing its identifier (for example, an S3 bucket name or an RDS DBInstanceIdentifier).
4. Execute the change set to complete the import. CloudFormation will adopt the resources into the stack without replacing them.

<Callout icon="lightbulb">
  When preparing your template, ensure each resource's logical ID and resource type match what you intend to manage, and include all properties CloudFormation requires to track the resource after import (for example, a bucket’s name or an RDS instance identifier).
</Callout>

Common example templates

Below are minimal YAML snippets that illustrate how to declare resources for import. These templates include the properties you must supply so CloudFormation can map the template resource to the existing physical resource.

S3 bucket example (YAML):

```yaml theme={null}
Resources:
  ExistingBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-existing-bucket-name
```

RDS DB instance example (YAML):

```yaml theme={null}
Resources:
  ExistingDB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: my-existing-db-identifier
      AllocatedStorage: 20
      DBInstanceClass: db.t3.medium
      Engine: mysql
```

Important constraints and considerations

| Constraint / Consideration                    | Explanation                                                                                                                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Physical ID cannot change during import       | CloudFormation adopts the existing resource as-is; you cannot assign a new physical ID in the same import.                                                         |
| Only importable resource types and properties | Not all AWS resource types or individual properties are supported for import. Check resource-level import support in the AWS docs.                                 |
| Accurate identifiers required                 | If the identifier you provide doesn’t match the existing resource, the import operation fails.                                                                     |
| Post-import management via CloudFormation     | After importing, make updates to the resource through CloudFormation to avoid drift; direct changes to the underlying resource may create drift and complications. |
| Precondition checks and constraints           | Some resources have additional preconditions (encryption, tags, or configuration) that must match the template to import successfully.                             |

<Callout icon="warning">
  Test imports in a non-production environment before importing production resources. Incorrect templates, missing required properties, or mismatched identifiers can cause import failures that require manual remediation.
</Callout>

Best practices and tips

* Validate templates before creating a change set. Use the CloudFormation template linter and the `aws cloudformation validate-template` API.
* Confirm the required importable properties for your resource type in the CloudFormation documentation:
  * [AWS CloudFormation Importing Resources](https://docs.aws.amazon.[SECRET_REDACTED]-import.html)
  * Resource-specific docs (e.g., [AWS::S3::Bucket](https://docs.aws.amazon.[SECRET_REDACTED]-properties-s3-bucket.html))
* Use change sets to preview the import and confirm that only the adoption occurs (no unintended replacements).
* If a resource is in use by other systems, schedule imports during a maintenance window to reduce risk.

References

* AWS CloudFormation import resources guide: [https://docs.aws.amazon.[SECRET_REDACTED]-import.html](https://docs.aws.amazon.[SECRET_REDACTED]-import.html)
* AWS CloudFormation User Guide: [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)

The following sections contain concrete, step-by-step examples and walkthroughs for typical imports (S3, RDS, EC2) so you can safely adopt resources into CloudFormation-managed stacks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/026ceaf9-07b6-4964-b49d-7190c136ea2b/lesson/9f30e4ee-6ece-4c48-9846-bcd6d451e481" />
</CardGroup>
