# Glasskube

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Tooling/Glasskube/page

Overview of Glasskube, a lightweight Kubernetes package manager using Helm and manifests, covering CLI, UI, GitOps workflows, architecture, controllers, installation, and usage

Glasskube is a lightweight package manager for Kubernetes that leverages Helm charts and plain Kubernetes manifests to provide a unified, developer-friendly package experience. Although the project began in February 2024 with a small core team, it has rapidly gained traction on GitHub thanks to a clear focus on CLI, UI, and GitOps-style workflows.

In this article you will learn:

* The primary ways to interact with Glasskube (CLI, UI, declarative).
* The core architecture and controllers that power package reconciliation.
* How to install and bootstrap Glasskube into a cluster.
* Practical next steps and useful references.

## Primary interaction methods

Glasskube provides three main interfaces for managing packages. Use the table below to quickly compare them.

|            Interface | Purpose                                                                                     | Example / Quick Command                                                |
| -------------------: | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
|                  CLI | Configure, install, update, and manage packages from the terminal.                          | `glasskube install <package>`                                          |
|       UI (Graphical) | Visual package discovery, installation, and status monitoring for users who prefer a GUI.   | Access via the Glasskube dashboard connected to your cluster           |
| Declarative (GitOps) | Define `Package` CustomResources in Git and let reconciliation apply changes automatically. | Commit `ClusterPackage` CRs to your repo and let controllers reconcile |

## Architecture overview

Glasskube follows a client-server model:

* Server-side: controllers running in-cluster (Package Controller, PackageInfo Controller) that reconcile package CRs and manage package lifecycles.
* Client-side: CLI, UI, and configured repositories (public or private) that submit `Package`/`ClusterPackage` resources and query status.

Example package CustomResource:

```yaml theme={null}
apiVersion: packages.glasskube.dev/v1alpha1
kind: ClusterPackage
metadata:
  name: kubernetes-dashboard
spec:
  packageInfo:
    name: kubernetes-dashboard
    version: v2.7.0+2
```

The controllers reconcile these CRs and ensure the desired package state is present in the cluster.

<Frame>
  <img alt="The image is a diagram of the Glasskube architecture, illustrating the interaction between client-side and server-side components, such as the Client, Kubernetes API, and PackageController, within a package management system." />
</Frame>

### Key server-side controllers

* Package Controller: manages package lifecycle operations (install, update, rollback) by reconciling `Package` and `ClusterPackage` CRs.
* PackageInfo Controller: fetches package manifests and metadata from repositories and exposes that information to the cluster via `PackageInfo` CRs.

On the client side, Glasskube reads from a central public Glasskube repository by default; you can also add private or additional public repositories. The UI and CLI interact with both the repository and the in-cluster controllers.

## Package installation flow (single repository)

A typical single-repository install flow:

1. A user selects a package in the CLI or UI.
2. The client validates the selection against the configured repository.
3. The client creates a `Package` or `ClusterPackage` CustomResource in the cluster.
4. The Kubernetes API notifies controllers and triggers reconciliation.
5. If needed, a `PackageInfo` CR is created and reconciled by the PackageInfo Controller.
6. PackageInfo fetches manifest and version details from the repository and updates the CR status.
7. The Package Controller reads the manifest and deploys the package resources through the Kubernetes API.
8. The client (CLI/UI) receives updates as reconciliation progresses.

Reconciliation runs periodically and continuously enforce desired state, enabling automatic remediation and drift detection (reinstall, revert, or repair when package health degrades).

<Frame>
  <img alt="The image is a workflow diagram illustrating the process of package validation, creation, and deployment using a Kubernetes API, involving client-side and server-side interactions. It includes steps like validating a package, reconciling 'Package' and 'PackageInfo', and deploying the package." />
</Frame>

## Multiple repositories and repository UI

Glasskube supports multiple repositories. This enables:

* Central public catalogs,
* Private team catalogs,
* Aggregation of multiple public sources.

Below is an example screenshot of the Glasskube repository UI (Rakkess backend) showing available packages, search, and filtering.

<Frame>
  <img alt="The image shows a webpage from the Glasskube package repository, listing supported software packages with filtering options. It features a search bar, category filters, and a section displaying various package options." />
</Frame>

## Getting started: install the CLI and bootstrap

Install the Glasskube CLI using a platform-appropriate method. Example commands:

```bash theme={null}
