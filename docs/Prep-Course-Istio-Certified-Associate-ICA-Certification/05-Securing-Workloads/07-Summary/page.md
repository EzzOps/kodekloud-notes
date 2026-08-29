# Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Summary/page

Explains Istio Zero Trust in Kubernetes, enforcing mTLS with PeerAuthentication, using AuthorizationPolicy for application layer access control, and contrasting Istio with Kubernetes NetworkPolicy.

This lesson reviewed Zero Trust architecture and how Istio enforces it in Kubernetes clusters. Key takeaways are:

* Always verify identity first, regardless of traffic origin. In Istio this is enforced by a `PeerAuthentication` resource applied either mesh-wide (global) or scoped to a specific namespace.
* Mutual TLS (mTLS) is negotiated and enforced by the data-plane proxy. In sidecar mode this is the Envoy sidecar injected into the workload. In Istio Ambient mode, TLS is handled by the ambient dataplane (ztunnel / ambient dataplane) and requires different labels and deployment patterns, but it still authenticates traffic to workloads.
* Authentication (who is making the request) is only the first step. After a client is authenticated, you must decide what that client is allowed to do. Istio `AuthorizationPolicy` objects define application-layer permissions (allow/deny) and evaluate attributes like principals, HTTP methods, paths, and other metadata.

<Frame>
  <img alt="The image outlines four objectives related to networking policies, focusing on authorization, Kubernetes network policies, Istio policies, and traffic handling layers. Each point is numbered and briefly described, emphasizing policy enforcement and control levels." />
</Frame>

Operational details and practical guidance

* Kubernetes `NetworkPolicy` resources operate at OSI layers 3 and 4 (network and transport). They control IP-level and port-level connectivity.
* Istio `AuthorizationPolicy` objects operate primarily at layer 7 (application). They enable request-level controls based on attributes such as HTTP methods, paths (for example, `GET /api`), or other application-level metadata.
* If your cluster uses the ambient dataplane (ztunnel) and you only need basic L4 redirection across namespaces, ztunnel will handle that traffic steering. For L7 controls (path- or method-specific rules), a waypoint proxy must be deployed for the workload; without a waypoint proxy, L7 rules may not be enforced.

Example checklist to implement a basic Zero Trust posture in Istio:

1. Enforce mTLS with `PeerAuthentication` (mesh or namespace scope).
2. Use `AuthorizationPolicy` to grant/deny access at the application layer.
3. Prefer `serviceAccount` principals for clearer, auditable authorization bindings.
4. If using ambient mode and you need L7 controls, deploy a waypoint proxy and label the namespace appropriately.

Quick configuration examples

* Mesh-wide PeerAuthentication to enforce mTLS:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

* AuthorizationPolicy using a service account principal and HTTP method/path constraints:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-read-api
  namespace: my-app
spec:
  selector:
    matchLabels:
      app: my-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/frontend/sa/frontend-sa"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/*"]
```

Comparing Kubernetes NetworkPolicy vs Istio AuthorizationPolicy

|           Feature | Kubernetes `NetworkPolicy`                   | Istio `AuthorizationPolicy`                                           |
| ----------------: | -------------------------------------------- | --------------------------------------------------------------------- |
|        OSI layers | L3/L4 (IP/port)                              | L7 (HTTP/gRPC/attributes)                                             |
|       Typical use | Allow/block pod-to-pod traffic by CIDR/ports | Allow/deny requests based on principals, methods, paths               |
| Enforcement point | Kubernetes network plugin                    | Istio data-plane proxy (Envoy) or ambient dataplane + waypoint for L7 |
|          Best for | Coarse network segmentation                  | Fine-grained application authorization                                |

Links and references

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

> **lightbulb** Practical checklist: first enforce mTLS with a `PeerAuthentication`, then layer `AuthorizationPolicy` rules to grant or deny access. Use service accounts as principals for clearer, auditable authorization bindings where appropriate.

> **lightbulb** Exam note: Ambient mode specifics are less likely to be heavily tested on the Istio Certified Associate exam, but you should understand differences between sidecar and ambient dataplanes and when a waypoint proxy is required for L7 enforcement. Review the Istio docs and practice hands-on; practical exercises align closely with exam topics.

That concludes this section.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/43dff065-fb80-4139-a280-fa3b491ffd08)
