# Create an Application (example)
argocd app create my-app \
  --repo https://github.com/example/repo.git \
  --path k8s/overlays/prod \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace my-namespace

# Trigger a manual sync
argocd app sync my-app

# Add a target cluster to ArgoCD control plane
argocd cluster add my-kube-context
```

Webhooks and refresh behavior

* Polling vs. webhook: ArgoCD can poll Git repositories on a periodic interval, but configuring webhooks on your Git provider (GitHub, GitLab, Bitbucket) reduces latency by informing ArgoCD immediately when changes occur.
* Webhook flow:
  1. Developer pushes/merges to Git.
  2. Git provider sends webhook to ArgoCD.
  3. ArgoCD refreshes its cache and triggers reconciliation for affected Applications.

Security considerations

> **warning** Store cluster credentials and Git access tokens securely. Avoid committing tokens or kubeconfig files into repositories. Use Kubernetes secrets, sealed-secrets, or external secret managers (Vault, AWS Secrets Manager, etc.) to protect sensitive credentials.

ArgoCD components and responsibilities (concise)

| Component              | Primary responsibility       | Notes                                     |
| ---------------------- | ---------------------------- | ----------------------------------------- |
| argocd-server          | Serves UI and API endpoints  | gRPC + REST (gRPC-gateway)                |
| repo-server            | Clones and renders manifests | Runs Helm/Kustomize rendering             |
| application-controller | Continuous reconciliation    | Detects drift and triggers syncs          |
| Redis (optional)       | Caching and work queues      | Improves performance at scale             |
| SSO connectors         | Authentication (Dex/OIDC)    | Integrates external identity providers    |
| Notifications          | Alerts on events             | Integrates with Slack, Teams, email, etc. |

Typical actors and integrations

| Actor / Integration          | Role                                                      |
| ---------------------------- | --------------------------------------------------------- |
| Users (UI / CLI)             | Create and manage Applications and Projects               |
| Git repositories             | Source of truth containing desired manifests              |
| Webhooks                     | Notify ArgoCD of Git events for immediate refresh         |
| ArgoCD API                   | Consumed by UI, CLI, and automation pipelines             |
| App controller & repo-server | Core controllers doing reconciliation and rendering       |
| Target clusters              | Actual Kubernetes clusters where ArgoCD applies resources |
| Observability systems        | Prometheus/Grafana for metrics and dashboards             |
| Notification channels        | Slack, Teams, email, GitHub notifications                 |

Best practices and tips

> **lightbulb** * Model each deployable component as an ArgoCD Application and group related Applications into Projects for access control and separation.
  * Use Git branching strategies (feature, release, main) and tie ArgoCD Applications to specific branches or tags for predictable deployments.
  * Enable webhooks for faster continuous delivery; rely on Prometheus metrics and Grafana dashboards for operational visibility.

Links and references

* Official ArgoCD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* GitOps principles: [https://www.gitops.tech/](https://www.gitops.tech/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Dex (SSO connector): [https://github.com/dexidp/dex](https://github.com/dexidp/dex)

This architecture enables a Git-centric, observable, and auditable continuous delivery control plane capable of managing multiple Kubernetes clusters from a single ArgoCD deployment.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/e28776ce-7d66-412b-9634-97607f8c6053)


# ArgoCD Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Basics/page

Introduction to ArgoCD GitOps continuous delivery for Kubernetes, explaining reconciliation, sync policies, supported tools, and enterprise features.

Let's briefly introduce ArgoCD and its core concepts for Kubernetes GitOps workflows.

## What is ArgoCD?

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It treats Git repositories as the single source of truth for application manifests and continuously ensures the cluster's live state matches the desired state stored in those repositories.

ArgoCD continuously:

* Monitors running applications
* Compares the cluster's live state with the desired state defined in Git
* Reports drift and differences
* Exposes visualizations and workflows for manual or automated synchronization

## Why use ArgoCD?

* Declarative Git-based management: Store cluster and application manifests in Git; ArgoCD reads and enforces them.
* Continuous operations: Detects drift, provides analytics, and enables remediation via manual or automated syncs.
* Enterprise readiness: Built-in audit trails, RBAC, SSO integration, and compliance features for production environments.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Use ArgoCD?&#x22; showing a cartoon octopus mascot and three key points: declarative Git-based management, continuous operations with monitoring/remediation, and enterprise-ready features like security, RBAC, and SSO." />
</Frame>

## How ArgoCD works

ArgoCD operates with a clear GitOps reconciliation loop and supports multiple manifest formats and tools.

* Source of truth\
  Git repositories contain application manifests (YAML/JSON, Helm charts, Kustomize overlays, Jsonnet, etc.). ArgoCD treats these repositories as the authoritative desired state.

* Continuous reconciliation\
  ArgoCD continuously compares the desired state stored in Git against the cluster's live state and highlights any differences (drift).

* Synchronization\
  When drift is detected—or on demand—ArgoCD applies manifests to bring the live state back to the desired state. Sync strategies can be manual, automated, or follow custom policies (hooks, sync waves, retry/backoff).

* Tooling support\
  ArgoCD natively supports multiple templating and configuration tools:

| Tool / Format   | Use Case                                          | Reference                                                           |
| --------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| Kustomize       | Manage overlays and environment-specific patches  | [Kustomize](https://learn.kodekloud.com/user/courses/kustomize)     |
| Helm charts     | Template-driven package management for Kubernetes | [Helm](https://learn.kodekloud.com/user/courses/helm-for-beginners) |
| Jsonnet         | Programmatic, data-driven manifests               | [Jsonnet](https://jsonnet.org/)                                     |
| Plain YAML/JSON | Static manifests for simple workloads             | Kubernetes manifests                                                |

## Key ArgoCD concepts

| Concept             | Description                                                                                                     |
| ------------------- | --------------------------------------------------------------------------------------------------------------- |
| Application         | A mapping between a Git repo (or path) and a target cluster/namespace; ArgoCD monitors and syncs this resource. |
| Repository          | Git repository that stores manifests and acts as the single source of truth.                                    |
| Sync Policy         | Controls how and when ArgoCD applies changes (manual, automated, hooks, and custom policies).                   |
| Reconciliation Loop | The continuous process that compares Git vs cluster and applies changes to remove drift.                        |

> **lightbulb** ArgoCD runs inside your Kubernetes cluster (typically as pods in a dedicated namespace) and needs appropriate RBAC and ServiceAccount permissions to apply manifests. A single ArgoCD instance can manage multiple target clusters using Kubernetes secrets or the ArgoCD cluster registration mechanism.

## Next steps and where to learn more

To deepen your understanding, explore topics such as ArgoCD architecture, installation options (Helm or manifests), defining Applications (AppProject, Application CR), sync hooks, and more advanced policies for production-grade deployments.

Links and resources:

* [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm](https://helm.sh/)
* [Kustomize](https://kustomize.io/)
* [Jsonnet](https://jsonnet.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/1838906f-aa30-45b1-9134-13c8b6de185d)
