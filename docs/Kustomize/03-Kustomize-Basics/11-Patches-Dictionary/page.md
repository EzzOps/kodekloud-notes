# base/kustomization.yaml
resources:
  - nginx-depl.yaml
  - service.yaml
  - redis-depl.yaml
```

Example of a base Deployment:

```yaml theme={null}
# base/nginx-depl.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```

<Callout icon="lightbulb">
  Make sure each file listed under `resources:` has a valid manifest. You can [validate your YAML](https://kubectl.docs.kubernetes.io/guides/validation/) with `kubectl apply --dry-run=client -f`.
</Callout>

***

## 2. Dev Overlay

The Dev overlay references the base and patches the replica count using JSON 6902.

```yaml theme={null}
# overlays/dev/kustomization.yaml
resources:
  - ../../base

patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: nginx-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 2
```

```bash theme={null}
# Generate dev manifests
kustomize build overlays/dev
```

| Field             | Description                                       |
| ----------------- | ------------------------------------------------- |
| `resources:`      | Relative path to the shared base directory        |
| `patchesJson6902` | JSON 6902 patch to modify `/spec/replicas` to `2` |

***

## 3. Production Overlay

For production, you can both patch existing resources and add new ones (e.g., a Grafana deployment).

```bash theme={null}
k8s/
└── overlays/
    └── prod/
        ├── kustomization.yaml
        ├── config-map.yaml
        └── grafana-depl.yaml
```

```yaml theme={null}
# overlays/prod/kustomization.yaml
resources:
  - ../../base
  - grafana-depl.yaml

patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: nginx-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 3
```

```yaml theme={null}
# overlays/prod/grafana-depl.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:latest
```

<Callout icon="triangle-alert">
  Ensure new resources like `grafana-depl.yaml` are listed under `resources:` in the overlay’s `kustomization.yaml`. Otherwise, they won’t be rendered.
</Callout>

***

## 4. Flexible Directory Structures

Kustomize supports organizing both **base** and **overlays** in nested feature folders. For example:

```bash theme={null}
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── db/
│   │   ├── db-depl.yaml
│   │   ├── db-svc.yaml
│   │   └── kustomization.yaml
│   └── api/
│       ├── api-depl.yaml
│       ├── api-svc.yaml
│       └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   ├── db/
    │   │   ├── db-patch.yaml
    │   │   └── kustomization.yaml
    │   └── api/
    │       ├── api-patch.yaml
    │       └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        └── api/
            ├── api-patch.yaml
            └── kustomization.yaml
```

* **Feature-based grouping**: Split `base/` into `db/` and `api/` with individual `kustomization.yaml`.
* **Overlay mirroring**: Maintain a similar hierarchy under each overlay for targeted patches.
* **Cross-references**: Each overlay’s kustomization file imports the correct child resources and patches.

***

## References

* [Kustomize Official Documentation](https://kubectl.docs.kubernetes.io/guides/introduction/)
* [JSON 6902 Patch](https://tools.ietf.org/html/rfc6902)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-c5e2-4411-afc1-443d3f2ba735/lesson/5feb97e6-536b-4eb9-adf9-f14ce520c327" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.[SECRET_REDACTED]-c5e2-4411-afc1-443d3f2ba735/lesson/20de59f0-9654-405a-af9e-6ebb063c29e1" />
</CardGroup>


# Patches Dictionary

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Patches-Dictionary/page

Learn to update, add, and remove keys in a Kubernetes Deployment using Kustomize with JSON 6902 and Strategic Merge Patches.

Learn how to update, add, and remove keys (e.g., labels) in a Kubernetes Deployment using Kustomize. We’ll demonstrate both JSON 6902 patches and Strategic Merge Patches with clear examples and best practices.

## Overview

Kustomize supports two main patch mechanisms:

| Patch Type            | Syntax       | Use Case                               | Reference                                                                                                         |
| --------------------- | ------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| JSON 6902 Patch       | JSON Pointer | Precise `add`, `replace`, `remove` ops | [JSON Patch (RFC6902)](https://tools.ietf.org/html/rfc6902)                                                       |
| Strategic Merge Patch | YAML merge   | Declarative updates, merges by key     | [Strategic Merge Patch](https://kubernetes.io/docs/concepts/overview/working-with-objects/strategic-merge-patch/) |

<Callout icon="lightbulb">
  Use JSON 6902 when you need fine-grained control. Choose Strategic Merge for simpler, declarative label or annotation updates.
</Callout>

***

## Base Deployment Configuration

Save this as `base/api-deployment.yaml`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
    spec:
      containers:
        - name: nginx
          image: nginx
```

In the same directory, your `kustomization.yaml` should include:

```yaml theme={null}
resources:
  - api-deployment.yaml
```

***

## 1. Replacing a Label

### 1.1 JSON 6902 Patch

Add this section under `patches` in `kustomization.yaml`:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /spec/template/metadata/labels/component
        value: web
```

* **op: replace** – updates the existing `component` label.
* **path** – JSON Pointer to `/spec/template/metadata/labels/component`.
* **value: web** – new label value.

### 1.2 Strategic Merge Patch

Reference an external YAML file in `kustomization.yaml`:

```yaml theme={null}
patches:
  - label-replace.yaml
```

Create `label-replace.yaml`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    metadata:
      labels:
        component: web
```

Kustomize merges only the provided fields, updating `component` to `web`.

***

## 2. Adding a Label

### 2.1 JSON 6902 Patch

In `kustomization.yaml`:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: add
        path: /spec/template/metadata/labels/org
        value: kodekloud
```

* **op: add** – inserts a new key `org`.
* **value: kodekloud** – label value added under `.spec.template.metadata.labels`.

### 2.2 Strategic Merge Patch

Reference a file in `kustomization.yaml`:

```yaml theme={null}
patches:
  - label-add.yaml
```

Create `label-add.yaml`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    metadata:
      labels:
        org: kodekloud
```

After applying, labels will include both `component: api` and `org: kodekloud`.

***

## 3. Removing a Label

Assume the Deployment now has:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
        org: kodekloud
    spec:
      containers:
      - name: nginx
        image: nginx
```

### 3.1 JSON 6902 Patch

In `kustomization.yaml`:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: remove
        path: /spec/template/metadata/labels/org
```

* **op: remove** – deletes the `org` key.

### 3.2 Strategic Merge Patch

Reference in `kustomization.yaml`:

```yaml theme={null}
patches:
  - label-remove.yaml
```

Create `label-remove.yaml`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    metadata:
      labels:
        org: null
```

<Callout icon="lightbulb">
  Setting `org: null` instructs Kustomize to remove that label key.
</Callout>

***

## Links and References

* [Kustomize Patches Reference](https://kubectl.docs.kubernetes.io/references/kustomize/patches/)
* [JSON Patch (RFC6902)](https://tools.ietf.org/html/rfc6902)
* [Strategic Merge Patch](https://kubernetes.io/docs/concepts/overview/working-with-objects/strategic-merge-patch/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-c5e2-4411-afc1-443d3f2ba735/lesson/581f5ca5-823d-4415-9f90-3853ccf009ab" />
</CardGroup>
