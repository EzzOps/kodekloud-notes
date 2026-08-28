# Workflow Login and Push to GHCR

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Workflow-Login-and-Push-to-GHCR/page

This article explains how to build and push Docker images to GitHub Container Registry using GitHub Actions.

Building a Docker image and pushing it to multiple registries—like Docker Hub, GitLab Container Registry, or GitHub Container Registry (GHCR)—is a common requirement for modern CI/CD pipelines. In this guide, we’ll focus on how to build and push an image to GHCR using GitHub Actions.

***

## What Is GitHub Container Registry?

GitHub Container Registry (ghcr.io) is part of [GitHub Packages](https://github.com/features/packages). It allows you to store and manage both Docker and OCI images, either publicly or privately.

<Frame>
  ![The image shows a GitHub Actions workflow page for a repository named "solar-system" by the user "sidd-harth-7," displaying a list of recent workflow runs with their statuses and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752876017/notes-assets/images/GitHub-Actions-Certification-Workflow-Login-and-Push-to-GHCR/github-actions-solar-system-workflow.jpg)
</Frame>

Key Features:

| Feature       | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| Namespace     | `ghcr.io`                                                     |
| Image Formats | Docker images, OCI artifacts                                  |
| Visibility    | Public or private                                             |
| Integration   | Tight integration with GitHub Actions and GitHub Packages API |

Click **Packages** → **Container registry** in your repo sidebar to explore existing images:

<Frame>
  ![The image shows a GitHub documentation page about GitHub Packages, detailing its features and usage for hosting and managing software packages. The sidebar includes links to various package registries and related topics.](https://kodekloud.com/kk-media/image/upload/v1752876019/notes-assets/images/GitHub-Actions-Certification-Workflow-Login-and-Push-to-GHCR/github-packages-documentation-features-usage.jpg)
</Frame>

***

## Authenticating to GHCR

You can authenticate using:

* A GitHub Personal Access Token (PAT) scoped for `read:packages` and `write:packages`.
* The automatically generated `GITHUB_TOKEN` in Actions workflows (requires explicit `packages: write` permission).

<Frame>
  ![The image shows a GitHub documentation page about authenticating to the container registry, detailing the use of personal access tokens and GitHub Actions workflows. The page includes a navigation menu on the left and a list of related topics on the right.](https://kodekloud.com/kk-media/image/upload/v1752876020/notes-assets/images/GitHub-Actions-Certification-Workflow-Login-and-Push-to-GHCR/github-authentication-container-registry-docs.jpg)
</Frame>

### Using a PAT Locally

```bash theme={null}
export CR_PAT=YOUR_PERSONAL_ACCESS_TOKEN
echo "$CR_PAT" | docker login ghcr.io -u YOUR_USERNAME --password-stdin
