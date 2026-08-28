# Metadata and Tags Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Metadata-and-Tags/Metadata-and-Tags-Introduction/page

Explains differences between CloudFormation Metadata and resource Tags, their uses, visibility, best practices, and examples for maintainers, automation, and operational governance.

Welcome to the lesson on Metadata and Tags in AWS CloudFormation. This guide clarifies what each concept is, how and when to use them, and the key differences that affect template authors, operators, and automation.

## What is Metadata in CloudFormation?

* Metadata stores additional information about the CloudFormation template or individual resources defined in the template.
* Think of Metadata as structured inline documentation or machine-readable notes inside the template that help maintainers and automation tooling.
* Common uses:
  * Documenting resource purpose, owner, or last review date
  * Adding operational notes for automation scripts
  * Recording template-level information (e.g., template version, authorship)
* Metadata is stored with the template and is not automatically applied to provisioned AWS resources (i.e., it does not appear in the AWS Console resource tag list).

Analogy: Metadata = a sticky note attached to a recipe (internal notes for maintainers and automation).

Example — resource-level Metadata and Tags in a CloudFormation template (YAML)

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Metadata:
      LastReviewed: "2024-03-01"
      Owner: "alice@example.com"
      Notes: "Used by analytics pipeline. Do not delete."
    Properties:
      BucketName: my-analytics-bucket
      Tags:
        - Key: Environment
          Value: Production
        - Key: Project
          Value: Analytics
        - Key: Owner
          Value: alice@example.com
```

<Callout icon="lightbulb">
  Use Metadata to document intent, ownership, and lifecycle information inside the template. Do not rely on Metadata for policies or access control — use tags, IAM, and other AWS features for that.
</Callout>

You can also add template-level Metadata (top of template) for things like template version or global author details:

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Metadata:
  TemplateVersion: '1.2.0'
  Author: 'platform-team@example.com'
Resources:
  ...
```

## What are Tags on AWS resources?

* Tags are key/value labels attached to the actual AWS resources when CloudFormation provisions them.
* Tags are visible in the AWS Management Console and are commonly used for:
  * Cost allocation and billing reports
  * Grouping and searching resources
  * Driving automation and some IAM policy conditions
* Typical tag keys: Name, Environment (Production/Dev/Test), Project, Owner.
* Tags are operational metadata — concise, visible, and often required for organizational governance.

<Frame>
  <img alt="A presentation slide titled &#x22;Tags – Introduction&#x22; showing a central &#x22;Resources&#x22; icon connected to multiple tag icons, illustrating that tags are labels attached to AWS resources. A use-case box notes developers tag resources by name, environment, project, etc." />
</Frame>

Analogy recap:

* Metadata = sticky note on the recipe (internal notes for maintainers).
* Tags = luggage tag on the bag (concise facts visible to handlers and useful at a glance).

<Callout icon="warning">
  Do not store secrets or sensitive information in Metadata or Tags. Metadata is intended for documentation/automation, and Tags may be visible across teams and in billing tools.
</Callout>

## Quick comparison

|                          Attribute |                       Metadata                       |                          Tags                          |
| ---------------------------------: | :--------------------------------------------------: | :----------------------------------------------------: |
|                       Stored where |          Inside the CloudFormation template          |            Attached to provisioned resources           |
|                         Visibility |            Template consumers, automation            |              AWS Console, billing, search              |
|                          Use cases | Documentation, automation hints, template-level info | Cost allocation, grouping, IAM conditions, ops tooling |
|                  Machine-readable? |            Yes (template-level JSON/YAML)            |                    Yes (API/console)                   |
|       Suitable for sensitive data? |                          No                          |                           No                           |
| Affects runtime resource behavior? |                          No                          |        Sometimes (e.g., IAM conditions use tags)       |

## Best practices

* Use Metadata for maintainability:
  * Include owner, review date, and purpose in Metadata to help future maintainers and automation.
  * Keep Metadata machine-friendly if automation will parse it (consistent keys, timestamps).
* Use Tags for operations and governance:
  * Enforce a tagging scheme (Name, Environment, Project, Owner) and apply tags consistently.
  * Use tags for cost allocation and to drive policy-based controls where appropriate.
* Never put secrets or credentials in either Metadata or Tags.

## Where to read more

* [AWS CloudFormation Metadata documentation](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [AWS Tagging strategies and best practices](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/)

Summary

* Metadata documents the template and resources for maintainers and automation (template-scoped).
* Tags label provisioned AWS resources for operations, billing, search, and policy-driven actions (console-visible and resource-attached).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2e1502d5-8cc7-4b67-a56a-6d65018f5458/lesson/a77b768d-cb52-4700-a534-902f8e8affab" />
</CardGroup>
