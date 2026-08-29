# DEMO Kustomize Controller Plain YAML Manifests in Different Repo

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Source-and-Kustomize-Controller/DEMO-Kustomize-Controller-Plain-YAML-Manifests-in-Different-Repo/page

This article explains how to configure FluxCD to deploy YAML manifests from a separate Git repository using Kustomize Controller.

In this lesson, you’ll configure FluxCD to pull plain YAML manifests from a different Git repository and apply them with Kustomize Controller. We’ll create a `GitRepository` source and a `Kustomization` resource step by step.

## Prerequisites

* A Kubernetes cluster with FluxCD v0.38+ installed
* `flux` CLI configured with your cluster’s kubeconfig
* Access to the `bb-app-source` repository on GitHub

***

## 1. Checkout the `2-demo` Branch

Switch to the `2-demo` branch in your `bb-app-source` repository:

```bash theme={null}
cd bb-app-source
git checkout 2-demo
```

You should see:

```bash theme={null}
Branch '2-demo' set up to track remote branch '2-demo' from 'origin'.
Switched to a new branch '2-demo'
```

## 2. Review the Application Manifest

Inspect the Deployment manifest under `manifests/`. Notice the image version has been updated to **7.2.0**:

```yaml theme={null}
