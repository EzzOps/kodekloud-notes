# Demo Vault Authentication

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Demo-Vault-Authentication/page

Learn to secure Kubernetes workloads using Vault’s Kubernetes authentication method for validating ServiceAccount JWTs and issuing short-lived Vault tokens.

Learn how to secure Kubernetes workloads by enabling Vault’s Kubernetes authentication method. This guide walks through configuring Vault to validate Kubernetes ServiceAccount JWTs via the Token Review API and issue short-lived Vault tokens.

| Requirement                          | Description                                                            |
| ------------------------------------ | ---------------------------------------------------------------------- |
| Vault CLI                            | Installed and pointed to your Vault server                             |
| Management Vault token (e.g., root)  | Has privileges to enable auth methods and manage roles                 |
| Kubernetes Service Account           | Bound to the `system:auth-delegator` ClusterRole for TokenReview calls |
| Kubernetes API server address and CA | Required for Vault to communicate with the cluster                     |

<Callout icon="lightbulb">
  You can use any non-root token with sufficient privileges instead of the root token. Follow [Vault best practices](https://www.vaultproject.io/docs/concepts/policies) for production environments.
</Callout>

***

## 1. (Optional) Create and Log In with a Vault Token

If you need a token to configure auth methods and roles, create one:

```bash theme={null}
vault token create
