# Whats New for 2025

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Wrap-Up/Whats-New-for-2025/page

Overview of Amazon SageMaker changes in 2025, detailing the split into SageMaker AI and SageMaker platform, Unified Studio, Projects, Spaces, governance, lakehouse and analytics integration

In this lesson we cover the major changes to Amazon SageMaker in 2025 and how the product split that started in late 2024 affects model development, data workflows, and governance.

At the end of 2024 AWS split the historical SageMaker product into two related offerings:

* SageMaker AI — the traditional product focused on model development, training, and deployment (this article concentrates on this product and its continuity).
* SageMaker platform — the broader platform now presented in the AWS Management Console simply as “SageMaker.” It extends SageMaker AI with data management, governance, SQL analytics, and integrated analytics/Bedrock access.

Because the naming changed, be explicit which product you mean:

* “SageMaker AI” = the model-focused product for building, training, and deploying models.
* “SageMaker” or “SageMaker platform” = the new, broader platform that includes SageMaker AI plus lakehouse, governance, and analytics features.

> **warning** The SageMaker platform is in technical preview at the time of this article. Rely on the [official AWS documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/) as the single source of truth for feature availability and behavior.

## Quick comparison: SageMaker AI vs SageMaker platform

Use the table below for a compact comparison of each product’s focus and when to choose one over the other.

|            Product | Focus                                                                                                      | When to choose                                                                                                                                      |
| -----------------: | :--------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
|       SageMaker AI | Model building, training, and deployment (historical SageMaker)                                            | You need full control of training code, CI/CD (SageMaker Projects, Pipelines), customized models, or fine-grained model ops.                        |
| SageMaker platform | End-to-end data + AI workflows: model building + lakehouse, governance, SQL analytics, Bedrock integration | You need integrated data discovery, governance, auditability, SQL-driven analytics, or managed collaboration across data engineers and MLOps teams. |

<Frame>
  <img alt="A slide titled &#x22;SageMaker AI vs SageMaker Platform&#x22; comparing SageMaker AI (left) which focuses on building, training, and deploying ML models. The right column lists the SageMaker Platform (2025) features — end-to-end AI workflows and included components like SageMaker AI, Lakehouse, Data & AI Governance, SQL Analytics, Unified Studio, and Bedrock integration." />
</Frame>

High-level summary:

* SageMaker AI remains the core model development and deployment environment.
* SageMaker platform is a superset that adds lakehouse metadata, governance, SQL analytics, and direct generative-AI (Bedrock) integrations.

## When to use each product

* Use SageMaker AI when your primary needs are model customization, experiments, training, and deployment with fine-grained control.
* Use the SageMaker platform when you require end-to-end workflows tightly integrated with data sources (data lakes, warehouses), governance, analytics, or collaborative workspaces.

<Frame>
  <img alt="A slide titled &#x22;When to Use SageMaker Platform?&#x22; that lists three reasons: for end-to-end data and AI workflows beyond model deployment; when integrating with data lakes, warehouses, and AWS tools; and when data governance, SQL analytics, or generative AI are required." />
</Frame>

Key platform differences:

* Tighter connectivity to Athena, Glue, and Redshift.
* Built-in data and AI governance (auditability, lineage).
* SQL-driven analytics and metadata discovery inside the project lifecycle.

## Getting started with the SageMaker platform: Unified Studio

To adopt the SageMaker platform you create a Unified Studio domain. The console will prompt you to create either:

* an Amazon SageMaker Unified Studio domain, or
* an Amazon DataZone domain.

<Frame>
  <img alt="A slide titled &#x22;Unified Studio&#x22; with the step &#x22;Create a Unified Studio Domain.&#x22; In the center is a panel offering two options — create an Amazon SageMaker Unified Studio domain or create an Amazon DataZone domain — each with orange call-to-action buttons." />
</Frame>

During domain creation you can choose Quick setup or Manual setup. Quick setup is useful for evaluation and short demos; Manual setup is recommended for production to configure organization-wide options such as IAM Identity Center SSO and multi-account support.

<Frame>
  <img alt="A slide titled &#x22;Unified Studio&#x22; showing step 3 with a screenshot of the AWS &#x22;Create domain&#x22; page where you choose between a quick setup (defaults) or a manual setup (custom values) for Amazon SageMaker Unified Studio. The screenshot lists capabilities like data analytics, machine learning, generative AI, and authentication options." />
</Frame>

After creation, open Unified Studio from the domain details to begin creating Projects.

<Frame>
  <img alt="A presentation slide titled &#x22;Unified Studio&#x22; showing a screenshot of an Amazon SageMaker Unified Studio domain details page with green success banners and an &#x22;Open unified studio&#x22; button. The slide instructs the user to click &#x22;Open Unified Studio&#x22; to explore the new UI." />
</Frame>

> **lightbulb** Projects and Spaces are the primary collaboration constructs in Unified Studio. Projects group resources and governance settings; Spaces provide managed compute sessions (JupyterLab) for teams.

## Projects — collaboration and toolchain integration

A Project groups all resources for an initiative: compute, repository links, lakehouse artifacts, governance settings, and CI/CD connections. Projects are designed as the collaboration unit for data engineers, data scientists, and MLOps.

When creating a Project you specify:

* Project name
* Tooling and connections — including a CodeStar connection to your Git provider (GitHub, Bitbucket, CodeCommit, etc.). Note: the CodeStar connection must exist before you select it in the Project form.

<Frame>
  <img alt="A dark-themed &#x22;Create Project&#x22; UI screen showing Step 3: &#x22;Customize parameters&#x22; with a &#x22;Tooling&#x22; form containing fields like connection name (default-connection), provider (CodeCommit), branch &#x22;main&#x22;, retention 731 and max EBS 100. The form is displayed inside a rounded, highlighted panel on a teal background." />
</Frame>

Project configuration also includes observability (CloudWatch retention), EBS sizes for managed compute, and optional lakehouse settings (Glue DB and Athena workgroup). SageMaker will create and manage lakehouse metadata tables stored in S3 and queryable via Athena.

You can also configure Redshift Serverless workgroups when you need data-warehouse capabilities.

<Frame>
  <img alt="A dark-themed &#x22;Create Project&#x22; UI modal showing sections to configure a Lakehouse Database and a Redshift Serverless workgroup. The form has input fields prefilled with names like &#x22;glue_db&#x22;, &#x22;workgroup&#x22;, and &#x22;dev&#x22;." />
</Frame>

## Spaces — managed compute for collaboration

Inside a Project you create Spaces. Spaces are managed compute environments (often JupyterLab) that host user sessions and interactive applications. Typical Space settings include:

* Instance size (e.g., ml.t3.medium)
* Container image (SageMaker Distribution image or a custom image)
* EBS storage and lifecycle configuration
* Idle timeout and privacy (private or shared)

<Frame>
  <img alt="A dark-themed screenshot titled &#x22;Spaces&#x22; showing a configuration panel for creating an Amazon EC2/SageMaker space. It lists settings like instance type (ml.t3.medium), image (SageMaker Distribution 2.2), EBS storage (16 GB), lifecycle config, idle time, and filesystem attachment." />
</Frame>

When you open a provisioned Space you’ll see a familiar JupyterLab interface that includes top-level project controls (Discover, Build, Govern) for accessing data, analytics, and governance workflows.

<Frame>
  <img alt="A dark-themed screenshot of the Jupyter interface (JupyterLab) showing a launcher with options for Notebook, Console, Terminal, and various file types. The header reads &#x22;Jupyter Interface&#x22; with the subtext &#x22;Access to integrated tools for data management and workflow orchestration.&#x22;" />
</Frame>

## Compatibility: existing SageMaker AI notebooks and SDKs

The SageMaker platform extends—not replaces—SageMaker AI. Your existing notebooks and SageMaker SDK code should continue to run as before. Typical imports remain the same:

```python theme={null}
import boto3
import sagemaker
```

You may see standard SDK informational logs on startup, for example:

```text theme={null}
sagemaker.config INFO - Not applying SDK defaults from location: /etc/xdg/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /home/sagemaker-user/.config/sagemaker/config.yaml
```

## Practical checklist: adopt the SageMaker platform (recommended approach)

* Decide if you need end-to-end data + AI workflows, governance, or SQL analytics. If so, use the SageMaker platform.
* Create a Unified Studio domain (manual setup for production).
* Pre-create any CodeStar connections to integrate your Git provider with Projects.
* Configure Project lakehouse settings (Glue DB, Athena workgroup) and observability options.
* Provision Spaces with appropriate instance types and images, and choose shared vs private depending on collaboration needs.
* Validate that existing SageMaker AI notebooks and SDK workflows run unchanged inside the new Unified Studio Spaces.

## Summary

* AWS split SageMaker into two offerings: SageMaker AI (model-focused) and the SageMaker platform (broader, console-facing “SageMaker”).
* SageMaker platform is a superset that adds lakehouse metadata, governance, SQL analytics, and tight data-source integration.
* To use the SageMaker platform create a Unified Studio domain, then create Projects (resource + governance containers) and Spaces (managed compute sessions).
* Existing SageMaker AI notebooks and SDK calls continue to work in the SageMaker platform; the platform adds integrated data governance and analytics to support end-to-end workflows.

For the most current, region-specific details and to verify preview vs GA features, always consult the official AWS documentation:

* [Amazon SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b8b80e38-7fae-401c-a5ff-d6f0af493cea/lesson/0bc8e755-4a98-4116-872c-c8beb8d397d3)
