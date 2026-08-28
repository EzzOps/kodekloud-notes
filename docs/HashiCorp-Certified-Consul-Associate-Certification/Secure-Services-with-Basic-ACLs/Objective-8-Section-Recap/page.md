# Objective 8 Section Recap

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Services-with-Basic-ACLs/Objective-8-Section-Recap/page

This article reviews securing services with HashiCorp Consul’s ACL system, covering bootstrapping, policy creation, token management, and request authentication.

In this section, we reviewed how to secure your services using HashiCorp Consul’s Access Control List (ACL) system. You’ll walk away with a clear understanding of bootstrapping ACLs, defining policies, managing token lifecycles, and authenticating requests.

## Key Topics Overview

| Topic                  | Description                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| ACL Bootstrapping      | Enable ACLs, initialize the management token, and verify ACL-enabled mode                        |
| Policy Creation        | Write ACL policies in HCL or JSON; apply them via UI, CLI, and HTTP API                          |
| Token Lifecycle        | Create multi-policy, role-attached, and service-identity tokens; set expirations; revoke tokens  |
| Authentication Methods | Use CLI flags or `CONSUL_HTTP_TOKEN`, HTTP headers (`X-Consul-Token` or `Authorization`), and UI |

***

## Detailed Recap

### 1. Bootstrapping and Configuration

* Enable ACL enforcement in your Consul configuration.
* Initialize the ACL system to generate the **management token**.
* Confirm ACL mode with:
  ```bash theme={null}
  consul acl status
  ```

<Callout icon="lightbulb">
  If you’re running Consul in a cluster, ensure all agents join with `-enable-agent` and share the same ACL configuration.
</Callout>

### 2. Creating and Managing Policies

* Define policies in HCL or JSON syntax.
* Apply policies with the CLI:
  ```bash theme={null}
  consul acl policy create -name "web-policy" -rules @web-policy.hcl
  ```
* Or via HTTP API:
  ```http theme={null}
  PUT /v1/acl/policy
  ```
* You can also manage policies inside the Consul UI under **Access Control** → **Policies**.

### 3. Token Lifecycle Management

* **Create Tokens**: single-policy, multi-policy, role-attached, or service-identity tokens.
  ```bash theme={null}
  consul acl token create -description "service-xyz" -policy-name web-policy
  ```
* **Set Expiration**: use the `-expire-time` flag for time-to-live.
* **Revocation**: revoke unused or compromised tokens immediately:
  ```bash theme={null}
  consul acl token revoke <token_id>
  ```

<Callout icon="triangle-alert">
  Always revoke tokens as soon as they’re no longer needed to minimize security risks.
</Callout>

### 4. Authenticating Requests

* **CLI**:
  ```bash theme={null}
  export CONSUL_HTTP_TOKEN=<your-token>
  consul kv put foo bar
  ```
  Or pass `--token=<your-token>`.
* **HTTP API**: include the header:
  ```text theme={null}
  X-Consul-Token: <your-token>
  ```
  or
  ```text theme={null}
  Authorization: Bearer <your-token>
  ```
* **UI**: log in using a browser session token via **Access Control** → **Tokens**.

<Frame>
  ![The image outlines objectives for securing services with Access Control Lists (ACLs), including setting up an ACL system, creating policies, managing token lifecycles, and performing CLI and API requests using tokens. It also indicates a difficulty level of 2.](https://kodekloud.com/kk-media/image/upload/v1752877961/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-8-Section-Recap/acl-security-objectives-policies-tokens.jpg)
</Frame>

***

## Next Steps

With these building blocks in place—bootstrapping ACLs, defining policies, issuing/revoking tokens, and authenticating requests—you’re ready to implement robust Service Mesh security in your environment.

## Further Reading

* [Consul ACLs](https://www.consul.io/docs/security/acl)
* [Consul HTTP API](https://www.consul.io/api-docs/acl)
* [Service Mesh Security Patterns](https://www.hashicorp.com/blog/service-mesh-zero-trust)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/db782b7c-8302-485d-809a-9639d2673808" />
</CardGroup>
