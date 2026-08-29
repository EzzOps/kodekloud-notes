# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Cloud/Introduction/page

Overview of Terraform Cloud, its plans, features, and guidance comparing managed SaaS versus self-hosted Terraform for team size, governance, and automation needs

Terraform Cloud plans

This article explains what Terraform Cloud is, the core problems it addresses, and how its different plans map to team size, governance needs, and automation requirements. You’ll also find a concise comparison between self-hosted Terraform and Terraform Cloud to help you decide which model fits your organization.

Terraform Cloud is a managed platform for running Terraform that centralizes state management, secures sensitive data, enables team collaboration, and standardizes workflows and policy across organizations. It provides remote runs, stores state securely, shares variables and secrets, and integrates with VCS and CI/CD systems to enforce consistent provisioning practices.

Each Terraform Cloud plan targets different levels of team maturity and operational requirements—ranging from individuals and small teams to large enterprises requiring advanced policy enforcement, SSO, and high-volume automation. Plans vary in concurrency limits, governance controls, audit logging, self-service modules, and support.

Self-hosted Terraform (running the Terraform CLI and managing state yourself) offers maximum control and customization, useful for strict compliance, bespoke integrations, or air-gapped environments. Terraform Cloud reduces operational overhead by offering a managed control plane for state, runs, and collaboration, and is often preferable for teams that want to focus on infrastructure rather than managing tooling.

<Frame>
  <img alt="The image is an introduction slide outlining three key topics: explaining Terraform Cloud, describing its plans and capabilities, and comparing it with self-hosted Terraform." />
</Frame>

## What is Terraform Cloud?

Terraform Cloud is HashiCorp’s SaaS offering that centralizes Terraform operations. Key capabilities include:

* Remote execution of Terraform plans and applies to remove sensitive credentials from local machines.
* Secure remote state storage with state locking and history.
* Encrypted variable and secret storage with granular workspace access controls.
* VCS integration (GitHub, GitLab, Bitbucket, Azure Repos) to drive runs from pull requests and commits.
* Policy enforcement with Sentinel or policy as code frameworks.
* Team collaboration features like role-based access control (RBAC), audit logs, and notifications.

<Callout icon="lightbulb">
  Terraform Cloud helps teams scale infrastructure safely by removing local state files and centralizing automation. Use VCS-backed workspaces to ensure reproducible, auditable changes.
</Callout>

## Terraform Cloud Plans (Overview)

Below is a high-level comparison of the common Terraform Cloud plans and their target use cases.

| Plan              | Target audience                          | Key capabilities                                                                        |
| ----------------- | ---------------------------------------- | --------------------------------------------------------------------------------------- |
| Free              | Individuals, small projects              | Remote runs, `remote` state, 1 concurrent run, basic VCS integration                    |
| Team & Governance | Teams requiring policy and collaboration | Multiple concurrent runs, policy enforcement, RBAC, private module registry, audit logs |
| Business          | Organizations with advanced governance   | SSO (SAML/OIDC), enhanced API rate limits, run tasks, private networking options        |
| Enterprise        | Large organizations at scale             | Dedicated support, deployment flexibility, advanced governance, custom SLAs             |

Note: Exact feature names, limits, and plan branding can change—refer to the official Terraform Cloud plans page for the latest details.

## Feature highlights by capability

* State & runs: centralized state storage, locking, and remote execution.
* Secrets & variables: workspace-level variables, environment variables, and integrations with secret managers.
* Collaboration: workspace access controls, team management, and audit logs.
* Governance & policy: policy-as-code enforcement for compliance and security.
* Integrations: VCS providers, CI/CD tools, and provider plugins.

## Self-hosted Terraform vs Terraform Cloud

The following table summarizes differences to help you evaluate which approach fits your needs:

| Aspect                 | Self-hosted Terraform (CLI + self-managed state)                           | Terraform Cloud (SaaS)                                                            |
| ---------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Control                | Maximum—manage state, storage, and runners yourself                        | Managed control plane with limited customization                                  |
| Operational overhead   | High—requires running and securing state backends and automation           | Lower—HashiCorp manages runs, state, and platform availability                    |
| Compliance & isolation | Easier to meet strict on-prem or air-gapped requirements                   | May require private networking or Enterprise plan for strict isolation            |
| Integrations           | Fully customizable but self-built                                          | Built-in VCS integrations, module registry, and provider plugins                  |
| Cost model             | Infrastructure + maintenance costs                                         | Subscription-based with predictable tiers and support                             |
| Recommended when       | You need bespoke integrations, no external network access, or full control | You want faster onboarding, lower ops burden, and built-in collaboration features |

<Callout icon="warning">
  If your environment requires complete air-gapped operation or very specific compliance controls, self-hosting Terraform and a private state backend may be necessary. Consider Terraform Enterprise if you want managed features with stronger isolation controls.
</Callout>

## When to choose each option

* Choose Terraform Cloud if:
  * You want a managed control plane for remote runs and central state.
  * Your team benefits from VCS-driven workflows, policy enforcement, and a private module registry.
  * You prefer reduced operational overhead and built-in collaboration.

* Choose self-hosted Terraform if:
  * You require full control over infrastructure, storage, and network isolation.
  * You need to run in environments with no external connectivity or strict data residency.
  * You plan extensive custom integrations or bespoke CI/CD flows not supported by Terraform Cloud.

## Further reading and references

* [Terraform Cloud documentation](https://www.terraform.io/cloud)
* [Terraform CLI documentation](https://www.terraform.io/docs/cli)
* [Using VCS with Terraform Cloud](https://www.terraform.io/cloud/docs/vcs)
* [Terraform Enterprise overview](https://www.hashicorp.com/products/terraform/enterprise)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/ca386519-4725-417d-a46f-642d0a683a01/lesson/8b594ec3-97b8-4510-98e7-b2ab30edde2c" />
</CardGroup>
