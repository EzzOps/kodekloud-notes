# DEMO Cosign OCI Artifacts

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-Cosign-OCI-Artifacts/page

This guide covers signing and verifying OCI artifacts using Cosign and configuring Flux CD for deployment in Kubernetes.

In this guide, we’ll walk through signing and verifying an OCI artifact using [Cosign](https://github.com/sigstore/cosign) and then configuring [Flux CD](https://fluxcd.io/) to fetch and verify that artifact before deploying it in Kubernetes.

## Prerequisites

* A fork or clone of the `bb-appsource-git` repository
* Docker CLI installed and authenticated
* A GitHub personal access token with **read:packages** and **write:packages** scopes
* [Flux CLI](https://fluxcd.io/docs/installation/) installed
* A Cosign key pair generated (`cosign.key` and `cosign.pub`)

***

## 1. Prepare the Repository

1. Switch to a new feature branch:

   ```bash theme={null}
   git checkout -b 10-demo
   ```

2. Under the `manifests/` folder, confirm you have:

   * `namespace.yaml`
   * `deployment.yaml`
   * `service.yaml`

3. Verify your `deployment.yaml` uses version **7.10.0**:

   ```yaml theme={null}
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: block-buster
     labels:
       app: block-buster
       api: downward
       usage: global
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: block-buster
     template:
       metadata:
         labels:
           app: block-buster
           env: dev
           version: 7.10.0
       spec:
         containers:
         - name: app
           image: siddharth67/block-buster-dev:7.10.0
           imagePullPolicy: Always
           resources:
             requests:
               cpu: "100m"
               memory: "256Mi"
   ```

***

## 2. Authenticate to GitHub Container Registry

Log in to [GitHub Container Registry (GHCR)](https://ghcr.io/) using your username and personal access token:

```bash theme={null}
docker login ghcr.io --username sidd-harth-2
