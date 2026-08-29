# download example (update URL/version accordingly)
curl -LO https://github.com/argoproj/argo-rollouts/releases/download/vX.Y.Z/argo-rollouts-linux-amd64

# make executable
chmod +x ./argo-rollouts-linux-amd64

# move to PATH
sudo mv ./argo-rollouts-linux-amd64 /usr/local/bin/argo-rollouts
```

<Callout icon="lightbulb">
  Using the CLI enables quick rollout status checks, traffic-shift visualizations, and troubleshooting commands. Check the official Argo Rollouts documentation for the latest installation instructions and binaries.
</Callout>

## Quick decision guide

* Use cluster-wide installation if:
  * You want centralized control over all rollouts.
  * You have cluster-admin privileges and a small number of operators.
* Use namespace-scoped installation if:
  * You operate a multi-tenant cluster and need to isolate teams.
  * You prefer giving namespace admins control without granting cluster-wide permissions (CRDs still need one-time cluster admin installation).

## Useful links and references

* Official Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Argo Rollouts GitHub releases (binaries & install artifacts): [https://github.com/argoproj/argo-rollouts/releases](https://github.com/argoproj/argo-rollouts/releases)
* [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/d2348f60-f369-4535-8291-d534d09567ef" />
</CardGroup>


# Introduction to Argo Rollouts and Features

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Introduction-to-Argo-Rollouts-and-Features/page

Overview of Argo Rollouts, a Kubernetes controller enabling canary and blue/green progressive deployments with metric-driven analysis, traffic shaping, automated rollbacks, and GitOps integration

Argo Rollouts is a Kubernetes controller for progressive delivery that gives you safer, more controlled application updates. It introduces a Rollout custom resource (CRD) that extends the standard Deployment to support advanced strategies such as Canary and Blue/Green updates, metric-driven analysis, traffic shaping, automated rollbacks, and optional manual approval gates.

Argo Rollouts can gradually expose a new application version to a subset of users, query metric providers (for example, [Prometheus](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)) to validate health, and automatically revert to a previous stable revision if analysis fails. It also integrates tightly with GitOps tools such as [ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd) for declarative, version-controlled delivery.

<Frame>
  <img alt="A flowchart titled &#x22;Argo Rollouts&#x22; that shows a canary deployment process: update to v2, incrementally increase canary weight (e.g., 5%), pause to collect and analyze metrics, then loop back on success or rollback on failure." />
</Frame>

The diagram above shows a typical canary workflow:

* Deploy a new revision (v2) alongside the stable revision.
* Incrementally shift a percentage of traffic to the canary (for example, 5%).
* Pause to collect and analyze metrics and probes.
* If the analysis passes, increase the canary weight or promote to stable; if it fails, automatically rollback to the previous stable revision.

<Callout icon="lightbulb">
  Argo Rollouts introduces the Rollout CRD (kind: Rollout). You continue to use ordinary Kubernetes primitives (Services, Ingress, etc.), but replace Deployments with a Rollout resource when you need progressive delivery features like canary or blue/green strategies and automated analysis.
</Callout>

## Core features — what Argo Rollouts provides

* Progressive delivery: Reduce blast radius by exposing changes gradually to a subset of users.
* Rollout CRD: A first-class Kubernetes resource to manage advanced deployment workflows.
* Canary releases: Route a small portion of traffic to a new revision, observe behavior, then increase exposure.
* Blue/Green deployments: Run two parallel environments and switch traffic when the new environment is validated.
* Analysis (metric providers): Query metrics from systems like Prometheus or Datadog to validate health gates during rollouts.
* Traffic shaping: Control traffic fractions using ingress controllers or service meshes (for example, [Istio](https://learn.kodekloud.com/user/courses/istio-service-mesh)) integrated with Argo Rollouts.
* Automated rollbacks: Automatically revert to a known-good revision if probes or metric analysis fail.
* GitOps integration: Works with [ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd) for declarative, version-controlled rollouts.

### Feature comparisons: when to use each strategy

| Feature                     | Use case                                                                             | Example                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Canary Releases             | Gradually validate a new version with a subset of users to limit impact              | Route 5% -> 25% -> 100% traffic to v2 while analyzing latency and error rates           |
| Blue/Green Deployments      | Quickly switch all traffic to a tested environment and roll back instantly if needed | Deploy v2 to Green environment, run integration tests, switch Service selector to Green |
| Analysis (metric providers) | Gate promotion based on real-time telemetry                                          | Query Prometheus for increased error rate or latency changes during canary windows      |
| Traffic Shaping             | Fine-grained control of traffic distribution                                         | Use Istio VirtualService or ingress rules to direct precise weights to revisions        |
| Automated Rollbacks         | Reduce manual response time to regressions                                           | Revert to previous revision automatically when SLA thresholds are breached              |
| GitOps Integration          | Keep rollouts declarative and auditable                                              | Manage Rollout manifests with ArgoCD for versioned rollouts and easy audits             |

<Frame>
  <img alt="A presentation slide titled &#x22;Argo Rollouts Features&#x22; showing eight numbered items. The features listed are Progressive Delivery, Rollout CRD, Canary Releases, Blue‑Green Deployments, Analysis (metric providers), Traffic Shaping, Automated Rollbacks, and GitOps Integration." />
</Frame>

## How Argo Rollouts fits into your delivery pipeline

* Observability-first deployments: Integrate metric providers (Prometheus, Datadog) and application probes to make promotion decisions data-driven.
* Service mesh / ingress integration: Use Istio, Linkerd, or supported ingress controllers for traffic splitting and weight-based routing.
* CI/CD and GitOps: Keep Rollout manifests in Git and let ArgoCD or your CI pipeline apply them to trigger controlled rollouts.
* Safety and automation: Combine automated analysis and rollbacks with optional manual approval steps (pauses) to balance safety and speed.

## Getting started resources

* Read the Argo Rollouts documentation to understand CRD fields and examples.
* Try a simple canary Rollout with a small traffic weight and a Prometheus-based analysis query.
* Integrate with ArgoCD for GitOps-managed rollouts and audits.

## Links and references

* [Argo Rollouts GitHub / docs](https://argoproj.github.io/argo-rollouts/)
* [Kubernetes documentation: What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Prometheus monitoring fundamentals](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)
* [ArgoCD GitOps course](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Istio service mesh course](https://learn.kodekloud.com/user/courses/istio-service-mesh)

This overview introduced the primary concepts and capabilities of Argo Rollouts. From here, explore example Rollout manifests, integrations with Prometheus and service meshes (for example, Istio), and how to configure automated analyses, pause steps, and manual approvals to make your Kubernetes deployments safer and more controlled.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/1617b29d-aac9-478d-8f04-37364db38df9" />
</CardGroup>
