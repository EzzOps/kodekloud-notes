# Service Mesh Istio Security Architecture

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Service-Mesh-Istio-Security-Architecture/page

This article explores Istio’s service mesh security, covering certificate issuance, mutual TLS, and authentication and authorization policies for microservices.

In this article, we explore how Istio’s service mesh delivers end-to-end security for microservices. You’ll learn how Istio issues certificates, enforces mutual TLS (mTLS), and applies authentication and authorization policies across your data plane.

> **lightbulb** The following diagram illustrates Istio’s security architecture. It shows secure service-to-service communication via Envoy sidecars, how ingress and egress gateways handle external traffic, and how the istiod control plane manages certificates and policies.

![The image illustrates the Istio Security Architecture, showing the interaction between services, proxies, and the control plane with secure communication protocols like mTLS. It highlights components such as Ingress, Egress, and the istiod control plane managing certificates and policies.](https://kodekloud.com/kk-media/image/upload/v1752880900/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Service-Mesh-Istio-Security-Architecture/istio-security-architecture-diagram.jpg)

## 1. istiod Control Plane as Certificate Authority

At the heart of Istio security, the **istiod** component serves as a built-in certificate authority (CA). It:

* Issues, rotates, and revokes workload certificates and private keys
* Manages SPIFFE-based identities for workloads
* Provides a configuration API server for distributing security policies

### How Certificate Issuance Works

1. When a new workload starts, its Envoy sidecar contacts the local Istio agent.
2. The agent requests a signed certificate and private key from istiod.
3. Istiod signs the CSR (Certificate Signing Request) and returns credentials.
4. The proxy establishes mTLS connections to other services using these certs.

## 2. Authentication, Authorization, and Secure Naming

Istio’s configuration API server (part of istiod) pushes the following policies to each Envoy proxy:

* **Authentication Policies**: Define which workloads require mTLS or JWT verification.
* **Authorization Policies**: Control access based on attributes like `source.principal` or `request.headers`.
* **Secure Naming**: Ensures that only services with valid SPIFFE identities can communicate.

By enforcing policies at each hop, Istio builds a **defense-in-depth** model rather than relying on perimeter security alone.

## 3. Data Plane Proxies: Sidecars, Ingress, and Egress Gateways

All traffic—both internal and external—flows through Envoy proxies:

| Component       | Role                                                 | Example Configuration                                   |
| --------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| Sidecar Proxy   | Intercepts and secures pod-to-pod traffic            | `sidecar.istio.io/inject: "true"`                       |
| Ingress Gateway | Terminates external traffic, applies edge policies   | `apiVersion: networking.istio.io/v1beta1` ingress specs |
| Egress Gateway  | Controls and monitors external egress, policy checks | `apiVersion: networking.istio.io/v1beta1` egress specs  |

### Traffic Flow

* **Internal**: Service A → its Envoy sidecar (mTLS) → Service B’s sidecar → Service B
* **Ingress**: External client → Ingress Gateway → Destination sidecar
* **Egress**: Service sidecar → Egress Gateway → External service

## 4. Mutual TLS Handshake

```bash theme={null}
