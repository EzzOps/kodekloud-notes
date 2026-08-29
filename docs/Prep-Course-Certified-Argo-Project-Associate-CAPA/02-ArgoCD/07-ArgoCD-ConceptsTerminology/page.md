# ArgoCD ConceptsTerminology

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-ConceptsTerminology/page

Overview of ArgoCD concepts, explaining Applications, Projects, sync and health statuses, GitOps reconciliation, supported source types, and best practices for deploying Kubernetes from Git

In this lesson we cover the essential ArgoCD concepts and terminology you need to operate ArgoCD effectively in a GitOps workflow. Familiarity with Git, Docker, Kubernetes manifests, and the basics of declarative infrastructure is assumed.

> **lightbulb** Prerequisites: familiarity with [Git for Beginners](https://learn.kodekloud.com/user/courses/git-for-beginners), [Kubernetes for the Absolute Beginners - Hands-on Tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial) (manifests, namespaces), and the idea of declarative infrastructure will help you follow this lesson.

## What is an ArgoCD Application (Kubernetes Custom Resource)

An ArgoCD Application is a Kubernetes custom resource (CR) that declares how ArgoCD should deploy and manage an application. It maps the Git (or other supported) source of truth to a target Kubernetes cluster and namespace, and specifies the toolchain used to render or package manifests.

Key responsibilities of an Application:

* Identify the source of truth (Git repo, Helm chart repo, etc.).
* Specify the packaging or templating tool (Helm, Kustomize, plain manifests, Jsonnet, etc.).
* Define the target cluster and namespace for deployment.
* Associate the Application with an ArgoCD Project for policy and access control.

A minimal example Application manifest:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
spec:
  project: default
  source:
    repoURL: https://github.com/example-org/guestbook
    path: overlays/prod
    targetRevision: main
    kustomize:
      namePrefix: guestbook-
  destination:
    server: https://kubernetes.default.svc   # in-cluster
    namespace: guestbook-prod
  syncPolicy:
    automated: {}    # optional: enable auto-sync (auto apply)
```

Notes about important fields:

* `source.repoURL` & `source.path` identify the configuration (the application’s source of truth).
* `source.targetRevision` pins the Git revision (branch, tag, or commit).
* `destination.server` and `destination.namespace` specify where resources are applied.
* `project` groups Applications and enforces boundaries (RBAC, allowed clusters/namespaces, repo rules).
* `syncPolicy` defines whether ArgoCD auto-applies changes or requires a manual sync.

## Supported Source Types

ArgoCD supports multiple source and packaging types. Choose the appropriate source type and set any tool-specific options when creating an Application.

| Source Type                | Use Case                                             | Example / Note                       |
| -------------------------- | ---------------------------------------------------- | ------------------------------------ |
| Plain Kubernetes manifests | Simple YAML/Kubernetes objects stored in a repo      | Directory of manifests or overlays   |
| Kustomize                  | Overlaying and patching manifests without templating | `kustomize` build options            |
| Helm charts                | Packaging with templating and values overrides       | Helm values files and `valueFiles`   |
| Jsonnet                    | Advanced declarative configuration language          | Jsonnet libraries and imports        |
| Config Management Plugins  | Custom build tools or processors                     | Use for bespoke or unsupported tools |

When configuring an Application, use the `source` block to indicate the repository, path, and tool-specific configuration (e.g., Helm `values`, Kustomize options).

## ArgoCD Projects

ArgoCD Projects are logical groups for Applications that help with multi-team organization and security. Projects let you:

* Restrict which clusters and namespaces Applications can deploy to.
* Control which Git repositories and revision patterns are allowed.
* Apply RBAC, admission, and resource quotas across Applications.

Use Projects to enforce policies and isolate teams or environments (dev, staging, prod).

## Target State vs Live State

* Target state: the desired/application configuration declared in Git (Application `source`).
* Live state: the actual state of Kubernetes resources running in the cluster.

ArgoCD continuously compares the live state to the target state and attempts to make them match (reconciliation).

## Synchronization (Reconciliation)

Synchronization (or reconciliation in GitOps terms) is the process of applying the target state to the cluster so the live state becomes identical to Git. Sync modes:

* Manual sync: triggered by an operator (UI, CLI, or API).
* Automated sync: ArgoCD automatically applies detected changes when `syncPolicy.automated` is configured.

Automation options include automatic pruning, self-heal, and specific sync hooks for more advanced flows.

## Statuses: Sync, Operation, and Health

ArgoCD reports multiple status dimensions for each Application — understanding these is critical for operations and troubleshooting.

| Status Type      | Common Values                                        | Meaning                                                     |
| ---------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| Sync status      | Synced / OutOfSync                                   | Whether the live state matches the target state             |
| Operation status | Succeeded / Failed / Running / Terminated / Error    | Result of the last sync or in-progress operation            |
| Health status    | Healthy / Progressing / Degraded / Missing / Unknown | Aggregated resource-level health computed via health checks |

* Sync status tells you if resources in the cluster match Git.
* Operation status reflects the most recent operation (for example, the result of a sync).
* Health status is derived from built-in or custom health checks per resource type and then aggregated for the Application.

> **lightbulb** You can extend or customize health checks for special resource types using custom health checks or resource health overrides.

## Refresh and Manual Sync (CLI examples)

* Refresh: re-evaluates the Application by fetching the latest revision from Git and comparing it to the cluster. It does not change cluster resources unless a sync follows.
* Manual Sync: applies the target state to the cluster. You can trigger this from the UI, the API, or the `argocd` CLI.

Common CLI examples (ensure your `argocd` CLI is authenticated to the ArgoCD server):

```bash theme={null}
