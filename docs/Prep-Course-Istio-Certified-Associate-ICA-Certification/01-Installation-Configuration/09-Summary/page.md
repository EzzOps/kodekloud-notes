# Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Summary/page

Guide to installing, configuring, and managing Istio on Kubernetes, covering installation methods, sidecar versus ambient modes, operator customization, and canary upgrades.

This lesson reviews the essential concepts and operational tasks for installing, configuring, and managing Istio in Kubernetes clusters. It covers prerequisites, recommended installation patterns, sidecar vs. sidecarless (ambient) modes, operator-based customization, and the canary (revision) upgrade workflow.

## Prerequisites

* A running Kubernetes cluster (cloud or local). Examples: AWS EKS, GKE, or local `kind`.
* Plan for additional cluster resources: Istio control plane and proxies consume CPU, memory, and network bandwidth.
* `kubectl` and `istioctl` (or Helm) installed on your local machine for management and troubleshooting.

## Installation methods

Choose the installation method based on how you manage cluster configuration (interactive installs vs GitOps).

| Method                      | When to use                                                                          | Example / Notes                                                    |
| --------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `istioctl install`          | Recommended for ad-hoc installs, quick evaluations, or interactive setups            | `istioctl install`                                                 |
| Helm charts                 | Use in GitOps workflows or when you need fine-grained templating and value overrides | Deploy `base`, `istiod`, and an optional ingress/gateway chart     |
| Operator / IstioOperator CR | Best for declarative control, reproducible configuration, and production management  | Manage via an `IstioOperator` spec applied with `istioctl` or Helm |

If you use Helm in GitOps (for example with Argo CD), you typically deploy three charts:

* `base`
* `istiod`
* `ingress` / `gateway` (optional if you do not accept external traffic)

> **lightbulb** If you are using Helm as part of a GitOps workflow, you will commonly deploy the `base`, `istiod`, and the ingress/gateway chart. Use `istioctl` for ad-hoc installs or interactive setups.

## Sidecar injection and namespace management

Istio does not modify namespaces by default. To enable automatic sidecar injection for workloads, label namespaces or perform manual injection.

| Injection approach                               | How to enable                                                                      | When to use                                                      |
| ------------------------------------------------ | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Legacy automatic injection                       | `kubectl label namespace <namespace> istio-injection=enabled`                      | Simple clusters; single control plane revision                   |
| Revision-based automatic injection (recommended) | `kubectl label namespace <namespace> istio.io/rev=<revision>`                      | Running multiple control plane revisions (canary upgrades)       |
| Manual injection                                 | `istioctl kube-inject -f deployment.yaml` or use `istioctl` sidecar inject command | When you prefer explicit control per workload or in CI pipelines |

Examples:

```bash theme={null}
