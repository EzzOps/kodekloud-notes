# Section Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Extending-Package-Management-with-GitOps/Section-Introduction/page

Creating a minimal Glasskube and Argo CD GitOps template to bootstrap and manage Kubernetes clusters with secure secret handling and reproducible, auditable workflows.

And just like that, we've arrived at the final section.

In this lesson we'll combine everything we've learned into a minimal, production-ready GitOps template that ties together Glasskube, Argo CD, and the package manifests required to bootstrap a Kubernetes cluster. We'll start with a concise GitOps refresher to ground the workflow and explain why we choose this approach for cluster bootstrapping and ongoing operations.

This section focuses on:

* A short GitOps refresher and the benefits it provides teams
* The end-to-end workflow that the Glasskube + Argo CD template will implement
* A minimal repository layout and example manifests to get a cluster ready in seconds
* Practical considerations for safely managing configuration and secrets during bootstrap

> **lightbulb** GitOps enables declarative, Git-centered operations for Kubernetes. By storing cluster state in Git and using Argo CD to continuously reconcile the cluster, you get auditable changes, safer rollbacks, and repeatable cluster bootstraps.

## Why GitOps for cluster bootstrap

GitOps is particularly well suited for cluster bootstrap and platform configuration because it makes the desired state explicit, versioned, and reviewable. Key benefits include:

* Improved collaboration via Git-based code review and approvals
* Safer, auditable configuration changes and clear rollback paths
* Reliable, automated deployments with continuous reconciliation
* Faster onboarding and reproducible environments

| Benefit       | What it means for teams                                              |
| ------------- | -------------------------------------------------------------------- |
| Collaboration | Everyone submits changes via Git (PRs, reviews)                      |
| Auditability  | Every change is tracked and attributable                             |
| Reliability   | Argo CD continuously ensures the cluster matches Git                 |
| Speed         | Templates and automation reduce bootstrap time from hours to minutes |

## What you'll build

By the end of this lesson you will have a working Kubernetes cluster configured using a minimal Glasskube GitOps template. The template is intentionally minimal so you can:

* Quickly provision a cluster with common platform packages
* See how Argo CD reconciles the repository to the cluster
* Extend the template for your environment and policies

## GitOps workflow (high level)

1. Define the desired cluster state in a Git repository (infrastructure, packages, configs).
2. Argo CD watches the Git repo and reconciles the cluster to match the declared state.
3. Changes are made via Git (pull requests), reviewed, and merged — Argo CD applies them automatically.
4. Continuous monitoring ensures drift is corrected and the repo remains the single source of truth.

## Example repository layout

Below is a minimal repo layout you can use as a starting point for a Glasskube + Argo CD GitOps template:

```text theme={null}
gitops-repo/
├── clusters/
│   └── production/
│       ├── kustomization.yaml     # cluster-level overlays
│       └── glasskube-packages/    # Glasskube package declarations
├── apps/
│   └── argocd/
│       └── application.yaml       # Argo CD Application to sync cluster repo
└── README.md
```

## Minimal Argo CD Application example

This example shows an Argo CD Application that targets the `clusters/production` path in the repository. Customize `destination.server` and `destination.namespace` for your cluster.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cluster-bootstrap
spec:
  project: default
  source:
    repoURL: 'https://github.com/your-org/gitops-repo.git'
    targetRevision: HEAD
    path: clusters/production
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

> **warning** Avoid committing plaintext secrets to Git. Use sealed-secrets, external secret stores (e.g., AWS Secrets Manager, HashiCorp Vault), or GitOps-compatible secret management to keep sensitive data safe.

## Practical tips for a minimal Glasskube template

* Start with a small set of packages that are essential for cluster operation (RBAC, ingress, monitoring).
* Keep overlays simple and use Kustomize or Helm charts as needed.
* Configure Argo CD with `prune` and `selfHeal` to ensure the cluster converges to Git state.
* Use branch protection and PR reviews to enforce change control.

## Links and references

* [Glasskube — KodeKloud course](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube)
* [Argo CD — GitOps for Kubernetes](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Sealed Secrets (Bitnami)](https://github.com/bitnami-labs/sealed-secrets)

Throughout the lesson you'll practice these concepts and configurations. By following this template you'll be able to provision and maintain a cluster that is auditable, reproducible, and ready for rapid iteration.

- [Watch Video](https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/0ddd5879-550c-4c12-82cd-ac19fb487de5/lesson/b80c5b04-728f-44e3-94ba-27513e89804e)
