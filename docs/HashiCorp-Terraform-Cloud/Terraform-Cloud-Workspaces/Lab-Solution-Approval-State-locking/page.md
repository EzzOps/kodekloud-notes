# Lab Solution Approval State locking

Source: https://notes.kodekloud.com/docs/HashiCorp-Terraform-Cloud/Terraform-Cloud-Workspaces/Lab-Solution-Approval-State-locking/page

Learn how Terraform Cloud manages state locks to prevent concurrent modifications and explore workspace locking configurations.

In this lab, you’ll learn how Terraform Cloud manages state locks to prevent concurrent state modifications. You’ll configure a remote backend, run a standard Terraform workflow, and explore both automatic and manual workspace locking.

## Prerequisites

* Terraform CLI installed (v1.0+ recommended)
* Terraform Cloud account with access to the `Mastering-Terraform-CI` organization
* An existing Terraform workspace named `devops-aws-myapp-dev`

<Callout icon="lightbulb">
  Ensure you have **Workspace Admin** privileges in Terraform Cloud to manage locks.
</Callout>

***

## 1. Configure the Remote Backend

Update your Terraform configuration to use Terraform Cloud as the remote backend:

```hcl theme={null}
terraform {
  cloud {
    organization = "Mastering-Terraform-CI"

    workspaces {
      name = "devops-aws-myapp-dev"
    }
  }
}
```

Commit this change to your repository before proceeding.

***

## 2. Authenticate and Initialize

1. Log in to Terraform Cloud:
   ```bash theme={null}
   terraform login
   ```
2. Clone the sample repo and initialize:
   ```bash theme={null}
   git clone https://github.com/hashicorp/tfc-getting-started.git
   cd tfc-getting-started
   terraform init
   scripts/setup.sh
   ```

You should see output similar to:

```plaintext theme={null}
Initializing Terraform Cloud...

Initializing provider plugins...
- Finding hashicorp/aws versions matching ">= 3.73.0, < 4.0"...
- Installing hashicorp/aws v4.32.0...
- Installed hashicorp/aws v4.32.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections. Include this file in your version control repository.

Terraform Cloud has been successfully initialized!
```

***

## 3. Run Terraform Plan & Apply

When you execute `terraform plan` or `terraform apply`, Terraform Cloud:

* Queues the run
* Automatically locks the workspace during execution
* Prevents other runs until the lock is released

```bash theme={null}
terraform plan
terraform apply
```

After a successful apply, you’ll see:

```plaintext theme={null}
Apply complete! Resources: 23 added, 0 changed, 0 destroyed.

Outputs:

clumsy-bird-ip  = "http://54.235.109.203:8001"
clumsy-bird-url = "http://ec2-54-235-109-203.compute-1.amazonaws.com:8001"
```

Commit any changes before moving on.

***

## 4. Understanding Lock Types

| Lock Type      | Trigger                     | Description                                                    |
| -------------- | --------------------------- | -------------------------------------------------------------- |
| Automatic Lock | `plan` / `apply` operations | Terraform Cloud locks the workspace during runs automatically. |
| Manual Lock    | User action in UI           | Administrators can prevent new runs until they unlock.         |

***

## 5. Manually Locking a Workspace

You can manually lock your workspace to halt any new runs:

1. In Terraform Cloud UI, go to **Workspaces > devops-aws-myapp-dev**.
2. Click **Lock workspace**.

You’ll see who owns the lock and any queued runs will wait:

<Frame>
  ![The image shows a KodeKloud lab interface for Terraform Cloud Workspaces, with instructions to unlock a workspace and a terminal window displaying a file explorer with Terraform files.](https://kodekloud.com/kk-media/image/upload/v1752878926/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Approval-State-locking/kodekloud-terraform-cloud-workspaces-lab.jpg)
</Frame>

<Callout icon="triangle-alert">
  Queued runs remain in the **Pending** state until the lock is released. Ensure this doesn’t block critical deployments.
</Callout>

***

## 6. Unlocking the Workspace

Once you're ready to proceed:

1. Navigate to **Manage lock** in the workspace settings.
2. Click **Unlock**.

<Frame>
  ![The image shows a Terraform Cloud workspace settings page with a focus on the "Locking" section, indicating the workspace is currently unlocked. A success message confirms the workspace has been unlocked.](https://kodekloud.com/kk-media/image/upload/v1752878927/notes-assets/images/HashiCorp-Terraform-Cloud-Lab-Solution-Approval-State-locking/terraform-cloud-workspace-locking-settings.jpg)
</Frame>

After unlocking, any pending runs will automatically move forward through plan and apply phases.

***

## Next Steps

* Automate approvals with [Run Tasks][run-tasks]
* Explore [Sentinel Policies][sentinel] to enforce compliance
* Integrate with VCS for pull request workflows

## Links and References

* [Terraform Cloud Documentation][tfc-docs]
* [Terraform CLI Command Reference][cli-ref]
* [Terraform Cloud API: Runs][api-runs]

[run-tasks]: https://www.terraform.io/docs/cloud/run-tasks/index.html

[sentinel]: https://www.terraform.io/docs/cloud/sentinel/index.html

[tfc-docs]: https://www.terraform.io/docs/cloud/index.html

[cli-ref]: https://www.terraform.io/docs/cli/index.html

[api-runs]: https://www.terraform.io/docs/cloud/api/runs.html

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-terraform-cloud/module/69fc91b2-bf0f-4922-831c-2aee42d19b03/lesson/537f3a1e-69b2-4fbf-afec-5664f7cff4fd" />
</CardGroup>
