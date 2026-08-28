# Server configuration: config/server.hcl
server = true
verify_incoming = true
verify_outgoing = true
ca_file = "/etc/consul/tls/ca.pem"
cert_file = "/etc/consul/tls/server.pem"
key_file = "/etc/consul/tls/server-key.pem"
```

```hcl theme={null}
# Client (agent) configuration: config/client.hcl
verify_incoming = true
verify_outgoing = true
ca_file = "/etc/consul/tls/ca.pem"
cert_file = "/etc/consul/tls/client.pem"
key_file = "/etc/consul/tls/client-key.pem"
```

Additional setting for the gossip encryption key:

```hcl theme={null}
encrypt = "base64-encoded-gossip-key"
```

### Best Practices

* Rotate TLS certificates and gossip keys regularly.
* Use a dedicated CA for your Consul datacenter.
* Automate certificate issuance with HashiCorp Vault or your PKI.

***

## Links and References

* [Consul TLS Encryption](https://www.consul.io/docs/security/tls)
* [HashiCorp Consul Security Model](https://www.consul.io/docs/enterprise/security)
* [Mutual TLS (mTLS) Overview](https://www.consul.io/docs/security/encryption#practical-mtls-configuration)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/777a613c-50bc-474c-9597-aec67eec52e0/lesson/8dc32ac1-875d-4361-ba08-9919e78a632d" />
</CardGroup>


# Objective 7 Section Recap

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Agent-Communication/Objective-7-Section-Recap/page

This article consolidates essential steps for securing Consul data centers using TLS encryption.

In this section, we consolidated the essential steps for hardening your Consul data center using TLS:

| Focus Area                     | Key Takeaways                                                               |
| ------------------------------ | --------------------------------------------------------------------------- |
| Consul Security & Threat Model | Overview of common attack vectors and Consul’s defense mechanisms.          |
| Secure Component Roles         | Roles of servers, clients, and proxies in maintaining a secure environment. |
| Certificate Types for TLS      | Differences between internal CA, external CA, and node certificates.        |
| TLS Encryption Settings        | Configuration of gossip encryption, RPC/TLS, and ACL integration.           |

<Callout icon="lightbulb">
  Rotate your certificates regularly and store them in a secure location to minimize the risk of credential compromise.
</Callout>

<Frame>
  ![The image outlines objectives related to secure agent communication, focusing on understanding Consul security, differentiating certificate types for TLS encryption, and understanding TLS encryption settings. It also includes a difficulty level indicator.](https://kodekloud.com/kk-media/image/upload/v1752877941/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-7-Section-Recap/secure-agent-communication-consul-tls.jpg)
</Frame>

Thank you for completing this objective. With a solid grasp of Consul’s security model, certificate management, and TLS configuration, you’re ready to deploy a fully encrypted and resilient Consul cluster.

## Links and References

* [Consul Security Model](https://www.consul.io/docs/security)
* [TLS Encryption in Consul](https://www.consul.io/docs/commands/agent#tls)
* [Managing Certificates](https://www.consul.io/docs/operations/security/tls)
* [HashiCorp Consul Documentation](https://www.consul.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/777a613c-50bc-474c-9597-aec67eec52e0/lesson/c3a023d8-9f2a-416a-804c-320704f3f05d" />
</CardGroup>
