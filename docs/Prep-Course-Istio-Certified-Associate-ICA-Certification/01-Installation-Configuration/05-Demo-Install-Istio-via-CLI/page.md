# Example output:
# Istio is not present in the cluster: no running Istio pods in namespace "istio-system"
# client version: 1.26.3
```

## 2 — Install Istio using the ambient profile

Install Istio with the ambient profile:

```bash theme={null}
istioctl install --set profile=ambient -y
# Processing resources for Istio core.
```

Wait for the control plane components to become ready.

## 3 — Verify Istio system pods and daemonsets

Check pods in `istio-system` — ambient mode shows `ztunnel` and `istio-cni-node`:

```bash theme={null}
kubectl get pods -n istio-system
# NAME                                READY   STATUS    RESTARTS   AGE
# istio-cni-node-xxxxx               1/1     Running   0          19s
# istiod-xxxx                        1/1     Running   0          27s
# ztunnel-xxxxx                      1/1     Running   0          13s
```

Check daemonsets (notice `ztunnel` and `istio-cni-node` run as DaemonSets):

```bash theme={null}
kubectl get ds -n istio-system
# NAME            DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                AGE
# istio-cni-node  1         1         1       1            1           kubernetes.io/os=linux       31s
# ztunnel         1         1         1       1            1           kubernetes.io/os=linux       25s
```

* ztunnel: handles L4 traffic interception for workloads in ambient mode.
* istio-cni-node: handles CNI and iptables conversions so workloads are transparently routed.

## 4 — Namespace labeling for ambient dataplane mode

In sidecar mode you'd label namespaces with `istio-injection=enabled`. For ambient mode, label namespaces with `istio.io/dataplane-mode=ambient`.

Check current namespace labels:

```bash theme={null}
kubectl get ns --show-labels
# NAME            STATUS   AGE   LABELS
# default         Active   3m7s  kubernetes.io/metadata.name=default
# istio-system    Active   73s   kubernetes.io/metadata.name=istio-system
```

`istioctl analyze` may still report injection info targeted at sidecar mode:

```bash theme={null}
istioctl analyze -n default
# Info [IST0102] (Namespace default) The namespace is not enabled for Istio injection.
# Run 'kubectl label namespace default istio-injection=enabled' to enable it...
```

Label the `default` namespace for ambient dataplane mode:

```bash theme={null}
kubectl label namespace default istio.io/dataplane-mode=ambient
# namespace/default labeled
```

Verify the label:

```bash theme={null}
kubectl get ns --show-labels
# default Active ... istio.io/dataplane-mode=ambient,kubernetes.io/metadata.name=default
```

## 5 — Run a test workload and confirm traffic is intercepted by ztunnel

Create a simple test pod (NGINX image used here):

```bash theme={null}
kubectl run test --image=nginx
# pod/test created
kubectl get pods
# NAME   READY   STATUS    RESTARTS   AGE
# test   1/1     Running   0          7s
```

Since ambient mode does not use a sidecar, the pod shows `1/1`. ztunnel intercepts the host‑level L4 traffic.

Tail ztunnel logs to observe intercepted connections:

```bash theme={null}
kubectl logs -n istio-system -f <ztunnel-pod-name>
# Look for lines like:
# info    proxy::outbound listener established address=[::]:15001 component="outbound" transparent=true
# info    access  connection complete  src.workload="test" src.namespace="default" dst.addr=74.125.126.104:80 direction="outbound" bytes_sent=79 bytes_recv=1028 duration="63ms"
```

From the `test` pod, execute a simple curl to an external site to generate outbound traffic:

```bash theme={null}
kubectl exec test -- curl --head www.google.com
# Should return HTTP/1.1 200 OK and headers
```

You should see corresponding `access connection complete` entries in the ztunnel logs. This confirms L4 interception and basic outbound connectivity through ztunnel.

> **warning** Ambient mode provides transparent L4 interception out of the box. For L7 features (HTTP routing, mirroring, fault injection) you must deploy waypoint proxies and use Kubernetes Gateway API resources (e.g., `HTTPRoute`). These are distinct from Istio sidecar VirtualServices and require additional CRDs and configuration.

## 6 — Install Kubernetes Gateway API CRDs (required for waypoint + HTTPRoute)

Install the Gateway API CRDs (example uses Gateway API v1.3.0 standard install):

```bash theme={null}
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
# customresourcedefinition.apiextensions.k8s.io/gatewayclasses.gateway.networking.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/gateways.gateway.networking.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/grpcroutes.gateway.networking.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/htroutes.gateway.networking.k8s.io created
# customresourcedefinition.apiextensions.k8s.io/referencegrants.gateway.networking.k8s.io created
```

Verify CRDs (partial list):

```bash theme={null}
kubectl get crd | grep gateway
# gatewayclasses.gateway.networking.k8s.io
# gateways.gateway.networking.k8s.io
# httproutes.gateway.networking.k8s.io
```

## 7 — Apply a waypoint proxy for layer‑7 capabilities (optional)

Create a waypoint in the namespace to enable an Envoy proxy as an entry point for L7 traffic:

```bash theme={null}
istioctl waypoint apply -n default
# ✅ waypoint default/waypoint applied
```

Check pods: a `waypoint` Deployment will create a pod:

```bash theme={null}
kubectl get pods
# NAME                                      READY   STATUS              RESTARTS   AGE
# test                                      1/1     Running             0          2m34s
# waypoint-7cb5d4bd6-crnmp                  1/1     Running             0          7s
```

Confirm the waypoint is created as a Deployment:

```bash theme={null}
kubectl get deployments.apps
# NAME       READY   UP-TO-DATE   AVAILABLE   AGE
# waypoint   1/1     1            1           99s
```

Use waypoint proxies when you need the L7 features (HTTPRoute, mirroring, fault injection) — note these use Gateway API resources like `HTTPRoute`, which are Kubernetes-native and not Istio VirtualServices.

## 8 — Remove waypoint proxy (if desired)

To delete all waypoint resources in a namespace:

```bash theme={null}
istioctl waypoint delete --all -n default
# waypoint default/waypoint deleted
kubectl get pods
# waypoint-* will be Terminating then removed
```

## Quick reference — Commands summary

| Task                        | Command                                                                                                          |                              |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Download Istio              | \`curl -L [https://istio.io/downloadIstio](https://istio.io/downloadIstio)                                       | ISTIO\_VERSION=1.26.3 sh -\` |
| Add istioctl to PATH        | `export PATH=$PWD/bin:$PATH`                                                                                     |                              |
| Install ambient profile     | `istioctl install --set profile=ambient -y`                                                                      |                              |
| Check pods                  | `kubectl get pods -n istio-system`                                                                               |                              |
| Check daemonsets            | `kubectl get ds -n istio-system`                                                                                 |                              |
| Label namespace for ambient | `kubectl label namespace default istio.io/dataplane-mode=ambient`                                                |                              |
| Run a test pod              | `kubectl run test --image=nginx`                                                                                 |                              |
| Tail ztunnel logs           | `kubectl logs -n istio-system -f <ztunnel-pod-name>`                                                             |                              |
| Install Gateway API CRDs    | `kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml` |                              |
| Apply waypoint              | `istioctl waypoint apply -n default`                                                                             |                              |
| Delete waypoint             | `istioctl waypoint delete --all -n default`                                                                      |                              |

## What to expect and exam note

* Ambient mode: uses `ztunnel` (daemon) + `istio-cni` to transparently intercept L4 traffic. Workloads do not show a sidecar container.
* Waypoint proxy: required for advanced L7 features. It relies on the Kubernetes Gateway API (`Gateway`, `HTTPRoute`) rather than Istio VirtualServices.
* If you’re preparing for the ICA/field exam: you typically only need to know how to install ambient mode and label namespaces to enable dataplane interception (L4). Deep waypoint or HTTPRoute configuration is usually out of scope.

## References

* Istio Ambient Mode (official docs): [https://istio.io/latest/docs/setup/additional-setup/ambient/](https://istio.io/latest/docs/setup/additional-setup/ambient/)
* Gateway API (GitHub releases): [https://github.com/kubernetes-sigs/gateway-api](https://github.com/kubernetes-sigs/gateway-api)
* istioctl documentation: [https://istio.io/latest/docs/reference/commands/istioctl/](https://istio.io/latest/docs/reference/commands/istioctl/)

That's the end of the demo — you should now have a working Istio ambient installation, observe L4 traffic handled by ztunnel, and understand when to use waypoint proxies for L7 features.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/105379ce-f1aa-4d80-ab41-b3bf398a80e1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/dcd771d9-ecff-4b53-bbbc-a98e43ab95b9)


# Demo Install Istio via CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Installation-Configuration/Demo-Install-Istio-via-CLI/page

Guide to installing Istio with istioctl, enabling automatic namespace sidecar injection, performing manual per-workload injection, and demonstrating with the Bookinfo sample on Kubernetes.

This guide demonstrates how to install Istio into a Kubernetes cluster using the `istioctl` CLI, enable automatic sidecar injection for a namespace, and perform manual (per-workload) injection. It uses the Bookinfo sample app to show sidecar behavior before and after injection.

Prerequisites: a running Kubernetes cluster and `kubectl` configured to talk to it.

> **lightbulb** Before you begin

  * Ensure `kubectl` is configured and can access your cluster.
  * Choose an Istio release (this lesson uses `1.26.3`). Keep your `istioctl` client version compatible with the control plane you intend to install.

## 1) Inspect the cluster and deploy the Bookinfo sample

First, confirm only the standard application pods are present (no Istio sidecars yet):

```bash theme={null}
root@controlplane:~# kubectl get pods
NAME                                    READY   STATUS             RESTARTS   AGE
details-v1-65599dcf88-k44bb            1/1     Running            0          11s
productpage-v1-9487c9c5b-9cqhs         0/1     ContainerCreating  0          10s
ratings-v1-59b99c644-fhsp8             1/1     Running            0          11s
reviews-v1-5985998584-k4lph            0/1     ContainerCreating  0          11s
reviews-v2-866dcc668-qntwq             0/1     ContainerCreating  0          11s
reviews-v3-dbbf5b5d-ffg9v              0/1     ContainerCreating  0          11s
```

Describe a pod (example: `details-v1`) to verify it currently contains only the application container and no `istio-proxy`:

```bash theme={null}
root@controlplane:~# kubectl describe pod details-v1-65599dcf88-k44bb
