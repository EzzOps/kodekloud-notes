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

# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: db-service
spec:
  selector:
    component: db-depl
  ports:
  - protocol: "TCP"
    port: 27017
    targetPort: 27017
  type: LoadBalancer
```

Suppose you want to add a common configuration—such as a label identifying your organization—to all your Kubernetes resources. Manually editing each YAML file is not scalable, particularly in environments with dozens of resources. Instead, Kustomize applies these common changes automatically using transformers.

For example, to add the label "org: KodeKloud" to every resource, you might update your files as follows:

```yaml theme={null}
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
      org: KodeKloud
  template:
    metadata:
      labels:
        component: api
        org: KodeKloud
    spec:
      containers:
      - name: nginx
        image: nginx

# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  labels:
    org: KodeKloud
spec:
  selector:
    component: api
  ports:
  - protocol: "TCP"
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

Or, if you need to append a suffix (e.g., "-dev") to resource names, your Deployment could be modified like this:

```yaml theme={null}
# db-depl.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
      org: KodeKloud
  template:
    metadata:
      labels:
        component: api
        org: KodeKloud
    spec:
      containers:
      - name: nginx
        image: nginx
```

Rather than editing each file manually, Kustomize uses transformers to automate these updates. Below are several common transformers you can leverage:

***

## Common Label Transformation

The common label transformer automatically adds a specified label to every resource included in your kustomization.yaml file. For instance, to ensure every resource includes the label "org: KodeKloud", add the following to your configuration:

```yaml theme={null}
commonLabels:
  org: KodeKloud
```

When applied, this transformer injects the label into the metadata of every resource, streamlining updates and reducing human error.

***

## Namespace Transformation

Assigning resources to a specific namespace is simplified with the namespace transformer. By specifying the namespace in your kustomization.yaml, you ensure that all resources are deployed into that namespace. For example, consider the following Service definition:

```yaml theme={null}
# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    branch: master
  labels:
    org: KodeKloud
spec:
  selector:
    component: api
  ports:
  - port: 80
    protocol: TCP
    targetPort: 3000
  type: LoadBalancer
```

And in your configuration file, include:

```yaml theme={null}
namespace: lab
```

> **lightbulb** This setting ensures that the Service, along with all other defined resources, will be deployed to the "lab" namespace.

***

## Prefix and Suffix Transformation

With the prefix/suffix transformer, you can automatically alter the names of your resources without manually editing every file. For example, to add the prefix "KodeKLOUD-" and suffix "-dev" to a Service name, use the following configuration:

```yaml theme={null}
namePrefix: KodeKLOUD-
nameSuffix: -dev
```

After transformation, the Service's name will be updated to "KodeKLOUD-api-service-dev". Here’s an example of the transformed Service resource:

```yaml theme={null}
# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: KodeKLOUD-api-service-dev
spec:
  selector:
    component: api
  ports:
  - port: 80
    protocol: TCP
    targetPort: 3000
  type: LoadBalancer
```

***

## Common Annotations Transformation

If you need to add common annotations to all Kubernetes objects, you can define these in your kustomization.yaml file. For example, to add the annotation "branch: master" everywhere, your configuration might look like this:

```yaml theme={null}
# db-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    branch: master
  labels:
    org: KodeKloud
  namespace: auth
spec:
  selector:
    component: api
  ports:
    - port: 80
      protocol: TCP
      targetPort: 3000
  type: LoadBalancer

# Kustomization.yaml
commonAnnotations:
  branch: master
```

This setup guarantees that the annotation is consistently applied across all resources, eliminating the need for repetitive edits.

***

## Summary of Common Transformers

Below is a table summarizing the common transformers available in Kustomize and their use cases:

| Transformer        | Use Case                                      | Example Configuration                           |
| ------------------ | --------------------------------------------- | ----------------------------------------------- |
| Common Label       | Add a label to all resources                  | `commonLabels: { org: KodeKloud }`              |
| Namespace          | Assign resources to a specific namespace      | `namespace: lab`                                |
| Prefix/Suffix      | Modify resource names with a prefix or suffix | `namePrefix: KodeKLOUD-` and `nameSuffix: -dev` |
| Common Annotations | Apply consistent annotations to resources     | `commonAnnotations: { branch: master }`         |

Using these transformers can greatly simplify deployment and maintenance processes, especially when managing a large suite of Kubernetes manifests.

For more details on Kubernetes and managing configurations, check out the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/f5d9be8b-990f-40eb-bfc2-6594c0cb8a3b)


# Components

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Components/page

This article explains Kustomize components for reusable configuration logic in Kubernetes, enabling optional features in specific application overlays.

In this lesson, we'll dive into a Kustomize feature called components. Components let you define reusable configuration logic that can be imported into multiple overlays. This approach is ideal when your application supports several optional features that should only be enabled in specific overlays.

Consider a scenario where you have feature-specific configurations. If the feature is required in every overlay, you might include the configuration in your base. However, when a feature should only be active in a subset of overlays, duplicating the configuration across these environments can lead to drift and maintenance headaches. Components address this challenge by allowing you to keep your configuration logic in one location and import it into the overlays that need it.

For example, imagine an application deployed in three variations: development, premium, and self-hosted. The shared base configuration applies to all overlays. Now, suppose the application supports two optional features:

1. Caching – enabled only for the premium and self-hosted versions. This requires a Redis database and its associated configurations.
2. An external database service (e.g., Postgres) – enabled only for the development and premium versions.

![The image describes components as reusable configuration logic pieces, useful for enabling optional features in specific application overlays.](https://kodekloud.com/kk-media/image/upload/v1752871121/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Components/frame_20.jpg)

Without components, you might consider placing the caching configuration in the base. However, this would enable caching for all overlays, including development, which is not desired. Alternatively, you could copy the caching configuration into the premium and self-hosted overlays, but this risks configuration drift and complicates scaling when more overlays are added. Components allow you to define the caching logic just once and import it wherever it's required.

Let's visualize how the project structure might look. Imagine a directory structure with overlays for development, premium, and self-hosted deployments, a base folder for shared configurations, and a separate directory for components:

```text theme={null}
k8s/
├── base/
│   ├── kustomization.yaml
│   └── api-depl.yaml
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

The three overlays each contain a minimal `kustomization.yaml` file that imports shared configurations from the base folder. The new "components" directory houses two distinct components: one for caching and one for the external database. For instance, the caching component includes all Kubernetes configurations necessary for setting up Redis (deployments, secrets, patches, etc.), while the database component manages all configurations needed for an external Postgres database.

![The image is a flowchart showing components like base, dev, Premium, Self-hosted, caching, and db, connected by arrows, under the title "Components."](https://kodekloud.com/kk-media/image/upload/v1752871122/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Components/frame_250.jpg)

> **lightbulb** By isolating the configuration logic into components, overlays that require specific features—such as caching or an external database—can simply import the corresponding component. This method minimizes duplicate code and reduces the chance of error.

***

## Implementing a Component

Consider the project structure described above. The `base` directory contains common configurations, including a `kustomization.yaml` file and an API deployment file. The `components` directory holds feature-specific folders for caching and the database, while the `overlays` directory contains environment-specific configurations for dev, premium, and standalone deployments.

Let's focus on the database component. Within the database component folder, you will find the following files:

* **postgres-depl.yaml:** Defines the Kubernetes Deployment required for a Postgres instance.
* **deployment-patch.yaml:** A strategic merge patch that modifies the base API deployment by adding an environment variable for the new database connection.
* **kustomization.yaml:** Specifies the component metadata, resources, secret generator, and patch references.

### Postgres Deployment Configuration

Below is an example of the Postgres Deployment configuration defined in `postgres-depl.yaml`:

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
          image: postgres
```

### Component kustomization.yaml

In the component's `kustomization.yaml` file, notice that the ApiVersion and Kind differ from a typical configuration file. Because this is defined as a component, the ApiVersion is `kustomize.config.k8s.io/v1alpha1` and the Kind is `Component`. This file references the resources for the component, defines a secret for the database password, and applies any necessary patches:

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

The secret generator ensures that the database password is managed and injected securely. Meanwhile, the patch described in `deployment-patch.yaml` adjusts the base API deployment to use the newly created secret.

### Updating the Base Deployment

The `deployment-patch.yaml` file adds an environment variable to the API deployment so that the application can connect to the new Postgres database. An example patch looks like this:

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

### Importing Components in Overlays

To incorporate the external database settings, overlays that require this feature (for example, the dev overlay) import the database component. The overlay's `kustomization.yaml` file includes the base configuration and then adds the component:

```yaml theme={null}
bases:
  - ../../base
components:
  - ../../components/db
```

This setup ensures that the base API deployment is patched with the database settings from the imported component.

> **lightbulb** Using components in your Kubernetes configuration allows you to manage optional features efficiently. It simplifies maintenance, reduces duplicate code, and minimizes the risk of configuration drift across multiple environments.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/19fbbe24-267f-48ea-9a01-56cf06d6c842)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/66fefe64-87fd-4d25-a46f-c66dce62def7)
