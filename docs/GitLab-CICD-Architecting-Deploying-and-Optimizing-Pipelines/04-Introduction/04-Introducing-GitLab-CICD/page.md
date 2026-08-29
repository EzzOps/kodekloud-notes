# Introducing GitLab CICD

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Introduction/Introducing-GitLab-CICD/page

This article explores how GitLab CI/CD automates build, test, security, and deployment tasks with minimal configuration.

Assume your organization has adopted GitLab as its central repository and now seeks a seamless CI/CD automation solution. GitLab Server is an open-source DevOps platform that consolidates your entire software development lifecycle—version control, issue tracking, CI/CD pipelines, package registries, and more—into a single interface.

Although numerous CI/CD tools exist, leveraging **GitLab CI/CD** streamlines workflows directly alongside your codebase. In this article, we’ll explore how GitLab CI/CD automates build, test, security, and deployment tasks with minimal configuration.

## What is GitLab CI/CD?

GitLab CI/CD is a built-in continuous integration and delivery system that runs pipeline jobs automatically on repository events. You define workflows in a single YAML file, and GitLab handles everything from spinning up environments to reporting results.

<Frame>
  ![The image is a flowchart illustrating the GitLab CI/CD process, including steps like building, unit testing, linting, dockerizing, security, deployment, and tests.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877307/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Introducing-GitLab-CICD/gitlab-ci-cd-flowchart.jpg)
</Frame>

## How CI/CD Jobs Are Executed

Every job in a pipeline runs on a **Runner**, a lightweight agent that executes tasks in an isolated environment. GitLab offers two Runner categories:

* SaaS Runners (hosted by GitLab.com)
* Self-Managed Runners (run on your own infrastructure)

<Callout icon="lightbulb">
  This article covers **SaaS Runners**. Self-managed Runners will be detailed in a separate guide.
</Callout>

<Frame>
  ![The image shows two types of GitLab Runners: "SaaS Runners" with a GitLab logo and "Self-Managed Runners" with an icon of a person.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877308/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Introducing-GitLab-CICD/gitlab-runners-saas-self-managed.jpg)
</Frame>

### SaaS Runners

SaaS Runners are enabled by default for all GitLab.com projects—no additional setup required. Depending on your build requirements, choose from:

| Runner Type            | Platform       | Use Case                                            |
| ---------------------- | -------------- | --------------------------------------------------- |
| Linux Runners          | Ubuntu, Alpine | Broad language & tooling support                    |
| Windows Runners (Beta) | Windows Server | Windows-specific builds (PowerShell, .NET, etc.)    |
| macOS Runners (Beta)   | macOS          | Apple ecosystem builds (Xcode, Swift, CocoaPods)    |
| GPU-enabled Runners    | Linux + GPUs   | High-performance workloads (ML training, inference) |

<Frame>
  ![The image shows icons representing GitLab CI/CD SaaS Runners for Ubuntu, Windows (Beta), MacOS (Beta), and GPU.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877309/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Introducing-GitLab-CICD/gitlab-ci-cd-saas-runners-icons.jpg)
</Frame>

With SaaS Runners, GitLab manages:

* Provisioning a fresh VM or container for each job
* Caching dependencies to accelerate subsequent builds
* Reporting detailed job status and logs

<Frame>
  ![The image outlines three tasks handled by GitLab CI/CD: tasks in virtual environments, caching necessary dependencies, and providing reports on outcomes.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877310/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Introducing-GitLab-CICD/gitlab-ci-cd-tasks-overview.jpg)
</Frame>

Automation benefits:

* Streamlined releases—deliver features and fixes faster
* Fewer manual errors—consistent, repeatable deployments
* Improved quality—catch issues earlier in the pipeline

<Frame>
  ![The image outlines the benefits of GitLab CI/CD, highlighting three key points: streamlining development, reducing manual errors, and increasing efficiency.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877311/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Introducing-GitLab-CICD/gitlab-ci-cd-benefits-outline.jpg)
</Frame>

## Defining a Pipeline

A **pipeline** is a sequence of one or more jobs triggered by repository events (e.g., commits, merge requests). To define yours, create a file named `.gitlab-ci.yml` at your project root:

```yaml theme={null}
