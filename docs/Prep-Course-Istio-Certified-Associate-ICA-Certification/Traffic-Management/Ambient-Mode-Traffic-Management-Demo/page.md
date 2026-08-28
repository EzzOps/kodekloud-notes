# Ambient Mode Traffic Management Demo

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Ambient-Mode-Traffic-Management-Demo/page

Demo of Istio Ambient Mode traffic management showing ztunnel L4, waypoint L7, differences from sidecar mode, and using HTTPRoute and waypoint for request splitting and fault injection

This guide demonstrates how common Istio traffic-management features behave in Ambient Mode. You'll learn which control-plane primitives still work, which require Kubernetes-native APIs (for example, HTTPRoute), and how the waypoint proxy fits into request flows.

Note: Ambient Mode is typically a small part of the [ICA exam objectives](https://learn.kodekloud.com/user/courses/istio-certified-associate). Practically, you should know how to install Ambient Mode and label namespaces. This article is a hands-on demo to illustrate Ambient Mode behavior and how to implement L7 features using a waypoint proxy.

<Callout icon="lightbulb">
  Ambient Mode uses the `ztunnel` DaemonSet for L4 routing and an optional waypoint (Envoy) proxy for L7 behaviors. Some Istio features (for example, split traffic using VirtualService subsets or mirroring) require different Kubernetes-native APIs in Ambient Mode.
</Callout>

***

## Table: Sidecar vs Ambient — API/Behavior mapping

| Feature                       | Sidecar mode (classic)                       | Ambient mode (ztunnel + waypoint)                                          |
| ----------------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| L4 routing                    | iptables + sidecar                           | `ztunnel` DaemonSet (L4)                                                   |
| L7 routing / weights          | `VirtualService` + `DestinationRule` subsets | `HTTPRoute` + waypoint; `VirtualService` may work when waypoint handles L7 |
| Fault injection (delay/abort) | `VirtualService` fault rules                 | Often via waypoint + `VirtualService` (depends on setup)                   |
| Mirroring                     | `VirtualService` mirror                      | Not supported / limited in Ambient Mode                                    |

References:

* [Istio Ambient Mode docs](https://istio.io/latest/docs/ops/deployment/ambient/)
* [Istio Gateway API support](https://istio.io/latest/docs/reference/config/networking/gateway/)

***

## Verify Ambient components

Assuming Istio Ambient Mode has been installed, confirm the core control-plane components are running in the `istio-system` namespace:

```bash theme={null}
kubectl get pods -n istio-system
```

Example (trimmed):

```text theme={null}
NAME                        READY   STATUS    RESTARTS   AGE
istio-cni-node-vdt82        1/1     Running   0          3m
istiod-6b85468cc-nnfk4      1/1     Running   0          3m
ztunnel-qgtj5               1/1     Running   0          3m
```

Check namespaces and labels. Ambient Mode commonly uses:

* `istio.io/dataplane-mode=ambient`
* `istio.io/use-waypoint=waypoint` (for namespaces that need L7 capabilities)

Inspect your namespaces:

```bash theme={null}
kubectl get ns --show-labels
```

Sample output:

```text theme={null}
NAME           STATUS   AGE     LABELS
hello          Active   5m      kubernetes.io/metadata.name=hello
test           Active   6m      kubernetes.io/metadata.name=test
istio-system   Active   8m      kubernetes.io/metadata.name=istio-system
