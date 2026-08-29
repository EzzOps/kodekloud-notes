# NAME        TYPE                               DATA   AGE
# flux-system Opaque                             3      17h
# ghcr-auth   kubernetes.io/dockerconfigjson     1      10s
```

## 4. Create a Kustomization for Deployment

Define a `Kustomization` that references your `OCIRepository`, sets up health checks, and enforces dependency ordering:

```bash theme={null}
flux create kustomization demo-kustomize-bb-app \
  --source OCIRepository/demo-source-oci-bb-app \
  --target-namespace bb-app \
  --interval 10s \
  --prune false \
  --timeout 2m \
  --depends-on infra-database-git-mysql \
  --health-check 'Deployment/block-buster-7-7-0' \
  --export > demo-kustomize-bb-app.yaml
```

`demo-kustomize-bb-app.yaml`:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: demo-kustomize-bb-app
  namespace: flux-system
spec:
  interval: 10s
  timeout: 2m0s
  prune: false
  dependsOn:
    - name: infra-database-git-mysql
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: block-buster-7-7-0
      namespace: bb-app
  sourceRef:
    kind: OCIRepository
    name: demo-source-oci-bb-app
    namespace: flux-system
  targetNamespace: bb-app
```

Apply the Kustomization:

```bash theme={null}
kubectl apply -f demo-kustomize-bb-app.yaml
```

### Health Checks

Flux polls the specified resource and waits until it’s ready before marking the Kustomization as healthy. Example for a Git-based Kustomization:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: backend
  namespace: default
spec:
  sourceRef:
    kind: GitRepository
    name: webapp
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: backend
      namespace: dev
```

### Dependencies

The `dependsOn` field enforces deployment order. In this demo, `bb-app` waits for `infra-database-git-mysql` (your SQL database) to succeed first.

## 5. Reconcile and Debug

Check the Kustomization status:

```bash theme={null}
flux get kustomizations
```

If reconciliation stalls or health checks time out, inspect the resource:

```bash theme={null}
kubectl -n flux-system get kustomizations.kustomize.toolkit.fluxcd.io demo-kustomize-bb-app -o yaml
```

Correct any mismatches (e.g., deployment names), then trigger a manual reconcile:

```bash theme={null}
flux reconcile kustomization demo-kustomize-bb-app
```

Verify the deployment reaches `Ready`:

```bash theme={null}
flux get kustomizations
# NAME                   READY   MESSAGE
# demo-kustomize-bb-app  True    Applied revision: 7.7.0-0bb2691@sha256:...
```

## 6. Verify the Deployment

List all resources in the `bb-app` namespace:

```bash theme={null}
kubectl -n bb-app get all
# NAME                                          STATUS    AGE
# pod/block-buster-7-7-0-768744659-879jt        Running   2m
# service/block-buster-service-7-7-0             NodePort 10.105.73.12 80:3770/TCP 2m
# deployment.apps/block-buster-7-7-0             1/1       2m
# replicaset.apps/block-buster-7-7-0-768744659   1/1       2m
```

Then open your browser at `http://127.0.0.1:3770`. In version 7.7.0 you’ll notice a new “High Score” field—but a known bug prevents high scores from persisting:

![The image shows a screenshot of a "Block Buster" game with a "Game Over" message. It includes game details like score, level, and lives, along with a colorful block layout.](https://kodekloud.com/kk-media/image/upload/v1752877621/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-Pull-and-Deploy-from-OCI-Registry/block-buster-game-over-screenshot.jpg)

That issue will be fixed in the next release. Thanks for following along!

## References

* [Flux CD Documentation](https://fluxcd.io/docs/)
* [GitHub Container Registry](https://github.com/features/packages)
* [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/b1d4efe5-a36b-4214-89ba-64e0fe859a29)


# DEMO HELM Controller with Git as Source

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/DEMO-HELM-Controller-with-Git-as-Source/page

This tutorial teaches deploying a Helm chart from a Git repository into a Kubernetes cluster using Flux’s Helm Controller.

In this tutorial, you’ll learn how to use Flux’s Helm Controller to deploy a Helm chart from a Git repository into your Kubernetes cluster. We’ll create Flux sources, overrides, and a HelmRelease to run the **block-buster-helm-app** version **7.5.0**.

***

## Prerequisites

* A Kubernetes cluster with [Flux CD](https://fluxcd.io/) installed
* `kubectl` configured for your cluster
* A Git repository containing your Helm chart

***

## Step 1: Prepare a Git Branch

Switch to the application source and create a new branch called `5-demo` based on `4-demo`:

```bash theme={null}
cd bb-app/source
git checkout 4-demo
git checkout -b 5-demo origin/5-demo
```

This branch contains the `block-buster-helm-app` chart at version **7.5.0**.

***

## Step 2: Inspect the Helm Chart

Open **Chart.yaml** to view the chart metadata:

```yaml theme={null}
apiVersion: v2
name: block-buster-helm-app
description: A Helm Chart for Block Buster App
version: 7.5.0
```

Review the default values in **values.yaml**:

```yaml theme={null}
image:
  repository: siddharth67/block-buster-dev:7.5.0
  pullPolicy: Always
service:
  type: ClusterIP
  port: 80
  targetPort: 80
namespace:
  name: demo-app
labels:
  app:
    name: bb-app
    version: 7.x.x
    env: uat
```

> **lightbulb** The `templates/` directory includes standard Kubernetes manifests like Deployment and Service.

***

## Step 3: Create a GitRepository Source

Tell Flux where to fetch your chart by defining a `GitRepository`:

```bash theme={null}
flux create source git 5-demo-source-git-helm-bb-app \
  --url https://github.com/sidd-harth-2/bb-app-source \
  --branch 5-demo \
  --timeout 10s \
  --export > flux-clusters/dev-cluster/5-demo-source-git-bb-app.yaml
```

Save the following in `flux-clusters/dev-cluster/5-demo-source-git-bb-app.yaml`:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: 5-demo-source-git-helm-bb-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/sidd-harth-2/bb-app-source
  ref:
    branch: 5-demo
```

***

## Step 4: Override Chart Values

Add a `5-demo-values.yaml` file in your Flux cluster repo to customize deployment:

```yaml theme={null}
