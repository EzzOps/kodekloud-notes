# Modify Dev Deployment Job to use Environment tags

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Modify-Dev-Deployment-Job-to-use-Environment-tags/page

This article explains how to modify a GitHub Actions deployment job to utilize environment tags for managing replica counts and enforcing environment policies.

Now that you’ve configured a GitHub Actions environment with protection rules, secrets, and variables, let’s update the **dev-deploy** job so it automatically picks up the right replica count and enforces your environment policies.

## Prerequisites

* A GitHub repository with an **development** environment that has:
  * One protection rule (e.g., required reviewers or wait timer)
  * One secret
  * Two environment-level variables
* A working Kubernetes cluster for the `development` namespace
* A Docker build job named `docker` in your workflow

<Callout icon="lightbulb">
  Environment-level variables override repository-level variables. In our example, the repository variable `REPLICAS` is set to `2`, while in the **development** environment it’s set to `1`.
</Callout>

<Frame>
  ![The image shows a GitHub repository settings page focused on configuring environments, with options for protection rules, secrets, and variables.](https://kodekloud.com/kk-media/image/upload/v1752876452/notes-assets/images/GitHub-Actions-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-repo-settings-environments-config.jpg)
</Frame>

<Frame>
  ![The image shows a GitHub repository settings page focused on "Secrets and variables," displaying environment and repository variables with options to manage or update them.](https://kodekloud.com/kk-media/image/upload/v1752876454/notes-assets/images/GitHub-Actions-Modify-Dev-Deployment-Job-to-use-Environment-tags/github-repo-settings-secrets-variables.jpg)
</Frame>

## Verify Current Kubernetes Deployment

Before modifying the workflow, let’s confirm the existing deployment in the `development` namespace:

```bash theme={null}
kubectl -n development get deployments.apps
