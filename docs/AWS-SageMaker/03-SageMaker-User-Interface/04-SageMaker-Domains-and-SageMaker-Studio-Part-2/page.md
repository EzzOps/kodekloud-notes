# SageMaker Domains and SageMaker Studio Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-User-Interface/SageMaker-Domains-and-SageMaker-Studio-Part-2/page

Guide to SageMaker Studio apps, spaces, EBS-backed storage, private versus shared collaboration, lifecycle and billing, and when to create separate domains for isolation.

SageMaker Studio is more than a hosted Jupyter environment — it’s a multi-application, containerized IDE that runs inside your AWS account. From the Studio URL you get a richer, dark‑mode interface (top-left applications panel) where multiple hosted apps are available and managed within your SageMaker domain and AWS region.

This guide explains the Studio applications, how spaces map to compute and storage, sharing and collaboration models, lifecycle and billing, and when to create a new domain.

## Studio applications at a glance

Applications in SageMaker Studio run inside managed EC2-backed spaces and pull container images that define the runtime (libraries, SDKs, and tools). Use the table below to understand each app and its common use case.

| Application           | Purpose / Typical Use Case                                                                          |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| JupyterLab            | Interactive data exploration, notebooks, and quick prototyping.                                     |
| RStudio               | Familiar environment for statisticians and R developers (some features require an RStudio license). |
| Code Editor (VS Code) | Refactor notebooks, build production-ready Python packages, and integrate with CI/CD.               |
| Canvas                | Low-code visual model building for users who prefer not to write Python.                            |
| MLflow                | Experiment tracking and model registry functionality integrated into Studio.                        |

We’ll briefly examine these apps’ roles and then focus on spaces, storage, and how to manage lifecycle and collaboration.

When you open Studio you may also see a “SageMaker Studio Classic” link (the legacy interface). Classic is deprecated in favor of modern Studio — prefer the modern experience unless you have a specific legacy requirement.

<Frame>
  <img alt="An infographic table titled &#x22;Workflow: SageMaker Studio&#x22; comparing features side-by-side between SageMaker Classic and SageMaker Studio. It lists differences across items like default creation, storage (shared Amazon EFS vs individual EBS), collaboration, execution role, customization, and application support." />
</Frame>

## Storage, spaces, and sharing — core concepts

A space is the managed compute environment that hosts one of the Studio applications (JupyterLab, Code Editor, RStudio, etc.). Each space is backed by an EC2 instance that runs one or more containers (from Amazon ECR or SageMaker-provided images) and attaches storage (EBS for modern Studio). When creating a space you typically choose:

* Instance size (for example, ml.t3.medium).
* Container image (SageMaker-provided image or your custom image).

### Private vs shared spaces

* Private space: a dedicated EC2 instance + EBS volume attached to a single user profile. Only that user sees the space and its running instance.
* Shared space: a single EC2 instance + EBS volume shared between multiple user profiles within the same domain; suitable for collaboration and real-time co-editing.

### Important storage change (EFS → EBS)

Modern SageMaker Studio uses EBS volumes attached to the EC2 instance that runs each space. Historically, Studio Classic used Amazon EFS (a network file system) for shared storage. The move to EBS provides improved performance and predictable IOPS for per-space work. If domain-level EFS exists, you can mount it manually inside a space (NFS), but it is not used automatically for Studio spaces.

> **lightbulb** Note: Older documentation (pre‑2025) may refer to EFS for shared Studio storage. Modern Studio spaces are EBS-backed by default—check the official AWS SageMaker docs for the current behavior: [https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)

## Spaces, users, and visibility

Consider a domain with multiple user profiles and two spaces:

* A private JupyterLab space for User A (visible only to User A).
* A shared JupyterLab space (visible to all users in the domain who have permission).

Visibility and access rules:

* Private space: only the creating user profile can see and open it.
* Shared space: visible to domain users, but actions still depend on IAM permissions and Studio settings.

Storage alignment:

* Private spaces: each has its own EBS volume attached to the instance.
* Shared spaces: one instance with a single attached EBS volume is shared among collaborators.
* Domain-level EFS (if present) is not automatically mounted; explicit NFS mounting is required.

## How a space runs applications (containers and registries)

When you start a space, Studio provisions an EC2 instance of the chosen type and runs one or more containers. These containers are pulled from a container registry — either Amazon ECR in your account or SageMaker-hosted images. The container image provides the application (JupyterLab, RStudio, Code Editor) and libraries such as NumPy, Pandas, the SageMaker Python SDK, and boto3.

A minimal example of Python imports that already work inside SageMaker’s default container image:

```python theme={null}
import sagemaker
import boto3
```

You typically don’t need to pip-install sagemaker or boto3 inside the default image because they are already included in official SageMaker images. For custom dependency requirements, build a custom image or use the environment’s package manager at startup.

<Frame>
  <img alt="A simple flow diagram titled &#x22;Workflow: JupyterLab Spaces&#x22; showing a SageMaker Distribution 2.1.0 container image in Amazon Elastic Container Registry being deployed (arrow) to a JupyterLab server container running on a managed EC2 instance (ml.t3.medium)." />
</Frame>

## Starting, stopping, and billing behavior

Start and stop spaces from the Studio UI or the AWS Console. Key points:

* Stopping a space terminates the EC2 instance — you stop paying for the instance hourly cost.
* Persistent data on the attached EBS volume remains (unless you explicitly delete it).
* External resources created from within the space (SageMaker endpoints, EMR clusters, S3 buckets, etc.) continue running and incurring charges until you explicitly delete them.

Always double-check for long‑running endpoints or clusters before stopping a space to avoid unexpected charges.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: JupyterLab Spaces&#x22; showing a dark-themed confirmation dialog to &#x22;Stop space&#x22; with a blue info box about additional resources and buttons labeled &#x22;Cancel&#x22; and &#x22;Stop space.&#x22; The slide caption beneath reads, &#x22;We can start and stop a space.&#x22;" />
</Frame>

## JupyterLab inside a space

When a JupyterLab space is running you can open JupyterLab from Studio. The JupyterLab launcher provides notebook kernels, terminals, Git integration, and the file browser common to JupyterLab.

Real-time collaboration (RTC)

* If a space is shared and RTC is enabled, Studio shows collaborator avatars (colored circles with initials) and indicates RTC presence, so multiple users can edit the same notebook in real time.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: JupyterLab Spaces&#x22; showing a JupyterLab screenshot with a purple circular user avatar in the top-right toolbar. The caption notes that each user gets a unique circle identity in the top-right toolbar." />
</Frame>

## Managing spaces: Studio UI vs AWS Console

You can manage spaces in two places:

1. Inside SageMaker Studio UI

* Applications panel → choose JupyterLab / Code Editor / RStudio → see and start/stop available spaces for your user profile.

2. AWS Management Console → SageMaker → Domain → Space management

* Administrators can view all spaces in the domain, their owner (user profile), type (private/shared), status (InService/Stopped), instance type, and perform administrative actions.
* Note: Administrators can view domain-level configuration, but private spaces remain visible only to their owner in the Studio UI.

<Frame>
  <img alt="A screenshot of a JupyterLab Space settings page (jupyterlab-space-2) in SageMaker showing instance info, storage settings and controls like &#x22;Stop space&#x22; and &#x22;Open JupyterLab.&#x22; A green notification at the bottom says the JupyterLab app was successfully created." />
</Frame>

## Instance properties, resizing, and stopped-state changes

* Instance properties include the instance type (e.g., ml.t3.medium) and the attached EBS volume size (for example, 5 GiB).
* To change instance type or increase EBS size you usually must stop the space first. Changes take effect when the space restarts.
* Always snapshot or back up important data before resizing or deleting volumes.

<Frame>
  <img alt="A slide titled &#x22;Workflow: JupyterLab Spaces&#x22; showing a SageMaker Studio &#x22;Running instances&#x22; dashboard with a JupyterLab space listed. The caption notes that private spaces are limited to a single user profile, so each user can only see their own spaces." />
</Frame>

## Private vs Shared — quick comparison

| Aspect            | Private Spaces                          | Shared Spaces                                                              |
| ----------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| Visibility        | Only the owner can see it               | Visible to all domain users (actions bound by IAM)                         |
| Compute & Storage | Dedicated EC2 instance + EBS volume     | Single EC2 instance + EBS shared among collaborators                       |
| Best for          | Sensitive work, heavy customizations    | Collaboration, real-time co-editing                                        |
| Admin access      | Admins do not automatically gain access | Administrators can manage domain-level settings; access still respects IAM |

<Frame>
  <img alt="A slide titled &#x22;Workflow: JupyterLab Spaces&#x22; comparing Private Spaces and Shared Spaces. The left column lists private-space rules (each user has their own view, only the creator can access, admins have no direct access) and the right column lists shared-space rules (visible to domain users and accessible with proper permissions)." />
</Frame>

## When to create a new SageMaker domain

Create a separate SageMaker domain when you need tenant-like isolation:

* Full separation of storage and compute boundaries.
* Distinct IAM or networking policies per tenant.
* Regulatory or billing isolation between teams.

Domains provide clean separation for users, resources, and admin boundaries.

## Closing notes and best practices

* Prefer modern SageMaker Studio (EBS-backed) rather than Studio Classic (EFS-based) unless you have legacy requirements.
* Use private spaces for sensitive work or when users need complete isolation.
* Use shared spaces for collaboration and real‑time co-editing, but enforce IAM and network controls for safety.
* De-provision endpoints, EMR clusters, and other long-running resources you no longer need before stopping a space to avoid unexpected charges.

## Links and references

* Official SageMaker Studio docs: [https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
* Amazon EFS — What is EFS: [https://docs.aws.amazon.com/efs/latest/ug/what-is-efs.html](https://docs.aws.amazon.com/efs/latest/ug/what-is-efs.html)
* Amazon EBS — EBS Overview: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs.html)
* Amazon ECR — What is ECR: [https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* SageMaker Python SDK: [https://sagemaker.readthedocs.io/en/stable/](https://sagemaker.readthedocs.io/en/stable/)
* boto3 documentation: [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

If you want, I can add example Terraform or CloudFormation snippets for creating a domain, user profiles, and spaces (including private vs shared configurations).

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b5e72234-012c-4793-ad8c-e1a7c6d3b8be/lesson/5b02cd21-61d0-4f88-a33f-5a6bb8c5a257)
