# Refresh application state (re-fetch Git and re-evaluate)
argocd app refresh guestbook

# Trigger a manual sync (apply Git changes to the cluster)
argocd app sync guestbook
```

Advanced CLI options include `--prune`, `--self-heal`, and `--revision` to control the sync behavior.

## Best Practices and Day-to-Day Concepts

* Keep the Git repository as the single source of truth for application configuration.
* Use Projects to enforce security and deployment boundaries.
* Pin `targetRevision` to a branch, tag, or commit for reproducible deployments.
* Prefer automated sync for stateless infra and manual sync for critical production systems unless you implement appropriate safeguards.
* Monitor Sync, Operation, and Health statuses in the UI or via alerts to detect drift and failures early.

## Summary

* An ArgoCD Application maps Git to cluster deployment and describes packaging and destination.
* Projects organize Applications and enforce policies and access boundaries.
* Target state is defined in Git; live state is what runs in Kubernetes.
* ArgoCD continuously reconciles live and target states and reports Sync, Operation, and Health statuses.
* Use refresh to re-evaluate an Application and sync to apply changes (manual or automated via `syncPolicy`).

This lesson covered the core ArgoCD concepts you'll use daily when implementing GitOps with ArgoCD.

## Links and References

* ArgoCD Documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* GitOps with ArgoCD: [https://argo-cd.readthedocs.io/en/stable/getting\_started/](https://argo-cd.readthedocs.io/en/stable/getting_started/)
* Kustomize: [https://kustomize.io/](https://kustomize.io/)
* Helm: [https://helm.sh/](https://helm.sh/)
* Git: [https://git-scm.com/](https://git-scm.com/)

For additional courses and guided tutorials, see the referenced learning paths at Learn KodeKloud.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/37b87ace-4404-4c7a-a919-6eace075053b" />
</CardGroup>


# ArgoCD Features

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Features/page

Overview of ArgoCD features for GitOps continuous delivery on Kubernetes, including continuous reconciliation, multi‑cluster deployments, config format support, SSO/RBAC, observability, hooks, webhooks and rollback

In this lesson we’ll explore ArgoCD and the core features that make it a powerful GitOps continuous delivery tool for Kubernetes. ArgoCD continuously reconciles the live cluster state with declarative configuration stored in Git, treating Git as the single source of truth. It supports multi-cluster deployments, multiple configuration formats, enterprise authentication and authorization, and extensive observability and automation capabilities.

Key platform capabilities include automated deployments, multi-cluster support, templating/tooling compatibility, enterprise SSO and directory integrations, secure multi-tenancy, and safe rollback via Git history.

## What ArgoCD provides

|                       Feature | What it does                                                                                 | Typical benefit / example                                        |
| ----------------------------: | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
|     Continuous reconciliation | Keeps live cluster state synchronized with Git declarative configs                           | Prevents configuration drift and enforces compliance             |
|     Multi-cluster deployments | Manages apps deployed across one or many clusters                                            | Centralized delivery for hybrid / multi-environment setups       |
|         Config format support | Works with Kustomize, Helm, Jsonnet, plain YAML (Ksonnet deprecated)                         | Integrates with your existing templating or packaging workflow   |
| SSO and directory integration | OIDC, OAuth2, SAML and directory providers (LDAP); integrations with GitHub/GitLab/Microsoft | Enforces corporate authentication and simplifies user management |
|          RBAC & multi-tenancy | Kubernetes RBAC plus ArgoCD role mappings and policies                                       | Enforces least privilege across teams and tenants                |
|      Rollback / roll-anywhere | Sync to any Git commit to restore previous state                                             | Fast recovery from failed upgrades or misconfigurations          |

<Frame>
  <img alt="A presentation slide titled &#x22;ArgoCD Features&#x22; listing five numbered features: automated deployments to multiple clusters; support for config/templating tools (Kustomize, Helm, Ksonnet, Jsonnet, plain YAML); SSO integrations (OIDC, OAuth2, LDAP, SAML, GitHub/GitLab/Microsoft/LinkedIn); multi‑tenancy and RBAC; and rollback/roll‑anywhere to Git commits. The footer shows © Copyright KodeKloud." />
</Frame>

## Health assessment, drift detection, observability, and hooks

ArgoCD provides continuous application health assessment, detects configuration drift, and exposes operational telemetry for monitoring and auditing.

* Health analysis: ArgoCD continuously checks the health of Kubernetes resources (Ready, Progressing, Degraded, etc.) and surfaces statuses through the UI and API so you can quickly spot problems.
* Drift detection: It compares live manifests against the Git source and visualizes differences to help you investigate and remediate drift.
* Observability: Exposes Prometheus-formatted metrics (typically at /metrics) for integration with monitoring stacks and dashboards.
* Auditing: Records application events and API calls to create an audit trail for security and compliance reviews.
* Sync hooks: PreSync, Sync, PostSync and lifecycle hooks enable running custom jobs or scripts at defined stages of deployment to manage complex rollout steps and handle migrations or validations.

<Frame>
  <img alt="A presentation slide titled &#x22;ArgoCD Features&#x22; showing a numbered list (06–10) of capabilities such as health status analysis, automated configuration drift detection and visualization, out-of-the-box Prometheus metrics, audit trails, and PreSync/Sync/PostSync hooks. The slide uses teal gradient bars and circular number badges on the left." />
</Frame>

## Operational integration and user experience

ArgoCD integrates with developer workflows, CI systems, and Git provider events to deliver a smooth operational experience.

* Webhooks: Connect to Git providers (GitHub, GitLab, Bitbucket) to trigger repository refreshes and — if auto-sync is enabled — start automatic syncs on new commits.
* Automation & CI integration: The argocd CLI and token-based authentication facilitate scripting and integration with CI/CD pipelines.
* Web UI: A real-time graphical interface shows applications, health, sync status, diffs, and deployment history for rapid troubleshooting and auditing.
* Sync strategies: Supports automatic sync (continuous delivery) or manual sync (controlled, human-driven deployments) to match your release and approval workflows.

<Frame>
  <img alt="A slide titled &#x22;ArgoCD Features&#x22; listing items 11–14: webhook integration (GitHub, BitBucket, GitLab); CLI and access tokens for automation/CI; a real-time Web UI; and automated or manual syncing to desired state. The slide uses turquoise numbered markers and a KodeKloud copyright." />
</Frame>

<Callout icon="lightbulb">
  ArgoCD is designed around Git as the single source of truth. Adopt Git workflows and branching strategies to manage application lifecycle (promotion, rollbacks, and approvals). Combine RBAC and SSO to enforce secure, multi-tenant operations and integrate ArgoCD metrics into Prometheus for centralized observability.
</Callout>

## Links and references

* [GitOps with ArgoCD course](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Kustomize course](https://learn.kodekloud.com/user/courses/kustomize)
* [Helm for Beginners](https://learn.kodekloud.com/user/courses/helm-for-beginners)
* [Prometheus Certified Associate](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca-certification)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/04bcf4d6-daad-42fd-ba23-ce4c3e8672e2" />
</CardGroup>
