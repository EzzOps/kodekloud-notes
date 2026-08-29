# Example output:
# NAME                       READY   STATUS    RESTARTS   AGE
# istio-cni-node-zr8pb       1/1     Running   0          57s
# istiod-6b54648cc-ppq86     1/1     Running   0          65s
# ztunnel-9wjg7              1/1     Running   0          51s
```

Ensure ztunnel is present — it handles Ambient mode data-plane enforcement (L3/L4 mTLS).

## Create a test pod for issuing requests

Create a lightweight curl pod in the `test` namespace to issue requests during the demo:

```bash theme={null}
kubectl run curl --image=curlimages/curl -n test --restart=Never --command -- sleep infinity
kubectl get pods -n test
# pod/curl should be listed
```

This pod will act as a simple client for verifying connectivity and enforcement behavior.

## Deploy the HelloWorld app into the `hello` namespace

From your demo directory (contains `helloworld.yaml`), label the `hello` namespace for Ambient dataplane mode and apply the manifest:

```bash theme={null}
cd ~/demo
ls -l
kubectl label namespace hello istio.io/dataplane-mode=ambient
kubectl apply -f helloworld.yaml -n hello
# Example output:
# service/helloworld created
# deployment.apps/helloworld-v1 created
# deployment.apps/helloworld-v2 created
```

Verify deployments and service:

```bash theme={null}
kubectl get pods -n hello
kubectl get svc -n hello
# Example output:
# NAME                               READY   STATUS    RESTARTS   AGE
# helloworld-v1-xxxxx                1/1     Running   0          9s
# helloworld-v2-xxxxx                1/1     Running   0          9s
#
# NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
# helloworld   ClusterIP   10.100.96.89   <none>        5000/TCP   13s
```

## Enforce mTLS globally with PeerAuthentication

Create a global PeerAuthentication in the `istio-system` namespace to enforce mTLS STRICT across the mesh.

Create `global-pa.yaml`:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

Apply it and confirm:

```bash theme={null}
kubectl apply -f global-pa.yaml
kubectl get peerauthentications.security.istio.io -A
# NAMESPACE      NAME      MODE    AGE
# istio-system   default   STRICT  6s
```

Now attempt to access HelloWorld from the `test` curl pod:

```bash theme={null}
kubectl exec -n test curl -- curl --head http://helloworld.hello.svc.cluster.local:5000/hello
```

You will likely see a connection reset because mTLS is enforced and the `test` pod is not yet participating in Ambient dataplane mode.

Example error:

```text theme={null}
# curl: (56) Recv failure: Connection reset by peer
# command terminated with exit code 56
```

Explanation: the `hello` namespace is labeled for Ambient mode but `test` is not. Ambient-mode enforcement expects the caller to be an ambient participant (or otherwise use mTLS-capable client identities). Label the `test` namespace for Ambient mode:

```bash theme={null}
kubectl label namespace test istio.io/dataplane-mode=ambient
```

Retry the request:

```bash theme={null}
kubectl exec -n test curl -- curl --head http://helloworld.hello.svc.cluster.local:5000/hello
# Example success:
# HTTP/1.1 200 OK
# Server: gunicorn
# Date: Mon, 01 Sep 2025 05:38:34 GMT
# Connection: keep-alive
```

<Callout icon="lightbulb">
  In Ambient mode, mTLS enforcement is handled by the ztunnel at the dataplane layer. For successful communication, both caller and callee namespaces should be labeled with `istio.io/dataplane-mode=ambient` (or the client must present mTLS identity).
</Callout>

## Authorization policies: layer-3/4 vs layer-7 differences

Ambient mode separates responsibilities:

* L3/L4 (identity, mTLS) — enforced by ztunnel
* L7 (HTTP route/method-level rules) — enforced by the waypoint proxy

This means AuthorizationPolicy behavior differs from sidecar mode. A policy that appears to be an L7 rule but lacks a configured waypoint or uses non-ambient constructs may be ignored or produce connection errors.

Example: create a basic AuthorizationPolicy that attempts to allow only GET/HEAD from the `test` namespace. Save as `hw-auth-policy.yaml`:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: hello-world-auth-policy
  namespace: hello
spec:
  action: ALLOW
  selector:
    matchLabels:
      app: helloworld
  rules:
    - from:
        - source:
            namespaces: ["test"]
      to:
        - operation:
            methods: ["GET", "HEAD"]
```

Apply it:

```bash theme={null}
kubectl apply -f hw-auth-policy.yaml
kubectl get authorizationpolicies.security.istio.io -A
# NAMESPACE  NAME                       ACTION  AGE
# hello      hello-world-auth-policy    ALLOW   5s
```

If you curl from `test` now, you may still get a connection reset or a 503. Why? Because the policy above is an L7 rule that relies on the waypoint to enforce route-level methods. Without a waypoint configured for the `hello` service, Ambient mode cannot reliably enforce this L7 policy and traffic may be rejected.

## Configure the waypoint proxy for the `hello` namespace

Apply a waypoint for the `hello` namespace and label the namespace to use it:

```bash theme={null}
istioctl waypoint apply -n hello
# Example output:
# ✔ waypoint hello/waypoint applied
```

Check pods to see the waypoint pod starting:

```bash theme={null}
kubectl get pods -n hello
# NAME                           READY   STATUS    RESTARTS   AGE
# helloworld-v1-...              1/1     Running   0          5m
# helloworld-v2-...              1/1     Running   0          5m
# waypoint-...                   1/1     Running   0          10s
```

Label the namespace to use the waypoint:

```bash theme={null}
kubectl label namespace hello istio.io/use-waypoint=waypoint
kubectl get ns hello --show-labels
# NAME   STATUS  AGE   LABELS
# hello  Active  9m    istio.io/dataplane-mode=ambient,istio.io/use-waypoint=waypoint, kubernetes.io/metadata.name=hello
```

Retry the curl from `test`:

```bash theme={null}
kubectl exec -n test curl -- curl --head http://helloworld.hello.svc.cluster.local:5000/hello
# Example:
# HTTP/1.1 503 Service Unavailable
# server: istio-envoy
# x-envoy-decorator-operation: helloworld.hello.svc.cluster.local:5000/*
```

A 503 indicates the request is reaching the waypoint Envoy, but the L7 enforcement point is rejecting the request. This commonly happens because the AuthorizationPolicy is not expressed in a form Ambient mode expects for L7 enforcement.

<Callout icon="warning">
  When you enable a waypoint for L7 enforcement, ensure AuthorizationPolicy targets and identity principals are expressed explicitly. Using namespace selectors alone often does not work for L7 in Ambient mode.
</Callout>

## AuthorizationPolicy for Ambient mode: use targetRefs + principals

Ambient mode follows a zero-trust, explicit model for L7 policies. Use `targetRefs` to point AuthorizationPolicy at a Service and `principals` to identify callers by mTLS identity (service account). Example `hw-auth-policy-v2.yaml`:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: hello-world-auth-policy
  namespace: hello
spec:
  targetRefs:
    - kind: Service
      group: ""
      name: helloworld
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/test/sa/default
      to:
        - operation:
            methods: ["GET", "HEAD"]
```

Key differences from the earlier policy:

* `targetRefs` targets the `helloworld` Service directly (L7 enforcement point expects explicit service targets).
* `from.source.principals` uses the mTLS identity `cluster.local/ns/<ns>/sa/<sa-name>` instead of namespace selectors.

Apply the v2 policy and verify:

```bash theme={null}
kubectl apply -f hw-auth-policy-v2.yaml
kubectl get authorizationpolicies.security.istio.io -A
# NAMESPACE  NAME                       ACTION  AGE
# hello      hello-world-auth-policy    ALLOW   4s
```

Retry from the `test` curl pod (default service account `default` in `test` namespace). It should now succeed:

```bash theme={null}
kubectl exec -n test curl -- curl --head http://helloworld.hello.svc.cluster.local:5000/hello
# HTTP/1.1 200 OK
```

## Validate the policy by testing from a non-allowed namespace

Create a new namespace `web`, label it for Ambient mode, and run an nginx pod. This pod will use the `default` service account in `web`, which is not allowed by the policy above.

```bash theme={null}
kubectl create namespace web
kubectl label namespace web istio.io/dataplane-mode=ambient
kubectl run app -n web --image=nginx --restart=Never
kubectl get pods -n web
```

From the `web` pod, curl the HelloWorld service:

```bash theme={null}
kubectl exec -n web app -- curl --head http://helloworld.hello.svc.cluster.local:5000/hello
# Expected result:
# HTTP/1.1 403 Forbidden
# content-length: 19
# content-type: text/plain
# server: istio-envoy
# x-envoy-decorator-operation: helloworld.hello.svc.cluster.local:5000/*
```

The 403 response indicates the incoming principal (e.g., `cluster.local/ns/web/sa/default`) is not allowed by the AuthorizationPolicy, which explicitly allowed only `cluster.local/ns/test/sa/default`.

## Notes about service accounts and principals

* Every namespace has a `default` service account. For least privilege and clearer policies, create dedicated service accounts for workloads and reference those in `principals`, for example: `cluster.local/ns/<ns>/sa/<service-account>`.
* Prefer `targetRefs` (Service) + `principals` (service account identity) for L7 AuthorizationPolicy in Ambient mode. This pattern aligns with Ambient mode’s explicit, identity-based enforcement.
* In sidecar mode, policies commonly use `selector.matchLabels` and `namespaces`. Ambient mode shifts L7 policy expression to service-targeted, identity-based constructs, enforced by the waypoint.

## Quick comparison: Sidecar mode vs Ambient mode (L7 enforcement)

| Aspect                               | Sidecar mode                          | Ambient mode                                          |
| ------------------------------------ | ------------------------------------- | ----------------------------------------------------- |
| L7 enforcement location              | Sidecar Envoy per workload            | Waypoint proxy (per-service/namespace)                |
| Common AuthorizationPolicy targeting | `selector.matchLabels` + `namespaces` | `targetRefs` (Service) + `principals` (mTLS identity) |
| mTLS enforcement                     | Sidecar dataplane                     | ztunnel (Ambient dataplane)                           |
| Typical failure modes                | Misapplied label selectors            | Missing waypoint or non-explicit principals           |

## Cleanup (optional)

To remove demo resources:

```bash theme={null}
kubectl delete -f hw-auth-policy-v2.yaml
kubectl delete -f hw-auth-policy.yaml || true
kubectl delete -f global-pa.yaml
kubectl delete -n web pod/app
kubectl delete pod/curl -n test
kubectl delete -n web namespace/web || true
```

## Summary

* Label namespaces with `istio.io/dataplane-mode=ambient` to participate in Ambient dataplane features.
* Enforce mTLS via PeerAuthentication; ensure both caller and callee can perform mTLS.
* For L7 AuthorizationPolicy in Ambient mode:
  * Configure a waypoint for the target namespace/service.
  * Prefer `targetRefs` + `principals` (service account-based mTLS identities) over namespace selectors.
* Ambient mode separates L3/L4 enforcement (ztunnel) from L7 (waypoint) — this changes how policies need to be expressed. Expect behavior to evolve as Ambient mode matures.

## Links and references

* Istio Ambient Mode overview: [https://istio.io/latest/docs/ops/deployment/ambient/](https://istio.io/latest/docs/ops/deployment/ambient/)
* AuthorizationPolicy reference: [https://istio.[AWS_SECRET_ACCESS_KEY]/authorization-policy/](https://istio.[AWS_SECRET_ACCESS_KEY]/authorization-policy/)
* PeerAuthentication reference: [https://istio.[AWS_SECRET_ACCESS_KEY]/peer\_authentication/](https://istio.[AWS_SECRET_ACCESS_KEY]/peer_authentication/)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/43061c1f-8ac1-4a33-aa98-dff962f9b9ad" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/2cd41378-65b3-4710-a7f0-46fbb10c4f77" />
</CardGroup>


# Demo Authentication

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Demo-Authentication/page

Guide to configuring Istio PeerAuthentication and mTLS, deploying hello-world, enforcing global strict mode, and overriding policies by namespace or workload selectors

In this lesson you'll configure authentication in Istio, deploy a simple hello-world app, observe how PeerAuthentication enforces mTLS, and learn how to override global policies at namespace or workload scope.

Prerequisites: `kubectl` and `istioctl` configured to talk to your cluster.

<Callout icon="lightbulb">
  Ensure your cluster has Istio installed and the `istio-system` namespace is present. Use `istioctl version` and `kubectl get ns` to validate installation before proceeding.
</Callout>

## 1) Verify Istio automatic sidecar injection on namespaces

Check namespace labels to determine whether automatic Envoy sidecar injection is enabled:

```bash theme={null}
kubectl get ns --show-labels
```

Example output:

```plaintext theme={null}
NAME            STATUS   AGE   LABELS
default         Active   3m   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system    Active   91s  kubernetes.io/metadata.name=istio-system
kube-system     Active   3m   kubernetes.io/metadata.name=kube-system
test            Active   6m   istio-injection=enabled,kubernetes.io/metadata.name=test
```

The label `istio-injection=enabled` means pods created in that namespace get the Envoy sidecar injected automatically. If a namespace has no such label, pods will not be injected and won't participate in mTLS unless manually proxied.

## 2) Deploy the helloworld sample

Apply the sample manifest to create the hello-world service and workloads:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.[SECRET_REDACTED].yaml
```

Verify pods are created and ready:

```bash theme={null}
kubectl get pods -l app=helloworld
```

Example ready state:

```plaintext theme={null}
NAME                            READY   STATUS    RESTARTS   AGE
helloworld-v1-7459d7b54b-f7cxb  2/2     Running   0          2m
helloworld-v2-654d97458-r84kp   2/2     Running   0          2m
```

Note: `2/2` indicates the application container plus the Envoy sidecar are running.

## 3) Create a test namespace and run a client pod

Create a namespace `test` (if it doesn't already exist) and run an nginx pod to act as a client:

```bash theme={null}
kubectl create ns test
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

If you accidentally created the `test` pod in the `default` namespace, delete and recreate it in `test`:

```bash theme={null}
kubectl delete pod test
kubectl run test --image=nginx -n test
```

## 4) Verify connectivity from the test pod to helloworld

From the `test` pod, curl the hello endpoint on the helloworld service in the `default` namespace:

```bash theme={null}
kubectl exec -ti -n test test -- curl helloworld.default.svc:5000/hello
```

You should receive a response similar to:

```plaintext theme={null}
Hello version: v2, instance: helloworld-v2-654d97458-r84kp
```

Why this works: by default, Istio does not enforce mTLS cluster-wide — plaintext traffic is still allowed unless you enable enforcement via PeerAuthentication.

## 5) Enforce global mTLS with a PeerAuthentication

Create a global PeerAuthentication resource in `istio-system` to enforce strict mTLS cluster-wide.

peer\_auth\_global.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

Apply it:

```bash theme={null}
kubectl apply -f peer_auth_global.yaml
```

Confirm the PeerAuthentication exists:

```bash theme={null}
kubectl get peerauthentications.security.istio.io -A
```

Example output:

```plaintext theme={null}
NAMESPACE      NAME      MODE     AGE
istio-system   default   STRICT   10s
```

Now retry the curl from the non-injected `test` pod (if `test` is not injection-enabled):

```bash theme={null}
kubectl exec -ti -n test test -- curl --head helloworld.default.svc:5000/hello
```

You will likely see a failure like:

```plaintext theme={null}
curl: (56) Recv failure: Connection reset by peer
command terminated with exit code 56
```

Explanation: the server requires mTLS (STRICT). Because the `test` pod lacks an Envoy sidecar, the client sends plaintext traffic which the server rejects.

## 6) Enable injection for `test` namespace and retry

Use `istioctl analyze` to surface issues and then enable injection:

```bash theme={null}
istioctl analyze -n test
kubectl label namespace test istio-injection=enabled
```

Recreate the client pod so it gets injected:

```bash theme={null}
kubectl delete pod test -n test
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

Now retry the curl (from the injected client):

```bash theme={null}
kubectl exec -ti -n test test -- curl --head helloworld.default.svc:5000/hello
```

Expected response headers:

```plaintext theme={null}
HTTP/1.1 200 OK
server: envoy
date: Tue, 15 Apr 2025 18:12:06 GMT
content-type: text/html; charset=utf-8
content-length: 60
x-envoy-upstream-service-time: 122
```

Both client and server traffic are now proxied through Envoy and use mTLS, so the connection succeeds.

## 7) Override global policy at namespace scope (PERMISSIVE)

A PeerAuthentication in `istio-system` sets a global default but can be overridden by PeerAuthentication resources in namespaces. To allow plaintext and mTLS traffic in the `default` namespace, create a PERMISSIVE PeerAuthentication:

peer\_auth\_default.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: PERMISSIVE
```

Apply it:

```bash theme={null}
kubectl apply -f peer_auth_default.yaml
kubectl get peerauthentications.security.istio.io -A
```

Example output:

```plaintext theme={null}
NAMESPACE     NAME      MODE        AGE
default       default   PERMISSIVE  6s
istio-system  default   STRICT      3m7s
```

With PERMISSIVE in `default`, clients that are not mTLS-capable (non-injected) can still reach workloads in `default` using plaintext.

## 8) Target permissive mode to specific workloads (selector)

Instead of making an entire namespace permissive, scope the permissive mode to only the workloads that match labels (e.g., `app=helloworld`):

peer\_auth\_default.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  selector:
    matchLabels:
      app: helloworld
  mtls:
    mode: PERMISSIVE
```

Apply the change:

```bash theme={null}
kubectl apply -f peer_auth_default.yaml
kubectl get peerauthentications.security.istio.io -A
```

Now PERMISSIVE applies only to pods in `default` that have `app=helloworld`. Other workloads in `default` remain governed by the global `STRICT` policy in `istio-system`.

### Test with an `app` namespace (non-injected)

Create a non-injected `app` namespace and run an nginx pod:

```bash theme={null}
kubectl create ns app
kubectl run test --image=nginx -n app
kubectl get pods -n app
```

From the non-injected `app` pod, curl the helloworld endpoint:

```bash theme={null}
kubectl exec -ti -n app test -- curl --head helloworld.default.svc:5000/hello
```

Expected (permissive applies to helloworld):

```plaintext theme={null}
HTTP/1.1 200 OK
server: istio-envoy
date: Tue, 15 Apr 2025 18:14:44 GMT
content-type: text/html; charset=utf-8
content-length: 60
x-envoy-upstream-service-time: 136
x-envoy-decorator-operation: helloworld.default.svc.cluster.local:5000/*
```

Now try productpage (Bookinfo) in `default` from the same non-injected `app` pod. Because the selector only matched `app=helloworld`, `productpage` is still subject to global STRICT and will reject plaintext:

```bash theme={null}
kubectl exec -ti -n app test -- curl --head productpage.default.svc:9080
```

You should see:

```plaintext theme={null}
curl: (56) Recv failure: Connection reset by peer
command terminated with exit code 56
```

The same request from an injected namespace (e.g., `test`) will succeed:

```bash theme={null}
kubectl exec -ti -n test test -- curl --head productpage.default.svc:9080
```

Expected success:

```plaintext theme={null}
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
content-length: 1683
server: envoy
date: Tue, 15 Apr 2025 18:19:47 GMT
x-envoy-upstream-service-time: 4
```

Summary: a global `STRICT` enforces mTLS cluster-wide. PeerAuthentication resources scoped to a namespace or to specific workloads via `selector` can override that setting to `PERMISSIVE` or `DISABLE`.

## PeerAuthentication modes at a glance

| Mode         | Effect                              | When to use                                            |
| ------------ | ----------------------------------- | ------------------------------------------------------ |
| `STRICT`     | Only mTLS traffic is accepted       | Enforce mutual TLS across services for strong security |
| `PERMISSIVE` | Accepts both plaintext and mTLS     | Gradual rollout/migration to mTLS                      |
| `DISABLE`    | Disables mTLS on targeted workloads | When specific services must allow plaintext only       |
| `UNSET`      | No explicit mode set                | Falls back to higher-priority or default policy        |

## Useful references

* [Istio: PeerAuthentication (mTLS)](https://istio.[SECRET_REDACTED]peer_authentication/)
* `istioctl analyze` — use for policy validation and troubleshooting

<Callout icon="lightbulb">
  For troubleshooting: know that a global PeerAuthentication in `istio-system` can be overridden by PeerAuthentication resources in a namespace or by selectors. Use `istioctl analyze` and `kubectl get peerauthentications.security.istio.io -A` to inspect effective policies.
</Callout>

<Frame>
  <img alt="The image shows a webpage from Istio's documentation about Peer Authentication, specifically focusing on MutualTLS settings." />
</Frame>

## Appendix — example YAMLs

Global strict (peer\_auth\_global.yaml):

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

Namespace override (peer\_auth\_default.yaml, permissive for all workloads in `default`):

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: PERMISSIVE
```

Namespace override with selector (permissive only for app=helloworld):

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  selector:
    matchLabels:
      app: helloworld
  mtls:
    mode: PERMISSIVE
```

That completes this demo on PeerAuthentication and mTLS enforcement with Istio.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/7afc3a1c-dc16-4d2f-9c30-2964d7839bfe" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/074126a9-c3c1-4922-a4d1-6c40c70e4cd8" />
</CardGroup>
