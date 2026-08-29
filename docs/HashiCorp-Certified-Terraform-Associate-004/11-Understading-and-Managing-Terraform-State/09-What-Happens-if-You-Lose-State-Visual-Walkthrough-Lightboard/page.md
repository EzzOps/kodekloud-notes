# See what would change (this triggers a refresh)
terraform plan

# Apply configuration changes to make real resources match the config
terraform apply
```

Resolving drift — two approaches

You have two main options when you detect drift: revert the external change, or adopt it.

1. Revert the external change (make real resources match your configuration)

* Keep the configuration as the source of truth.
* Use Terraform to change the real resource back to your desired values.

Typical workflow:

```bash theme={null}
terraform plan
terraform apply
```

After `apply`, Terraform calls the provider APIs to modify the real resource and then updates the state file so configuration, state, and reality match again.

2. Accept the external change (make Terraform state and configuration reflect the new real-world state)

* If the external change was intentional and should become the desired state, update Terraform’s recorded state and then your configuration.
* Use `terraform apply -refresh-only` to refresh the state from the provider and write those values into the state file without changing infrastructure.

Workflow to adopt an external change:

```bash theme={null}
# Refresh and write the provider's current state into state file only
terraform plan
terraform apply -refresh-only

# Then update your HCL configuration to match the new reality, and apply
# (if configuration matches refreshed state, apply will perform no real changes)
terraform plan
terraform apply
```

<Callout icon="lightbulb">
  `terraform plan` refreshes the state from the provider and compares it to your configuration. Use `terraform apply -refresh-only` to update state without making infrastructure changes when you want Terraform to adopt external updates.
</Callout>

Practical notes and recommendations

* Reverting external changes with `terraform apply` ensures the configuration remains the single source of truth.
* Accepting external changes with `-refresh-only` writes the provider state into Terraform’s state file; follow this with configuration updates so IaC stays authoritative.
* Enforce change control: restrict direct console edits via IAM, require PRs, or centralize changes through a CI/CD pipeline that runs Terraform.
* Consider state locking (backends like S3 + DynamoDB, or remote backends) to prevent concurrent modifications to state.

Quick reference — common commands

| Command                         | Purpose                                                                |
| ------------------------------- | ---------------------------------------------------------------------- |
| `terraform plan`                | Refresh state from provider and show proposed changes                  |
| `terraform apply`               | Reconcile configuration with real resources (update resources & state) |
| `terraform apply -refresh-only` | Refresh and update state only, do not change real resources            |
| `terraform state`               | Inspect or manipulate the state file (advanced use cases)              |

<Callout icon="warning">
  Avoid relying on `-refresh-only` as a permanent workaround. Prefer workflows where all changes go through Terraform so configuration, state, and real resources remain consistent and auditable.
</Callout>

Summary

* Terraform state drift happens when real-world resources diverge from the state file and configuration.
* `terraform plan` detects drift by refreshing state and comparing it to configuration.
* To revert drift, run `terraform apply` to make real resources match the configuration.
* To accept drift, run `terraform apply -refresh-only`, then update your configuration and apply.

Links and references

* [Terraform CLI Docs — plan](https://www.terraform.io/cli/commands/plan)
* [Terraform CLI Docs — apply](https://www.terraform.io/cli/commands/apply)
* [Terraform State Documentation](https://www.terraform.io/language/state)
* [Best practices for Terraform state management](https://www.terraform.io/docs/cloud/run/state-management.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/61bd1ccb-f0e8-4e48-9fc5-2984237200dd" />
</CardGroup>


# What Happens if You Lose State Visual Walkthrough Lightboard

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/What-Happens-if-You-Lose-State-Visual-Walkthrough-Lightboard/page

Explains consequences of losing Terraform state and recovery methods including restoring state, re-importing resources, and best practices to prevent state loss.

Terraform state is Terraform’s “memory” of the real-world resources it manages. This guide walks through a simple scenario—five virtual machines—showing what happens if Terraform loses access to its state file, and how to recover safely.

Imagine a Terraform configuration that defines five virtual machines. You run `terraform apply`, and the state file is stored remotely (for example, in an S3 bucket). Configuration, state, and cloud resources are all in sync.

<Frame>
  <img alt="A person is writing on a transparent board, creating a diagram with numbered squares in one section and arrows pointing to a box labeled &#x22;S3&#x22;." />
</Frame>

Now you have five VMs running in the cloud and a state file that records those resources.

<Frame>
  <img alt="The image shows a person standing in front of a blackboard, drawing a flowchart with boxes and arrows labeled with numbers, &#x22;S3,&#x22; and &#x22;CLOUD.&#x22;" />
</Frame>

If the state file is deleted, corrupted, or otherwise inaccessible, Terraform no longer knows about the existing infrastructure. With the same configuration files, running `terraform plan` or `terraform apply` makes Terraform behave as if it’s starting from scratch.

<Frame>
  <img alt="A person is standing in front of a transparent board with a diagram drawn in blue and orange marker, illustrating a process from a group of numbered boxes to the cloud, bypassing a labeled section marked &#x22;S3.&#x22;" />
</Frame>

Because the state is missing, Terraform will query the cloud for resources but—finding no local state entries—it will plan to create the five VMs described in your configuration. This results in Terraform attempting to provision new resources in addition to the ones already running in your cloud, since it can’t tell they already exist.

In short: losing the Terraform state causes Terraform to try to re-create resources it believes are absent unless you recover the state or re-associate existing resources with your configuration.

Recovery options

1. Restore the state file

* If you use a remote backend (for example, an [Amazon S3](https://aws.amazon.com/s3/) bucket), check for backups or enablement of versioning. Restoring a prior `terraform.tfstate` is often the fastest way to recover.
* Restore the backup/version of `terraform.tfstate` into the remote backend so Terraform can pick it up.

<Frame>
  <img alt="The image shows a person standing in front of a transparent board with a diagram illustrating a &#x22;terraform plan,&#x22; featuring boxes, arrows, and cloud-related elements." />
</Frame>

<Callout icon="lightbulb">
  Enable remote backend versioning and periodic backups (for example, S3 versioning or GCS object versioning). Store copies of `terraform.tfstate` so state restoration is straightforward when needed.
</Callout>

2. Re-import existing resources into state
   If you cannot restore a prior state file, re-associate real resources with your Terraform configuration using `terraform import` (official docs: [https://developer.hashicorp.com/terraform/cli/commands/import](https://developer.hashicorp.com/terraform/cli/commands/import)). The workflow:

* Ensure your Terraform configuration contains resource blocks that match the resources you want to manage. Create or update resource blocks first so each real resource has a corresponding address.
* Use `terraform import` to map each existing cloud resource into the matching resource block address.

Example: import a single EC2 instance into a resource named `aws_instance.web`:

```bash theme={null}
terraform import aws_instance.web i-0123456789abcdef0
```

If the resources were created with `count` or `for_each`, import using the indexed address:

```bash theme={null}
terraform import 'aws_instance.web[0]' i-0123456789abcdef0
```

After importing every resource, run:

```bash theme={null}
terraform plan
```

Terraform will list imported resources in state and display differences between your configuration and the actual resource attributes. Adjust either the configuration or the real resources so they match.

<Callout icon="warning">
  Import is a per-resource operation and can be time-consuming for large fleets. Always run `terraform plan` after imports and review planned changes before `terraform apply` to avoid unintended modifications or replacements.
</Callout>

Tips for successful imports

* Add resource blocks to your configuration before importing so you have deterministic addresses to import into.
* Import each resource (or each indexed element) individually; there’s no bulk-import native to Terraform core.
* Use `terraform state list` and `terraform state show` after importing to inspect entries and verify attributes.
* When possible, prefer reconciling configuration to actual resource attributes rather than changing resources to match configuration.

Why a config-driven recovery is best

* A configuration-first approach (define resources in code, then import real resources into those blocks) restores state while preserving a version-controlled source of truth. This avoids adhoc fixes and helps teams understand intended infrastructure.

Recovery options at a glance

| Recovery method     | When to use                            | Notes                                                  |
| ------------------- | -------------------------------------- | ------------------------------------------------------ |
| Restore state file  | You have backups or backend versioning | Fastest, simplest; restores exact prior state          |
| Re-import resources | No backups available                   | Safe but manual; ensure config matches real resources  |
| Recreate resources  | When resources are disposable or cheap | Risky for production—can cause duplicates or lost data |

Recap

* Losing Terraform state causes Terraform to treat existing resources as absent and plan to recreate them.
* Recovery approaches:
  * Restore the state file from backend versioning or backups (recommended if available).
  * Re-import existing resources into properly defined resource blocks using `terraform import`.
* Best practices to avoid or mitigate state loss:
  * Use remote backends (S3, GCS, Terraform Cloud).
  * Enable object/version backups.
  * Store Terraform configuration in source control.
  * Periodically back up state snapshots and test recovery procedures.

Links and references

* [Terraform import command docs](https://developer.hashicorp.com/terraform/cli/commands/import)
* [Amazon S3](https://aws.amazon.com/s3/)
* [Google Cloud Storage](https://cloud.google.com/storage/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/8db96827-5798-42a8-9939-dbea3af2ab82" />
</CardGroup>
