# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.name }}
spec:
  replicas: {{ .Values.replicas }}
  selector:
    matchLabels:
      app: {{ .Values.name }}
  template:
    metadata:
      labels:
        app: {{ .Values.name }}
    spec:
      containers:
        - name: {{ .Values.name }}-container
          image: my-app-image:1.0
```

```yaml theme={null}
# values.yaml
name: my-app
replicas: 3
```

```bash theme={null}
# Render the chart templates to stdout (does not install)
helm template my-chart
```

To install (render and submit) a chart into a cluster, give it a release name and optionally pass a values file:

```bash theme={null}
# Install the chart into the cluster using the values.yaml file
helm install my-release ./my-chart -f values.yaml
```

> **warning** Be careful with templates that manipulate namespaces or CRDs. Helm does not automatically update CRDs, and dependency namespace handling can cause unexpected results unless charts are designed properly.

## Pros and cons of using Helm

| Pros                                                                                            | Cons                                                                                                                     |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Reusable templating system promotes consistency and reduces duplication.                        | The Go templating language can be tricky to learn and debug for complex templates.                                       |
| Simplifies management of many Kubernetes manifests — install, upgrade, and delete complex apps. | Namespace handling for dependencies can be problematic and lead to conflicts.                                            |
| Large community and many pre-built charts available on Artifact Hub.                            | Helm doesn’t natively manage CRD upgrades — manual steps or hooks are often required.                                    |
| Supports package dependencies and tracks release history for rollbacks.                         | Helm does not automatically upgrade releases; external tooling is needed for automated updates.                          |
| Integrates with CI/CD and GitOps workflows for repeatable deployments.                          | Helm does not continuously monitor application health after install — combine with controllers or observability tooling. |

All in all, Helm excels at packaging and templating for Kubernetes workloads, but you should plan for lifecycle gaps (CRDs, automated upgrades, runtime health checks) by integrating additional tooling or processes where needed.

<Frame>
  <img alt="The image is a comparison chart showing the pros and cons of a topic, with pros listed on a green background and cons on a red-orange background." />
</Frame>

Glasskube addresses some of these Helm limitations; this article series explores how it integrates with and extends Helm workflows.

## Links and references

* [Artifact Hub](https://artifacthub.io) — find community Helm charts
* [text/template (Go)](https://pkg.go.dev/text/template) — Go templating language reference
* [Helm documentation](https://helm.sh/docs/) — official Helm docs and guides
* [Kubernetes documentation](https://kubernetes.io/docs/) — core API and resource references
* Helm for Beginners course (Mumshad Mannambeth) — recommended beginner resource

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/140a6ea0-1539-4d23-9aa6-0d07654a4526/lesson/56a35556-b899-412b-a19e-1ab1010723f4)


# Kubernetes Manifests

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Tooling/Kubernetes-Manifests/page

Explains Kubernetes manifests, declarative YAML resource definitions, usage with kubectl, benefits and trade offs, and why teams use tools like Helm for templating and packaging.

Kubernetes manifests are the foundational, declarative files that define the desired state of Kubernetes objects such as Deployments, Services, ClusterRoles, ReplicaSets, and CustomResourceDefinitions. While manifests themselves are not package managers, they are central to how you describe and manage native Kubernetes resources.

<Frame>
  <img alt="The image illustrates components of a Kubernetes cluster such as Pod, Service, and Deployment, represented as a structured diagram with a YAML file input." />
</Frame>

Manifests are typically authored in YAML (or JSON) — the formats accepted by the Kubernetes API — and applied to a cluster to create or update resources. They are declarative: you describe what you want, and the Kubernetes control plane reconciles the cluster to match that state.

Below is a simple example that defines a Deployment and a Service in a single manifest file:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-web-app
  labels:
    app: my-web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-web-app
  template:
    metadata:
      labels:
        app: my-web-app
    spec:
      containers:
        - name: my-web-app
          image: nginx:latest
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: my-web-app-service
  labels:
    app: my-web-app
spec:
  type: ClusterIP
  selector:
    app: my-web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply this manifest to your cluster using kubectl:

```bash theme={null}
kubectl apply -f my-manifests.yaml
```

> **lightbulb** Keep YAML indentation consistent and ensure the Deployment's pod template (spec.template under spec) is present — otherwise the API will reject the object.

Advantages and trade-offs of using raw Kubernetes manifests:

| Benefit                 | Details                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| Full control            | Manifests expose all fields of the Kubernetes API so you can tune behavior precisely. |
| Declarative & native    | The YAML maps directly to Kubernetes objects and describes the desired cluster state. |
| No abstraction overhead | No hidden behavior — what you declare is what Kubernetes understands.                 |

| Trade-off             | Details                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------- |
| Repetition            | No built-in templating or parameterization leads to duplicated manifests across environments. |
| Dependency management | You must handle ordering and inter-resource relationships outside the manifest files.         |
| Reuse and versioning  | Manifests lack native packaging/versioning; teams rely on external tools or workflows.        |
| Human error           | Large sets of hand-edited YAML can be error-prone and harder to maintain.                     |

<Frame>
  <img alt="The image shows a comparison of pros and cons, with &#x22;Pros&#x22; in green including aspects like fine-grained control and customization, and &#x22;Cons&#x22; in red highlighting issues like manual overhead and lack of templating." />
</Frame>

Because of these limitations, teams commonly adopt packaging or templating tools to reduce duplication, manage dependencies, and improve reuse. Helm is the most popular package manager for Kubernetes and is often chosen to add templating, versioning, and dependency features on top of raw manifests.

Links and references

* [Kubernetes Concepts — What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kubectl apply — Kubernetes CLI documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
* [Helm — The Kubernetes Package Manager](https://helm.sh/)

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/140a6ea0-1539-4d23-9aa6-0d07654a4526/lesson/c78e8d70-c8e4-41e4-8a8f-92e5e6b1d20b)
