# HCP Terraform Execution Modes

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/HCP-Terraform-Execution-Modes/page

Guide explaining HCP Terraform execution modes remote local and agent, their behaviors, trade offs, networking considerations, and per workspace selection guidance

Understanding where your Terraform runs is critical for security, networking, and team workflows. This guide explains the three execution modes available with HCP Terraform, how each mode behaves, and trade-offs to consider when choosing per workspace.

Below is a concise overview followed by detailed descriptions and practical examples.

## Quick summary

| Execution mode   |                       Where operations run | State storage           | Best for                                                           | Key trade-offs                                                                                                |
| ---------------- | -----------------------------------------: | ----------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Remote (default) | HashiCorp-managed ephemeral infrastructure | Remote in HCP Terraform | Teams requiring collaboration, policy enforcement, cost estimation | Full feature set, centralized control; requires outbound connectivity from HCP to targets (or network access) |
| Local            |             Developer machine or CI runner | Remote in HCP Terraform | Individuals or teams who prefer running Terraform locally          | Local visibility of variables only; loses remote-run features such as Sentinel enforcement                    |
| Agent            |   Self-hosted agent inside private network | Remote in HCP Terraform | Private data centers, resources behind firewalls                   | Allows access to internal endpoints; requires deploying and maintaining agents                                |

For more details about execution modes and networking considerations, see the official Terraform Cloud execution modes docs: [https://developer.hashicorp.com/terraform/cloud/run/execution-modes](https://developer.hashicorp.com/terraform/cloud/run/execution-modes)

## 1) Remote execution (recommended — default)

By default, HCP Terraform executes `terraform plan` and `terraform apply` remotely on HashiCorp-managed ephemeral VMs. This is commonly referred to as remote execution.

Benefits

* Team collaboration and visibility: runs appear in the HCP Terraform app, where you can review plan output, see who triggered runs, and audit changes.
* Full feature access: Sentinel policy checks, cost estimation, run notifications, and other advanced features depend on remote execution.
* Centralized governance: consistent runtime environment and standardized logging across teams.

When to choose remote execution

* You need policy enforcement (Sentinel) or centralized run approval.
* Multiple team members collaborate and require a single source of truth for run logs and plans.
* You prefer HashiCorp’s managed compute for running ephemeral Terraform operations.

## 2) Local execution

In local execution mode, Terraform operations run on your local machine or wherever you invoke Terraform (for example, in CI). HCP Terraform still manages the workspace state remotely.

Common commands

```bash theme={null}
terraform plan
terraform apply
```

Key characteristics

* State storage and locking: Workspace state remains in HCP Terraform, so you retain remote state locking, versioning, and encryption.
* Local runtime: `plan` and `apply` execute in your local environment or CI runner.
* Limited remote features: features that require code execution on HCP-managed runners (like Sentinel evaluations tied to remote runs) are not performed during local runs.

> **warning** In local execution mode, workspace variables and variable sets configured in HCP Terraform are not evaluated during local `plan` and `apply`. Local Terraform only reads values from `-var` CLI flags, local `*.tfvars` files, and environment variables. Ensure required variables are available in your local environment or CI before running Terraform locally.

When to choose local execution

* Developers or DB teams prefer to execute changes from their machines.
* Your workflow requires CI-native runs that are executed in your own runners rather than HashiCorp’s ephemeral infrastructure.
* You still want centralized state management but need Terraform to run in a specific runtime environment.

## 3) Agent execution

Agent execution is designed for situations where HCP Terraform cannot reach target infrastructure directly (for example, private networks, on-premises systems, or resources behind a strict firewall).

How agent mode works

* Deploy a lightweight HCP Terraform agent inside your private network where it has network access to target resources.
* The agent establishes an outbound connection to HCP Terraform and receives run instructions.
* `plan` and `apply` are executed on the self-hosted agent, enabling access to internal endpoints while operations are still coordinated through HCP.

Why use agents

* You need secure, inbound-restricted access to private networks.
* You want the governance and centralized state of HCP Terraform, but the runtime must execute inside your network perimeter.
* The same agent implementation can be used across HCP Terraform and Terraform Enterprise for policy evaluation and runs.

When to choose agent execution

* Managing internal infrastructure (monitoring, networking, databases) that is not reachable from HashiCorp-managed infrastructure.
* Maintaining stronger network isolation, while still retaining centralized state and run tracking.

## Per-workspace configuration: mix-and-match

Execution mode is configured per workspace — not at the organization or project level. Each workspace can be set independently to remote, local, or agent execution depending on operational, security, and collaboration requirements.

Examples

* `networking-prod`: remote execution for centralized policy checks and team visibility.
* `monitoring-prod`: agent execution so the agent can access internal monitoring endpoints behind a firewall.
* `db-prod`: local execution if the database team runs Terraform locally while still using HCP Terraform for state.

Design considerations

* Use remote execution to unlock full platform features and centralized governance.
* Use agent execution to reach internal-only resources without opening inbound network ports.
* Use local execution when developers or CI systems must run Terraform in a specific environment, and you can surface all required variables locally.

> **lightbulb** Execution mode controls where Terraform runs; it does not change that HCP Terraform can still manage workspace state (unless you explicitly choose a different backend). Configure execution mode per workspace to match networking, security, and governance requirements.

## Links and references

* Terraform Cloud/Enterprise execution modes: [https://developer.hashicorp.com/terraform/cloud/run/execution-modes](https://developer.hashicorp.com/terraform/cloud/run/execution-modes)
* Terraform documentation: [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)
* HashiCorp Cloud Platform: [https://www.hashicorp.com/cloud](https://www.hashicorp.com/cloud)

If you need a quick comparison table or help deciding which mode suits a specific scenario, list your constraints (networking, policy, team workflow) and we can create tailored recommendations.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/17b51d82-fcd9-4b8b-93a6-9b132e49510b)
