# Create and enter a directory for the runner
mkdir actions-runner && cd actions-runner

# Download the runner package (update version as needed)
curl -o actions-runner.tar.gz \
  https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-x64-2.309.0.tar.gz

# Extract the files
tar xzf actions-runner.tar.gz

# Configure with your repo URL and token
./config.sh --url https://github.com/sidd-harth/repository \
            --token AP3V5NDFAQIMO

# Follow the prompts:
# • Runner group: [press Enter for Default]
# • Runner name: linux-gpu-runner
# • Labels: gpu
# After setup, you’ll see:
# Start the runner
./run.sh
# Expected output:
# √ Connected to GitHub
# Listening for Jobs...
```

### 3. Target Your Self-Hosted Runner in Workflows

Add the labels you chose to the `runs-on` field:

```yaml theme={null}
jobs:
  build:
    runs-on: [self-hosted, Linux, gpu]
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3
      # …additional steps…
```

***

## Comparing GitHub-Hosted vs. Self-Hosted Runners

| Aspect             | GitHub-Hosted                              | Self-Hosted                                |
| ------------------ | ------------------------------------------ | ------------------------------------------ |
| Management         | Fully managed by GitHub                    | You install, update, and secure the runner |
| Customization      | Predefined OS and toolset                  | Full control over OS, tools, and drivers   |
| Resource Sharing   | Shared infrastructure with other customers | Dedicated resources                        |
| Scaling            | Limited by GitHub’s concurrency quotas     | Autoscale via your infrastructure          |
| Maintenance        | Automatic updates and patches              | Manual updates and patch management        |
| Cost               | Billed per-minute, free for public repos   | Infrastructure and maintenance costs apply |
| Security           | GitHub’s built-in security policies        | Your network/host security measures        |
| Instance Lifecycle | Fresh VM per job                           | Persistent instance across jobs            |

![The image is a comparison table between GitHub-Hosted Runner and Self-Hosted Runner, highlighting differences in management, customization, resource sharing, scaling, maintenance, usage costs, security, and instance handling.](https://kodekloud.com/kk-media/image/upload/v1752876438/notes-assets/images/GitHub-Actions-Certification-Types-of-Runners/github-vs-self-hosted-runner-comparison.jpg)

***

## Links and References

* [GitHub Actions Runners Documentation](https://docs.github.com/actions/hosting-your-own-runners)
* [GitHub Actions Pricing](https://github.com/pricing)
* [actions/checkout GitHub Action](https://github.com/actions/checkout)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/7cc7bcee-0af6-41af-9653-dfd6e0403fe9/lesson/f55a71c6-e83e-4aa5-a5fc-3f9e95a2fd36)


# Uninstalling Self Hosted Runner

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Self-Hosted-Runner/Uninstalling-Self-Hosted-Runner/page

This guide explains how to uninstall a self-hosted runner in GitHub Actions, covering removal methods and cleanup procedures.

## Overview

GitHub Actions lets you host your own runners for custom build environments. Whether you’re removing a runner at the repository, organization, or enterprise level, this guide walks you through:

* Removing a runner via the GitHub UI
* Cleaning up the runner machine
* Temporarily disabling a runner

## Removal Methods at a Glance

| Method            | Scope                                | Description                                             |
| ----------------- | ------------------------------------ | ------------------------------------------------------- |
| UI Removal        | Repository, Organization, Enterprise | Permanently deletes the runner from GitHub.             |
| CLI Cleanup       | Runner VM                            | Unregisters the runner and removes local configuration. |
| Temporary Disable | Runner VM                            | Marks the runner offline without full uninstall.        |

## 1. Removing a Runner via GitHub UI

1. In your repository, go to **Settings** > **Actions** > **Runners**.
2. Locate the runner and click **Remove**.

![The image shows a GitHub repository settings page, specifically the "Runners" section, displaying a self-hosted runner named "prod-ubuntu-runner" with an idle status.](https://kodekloud.com/kk-media/image/upload/v1752876439/notes-assets/images/GitHub-Actions-Certification-Uninstalling-Self-Hosted-Runner/github-repo-settings-runners-prod-ubuntu.jpg)

> **triangle-alert** Removing a runner is permanent. If MFA is enabled, you’ll be prompted for a code to confirm deletion.

For organization or enterprise-level runners:

1. Navigate to **Settings** > **Actions** > **Runners** in your org/enterprise dashboard.
2. Select the runner you wish to uninstall and click **Remove**.

![The image shows a GitHub Actions settings page for a self-hosted runner named "prod-ubuntu-runner" with no active jobs running. There is a "Remove" button highlighted in red.](https://kodekloud.com/kk-media/image/upload/v1752876441/notes-assets/images/GitHub-Actions-Certification-Uninstalling-Self-Hosted-Runner/github-actions-self-hosted-runner-settings.jpg)

After confirmation, GitHub permanently deletes the runner entry.

## 2. Cleaning Up the Runner Machine

Once removed from GitHub, unregister the runner on the VM:

```bash theme={null}
./config.sh remove --token YOUR_RUNNER_TOKEN
```

Replace `YOUR_RUNNER_TOKEN` with the token from your initial configuration. This command:

* Unregisters the runner from GitHub
* Deletes local configuration files

> **lightbulb** If you see permission errors, retry with elevated privileges (e.g., `sudo` on Linux).

Alternatively, use **Force remove** in the GitHub UI to uninstall the runner application completely.

## 3. Temporarily Disabling a Runner

To pause job execution without full removal:

1. Shut down the VM or stop the runner service/script.
2. The runner will show as **offline** and won’t accept new jobs.

![The image shows a GitHub documentation page about removing self-hosted runners, detailing how to permanently remove a runner from a repository or organization.](https://kodekloud.com/kk-media/image/upload/v1752876442/notes-assets/images/GitHub-Actions-Certification-Uninstalling-Self-Hosted-Runner/github-remove-self-hosted-runners-docs.jpg)

GitHub automatically deletes any self-hosted runner that remains offline for more than 30 days, preventing stale entries.

## References

* [Removing self-hosted runners (GitHub Docs)](https://docs.github.com/actions/hosting-your-own-runners/removing-self-hosted-runners)
* [Introduction to GitHub Actions](https://docs.github.com/actions/learn-github-actions/introduction-to-github-actions)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/7cc7bcee-0af6-41af-9653-dfd6e0403fe9/lesson/923fd5a4-379e-49cf-aaa2-3b48e9ef4329)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/github-actions-certification/module/7cc7bcee-0af6-41af-9653-dfd6e0403fe9/lesson/f86e99e7-efc9-4b84-ae22-30501dc23d7b)
