# Infrastructure as Code IaC Introduction

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Infrastructure-as-Code-IaC-Introduction/page

Introduction to Infrastructure as Code explaining benefits, history, and using tools like Terraform and CDK for Terraform with TypeScript for reproducible automated cloud infrastructure.

Infrastructure as code (IaC) lets you define, provision, and manage infrastructure using code instead of manual clicks in a cloud console. Tasks you would normally perform interactively in the AWS console — for example, creating an S3 bucket — become declarative or programmatic definitions stored in a codebase, making infrastructure repeatable, auditable, and automatable.

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Create bucket&#x22; page showing general configuration for a new bucket (AWS Region: Asia Pacific Singapore) with the bucket name field filled as &#x22;myawsbucket.&#x22; The lower section shows object ownership options and ACL settings." />
</Frame>

Why use IaC? Key benefits at a glance:

| Benefit                         | What it solves                                                                                  | Example                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Reproducibility and consistency | Eliminates configuration drift between environments by expressing desired state as code         | Deploy identical infrastructure to `development`, `staging`, and `production` |
| Automation and speed            | Removes manual, error-prone steps so environments can be created, updated, or destroyed quickly | Provision a complete test environment with a single command                   |
| Versioning and collaboration    | Lets teams review, track, and roll back infrastructure changes using source control and CI/CD   | Store Terraform/TypeScript IaC in Git and use PRs for change reviews          |

> **lightbulb** Best practice: keep IaC in version control (e.g., Git), run automated tests, and deploy changes through CI/CD pipelines to ensure safe, auditable infrastructure changes.

<Frame>
  <img alt="A presentation slide titled &#x22;IaC – Benefits&#x22; showing two colored cards: &#x22;01 Reproducibility and consistency&#x22; (orange) and &#x22;02 Automation and speed&#x22; (green). The slide is branded © Copyright KodeKloud." />
</Frame>

A brief history of infrastructure management

| Period    | Phase                                 | Summary                                                                                                                                          |
| --------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2000s     | Manual server management              | Early teams provisioned servers and configured software by hand — a slow, error-prone process                                                    |
| Mid-2000s | Configuration management              | Tools like Puppet and Chef automated server configuration and state management                                                                   |
| 2014      | Declarative IaC                       | Terraform introduced HCL and a declarative model focused on the desired end state (the "what")                                                   |
| 2015+     | Cloud-native templates                | Provider-specific declarative formats (CloudFormation, ARM, Deployment Manager) standardized cloud templates                                     |
| 2019      | Modern IaC with programming languages | Tools such as Pulumi and CDK for Terraform (CDKTF) enabled IaC using general-purpose languages like TypeScript for greater reuse and testability |

<Frame>
  <img alt="A timeline slide titled &#x22;Infrastructure Management – Evolution&#x22; showing milestones from 2000 to 2019. It highlights stages like Manual Server Management, Configuration Management tools, the rise of declarative IaC (Terraform, 2014), cloud-native IaC (CloudFormation, 2015), and modern IaC with programming languages (AWS CDK, Pulumi, 2019)." />
</Frame>

Next steps

In the next lesson/article we'll begin practical, hands-on work with infrastructure as code using [CDK for Terraform with TypeScript](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript). You’ll learn core concepts, see examples that compile to Terraform, and build reusable, testable constructs with TypeScript.

Links and references

* [CDK for Terraform (CDKTF) — KodeKloud course](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript)
* [Terraform documentation](https://www.terraform.io/docs)
* [Pulumi documentation](https://www.pulumi.com/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/b927df18-8e80-43a6-98d4-86ca71adacd8)
