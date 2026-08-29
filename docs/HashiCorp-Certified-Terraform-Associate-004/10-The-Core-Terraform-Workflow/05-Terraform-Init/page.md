# Interactively destroy all resources managed in the current workspace (confirmation required)
terraform destroy
```

Useful flags:

* `-target=RESOURCE_ADDRESS` — destroy only a specific resource (advanced use).
* `-auto-approve` — skip the interactive confirmation (use with caution).

Example targeted destroy:

```bash theme={null}
terraform destroy -target=aws_instance.web1
```

<Callout icon="lightbulb">
  Prefer removing resource blocks from your `.tf` files and running `terraform apply` when you want to remove specific resources. This keeps your configuration consistent with desired state and avoids accidental drift.
</Callout>

## Two common workflows to remove resources

| Workflow                                  | When to use                                                             | Example                                                            |
| ----------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `terraform destroy`                       | Tear down the entire Terraform-managed stack in the current workspace   | `terraform destroy` or `terraform destroy -auto-approve`           |
| Delete resource block + `terraform apply` | Remove selected resources and keep configuration as the source of truth | Remove block from `main.tf` → `terraform plan` → `terraform apply` |
| `terraform destroy -target`               | Advanced: destroy a single resource immediately (use sparingly)         | `terraform destroy -target=aws_instance.web1`                      |

## Best practice recommendations

* Use configuration-first removals (delete resource block + `terraform apply`) for selective removals.
* Use `terraform destroy` when you intentionally want to tear down the whole workspace.
* Avoid using `-target` for routine operations; it’s intended for troubleshooting and advanced scenarios.
* Remember: destroyed resources are removed from the Terraform state file.

## Practical workflow to remove a resource from your configuration

1. Delete the resource block from your `.tf` files (for example, from `main.tf`).
2. Run `terraform plan` and review the plan to verify the exact resources that will be removed.

```bash theme={null}
terraform plan
```

3. Run `terraform apply` and confirm to destroy the real-world resource and update the state.

```bash theme={null}
terraform apply
# type "yes" to confirm, or use -auto-approve if you understand the consequences
```

If you only want to remove a resource from the Terraform state (without destroying the real-world resource), consider `terraform state rm RESOURCE_ADDRESS`. This is advanced and will leave the real resource unmanaged by Terraform.

## Visualizing destruction order

Consider an example infrastructure: a virtual network, three subnets, and several VMs. Running `terraform destroy` without flags will destroy all resources Terraform manages in dependency-aware order — typically the reverse of creation. Terraform will delete the VMs first (because they depend on subnets), then the subnets, and finally the virtual network.

<Frame>
  <img alt="The image shows a diagram of a virtual network with subnets and VMs, accompanied by text about destroying resources using the terraform destroy command, indicating it will remove all resources managed by Terraform." />
</Frame>

Because Terraform resolves and respects dependencies declared in the configuration, it avoids dependency errors (for example, you cannot delete a subnet that still has VMs attached — Terraform will delete the VMs first).

## Targeted destruction details

Using `-target` with `terraform destroy` lets you remove a single resource immediately:

```bash theme={null}
terraform destroy -target=aws_instance.web1
```

Important caveats:

* Targeted destroys bypass the usual full-plan review and can lead to configuration drift if the resource block remains in your `.tf` files.
* If you destroy a resource via `-target` but leave its resource block in your configuration, the next `terraform apply` will recreate it. To permanently remove it, delete the resource block from your configuration before applying.

## Important warning

<Callout icon="warning">
  Destroy operations are effectively irreversible from Terraform's perspective. Once Terraform deletes resources, it cannot restore them. Some cloud providers may offer backups or snapshots outside Terraform, but Terraform itself has no built-in "undo." Always review the destruction plan carefully and ensure you have backups or snapshots if needed, especially for production resources.
</Callout>

## Summary

* `terraform destroy` removes all resources managed in the current workspace after showing a destruction plan and requiring confirmation.
* For selective removals, prefer deleting resource blocks and running `terraform apply` so your configuration remains the source of truth.
* Destroyed resources are removed from the Terraform state file.
* Targeted destruction (`-target`) can remove a specific resource quickly but may cause drift and should be used sparingly.
* Always double-check destruction plans and consider backups before proceeding in production.

## Links and references

* [Terraform CLI Docs — destroy](https://www.terraform.io/cli/commands/destroy)
* [Terraform state subcommands](https://www.terraform.io/cli/commands/state)
* [HashiCorp Terraform Documentation](https://www.terraform.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/19517524-ccdf-423f-9e73-9d2eeb633e0a" />
</CardGroup>


# Terraform Init

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Terraform-Init/page

Explains terraform init, how it initializes providers, modules, backend, the .terraform directory and lock file, and when to run and manage these artifacts.

Let's walk through `terraform init` — the first command you run in any new Terraform project. It prepares your working directory so Terraform can download required providers, fetch modules, and configure the backend. After `terraform init` you can run `terraform plan` and `terraform apply` reliably.

In this article you'll learn what `terraform init` does, when to run it, and the files and directories it creates and manages.

## What `terraform init` does

`terraform init` sets up the working environment by:

* Downloading provider plugins referenced in your configuration (for example, AWS, Azure, GCP).
* Fetching referenced modules from the Terraform Registry, Git, or other sources.
* Configuring the backend where the Terraform state is stored (local or remote backends such as S3, Azure Storage, etc.).
* Creating or updating the dependency lock file ` .terraform.lock.hcl` to pin provider versions and checksums.

Think of `terraform init` as the foundation step — Terraform ensures all dependencies are available locally before any planning or applying occurs. The command is incremental: if you update a single provider, Terraform downloads only the changed provider and leaves other cached providers intact.

When to run `terraform init`:

* At the start of a new Terraform project.
* After adding, removing, or upgrading providers or modules.
* After changing backend settings.
* Any time you want to refresh locally cached dependencies.

<Frame>
  <img alt="The image explains the Terraform lock file, highlighting its creation during terraform init, its purpose for locking dependency versions, its storage location, and best practices for version control." />
</Frame>

<Callout icon="lightbulb">
  Commit ` .terraform.lock.hcl` to version control. It pins provider versions and checksums so every team member and CI run uses the same provider binaries, preventing “works on my machine” issues.
</Callout>

## The lock file: ` .terraform.lock.hcl`

Each run of `terraform init` will create or update a ` .terraform.lock.hcl` file in your working directory (the same folder as your `*.tf` files). This lock file:

* Records provider versions and checksums selected during initialization.
* Ensures consistent provider selection across machines and CI runs.
* Is managed automatically by Terraform — do not edit it manually.

Best practice: include ` .terraform.lock.hcl` in your repository so provider selection changes are visible in code reviews.

## Example output from `terraform init`

Typical output from `terraform init` shows backend initialization, provider discovery and installation, and confirmation of the lock file creation. Example:

```bash theme={null}
$ terraform init
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/vsphere...
- Finding latest version of hashicorp/random...
- Finding latest version of hashicorp/vault...
- Installing hashicorp/vault v4.5.0...
- Installed hashicorp/vault v4.5.0 (signed by HashiCorp)
- Installing hashicorp/vsphere v2.10.0...
- Installed hashicorp/vsphere v2.10.0 (signed by HashiCorp)
- Installing hashicorp/random v3.6.3...
- Installed hashicorp/random v3.6.3 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

This output highlights:

* Backend initialization (where Terraform state will be stored).
* Provider discovery and installation (including versions and signatures).
* Creation of ` .terraform.lock.hcl` and successful initialization.

## When to re-run `terraform init` (quick reference)

| Trigger                           | Why re-run `terraform init`?                    | Recommended action                                 |
| --------------------------------- | ----------------------------------------------- | -------------------------------------------------- |
| New project                       | No provider or module cache exists locally      | Run `terraform init` once in the project directory |
| Added or removed providers        | Provider binaries need to be downloaded/removed | Run `terraform init` to update plugins             |
| Changed module source or versions | Terraform must fetch fresh module code          | Run `terraform init` to download new modules       |
| Changed backend configuration     | Terraform must reconfigure the state backend    | Run `terraform init` to reinitialize the backend   |
| CI pipeline run                   | Ensure deterministic provider selection         | Run `terraform init -input=false` in CI            |

## The `.terraform` directory

Running `terraform init` creates a local `.terraform` directory in your working directory. This is Terraform’s local cache and contains provider binaries and downloaded modules.

Common contents of ` .terraform`:

| Item                    | Description                                                   | Commit to VCS? |
| ----------------------- | ------------------------------------------------------------- | -------------- |
| `plugins` / `providers` | Cached provider binaries used to communicate with cloud APIs  | No             |
| `modules`               | Downloaded copies of modules referenced by your configuration | No             |
| backend/plugin metadata | Internal metadata used by Terraform during operations         | No             |

<Frame>
  <img alt="The image explains the structure of the .terraform directory used by Terraform, highlighting the organization of providers and modules within a working directory." />
</Frame>

Terraform manages everything inside `.terraform`. Do not manually edit these files; Terraform will recreate or update them when needed.

## Version control and `.terraform`

Should you commit the `.terraform` directory to version control? No — add it to `.gitignore` instead.

Reasons to ignore `.terraform`:

* The directory is a cache of files that can be recreated by running `terraform init`.
* Provider binaries are large and platform-specific (different OS/architecture).
* Committing it introduces noise and potential merge conflicts.

If cached providers or modules become corrupted or inconsistent, delete the `.terraform` directory and run `terraform init` again to rebuild the cache.

<Frame>
  <img alt="The image provides guidance on handling the .terraform directory, advising not to include it in version control and noting it can be deleted and recreated with terraform init." />
</Frame>

<Callout icon="warning">
  Do not commit the `.terraform` directory. Treat it as a local cache that can be deleted and recreated with `terraform init`.
</Callout>

## Summary

* Run `terraform init` at the start of a project and whenever providers, modules, or backend configuration change.
* `terraform init` downloads providers and modules, configures the backend, creates/updates ` .terraform.lock.hcl`, and populates the `.terraform` directory.
* Commit ` .terraform.lock.hcl` to version control to ensure consistent provider versions across environments.
* Do not commit `.terraform`; add it to `.gitignore` and recreate it with `terraform init` if needed.

## Links and References

* [Terraform CLI: init](https://www.terraform.io/cli/commands/init)
* [Terraform Providers and Provider Versioning](https://www.terraform.io/language/providers)
* [Terraform Lock File Documentation](https://www.terraform.io/language/files/lock)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/0f269c55-532e-4097-87e3-4f179f5154a2" />
</CardGroup>
