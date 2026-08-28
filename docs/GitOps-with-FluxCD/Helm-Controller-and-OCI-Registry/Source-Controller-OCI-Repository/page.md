# Git-based Helm charts
flux create source git my-helm-charts \
  --url https://github.com/sidd-harth/charts \
  --branch main

# Bitnami Helm repository with TLS certs
flux create source helm bitnami \
  --url https://charts.bitnami.com/bitnami \
  --cert-file=./cert.crt \
  --key-file=./key.crt \
  --ca-file=./ca.crt
```

<Callout icon="lightbulb">
  Ensure your credentials (`--cert-file`, `--key-file`, `--ca-file`) are stored securely and referenced via [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
</Callout>

After a reconciliation cycle, inspect the contents of the Source Controller’s data directory:

```bash theme={null}
kubectl -n flux-system exec -it source-controller -- sh
~ # tree data/
data/
├── gitrepository
│   └── flux-system
│       └── my-helm-charts
│           ├── 1b31558bb1a701c7592652bbc9e3.tar.gz
│           └── latest.tar.gz
├── helmrepository
│   └── flux-system
│       └── bitnami
│           ├── index-e6dc924894f5f871db9b968.yaml
│           └── index.yaml
```

## Defining a HelmRelease

A `HelmRelease` is a Flux custom resource that declares the desired state of a Helm chart deployment. The Helm Controller watches these resources and orchestrates Helm operations accordingly.

Create a `HelmRelease` resource:

```bash theme={null}
flux create helmrelease chart-z-release \
  --source HelmRepository/bitnami \
  --chart chart-z \
  --chart-version 1.2.3 \
  --values values.yaml
```

This command generates a `HelmChart` object, which the Source Controller will reconcile and produce as an artifact:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmChart
metadata:
  name: flux-system-chart-z-release
spec:
  interval: 1m0s
  chart: chart-z
  reconcileStrategy: ChartVersion
  sourceRef:
    kind: HelmRepository
    name: bitnami
    version: "1.2.3"
status:
  artifact:
    path: helmchart/flux-system/flux-system-chart-z-release/chart-z-release-1.2.3.tgz
    revision: 1.2.3
    url: http://source-controller-flux-system.svc.cluster.local/.helmchart/flux-system/flux-system-chart-z-release/chart-z-release-1.2.3.tgz
```

Verify the published chart artifact:

```bash theme={null}
kubectl -n flux-system exec -it source-controller -- sh
~ # tree data/
data/
├── gitrepository
│   └── flux-system
│       └── my-helm-charts
│           ├── 1b31558bb1a701c7592652bbc9e3.tar.gz
│           └── latest.tar.gz
├── helmrepository
│   └── flux-system
│       └── bitnami
│           ├── index-e6dc924894f5f871db9b968.yaml
│           └── index.yaml
└── helmchart
    └── flux-system-chart-z-release
        ├── chart-z-release-1.2.3.tgz
        └── latest.tar.gz
```

## Helm Controller Responsibilities

The Flux Helm Controller automates the lifecycle of Helm releases:

* Watches `HelmRelease` CRs and reconciles them into `HelmChart` artifacts.
* Retrieves packaged charts from the Source Controller.
* Executes Helm commands: install, upgrade, test, rollback, and uninstall.
* Supports automatic rollbacks on failed deployments.
* Cleans up resources when a `HelmRelease` is deleted.

<Callout icon="triangle-alert">
  Deleting a `HelmRelease` object will trigger the uninstallation of the associated release. Backup any persistent data before removal.
</Callout>

***

## Links and References

* [Flux Helm Controller Documentation](https://fluxcd.io/docs/components/helm/helm-controller/)
* [Source Controller Documentation](https://fluxcd.io/docs/components/source/)
* [GitOps with Flux](https://fluxcd.io/docs/)
* [Helm Charts Guide](https://helm.sh/docs/topics/charts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/e700bfa3-d070-452d-a9c4-7fad1dfcff87" />
</CardGroup>


# Source Controller OCI Repository

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/Source-Controller-OCI-Repository/page

This guide explains how to use the Flux Source Controller to fetch resources from an OCI artifacts repository.

In this guide, we’ll show you how to use the Flux Source Controller to fetch resources from an OCI artifacts repository. This approach works with any compliant OCI registry—such as GitHub Container Registry (GHCR), Docker Hub, or cloud‐hosted registries—by leveraging the OCI Artifacts API.

## Prerequisites

* A running Kubernetes cluster with Flux installed in the `flux-system` namespace
* An OCI registry account (e.g., GitHub Container Registry)
* A personal access token (PAT) or registry credentials with pull permissions

## 1. Create the OCI Secret

First, store your registry credentials in a Flux `Secret` of type `OCI`. This will allow Flux to authenticate when fetching artifacts.

<Callout icon="triangle-alert">
  Do **not** commit your `<GitHub-Personal-Access-Token>` or any credentials into your Git repository. Treat them as sensitive data.
</Callout>

```bash theme={null}
flux create secret oci ghcr-auth \
  --url ghcr.io \
  --username sidd-harth \
  --password <<GitHub-Personal-Access-Token>>
