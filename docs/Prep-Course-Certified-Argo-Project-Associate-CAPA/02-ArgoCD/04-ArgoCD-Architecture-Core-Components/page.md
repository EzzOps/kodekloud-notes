# ArgoCD Architecture Core Components

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Architecture-Core-Components/page

Overview of Argo CD core components, their roles inside a Kubernetes cluster, and how they interact to implement GitOps workflows including auth, caching, reconciliation, notifications, and observability.

This document reviews Argo CD's core components, how they run inside a Kubernetes cluster, and how they interact to deliver GitOps workflows. Argo CD components run as pods in the `argocd` namespace and provide the API surface, repository operations, reconciliation logic, authentication, caching, notifications, and observability.

1. ArgoCD API server (argocd-server)

* The argocd-server is the primary API endpoint (gRPC + REST) used by the Web UI, the CLI (`argocd`), and external CI/CD systems.
* Key responsibilities:
  * Exposes application management APIs (create, update, delete).
  * Handles user operations such as sync, rollback, and health checks.
  * Manages credentials, enforces authentication and RBAC, and serves the Argo UI.
  * Exposes Prometheus-compatible metrics and health endpoints for scraping.

2. Authentication and RBAC (Dex and external IdPs)

* Argo CD can delegate authentication to external identity providers (Okta, GitHub, Google, etc.) using OpenID Connect (OIDC). Many deployments use Dex as an OIDC broker, although Argo CD also supports direct OIDC integration.
* RBAC within Argo CD is enforced based on configured policies and the identities asserted by the identity provider.

> **lightbulb** Dex ([https://dexidp.io](https://dexidp.io)) commonly acts as an OIDC broker between Argo CD and external identity providers. Configure your IdP in Argo CD (or via Dex) so Argo CD can consume issued tokens for authentication and RBAC decisions.

3. Caching and persistence (Redis + Kubernetes API / etcd)

* Redis is used as an in-memory cache for transient data: repository indexes, session storage, and short-lived caches to speed up operations.
* All persistent configuration—application definitions, repo credentials, and plugin settings—are stored as Kubernetes objects (Secrets, ConfigMaps, CRs) persisted in etcd via the Kubernetes control plane. Redis failures do not cause permanent data loss because Argo CD can rebuild caches from Git and Kubernetes resources.

4. Retrieve phase (argocd-repo-server)

* The repo-server performs the "retrieve" stage:
  * Clones Git repositories, resolves templates, and renders final Kubernetes manifests.
  * Supports Helm, Kustomize, Jsonnet, plain YAML, and Config Management Plugins (CMP).
  * Caches generated manifests for consumption by the controller and UI.

5. Reconcile phase (argocd-application-controller)

* The application-controller is a Kubernetes controller that implements reconciliation:
  * Compares desired state (manifests from the repo-server) with the live cluster state.
  * Detects drift and applies changes according to configured sync policies (manual, automatic, hooks, pruning).
  * Manages sync waves, resource ordering, and finalizers when needed.

6. Notifications (argocd-notifications)

* The notifications controller watches application and cluster events, then dispatches alerts via configured channels:
  * Slack, email, webhooks, Teams, or custom providers.
  * Uses templates and triggers to customize when and how notifications are sent.

7. Metrics and observability

* Argo CD components expose Prometheus-compatible metrics on HTTP endpoints for monitoring:
  * argocd-server: API traffic, auth events.
  * repo-server: repo clone times, template rendering stats.
  * application-controller: reconciliation loop durations, sync counts.
  * notifications: delivery attempts and success/failure counts.
* Use Prometheus ServiceMonitors to scrape these endpoints and visualize them with Grafana dashboards for cluster and application visibility.

<Frame>
  <img alt="A labeled architecture diagram of ArgoCD core components showing argocd-server, repo-server, dex, application-controller, redis, and notification controller. It illustrates user/CI access, authentication providers, metrics, notifications, and deployments to multiple Kubernetes clusters (dev, staging, prod)." />
</Frame>

Summary table: core components and responsibilities

|                        Component | Purpose                                    | Notable endpoints / notes                      |
| -------------------------------: | ------------------------------------------ | ---------------------------------------------- |
|                    argocd-server | API surface, Web UI, authentication & RBAC | REST/gRPC API, UI, metrics endpoint            |
|               argocd-repo-server | Retrieves and renders manifests            | Git clone, Helm/Kustomize/Jsonnet, CMP support |
|    argocd-application-controller | Reconciliation and drift correction        | Watches Application CRs, applies syncs/prunes  |
|                            Redis | In-memory cache and transient storage      | Not persistent for long-term config            |
|                   Dex / OIDC IdP | Authentication broker / provider           | OIDC tokens for Argo CD users                  |
|             argocd-notifications | Event-driven notifications                 | Slack, email, webhooks; templated triggers     |
| Prometheus / Grafana integration | Observability and dashboards               | Scrape metrics + visualize in Grafana          |

Links and references

* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Dex (OIDC broker): [https://dexidp.io](https://dexidp.io)
* Redis: [https://redis.io](https://redis.io)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana: [https://grafana.com](https://grafana.com)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

> **lightbulb** Best practices:

  * Keep Argo CD configuration (Applications, Repo credentials) as Kubernetes objects committed and backed up.
  * Treat Redis as ephemeral: ensure persistent state is in Kubernetes resources and Git.
  * Scrape Argo CD metrics with Prometheus ServiceMonitors and add Grafana dashboards for visibility.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/001dfb64-f1a3-4c0a-bcef-eff54821cebb)
