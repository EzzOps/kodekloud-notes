# Terraform Cloud Workspaces

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Workspaces/Terraform-Cloud-Workspaces/page

Terraform Cloud Workspaces are organizational units that manage and isolate infrastructure collections, each with its own state, variables, and run history.

Terraform Cloud Workspaces are the core organizational units within Terraform Cloud. They let you isolate, manage, and collaborate on collections of infrastructure—each with its own state, variables, and run history.

A workspace bundles everything Terraform needs to manage a specific environment or component in your Terraform Cloud organization:

![The image explains what Terraform Cloud workspaces are and what they contain, including a linked VCS repository, variables, the current state file, and historical states and logs. It features the Terraform Cloud logo and cartoon characters at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878942/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-cloud-workspaces-explained.jpg)

Key features include:

* Linked Version Control System (VCS) repository for configuration
* Workspace-level variables (plaintext and sensitive)
* Remote, managed state storage
* Historical run logs, cost estimation, governance, and notifications

***

## Table of Contents

1. [Key Components](#key-components-of-a-workspace)
2. [Units of Isolation](#units-of-isolation)
3. [Real-World Example: Airline Corporation](#real-world-example-airline-corporation)
4. [Reducing the Blast Radius](#reducing-the-blast-radius)
5. [Naming Conventions](#naming-conventions)
6. [Workspace Settings](#workspace-settings)
7. [Execution Modes](#execution-modes)
8. [Getting Started](#getting-started-with-terraform-cloud)
9. [References](#references)

***

## Key Components of a Workspace

| Component         | Description                                                                            | Benefits                                      |
| ----------------- | -------------------------------------------------------------------------------------- | --------------------------------------------- |
| Remote State      | Stores Terraform state files centrally in Terraform Cloud.                             | Secure, shareable state with version history  |
| Variables         | Define environment-specific or secret values in the workspace UI or via API.           | Centralized management of sensitive data      |
| Operations & Logs | Execute `plan`, `apply`, and `destroy` remotely or locally, with complete run history. | Audit trail, notifications, and collaboration |

***

## Units of Isolation

Workspaces act as isolated directories, each maintaining its own state. This decomposition reduces risk by preventing unintended cross-environment changes:

![The image explains the concept of "Units of Isolation" in Terraform, illustrating how monolithic infrastructure is decomposed into workspaces, each containing a state file for different components like app, network, and database.](https://kodekloud.com/kk-media/image/upload/v1752878943/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/units-of-isolation-terraform-diagram.jpg)

Typical decomposition:

* **App** → Dedicated workspace
* **Network** → Shared workspace
* **Database** → Separate workspace

***

## Real-World Example: Airline Corporation

An airline might organize by application tier and environment:

![The image illustrates a Terraform Cloud organization for an airline corporation, showing different workspaces for applications like Ticket App and Baggage Tracking App, each with separate functions such as Front End, Backend, Networking, Prod, QA, and Dev.](https://kodekloud.com/kk-media/image/upload/v1752878944/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-cloud-airline-workspaces-diagram.jpg)

Possible workspace layout:

| Component  | Environments            |
| ---------- | ----------------------- |
| Front End  | dev, qa, prod           |
| Back End   | dev, qa, prod           |
| Networking | shared network services |

***

## Reducing the Blast Radius

Combining multiple environments in one state file risks cross-environment side effects. By isolating Dev, QA, and Prod in separate workspaces, changes in QA can never impact Prod:

![The image is a presentation slide discussing the use of a single state file in software development, highlighting the potential impacts of changes on different resources and environments. It includes a diagram showing how updates to a development app can affect cloud resources, VMs/containers, and applications across different apps.](https://kodekloud.com/kk-media/image/upload/v1752878946/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/single-state-file-impact-diagram.jpg)

With dedicated `qa` and `prod` workspaces:

![The image illustrates a workflow for reducing the blast radius in software development, showing a process from a developer committing changes to a code repository, through Terraform Cloud execution, and applying updates in a QA workspace without impacting production infrastructure.](https://kodekloud.com/kk-media/image/upload/v1752878947/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/blast-radius-reduction-workflow-diagram.jpg)

***

## Naming Conventions

Consistent workspace names simplify filtering, access control, and governance. Include:

* Application or component
* Environment (e.g., `dev`, `qa`, `prod`)
* Region or cloud provider
* Team or project prefix

Examples:

| Naming Pattern         | Example          |
| ---------------------- | ---------------- |
| `<app>-<env>`          | `ecom-web-prod`  |
| `<team>-<app>-<env>`   | `adt-mobile-qa`  |
| `<app>-<region>-<env>` | `ecom-usw1-prod` |

***

## Workspace Settings

Each workspace offers granular settings:

![The image lists various workspace components related to Terraform, such as configurations, state file, variables, run history, and more, each represented with icons. It also includes two cartoon characters at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878948/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-workspace-components-icons-cartoon.jpg)

* Terraform version selection
* Run history, logs, and cost estimates
* Role-based access control (RBAC)
* Notifications (email, Slack, webhook)
* Governance & policy checks via Sentinel or OPA

***

## Execution Modes

Terraform Cloud supports two modes for running operations:

### Local Execution

Run Terraform commands on your workstation, but store state remotely in Terraform Cloud. Ideal for minimal workflow changes:

![The image explains that Terraform will no longer write to the local .tfstate file, with the state now stored on Terraform Cloud, while the local workflow remains unchanged. It includes a diagram showing the process from a local machine to Terraform Cloud.](https://kodekloud.com/kk-media/image/upload/v1752878950/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-cloud-local-workflow-diagram.jpg)

### Remote Execution

All operations execute within Terraform Cloud’s infrastructure, centralizing runs, logs, and policies:

![The image is a diagram listing components for remote execution in HashiCorp Terraform Cloud, including configurations, state file, notifications, variables, run history, and version. It features icons and a cloud logo, with two cartoon characters at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752878951/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-cloud-remote-execution-diagram.jpg)

> **triangle-alert** To enable policy enforcement, advanced cost estimation, and team management, consider upgrading your Terraform Cloud plan.

![The image is an infographic promoting the upgrade of a Terraform Cloud plan, listing features like configurations, state file, policies, and cost estimation. It includes icons and checkmarks to highlight available features.](https://kodekloud.com/kk-media/image/upload/v1752878952/notes-assets/images/HashiCorp-Terraform-Cloud-Terraform-Cloud-Workspaces/terraform-cloud-upgrade-infographic.jpg)

***

## Getting Started with Terraform Cloud

Add a `backend` or `cloud` block in your `terraform` configuration, then initialize:

```hcl theme={null}
