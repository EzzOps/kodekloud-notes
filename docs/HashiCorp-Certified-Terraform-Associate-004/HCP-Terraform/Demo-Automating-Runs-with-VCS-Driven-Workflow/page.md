# Demo Automating Runs with VCS Driven Workflow

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/Demo-Automating-Runs-with-VCS-Driven-Workflow/page

Converting a Terraform Cloud workspace to a VCS-driven workflow where Git commits and pull requests automatically trigger Terraform plans with options for reviewing and auto-applying changes

Now that the Terraform state has been migrated into an HCP (Terraform Cloud) workspace and the workspace is managing both state and configuration, the next step is converting that workspace from a CLI-driven workflow to a VCS-driven workflow. With a VCS-driven workspace, commits to your Git repository automatically trigger Terraform runs (plans) in the workspace, and pull requests can trigger speculative plans for previewing changes.

<Frame>
  <img alt="The image shows a dashboard for a Terraform Cloud workspace named &#x22;hcp-demo,&#x22; displaying details about the latest run triggered via CLI, along with resource and execution metrics." />
</Frame>

Overview — high-level steps

* Push your Terraform configuration to a Git repository (e.g., GitHub).
* Configure your Terraform Cloud workspace to use that repository and branch.
* Commits to the configured branch will trigger runs (plans) automatically; pull requests can trigger speculative plans.
* Review and optionally apply plans from the Terraform Cloud UI or enable Auto-Apply for automatic applies.

Preparing your repository

1. Confirm the repository contains the Terraform files you want Terraform Cloud to run.
2. Push the files to the branch that the workspace will monitor.

Example: verify local git status

```bash theme={null}
