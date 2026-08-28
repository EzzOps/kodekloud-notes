# Understanding State Drift Visual Walkthrough Lightboard

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/Understanding-State-Drift-Visual-Walkthrough-Lightboard/page

Explains Terraform state drift, how plan detects mismatches, and practical ways to reconcile by reverting or adopting external changes while maintaining IaC best practices.

All right — Terraform state.

You either love it or you hate it, but it’s essential to reliable infrastructure as code. In this guide you’ll learn what happens when your Terraform state diverges from real-world infrastructure (known as Terraform state drift), how Terraform detects that divergence, and practical ways to reconcile or adopt changes.

Why this matters

* Drift breaks the guarantees provided by IaC: reproducibility, auditability, and safe automation.
* Detecting drift early prevents unexpected infrastructure changes and outages.
* Choosing the right remediation keeps your Terraform configuration, state, and real resources aligned.

Conceptual setup

* You author Terraform configuration files that describe your desired infrastructure.
* Running Terraform records known resources and their attributes in the state file.
* Terraform then creates or updates real resources in the provider (for example, VMs).

After a successful apply, three things are expected to match:

* Desired configuration = Terraform configuration files
* State = Terraform state file
* Real world = Provider-managed resources

| Piece                 | What it represents                     | Example                                          |
| --------------------- | -------------------------------------- | ------------------------------------------------ |
| Desired configuration | Source of truth written in HCL         | `main.tf` resource blocks for two web servers    |
| State                 | Terraform's recorded view of resources | `terraform.tfstate` (local or remote backend)    |
| Real world            | Actual cloud resources                 | Instances and attributes in the provider console |

Imagine a simple configuration that defines two web servers. One is intended to have two CPUs and moderate memory; the other, one CPU and a lot of memory. After you apply the configuration, the configuration, the state, and the real cloud resources all align.

Drift scenario

If someone or something modifies a resource outside Terraform (for example, a colleague in the cloud console, a maintenance script, or an automated pipeline), the real resource can change without Terraform updating either the state file or your configuration. That mismatch is state drift: state ≠ real world.

<Frame>
  <img alt="A person stands in front of a transparent board with blue diagrams depicting a Terraform setup process involving state management." />
</Frame>

Example: user changes a VM directly

Suppose someone edits a VM instance in the cloud console and swaps CPU and memory values on one of the web servers. After that manual change:

* Real-world VM attributes no longer match Terraform’s state file.
* The Terraform configuration files still express the original desired values.
* Terraform’s state remains stale until a refresh occurs.

This is drift — and it’s what `terraform plan` is designed to detect.

How Terraform detects drift

* When you run `terraform plan`, Terraform first refreshes the state by querying the provider for current attributes of managed resources.
* It compares the refreshed state against the configuration you’ve authored.
* Any differences that require action will be shown in the plan output as proposed changes.

Example commands

```bash theme={null}
