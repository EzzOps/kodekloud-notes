# Starting a GitHub Codespace

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Codespaces/Starting-a-GitHub-Codespace/page

Guide to launching and provisioning GitHub Codespaces, using devcontainer configurations to create reproducible cloud development environments accessible via browser, VS Code, or the GitHub CLI.

In this lesson we’ll cover how to start a GitHub Codespace and what happens when one is provisioned. GitHub Codespaces provides cloud-hosted, containerized development environments you can launch from multiple interfaces and stages of the development lifecycle. Codespaces run on virtual machines hosted on Azure and use a devcontainer configuration to deliver a reproducible workspace with the tools, extensions, and runtimes your project needs.

<Frame>
  <img alt="The image is a diagram explaining the process of starting a GitHub Codespace, showing different interfaces (GitHub.com, VS Code, GitHub CLI) and detailing the components involved, like code editors and virtual machine hosting on Azure. It outlines steps to initiate a codespace from templates, branches, pull requests, or commits and describes components such as container environments and supported languages." />
</Frame>

What you can do with Codespaces

* Create a fresh, reproducible development environment for a repository without installing dependencies locally.
* Connect from the browser, from Visual Studio Code (desktop or web), or manage environments from the terminal using the GitHub CLI.
* Launch environments that match a repository’s branch, pull request, commit, or template state to ensure deterministic development and testing.

Primary ways to launch and manage a Codespace

| Channel              | Best for                                                                           | Quick example                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| GitHub.com (browser) | Fast, no-local-setup creation; good for reviewers and contributors                 | Use the Code menu → Codespaces to create a new environment for a repo, branch, PR, or commit. |
| Visual Studio Code   | Native editing, debugging, and extension support connected to the remote container | Open VS Code, choose "Remote - Containers" or use the Codespaces extension to connect.        |
| GitHub CLI           | Terminal-driven workflows, scripts and automation                                  | `gh codespace create --repo owner/repo --branch feature-branch` and `gh codespace list`       |

Example: GitHub CLI snippets

```bash theme={null}
