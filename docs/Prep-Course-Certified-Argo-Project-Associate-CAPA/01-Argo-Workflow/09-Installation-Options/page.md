# Installation Options

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Installation-Options/page

Guide comparing Argo Workflows installation options, scopes, and argo CLI setup for minimal versus production deployments and cluster wide or namespace scoped configurations.

This guide compares installation choices for Argo Workflows: minimal vs production installs, cluster-wide vs namespace-scoped deployments, and how to install the `argo` CLI to manage workflows from your terminal. It preserves examples using the v3.7.2 release; always verify the latest release at the Argo Workflows releases page before installing.

## Minimal vs Production install

Minimal and production installs target different use cases. Use the minimal install to get started quickly or for local development; choose the production install for stable, long-running clusters with proper persistence, observability, and security.

| Installation Type  | Intended Use                              | Key characteristics                                                                                                                          | When to choose                              |
| ------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Minimal install    | Local dev, testing, quick demos           | Small manifest that installs core components with minimal overhead                                                                           | Experimentation, PoCs, learning             |
| Production install | Critical workloads, multi-tenant clusters | Full manifests from stable releases, persistent artifact store (S3/MinIO), stricter RBAC, extra components for observability and reliability | Production deployments, multi-team clusters |

Example commands (v3.7.2)

* Minimal (quick-start) install — creates the `argo` namespace and applies the minimal quick-start manifest:

```bash theme={null}
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/v3.7.2/quick-start-minimal.yaml"
```

* Production install — full install manifest from the release (includes production-oriented defaults):

```bash theme={null}
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/v3.7.2/install.yaml"
```

> **lightbulb** Choose the minimal install for fast experimentation. For production, use the full install manifest, configure a persistent artifact repository (S3/MinIO/etc.), and follow the official Argo Workflows documentation for securing RBAC and multi-tenant setups: [https://argoproj.github.io/argo-workflows/security/](https://argoproj.github.io/argo-workflows/security/)

## Scopes: cluster-wide vs namespace-scoped

Decide whether you want a centralized controller that manages all namespaces (cluster-wide) or isolated controllers per namespace (namespace-scoped).

* Cluster-wide installation (default)
  * Single controller with visibility across all namespaces.
  * Simplifies administration and shared control plane for multiple teams.
  * Requires cluster-scoped RBAC.

* Namespace-scoped installation
  * Controller is restricted to a single namespace and limited RBAC.
  * Useful for stricter isolation between environments (dev/test/prod) or for multi-tenant setups where teams manage their own controllers.
  * Implementation details and exact manifests for fully namespaced installs vary between releases.

Quick comparison:

| Scope            | Visibility       | RBAC requirements   | Use cases                                 |
| ---------------- | ---------------- | ------------------- | ----------------------------------------- |
| Cluster-wide     | All namespaces   | Cluster-scoped RBAC | Centralized control plane for many teams  |
| Namespace-scoped | Single namespace | Namespaced RBAC     | Isolated environments, team-level control |

Note: The exact steps to achieve a fully namespaced installation (avoiding cluster-scoped RBAC) can change between releases. Always consult the release notes and official docs for the recommended namespaced manifest or flags for your target release.

> **warning** When attempting a namespace-scoped installation, consult the Argo Workflows release notes ([https://github.com/argoproj/argo-workflows/releases](https://github.com/argoproj/argo-workflows/releases)) and documentation ([https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)) for release-specific instructions to avoid unintentionally granting cluster-scoped privileges.

## Install and use the argo CLI

The `argo` CLI lets you submit, manage, and inspect workflows from your terminal. Below is an example for Linux using the v3.7.2 release. Replace the version string with the release you intend to use, or fetch the latest from the releases page.

Linux example:

```bash theme={null}
