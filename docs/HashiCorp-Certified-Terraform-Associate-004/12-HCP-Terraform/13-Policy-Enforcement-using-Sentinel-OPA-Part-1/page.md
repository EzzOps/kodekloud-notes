# Policy Enforcement using Sentinel OPA Part 1

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/Policy-Enforcement-using-Sentinel-OPA-Part-1/page

Explains HCP Terraform policy enforcement using Sentinel and OPA to evaluate Terraform plans and automatically block non compliant changes during CI/CD

We've built the foundation of HCP Terraform — workspaces, teams, permissions, and a private registry. Now we focus on one of HCP Terraform's most powerful capabilities: automatically enforcing policies on every Terraform run.

Policy enforcement is where governance meets automation. For teams that provision infrastructure continuously, automated policy checks prevent misconfigurations from being deployed. This lecture covers the concepts and mechanics so you can design safe, auditable infrastructure pipelines.

Why this matters

A developer runs a Terraform configuration:

```bash theme={null}
terraform apply
```

Terraform will do exactly what the configuration specifies. If a storage bucket is accidentally made public or a security group is left wide open, Terraform will provision those resources — and the consequences can be severe. Policy enforcement lets you catch such mistakes during the CI/CD flow before resources are ever created.

What is policy as code?

* Codified rules: Security, compliance, and operational controls are written in a policy language so machines can evaluate them consistently.
* Version controlled: Policies live in VCS, are reviewed via pull requests, and follow the same change-management workflow as your infrastructure code.
* Automatically enforced: Policies run on each Terraform run. Checks are executed as part of the pipeline, removing manual gatekeeping and reducing human error.

<Frame>
  <img alt="The image is a slide titled &#x22;Policy as Code&#x22; with two main points: &#x22;Codified Rules&#x22; and &#x22;Version Controlled.&#x22; It highlights writing security and compliance requirements as code and storing them in version control systems for review." />
</Frame>

This is the same evolution we applied with infrastructure-as-code: codify manual processes and automate them. Policy as code applies that same discipline to governance.

Terraform runs without policies

The standard flow without policy enforcement:

* Author Terraform configuration (infrastructure as code).
* Push to HCP Terraform / trigger a run.
* Terraform performs a plan, then apply if the plan succeeds.
* Resources are provisioned in the cloud with no automatic compliance checks between plan and apply.

<Frame>
  <img alt="The image illustrates the process of running Terraform, showing steps from &#x22;Infrastructure as Code&#x22; through &#x22;Plan&#x22; and &#x22;Apply&#x22; to &#x22;Managed Infrastructure,&#x22; with a focus on policies before execution." />
</Frame>

Out of the box, nothing blocks Terraform from applying a plan that is non-compliant — if the plan is valid and the provider accepts it, apply proceeds.

Terraform runs with policy enforcement

With policy enforcement enabled, HCP Terraform introduces a policy check step between plan and apply:

* Push configuration → run starts → plan phase
* Plan succeeds → policy check phase (evaluates the plan)
* Policies pass → apply phase → managed infrastructure
* Policies fail → run is blocked (depending on enforcement level)

Policies analyze the Terraform plan (the proposed changes), not existing resources. This lets you prevent problematic changes before anything is provisioned.

<Frame>
  <img alt="The image is an infographic outlining the steps in a &#x22;Policy Check&#x22; process, highlighting the evaluation of plan data, the potential blockage of applications if policies fail, and access to cost estimation data. It features a purple color scheme with icons and text." />
</Frame>

Common policy use cases

* Restrict allowed regions or account IDs.
* Block public access to storage buckets.
* Disallow open security group rules or SSH from the Internet.
* Enforce instance sizing, tagging, or naming standards.
* Reject plans that exceed a monthly cost threshold (cost-aware policies).

Key facts about the policy check phase

| Fact                | Behavior                                                                   |
| ------------------- | -------------------------------------------------------------------------- |
| Policy input        | Policies evaluate the Terraform plan data (the proposed changes).          |
| Timing              | Policies run after a successful plan and before apply.                     |
| Blocking            | Failed policies can block apply depending on enforcement level.            |
| Cost data           | Sentinel policies can access HCP cost estimates to reject expensive plans. |
| No plan = no policy | If plan fails (compilation or provider errors), policies are not executed. |

Two policy frameworks in HCP Terraform

HCP Terraform supports two frameworks: HashiCorp Sentinel and Open Policy Agent (OPA). You can choose one or use both in the same environment.

| Framework  | Language                 | Strengths                                                                                                                           | Links                                                                                |
| ---------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Sentinel   | Sentinel policy language | Tight integration with HashiCorp products; official policy library and support; access to HCP-specific imports (e.g., `tfplan/v2`). | [https://developer.hashicorp.com/sentinel](https://developer.hashicorp.com/sentinel) |
| OPA (Rego) | Rego                     | CNCF project with broad community ecosystem; used across Kubernetes, CI systems, proxies; many open-source Rego policies available. | [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)                 |

Sentinel

* Built and maintained by HashiCorp.
* Deep integration with Terraform/HCP features and imports.
* Good starting point if you rely heavily on HashiCorp tooling and HashiCorp-provided policies.

OPA

* CNCF-graduated project with a large ecosystem.
* Rego is expressive for policies over structured data.
* Ideal when you want a cloud-native, multi-platform policy solution.

What real policies look like

Below are concrete examples showing the typical pattern: read the Terraform plan, evaluate conditions, and return pass/fail results.

Sentinel example (GCP): ensure SSH access is not open to the Internet

```sentinel theme={null}
import "tfplan/v2" as tfplan

unsupported = [
    "0.0.0.0/0",
    "::/0",
]

firewalls = filter tfplan.resource_changes as _, r {
    r.type is "google_compute_firewall" and
    r.mode is "managed" and
    (r.change.actions contains "create" or r.change.actions contains "update")
}

ssh_allows_public = any firewalls as _, fw {
    any fw.change.after.allow as _, allow {
        allow.ports contains "22" and
        any fw.change.after.source_ranges as _, sr {
            sr in unsupported
        }
    }
}

main = rule {
    not ssh_allows_public
}
```

* The policy imports plan data via `tfplan/v2`.
* It defines unsupported source ranges representing the public Internet.
* It filters for managed `google_compute_firewall` resources being created or updated and inspects their post-change attributes.
* If any rule allows port 22 from `0.0.0.0/0` or `::/0`, the `main` rule fails and blocks the run.

OPA / Rego example (AWS): detect security groups allowing ingress from 0.0.0.0/0

```rego theme={null}
package terraform.policy

deny[msg] {
  rc := input.resource_changes[_]
  rc.type == "aws_security_group"
  rc.change.after.ingress[_] == ingress
  ingress.cidr_blocks[_] == "0.0.0.0/0"
  msg = sprintf("Security group %s allows ingress from 0.0.0.0/0", [rc.address])
}
```

* This Rego policy iterates the plan's resource changes.
* It looks for `aws_security_group` resources whose ingress rules include the CIDR `0.0.0.0/0`.
* When found, it emits a deny message identifying the resource, causing the policy to fail.

Both examples demonstrate how policies consume the plan, evaluate conditions, and decide whether a run can proceed. The difference is primarily the language and ecosystem: Sentinel for tight HashiCorp integration, Rego for broader cloud-native use.

<Callout icon="lightbulb">
  Policies run only on successful plans. If a plan fails compilation or provider validation, policy checks are not executed because there is no plan data to evaluate.
</Callout>

Links and references

* HashiCorp Sentinel: [https://developer.hashicorp.com/sentinel](https://developer.hashicorp.com/sentinel)
* Open Policy Agent (OPA): [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)
* HCP Terraform policy enforcement (HCP docs) — search HCP Terraform policy enforcement in the HashiCorp docs for workspace-specific setup steps.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/a60c20ce-8030-4832-8fdd-344d46ef7037" />
</CardGroup>
