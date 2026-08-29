# Manifest Format and Packaging

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Manifest-Format-and-Packaging/page

Comparison of Kubernetes manifest approaches for GitOps including plain YAML, Kustomize, and Helm, outlining workflows, benefits, limitations, and guidance on when to use each.

When using GitOps, your Git repository is the single source of truth for the declarative desired state of your system. What you store in Git are the Kubernetes manifests—the YAML files that describe the applications, infrastructure, and configuration that should exist in your cluster.

As systems scale, you need patterns to create, organize, and manage manifests consistently. This guide explains three common approaches—plain Kubernetes YAML, Kustomize, and Helm—how they integrate with GitOps, and when to choose each approach.

## 1) Plain Kubernetes manifests

The simplest approach is to store raw Kubernetes YAML files (for example `deployment.yaml`, `service.yaml`, `ingress.yaml`) directly in your repository. GitOps operators such as Argo CD or Flux CD read these files and apply them directly to the Kubernetes API without additional rendering.

Example repository layout:

```text theme={null}
my-simple-app-repo/
├── k8s/
│   ├── deployment.yaml   # Defines the application deployment
│   ├── service.yaml      # Exposes the application
│   └── ingress.yaml      # Manages external access
├── README.md
└── .gitignore
```

Why choose plain YAML:

* Direct one-to-one mapping to Kubernetes API objects—every field is explicit.
* Easy to inspect, review in PRs, and reason about.
* Low tooling overhead; minimal learning curve.

Limitations:

* Duplication across environments (dev/prod/staging) when only a few values differ.
* Manual updates across many manifests can be error-prone at scale.

When to use:

* Very small apps or proofs-of-concept.
* Cases where you need line-by-line control with no templating.

## 2) Kustomize

Kustomize is a native Kubernetes configuration tool for patching and composing YAML without templating. The common pattern uses a `base` (shared resources) and `overlays` (environment-specific patches).

Example project layout:

```text theme={null}
.
├── highway-animation
│   ├── base
│   │   ├── deployment.yml
│   │   ├── kustomization.yml
│   │   ├── namespace.yml
│   │   └── service.yml
│   └── overlays
│       ├── dev
│       │   ├── env-patch.yml
│       │   ├── kustomization.yml
│       │   └── replica-patch.yml
│       └── prod
│           ├── env-patch.yml
│           ├── image-patch.yml
│           ├── kustomization.yml
│           └── replica-patch.yml
```

Example `overlays/prod/kustomization.yaml`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namespace: kustomize-prod
patches:
  - path: replica-patch.yml
    target:
      kind: Deployment
      name: highway-animation
  - path: env-patch.yml
    target:
      kind: Deployment
      name: highway-animation
  - path: image-patch.yml
    target:
      kind: Deployment
      name: highway-animation
```

How Kustomize works with GitOps:

* Store `base` and `overlays` in Git.
* GitOps operators that support Kustomize (Argo CD, Flux) will render the selected overlay by applying patches to the base, producing final YAML that is applied to the cluster.

Benefits:

* Avoids duplicate manifests for each environment.
* Clear separation between shared resources and environment-specific changes (replicas, images, env vars).
* No templating language to learn—uses standard YAML plus patches.

Limitations:

* Best suited for incremental differences to a base. Large divergences across environments can be awkward.
* Less ideal for packaging reusable distributed charts with complex templating needs.

When to use:

* Single applications deployed to multiple environments with small variations.
* Teams preferring YAML-native tooling and minimal templating.

## 3) Helm

Helm is a package manager for Kubernetes that uses templates and `values.yaml` to generate final manifests. Helm charts bundle related resources and can declare dependencies.

Typical GitOps workflow with Helm:

* Commit your chart (or a reference to a chart) and `values.yaml` to Git.
* GitOps operators with Helm support render the chart using your values and apply the rendered manifests to the cluster.

Example `values.yaml` (custom overrides):

```yaml theme={null}
replicaCount: 5
image:
  tag: "2.0.0-prod"
service:
  type: LoadBalancer
```

Benefits:

* Charts bundle complex applications and dependencies, enabling sharing and reuse.
* Powerful templating and overrides (`values.yaml`) for flexible environment configuration.
* Widely used for distributing third-party software (Prometheus, NGINX Ingress) via public Helm repositories.

Limitations:

* Templating adds complexity and a learning curve.
* Rendered output is generated at deploy time—less direct visibility into final manifests unless you render locally or rely on the GitOps operator to show rendered output.

When to use:

* Packaging complex applications or shared infrastructure components.
* Deploying third-party software or when you need versioned, distributable application packages.

## Choosing the right approach

Which approach to choose depends on your project complexity and operational needs:

| Approach   | Best for                                    | Key advantages                                        | Example files                                  |
| ---------- | ------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------- |
| Plain YAML | Small/simple apps, PoCs                     | Direct API mapping, easy review                       | `deployment.yaml`, `service.yaml`              |
| Kustomize  | Same app across multiple environments       | Reuse base, apply patches per environment             | `base/`, `overlays/dev/`, `kustomization.yaml` |
| Helm       | Complex apps, packaged charts, dependencies | Templating, versioned charts, `values.yaml` overrides | `Chart.yaml`, `templates/`, `values.yaml`      |

You can also mix approaches. For example, use Kustomize to patch a set of manifests that include rendered Helm releases, or keep simple resources as plain YAML while packaging third-party components with Helm. The important part: keep everything declarative in Git so your GitOps operator can manage the complete deployment pipeline.

<Callout icon="lightbulb">
  Mix-and-match strategies are common: use plain YAML for small resources, Kustomize for environment overlays, and Helm for complex or third-party packages. Most GitOps operators (Argo CD, Flux) can render and apply manifests from any of these formats.
</Callout>

<Frame>
  <img alt="The image compares three Kubernetes manifest formats and packaging tools: plain YAML for simple applications, Kustomize for managing configurations across environments, and Helm for packaging complex applications with dependencies." />
</Frame>

## Links and references

* [Argo CD documentation](https://argo-cd.readthedocs.io/)
* [Flux CD documentation](https://fluxcd.io/)
* [Kustomize documentation](https://kustomize.io/)
* [Helm documentation](https://helm.sh/docs/)
* Kubernetes concepts: [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/0ce93da9-fc89-4973-8147-2f87e1d965d0" />
</CardGroup>
