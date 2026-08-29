# Github Actions Basics

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Github-Actions-Basics/page

GitHub Actions is a CI/CD and automation platform for GitHub repositories, enabling workflow automation for builds, tests, deployments, and repository maintenance tasks.

GitHub Actions is a powerful CI/CD and automation platform built into GitHub repositories. By defining workflow files directly in your project, you can automate builds, tests, deployments, and repository maintenance tasks without relying on external tools.

## What Is GitHub Actions?

GitHub Actions lets you create **workflows**—collections of **jobs** and **steps**—that run in response to repository events like `push`, `pull_request`, `schedule`, and more.

<Frame>
  ![The image shows a GitHub Actions interface displaying a list of workflow runs for a project, with details such as event status, branch, and actor.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870447/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-workflow-runs-interface.jpg)
</Frame>

With just a YAML file, you can trigger workflows on every pull request, run unit tests, and even deploy merged changes to production.

<Frame>
  ![The image shows a GitHub Actions interface with a workflow in progress for a project. It includes details about a job triggered by a push, with steps like building the application and unit testing.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870448/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-workflow-progress.jpg)
</Frame>

GitHub Actions provides first-class support for runners on Ubuntu, Windows, and macOS.

<Frame>
  ![The image shows icons for Ubuntu, Windows, and MacOS, labeled as 1, 2, and 3 respectively, under the title "GitHub Actions."](../../../../images/kodekloud.com/kk-media/image/upload/v1752870449/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-ubuntu-windows-macos.jpg)
</Frame>

All infrastructure—server provisioning, auto-scaling, and environment maintenance—is handled by GitHub, so you can focus on writing workflows.

<Frame>
  ![The image is an infographic titled "GitHub Manages Infrastructure," showing three steps: setting up servers, scaling resources, and managing execution environments. Each step is represented with an icon and a number.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870450/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-manages-infrastructure-infographic.jpg)
</Frame>

## Beyond CI/CD: Repository Automation

While GitHub Actions shines for CI/CD—building, packaging, and deploying code—it also responds to many repository events, such as issues, pull requests, releases, and registry packages:

<Frame>
  ![The image is a diagram illustrating GitHub Actions for automating CI/CD, showing steps like building, unit testing, linting, dockerizing, security, deployment, and tests.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870453/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-cicd-diagram.jpg)
</Frame>

<Frame>
  ![The image is a flowchart illustrating GitHub Actions for automating repository actions, including pull requests, issues, releases, and registry packages, with various sub-actions like open, closed, merged, labeled, and published.](../../../../images/kodekloud.com/kk-media/image/upload/v1752870454/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-flowchart-automation.jpg)
</Frame>

For example, on a new pull request you could automatically:

* Post a welcome comment
* Apply labels based on modified files
* Assign reviewers or assignees

These patterns can extend to issues (`opened`, `labeled`), releases (`published`), and package registry events.

## Core Concepts

### Workflows

A **workflow** is defined by a YAML file in your repository’s `.github/workflows/` directory. You can have multiple workflows, each triggered by different events:

```yaml theme={null}
