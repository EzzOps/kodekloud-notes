# consul.hcl
encrypt = "BASE64_ENCRYPTION_KEY"
```

### Enable the ACL System

By default, ACLs are disabled. Turning them on enforces policies for KV operations and API endpoints:

```json theme={null}
{
  "acl": {
    "enabled": true,
    "default_policy": "deny",
    "down_policy": "extend-cache"
  }
}
```

<Frame>
  ![The image is a slide titled "Consul Security/Threat Model," discussing the Gossip Protocol and ACL System, highlighting their features and objectives. It includes colorful text and a pixelated design on the right side.](https://kodekloud.com/kk-media/image/upload/v1752877937/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Consul-SecurityThreat-Model/consul-security-threat-model-gossip-acl.jpg)
</Frame>

***

## 2. Consul Agent TLS

Securing agent-to-agent communication is critical when running in untrusted networks or across cloud regions. Consul agents can use TLS certificates for both RPC (Raft, Serf) and the HTTP API.

Add the following to each agent’s JSON or HCL configuration:

```json theme={null}
{
  "tls_cert_file": "/path/to/agent.crt",
  "tls_key_file":  "/path/to/agent.key",
  "tls_ca_file":   "/path/to/ca.pem"
}
```

<Callout icon="lightbulb">
  Consul will verify peer hostnames on incoming connections. Ensure your certificate’s Common Name (CN) or SAN matches the agent’s advertised address.
</Callout>

***

## 3. Mutual TLS (mTLS)

mTLS provides both encryption and peer authentication, forming the backbone of Consul’s Service Mesh:

* Services present client certificates issued by a trusted CA.
* Peers validate each other’s certificates before establishing an encrypted channel.
* Identity information (e.g., service name) is embedded in the certificate and used for authorization.

<Frame>
  ![The image is a slide titled "Consul Security/Threat Model," detailing features of the Consul Agent and mTLS for encrypting communications and validating authenticity.](https://kodekloud.com/kk-media/image/upload/v1752877939/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Consul-SecurityThreat-Model/consul-security-threat-model-mtls.jpg)
</Frame>

***

## 4. Certificate Authority Integration

Consul can act as its own CA or delegate certificate issuance to an external CA such as HashiCorp Vault. Centralized certificate management simplifies rotation and revocation.

### Using the Built-in CA

```bash theme={null}
# Generate server cert
consul tls cert create -server

# Generate client cert
consul tls cert create -client

# Generate CLI cert
consul tls cert create -cli
```

### Delegating to Vault (or other CA)

```hcl theme={null}
# consul.hcl
certificate_authority = {
  provider = "vault"
  options = {
    address = "https://vault.example.com"
    token   = "VAULT_TOKEN"
    # additional Vault settings…
  }
}
```

<Callout icon="lightbulb">
  When integrating with Vault, configure ACL tokens and policies to allow Consul to request and renew certificates automatically.
</Callout>

***

By enabling Gossip encryption, the ACL system, agent TLS, mTLS, and CA integration, you secure every layer of Consul’s communication—from cluster membership and Raft consensus to HTTP APIs and service-to-service traffic in the mesh.

## Links and References

* [Consul Security Model](https://www.consul.io/docs/enterprise/security)
* [HashiCorp Vault PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki)
* [Consul ACLs](https://www.consul.io/docs/acl)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/777a613c-50bc-474c-9597-aec67eec52e0/lesson/63487456-c2ac-4fb8-8f18-1be21cbfe680" />
</CardGroup>


# Objective 7 Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Agent-Communication/Objective-7-Section-Overview/page

This lesson covers securing communication between Consul agents, including the security model, TLS certificate types, and encryption settings for a secure datacenter.

In this lesson, we’ll cover how to secure communication between Consul agents in a datacenter. You will learn:

1. Consul security model and threat assumptions
2. TLS certificate types: server CA, client certificates, and more
3. TLS encryption settings to fully lock down your Consul datacenter

<Frame>
  ![The image outlines objectives for "Secure Agent Communication," focusing on understanding Consul security, differentiating certificate types for TLS encryption, and understanding TLS encryption settings for a secure datacenter. It also indicates a difficulty level of 2.](https://kodekloud.com/kk-media/image/upload/v1752877940/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-7-Section-Overview/secure-agent-communication-tls-objectives.jpg)
</Frame>

***

## Table of Contents

* [Consul Security Model](#consul-security-model)
* [TLS Certificate Types](#tls-certificate-types)
* [Configuring TLS Encryption](#configuring-tls-encryption)

***

## Consul Security Model

Consul’s security model is built around a zero-trust philosophy, where every component must authenticate and authorize requests. The threat model assumes:

* Agents or servers may be compromised.
* Network traffic could be intercepted or manipulated.
* Attackers might attempt to impersonate nodes or services.

<Callout icon="lightbulb">
  Consul uses mutual TLS (mTLS) to enforce identity verification and data confidentiality across all RPC calls.
</Callout>

### Key Security Principles

* **Authentication**: Verify node and service identity using TLS certificates.
* **Authorization**: Control access via ACL tokens.
* **Encryption**: Encrypt all RPC and gossip traffic with TLS.

***

## TLS Certificate Types

Consul requires several certificate types to establish encrypted channels. Use the table below to understand their roles:

| Certificate Type      | Purpose                                          | Example Configuration          |
| --------------------- | ------------------------------------------------ | ------------------------------ |
| Server CA             | Signs TLS certificates for Consul servers        | `ca.pem`                       |
| Client Certificate    | Authenticates Consul clients (agents) to servers | `client.pem`, `client-key.pem` |
| Gossip Encryption Key | Secures gossip layer traffic (optional)          | `gossip-encryption-key`        |

<Callout icon="triangle-alert">
  Protect your private keys (`.pem` files). Unauthorized access may allow attackers to impersonate nodes.
</Callout>

***

## Configuring TLS Encryption

To enforce TLS encryption in Consul, update your agent and server configuration files (`config.hcl`) with the following parameters:

```hcl theme={null}
