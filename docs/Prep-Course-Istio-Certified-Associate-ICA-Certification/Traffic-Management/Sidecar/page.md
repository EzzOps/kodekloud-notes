# Sidecar

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Sidecar/page

Explains Istio Envoy sidecars, automatic injection, configuring Sidecar resources to control egress/ingress, and using PeerAuthentication to enforce mTLS for namespaces and workloads.

Envoy sidecars (injected by Istio) provide security, observability, and traffic-management features for workloads. If a namespace is not labeled for Istio automatic sidecar injection, its pods will not receive an Envoy proxy and therefore will not automatically benefit from mesh features such as mTLS, telemetry, retries, mirroring, and fault injection.

<Frame>
  <img alt="The image is a diagram illustrating Istio's automatic sidecar injection within a Kubernetes control plane, showing the interaction between different nodes and services via Envoy proxies." />
</Frame>

When automatic injection is enabled for a namespace, Istio inserts a default Envoy sidecar for each pod. The default sidecar behavior is permissive: it intercepts traffic and allows both mTLS and plaintext traffic unless you explicitly enforce mTLS via PeerAuthentication.

<Frame>
  <img alt="The image illustrates Istio's sidecar behavior where Envoy proxies provide ingress and egress listeners for services A, B, C, and D, enabling basic mesh features." />
</Frame>

Default sidecar responsibilities include:

* Intercepting inbound and outbound traffic for the workload
* Enforcing mTLS if configured (not enabled by default)
* Providing traffic-management primitives: load balancing, timeouts, retries, logging, circuit breaking, rate limiting, etc.

<Frame>
  <img alt="The image outlines the behavior of a sidecar proxy, detailing aspects like traffic management by Envoy Proxy, egress policies, mTLS support, and built-in traffic features." />
</Frame>

<Callout icon="lightbulb">
  Enable automatic sidecar injection for namespaces that should take advantage of Istio features. You can label a namespace with `istio-injection=enabled` before creating pods to have Envoy injected automatically.
</Callout>

Controlling sidecar behavior per namespace or per workload is useful when you need fine-grained network segmentation. For example, you may wish to restrict the payments namespace so its workloads only talk to the app namespace and `istio-system`, and deny all other egress.

<Frame>
  <img alt="The image is a diagram representing a Kubernetes architecture integrated with Istio, showing nodes, services, and communication paths with secure, blocked, and successful connections." />
</Frame>

## Restricting egress with a Sidecar resource

To override the default (broad) sidecar behavior for a namespace, create a `Sidecar` resource that defines allowed egress hosts. The example below restricts the `payments` namespace so workloads can only call:

* workloads in the same namespace (`./*`)
* workloads in the `app` namespace (`app/*`)
* workloads in `istio-system` (`istio-system/*`)

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: payments
spec:
  egress:
  - hosts:
    - "./*"
    - "app/*"
    - "istio-system/*"
```

Notes on host patterns:

* `./*` matches all services in the same namespace as the Sidecar (i.e., `payments`).
* `app/*` matches all services in the `app` namespace.
* `istio-system/*` matches services in the Istio control-plane namespace.

Apply the Sidecar with `kubectl apply -f sidecar.yaml` (or your preferred deployment method). Only workloads in the `payments` namespace that have an Envoy sidecar will be affected by this config.

<Callout icon="warning">
  A `Sidecar` or `PeerAuthentication` resource created in a namespace without Envoy-injected workloads will have no practical effect. Ensure the namespace is labeled for Istio injection or that pods were injected manually.
</Callout>

## Enforcing mTLS with PeerAuthentication

Istio’s default PeerAuthentication mode is permissive, which means workloads accept either mTLS or plaintext connections. To require mTLS for a namespace, create a `PeerAuthentication` resource and set `mtls.mode: STRICT`. Example for the `app` namespace:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: app
spec:
  mtls:
    mode: STRICT
```

With this policy:

* Any client calling workloads in the `app` namespace must use mTLS.
* Clients without an Envoy sidecar (or not participating in the mesh) will be unable to connect.

Ensure both client and server namespaces have injection enabled (or are otherwise mesh-enabled) if you expect mutual TLS traffic.

## Per-workload Sidecar example

You can scope Sidecar resources to specific workloads by using `workloadSelector`. The following example targets pods with label `app: ratings` in the `bookinfo` namespace. It configures a custom ingress port (9080 bound to a UDS) and restricts egress to `bookinfo/*` and `istio-system/*` on port 9080.

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: ratings
  namespace: bookinfo
spec:
  workloadSelector:
    labels:
      app: ratings
  ingress:
  - port:
      number: 9080
      protocol: HTTP
    name: ratings
    defaultEndpoint: unix:///var/run/someuds.sock
  egress:
  - port:
      number: 9080
      protocol: HTTP
    name: egresshttp
    hosts:
    - "bookinfo/*"
    - "istio-system/*"
```

This configuration:

* Accepts HTTP traffic on port 9080 and forwards it to the workload via the specified Unix Domain Socket.
* Limits egress to the `bookinfo` and `istio-system` namespaces on that same port.

## Quick reference

| Resource           | Purpose                                                                        | Example snippet                                              |
| ------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| Sidecar            | Limit ingress/egress and define port-level behavior per namespace or workload  | `spec.egress: - hosts: - "./*" - "app/*" - "istio-system/*"` |
| PeerAuthentication | Configure mTLS mode (DISABLE / PERMISSIVE / STRICT) at namespace or mesh level | `spec: mtls: mode: STRICT`                                   |

## Where to find more details

* Istio Sidecar reference: [https://istio.io[AWS_SECRET_ACCESS_KEY]/sidecar/](https://istio.io[AWS_SECRET_ACCESS_KEY]/sidecar/)
* Istio PeerAuthentication reference: [https://istio.[AWS_SECRET_ACCESS_KEY]/peer\_authentication/](https://istio.[AWS_SECRET_ACCESS_KEY]/peer_authentication/)

This is an important topic for the exam—know how to:

* Identify when a namespace has injection enabled,
* Read and author `Sidecar` resources to restrict egress/ingress,
* Enforce mTLS via `PeerAuthentication`.

In the next section/demonstration, we’ll apply these resources and observe their effects in a live cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/22f21815-d96e-43d7-b654-21ad88095325" />
</CardGroup>
