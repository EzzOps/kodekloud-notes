# HCP Terraform Overview longer video

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/HCP-Terraform-Overview-longer-video/page

Overview of HCP Terraform, a managed HashiCorp platform that centralizes remote state, collaboration, remote execution, cost estimation, and governance while preserving Terraform CLI workflows.

<Callout icon="lightbulb">
  This lesson is presented for educational purposes (Terraform Associate exam preparation) and is not intended as marketing material.
</Callout>

Welcome to this lesson on HCP Terraform — an introduction tailored for newcomers and for experienced practitioners preparing for the Terraform Associate exam. This guide explains how HashiCorp Cloud Platform (HCP) for Terraform extends the Terraform CLI experience by adding managed services for remote state, collaboration, remote runs, and governance without changing the Terraform language or configuration model.

What is HCP Terraform?

* HCP stands for HashiCorp Cloud Platform.
* HCP Terraform is a hosted, managed service that enables teams to use Terraform to provision infrastructure while adding collaboration, remote state management, and workflow automation.
* HCP Terraform does not replace the Terraform language or providers. You still author the same Terraform configurations — what changes is where runs occur and how teams coordinate around them.

Core capabilities

HCP Terraform delivers several capabilities that benefit teams of all sizes:

* Secure remote state storage (encrypted at rest, locking, versioned state).
* Team collaboration (shared workspaces, role-based access control, audit logs).
* Remote execution (consistent cloud-based plan/apply runs with controlled environments).
* Governance and policy enforcement (native Sentinel support; integrations with tools like OPA are also possible).

<Frame>
  <img alt="The image is an infographic titled &#x22;The Value of HCP Terraform,&#x22; highlighting four benefits: secure remote state storage, team collaboration, remote execution, and governance & policy. Each benefit is briefly described with key features underneath." />
</Frame>

Additional platform features include cost estimation — which estimates cloud spend for public providers before you run `terraform apply` — and drift detection, which alerts you when infrastructure diverges from Terraform-managed configuration.

How HCP Terraform relates to the Terraform CLI

HCP Terraform extends the Terraform CLI experience rather than replacing it. Your existing workflow, providers, modules, and language syntax remain unchanged; HCP adds platform services that centralize and standardize collaboration and execution.

Feature comparison

| Feature area        | Terraform CLI (local/community)              | HCP Terraform (managed)                                    |
| ------------------- | -------------------------------------------- | ---------------------------------------------------------- |
| State storage       | Local `terraform.tfstate` or custom backends | Managed, encrypted remote state with locking               |
| Execution           | Local runs (machine-specific)                | Remote execution in a consistent environment (recommended) |
| Collaboration       | File sharing, CI/CD integration              | Workspaces, RBAC, run visibility, audit logs               |
| Policy & governance | Local/CI checks, ad-hoc tools                | Policy enforcement (Sentinel, OPA integrations)            |
| Cost visibility     | Third-party tools or manual                  | Built-in cost estimation                                   |
| Module sharing      | Public/Private registries manually managed   | Private module registry and governance controls            |

<Frame>
  <img alt="The image compares Terraform Community with HCP Terraform, listing features such as infrastructure as code and rich integrations for the community, and managed remote state storage and RBAC for HCP Terraform." />
</Frame>

Adoption impact for existing Terraform users

Adopting HCP Terraform is designed to be low-friction:

* No need to rewrite Terraform configurations. Resource blocks, data sources, modules, and provider usage remain the same.
* Existing CLI workflows, VCS integration, and CI/CD pipelines continue to work.
* You gain centralized state, audit logging, and RBAC while keeping established processes.
* Adoption can be incremental — start with managed state, then enable remote execution and policy controls when ready.

<Frame>
  <img alt="The image explains how HCP Terraform impacts users, highlighting that existing code remains functional, workflows are leveraged, and adoption can be gradual. It assures users that their skills and processes can transition smoothly to HCP Terraform." />
</Frame>

Workflow with HCP Terraform

The typical Terraform cycle — write → plan → apply — remains the same, but HCP shifts where the plan/apply runs and where state is stored.

1. Write
   * Author Terraform configuration (TF files), variable files, and modules locally.
   * Commit changes to VCS.

2. Plan
   * With remote execution, `terraform plan` is executed in HCP’s environment. The platform evaluates the configuration and sends the plan output back to your CLI for review and collaboration.

3. Apply
   * `terraform apply` runs remotely (when remote execution is enabled). HCP provisions resources and stores state in the workspace — no local `terraform.tfstate` file is required.

This loop repeats as you iterate on infrastructure, now with centralized state, run history, and team visibility.

Remote vs local execution

HCP Terraform supports both remote and local execution modes:

* Remote execution (recommended for teams)
  * Plans and applies run in HCP-managed infrastructure.
  * Enables policy enforcement, cost estimates, run visibility, and audit trails.
  * Run output streams to your CLI for real-time feedback.

* Local execution
  * Your machine runs plans/applies while state is stored in HCP.
  * Useful for providers requiring local resources, local file access, or staged migration.
  * Local execution may not trigger all HCP platform features (for example, some policy checks).

<Frame>
  <img alt="The image compares remote and local execution modes for Terraform, highlighting key differences such as execution location, team recommendation, feature availability, and result streaming." />
</Frame>

Example CLI commands (with remote execution enabled):

```bash theme={null}
$ terraform plan
$ terraform apply
```

Why remote execution matters

* Consistent execution environments and Terraform versions across the team.
* Eliminates “works on my machine” problems caused by local environment differences.
* Runs can continue in HCP even if your laptop disconnects or fails.
* Centralized logs and run metadata improve auditing and troubleshooting.

Connecting your local Terraform configuration to HCP Terraform

To use HCP as the remote backend and optionally enable remote execution, add a `cloud` block to the top-level `terraform` configuration:

```hcl theme={null}
terraform {
  cloud {
    organization = "my-org"
    hostname     = "app.terraform.io"
  }

  workspaces {
    name = "networking-development"
  }
}
```

Notes:

* `organization` is the HCP organization name you create in the HCP Terraform dashboard.
* `workspaces.name` selects the workspace where state, variables, and run history are stored.
* `hostname` defaults to `app.terraform.io` for Terraform Cloud; some HCP deployments may use a different hostname.
* Use `terraform login` to authenticate your CLI to HCP Terraform before running remote plans/applies.

<Callout icon="lightbulb">
  Tip: If you plan a gradual migration, start by using HCP only for managed state (local execution), then enable remote execution once your team is ready. Always run `terraform login` to store HCP credentials for CLI access.
</Callout>

HCP Terraform tiers

Below is an overview to help you choose a tier based on use case. Features and limits change over time — check the official pricing page for current details.

| Tier       | Best for                 | Key features                                                                     |
| ---------- | ------------------------ | -------------------------------------------------------------------------------- |
| Free       | Learning, small projects | Managed state, basic workspace features, up to 500 resources (subject to change) |
| Essentials | Small teams              | Additional team features, more runs, basic collaboration                         |
| Standard   | Production teams         | Drift detection, audit events, policy enforcement (Sentinel), golden patterns    |
| Premium    | Large enterprises        | Private VCS, run tasks, advanced governance and enterprise features              |

For the latest pricing and tier details, see the HCP Terraform pricing page: [https://www.hashicorp.com/products/terraform/pricing](https://www.hashicorp.com/products/terraform/pricing).

Getting started (step-by-step)

1. Sign up for HCP Terraform: visit `https://app.terraform.io/` and create a free account.
2. Create an organization and one or more workspaces in the HCP dashboard.
3. Authenticate your CLI: run `terraform login` and follow the prompts.
4. Add the `cloud` block to your Terraform configuration (see example above).
5. Commit your configuration to VCS and trigger a run (via CLI or VCS integration) to start using managed state and remote execution.

Key takeaways

* HCP Terraform is a managed platform that extends, not replaces, Terraform CLI.
* Your Terraform code, providers, and modules remain unchanged; HCP changes where plan/apply runs and where state is stored.
* Remote execution is recommended for consistent team workflows; local execution with remote state is supported for special cases or migration.
* Adoption is incremental — start with managed state, add remote execution, then enable policy and governance.

Next steps

* Authenticate with HCP using `terraform login`.
* Configure the `cloud` block and workspaces in detail.
* Connect local Terraform to HCP and run example plans/applies.
* Explore Sentinel policies or OPA integrations for governance and compliance.

If you haven't already, create a free HCP Terraform account so you can follow along with the hands-on portions of this course.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/738a4a65-2650-4f59-af4b-feee09f34caf" />
</CardGroup>
