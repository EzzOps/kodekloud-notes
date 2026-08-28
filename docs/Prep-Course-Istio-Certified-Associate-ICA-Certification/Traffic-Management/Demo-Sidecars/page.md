# Demo Sidecars

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Sidecars/page

Hands-on Istio Sidecars lab demonstrating sidecar injection, mTLS PeerAuthentication effects, and Sidecar egress/workload restrictions using the Bookinfo sample.

Welcome to the Sidecars lab — the first hands-on exercise in Traffic Management. This guide preserves the original flow while clarifying steps, commands, and outcomes so you can reproduce and understand how Istio sidecars, PeerAuthentication (mTLS), and Sidecar resources interact.

## Goals

* Verify Istio injection labels on namespaces
* Deploy the Bookinfo sample app
* Observe sidecar injection behavior
* Apply a `PeerAuthentication` (mTLS STRICT) to the `default` namespace and see the effect
* Enable injection on a client namespace to restore connectivity
* Create `Sidecar` resources to restrict egress for workloads and observe how workload selectors change behavior

***

## 1) Verify namespace labels and deploy Bookinfo

Confirm the default namespace has Istio injection enabled:

```bash theme={null}
kubectl get ns --show-labels
```

Example output:

```plaintext theme={null}
NAME              STATUS   AGE   LABELS
default           Active   4m2s  istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   91s   kubernetes.io/metadata.name=istio-system
kube-node-lease   Active   4m2s  kubernetes.io/metadata.name=kube-node-lease
kube-public       Active   4m2s  kubernetes.io/metadata.name=kube-public
kube-system       Active   2m2s  kubernetes.io/metadata.name=kube-system
```

Apply the Bookinfo sample manifest:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml
```

You should see resources being created, e.g.:

```plaintext theme={null}
service/details created
deployment.apps/details-v1 created
service/productpage created
deployment.apps/productpage-v1 created
