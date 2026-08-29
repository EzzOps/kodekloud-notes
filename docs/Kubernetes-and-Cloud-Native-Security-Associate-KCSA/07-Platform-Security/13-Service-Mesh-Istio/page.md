# Example: Enforce strict mTLS namespace-wide
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: your-namespace
spec:
  mtls:
    mode: STRICT
EOF
```

1. Sidecar A presents its certificate to Sidecar B.
2. Sidecar B verifies the certificate against Istio’s root CA.
3. Both proxies agree on encryption keys.
4. Secure channel established—data is encrypted, authenticated, and authorized.

## References

* [Istio Security Concepts](https://istio.io/latest/docs/concepts/security/)
* [Envoy Proxy Architecture](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/overview)
* [SPIFFE and SPIRE](https://spiffe.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/014b7517-1b8b-4f36-913a-6f0cc19fc7db)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/41f39dd4-0f29-4d3f-9f10-8143bb6fc65d)


# Service Mesh Istio

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Service-Mesh-Istio/page

This guide explores Istio, an open-source service mesh, covering its architecture, core components, and practical examples for microservices management.

In this guide, we'll dive into Istio, the leading open-source service mesh. You’ll learn how Istio works, explore its architecture, and review its essential components—all with practical examples and best practices.

## What Is Istio?

Istio is a free, open-source service mesh that secures, connects, and observes microservices. It integrates seamlessly with [Kubernetes](https://kubernetes.io/) and virtual machine-based workloads to provide:

* Fine-grained traffic control and routing
* Automatic mutual TLS for service identity and encryption
* Telemetry collection and distributed tracing
* Policy enforcement and rate limiting

Istio is backed by industry leaders and supported by major cloud providers, making it ideal for scalable, production-grade deployments.

## Istio Architecture

Istio decouples service-to-service communication concerns from application code using a two-plane architecture:

| Plane         | Description                                                                                    |
| ------------- | ---------------------------------------------------------------------------------------------- |
| Control Plane | Manages configurations, policies, and certificates via a unified binary, Istiod.               |
| Data Plane    | Consists of Envoy sidecar proxies that enforce policies, route traffic, and collect telemetry. |

### Control Plane: Istiod

Originally built from Pilot, Citadel, and Galley, Istio’s control plane is now a single binary: **Istiod**. It handles:

* Service discovery and traffic configuration
* Certificate issuance and rotation (mutual TLS)
* Configuration validation and distribution

> **lightbulb** Istiod simplifies management by consolidating multiple components into one. Upgrading or securing Istiod affects all control-plane functionality.

### Data Plane: Envoy Sidecars

Every workload (e.g., a Kubernetes Pod) runs an **Envoy** sidecar proxy alongside the application container. Envoy handles:

* Traffic routing, retries, and failover
* Secure communication with automatic TLS
* Metrics and logs for telemetry and monitoring

## Core Istio Components

### Envoy Sidecar Proxy

Envoy is a high-performance proxy that intercepts inbound and outbound service traffic. Key features:

```bash theme={null}
