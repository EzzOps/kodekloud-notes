# DEMO Push Kubernetes Manifest to OCI Registry

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/DEMO-Push-Kubernetes-Manifest-to-OCI-Registry/page

This article explains how to package Kubernetes manifests as OCI artifacts and push them to GitHub Container Registry using Flux.

In this walkthrough, we’ll package Kubernetes manifests as an OCI artifact and push them to GitHub Container Registry (GHCR). Flux can then pull and deploy these manifests directly.

## Prerequisites

You need a GitHub Personal Access Token (PAT) with permissions to manage packages and your repository:

| Scope             | Description                          |
| ----------------- | ------------------------------------ |
| `repo`            | Full control of private repositories |
| `write:packages`  | Upload and publish packages          |
| `delete:packages` | Remove packages from GHCR            |

<Callout icon="lightbulb">
  If you already have a PAT, update it to include `repo`, `write:packages`, and `delete:packages`.
</Callout>

<Frame>
  ![The image shows a GitHub settings page for editing a personal access token, with various scopes selected for repository and package management permissions.](https://kodekloud.com/kk-media/image/upload/v1752877631/notes-assets/images/GitOps-with-FluxCD-DEMO-Push-Kubernetes-Manifest-to-OCI-Registry/github-settings-personal-access-token-scopes.jpg)
</Frame>

Once the correct scopes are selected, click **Update Token** and save the token value securely.

<Frame>
  ![The image shows a GitHub settings page for managing personal access tokens, specifically the "Tokens (classic)" section, with options to generate or revoke tokens.](https://kodekloud.com/kk-media/image/upload/v1752877632/notes-assets/images/GitOps-with-FluxCD-DEMO-Push-Kubernetes-Manifest-to-OCI-Registry/github-settings-personal-access-tokens.jpg)
</Frame>

***

## 1. Prepare the Local Repository

1. Navigate to your source directory and switch to the demo branch:
   ```bash theme={null}
   cd ~/bb-app-source
   git checkout 7-demo
   ```

2. If you see a “dubious ownership” error on Ubuntu, mark it as safe:
   ```bash theme={null}
   git config --global --add safe.directory "$(pwd)"
   git checkout 7-demo
   ```

3. Enter the versioned folder and inspect its contents:
   ```bash theme={null}
   cd 7.7.0
   sudo apt update && sudo apt install -y tree
   tree
   ```
   You should see the `manifests/` directory alongside YAML files.

## 2. Log in to GHCR

Use Docker to authenticate against GHCR. Replace `<username>` with your GitHub handle:

```bash theme={null}
docker login ghcr.io --username <username>
