# 1. Log in to ghcr.io
docker login ghcr.io \
  --username sidd-harth \
  --password <GH_PERSONAL_ACCESS_TOKEN>
# 2. Verify local image
docker images nginx
# REPOSITORY   TAG       IMAGE ID    CREATED     SIZE
# 3. Tag for ghcr.io
docker tag nginx ghcr.io/sidd-harth/nginx:1.1.0

# 4. Push the tagged image
docker push ghcr.io/sidd-harth/nginx:1.1.0
# The push refers to repository [ghcr.io/sidd-harth/nginx]
# 1.1.0: digest sha256:6ad839ec10c687385 size: 1570
```

> **triangle-alert** Never commit your `Personal Access Token` or other credentials to version control. Store them securely with your CI/CD secrets manager.

***

## 2. Pushing a Helm Chart

1. Generate a new chart.
2. Package it into a `.tgz`.
3. Authenticate via Helm.
4. Push to the OCI registry.

```bash theme={null}
# 1. Create a chart named "app1"
helm create app1
# 2. Package the chart
helm package app1
# 3. Log in to ghcr.io with Helm
helm registry login ghcr.io \
  --username sidd-harth \
  --password <GH_PERSONAL_ACCESS_TOKEN>
# 4. Push the chart to OCI
helm push app1-1.0.0.tgz oci://ghcr.io/sidd-harth/nginx
# Pushed: ghcr.io/sidd-harth/nginx/app1:1.0.0
# Digest: sha256:81de917eaf38536b1145bdde2984d2cfd14
```

***

## 3. Publishing Plain Kubernetes Manifests

Bundle your plain YAML manifests as an OCI artifact using the Flux CLI.

```bash theme={null}
# Example directory layout
tree nginx/
├── manifests
│   ├── deployment.yaml
│   └── service.yaml
```

1. Ensure you’re logged in (via Docker).
2. Push the manifest directory.

```bash theme={null}
# 1. Authenticate (if not already)
docker login ghcr.io \
  --username sidd-harth \
  --password <GH_PERSONAL_ACCESS_TOKEN>
# 2. Push manifests as OCI artifact
flux push artifact oci://ghcr.io/sidd-harth/nginx-2:$(git rev-parse --short HEAD) \
  --path="./nginx/manifests" \
  --source="$(git config --get remote.origin.url)" \
  --revision="$(git branch --show-current)-$(git rev-parse HEAD)"
# ✓ pushing to ghcr.io/sidd-harth/nginx-2:1b31558
# artifact successfully pushed to ghcr.io/sidd-harth/nginx-2@sha256:235b486d4f4a38f0151
```

***

## What’s Next?

With your artifacts securely stored in an OCI registry, you can seamlessly integrate any GitOps tool—such as [Flux](https://fluxcd.io)—to pull, verify, and deploy them into your Kubernetes clusters.

***

## Links and References

* [Open Container Initiative (OCI)](https://opencontainers.org)
* [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec)
* [GitHub Container Registry](https://github.com/features/packages)
* [Helm OCI Registry Support](https://helm.sh/docs/topics/registries/)
* [Flux CLI: push artifact](https://fluxcd.io/docs/cmd/flux_push_artifact/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/a341e1a3-4789-4f0e-8f85-52391332cb74)


# DEMO Initialize DockerHub

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Image-Automation-Controller/DEMO-Initialize-DockerHub/page

This article provides a walkthrough to connect Kubernetes deployment to Docker Hub and automate updates using Flux GitOps.

In this walkthrough, you’ll connect your Kubernetes deployment to Docker Hub and automate updates via Flux GitOps. We’ll cover:

1. Logging in to Docker Hub
2. Pulling an existing image
3. Retagging and pushing to your account
4. Updating the Kubernetes Deployment manifest
5. Deploying via Flux
6. Verifying the live application

## Prerequisites

| Requirement                             | Purpose                              |
| --------------------------------------- | ------------------------------------ |
| Docker Hub account (free tier)          | Host and manage container images     |
| Docker CLI installed                    | Build, pull, push, and manage images |
| Clone of the `bb-app-source` repository | Source manifests for the application |

![The image shows a Docker login page where a user is prompted to enter their username or email address to continue to Docker Hub.](https://kodekloud.com/kk-media/image/upload/v1752877640/notes-assets/images/GitOps-with-FluxCD-DEMO-Initialize-DockerHub/docker-login-page-username-email.jpg)

***

## 1. Log in to Docker Hub

First, clear any existing sessions and then authenticate:

```bash theme={null}
docker logout
docker login
