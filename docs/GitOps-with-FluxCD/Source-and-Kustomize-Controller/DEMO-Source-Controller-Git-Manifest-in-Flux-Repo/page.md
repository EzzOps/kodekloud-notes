# bb-app-source/manifests/deployment.yaml
env: dev
version: 7.2.0
spec:
  containers:
    - name: app
      image: siddharth67/block-buster-dev:7.2.0
      imagePullPolicy: Always
      resources:
        requests:
          memory: "10Mi"
          cpu: "10m"
        limits:
          memory: "64Mi"
          cpu: "20m"
```

***

## 3. Create the GitRepository Source

From your Flux cluster configuration directory (`block-buster/flux-clusters/dev-cluster`), run:

```bash theme={null}
cd ../block-buster/flux-clusters/dev-cluster
flux create source git bb-app-2demo \
  --url https://github.com/sidd-harth-2/bb-app-source \
  --branch 2-demo \
  --timeout 10s \
  --export > bb-app-2demo-source.yaml
```

This generates:

```yaml theme={null}
# bb-app-2demo-source.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: bb-app-2demo
  namespace: flux-system
spec:
  interval: 1m0s
  url: https://github.com/sidd-harth-2/bb-app-source
  ref:
    branch: 2-demo
```

Commit and push this file so Flux can fetch your manifests automatically.

***

## 4. Create the Kustomization Resource

Use the Flux CLI to define a `Kustomization` that points to the `manifests` folder in your `bb-app-source` repo:

```bash theme={null}
flux create kustomization bb-app-2demo-kustomize \
  --source GitRepository/bb-app-2demo \
  --path ./manifests \
  --prune=true \
  --interval=10s \
  --target-namespace 2-demo \
  --export > bb-app-2demo-kustomize.yaml
```

```yaml theme={null}
# bb-app-2demo-kustomize.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: bb-app-2demo-kustomize
  namespace: flux-system
spec:
  interval: 10s
  path: ./manifests
  prune: true
  sourceRef:
    kind: GitRepository
    name: bb-app-2demo
  targetNamespace: 2-demo
```

<Callout icon="triangle-alert">
  The `--prune=true` flag will remove any Kubernetes resources in the target namespace that are not tracked by this Kustomization. Ensure you don’t have unmanaged resources in `2-demo`.
</Callout>

Commit and push the Kustomization YAML so Flux can reconcile it.

***

## 5. Overview of Created Resources

| Resource Type | Purpose                                          | Flux CLI Example                                                     |
| ------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| GitRepository | Fetch remote plain YAML manifests                | `flux create source git bb-app-2demo … --export > source.yml`        |
| Kustomization | Apply and reconcile manifests in the `2-demo` NS | `flux create kustomization bb-app-2demo-kustomize … > kustomize.yml` |

***

## 6. Verify Flux Reconciliation

First, check your Git sources:

```bash theme={null}
flux get sources git
```

Expected output:

```text theme={null}
NAME         REVISION                READY   MESSAGE
bb-app-2demo 2-demo@sha1:7dfa8105     True    stored artifact for revision '2-demo@sha1:7dfa8105'
flux-system  main@sha1:cf1664a0       True    stored artifact for revision 'main@sha1:cf1664a0'
```

Next, verify Kustomizations:

```bash theme={null}
flux get kustomizations
```

You should see:

```text theme={null}
NAME                    REVISION                 READY   MESSAGE
bb-app-2demo-kustomize  2-demo@sha1:7dfa8105     True    Applied revision: 2-demo@sha1:7dfa8105
```

***

## 7. Confirm Kubernetes Resources

List your namespaces and workload in `2-demo`:

```bash theme={null}
kubectl get ns
kubectl get all -n 2-demo
```

You should observe the `block-buster` Deployment, Service, and Pods running version **7.2.0**.

***

## 8. Access the Application

Find the NodePort for the `block-buster-service`:

```bash theme={null}
kubectl get svc block-buster-service -n 2-demo
```

Open your browser at `http://<NODE_IP>:<NODE_PORT>`. You’ll see the updated “Block Buster” game interface running version 7.2.0:

<Frame>
  ![The image shows a "Block Buster" game interface with colorful blocks, a ball, and a paddle. It includes game details like pod name, IP, and version information.](https://kodekloud.com/kk-media/image/upload/v1752877692/notes-assets/images/GitOps-with-FluxCD-DEMO-Kustomize-Controller-Plain-YAML-Manifests-in-Different-Repo/block-buster-game-interface-details.jpg)
</Frame>

***

## Links and References

* [FluxCD Source Toolkit – GitRepository](https://fluxcd.[SECRET_REDACTED]/)
* [FluxCD Kustomize Toolkit – Kustomization](https://fluxcd.io[AWS_SECRET_ACCESS_KEY]/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitOps with FluxCD](https://fluxcd.io/)
* [Docker Hub – block-buster-dev Image](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/0a35e61b-97b5-4843-a2a0-4ca83525a2f7" />
</CardGroup>


# DEMO Source Controller Git Manifest in Flux Repo

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Source-and-Kustomize-Controller/DEMO-Source-Controller-Git-Manifest-in-Flux-Repo/page

This guide explains how Flux’s Source Controller retrieves manifests from a Git repository and how the Kustomize Controller applies them to a Kubernetes cluster.

In this guide, you’ll learn how Flux’s Source Controller pulls manifests from a Git repository and how the Kustomize Controller applies them to a Kubernetes cluster, showcasing a GitOps-driven workflow.

<Callout icon="lightbulb">
  Ensure you’ve bootstrapped Flux CD with SSH credentials so the `secretRef` in your `GitRepository` can authenticate to GitHub.\
  See [Flux CD installation](https://fluxcd.io/docs/installation/) for details.
</Callout>

## 1. Define GitRepository and Kustomization

Create a `GitRepository` to tell Flux where to fetch your manifests, then reference it in a `Kustomization`:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 10s
  url: ssh://git@github.com/sidd-harth-2/block-buster
  ref:
    branch: main
  secretRef:
    name: flux-system
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 10s
  path: ./flux-clusters/dev-cluster
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
```

Key fields explained:

* `interval`: reconciliation frequency
* `url`/`ref`: Git source and branch
* `secretRef`: SSH key for cloning
* `path`: directory in the repo to apply
* `prune`: deletes resources removed from Git

### Flux Controllers Overview

| Flux Controller      | Resource      | Purpose                              | Example CLI               |
| -------------------- | ------------- | ------------------------------------ | ------------------------- |
| Source Controller    | GitRepository | Fetches manifests from Git           | `flux get sources git`    |
| Kustomize Controller | Kustomization | Applies overlays and syncs resources | `flux get kustomizations` |

## 2. Verify Flux Sources and Kustomizations

Confirm that Flux has registered your sources and kustomizations:

```bash theme={null}
