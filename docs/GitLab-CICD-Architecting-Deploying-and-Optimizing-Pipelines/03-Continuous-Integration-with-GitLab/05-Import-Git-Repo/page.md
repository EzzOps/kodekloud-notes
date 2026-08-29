# Import Git Repo

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Import-Git-Repo/page

This article explains how to import a Node.js application repository into GitLab, detailing prerequisites and a step-by-step guide.

In this lesson, you’ll import your [Node.js](https://nodejs.org/) application’s source code—structured as the **Solar-System** project—into [GitLab](https://gitlab.com/). The repository contains application logic, test cases, a `Dockerfile`, and several [Kubernetes](https://kubernetes.io/) manifest files.

![The image shows a GitLab repository page for a project named "Solar-System," displaying files, commit history, and project details. The sidebar includes options for managing, planning, and deploying the project.](https://kodekloud.com/kk-media/image/upload/v1752877263/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Import-Git-Repo/gitlab-solar-system-repo-page.jpg)

## Prerequisites

* A GitLab account with at least **Developer** access in your target group.
* The repository’s clone URL (ending in `.git`).
* *(Optional)* A [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) if you’re importing a private repository.

> **lightbulb** If your source repo is private, create a Personal Access Token with the **read\_repository** scope and use it when prompted for credentials.

## Step-by-Step Import Guide

1. **Copy the Git URL**\
   Grab the HTTPS or SSH clone URL of your source repository, ensuring it ends with `.git`.

2. **Start a New Project**\
   In GitLab’s top bar, click the **+** icon and select **New project/repository**.

3. **Select Import Method**\
   Choose **Import project**, then click **Repo by URL**.

4. **Fill in Import Details**
   * **Git repository URL**: Paste the `.git` link.
   * **Project name**: Enter `Solar-System`.
   * **Project slug**: Adjust only if you want a custom URL path.
   * **Group (Namespace)**: Pick your target group, e.g., `demos`.
   * **Visibility**: Set to **Public**, **Internal**, or **Private**.

![The image shows a GitLab interface for importing a project, with fields for entering a Git repository URL, username, password, project name, and project description.](https://kodekloud.com/kk-media/image/upload/v1752877264/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Import-Git-Repo/gitlab-import-project-interface.jpg)

5. **Create the Project**\
   Click **Create project**. GitLab will clone and import your repository—this can take a few moments.

6. **Verify the Import**\
   Once completed, you’ll see your full project structure exactly as it was in the source:

![The image shows a GitLab repository interface for a project named "Solar System," displaying a list of files and directories with their last commit messages and update times. The project was successfully imported, and the interface includes options for managing and configuring the project.](https://kodekloud.com/kk-media/image/upload/v1752877265/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Import-Git-Repo/gitlab-solar-system-repo-interface.jpg)

Your **Solar-System** repository now lives in the `demos` group on GitLab. Next, we’ll implement the CI/CD pipeline to run unit tests, measure code coverage, and deploy to Kubernetes.

## Import Form Field Reference

| Field              | Description                                       | Example                |
| ------------------ | ------------------------------------------------- | ---------------------- |
| Git repository URL | Clone URL of the source repo (must end in `.git`) | `https://.../repo.git` |
| Project name       | Display name in GitLab                            | `Solar-System`         |
| Project slug       | URL-friendly identifier                           | `solar-system`         |
| Namespace (Group)  | Target group or personal namespace                | `demos`                |
| Visibility Level   | Public, Internal, or Private                      | `Public`               |

## Links and References

* [Node.js Official Site](https://nodejs.org/)
* [GitLab Import Documentation](https://docs.gitlab.com/ee/user/project/import/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/68ab3093-9af1-44bc-ace0-7290c8bdc6d6)
