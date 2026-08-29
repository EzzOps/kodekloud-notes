# Demo Istio mTLS

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Demo-Istio-mTLS/page

This tutorial teaches how to enforce mutual TLS between Kubernetes workloads using Istio’s PeerAuthentication API.

In this tutorial, you’ll learn how to enforce mutual TLS (mTLS) between your Kubernetes workloads using Istio’s PeerAuthentication API. We’ll cover:

* Listing Istio Custom Resource Definitions (CRDs)
* Inspecting pods and services in the `prod` namespace
* Observing traffic before and after mTLS
* Applying `DISABLE`, `PERMISSIVE`, and `STRICT` mTLS modes
* Verifying encryption with packet capture

## Prerequisites

* A running Kubernetes cluster with Istio installed
* `kubectl` configured for your cluster
* Kiali add-on for traffic visualization

## 1. List Istio CRDs

Istio installs several CRDs, including PeerAuthentication. To view them:

```bash theme={null}
kubectl get crd
```

Example output:

```bash theme={null}
NAME                                                   CREATED AT
authorizationpolicies.security.istio.io               2021-06-20T13:04:57Z
envoyfilters.networking.istio.io                       2021-06-20T13:04:57Z
gateways.networking.istio.io                           2021-06-20T13:04:57Z
istiooperators.install.istio.io                        2021-06-20T13:04:57Z
monitoringdashboards.monitoring.kiali.io               2021-06-20T13:04:36Z
peerauthentication.security.istio.io                   2021-06-20T13:04:57Z
requestauthentications.security.istio.io               2021-06-20T13:04:57Z
services.networking.istio.io                           2021-06-20T13:04:57Z
sidecars.networking.istio.io                           2021-06-20T13:04:57Z
virtualservices.networking.istio.io                    2021-06-20T13:04:57Z
workloadentries.networking.istio.io                    2021-06-20T13:04:57Z
workloadgroups.networking.istio.io                     2021-06-20T13:04:56Z
```

By default, no PeerAuthentication resources are defined:

```bash theme={null}
kubectl get peerauthentication -A
