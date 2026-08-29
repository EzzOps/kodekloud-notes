# Managing Directories

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Managing-Directories/page

This article explains how to manage Kubernetes manifests using Kustomize, including directory structures and deployment commands.

Even with a minimal `kustomization.yaml`, Kustomize lets you orchestrate Kubernetes manifests across many folders—no extra scripting required.

## Flat Directory Structure

When you start small, a single directory often suffices:

```text theme={null}
k8s/
├── api-depl.yaml
├── api-service.yaml
├── db-depl.yaml
└── db-service.yaml
```

To deploy all resources at once:

```bash theme={null}
kubectl apply -f k8s/
```

This is plain Kubernetes—no Kustomize features yet.

## Introducing Subdirectories

As your manifest count grows, you might split them:

```text theme={null}
k8s/
├── api/
│   ├── api-depl.yaml
│   └── api-service.yaml
└── db/
    ├── db-depl.yaml
    └── db-service.yaml
```

Now deployment requires two commands:

```bash theme={null}
kubectl apply -f k8s/api/
kubectl apply -f k8s/db/
```

<Callout icon="triangle-alert">
  Manually running `kubectl apply` in each subfolder can be error-prone and difficult to automate in CI/CD.
</Callout>

## Single Root kustomization.yaml

Instead of listing directories every time, create a single `kustomization.yaml` at `k8s/`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/api-depl.yaml
  - api/api-service.yaml
  - db/db-depl.yaml
  - db/db-service.yaml
```

Then deploy with one of these commands:

```bash theme={null}
kustomize build k8s/ | kubectl apply -f -
