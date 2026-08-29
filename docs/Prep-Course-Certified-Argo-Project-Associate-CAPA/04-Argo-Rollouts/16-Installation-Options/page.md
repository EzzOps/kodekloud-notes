# Installation Options

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Installation-Options/page

Explains Argo Rollouts installation options, comparing cluster-wide and namespace-scoped controllers, permission and CRD requirements, and recommended CLI usage.

Let's review the installation options for Argo Rollouts. There are two controller installation modes that differ by scope and required permissions. Choose the one that matches your cluster governance, security posture, and team boundaries.

## Overview

Argo Rollouts supports:

* A default, cluster-wide controller that can manage rollout resources across all namespaces.
* A restricted, namespace-scoped controller that operates only inside its own namespace (blind to other namespaces).

Both options require installing the Rollouts CustomResourceDefinitions (CRDs) once for the cluster. You can combine either controller mode with a CLI installation to manage and visualize rollouts from your workstation.

| Installation Mode           | Scope                              | Required Permissions                                                                                      | Typical Use Case                                                       |
| --------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Cluster-wide controller     | All namespaces (single controller) | Cluster administrator privileges to install controller and CRDs                                           | Centralized deployments, single-operator management for entire cluster |
| Namespace-scoped controller | Single namespace only              | Namespace-level admin to install controller; Cluster admin required only once to install CRDs for cluster | Multi-tenant clusters, team isolation, limited blast radius            |

## 1) Cluster-wide (default) installation

This is the most common method for installing Argo Rollouts.

* Scope: Installs a single controller that can manage rollout resources across every namespace in the cluster.
* Permissions: Requires a cluster administrator to install (controller needs cluster-wide RBAC).
* Use cases: Ideal for centralized management of application deployments, especially when a single operator manages rollouts for all teams.
* Integration note: When used together with GitOps tools such as ArgoCD, the controller typically runs in the same namespace used for rollout management. For example, see the [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd) workflow for related patterns.

<Callout icon="warning">
  Cluster-wide installation requires cluster-admin privileges. Ensure your security policy allows a controller with cluster-scoped permissions before proceeding.
</Callout>

## 2) Namespace-scoped (restricted) installation

This option limits the controller's visibility and control to a single namespace.

* Scope: Controller operates only within the namespace where it is installed; it cannot see or manage resources in other namespaces.
* Permissions:
  * A namespace administrator can install the controller in that namespace.
  * A cluster administrator must install Rollouts CRDs once for the entire cluster (a one-time step).
* Use cases: Best for multi-tenant or strongly isolated clusters where teams run independent controllers and you want to limit cross-namespace impact.

<Callout icon="lightbulb">
  Namespace-scoped controllers help enforce isolation between teams. If you need multi-tenant separation without repeated cluster-admin operations, install the CRDs once and allow team admins to run namespace-scoped controllers.
</Callout>

## One-time CRD installation (required for namespace-scoped)

When using namespace-scoped controllers, CRDs must exist cluster-wide so that the Kubernetes API recognizes Rollout custom resources. This is a single cluster-admin operation and does not grant controller access to all namespaces.

Suggested flow:

1. Cluster admin installs Rollouts CRDs.
2. Namespace admins install the namespace-scoped controller in their namespace.

## CLI (recommended)

A dedicated CLI for Argo Rollouts greatly simplifies rollout management and visualization from the command line. Installing the CLI is optional but highly recommended.

Typical installation steps (replace URLs and version tags with the current release from the official docs or repository):

* Download the binary for your OS.
* Make it executable:
  * chmod +x ./\<binary-name>
* Move it into your PATH:
  * sudo mv ./\<binary-name> /usr/local/bin/\<binary-name>

Example (generic):

```bash theme={null}
