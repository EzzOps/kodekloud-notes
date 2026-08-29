# Service Mesh

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Explain-Consul-Architecture/Service-Mesh/page

This article explains how Consul Service Mesh secures microservices communication using sidecar proxies, mTLS encryption, and access control policies.

Service meshes provide a dedicated infrastructure layer to secure, observe, and control traffic between microservices. By leveraging sidecar proxies, mutual TLS (mTLS) encryption, and fine-grained policies, Consul Service Mesh ensures encrypted, authenticated communication without any changes to application code.

## What Is a Service Mesh?

A service mesh decouples network-level logic from application logic by injecting lightweight proxies alongside each service instance. These proxies handle:

* Traffic encryption and decryption
* Service discovery and load balancing
* Access control policies

## Sidecar Architecture and mTLS

In Consul Service Mesh, every service instance runs with an Envoy sidecar proxy. Envoy intercepts all inbound/outbound requests, transparently handling certificate management, TLS handshakes, and routing.

![The image is a slide about "Service Mesh," highlighting its role in enabling secure communication between services using mTLS, sidecar architecture, and defined access control.](https://kodekloud.com/kk-media/image/upload/v1752877864/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Service-Mesh/service-mesh-secure-communication-slide.jpg)

### Key Benefits of Consul Service Mesh

| Feature                        | Benefit                 | Description                                                      |
| ------------------------------ | ----------------------- | ---------------------------------------------------------------- |
| mTLS Encryption                | Secure by default       | All traffic is encrypted using certificates issued by Consul CA. |
| Sidecar Proxies (Envoy)        | Transparent integration | Proxies handle TLS handshakes and routing without code changes.  |
| Intentions (Access Control)    | Fine-grained policies   | Define which services can or cannot communicate.                 |
| Automatic Certificate Rotation | Zero-touch security     | Consul issues and rotates certificates automatically.            |

> **lightbulb** Consul’s built-in Certificate Authority (CA) automatically issues, renews, and revokes TLS certificates, reducing operational overhead.

## Defining Access Control with Intentions

Consul uses **intentions** to enforce service-to-service policies. An intention is a rule that explicitly `allow`s or `deny`s traffic between two services.

| Intention Type | Effect          | CLI Example                                    |
| -------------- | --------------- | ---------------------------------------------- |
| Allow          | Permits traffic | `consul intention create web payment`          |
| Deny           | Blocks traffic  | `consul intention create -deny search payment` |

```bash theme={null}
