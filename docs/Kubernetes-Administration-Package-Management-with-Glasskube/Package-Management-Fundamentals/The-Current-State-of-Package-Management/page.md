# The Current State of Package Management

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Management-Fundamentals/The-Current-State-of-Package-Management/page

Overview of Kubernetes package management challenges, workflows, Helm limitations, CRD handling, dependency and namespace isolation, secrets management, and desired features for GitOps-driven deployments

To understand the current state of package management for Kubernetes, we first need to agree on what a "package" means in this context.

When you inspect a complex Kubernetes application—take the Argo CD dashboard below as an example—you’ll find many components and Kubernetes objects deployed and orchestrated together. Each of those objects is part of a broader package that includes manifests, CRDs, configuration, and dependencies.

<Frame>
  <img alt="The image shows a user interface of a software application, displaying a dashboard with several tiles representing different applications, each with options to sync, refresh, or delete. It includes filters for sync and health status on the left side." />
</Frame>

What a Kubernetes package typically contains

| Component                          | What it contains / example                                                                                 |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Manifests                          | Kubernetes YAML manifests for `Deployment`, `Service`, `ConfigMap`, `Secret`, etc.                         |
| CRDs (Custom Resource Definitions) | Definitions that extend the Kubernetes API for more complex applications (e.g., Argo CD CRDs).             |
| Configuration values               | Exposed configuration surface for customization at deploy/upgrade time (for Helm charts, `values.yaml`).   |
| Dependencies                       | Other packages or charts required for the package to function (e.g., sidecars, operators).                 |
| Bundles of YAML files              | The final installable artifacts: collections of manifests that the package manager applies to the cluster. |

<Frame>
  <img alt="The image shows a diagram featuring categories such as Manifests, CRDs, Configuration Values, and Dependencies, each represented by icons, with YAML file bundles below. There's also a cartoon character on the left." />
</Frame>

Typical package lifecycle

Package management workflows generally include four core phases. Each phase benefits from automation, validation, and observability to reduce risk and operational overhead.

| Step      | Purpose                                         | Tooling / benefits                                              |
| --------- | ----------------------------------------------- | --------------------------------------------------------------- |
| Test      | Validate package behavior in sandbox or staging | Automated tests, dry-run renders, CI pipelines                  |
| Configure | Set and customize package settings              | Values files, parameterized templates, secure secrets injection |
| Install   | Deploy package into a target cluster            | Declarative installers, RBAC, namespace isolation               |
| Update    | Apply controlled upgrades and rollbacks         | Versioned releases, health checks, canaries/blue-green          |

<Frame>
  <img alt="The image illustrates &#x22;A Typical Package Lifecycle&#x22; with four steps: Test, Configure, Install, and Update, each represented within colored boxes." />
</Frame>

Two common, historical approaches

Without a unified package manager, operators have typically relied on:

* Raw Kubernetes manifests — full control, but hard to scale for complex apps and upgrades.
* Helm — a widely-used package manager that offers templating and dependency support, but it doesn’t address every operational requirement (for example, strict namespace isolation for dependencies).

Package manager wishlist

An ideal Kubernetes package manager would solve the major pain points operators face today:

1. Full package definition capabilities, including CRDs, manifests, lifecycle hooks, and metadata.
2. Clear and declarative dependency management, with namespace and installation separation.
3. Simple, safe install and upgrade workflows, including rollbacks and health-aware upgrades.
4. Real-time state and health monitoring for installed packages.
5. Flexible templating plus secure secret injection and management.
6. Native GitOps support for declarative workflows, auditability, and observability.

<Frame>
  <img alt="The image displays a &#x22;Package Management Wish List&#x22; with nine items including package definition, customization, and GitOps, among others. Each item is numbered and presented in a blue-green gradient box." />
</Frame>

An example: umbrella charts and namespace isolation

A common practical shortcoming involves how Helm handles dependencies. Consider an umbrella Helm chart that depends on another chart. Here’s an umbrella chart example for an NVIDIA GPU Operator that depends on the Node Feature Discovery chart:

```yaml theme={null}
apiVersion: v2
name: gpu-operator
version: v1.0.0-devel
kubeVersion: ">= 1.16.0-0"
sources:
  - https://github.com/NVIDIA/gpu-operator
home: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/overview.html
dependencies:
  - name: node-feature-discovery
    version: v0.16.3
    repository: https://kubernetes-sigs.github.io/node-feature-discovery/charts
    condition: nfd.enabled
```

When you install this umbrella chart, Helm typically renders and installs both the parent chart and its dependency into the same target namespace. That causes components representing different logical packages to live together in one namespace, which breaks common best practices for isolation and lifecycle management.

<Callout icon="lightbulb">
  Umbrella charts make dependency installation easy, but they do not provide built-in, declarative control over installing dependencies into separate namespaces. That often forces operators to adopt additional conventions or tooling to achieve proper isolation.
</Callout>

Current package management pain points

Comparing today’s tooling with the wishlist shows several recurring issues operators face:

* Dependency management: handling complex graphs, version constraints, and cross-package interactions is inconsistent across tools.
* Configuration complexity: large, nested `values.yaml` files make customization and overrides error-prone.
* Secret injection: secure secrets handling often depends on external tools (for example, SealedSecrets or External Secrets) and extra integration work.
* Umbrella chart limitations: namespace collisions and ambiguous installation scope can complicate multi-tenant deployments.
* CRD updates: safely upgrading CRDs is difficult; Helm’s CRD handling is limited and can cause upgrade friction.
* Lacking GitOps standardization: no single standard exists for how packages should be packaged and operated in GitOps workflows like Argo CD.

<Frame>
  <img alt="The image lists common package management bottlenecks, including dependency management, configuration complexity, secret injection, umbrella charts, CRD updates, and lacking GitOps support." />
</Frame>

Links and references

* Argo CD: [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* Helm (for chart concepts and templating): [https://learn.kodekloud.com/user/courses/helm-for-beginners](https://learn.kodekloud.com/user/courses/helm-for-beginners)
* Node Feature Discovery chart repo: [https://kubernetes-sigs.github.io/node-feature-discovery/charts](https://kubernetes-sigs.github.io/node-feature-discovery/charts)
* SealedSecrets intro: [https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes](https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes)
* External Secrets: [https://external-secrets.io/](https://external-secrets.io/)

Keywords: Kubernetes package management, Helm umbrella charts, CRDs, GitOps, namespace isolation, secrets injection, package lifecycle, Argo CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/60afaf37-3ea5-4474-b262-dc8c13c3afd4/lesson/7d89da6a-302b-4975-a9d2-072d4a7db409" />
</CardGroup>
