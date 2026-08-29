# oci secret 'ghcr-auth' created in 'flux-system' namespace
```

## 2. Register the OCI Repository as a Source

Point Flux to your OCI‐hosted image or artifact by creating an `OCIRepository` source.

```bash theme={null}
flux create source oci nginx \
  --url oci://ghcr.io/sidd-harth/nginx \
  --tag 1.0.0 \
  --secret-ref ghcr-auth \
  --provider generic
# applying OCIRepository
# OCIRepository updated
# waiting for OCIRepository reconciliation
# OCIRepository reconciliation completed
# fetched revision: 1b31558/235b486df4a38f99336712
```

## 3. Apply Manifests with Kustomization

Once the `OCIRepository` is ready, deploy its manifests into your cluster via a `Kustomization`.

```bash theme={null}
flux create kustomization kust-nginx-oci \
  --source OCIRepository/nginx \
  --target-namespace default \
  --interval 10s \
  --prune=false \
  --health-check="Deployment/nginx.default"
# generating Kustomization
# applying Kustomization
# Kustomization updated
# waiting for Kustomization reconciliation
# Kustomization kust-nginx-oci is ready
# applied revision 1b31558/235b486df4a38f99336712
```

> **lightbulb** Set `--prune=false` if you want to retain orphaned resources. Adjust `--interval` to control reconciliation frequency.

***

## 4. Fetching OCI-Hosted Helm Charts

Flux’s Kustomize Controller cannot process Helm charts directly. To deploy charts stored in an OCI registry, register the same registry as a Helm source.

### 4.1 Register the Helm Repository

```bash theme={null}
flux create source helm chart-oci \
  --url oci://ghcr.io/sidd-harth/chart \
  --secret-ref ghcr-auth
# generating HelmRepository source
# applying HelmRepository source
# HelmRepository source updated
# waiting for HelmRepository source reconciliation
# HelmRepository source reconciliation completed
```

### 4.2 Deploy the Helm Chart

Create a `HelmRelease` to instruct Flux’s Helm Controller to fetch and install the chart.

```bash theme={null}
flux create helmrelease chart-oci-release \
  --source HelmRepository/chart-oci \
  --target-namespace nginx \
  --chart nginx \
  --chart-version 0.1.0
# generating HelmRelease
# applying HelmRelease
# HelmRelease chart-oci-release created
# waiting for HelmRelease reconciliation
# HelmRelease chart-oci-release is ready
# applied revision 0.1.0
```

This will trigger the Helm Controller to pull chart artifacts from your OCI registry and perform automated releases.

***

## Comparison of OCI vs. Helm Sources

| Resource Type  | Controller           | Use Case                        |
| -------------- | -------------------- | ------------------------------- |
| OCIRepository  | Source Controller    | Static YAML, images, configs    |
| Kustomization  | Kustomize Controller | Apply kustomized manifests      |
| HelmRepository | Source Controller    | OCI-packaged Helm charts        |
| HelmRelease    | Helm Controller      | Automated Helm chart deployment |

***

## Links and References

* [Flux CD Documentation](https://fluxcd.io/docs/)
* [OCI Artifacts Specification](https://github.com/opencontainers/artifacts)
* [Kustomize Controller](https://fluxcd.io/docs/components/kustomize/)
* [Helm Controller](https://fluxcd.io/docs/components/helm/)
* [GitHub Container Registry](https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/e0dac113-2d98-451d-a64c-9989507e8b8c)


# What are OCI Artifacts

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/What-are-OCI-Artifacts/page

This guide explains how OCI Artifacts streamline the storage and distribution of Kubernetes resources in a unified registry.

In this guide, you’ll discover how **OCI Artifacts** simplify storing and distributing a variety of Kubernetes-related resources in a single, unified registry. By leveraging any OCI-compliant registry, you benefit from consistent authentication, authorization, and versioning across:

* Container images
* Helm charts
* Kubernetes manifests
* Kustomize overlays
* OPA policies

## Traditional vs. OCI-Based Storage

| Resource Type                   | Traditional Storage                                                           | Unified OCI Registry   |
| ------------------------------- | ----------------------------------------------------------------------------- | ---------------------- |
| Container images                | Container registries                                                          | OCI-compliant registry |
| Helm charts                     | [Artifact Hub](https://artifacthub.io) or Helm registries                     | OCI-compliant registry |
| Kubernetes manifests & overlays | Git repositories                                                              | OCI-compliant registry |
| OPA policies                    | [Open Policy Registry](https://openpolicyagent.org/docs/latest/opa-registry/) | OCI-compliant registry |

> **lightbulb** An OCI registry implements the [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec), enabling you to store any artifact type beyond container images.

***

## OCI Registries and Repositories

An **OCI Registry** is a server-side component that hosts one or more **repositories**, each containing multiple **artifacts** at various tags or digests.

* Registry → Repository → Artifact
* Artifacts can be images, charts, manifests, or any OCI-compatible payload

Next, we’ll walk through pushing three artifact types—Docker images, Helm charts, and plain Kubernetes manifests—to GitHub Container Registry (`ghcr.io`). The workflow applies equally to Azure, GCR, ECR, and other OCI-compliant registries.

***

## 1. Pushing a Docker Image

1. Authenticate with the registry.
2. Tag your local image.
3. Push it upstream.

```bash theme={null}
