# Demo Accessing documentation on CloudFormation

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/AWS-CloudFormation-Introduction/Demo-Accessing-documentation-on-CloudFormation/page

Guide to finding and using official AWS CloudFormation documentation, including resource references, examples, CLI and API details, and bookmarking tips for template development.

Welcome to this demo focused on finding and using the official AWS CloudFormation documentation. When learning and building CloudFormation templates, keeping the authoritative docs bookmarked gives you a reliable, up-to-date reference for resource specifications, examples, CLI/API details, and troubleshooting.

This lesson references the KodeKloud course: [https://learn.kodekloud.com/user/courses/aws-cloud-formation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

## Why use the official documentation?

* It’s the canonical source for resource types, properties, and constraints.
* Example templates and best practices help you design robust stacks.
* CLI and API references show exact parameters and response formats.
* Regular updates reflect new AWS features and resource types.

## How to get to the documentation — quick steps

1. Open your web browser and search for "AWS CloudFormation documentation".
2. Select the official AWS result, which points to the AWS CloudFormation User Guide.
   * Canonical landing page: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
3. Bookmark the landing page and the Resource and Property Reference page for quick access during hands‑on work.

> **lightbulb** Bookmark the CloudFormation User Guide ([https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)) and the Resource Reference page — they will be the most frequently used references throughout this lesson.

## What you’ll find on the CloudFormation docs

|                         Resource | Use case                                                               | Where to look                         |
| -------------------------------: | ---------------------------------------------------------------------- | ------------------------------------- |
|                       User Guide | Conceptual overviews, tutorials, walkthroughs, authoring help          | CloudFormation User Guide             |
|  Resource and property reference | Exact property names, types, required/optional flags, update behavior  | Resource and Property Reference       |
|              CLI / API reference | `create-stack`, `update-stack`, API operations, parameters, pagination | AWS CLI and API docs                  |
|      Examples & sample templates | Ready-to-use templates and patterns to adapt                           | Examples section and GitHub repos     |
| Best practices & troubleshooting | Stack design, rollback behavior, drift detection, error resolution     | Best practices, Troubleshooting pages |

## Quick search tips (save time)

* Use the docs site search for direct queries like:
  * AWS::S3::Bucket
  * AWS::Lambda::Function environment variables
* Use search engine operators to jump straight to resource references:
  * site:docs.aws.amazon.com "AWS::S3::Bucket"
  * site:docs.aws.amazon.com "AWS::CloudFormation" "resource types"
* Add "examples" or "template" to your query to find sample templates quickly:
  * site:docs.aws.amazon.com "AWS::EC2::Instance" examples

## Useful links and references

* AWS CloudFormation User Guide — [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
* Resource and Property Reference — [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
* AWS CLI Reference for CloudFormation — [https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html)
* CloudFormation sample templates (AWS GitHub) — [https://github.com/awslabs/aws-cloudformation-templates](https://github.com/awslabs/aws-cloudformation-templates)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for container orchestration context)
* KodeKloud CloudFormation course — [https://learn.kodekloud.com/user/courses/aws-cloud-formation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

Follow these steps and bookmarks as you progress through the course—keeping the official documentation at hand will speed up development, reduce errors, and help you adopt best practices when authoring CloudFormation templates.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2ec6349c-f14b-48d2-8049-b313938d561e/lesson/13ff05ae-9895-4545-b3aa-8ec573c81eb2)
