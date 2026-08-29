# Policy Enforcement using Sentinel OPA Part 2

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/Policy-Enforcement-using-Sentinel-OPA-Part-2/page

Explains HCP Terraform policy enforcement with Sentinel and OPA, comparing enforcement levels, policy set management, capabilities and limits, and practical governance best practices.

Policy enforcement behavior depends on the enforcement level you choose. Understanding enforcement levels is critical for effective governance and minimizing disruption to teams.

## Enforcement levels comparison

Sentinel supports three enforcement levels and OPA uses two. The table below summarizes their behavior and override characteristics.

| Framework  | Enforcement levels | Behavior                                                                                                                                               | Can be overridden?                                   |
| ---------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Sentinel   | Advisory           | Produces a warning; the run continues. Useful for introducing policies gradually.                                                                      | N/A                                                  |
| Sentinel   | Soft-mandatory     | Blocks the run, but users with the appropriate HCP Terraform permission can override. Overrides are logged for auditing.                               | Yes — requires overrides permission in HCP Terraform |
| Sentinel   | Hard-mandatory     | Blocks the run and cannot be overridden. Use for non-negotiable controls (e.g., regulatory requirements).                                              | No                                                   |
| OPA (Rego) | Advisory           | Same as Sentinel advisory: warning, run continues.                                                                                                     | N/A                                                  |
| OPA (Rego) | Mandatory          | Blocks the run. In HCP Terraform, a properly permissioned user can override, which makes it behave similarly to Sentinel’s soft-mandatory in practice. | Yes — when using HCP Terraform override permissions  |

<Frame>
  <img alt="The image describes three Sentinel Enforcement Levels: Advisory, Soft Mandatory, and Hard Mandatory, detailing the actions and permissions associated with each level." />
</Frame>

Summary: Sentinel exposes three distinct enforcement modes (advisory → soft-mandatory → hard-mandatory). OPA uses advisory and mandatory; on HCP Terraform the mandatory OPA enforcement can be overridden with the right permissions.

## Organizing policies in HCP Terraform

Best practice is to author policies inside your HCP Terraform organization and then assign them to workspaces through policy sets. You can mix frameworks across your organization — some policies may be Sentinel (HashiCorp) and others OPA (Rego) — but policies are attached via sets, not individually to workspaces.

Example setup:

* Sentinel policies: require mandatory tags, restrict instance types, enforce S3 encryption.
* OPA policies: block public ingress, limit auto-apply.

After writing policies, attach them (via policy sets) to the appropriate workspaces so every run is evaluated against the assigned sets.

<Frame>
  <img alt="The image shows a diagram titled &#x22;Develop Policies&#x22; with a list of policies that are assigned to multiple workspaces for enforcement." />
</Frame>

## Policy sets: grouping and scope

Policy sets are containers for related policies. Think of a policy set like a team or project grouping — they make governance scalable and consistent.

Key constraints and behaviors:

* A single policy set may contain policies from only one framework (Sentinel OR OPA). Mixing frameworks inside one policy set is not allowed.
* You can attach both a Sentinel policy set and an OPA policy set to the same workspace; both sets will be evaluated during runs.
* Policy sets can be scoped at multiple levels: global, by project, or to specific workspaces.
* You can exclude individual workspaces from a policy set for exceptions.
* Policy sets can be managed via the HCP Terraform UI, VCS-backed workflows, or the HCP API.

<Frame>
  <img alt="The image shows a diagram titled &#x22;Policy Sets&#x22; with two main categories: &#x22;Policies&#x22; and &#x22;Policy Sets&#x22; including &#x22;Sentinel - Security&#x22; and &#x22;OPA - Security&#x22;. Various policies like &#x22;stl-require-mandatory-tags&#x22; are listed under each section." />
</Frame>

<Frame>
  <img alt="The image is a slide about &#x22;Policy Sets,&#x22; highlighting features such as grouping policies, framework exclusivity, scoping options, workspace exclusion, and management methods." />
</Frame>

## What policies can and cannot do

Understanding the limits of provisioning-time policies will help you design a complete governance strategy.

What policies can do (examples)

* Block creation of public S3 buckets by inspecting the Terraform plan and refusing runs that would create a publicly accessible bucket.
* Restrict allowed instance types (e.g., only allow `t3.medium` and `t3.large`).
* Enforce required tags (e.g., every resource must have `team`, `environment`, and `cost-center` tags).
* Limit regions for deployment (e.g., allow only `us-east-1` and `eu-west-1`).
* Enforce cost controls: Sentinel policies can access cost estimation data to enforce spending constraints.

What policies cannot do

* Continuously monitor resources after deployment — they run only during plan/apply and do not provide ongoing monitoring.
* Remove or remediate existing resources — policies prevent new violations but do not modify or delete already-provisioned resources.
* Validate existence of external resources referenced by configuration (e.g., a policy can require a KMS key ID be supplied, but cannot prove the key actually exists in AWS).
* Analyze runtime behavior of deployed applications — runtime security and observability must be handled by other tooling.

<Frame>
  <img alt="The image outlines examples of what policies can do, such as blocking public S3 buckets, and what they cannot do, like continuously monitoring after deployment." />
</Frame>

## Practical tips

* Start new policies as advisory so teams can adapt without being blocked; promote them to mandatory/soft-mandatory once validated.
* Use policy sets to enforce consistent controls across projects and to simplify exceptions management.
* Audit overrides: require and monitor override actions to prevent policy erosion.
* Combine HCP Terraform policy enforcement with runtime monitoring and security tools for full lifecycle protection.

## Key points recap

* Policies evaluate after the plan phase but before apply, preventing misconfigurations from being provisioned.
* HCP Terraform supports both Sentinel (HashiCorp) and OPA (Rego).
* Enforcement levels:
  * Sentinel: advisory, soft-mandatory (overridable), hard-mandatory (non-overridable).
  * OPA: advisory and mandatory (HCP Terraform’s permissions allow overrides, making mandatory behave like soft-mandatory in practice).
* Policy sets group policies by framework and can be scoped globally, to projects, or to specific workspaces; you can exclude specific workspaces.
* Overriding a failed policy requires the managed `overrides` permission in HCP Terraform and override actions are logged for auditing.
* Exam note: the focus is on high-level concepts (frameworks, enforcement levels, policy sets, integration points), not on authoring Sentinel or Rego code.

> **lightbulb** Remember: policies are a provisioning-time control. They are powerful for preventing new misconfigurations, but they’re not a substitute for continuous monitoring and runtime security controls.

## Links and references

* HCP Terraform (Policy Enforcement): [https://www.hashicorp.com/products/terraform](https://www.hashicorp.com/products/terraform)
* Sentinel documentation: [https://www.hashicorp.com/sentinel](https://www.hashicorp.com/sentinel)
* Open Policy Agent (OPA) and Rego: [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)

That concludes this lesson on policy enforcement with Sentinel and OPA. I hope it was helpful.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/ade9d757-2ec9-4a5e-9b7d-629be6bd2438)
