# Expected output:
# serviceaccount/httpbin created
# service/httpbin created
# deployment.apps/httpbin created
```

Verify the httpbin pod is running:

```bash theme={null}
kubectl get pods
# NAME                      READY   STATUS    RESTARTS   AGE
# httpbin-787cdcc9df-nq8ht  2/2     Running   0          74s
```

Create a `test` namespace and enable automatic Envoy sidecar injection:

```bash theme={null}
kubectl create ns test
kubectl label ns test istio-injection=enabled
# Optional: validate the namespace with istioctl
# istioctl analyze -n test
# ✔ No validation issues found when analyzing namespace: test.
```

Run a simple client pod (nginx) in the `test` namespace — the Istio sidecar will be injected:

```bash theme={null}
kubectl run test --image=nginx -n test
# pod/test created
kubectl get pods -n test
# NAME   READY   STATUS    RESTARTS   AGE
# test   2/2     Running   0          7s
```

Get the httpbin service (note: this sample uses port 8000):

```bash theme={null}
kubectl get svc
# NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# httpbin      ClusterIP   10.96.105.55    <none>        8000/TCP   90s
# kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    39m
```

From the `test` pod, verify connectivity to httpbin (no policies yet):

```bash theme={null}
kubectl exec -ti test -n test -- curl --head http://httpbin.default.svc:8000
# HTTP/1.1 200 OK
# server: envoy
# x-envoy-upstream-service-time: 11
```

***

## 2. Enforce mTLS cluster-wide

Create a PeerAuthentication in the `istio-system` namespace to enforce strict mTLS:

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
# peerauthentication.security.istio.io/default created
kubectl get peerauthentications.security.istio.io -A
# NAMESPACE      NAME     MODE   AGE
# istio-system   default  STRICT 17s
```

With strict mTLS enforced, workloads in the mesh must present mTLS to communicate; Istio manages certificates via Citadel / Istiod.

***

## 3. Basic ALLOW policy — namespace-based, method-scoped

Create an AuthorizationPolicy that ALLOWs only GET requests from namespace `test` to the workload(s) in the policy scope.

auth\_policy\_allow\_test.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: httpbin-auth-policy
spec:
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["test"]
      to:
        - operation:
            methods: ["GET"]
```

Apply the policy and inspect:

```bash theme={null}
kubectl apply -f auth_policy_allow_test.yaml
kubectl get authorizationpolicies.security.istio.io
# NAME                ACTION   AGE
# httpbin-auth-policy ALLOW    7s
```

Important: `curl --head` issues an HTTP `HEAD` request, not `GET`. Because this policy allows only `GET`, `HEAD` requests will be denied.

<Callout icon="lightbulb">
  Tip: When testing method-based policies, use `curl --request GET` or a plain `curl` (defaults to GET). If you prefer HEAD behavior, include `HEAD` in the policy (e.g., `methods: ["GET", "HEAD"]`).
</Callout>

Update the policy to allow both GET and HEAD:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: httpbin-auth-policy
spec:
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["test"]
      to:
        - operation:
            methods: ["GET", "HEAD"]
```

Apply the updated policy and test again; now both HEAD and GET succeed from `test`.

***

## 4. Namespace scoping — allow only selected namespaces

Create another namespace `app`, enable injection, and run a test client there:

```bash theme={null}
kubectl create ns app
kubectl label ns app istio-injection=enabled
kubectl get ns --show-labels
# NAME    STATUS   AGE   LABELS
# app     Active   18s   istio-injection=enabled,kubernetes.io/metadata.name=app
# test    Active   5m58s istio-injection=enabled,kubernetes.io/metadata.name=test
# default Active   ...   istio-injection=enabled,kubernetes.io/metadata.name=default
```

Run a test pod in `app`:

```bash theme={null}
kubectl run test --image=nginx -n app
kubectl get pods -n app
# NAME   READY   STATUS    RESTARTS   AGE
# test   2/2     Running   0          16s
```

A request from `app` will be denied by the policy that allows only `test`:

```bash theme={null}
kubectl exec -ti test -n app -- curl --head http://httpbin.default.svc:8000
# HTTP/1.1 403 Forbidden
# server: envoy
```

To permit both `test` and `app`, include both namespaces in `from.source.namespaces`:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: httpbin-auth-policy
spec:
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["test", "app"]
      to:
        - operation:
            methods: ["GET", "HEAD"]
```

Apply and verify connectivity from both namespaces succeeds.

***

## 5. DENY specific paths and the DENY warning

Create a DENY policy that blocks requests to the `/delay` path:

auth\_policy\_deny.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: httpbin-auth-deny-policy
spec:
  action: DENY
  rules:
    - to:
        - operation:
            paths: ["/delay"]
```

Before applying, note the API warning behavior:

<Callout icon="warning">
  Warning: A DENY rule that uses only HTTP attributes (methods, paths) can impact TCP traffic under its scope unless you explicitly specify `ports`. Istio will warn when you apply such a rule. To avoid unintended TCP denial, scope the policy by `ports`, `selector`, or namespace.
</Callout>

Apply the DENY policy:

```bash theme={null}
kubectl apply -f auth_policy_deny.yaml
# Warning: configured AuthorizationPolicy will deny all traffic to TCP ports under its scope due to the use of only HTTP attributes in a DENY rule; it is recommended to explicitly specify the port
# authorizationpolicy.security.istio.io/httpbin-auth-deny-policy created
kubectl get authorizationpolicies.security.istio.io
# NAME                      ACTION   AGE
# httpbin-auth-deny-policy  DENY     7s
```

Requests to `http://httpbin.default.svc:8000/delay` will now be denied, even if an ALLOW policy also matches — see DENY precedence below.

***

## 6. Scoping ALLOW policies by selector, path, and methods

For precise allow rules (e.g., allow only GET/HEAD to `/get` from clients in `app` and only for the `httpbin` workload), use a `selector` and explicit paths:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: httpbin-auth-policy
spec:
  action: ALLOW
  selector:
    matchLabels:
      app: httpbin
  rules:
    - from:
        - source:
            namespaces: ["app"]
      to:
        - operation:
            methods: ["GET", "HEAD"]
            paths: ["/get"]
```

Apply the policy and test `/get` from a pod running in `app`.

***

## 7. DENY-all pattern and rule precedence

A deny-all policy example:

auth\_deny\_all.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  action: DENY
  rules:
    - {}
```

Important behavior to remember:

* DENY policies are evaluated before ALLOW policies. If a DENY matches, the request is rejected even if an ALLOW would also match.
* A broad deny-all in the same scope will block traffic unless you remove it or more specifically scope other policies.

If you need to restore access after applying a deny-all, delete it:

```bash theme={null}
kubectl delete -f auth_deny_all.yaml
# authorizationpolicy.security.istio.io "deny-all" deleted
```

### Per-workload deny example (target productpage only)

Instead of denying cluster-wide, target a specific workload via `selector`:

auth\_deny\_product.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all-product
spec:
  selector:
    matchLabels:
      app: productpage
  action: DENY
  rules:
    - {}
```

Apply it:

```bash theme={null}
kubectl apply -f auth_deny_product.yaml
# authorizationpolicy.security.istio.io/deny-all-product created
```

Now calls to productpage will return 403, while other services (e.g., httpbin) remain accessible:

```bash theme={null}
kubectl exec -ti test -n app -- curl --head http://productpage.default.svc:9080/productpage
# HTTP/1.1 403 Forbidden
kubectl exec -ti test -n app -- curl --head http://httpbin.default.svc:8000/get
# HTTP/1.1 200 OK
```

View active policies:

```bash theme={null}
kubectl get authorizationpolicies.security.istio.io -A
# NAMESPACE  NAME                 ACTION AGE
# default    deny-all-product     DENY   22s
# default    httpbin-auth-policy  ALLOW  33m
```

<Callout icon="lightbulb">
  Deny rules are evaluated before allow rules. If both DENY and ALLOW match a request, the DENY takes precedence. Use targeted DENY rules (by selector, namespace, port, or path) rather than a broad deny-all unless you intend to explicitly allow everything else.
</Callout>

***

## Summary table — useful Istio security resources

| Resource Type              | Purpose                                           | Example / Notes                                                      |
| -------------------------- | ------------------------------------------------- | -------------------------------------------------------------------- |
| PeerAuthentication         | Configure mTLS mode (DISABLE, PERMISSIVE, STRICT) | `PeerAuthentication` in `istio-system` to enable STRICT cluster-wide |
| AuthorizationPolicy        | Allow/deny/AUDIT/CUSTOM for workload access       | `AuthorizationPolicy` with `selector`, `from`, `to`, `when`          |
| ServiceAccount / Principal | Identities used in `from.source.principals`       | Use `cluster.local/ns/<ns>/sa/<sa>` for principals                   |
| Operation attributes       | Filter by HTTP method/path/port                   | `to.operation.methods`, `to.operation.paths`, `to.operation.ports`   |

***

## Reference and additional resources

<Frame>
  <img alt="The image shows a webpage from the Istio documentation focused on &#x22;Authorization,&#x22; detailing various access control methods for Istio services. It includes links for setting up access controls like HTTP traffic, TCP traffic, and JWT tokens." />
</Frame>

The Istio AuthorizationPolicy API supports:

* Scoping by workload (`selector.matchLabels`)
* `from` (source: namespaces, principals, service accounts)
* `to` (operation: methods, paths, ports)
* `when` (conditions based on request attributes, JWT claims)
* Actions: `ALLOW`, `DENY`, `AUDIT`, `CUSTOM` (`ALLOW` and `DENY` are most commonly used)

For authoritative documentation and examples, see the Istio Authorization Policy reference:

* [https://istio.io/latest/docs/reference/config/security/authorization-policy/](https://istio.io/latest/docs/reference/config/security/authorization-policy/)

<Frame>
  <img alt="The image shows a webpage from Istio's documentation discussing the &#x22;Authorization Policy,&#x22; which involves access control on workloads in the mesh. It outlines the use of CUSTOM, DENY, and ALLOW actions for access control." />
</Frame>

***

## Key takeaways

* Authentication (mTLS) establishes identity; authorization decides what that identity may do.
* AuthorizationPolicy is powerful but can be subtle. Pay attention to:
  * Rule scope (namespace-level vs workload `selector`)
  * Verb vs method differences (e.g., `GET` vs `HEAD`)
  * `DENY` precedence over `ALLOW`
  * Warnings about `DENY` rules with only HTTP attributes and their potential effect on TCP traffic
* Practice common patterns: allow-by-namespace, allow-by-service-account, deny-by-path, and per-workload deny to build confidence for production and certification scenarios.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/a1c6e62c-1037-47a6-8ed9-d7cda24ad89b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/4720e4dc-a793-4ae5-945d-1f639d5b6612" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Introduction/page

Overview of Istio Zero Trust for workloads, covering PeerAuthentication, mTLS, AuthorizationPolicy, policy interactions, and ambient mode implications.

This brief—but important—lesson introduces Zero Trust Architecture in the context of Istio and covers authentication and authorization for workloads.

We'll start by clarifying what Zero Trust means for workloads and how Istio's `PeerAuthentication` resource is used to implement it. Then we'll examine how encrypted traffic is handled and how authentication and encryption interact.

<Frame>
  <img alt="The image lists four objectives related to Istio: introducing Zero-Trust Architecture, exploring authentication resources, explaining encrypted traffic handling, and discussing authorization after authentication." />
</Frame>

After authentication, the natural follow-up is: what can an authenticated identity do? Istio's `AuthorizationPolicy` answers that by letting you define fine-grained allow/deny rules for workloads. We'll explain common policy patterns, the kinds of rules you can write, and the complexity that arises when multiple policies interact.

You should expect three core questions around authentication and authorization; mastering these will be important for understanding how Istio secures traffic between workloads.

Finally, we'll discuss how Istio's ambient mode interacts with security resources. Ambient mode material is useful to understand modern Istio deployments, although it is not required for the exam objectives.

<Callout icon="lightbulb">
  This lesson focuses on concepts and configurations for Istio authentication and authorization. Ambient mode details are included for completeness but are not required for the exam.
</Callout>

What you'll learn in this lesson:

* Why Zero Trust matters for workloads and how Istio implements it.
* How `PeerAuthentication` and mTLS control workload authentication and encryption.
* How `AuthorizationPolicy` enforces what authenticated identities are allowed to do.
* How authentication and authorization interact, and patterns to avoid policy conflicts.
* A brief overview of Istio Ambient mode and its relationship with these resources.

Quick reference table of core resources:

| Resource              | Purpose                                                                                     | Where to learn more                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `PeerAuthentication`  | Configure peer (client-to-server) authentication and mTLS modes for workloads               | [Istio PeerAuthentication docs](https://istio.io/latest/docs/reference/config/security/peer_authentication/)   |
| `AuthorizationPolicy` | Define allow/deny rules for workload access based on identity, request attributes, and more | [Istio AuthorizationPolicy docs](https://istio.io/latest/docs/reference/config/security/authorization-policy/) |

Expect to answer these three core questions by the end of this lesson:

1. How does Istio establish and enforce workload identity and mutual TLS (mTLS)?
2. How does encrypted traffic (mTLS) affect authentication configuration and policy decisions?
3. Once a request is authenticated, how do you express and scope authorization rules with `AuthorizationPolicy`?

If you're ready, grab a cup of coffee and let's begin the lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/1bef1776-edd7-44d5-99db-28b02fee0f36" />
</CardGroup>
