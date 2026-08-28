# db-depl.yaml
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

```yaml theme={null}
# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: db-service
spec:
  selector:
    component: db-depl
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
  type: LoadBalancer
```

Your goal is to:

* Add a shared label: `org: KodeKloud`
* Append `-dev` to every resource name

Manually editing each file is tedious and error-prone. Kustomize simplifies this with common transformers.

## Common Transformers Overview

<Frame>
  ![The image lists common transformations for Kubernetes resources, including adding labels, prefixes/suffixes, namespaces, and annotations.](https://kodekloud.com/kk-media/image/upload/v1752880922/notes-assets/images/Kustomize-Common-Transformers/kubernetes-resource-transformations-list.jpg)
</Frame>

| Transformer        | Field Name                     | Purpose                                      |
| ------------------ | ------------------------------ | -------------------------------------------- |
| Common Labels      | `commonLabels`                 | Add one or more labels to all resources      |
| Name Prefix/Suffix | `namePrefix`<br />`nameSuffix` | Prepend or append text to resource names     |
| Namespace          | `namespace`                    | Assign a namespace to every resource         |
| Common Annotations | `commonAnnotations`            | Add one or more annotations to all resources |

### 1. Apply Common Labels

Add the `commonLabels` block to your `kustomization.yaml`:

```yaml theme={null}
resources:
  - db-depl.yaml
  - db-service.yaml

commonLabels:
  org: KodeKloud
```

<Callout icon="lightbulb">
  When you run `kustomize build`, these labels will be merged into every resource’s `metadata.labels`.
</Callout>

**Generated output (Service example):**

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: db-service
  labels:
    org: KodeKloud
spec:
  selector:
    component: db-depl
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
  type: LoadBalancer
```

### 2. Set a Namespace

To place all resources into a specific namespace:

```yaml theme={null}
namespace: lab
```

**Resulting snippet:**

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: db-service
  namespace: lab
  labels:
    org: KodeKloud
# …
```

### 3. Add Name Prefix & Suffix

Prepend and append text to every resource name:

```yaml theme={null}
namePrefix: kodekloud-
nameSuffix: -dev
```

**Rendered output:**

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: kodekloud-db-service-dev
  labels:
    org: KodeKloud
  namespace: lab
# …
```

<Callout icon="triangle-alert">
  Choosing very long prefixes or suffixes can push resource names over Kubernetes’ max-length limit (63 characters). Always verify final name lengths.
</Callout>

### 4. Inject Common Annotations

Include the following to add annotations across all manifests:

```yaml theme={null}
commonAnnotations:
  branch: master
```

**Sample annotation merge:**

```yaml theme={null}
metadata:
  annotations:
    branch: master
# …
```

***

By combining these four settings in a single `kustomization.yaml`, you can transform your base manifests consistently and safely—no manual edits required.

## Links and References

* [Kustomize Official Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubernetes Resource Configuration](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* [Managing Kubernetes with Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/8b591384-c5e2-4411-afc1-443d3f2ba735/lesson/d3956634-6fe0-4c41-b8bf-bfed87fc99dd" />
</CardGroup>


# Components

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Components/page

This guide explains how to define and use components in Kustomize for packaging optional features into reusable configuration blocks.

In this guide, you’ll learn how to define and consume **components** in Kustomize. Components let you package optional features—such as additional resources, patches, ConfigMaps, or Secrets—into self-contained units. You can then import them in selected overlays without duplicating code, ensuring consistency and reducing configuration drift.

## When to Use Components

Use components when an application offers optional features that only apply to some overlays. If a feature is required in **all** overlays, include it in your base. For features needed by only a **subset**, bundle them as components to avoid repetition.

## Visual Example

Consider three deployment environments:

* **dev** (development)
* **premium** (for premium customers)
* **standalone** (self-hosted)

Our shared **base/** folder holds common resources. We also have two optional features:

* **Caching** (backed by Redis) — enabled in **premium** and **standalone**
* **External DB** (Postgres) — enabled in **dev** and **premium**

Where should we place the Redis and Postgres manifests so only the right overlays include them?

<Frame>
  ![The image is a flowchart showing components with connections between "base," "caching," "dev," "Premium," and "Self hosted." It also lists "Caching" and "External DB" with related items.](https://kodekloud.com/kk-media/image/upload/v1752880923/notes-assets/images/Kustomize-Components/flowchart-base-caching-dev-premium-selfhosted.jpg)
</Frame>

Instead of duplicating manifests in overlays—or adding unwanted features to **base**—we create two components (`caching` and `db`) and import them selectively.

<Frame>
  ![The image is a flowchart titled "Components" showing a hierarchy with nodes labeled "base," "dev," "Premium," "Self hosted," "Components," "caching," and "db." It illustrates the relationships between these components.](https://kodekloud.com/kk-media/image/upload/v1752880924/notes-assets/images/Kustomize-Components/components-flowchart-hierarchy-nodes.jpg)
</Frame>

## Component Features Table

| Component     | Purpose                          | Overlays            |
| ------------- | -------------------------------- | ------------------- |
| caching       | Redis Deployment & service       | premium, standalone |
| db (External) | Postgres Deployment & DB secrets | dev, premium        |

## Project Structure

```plaintext theme={null}
k8s/
├── base/
│   ├── api-depl.yaml
│   └── kustomization.yaml
├── components/
│   ├── caching/
│   │   ├── kustomization.yaml
│   │   ├── deployment-patch.yaml
│   │   └── redis-depl.yaml
│   └── db/
│       ├── kustomization.yaml
│       ├── deployment-patch.yaml
│       └── postgres-depl.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── premium/
    │   └── kustomization.yaml
    └── standalone/
        └── kustomization.yaml
```

* **base/**: Common resources (e.g., API Deployment)
* **components/**: Feature directories (`caching/`, `db/`)
* **overlays/**: Environment-specific kustomizations

***

## Database Component

The **db** component adds a Postgres deployment, a Secret for credentials, and patches your API Deployment.

### `postgres-depl.yaml`

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: postgres
  template:
    metadata:
      labels:
        component: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:latest
```

<Callout icon="lightbulb">
  Components require `kind: Component` with the `v1alpha1` API. Ensure you’re running Kustomize v4.x or later.
</Callout>

### `kustomization.yaml` (Component)

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component
resources:
  - postgres-depl.yaml
secretGenerator:
  - name: postgres-cred
    literals:
      - password=postgres123
patches:
  - deployment-patch.yaml
```

### `deployment-patch.yaml`

This strategic merge patch injects the `DB_PASSWORD` from the Secret into your API Deployment:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    spec:
      containers:
        - name: api
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-cred
                  key: password
```

***

## Overlay Configuration

Each overlay’s `kustomization.yaml` pulls in `base` plus the desired components.

### Example: Dev Overlay

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
components:
  - ../../components/db
```

* **premium** overlay adds both `../../components/db` and `../../components/caching`.
* **standalone** overlay adds only `../../components/caching`.

With Kustomize components, you can define optional feature logic once and enable it in any overlay by adding a single entry.

## Links and References

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubernetes Concepts: Overlays](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#kustomize-overlays)
* [Redis Official Image](https://hub.docker.com/_/redis)
* [Postgres Official Image](https://hub.docker.com/_/postgres)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/8b591384-c5e2-4411-afc1-443d3f2ba735/lesson/baa7cfb7-7316-4be4-88c5-acfe45f59d8e" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kustomize/module/8b591384-c5e2-4411-afc1-443d3f2ba735/lesson/bb1ad6fa-3980-4462-bdf4-4fe87d267fe7" />
</CardGroup>
