# Terraform Cloud Plans

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Cloud/Terraform-Cloud-Plans/page

Overview of Terraform Cloud and Enterprise plans, comparing tiers, features, governance, security, collaboration, and support to help teams choose the right infrastructure-as-code offering

This guide summarizes Terraform Cloud’s available plans and the capabilities each tier provides. Use it to evaluate collaboration, governance, security, and operational controls that best match your team or organization’s infrastructure-as-code needs.

## Free plan

The Free plan is ideal for individuals, learners, and very small teams who want to try Terraform Cloud or run non-critical workloads at no cost. Key features and constraints:

* Remote state storage and remote runs: State is stored securely in Terraform Cloud and runs can execute in the cloud, removing reliance on local state files and reducing risk from developer machines.
* Private module registry: Share reusable Terraform modules inside your organization to standardize patterns and accelerate adoption.
* Community support: Access documentation and community forums for self-service troubleshooting.
* Resource limit: Supports up to 500 managed resources.
* No credit card required: Convenient for evaluations and personal projects.

<Frame>
  <img alt="The image is about Terraform Cloud's free plan, highlighting features such as remote state execution, private module sharing, community support, and a resource limit of up to 500 managed resources per month." />
</Frame>

The Free plan is best for learning Terraform Cloud fundamentals and managing small, low-risk environments.

## Standard plan

Designed for small teams moving toward collaborative infrastructure workflows, the Standard plan adds essential collaboration and governance features on top of the Free tier:

* Team collaboration and role-based access: Granular permissions to control who can plan, apply, or manage infrastructure.
* Cost estimation and checks: Preview estimated cloud costs for proposed changes and add checks to limit unexpected spend.
* VCS integration: Full integration with GitHub, GitLab, Bitbucket, and other supported version control systems to enforce GitOps practices.
* Silver-level support from HashiCorp.

<Frame>
  <img alt="The image is an advertisement for Terraform Cloud's Standard Plan, highlighting features such as team collaboration, role-based access control, and task and cost estimation. The plan starts at $0.10 per resource per month." />
</Frame>

Standard is a good fit for teams transitioning from individual use to production-ready, collaborative infrastructure management.

## Plus plan

The Plus plan targets organizations standardizing infrastructure-as-code across teams and environments by improving governance, visibility, and automation:

* Auditability: Track user actions and infrastructure changes for traceability and compliance reviews.
* Drift detection: Detect when live infrastructure diverges from declared configuration and surface remediation options.
* Continuous validation: Enforce validation rules and policy checks before changes are applied.
* Silver-level support included.

<Frame>
  <img alt="The image is an informational graphic describing features of the Terraform Cloud Plus Plan, which includes enterprise-ready automation, audit logging, drift detection, and continuous validation with silver support, starting at $0.47 per resource per month." />
</Frame>

Plus is ideal for organizations requiring stronger governance and visibility while scaling Terraform usage across multiple teams.

## Premium plan

Premium provides enterprise-grade controls for large organizations with advanced security, compliance, and scale requirements:

* Self-service provisioning with organizational controls for safe team deployments.
* Enterprise identity provider integrations for secure authentication and centralized identity management.
* Execution concurrency controls and support for self-hosted agents to meet network and compliance constraints.
* Policy-as-code enforcement (HashiCorp Sentinel) and SLA-backed availability with advanced support.

Premium suits enterprises that need advanced control, security, and scalability for mission-critical infrastructure.

## Terraform Enterprise (self-hosted)

Terraform Enterprise is the self-hosted distribution of Terraform Cloud for organizations that need complete control over deployment, data residency, and compliance:

* On-premises or private-cloud deployment to keep state and execution environments under organizational control.
* Fine-grained RBAC and SAML/SSO integration for enterprise identity and access management.
* Scalable workflows with advanced concurrency, performance, and policy controls for complex environments.
* Built-in audit logging, compliance enforcement, and enterprise-grade SLA/support for regulated industries.

Terraform Enterprise is optimal for organizations with strict regulatory, residency, or customization requirements.

> **lightbulb** This series uses the self-hosted option (Terraform Enterprise). Subsequent articles focus on Terraform Enterprise deployment patterns, operational setup, and ongoing maintenance.

## Plan comparison at a glance

| Plan                               | Best for                                       | Notable features                                                                             | Support level            |
| ---------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------ |
| Free                               | Individuals, learners, small personal projects | Remote state & runs, private module registry, community support, up to 500 managed resources | Community                |
| Standard                           | Small teams & early adopters                   | RBAC, VCS integration, cost estimation, team collaboration                                   | Silver                   |
| Plus                               | Growing organizations                          | Audit logs, drift detection, continuous validation, stronger governance                      | Silver                   |
| Premium                            | Large enterprises                              | Self-service provisioning, IdP integrations, self-hosted agents, Sentinel policies, SLA      | Enterprise support       |
| Terraform Enterprise (self-hosted) | Regulated or highly controlled environments    | Full data residency, SSO/RBAC, enterprise performance & compliance controls, auditability    | Enterprise SLA & support |

## Useful links and references

* [Terraform Cloud documentation](https://www.terraform.io/cloud)
* [Terraform Enterprise documentation](https://www.terraform.io/enterprise)
* [HashiCorp Sentinel policy-as-code](https://www.hashicorp.com/sentinel)
* [VCS integrations (GitHub, GitLab, Bitbucket)](https://www.terraform.io/cloud/vcs)

Use this guide to match the right Terraform offering to your team’s collaboration, governance, and compliance needs.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ca386519-4725-417d-a46f-642d0a683a01/lesson/97b9e661-a557-4d7a-8d6c-1a4fdbe547e1)
