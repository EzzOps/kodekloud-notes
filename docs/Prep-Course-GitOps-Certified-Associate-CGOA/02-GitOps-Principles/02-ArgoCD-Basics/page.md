# Application 'color-app' created
```

After you create the Application, Argo CD continuously compares the live cluster state against the Git-specified desired state and will deploy or reconcile resources according to the configured sync policy.

> **lightbulb** An Argo CD Application has two primary parts:

  * `source`: where the desired manifests live (Git repo, path, branch/tag, Helm chart, Kustomize or Jsonnet).
  * `destination`: the target Kubernetes API server and namespace where resources should be applied.

## Example Application manifest

Below is a representative `Application` manifest for the same app created above:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: color-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/sid/app-1.git'
    targetRevision: HEAD
    path: team-a/color
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: color
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Key fields explained

| Field                                  | Purpose                                                                                                            | Example / Notes                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `metadata.name` / `metadata.namespace` | Identifies the Application resource and the namespace where Argo CD control plane runs                             | `name: color-app`<br />`namespace: argocd`                                                          |
| `spec.project`                         | Associates the Application with an Argo CD Project to enforce repo/cluster/namespace policies                      | `project: default`                                                                                  |
| `spec.source`                          | Where to retrieve and how to render the desired state (Git repo, path, branch/tag, Helm chart, Kustomize, Jsonnet) | `repoURL: 'https://github.com/sid/app-1.git'`<br />`targetRevision: HEAD`<br />`path: team-a/color` |
| `spec.destination`                     | The target Kubernetes API server and namespace where resources will be applied                                     | `server: 'https://kubernetes.default.svc'` (in-cluster) <br />`namespace: color`                    |
| `spec.syncPolicy`                      | How Argo CD should keep cluster state in sync with Git (automated/manual, self-heal, sync options)                 | Example:<br />`automated: { selfHeal: true }`<br />Sync option: `CreateNamespace=true`              |

### Notes on `spec.source`

* Supports multiple formats: Git manifests, Helm charts, Kustomize overlays, and Jsonnet.
* `targetRevision` accepts a branch name, tag, or commit SHA (default: `HEAD`).

### Notes on `spec.destination`

* For in-cluster deployments use `https://kubernetes.default.svc`.
* For external clusters use the API server URL as registered in Argo CD (via `argocd cluster add` or the UI).

### Notes on `spec.syncPolicy`

* `automated` causes Argo CD to automatically apply Git changes.
* `selfHeal: true` instructs Argo CD to detect and revert out-of-band changes made directly in the cluster.
* Use `syncOptions` (for example, `CreateNamespace=true`) to control sync-time behaviors.

## Common use cases and behavior

* Continuous delivery: Argo CD watches the Git repo and automatically synchronizes changes (when `automated` is enabled).
* Drift detection & remediation: With `selfHeal: true`, Argo CD restores cluster state when manual changes diverge from Git.
* Multi-cluster deployments: Use `destination.server` values that target different clusters registered in Argo CD.

## References and further reading

* Argo CD official docs: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* GitOps overview: [https://www.gitops.tech/](https://www.gitops.tech/)
* Helm: [https://helm.sh/](https://helm.sh/)
* Kustomize: [https://kubectl.docs.kubernetes.io/references/kustomize/](https://kubectl.docs.kubernetes.io/references/kustomize/)
* Jsonnet: [https://jsonnet.org](https://jsonnet.org)

For step-by-step tutorials and deeper examples, see the Argo CD documentation and community guides linked above.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/eb4ae0e2-b87a-4e9c-a480-63f94fa8f583)


# ArgoCD Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/ArgoCD-Basics/page

Introduction to ArgoCD and GitOps explaining declarative continuous delivery for Kubernetes, reconciliation, sync strategies, manifest sources, multi cluster management, and observability

In this lesson we use ArgoCD to learn core GitOps terminology and practical features. The goal is to explain the essential ArgoCD concepts and workflows needed to implement GitOps-inspired continuous delivery for Kubernetes—not to exhaustively document every ArgoCD capability.

> **lightbulb** This lesson focuses on the essential ArgoCD features needed to learn GitOps concepts and workflows.

What is ArgoCD?

* ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes.
* It treats one or more Git repositories as the single source of truth for application manifests and continuously ensures the cluster state matches the desired state defined in Git.
* ArgoCD monitors running applications, computes diffs between live and desired states, surfaces deviations, and provides visual and programmatic controls to synchronize the live state manually or automatically.

How ArgoCD fits the GitOps pattern

* Desired state: stored in Git (manifests, charts, overlays, templates).
* Reconciliation: ArgoCD pulls from Git, compares with cluster state, and applies Kubernetes manifests to reach the declared state.
* Observability & Safety: diffs, health checks, RBAC, and audit logs enable safe, auditable deployments.

Key behaviors

* Continuous reconciliation loop: ArgoCD periodically (or on-demand) checks Git and the cluster, reporting drift.
* Two sync modes: manual (operator approves changes) or automated (ArgoCD applies changes automatically).
* Multi-cluster support: manage applications across many Kubernetes clusters from one control plane.
* Extensible input sources: supports multiple templating engines and generators.

<Frame>
  <img alt="The image explains ArgoCD, a declarative GitOps continuous delivery tool for Kubernetes, detailing its purpose, benefits, and functionality including Git-based configuration, automation of synchronization, and its compatibility with various applications like Helm and Ksonnet." />
</Frame>

Supported manifest sources and when to use them

| Source                  |                                                         Use case | Notes / Links                                                                                                  |
| ----------------------- | ---------------------------------------------------------------: | -------------------------------------------------------------------------------------------------------------- |
| `Helm charts`           | Package-based templating for complex apps and chart repositories | Great when reusing or customizing community charts — [https://helm.sh/](https://helm.sh/)                      |
| `Kustomize overlays`    |                     Patch-based customization without templating | Useful for environment overlays and declarative customization — [https://kustomize.io/](https://kustomize.io/) |
| `Plain Kubernetes YAML` |                                       Simple, explicit manifests | Best for small apps or when avoiding template complexity                                                       |
| `Jsonnet`               |                Programmatic manifests for advanced customization | Good for large systems needing reusable logic — [https://jsonnet.org/](https://jsonnet.org/)                   |
| `Other generators`      |                        Custom tooling or plugin-based generators | ArgoCD supports additional supported plugins and generators                                                    |

> **warning** Some older tools (for example, `ksonnet`) are deprecated and no longer actively maintained. Prefer actively supported tools such as `Helm`, `Kustomize`, or `Jsonnet` for templating and generation.

Sync strategies, diffs, and hooks

* Sync strategies:
  * Manual: operator reviews diffs and triggers sync.
  * Automated: ArgoCD applies changes automatically when Git changes are detected (can be gated with health checks).
* Diffs & visualizations: ArgoCD highlights added, changed, and removed resources, making it easy to review intended changes before applying.
* Lifecycle hooks: support pre-sync and post-sync hooks (Jobs, scripts) to orchestrate database migrations, canary steps, or cleanup tasks.
* Health assessment: ArgoCD evaluates resource health and can be configured to stop or roll back on failures.

Benefits of using ArgoCD

* Git as source of truth: versioning, code review, and auditability for deployments.
* Continuous, automated reconciliation: reduces configuration drift and manual errors.
* Centralized multi-cluster management: consistent deployments across environments.
* Visibility & control: built-in UI, CLI, and API for observing and controlling application state.

Quick reference of core components

| Component      | Purpose                                                                 |
| -------------- | ----------------------------------------------------------------------- |
| Application    | Logical mapping of a Git repo (or path) to a target cluster/namespace   |
| App-of-Apps    | Pattern to manage multiple applications via a single parent application |
| Repository     | Git server or Helm repo where manifests are stored                      |
| Controller     | Reconciliation engine that applies manifests to clusters                |
| API / UI / CLI | Methods to interact with ArgoCD (sync, rollback, diff, inspect)         |

Links and References

* ArgoCD project: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Helm: [https://helm.sh/](https://helm.sh/)
* Kustomize: [https://kustomize.io/](https://kustomize.io/)
* Jsonnet: [https://jsonnet.org/](https://jsonnet.org/)
* GitOps concepts: [https://www.weave.works/technologies/gitops/](https://www.weave.works/technologies/gitops/)

Further learning

* Try deploying a simple app with ArgoCD using a Helm chart or plain YAML to see reconciliation and diff behavior.
* Explore RBAC, SSO integration, and metrics/auditing for production-ready setups.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/e31b7279-e0c3-4eb9-8f23-2699ecaa351f)
