# local repository
git status
```

Sample output:

```plaintext theme={null}
On branch main
No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        main.tf
        providers.tf
        variables.tf
```

Initial Terraform configuration
Below is the initial `main.tf` used in this demo — a simple VPC and a private subnet.

```hcl theme={null}
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "dev-main-vpc"
    Environment = "development"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = var.private_subnet_az

  tags = {
    Name = "main-subnet"
  }
}
```

Stage and push these files to your remote repository:

```bash theme={null}
git add main.tf providers.tf variables.tf
git commit -m "initial Terraform configuration"
git push origin main
```

Successful push feedback (example):

```plaintext theme={null}
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 10 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 945 bytes | 945.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
To https://github.com/your-org/hcp-demo.git
   adlae35..6fb376a  main -> main
```

Configure the workspace to use VCS

1. In Terraform Cloud, open the workspace.
2. Go to Settings → Version Control.
3. Connect or select your VCS provider (GitHub, GitLab, Bitbucket, Azure DevOps, etc.).
4. Pick the repository and branch you pushed your code to, and save the settings.

<Frame>
  <img alt="The image shows a web interface for configuring version control settings in Terraform Cloud, where a repository is being selected for hosting Terraform source code." />
</Frame>

VCS configuration options

* Working directory: set a subdirectory if your Terraform root is not at the repository root (leave blank for root).
* Auto-apply: enable to automatically apply successful plans.
* Trigger type: branch or tag based; pull request behavior (speculative plans) depends on provider and integration settings.

> **lightbulb** Connecting a workspace to VCS enables automatic plans whenever commits are pushed; pull requests can trigger speculative plans. You can enable Auto-Apply to apply changes automatically after a successful plan, but it’s common to require manual approval for production-sensitive workspaces.

First run after connecting VCS
As soon as the workspace is connected to the repository and branch, Terraform Cloud queues an initial plan. This first run maps the repository configuration to the state currently managed by the workspace. In many cases this initial plan will report no changes if the state and configuration already match.

<Frame>
  <img alt="The image shows a Terraform Cloud web interface with a workspace titled &#x22;hcp-demo.&#x22; It displays details about the latest run, resources, and settings." />
</Frame>

Demonstrating an update via VCS
To demonstrate how commits trigger runs, update your local configuration (for example, add environment tags to the private subnet and create a public subnet). The updated portion of `main.tf`:

```hcl theme={null}
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = var.private_subnet_az

  tags = {
    Name        = "main-subnet"
    Environment = "development"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.public_subnet_az
  map_public_ip_on_launch = true

  tags = {
    Name        = "public-subnet"
    Environment = "development"
  }
}
```

Commit and push the changes:

```bash theme={null}
git status
git add main.tf
git commit -m "add environment tags and public subnet"
git push origin main
```

Example push output:

```plaintext theme={null}
Counting objects: 5, done.
Delta compression using up to 10 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 297 bytes | 297.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
To https://github.com/your-org/hcp-demo.git
   6fb376a..e9daeed  main -> main
```

Automatic runs and reviewing plans
After the push completes, Terraform Cloud detects the commit and automatically triggers a run for the workspace. If this change were part of a pull request, Terraform Cloud would present a speculative plan tied to that PR. Each run is associated with the commit that triggered it so you can see exactly what Terraform will change.

<Frame>
  <img alt="The image shows a Terraform Cloud interface displaying run details of a plan that changed subnet tags to &#x22;development,&#x22; with a focus on AWS subnets configuration." />
</Frame>

From the run details you can:

* Review the plan, then click Confirm & Apply to execute the changes, or
* Enable Auto-Apply so successful plans are applied automatically.

I chose Confirm & Apply in this demo. Terraform Cloud executed the apply, updated the workspace state, and created a new state version. You can verify the new state under the workspace States tab.

Benefits of a VCS-driven Terraform workflow

| Benefit                  | Description                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| Versioned IaC            | Keep your infrastructure-as-code in Git with commit history and diffs.                           |
| Automated runs           | Commits trigger plans automatically; PRs can trigger speculative plans for pre-merge validation. |
| Auditing & visibility    | See who triggered runs and why; Terraform Cloud logs runs and state versions for compliance.     |
| Flexible apply workflows | Choose manual Confirm & Apply for control or Auto-Apply for automation.                          |

Links and references

* [Terraform Cloud Version Control documentation](https://www.terraform.io/cloud)
* [GitHub](https://github.com) — example VCS provider used in this demo
* [Terraform state and workspaces](https://www.terraform.io/docs/state)

Next steps
With the workspace now VCS-connected, you can extend this pattern to:

* Create additional workspaces per environment (dev, staging, prod),
* Use workspace variables and policies to enforce guardrails,
* Integrate CI/CD pipelines to manage more complex workflows.

Now that the workspace is VCS-driven, subsequent changes to infrastructure will be governed by commits and PR workflows, improving collaboration, traceability, and automation.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/d974ecea-d6d2-4c48-b872-597eedf5f9e4)


# Demo Creating Variable Sets

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/HCP-Terraform/Demo-Creating-Variable-Sets/page

How to create and manage Terraform Cloud variable sets at organization and project levels, apply scopes to workspaces, and understand precedence and Priority for overriding variables.

Welcome back to [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004). In this lesson we demonstrate how to create and apply Terraform Cloud variable sets at the organization and project levels, and how variable precedence works when sets are applied to workspaces.

What you’ll learn

* How to create an organization-level variable set and apply it organization-wide or to specific projects/workspaces.
* How to create a project-level variable set and scope it to a project or its workspaces.
* How variable precedence (including the Priority option) affects the effective value in a workspace.

Open your Terraform Cloud organization and navigate to Settings → Variable Sets.

<Frame>
  <img alt="The image shows a Terraform Cloud interface displaying a list of workspaces, their run status, associated repositories, and latest change timestamps. The sidebar includes options for managing projects, stacks, registry, usage, and settings." />
</Frame>

## Create an organization-level variable set

Steps:

1. Go to Settings → Variable Sets and click Create variable set → Organization.
2. Give the set a clear name and description (for example: Name: `AWS Production`, Description: `production credentials`).
3. Choose the scope:
   * Apply to all projects and workspaces (organization-wide)
   * Apply to specific projects and workspaces

Organization-level variable sets are useful for values shared across many projects or workspaces (for example, organization-wide configuration or shared service credentials). If you need strict isolation for secrets, prefer narrowly scoped sets or other secret management practices.

When applying to specific projects, any current or future workspaces within those projects will inherit the variable set automatically.

<Frame>
  <img alt="The image shows a web interface for creating a new variable set in Terraform Cloud. It includes options to apply the variable set to specific projects and workspaces." />
</Frame>

### Variable set priority

At the bottom of the variable set creation screen there is a Priority option:

* When Priority is enabled, variables in the variable set will override variables with the same name in more specific scopes (for example, workspace-level variables).
* When Priority is unchecked, the usual precedence applies where more specific scopes (workspace) override less specific ones (organization/project).

## Adding variables to the set

* Click Add variable to create entries in the set. For each entry choose if it is a Terraform variable or an environment variable.
* Mark secret values as Sensitive — these are encrypted and hidden in the UI.
* Example AWS credential names:
  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`

After adding variables, click Create variable set. The new organization-level set will appear in the Variable Sets list with its scope and variables visible to users with the appropriate permissions.

<Frame>
  <img alt="The image shows a Terraform Cloud settings page for variable sets, specifically focusing on variable set scope and priority, with an example of a sensitive access key variable." />
</Frame>

## Create a project-level variable set

You can create variable sets from within a project:

1. Navigate to the project (for example, `HCP demo`) → Settings → Variable Sets.
2. Click Create variable set → Project.
3. Name the set, choose scope (entire project or specific workspaces within the project), add variables, and mark Sensitive values as needed.
4. Optionally enable Priority if you want this set to override workspace-level values.

Notes:

* Project-level variable sets are visible only within the project.
* You cannot create an organization-wide scope from inside a project — organization-level sets must be created from the organization Settings page.
* Workspaces not associated with the project will not appear in the selection list.

When applied, the project-level set is inherited by the selected workspaces or by all workspaces in the project depending on the chosen scope.

When you open a workspace’s Variables page you’ll see all applied variable sets (organization, project, workspace) and which variables are inherited from each.

<Frame>
  <img alt="The image shows a web interface for managing variable sets in Terraform, displaying sections for &#x22;project-variable-set&#x22; with no variables added, and &#x22;aws-production&#x22; with sensitive AWS credentials." />
</Frame>

## Variable scope and precedence

Use the following quick reference to decide where to place variables and how precedence works.

| Scope option      | When to use                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Organization-wide | Shared values that must be available to many projects/workspaces (non-sensitive config or centrally managed secrets if appropriate) |
| Project-level     | Values scoped to a single project and its workspaces (team-level configs or project-specific credentials)                           |
| Workspace-level   | Workspace-specific values that must not be shared (environment-specific overrides, test credentials)                                |

| Scenario                           | Result / precedence                                                                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| No Priority checked                | Workspace variables override project and organization variable sets for the same variable name.                                                   |
| Priority checked on a variable set | Variables in that set will override same-named variables in more specific scopes (workspace, project) according to the set’s configured priority. |

## Best practices

> **lightbulb** * Use clear, descriptive names and descriptions for variable sets to make intent obvious.
  * Mark all secrets as `Sensitive` — Terraform Cloud encrypts and hides these values in the UI.
  * Prefer narrow scoping for secrets; only apply highly privileged credentials where necessary.
  * Use Priority deliberately — it changes the usual precedence behavior.

> **warning** Enabling Priority on a variable set causes its values to override more specific workspace variables. Use Priority sparingly and document any cases where you rely on it to avoid accidental overrides.

## References

* Terraform Cloud Variable Sets — [https://www.terraform.io/cloud-docs/variables/variable-sets](https://www.terraform.io/cloud-docs/variables/variable-sets)
* Terraform Cloud Concepts — [https://www.terraform.io/cloud-docs](https://www.terraform.io/cloud-docs)

That covers creating organization- and project-level variable sets, how they inherit to workspaces, and how Priority affects variable precedence.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/110bee15-3e45-411c-a55c-e8dfff73d23a/lesson/d2d034a0-c9c4-4d0f-81d8-b724cdabaf68)
