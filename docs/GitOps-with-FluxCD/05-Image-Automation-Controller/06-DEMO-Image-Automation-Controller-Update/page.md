# DEMO Image Automation Controller Update

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Image-Automation-Controller/DEMO-Image-Automation-Controller-Update/page

This article provides a hands-on guide to automate container image tag updates in Kubernetes using Fluxs ImageUpdateAutomation controller.

In this hands‐on walkthrough, you’ll use Flux’s ImageUpdateAutomation controller to detect new container image tags, commit updates to your Git repository, and deploy the changes automatically on your Kubernetes cluster.

***

## Overview of Resources

| Resource Type           | Purpose                                               | Flux CLI Example                                                                                  |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| GitRepository           | Tracks your application manifests in Git              | `flux create source git <name> --url=<repo-url> --branch=<branch> --export`                       |
| ImageUpdateAutomation   | Automates image tag updates in YAML and pushes to Git | `flux create image update <name> --git-repo-ref=<git-source> --interval=1m --export`              |
| Secret (Git deploy key) | Holds SSH key for authenticating Git pushes           | `flux create secret git <name> --url=ssh://git@github.com/... --ssh-key-algorithm=ecdsa --export` |

***

## Prerequisites

* A Kubernetes cluster with Flux v0.34+ installed.
* A Git repository containing your application’s Kubernetes manifests under `./manifests`.
* An `ImagePolicy` resource in `flux-system` (e.g., `8-demo-image-policy-bb-app`) selecting the desired image tags.

For more details, see the [Flux Image Automation Guide](https://fluxcd.io/docs/guides/image-automation/) and the [Flux CLI reference](https://fluxcd.io/docs/cmd/flux/).

***

## 1. Inspect the Flux CLI for Image Updates

Open a terminal in your cluster directory and verify the ImageUpdateAutomation commands:

```bash theme={null}
flux create image update -h
```

You should see usage details for creating an `ImageUpdateAutomation` resource, which watches a Git repo and applies image tag updates to your manifests.

***

## 2. Create the ImageUpdateAutomation Resource

Generate the `ImageUpdateAutomation` YAML without applying it:

```bash theme={null}
flux create image update 8-demo-image-update-bb-app \
  --git-repo-ref=8-demo-source-git-bb-app \
  --checkout-branch=8-demo \
  --author-name=fluxcdbot \
  --author-email=fluxcdbot@users.noreply.github.com \
  --git-repo-path="./manifests" \
  --push-branch=8-demo \
  --interval=100s \
  --export > 8-demo-image-update-bb-app.yml
```

Inspect `8-demo-image-update-bb-app.yml`:

```yaml theme={null}
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: 8-demo-image-update-bb-app
  namespace: flux-system
spec:
  interval: 1m40s
  sourceRef:
    kind: GitRepository
    name: 8-demo-source-git-bb-app
  git:
    checkout:
      ref:
        branch: 8-demo
    commit:
      author:
        name: fluxcdbot
        email: fluxcdbot@users.noreply.github.com
    push:
      branch: 8-demo
  update:
    path: ./manifests
    strategy: Setters
```

***

## 3. Configure the GitRepository Source

Define your application Git source and reconcile it:

```bash theme={null}
flux create source git 8-demo-source-git-bb-app \
  --url=https://github.com/sidd-harth-2/bb-app-source \
  --branch=8-demo \
  --interval=1m0s \
  --export > 8-demo-source-git-bb-app.yml

kubectl apply -f 8-demo-source-git-bb-app.yml
kubectl apply -f 8-demo-image-update-bb-app.yml

flux reconcile source git 8-demo-source-git-bb-app -n flux-system
flux reconcile image update 8-demo-image-update-bb-app -n flux-system
flux get images all
flux get image update
```

At this stage, `ImageUpdateAutomation` will report **no updates made**, since it doesn’t know where in your manifests to apply new tags.

***

## 4. Mark the Deployment Manifest for Automated Updates

> **lightbulb** Ensure an `ImagePolicy` named `8-demo-image-policy-bb-app` exists in `flux-system` to select the desired image tags.

Edit `manifests/deployment.yml` and annotate the `image` field:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: block-buster
  namespace: 8-demo
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: app
          image: siddharth67/bb-app-flux-demo:7.8.0 # {"$imagepolicy": "flux-system:8-demo-image-policy-bb-app"}
          imagePullPolicy: Always
```

Commit and push your changes:

```bash theme={null}
git add manifests/deployment.yml
git commit -m "Add image policy marker"
git push origin 8-demo

flux reconcile source git 8-demo-source-git-bb-app -n flux-system
flux get image update
```

***

## 5. Handle Git Authentication for Push Access

After marking the manifest, the controller locates the change but cannot push:

```bash theme={null}
flux get image update
