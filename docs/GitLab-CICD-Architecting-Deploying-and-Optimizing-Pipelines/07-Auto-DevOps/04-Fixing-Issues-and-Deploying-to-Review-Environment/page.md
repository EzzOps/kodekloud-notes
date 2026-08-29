# Fixing Issues and Deploying to Review Environment

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Auto-DevOps/Fixing-Issues-and-Deploying-to-Review-Environment/page

This guide resolves GitLab Auto DevOps review pipeline failures by configuring MongoDB secrets, adjusting Kubernetes probe ports, and performing deployment and cleanup procedures.

In this guide, we’ll resolve a failed GitLab Auto DevOps review pipeline by correctly injecting MongoDB secrets, aligning Kubernetes probe ports, and redeploying to the review environment. We’ll also cover performance testing and cleanup procedures.

## 1. Identifying the Pipeline Failure

The review stage failed because the application pod couldn’t access the MongoDB environment variables:

![The image shows a GitLab pipeline interface with various stages like build, test, review, performance, and cleanup. The review stage has failed, indicated by a red icon, while other stages have passed or are pending.](https://kodekloud.com/kk-media/image/upload/v1752877095/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-pipeline-interface-review-failed.jpg)

Pipeline Stages Overview:

| Stage       | Status    | Description                    |
| ----------- | --------- | ------------------------------ |
| build       | ✅ Passed  | Build and push container image |
| test        | ✅ Passed  | Run unit and integration tests |
| review      | ❌ Failed  | Deploy to review environment   |
| performance | ⏳ Pending | Browser performance testing    |
| cleanup     | ⏳ Pending | Teardown review environment    |

## 2. Configuring Kubernetes Secrets via CI/CD Variables

Store your MongoDB credentials as CI/CD variables in GitLab:

1. Go to **Settings > CI/CD > Variables** under the Auto DevOps customizer.
2. Prefix each key with `K8S_SECRET_` so Auto DevOps creates a Kubernetes Secret and injects it into pods.

> **lightbulb** Auto DevOps will map `K8S_SECRET_<NAME>` to a Kubernetes secret named `<NAME>`, making it available as an environment variable inside your pod.

![The image shows a GitLab CI/CD settings page with a list of environment variables, including keys like K8S\_SECRET\_MONGO\_URI and K8S\_SECRET\_MONGO\_USERNAME, with their values masked. On the right, there's a section for adding a new variable with options for type, environments, and flags.](https://kodekloud.com/kk-media/image/upload/v1752877096/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Fixing-Issues-and-Deploying-to-Review-Environment/gitlab-ci-cd-environment-variables.jpg)

Example (in CI/CD UI or via `curl` API):

```bash theme={null}
