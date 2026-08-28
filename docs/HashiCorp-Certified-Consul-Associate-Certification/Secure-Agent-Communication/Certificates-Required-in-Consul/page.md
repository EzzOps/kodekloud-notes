# Certificates Required in Consul

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Agent-Communication/Certificates-Required-in-Consul/page

This guide covers the TLS certificates required for securing Consuls control plane, data plane, and HTTP APIs.

Consul relies on TLS certificates to secure its control plane, data plane, and HTTP APIs. In this guide, we’ll cover the certificates needed for:

* API and RPC encryption between clients and servers
* Mutual TLS (mTLS) in the service mesh (Connect)
* Optional HTTPS on the HTTP API endpoint

Proper certificate management ensures confidentiality, integrity, and authentication across your Consul deployment.

## Overview of TLS Certificate Requirements

| Communication Channel  | Purpose                                       | Certificates Required                         |
| ---------------------- | --------------------------------------------- | --------------------------------------------- |
| API & RPC              | Secure HTTP API and internal RPC traffic      | Server and client TLS certificates            |
| Service Mesh (Connect) | mTLS for all service-to-service communication | Mutual TLS certificates issued by Consul’s CA |
| HTTPS API (Optional)   | Encrypt HTTP listener on port 8500            | HTTP TLS certificate and private key          |

## TLS for API and RPC

By default, Consul’s HTTP API and internal RPC talk over plain TCP/HTTP. To enable encryption:

1. Generate a server certificate (with `server.service.consul` as a SAN).
2. Generate client certificates for each agent or external client.
3. Distribute `cert_file` and `key_file` in the agent configuration.

<Callout icon="lightbulb">
  Without TLS, all API calls and gossip traffic are unencrypted. Enable certificates to protect sensitive data in transit.
</Callout>

## Service Mesh (Connect) and mTLS

When Connect is enabled, Consul automatically issues and rotates certificates for every service proxy:

* Each side presents a certificate signed by the same CA.
* Identity is verified before any data exchange.
* Traffic is fully encrypted in transit.

Consul’s built-in CA handles issuance and rotation by default. You do *not* need an external CA unless you have specific compliance needs.

## HTTP API over HTTPS (Optional)

If you prefer to secure only the HTTP API (port 8500) without using Connect, configure the HTTP listener for TLS:

```hcl theme={null}
