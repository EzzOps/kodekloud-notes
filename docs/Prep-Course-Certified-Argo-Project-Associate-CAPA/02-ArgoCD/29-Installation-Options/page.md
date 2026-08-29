# Example git revert command
git revert o3u9n
[master s5e79] Revert "Config change"
 1 file changed, 1 deletion(-)
```

* Operator-driven rollback: ArgoCD and similar tools can be configured to revert to a known-good state automatically if health checks fail.

Why rollback matters:

* Speeds recovery after bad deployments.
* Minimizes downtime and risk.
* Gives teams confidence to ship changes more frequently.

## Quick Reference Table

| Concept        | What it means                                   | Example / Tooling                 |
| -------------- | ----------------------------------------------- | --------------------------------- |
| Continuous     | Always-on reconciliation loop                   | ArgoCD, FluxCD                    |
| Declarative    | Describe desired state, not steps               | Kubernetes YAML manifests         |
| Desired State  | Canonical config stored in Git                  | .k8s/manifests/\*                 |
| State Drift    | Actual ≠ Desired (unauthorized changes)         | kubectl scale changed replicas    |
| Reconciliation | Detect and correct drift (observe → diff → act) | GitOps operator                   |
| State Store    | Central repo (single source of truth)           | Git                               |
| Feedback Loop  | Telemetry → alerts → changes in Git             | Prometheus, Grafana, Alertmanager |
| Rollback       | Revert changes quickly via Git or operator      | git revert, ArgoCD auto-rollback  |

## Tools & Further Reading

* ArgoCD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* FluxCD: [https://fluxcd.io/](https://fluxcd.io/)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)
* Git basics: [https://git-scm.com/docs](https://git-scm.com/docs)

<Callout icon="warning">
  While GitOps automates reconciliation, ensure you have proper observability and guardrails (health checks, alerts, RBAC) in place—automation without visibility can amplify issues.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/75fb1813-439b-4d52-8730-b47d7eb59702" />
</CardGroup>


# Installation Options

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Installation-Options/page

Argo CD installation options and guidance covering core and multi-tenant modes, HA vs non-HA manifests, cluster or namespace scopes, Helm and CLI install examples.

Let's review the common Argo CD installation options, when to use each, and example commands to get you started quickly.

Argo CD supports two broad deployment modes:

* Core — a minimal, single-user or single-team installation. Fewer components and simpler configuration, suitable for lightweight use cases and labs.
* Multi-tenant — intended for platform teams managing multiple development teams. Multi-tenant installs come in two operational modes: non-high-availability (non-HA) and high-availability (HA).

<Callout icon="warning">
  The non-HA manifests are intended for testing and proof-of-concept (POC) usage only; they are not recommended for production. For production, use the HA manifests which run multiple replicas for resilience.
</Callout>

Multi-tenant manifest flavors (common in the official repo):

* install.yaml — cluster-scoped installation that assumes cluster-level permissions (cluster-admin). Use this when Argo CD will manage the same cluster it runs in.
* namespace-install.yaml — namespace-scoped installation suitable when Argo CD runs in a single namespace and primarily manages remote clusters.

The HA variants follow the same cluster-scoped or namespace-scoped options, but add multiple replicas and production-grade resources for resilience.

<Callout icon="lightbulb">
  Choose install.yaml (cluster-scoped) if Argo CD will manage the cluster it runs in and you can grant cluster-admin permissions. Choose namespace-install.yaml for a namespace-scoped installation, commonly used when managing remote clusters.
</Callout>

Summary of the options

| Installation Mode     | Scope                       | Use Case                        | Production Ready                 |
| --------------------- | --------------------------- | ------------------------------- | -------------------------------- |
| Core                  | Namespace or single cluster | Single-user / single-team, labs | No (lightweight)                 |
| Multi-tenant (non-HA) | Cluster or Namespace        | POCs, demos, labs               | No — for testing only            |
| Multi-tenant (HA)     | Cluster or Namespace        | Production platforms            | Yes — recommended for production |

Recommended choice for labs and demos

* For hands-on labs and POCs, the non-HA cluster-scoped manifest (install.yaml) or the namespace-scoped manifest (namespace-install.yaml) are the most straightforward options.
* For production deployments, use the HA manifests (cluster- or namespace-scoped), or enable HA through the Helm chart and provision the required permissions and infrastructure (multiple replicas, persistent storage, etc.).

Installation methods
You can install Argo CD either by applying the official upstream manifests or by using the community-maintained Helm chart. The Helm chart defaults to a non-HA configuration unless you override values to enable HA.

Apply upstream non-HA cluster-scoped manifest (quick start):

```bash theme={null}
