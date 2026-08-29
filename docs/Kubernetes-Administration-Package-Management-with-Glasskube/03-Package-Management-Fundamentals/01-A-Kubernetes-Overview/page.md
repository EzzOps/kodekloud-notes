# A Kubernetes Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Management-Fundamentals/A-Kubernetes-Overview/page

Kubernetes overview covering cluster architecture, core components, objects, administrator responsibilities, and package management fundamentals for deploying and managing containerized applications

<Callout icon="lightbulb">
  If you're new to Kubernetes, start with Mumshad's "Kubernetes for the Absolute Beginners - Hands-on Tutorial" on KodeKloud: [https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial). This guide assumes a basic familiarity with Kubernetes concepts; the summary below focuses on the core ideas needed for package management and cluster administration.
</Callout>

Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications. It provides a logical management plane that abstracts physical infrastructure so teams can deploy and run distributed, microservice-based applications reliably across environments.

This section summarizes the cluster architecture, core objects, and the administrator responsibilities that are most relevant for package and cluster lifecycle management.

<Frame>
  <img alt="The image shows a diagram of a Kubernetes single-node cluster, highlighting components of the control plane and worker node, along with various namespaces and their corresponding elements like Pods and Services." />
</Frame>

## Key concepts

* Cluster: A set of nodes (physical or virtual) managed by Kubernetes.
* Control plane: Centralized components that manage the cluster state and scheduling.
* Worker nodes: Run containerized workloads (Pods).
* Objects (Manifests): Declarative YAML resources (Pods, Services, Deployments, CRDs, etc.) that describe desired state.
* API-first: Everything in Kubernetes is exposed and managed via the Kubernetes API (kubectl, controllers, operators).

## Core components

Below is a concise breakdown of the control plane and node-level components you’ll encounter frequently.

| Component type |          Component | Purpose / Responsibilities                                                    |
| -------------- | -----------------: | ----------------------------------------------------------------------------- |
| Control plane  |         API Server | Central communication endpoint for all clients and components.                |
| Control plane  |          Scheduler | Assigns Pods to nodes based on constraints and resource availability.         |
| Control plane  | Controller Manager | Reconciliation loop(s) that ensure desired state (replicas, endpoints, etc.). |
| Control plane  |               etcd | Distributed key-value store persisting cluster state and configuration.       |
| Worker node    |            kubelet | Agent that ensures Pods and containers are running according to spec.         |
| Worker node    |         kube-proxy | Implements Service networking and load-balancing rules on each node.          |

We’ll use a single-node cluster for labs, but the same components apply in multi-node production clusters.

## Built-in Kubernetes objects

Kubernetes provides built-in types used to define applications and infrastructure. Common examples include:

* Namespace
* Pod
* Deployment
* Service
* ConfigMap
* Secret
* Ingress

Custom Resource Definitions (CRDs) let you extend the API with new resource kinds that behave like native objects.

## Manifest structure

Kubernetes manifests are declarative YAML documents that generally follow the same top-level fields: `apiVersion`, `kind`, `metadata`, and `spec`. The example below shows a typical Deployment and a custom Package manifest (a CRD-style resource).

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
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
          image: nginx:1.21.6
          ports:
            - containerPort: 80
---
apiVersion: packages.example.com/v1
kind: PackageManifest
metadata:
  name: my-package
  namespace: default
spec:
  packageName: "crd-example"
  version: "1.21.6"
  repository: "https://packagecontroller.org/packages/mainline"
  configuration:
    replicas: 3
    resources:
      limits:
        cpu: "500m"
        memory: "256Mi"
```

<Callout icon="lightbulb">
  Custom Resource Definitions (CRDs) extend the Kubernetes API by allowing you to define new resource types. After a CRD is created, the API accepts and stores objects of that new type and they can be managed with the same tooling (`kubectl`, operators, controllers).
</Callout>

<Frame>
  <img alt="The image is a diagram of a Kubernetes single-node cluster, showing the control plane components (API Server, Scheduler, Controller Manager, etcd) and worker node components (Kubelet, Proxy) alongside various namespaces with Pods, Services, ConfigMaps, and other resources." />
</Frame>

## Operational landscape and ecosystem

Kubernetes provides primitives and an extensible API, but running a cluster at scale requires assembling many complementary tools. As Kelsey Hightower famously said, Kubernetes is a platform for building platforms — you still choose, integrate, and operate the pieces that meet your needs.

The Cloud Native Landscape (CNCF) categorizes projects across areas such as build, delivery, observability, and storage. Selecting the right tools (networking, policy, CI/CD, observability, etc.) is part of the administrative responsibility.

<Frame>
  <img alt="The image shows a section of the Cloud Native Landscape, displaying various projects and products categorized under &#x22;Application Definition & Image Build,&#x22; &#x22;Continuous Integration & Delivery,&#x22; &#x22;Database,&#x22; and &#x22;Streaming & Messaging.&#x22; Each category contains multiple logos representing different tools and platforms." />
</Frame>

Examples of platform components you’ll commonly integrate:

* Networking and security: Cilium
* Policy/authorization: Open Policy Agent (OPA)
* GitOps / CD: Argo CD
* Observability: Jaeger (tracing), Grafana (metrics)

## Role of the Kubernetes administrator

Kubernetes administrators (cluster operators) are responsible for building and maintaining the platform and its packages. Core responsibilities include:

| Area                          | Responsibilities / Examples                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| Setup & configuration         | Provision nodes, configure networking/storage, set up authentication and RBAC          |
| Package & cluster maintenance | Install, configure, and upgrade packages/CRs and ensure health and compatibility       |
| Security                      | Implement access control, network policies, image scanning, and vulnerability response |
| Resource management           | Monitor resource usage, apply quotas/limits, and optimize performance                  |
| Troubleshooting & support     | Diagnose issues, review logs/metrics/traces, and provide operational support           |

<Frame>
  <img alt="The image outlines the role of a Kubernetes Admin, highlighting tasks like cluster setup, maintenance, security, and resource management. It includes a visual of a gear with the Kubernetes logo and a stylized figure." />
</Frame>

Roles and responsibilities vary between organizations, but the areas above reflect the typical focus for admins, especially when managing package lifecycle and cluster health.

## Next steps

With this refresher complete, you have the cluster and object context needed to continue into package management topics: package authorship, CRDs for package controllers, installation workflows, and upgrade/rollback patterns.

## Links and references

* Kubernetes official docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Cloud Native Landscape (CNCF): [https://landscape.cncf.io/](https://landscape.cncf.io/)
* KodeKloud: [https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)
* Argo CD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Open Policy Agent (OPA): [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/60afaf37-3ea5-4474-b262-dc8c13c3afd4/lesson/4879d74c-34ea-4c86-a14d-a7e7462e0e27" />
</CardGroup>
