# Abort
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-route
spec:
  hosts:
    - ratings.prod.svc.cluster.local
  http:
    - route:
        - destination:
            host: ratings.prod.svc.cluster.local
            subset: v1
      fault:
        abort:
          percentage:
            value: 10.0
          httpStatus: 400

# Delay
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
    - reviews.prod.svc.cluster.local
  http:
    - match:
        - sourceLabels:
            env: prod
      route:
        - destination:
            host: reviews.prod.svc.cluster.local
            subset: v1
      fault:
        delay:
          percentage:
            value: 10.0
          fixedDelay: 5s
```

Best practices

* Start small: low percentages and short durations.
* Scope faults with `match` conditions to avoid broad impact.
* Monitor application and platform metrics (latency, error rates, SLOs) while testing.
* Validate fallbacks and circuit breakers before increasing fault intensity.
* Prefer running fault injection in staging or dedicated chaos environments before production.

Links and References

* [Istio Documentation](https://istio.io/latest/docs/) — official reference for VirtualService and fault injection.
* [Istio Service Mesh course](https://learn.kodekloud.com/user/courses/istio-service-mesh) — contextual learning resources.
* [Netflix Chaos Monkey](https://netflix.github.io/chaosmonkey/) — example of large-scale chaos engineering practices.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/7c3bd89f-cc7b-41d8-8265-25cfe0d44c4e)


# Summary

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Summary/page

Overview of Istio traffic management concepts including VirtualService DestinationRule mTLS gateways traffic mirroring fault injection and hardening

Well done — this was a long module. Take a moment to pat yourself on the back.

This lesson reviewed the key Istio traffic-management concepts you need for the Istio Service Mesh certification and practical production use. Below is a concise, structured summary to reinforce the most important points and help with exam preparation and real-world application.

## Sidecar proxy behavior and hardening

* Envoy sidecar proxies intercept inbound and outbound pod traffic. By default, outbound traffic can reach other services across the mesh.
* Use a `Sidecar` resource to restrict the set of outbound listeners and hosts for a workload. This hardens egress and reduces blast radius.
* Use `PeerAuthentication` to control workload mTLS. Setting `mode: STRICT` enforces mutual TLS for workloads covered by the policy.

> **lightbulb** `PeerAuthentication` has three modes (`DISABLE`, `PERMISSIVE`, `STRICT`). For strict mTLS enforcement, use `mode: STRICT`. Use a `Sidecar` resource when you need to limit which outbound hosts a workload can access.

Example PeerAuthentication (enforce mTLS):

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default-strict
spec:
  mtls:
    mode: STRICT
```

## VirtualService responsibilities

* `VirtualService` is the primary resource for advanced request-level routing:
  * Traffic splitting (weighted routing between subsets)
  * Retries and timeouts
  * Fault injection (delays and aborts)
  * Traffic mirroring (shadowing)
  * Header-based, path-based, and other rule-based routing
* Fault injection is configured inside `VirtualService` routes and can affect a percentage of traffic (e.g., delay 100ms for 50% of requests).

Example VirtualService snippet (traffic mirror):

```yaml theme={null}
http:
  - route:
      - destination:
          host: reviews
          subset: v1
        weight: 100
    mirror:
      host: reviews
      subset: v2
    mirrorPercent: 10
```

## DestinationRule responsibilities

* `DestinationRule` applies policies to traffic *after* routing decisions:
  * Subsets (used for versioned routing)
  * Load balancing settings
  * Connection pools and circuit breakers
  * TLS settings (e.g., client-side TLS, common-name)
* Circuit breaking and connection-pool limits belong in `DestinationRule`, not `VirtualService`.
* Define subsets in `DestinationRule` and then reference them from `VirtualService` to implement traffic shifting (e.g., 50/50 or 80/20 across v1/v2).

## Traffic mirroring (shadowing)

* Mirroring lets you send a copy of live requests to another service/version to test behavior under production load without impacting the primary response.
* Configure mirroring with `mirror` and `mirrorPercent` in a `VirtualService`.
* Use `DestinationRule` subsets when you need to mirror to a specific version.

## Gateways and exposure

* Use an Ingress Gateway to expose services to external clients. If a service is internal only, you can avoid adding an ingress gateway.
* Use an Egress Gateway to centralize and control egress traffic from the mesh (useful for TLS origination, logging, consistent egress IPs, and policy enforcement).
* `ServiceEntry` allows external services to be added to Istio’s service registry so they can be governed by Istio policies and telemetry.

## Fault injection (conceptual)

* Delays: add a fixed delay (e.g., 100ms) to a percentage of requests to test latency handling.
* Aborts: return an HTTP error code (e.g., 503) for a percentage of requests to test error handling and retries.
* Use fault injection to validate resilience, circuit breaking, and observability (tracing/metrics).

<Frame>
  <img alt="The image presents a list of objectives related to application performance, including rate limiting, intentional failures, fixed delays, and abort injections. It is visually organized with colorful numbered markers alongside each objective." />
</Frame>

## Rate limiting and connection limits

* Use `DestinationRule` (and Envoy settings) to configure connection pools and circuit-breaking thresholds (concurrent connections, pending requests).
* Request-rate limiting (RPS) is typically implemented using Envoy filters, external rate-limit services, or specific Istio extensions rather than `DestinationRule` alone.
* Circuit breaking is critical to prevent cascading failures in microservice architectures.

## Waypoint proxies and HTTPRoute (Gateway API)

* Waypoint proxies centralize traffic capture for workloads and can integrate with Gateway API resources (e.g., `HTTPRoute`) for advanced routing and observability.
* These capabilities are valuable for large meshes and progressive adoption patterns but are less likely to be a heavy focus on the certification beyond basic installation and labels.

> **warning** If you use Ambient mode or waypoint proxies, ensure namespaces are labeled correctly and the waypoint proxy is installed where required. Missing labels or waypoint installation will break expected behavior.

## Quick reference: Istio traffic-management objects

| Resource Type              | Purpose                                                        | Example / Where to configure                 |
| -------------------------- | -------------------------------------------------------------- | -------------------------------------------- |
| `VirtualService`           | Advanced routing, traffic shifting, mirroring, fault injection | Configure routes, weights, `mirror`, `fault` |
| `DestinationRule`          | Post-routing policies: subsets, LB, TLS, circuit breaking      | Define `subsets`, `trafficPolicy`            |
| `PeerAuthentication`       | mTLS mode for workloads                                        | `mode: STRICT` to enforce mTLS               |
| `Sidecar`                  | Limit outbound listeners/hosts for a workload                  | Bound egress to specific services            |
| `ServiceEntry`             | Bring external services into Istio registry                    | Define external hosts and ports              |
| `Gateway` / Ingress/Egress | Expose mesh to outside or control outgoing traffic             | Configure hosts, ports, and exposed services |

## Exam tip and coverage

* Be comfortable with: `VirtualService`, `DestinationRule`, `PeerAuthentication`, `Sidecar`, `ServiceEntry`, and Ingress/Egress Gateways.
* Key features to understand: fault injection (`VirtualService`), circuit breaking (`DestinationRule`), traffic shifting (`VirtualService` + `DestinationRule` subsets), traffic mirroring (`VirtualService`), and external service access (`ServiceEntry`).
* Know where to configure policies (routing vs. post-routing policies) and how mTLS is enforced in Istio.

Further reading:

* [Istio Traffic Management Concepts](https://istio.io/latest/docs/concepts/traffic-management/)
* [Istio Peer Authentication (mTLS)](https://istio.io/latest/docs/tasks/security/authentication/peer-auth/)
* [Istio Gateways and ServiceEntry docs](https://istio.io/latest/docs/reference/config/networking/)

Great job getting through the material. Take a break — you deserve it. I’ll see you in the next section where we’ll continue with the remaining topics.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/ec420b2a-4212-4fab-ba1d-2366edc80bb9)
