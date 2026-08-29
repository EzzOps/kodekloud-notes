# Connectivity TLS in Kubernetes

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Connectivity-TLS-in-Kubernetes/page

Learn to encrypt and authenticate traffic in a Kubernetes cluster using TLS, covering keys, certificates, and best practices for mutual TLS implementation.

In this guide, you’ll learn how to encrypt and authenticate all traffic in a Kubernetes cluster using TLS. We’ll cover:

* The role of keys, certificates, and Certificate Authorities (CAs)
* TLS requirements for Kubernetes control plane and data plane
* Mapping server and client certificates to Kubernetes components
* Best practices for generating and signing certificates

By the end, you’ll understand how to implement mutual TLS (mTLS) across every communication channel in your cluster.

***

## 1. TLS Fundamentals: Keys, Certificates, and CAs

Before diving into Kubernetes-specific details, let’s recap the core concepts:

* **Public/Private Key Pair**\
  Each entity (server or client) generates a private key and a corresponding public key.

* **Server Certificates** (`server.crt`, `server.key`)\
  Used by services exposing HTTPS endpoints.

* **Client Certificates** (`client.crt`, `client.key`)\
  Prove a client’s identity to the server.

* **Certificate Authority (CA)** (`ca.crt`, `ca.key`)\
  Signs certificates and establishes a trust chain.

### Naming Conventions

<Callout icon="lightbulb">
  * Public certificates: use `.crt` or `.pem`
  * Private keys: use `.key` or include “key” in the filename
  * Examples: `apiserver.crt` + `apiserver.key`, `client.pem`, `client-key.pem`
</Callout>

***

## 2. TLS Requirements in Kubernetes

All Kubernetes communications—intra-cluster or external—must be both encrypted and authenticated:

1. **Server Certificates**\
   Each service that exposes an HTTPS endpoint (API server, etcd, kubelet).

2. **Client Certificates**\
   Every client connecting to those services (`kubectl`, system components).

Mutual TLS ensures that both sides verify each other’s identity and encrypt data in transit.

***

## 3. Certificate Assignments for Kubernetes Components

### 3.1 Server-Side Certificates

| Component        | Certificate File  | Key File          |
| ---------------- | ----------------- | ----------------- |
| API Server       | `apiserver.crt`   | `apiserver.key`   |
| etcd Server      | `etcd-server.crt` | `etcd-server.key` |
| Kubelet (worker) | `kubelet.crt`     | `kubelet.key`     |

```bash theme={null}
