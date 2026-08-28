# Create a codespace for a repo and branch
gh codespace create --repo owner/repo --branch feature-branch

# List running/available codespaces
gh codespace list
```

How Codespaces are initialized

* Templates: Repository templates or starter templates bootstrap a new project. Templates commonly include a `.devcontainer` folder (with `devcontainer.json` and an optional Dockerfile) that specifies the container image, required packages, extensions, and forwarded ports.
  <Callout icon="lightbulb">
    Using a `.devcontainer` codifies the OS image, packages, and editor extensions so every codespace launched from the repo delivers a consistent developer experience.
  </Callout>
* Branch: Launch from a specific branch to develop in the same code and config context as that branch.
* Pull request: Start a Codespace from a pull request to run the changes in an isolated environment for review and validation.
* Commit: Create a Codespace tied to a commit hash to reproduce the repository state at a precise point in time—valuable for debugging and regression testing.

Under the hood

When you start a Codespace, GitHub provisions an Azure virtual machine and then starts one or more containers defined by the devcontainer configuration. The container image and devcontainer settings determine which languages, runtimes, CLIs, and VS Code extensions are available when the environment starts. This architecture ensures that the development environment is portable, reproducible, and isolated from your local machine.

Important considerations

<Callout icon="warning">
  Codespaces availability and billing depend on your GitHub account or organization plan and policies. Verify enabled regions, allowed machine types, and usage quotas in your organization settings before provisioning large or long-running environments.
</Callout>

Quick tips and best practices

* Add a complete `.devcontainer` configuration to your repository to lower onboarding friction for contributors.
* Use lightweight base images for faster spin-up times.
* Forward only required ports and set workspace-specific secrets via repository or organization settings.
* Stop or delete idle Codespaces to minimize billing and resource usage.

Links and references

* [GitHub Codespaces documentation](https://docs.github.com/en/codespaces)
* [Visual Studio Code - Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
* [GitHub CLI](https://cli.github.com/)
* [Azure Virtual Machines](https://azure.microsoft.com/services/virtual-machines/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c4995815-313c-40eb-a9c1-aedee41abd7d/lesson/9f74e8f1-7b27-4a89-8552-30978af919d8" />
</CardGroup>


# The Codespace Lifecycle

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/The-Codespace-Lifecycle/page

Overview of the GitHub Codespaces lifecycle, covering provisioning, operational states, persistence, rebuilding, saving work, cost management, and final deletion

The GitHub Codespaces lifecycle describes the journey of a cloud-hosted development environment from provisioning to termination. Understanding this lifecycle helps you manage costs, protect work, and ensure reliable developer workflows.

<Frame>
  <img alt="The image shows a diagram of the lifecycle of a codespace, highlighting creation, persistence, saving work, and deletion, along with actions like creating, stopping, deleting, and rebuilding a codespace." />
</Frame>

## Quick overview: lifecycle phases

1. Provisioning (creation) — a VM and persistent storage are allocated; the development container image is built or pulled; connections and initialization run.
2. Active (connected) — you work in the Codespace, running terminals and services.
3. Idle / Stopped — compute is halted to save costs while persistent disk retains files.
4. Rebuild — the environment can be rebuilt from the repository configuration.
5. Deletion — VM and persistent storage are removed; data cannot be recovered.

## Provisioning (creation)

When you create a Codespace, GitHub performs several backend steps to prepare a reproducible development environment:

* Resource allocation: a virtual machine plus dedicated persistent disk are provisioned.
* Containerization: the devcontainer image is built or pulled using your repository’s configuration (`devcontainer.json`, Dockerfile).
* Connection setup: a secure channel is established between your client (browser or VS Code) and the VM.
* Post-creation configuration: setup scripts and extensions run to install dependencies and apply custom settings.

Recommendations:

* Keep your `devcontainer.json` and Dockerfiles small and cache-friendly to reduce creation and rebuild times.
* Use prebuilt images where available to speed provisioning.

## Operational states: connected, disconnected, stopped

Codespaces offers flexible states so you can pause and resume work without losing progress:

| State        | What happens                                                                  | Typical use case                                                                 |
| ------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Connected    | Your client (browser/VS Code) is attached; terminals and services run.        | Active development and debugging.                                                |
| Disconnected | Client is closed but the VM remains running; processes continue in the cloud. | Long-running processes you want to keep running while switching devices.         |
| Stopped      | VM is shut down to save compute; persistent disk retains file changes.        | Save costs when not actively developing; restart later to resume.                |
| Deleted      | VM and its persistent storage are removed permanently.                        | Clean up old environments or reclaim resources; irreversible.                    |
| Rebuild      | Container image and setup scripts re-run to restore or update environment.    | Apply configuration changes, refresh dependencies, or recover a corrupted image. |

* Disconnecting preserves running processes but continues billing for the VM.
* Stopping conserves compute (and costs) while preserving files on disk.
* Rebuilding re-applies the repository-defined configuration and can refresh a corrupted or outdated environment.

<Frame>
  <img alt="The image shows a circular lifecycle diagram describing different stages related to &#x22;Codespace&#x22; such as creation, stopping, rebuilding, and deleting. On the left, there's a list highlighting &#x22;Persistence&#x22; among other stages like creation and deletion." />
</Frame>

<Callout icon="lightbulb">
  Set automatic stop timeouts for idle Codespaces to reduce costs. Organizations and users can configure stop timeouts so idle Codespaces are automatically stopped after a configured period.
</Callout>

## Saving and synchronizing your work

Files you edit inside a Codespace are stored on that Codespace’s persistent disk for the lifetime of the environment. Important points:

* Local changes on the Codespace disk exist only in that Codespace until you record them in Git and push to the remote repository.
* The integrated web editor has autosave enabled by default. When using the VS Code desktop client, enable autosave in VS Code or ensure you save files before committing.
* The default workspace path inside a Codespace is ` /workspaces/<repository-name>` — use that path when running scripts that expect the repository root.

Example Git workflow to make work permanent and shareable:

```bash theme={null}
