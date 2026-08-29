# Run inside a JupyterLab terminal to inspect storage backing
df -h

# Example: EFS (Studio Classic)
# Filesystem         Size  Used Avail Use% Mounted on
# Example: EBS (Studio new)
# Filesystem        Size  Used Avail Use% Mounted on
# /dev/nvme1n1       50G   5G   45G   10% /home/sagemaker-user
```

If you see an EFS mount (efs-xxxx:/), the space uses Studio Classic storage. If you see an NVMe device such as /dev/nvme1n1, the space uses EBS (Studio new).

When launching a JupyterLab space as a different user, spaces may be private or shared. Private spaces created by another user will not appear for user2; only spaces explicitly shared or created for user2 will be visible.

<Frame>
  <img alt="A dark-themed screenshot of the &#x22;Workflow: Launching JupyterLab&#x22; screen in SageMaker Studio showing the JupyterLab dashboard. It shows a running JupyterLab space, sidebar app icons (JupyterLab, RStudio, Canvas, etc.), and action buttons like Stop and Open." />
</Frame>

Open the space to begin using notebooks and other Studio apps as usual.

<Frame>
  <img alt="A screenshot of the JupyterLab interface titled &#x22;Workflow: Launching JupyterLab,&#x22; showing a file browser on the left and a launcher on the right with notebook and console kernel tiles (Python 3, Glue PySpark, SparkMagic, etc.)." />
</Frame>

If you created the profile as SageMaker Studio Classic, UI customization options are limited. Notebook sharing must be explicitly enabled and requires a specific S3 share location. Example S3 path used for Classic notebook sharing:

s3://sagemaker-studio-485186561655-ocndvxhvpI9/sharing

This S3-based sharing step applies only to Studio Classic — Studio (new) does not require it.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: User Profile Classic&#x22; showing an Amazon SageMaker &#x22;Add user profile&#x22; configuration screen. The screenshot highlights choosing &#x22;SageMaker Studio Classic&#x22; as the default Studio application and shows JupyterLab idle-shutdown options." />
</Frame>

When Studio Classic is selected, UI customization toggles are hidden.

<Frame>
  <img alt="A screenshot of an &#x22;Add user profile&#x22; workflow for Amazon SageMaker titled &#x22;Workflow: User Profile Classic.&#x22; The page shows the &#x22;Customize Studio UI&#x22; step with a yellow warning saying customization isn't available for SageMaker Studio Classic, plus left-side step navigation and Back/Next buttons." />
</Frame>

Recommendation: Prefer SageMaker Studio (new) unless you have a legacy requirement. Studio (new) offers productivity, resource, MLOps, and security advantages:

1. Streamlined development & collaboration

* JupyterLab-based IDE.
* Shared spaces for real-time collaboration.
* Notebook sharing (link-based or via Git).
* SageMaker Experiments for logging and comparing runs.

<Frame>
  <img alt="A presentation slide titled &#x22;Result: SageMaker Studio – Enhanced ML Productivity&#x22; showing four numbered feature cards. The cards list JupyterLab-Based IDE, Shared Spaces, Notebook Sharing, and Experiment Tracking with short descriptions." />
</Frame>

2. Better resource and compute management

* On-demand kernel selection across tabs.
* Auto-shutdown and resource scaling to save costs.
* EBS storage in Studio (new) for lower latency and higher throughput vs EFS.

<Frame>
  <img alt="A presentation slide titled &#x22;Result: SageMaker Studio – Enhanced ML Productivity&#x22; showing the section &#x22;2. Better Resource and Compute Management&#x22; with three feature cards: On‑Demand Kernel Selection, Auto‑Shutdown & Resource Scaling, and EBS Storage (instead of EFS). The cards include brief explanations about switching kernels without restarting, cost‑saving auto‑stop/scaling, and faster isolated storage." />
</Frame>

3. Improved MLOps and automation

* SageMaker Pipelines to orchestrate ML workflows.
* Integrated Git support for loading repos into Studio.
* SageMaker Debugger and Model Monitor for production debugging and observability.
* Streamlined deployment to SageMaker endpoints.

<Frame>
  <img alt="A presentation slide titled &#x22;Result: SageMaker Studio – Enhanced ML Productivity&#x22; showing four feature cards under &#x22;3. Improved MLOps and Automation.&#x22; The cards list SageMaker Pipelines (automate ML lifecycle), Integrated Git Support, Debugging and Monitoring, and Easier Deployment to SageMaker Endpoints." />
</Frame>

4. Security and governance improvements

* Fine-grained IAM controls for Studio features.
* VPC and network isolation options for managed instances.
* Better auditability via CloudTrail and CloudWatch for jobs, endpoints, and provisioning.

<Frame>
  <img alt="A presentation slide titled &#x22;Result: SageMaker Studio – Enhanced ML Productivity&#x22; under the heading &#x22;4. Security and Governance Improvements.&#x22; It shows three cards describing IAM role‑based access control, network isolation, and auditability/logging (integrated with CloudTrail and CloudWatch)." />
</Frame>

Many newer SageMaker features (Model Monitor, Feature Store, Model Registry, Debugger, Canvas, Pipelines) are accessible only from Studio (new).

You must create a SageMaker Domain before launching Studio. Domains are the administrative boundary: within a domain you define users, applications, storage, and networking. Quick start domains are convenient for learning but not recommended for production since they use the default VPC. For production, create domains integrated with IAM/Identity Center and a custom VPC.

Studio is more than notebooks — it hosts multiple apps such as Code Editor/VS Code, RStudio, MLflow integrations, third-party SaaS tools, and more.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists four key points about Amazon SageMaker Studio. The points note Studio is required for newer features, is launched within a domain that defines users/applications/storage, quickstart domain setup supports multiple users, and multiple apps are available (JupyterLab, Code Editor, RStudio, MLflow)." />
</Frame>

Quick reminders:

* Launching JupyterLab requires a managed compute-backed JupyterLab space (a managed EC2 instance—choose sizes like m5.large).
* Spaces can be private (single user) or shared (visible to multiple user profiles).
* SageMaker Studio Classic is legacy and should be used only for continuity in existing Classic environments.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with three numbered points: JupyterLab requires a space backed by a managed EC2 instance, spaces can be private or shared, and SageMaker Classic is outdated and should only be used in legacy environments." />
</Frame>

That concludes this section. Further guidance on configuring spaces, compute, and kernel management in JupyterLab will be covered in a later chapter.

Table — Quick comparison: SageMaker Studio (new) vs Studio Classic

| Feature / Area         | SageMaker Studio (new)   | SageMaker Studio Classic           |
| ---------------------- | ------------------------ | ---------------------------------- |
| Recommended?           | Yes (default)            | No (legacy)                        |
| Storage backend        | EBS (per-user volumes)   | EFS (shared POSIX)                 |
| UI customization       | Visible and granular     | Limited / hidden                   |
| Notebook sharing       | Built-in (links, Git)    | S3-based sharing required          |
| New SageMaker features | Supported                | Often unsupported                  |
| Best for               | New projects, production | Legacy migrations or compatibility |

Links and references

* [Amazon SageMaker Studio documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* [SageMaker Domains and User Profiles](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-domains.html)
* [AWS Identity Center (SSO)](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/378c1c95-e9c8-403b-b915-94effbf7dd25" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/36b760dd-2200-4b8b-9a8c-a16e9f1304e2" />
</CardGroup>


# SageMaker Domains and SageMaker Studio

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/SageMaker-Domains-and-SageMaker-Studio/page

Overview of Amazon SageMaker Domains and Studio, explaining benefits over notebook instances, architecture, setup options, user profiles, and launching Studio for collaborative ML workflows

In this lesson we cover Amazon SageMaker Domains and the SageMaker Studio web IDE. You'll learn why Studio was introduced, how a SageMaker Domain maps to the Studio experience, the trade-offs between quick and manual domain setup, and how to launch Studio and manage user profiles.

We will:

* Review limitations of SageMaker Jupyter notebook instances and why Studio is preferable for team workflows.
* Explain the components and architecture of a SageMaker Domain and how Studio uses them.
* Compare quick setup vs. manual (organization) setup choices.
* Walk through accessing Studio from the AWS Management Console and managing user profiles and personal apps.

## Limitations of Jupyter notebook instances

SageMaker supports single-user Jupyter notebook instances, but they present practical and operational limits for teams and production workflows:

* One instance per user leads to many long-running VMs when teams each create an instance.
* Billing continues while instances run; they do not auto-stop by default, increasing costs if users forget to shut them down.
* No built-in experiment tracking or standard reproducibility workflow.
* No automatic Git integration—each user must clone or configure repositories manually.
* Notebook instances provide only the Jupyter environment; integrating other SageMaker features often requires manual work.

These limitations motivate an integrated, collaborative IDE that bundles notebooks, experiment tracking, Git, and orchestration tools.

| Limitation Area          | Notebook Instances   | SageMaker Studio                           |
| ------------------------ | -------------------- | ------------------------------------------ |
| Multi-user collaboration | No (one-to-one)      | Shared workspaces available                |
| Experiment tracking      | None built-in        | SageMaker Experiments, MLflow integrations |
| Git integration          | Manual               | Built-in or mountable repos                |
| Cost control             | Manual stop required | Centralized management and policies        |
| Multi-IDE support        | Jupyter only         | JupyterLab, RStudio, Code Editor, and more |

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Jupyter Instances Limited.&#x22; It lists five numbered issues: no experiment tracking; manual Git setup; each user manages instances independently; manual stop risks extra charges; and limited to notebooks requiring external tools." />
</Frame>

## Experiment tracking and reproducibility

Tracking experiment inputs (data versions, preprocessing, model code, hyperparameters) and outputs (metrics, model artifacts) is essential for reproducibility and collaboration. Without a standard approach, teams risk losing context from prior runs—hyperparameters or dataset versions can be forgotten, and results become hard to compare.

SageMaker Studio addresses this by offering integrated experiment tools:

* SageMaker Experiments for tracking runs, lineage, and metadata: [https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html)
* Integrations with external frameworks such as MLflow: [https://mlflow.org](https://mlflow.org)

Third-party tools (CometML, Truera, etc.) can still be used, but Studio reduces dependency overhead by providing first-class experiment features and easier reproducibility.

## SageMaker Domain and Studio architecture

SageMaker Studio is deployed inside a SageMaker Domain. A Domain is an administrative boundary that groups users, shared storage, execution roles, and policy controls. Main components include:

* Shared file system: an Amazon EFS share is created for the Domain so users can access shared files. Note that Studio storage architectures and trade-offs have evolved; evaluate EFS performance and costs for production use.
* User profiles: each person must have a user profile in the Domain to open Studio. An AWS account or IAM user alone does not grant Studio access; the user profile binds the user to the Domain.
* Studio applications: the browser IDE exposes multiple applications (JupyterLab, RStudio, Code Editor, and other Studio apps).
* Execution role(s): IAM role(s) define what AWS resources Studio and user workloads can access (S3 buckets, model APIs, etc.).

<Frame>
  <img alt="A dark-themed diagram titled &#x22;Solution: SageMaker Domain and Studio&#x22; showing the architecture and components of an AWS SageMaker domain. It highlights user profiles, shared Elastic File System (EFS) storage, Studio applications (JupyterLab, R Studio, Code Editor, Studio Classic), and the IAM execution role." />
</Frame>

## What Studio provides over notebook instances

Moving from isolated notebook instances to a SageMaker Domain + Studio yields several operational and developer productivity benefits:

* Shared workspaces and file storage for team collaboration.
* Built-in or easily mounted Git repositories to support version-control driven workflows.
* Native experiment tracking (SageMaker Experiments) plus integrations like MLflow.
* Orchestration with SageMaker Pipelines to build repeatable ML workflows: [https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
* Fine-grained IAM control for datasets, models, and pipelines.
* Multiple hosted IDEs: JupyterLab, RStudio (check licensing), and a hosted VS Code-like Code Editor.

Summary of benefits:

| Feature               | Notebook Instances | Studio (Domain)                    |
| --------------------- | ------------------ | ---------------------------------- |
| Collaboration         | Limited            | Shared EFS, shared notebooks       |
| Experiment management | External tooling   | Built-in and integrated            |
| Orchestration         | Manual             | SageMaker Pipelines                |
| IDE options           | Jupyter only       | JupyterLab, RStudio, Code Editor   |
| Access control        | Instance-level     | Domain + IAM roles + user profiles |

Studio Classic vs. current Studio

* Studio Classic refers to the original UI and older architecture. AWS recommends using the current SageMaker Studio, which exposes newer capabilities and UI updates. Plan migration if you still use Studio Classic.

## Accessing SageMaker Studio (console walkthrough)

To open Studio from the AWS Management Console:

1. Open Amazon SageMaker.
2. In the left navigation under "Applications and IDEs", click Studio.

When creating a Domain, the console presents two provisioning paths: quick setup (single-user) and manual (organization) setup. Choose based on your needs: rapid evaluation vs. production readiness.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Creating a Domain&#x22; showing the Amazon SageMaker &#x22;Set up SageMaker Domain&#x22; screen. It displays side-by-side options for a single-user (quick setup) and an organization setup with feature checklists and a &#x22;Set up&#x22; button." />
</Frame>

## Quick setup vs. manual setup

* Quick setup: fastest path to a Domain. It creates a Domain with defaults (region default VPC, default user profile). Ideal for personal learning, experiments, or proofs-of-concept.
* Manual setup: required for production or regulated environments. It allows full control over VPC/subnets, KMS encryption keys, authentication (federated SSO via AWS Identity Center / Microsoft Entra), and granular IAM policies.

<Callout icon="lightbulb">
  Use quick setup for learning, demos, and short-term experimentation. For production, compliance, or private-network workloads, select manual setup to control networking, encryption, and authentication.
</Callout>

Manual setup considerations:

* Security & access control: design custom IAM roles and policies, configure KMS keys, and integrate identity federation where needed.
* Infrastructure & resources: choose subnets, EBS or other storage choices, and configure VPC endpoints for secure access.
* Integration & compliance: enable audit logging, align with organizational policies, and integrate required services.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Creating a Domain&#x22; showing a three-column table of &#x22;Manual Setup Considerations.&#x22; The columns list bullet points under &#x22;Security & Access Control,&#x22; &#x22;Infrastructure & Resources,&#x22; and &#x22;Integration & Compliance&#x22; (IAM/VPC/encryption, subnet/EBS/resource settings, and integration/audit items)." />
</Frame>

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Workflow: Creating a Domain&#x22; with the subtitle &#x22;When to Choose Manual Setup.&#x22; It lists six reasons: precise security control, integration with existing infrastructure, compliance with policies, cost optimization, custom network configurations, and specific authentication methods." />
</Frame>

<Callout icon="warning">
  [JupyterLab](https://jupyter.org) 3 notebooks on SageMaker Studio Classic have reached end of support. If you are still using Studio Classic, migrate to the current SageMaker Studio and newer JupyterLab versions to continue receiving security fixes and feature updates.
</Callout>

## Domains, user profiles, and launching Studio

After a Domain is created:

* The Studio section in SageMaker will show an "Open Studio" action under Applications and IDEs.
* Domains contain user profiles—each person needs a user profile associated with the Domain to launch Studio. Having IAM credentials alone does not grant access.
* Quick setup creates a default user profile; manual setup requires you to create user profiles explicitly.

To view or manage user profiles:

1. In the SageMaker console sidebar, open "Admin configurations" → "Domains".
2. Click the domain name, then open the "User profiles" tab.

From the "User profiles" tab you can launch Studio on behalf of a user. The launch menu exposes the user’s available personal apps (for example: Studio, Canvas, TensorBoard, Profiler, Spaces) so the user can select which application to open.

<Frame>
  <img alt="A screenshot of an &#x22;Workflow: User Profiles&#x22; page in Amazon SageMaker showing domain details and the &#x22;User profiles&#x22; tab with a listed default user. A &#x22;Personal apps&#x22; launch menu is open on the right, showing options like Studio, Canvas, TensorBoard, Profiler, and Spaces." />
</Frame>

When you open SageMaker Studio, it opens in a new browser tab at a Studio-specific endpoint (for example: `https://studio-<unique-id>.<region>.sagemaker.aws`), which is distinct from the AWS Management Console URL.

## Summary

SageMaker Domains + SageMaker Studio deliver a managed, collaborative, and production-capable environment that addresses limitations of single-user notebook instances. Key takeaways:

* Studio provides shared file storage, integrated experiment tracking, and pipeline orchestration.
* Studio supports Git integration and multiple IDEs (JupyterLab, RStudio, Code Editor).
* For rapid evaluation, use quick setup. For production, compliance, or private-network requirements, choose manual setup and design networking, encryption, and IAM accordingly.
* Ensure migration from Studio Classic and older JupyterLab versions to benefit from continued support.

Links and references

* SageMaker Documentation: [https://docs.aws.amazon.com/sagemaker/](https://docs.aws.amazon.com/sagemaker/)
* SageMaker Experiments: [https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html)
* SageMaker Pipelines: [https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
* JupyterLab: [https://jupyter.org](https://jupyter.org)
* MLflow: [https://mlflow.org](https://mlflow.org)
* AWS Identity Center: [https://aws.amazon.com/identity/identity-center/](https://aws.amazon.com/identity/identity-center/)
* Microsoft Entra (identity docs): [https://learn.microsoft.com/en-us/entra/](https://learn.microsoft.com/en-us/entra/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/0e5adf40-c164-4a70-8932-d610dcedffec" />
</CardGroup>
