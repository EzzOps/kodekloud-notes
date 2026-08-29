# Set your ACL token
export CONSUL_HTTP_TOKEN=aba7cbe5-879b-999a-07cc-2efd9ac0ffe
```

### Common Commands

| Command                                        | Description                             |
| ---------------------------------------------- | --------------------------------------- |
| `consul intention create [--deny] <src> <dst>` | Create a new intention (default: allow) |
| `consul intention delete <src> <dst>`          | Remove an existing intention            |
| `consul intention list`                        | List all intentions                     |
| `consul intention get <src> <dst>`             | Show details of a specific intention    |
| `consul intention check <src> <dst>`           | Test intent between two services        |
| `consul intention match <src> <dst>`           | Display the effective intention         |

#### Examples

```bash theme={null}
# Allow web-01 → db-01
consul intention create web-01 db-01
# Deny web-01 → db-01
consul intention create --deny web-01 db-01
# Output: Created: web-01 => db-01 (deny)
```

> **lightbulb** Omitting `--deny` on `create` defaults to an `allow` intention.

***

Next, apply these approaches within your own Consul cluster to enforce secure, service-to-service communication.

## Links and References

* [Consul Service Mesh Intentions (Official Docs)](https://www.consul.io/docs/connect/intentions)
* [Consul HTTP API Reference](https://www.consul.io/api-docs)
* [Consul CLI Commands](https://www.consul.io/docs/commands)
* [HashiCorp Learn: Service Mesh with Consul](https://learn.hashicorp.com/consul)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/be057676-1d98-4d78-89c8-b8be2a9c2967/lesson/500cb3bf-6fe4-49c0-9eb2-f4cbb3cbc307)


# Objective 6 Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Register-a-Service-Proxy/Objective-6-Section-Overview/page

Learn to deploy, secure, and manage HashiCorp Consul’s Connect service mesh, covering fundamentals, proxy registration, and traffic policy management.

Learn how to deploy, secure, and manage HashiCorp Consul’s Connect service mesh. This objective guides you through service mesh fundamentals, proxy registration, traffic policy definitions (intentions), and managing those policies via CLI, UI, and API.

## Lesson Overview

Below is a summary of what you’ll cover in this lesson:

| Topic                     | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| Service mesh fundamentals | Overview of Consul Connect architecture, data plane, control plane, and proxies. |
| Proxy registration        | Step-by-step guide to configuring and registering sidecar proxies.               |
| Intentions                | Creating and enforcing traffic policies to secure service-to-service traffic.    |
| Managing intentions       | Using the Consul CLI, UI, and REST API to list, update, and delete intentions.   |

> **lightbulb** This is one of the most challenging objectives in the [Consul Associate exam](https://www.hashicorp.com/certification/consul-associate). We’ll break down each concept with detailed examples to simplify implementation and management.

Let’s begin with service mesh fundamentals.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/be057676-1d98-4d78-89c8-b8be2a9c2967/lesson/61153589-079c-44c4-9e17-cf89b0ac8dd8)
