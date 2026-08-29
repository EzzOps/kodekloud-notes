# DEMO Flux Pull and Deploy from OCI Registry

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/DEMO-Flux-Pull-and-Deploy-from-OCI-Registry/page

This tutorial explains how to use Flux CD to pull container images from an OCI registry and deploy them to a Kubernetes cluster.

In this tutorial, you’ll learn how to use the Flux Source Controller to fetch container images from an OCI-compatible registry (GitHub Container Registry) and deploy them to your Kubernetes cluster. We’ll pull the `bb-app` image (`7.7.0-0bb2691`) from GHCR, configure authentication, and create a Kustomization to manage deployments.

## Prerequisites

* A Kubernetes cluster with Flux CD installed ([Flux Installation Guide](https://fluxcd.io/docs/installation/)).
* `flux` CLI and `kubectl` configured to target your cluster.
* Docker (optional) to verify the image locally.

## Overview of Flux Resources

| Resource Type | Purpose                                 | Flux Command Example                                                                                                      |
| ------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| OCIRepository | Registers an OCI image as a Flux source | `flux create source oci demo-source-oci-bb-app --url oci://ghcr.io/...`                                                   |
| Secret (OCI)  | Stores registry credentials             | `flux create secret oci ghcr-auth --url ghcr.io --username USER --password TOKEN`                                         |
| Kustomization | Pulls and applies manifests or images   | `flux create kustomization demo-kustomize-bb-app --source OCIRepository/demo-source-oci-bb-app --target-namespace bb-app` |

## 1. Pull the OCI Image Locally (Optional)

Verify the `bb-app` image before integrating with Flux:

```bash theme={null}
docker pull ghcr.io/sidd-harth-2/bb-app:7.7.0-0bb2691
```

You need both the image path (`ghcr.io/sidd-harth-2/bb-app`) and the tag (`7.7.0-0bb2691`).

> **lightbulb** Public OCI registries (e.g., Docker Hub) typically don’t require authentication. Private registries like GHCR do.

## 2. Create an OCIRepository Source

Register the image in Flux by creating an `OCIRepository`. Update the tag to `7.7.0-0bb2691`:

```bash theme={null}
cd block-buster/flux-clusters/dev-cluster

flux create source oci demo-source-oci-bb-app \
  --url oci://ghcr.io/sidd-harth-2/bb-app \
  --tag 7.7.0-0bb2691 \
  --secret-ref ghcr-auth \
  --provider generic \
  --interval 1m \
  --export > demo-source-oci-bb-app.yaml
```

Contents of `demo-source-oci-bb-app.yaml`:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: demo-source-oci-bb-app
  namespace: flux-system
spec:
  interval: 1m0s
  provider: generic
  url: oci://ghcr.io/sidd-harth-2/bb-app
  ref:
    tag: 7.7.0-0bb2691
  secretRef:
    name: ghcr-auth
```

## 3. Create the OCI Authentication Secret

Flux requires credentials to pull from a private registry. Generate a GitHub Personal Access Token (PAT) with the `read:packages` scope, then create the secret:

```bash theme={null}
flux create secret oci ghcr-auth \
  --url ghcr.io \
  --username sidd-harth-2 \
  --password <GITHUB_PERSONAL_ACCESS_TOKEN> \
  --export > ghcr-auth.yaml
```

> **triangle-alert** Keep your GitHub PAT secure. Do not commit `ghcr-auth.yaml` to public repositories.

Apply both manifests:

```bash theme={null}
kubectl apply -f ghcr-auth.yaml
kubectl apply -f demo-source-oci-bb-app.yaml
```

Verify the secret in the `flux-system` namespace:

```bash theme={null}
kubectl -n flux-system get secrets
