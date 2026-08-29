# ArgoCD Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Architecture/page

Overview of ArgoCD architecture explaining components, workflows, and integrations that implement GitOps to continuously reconcile Git declared desired state with Kubernetes clusters.

Let's examine the ArgoCD architecture at a high level and explain how its components, flows, and integrations work together to implement GitOps for Kubernetes.

ArgoCD runs inside a Kubernetes cluster as a set of controllers and services. Users interact with ArgoCD via the web UI or the CLI to create Application resources, manage Projects, configure single sign-on (SSO), and define sync behavior (manual, automatic, pruning, self-heal, etc.). The desired state lives in Git, and ArgoCD continuously monitors Git repositories to reconcile cluster state with that desired state.

Key concepts and flows

* Desired state in Git
  * Manifests (YAML), Helm charts, Kustomize overlays, Jsonnet, or Helmfile live in your Git repositories. These repositories act as the single source of truth.
* Continuous reconciliation
  * ArgoCD continuously compares the desired state in Git with the actual state in the target clusters. When drift is detected, the reconciliation loop can apply changes according to the sync policy (manual or automatic).
* Webhooks for faster sync
  * You can configure webhooks on your Git provider to notify ArgoCD of push/merge events. Webhooks prompt immediate refresh and reconciliation rather than waiting for the next polling interval.
* API server (gRPC + REST)
  * ArgoCD exposes gRPC endpoints and a REST interface (via gRPC-gateway). These are used by the UI, CLI (argocd), and automation tools.
* Component responsibilities
  * repo-server: clones repositories and renders manifests (Helm/Kustomize).
  * application-controller: performs the continuous reconciliation between Git and clusters.
  * argocd-server: serves the UI, CLI API, and authentication endpoints.
  * Redis (optional): used for caching and work queues.
  * SSO connectors (optional): Dex or external OIDC providers for authentication.
* Multi-cluster control plane
  * A single ArgoCD control plane can manage deployments across multiple target clusters. Cluster credentials are stored in the control plane and used to apply manifests to registered clusters.
* Observability & notifications
  * ArgoCD exports Prometheus metrics for monitoring (visualized in Grafana).
  * ArgoCD Notifications supports triggers, templates, and integrations (Slack, Teams, email, GitHub, etc.) to alert teams about syncs, health changes, and failures.

<Frame>
  <img alt="A diagram of ArgoCD architecture showing the ArgoCD server (octopus) pulling from GitHub and receiving webhook events, being managed via UI/CLI and CI, and syncing/deploying manifests to multiple Kubernetes clusters (prod, dev, staging). It also shows notifications/metrics flowing to tools like Teams/Gmail/Slack/Grafana/Prometheus." />
</Frame>

How the reconciliation loop works

1. ArgoCD reads Application manifests that reference Git repositories and target clusters.
2. The repo-server clones the repository and renders manifests for the specified revision (branch, tag, commit).
3. The application-controller compares the rendered desired state with the live cluster resources.
4. If divergence (drift) is detected, the controller either:
   * Enqueues a sync operation (automatic sync policy), or
   * Marks the Application as OutOfSync for an operator to manually sync (manual policy).
5. During sync, ArgoCD applies the manifests to the target cluster and can perform pruning (remove resources no longer in Git) and self-heal (auto-correct drift).

Common sync commands

```bash theme={null}
