# Installing a Self Hosted Runner

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Self-Hosted-Runner/Installing-a-Self-Hosted-Runner/page

This guide explains how to set up a self-hosted GitHub Actions runner on a Linux repository.

This guide walks you through attaching a self-hosted runner directly to your GitHub repository. While organization- and enterprise-level runners are possible, this tutorial focuses on repository-level setup for Linux.

Refer to the official GitHub docs for detailed requirements, auto-scaling, limits, and best practices: [Hosting your own runners](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners).

![The image shows a GitHub Docs page about self-hosted runners, explaining their use in GitHub Actions workflows. It includes navigation links and a detailed description of self-hosted runners.](https://kodekloud.com/kk-media/image/upload/v1752876769/notes-assets/images/GitHub-Actions-Installing-a-Self-Hosted-Runner/github-docs-self-hosted-runners.jpg)

## 1. Add a New Self-Hosted Runner in GitHub

1. In your repository, go to **Settings** → **Actions** → **Runners**.
2. Click **New self-hosted runner**.
3. Select **Linux** as the OS and **x64** as the architecture. GitHub then displays the setup commands.

![The image shows a GitHub repository page with details about branches, files, and a README section discussing GitHub Actions. The interface includes options for code management and repository settings.](https://kodekloud.com/kk-media/image/upload/v1752876770/notes-assets/images/GitHub-Actions-Installing-a-Self-Hosted-Runner/github-repo-branches-files-readme.jpg)

### Available Runner Platforms

| Operating System | Architecture |
| ---------------- | ------------ |
| Linux            | x64          |
| macOS            | x64, ARM     |
| Windows          | x64, ARM     |

## 2. Install the Runner on Your Linux VM

Open a terminal and execute:

```bash theme={null}
