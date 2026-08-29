# Authorizaton

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Authorizaton/page

Explains Istio AuthorizationPolicy for L7 access control with ALLOW and DENY examples, JWT claim checks, selectors, and contrasts with Kubernetes NetworkPolicy

Think of Istio authorization like a ticketed event: authentication (mTLS / JWT verification) is the identity check at the gate, while authorization is the assigned seating—who can access which services, on which paths and methods. After workloads are authenticated, Istio authorization policies determine what each workload is allowed to do inside the mesh.

<Frame>
  <img alt="The image illustrates an Istio authorization setup within a Kubernetes cluster, depicting a service mesh across three nodes. Each node hosts an application and service, with Envoy proxies managing communication and authorization between services." />
</Frame>

Example scenario: the inventory service can POST to the shoes service on port 80 but cannot GET the user service on port 80. All services have Envoy sidecars injected, so authentication has already occurred. Authorization policies then allow or deny requests according to rules you declare.

<Frame>
  <img alt="The image illustrates an authorization example using a proxy architecture with services for inventory, shoes, and users, showing request flows and authorization outcomes." />
</Frame>

## AuthorizationPolicy: basic examples

Authorization policies are custom resources (`AuthorizationPolicy`) in Istio. The examples below demonstrate common patterns: ALLOW, DENY, and a more expressive policy that checks identity and JWT claims.

Example: allow POST requests to any workload in the `payments` namespace coming from workloads in the `app` namespace:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payments-allow-pol
  namespace: payments
spec:
  action: ALLOW
  rules:
  - from:
    - source:
        namespaces: ["app"]
    to:
    - operation:
        methods: ["POST"]
```

Example: deny GET requests from the `app` namespace to the `/credit-cards-info` path in the `payments` namespace:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payments-deny-pol
  namespace: payments
spec:
  action: DENY
  rules:
  - from:
    - source:
        namespaces: ["app"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/credit-cards-info"]
```

Advanced example: allow requests to the `payments` service when the request comes from either:

* the specific service account `cluster.local/ns/identity/sa/app` (a principal), OR
* any workload in the `app` namespace,

and allow GET to `/data` and POST to `/purchases` only when the JWT issuer (`request.auth.claims[iss]`) equals `https://accounts.google.com`:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payments-allow-pol
  namespace: payments
spec:
  action: ALLOW
  rules:
  - selector:
      matchLabels:
        app: payments
    from:
    - source:
        principals: ["cluster.local/ns/identity/sa/app"]
    - source:
        namespaces: ["app"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/data"]
    - operation:
        methods: ["POST"]
        paths: ["/purchases"]
    when:
    - key: request.auth.claims[iss]
      values: ["https://accounts.google.com"]
```

> **lightbulb** Important: Entries under `from:` are evaluated as OR between list items. If you combine multiple conditions under a single `source:` block instead of listing them separately, you may unintentionally require all conditions to be true (AND).

You can list multiple `operation` blocks under `to:` to allow different method/path combinations for the same rule. Use `selector` to scope policies to specific workloads (by labels) in the namespace.

## Istio Authorization vs Kubernetes NetworkPolicy

Istio AuthorizationPolicy enforces application-layer (L7) access control with identity and request attributes (methods, paths, JWT claims). Kubernetes NetworkPolicy enforces network/transport-layer (L3/L4) rules like pod selectors, namespaces, IPBlocks, and ports.

| Feature                                  |                  Kubernetes NetworkPolicy | Istio AuthorizationPolicy                          |
| ---------------------------------------- | ----------------------------------------: | -------------------------------------------------- |
| OSI layer                                |               L3/L4 (Network / Transport) | L7 (Application)                                   |
| Can inspect HTTP methods/paths?          |                                        No | Yes                                                |
| Identity-aware (service accounts / JWT)? |                                        No | Yes                                                |
| Example use case                         | Allow pod-to-pod traffic on TCP port 8080 | Allow GET `/api` only for certain service accounts |
| Example (command)                        |     `kubectl apply -f networkpolicy.yaml` | `kubectl apply -f authorizationpolicy.yaml`        |

Example NetworkPolicy that allows traffic to pods labeled `app: payments` from the `app` namespace on TCP port 8080:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payments-allow-pol
  namespace: payments
spec:
  podSelector:
    matchLabels:
      app: payments
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              app: app
      ports:
        - protocol: TCP
          port: 8080
```

Example Istio AuthorizationPolicy that enforces a GET to `/api` on port 8080 and only allows requests from the `app` namespace:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payments-allow-pol
  namespace: payments
spec:
  action: ALLOW
  rules:
  - selector:
      matchLabels:
        app: payments
    from:
    - source:
        namespaces: ["app"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api"]
        ports: ["8080"]
```

Because Istio enforces policies at the Envoy sidecar (L7), you can implement fine-grained, identity-aware, zero-trust access control (least privilege). Policies are declarative, GitOps-friendly, and auditable.

<Frame>
  <img alt="The image is a slide titled &#x22;Why Use Authorization Policies?&#x22; showing four benefits: fine-grained access control, zero-trust architecture, identity-based access, and declarative policies." />
</Frame>

## Fields and examples you’ll see on the exam

Here are common source fields and fragments you may encounter in questions or practical tasks—study the full reference in the Istio docs:

```yaml theme={null}
