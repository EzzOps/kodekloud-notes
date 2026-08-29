# Different Types of Patches

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Different-Types-of-Patches/page

This article explains Kustomize patch strategies, including JSON 6902 and Strategic Merge, for customizing Kubernetes manifests using inline or external patches.

Kustomize supports two patch strategies—JSON 6902 and Strategic Merge—to help you customize Kubernetes manifests. Use inline patches for quick edits or external patch files for better organization as your configuration grows.

## Patch Overview

| Patch Type            | Operation Style                                        | Inline | External File |
| --------------------- | ------------------------------------------------------ | :----: | :-----------: |
| JSON 6902 Patch       | JSON Patch RFC 6902 (`add`, `remove`, `replace`, etc.) |    ✅   |       ✅       |
| Strategic Merge Patch | Declarative field merge using Kubernetes’ native logic |    ✅   |       ✅       |

***

## JSON 6902 Patches

JSON 6902 patches let you apply JSON-style operations to modify existing resources.

### 1. Inline Definition

Embed the patch directly in your `kustomization.yaml` under `patchesJson6902`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml

patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: api-deployment
    patch: |
      - op: replace
        path: /spec/replicas
        value: 5
```

### 2. External File

Separate the patch into its own file (`replica-patch.yaml`) and reference it:

**kustomization.yaml**

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml

patchesJson6902:
  - path: replica-patch.yaml
    target:
      group: apps
      version: v1
      kind: Deployment
      name: nginx-deployment
```

**replica-patch.yaml**

```yaml theme={null}
- op: replace
  path: /spec/replicas
  value: 5
```

> **lightbulb** External JSON 6902 patches are ideal when you need to apply multiple operations or share patches across environments.

***

## Strategic Merge Patches

Strategic Merge Patches allow you to declaratively merge fields into existing resources.

### 1. Inline Definition

Define the merge patch inline in `kustomization.yaml` under `patchesStrategicMerge`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml

patchesStrategicMerge:
  - |
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: api-deployment
    spec:
      replicas: 5
```

### 2. External File

Store the merge patch in a file (`strategic-replica-patch.yaml`) and reference it:

**kustomization.yaml**

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml

patchesStrategicMerge:
  - strategic-replica-patch.yaml
```

**strategic-replica-patch.yaml**

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 5
```

> **triangle-alert** The `metadata.name` in your patch must exactly match the target resource name; otherwise, the patch won’t be applied.

***

## Best Practices

* Use **inline patches** for small, one-off tweaks.
* Move to **external files** when your patches multiply or you need reuse.
* Group related patches in directories to manage environment overlays (e.g., `overlays/staging`, `overlays/production`).

***

## References

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [JSON Patch RFC 6902](https://tools.ietf.org/html/rfc6902)
* [Kubernetes Strategic Merge Patches](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kustomize/module/8b591384-c5e2-4411-afc1-443d3f2ba735/lesson/3143d106-366c-4cec-95d5-b7f9b3e890cf)
