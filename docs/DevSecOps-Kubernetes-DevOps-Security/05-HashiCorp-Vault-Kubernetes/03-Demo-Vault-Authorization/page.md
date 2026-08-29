# Example output:
# Key                Value
# ---                -----
# token              s.t3Z3Qzflc14FRideymCDYn
# token_accessor     3gZeW9G8OcK80Wyewuzigth
# token_policies     ["root"]
```

Log in using the new token:

```bash theme={null}
vault login s.t3Z3Qzflc14FRideymCDYn
# Success! You are now authenticated.
```

***

## 2. Enable the Kubernetes Auth Method

Turn on the Kubernetes auth backend in Vault:

```bash theme={null}
vault auth enable kubernetes
# Success! Enabled kubernetes auth method at: kubernetes/
```

***

## 3. Configure Vault to Talk to Kubernetes

Provide Vault with the ServiceAccount reviewer JWT, the cluster’s API endpoint, and the CA certificate:

```bash theme={null}
vault write auth/kubernetes/config \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_host="https://${KUBERNETES_PORT_443_TCP_ADDR}:443" \
  kubernetes_ca_cert="@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
# Success! Data written to: auth/kubernetes/config
```

<Callout icon="triangle-alert">
  Ensure your environment variable `KUBERNETES_PORT_443_TCP_ADDR` points to the correct API server IP or DNS name before running this command.
</Callout>

***

## 4. Create a Kubernetes Auth Role Mapping to Vault Policies

Define a role (`phpapp`) that binds a specific ServiceAccount in a namespace to a Vault policy:

```bash theme={null}
vault write auth/kubernetes/role/phpapp \
  bound_service_account_names=app \
  bound_service_account_namespaces=demo \
  policies=app \
  ttl=1h
# Success! Data written to: auth/kubernetes/role/phpapp
```

This role ensures that only pods using the `app` ServiceAccount in the `demo` namespace receive Vault tokens scoped to the `app` policy, valid for one hour.

***

## 5. Verify TokenReview Permissions

Check that the Vault ServiceAccount (for example, `vault` in `demo` namespace) has the `system:auth-delegator` ClusterRole to call the TokenReview API:

```bash theme={null}
kubectl describe clusterrolebinding vault-server-binding
```

Example output:

```YAML theme={null}
Name:         vault-server-binding
Role:
  Kind:       ClusterRole
  Name:       system:auth-delegator
Subjects:
  Kind:             ServiceAccount
  Name:             vault
  Namespace:        demo
```

***

## Next Steps

With Kubernetes auth enabled and roles configured, you can deploy application pods that request Vault tokens via their ServiceAccount JWTs and fetch secrets at runtime.

## Links and References

* [Vault Kubernetes Auth Method](https://www.vaultproject.io/docs/auth/kubernetes)
* [Kubernetes TokenReview API](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)
* [HashiCorp Vault Documentation](https://www.vaultproject.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/2f1b7046-4f0b-40bd-9dfc-c2c53311f905" />
</CardGroup>


# Demo Vault Authorization

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Demo-Vault-Authorization/page

This lesson explores Vault's authorization model and how to define access controls using policies written in HCL.

In this lesson, we’ll dive into Vault’s authorization model and learn how to define fine-grained access controls using policies. Vault policies, written in HCL, dictate which operations a user or machine can perform on specific secret paths. Every Vault token attaches to one or more policies, and access is always scoped by path.

## Vault Policies and Paths

Imagine you have credential data for MongoDB and MySQL stored under a KV v2 secrets engine mounted at `crds`. You want:

* Full CRUD (create, read, update) access to `crds/data/mongodb`
* Read-only access to `crds/data/mysql`

| Path                | Capabilities         | Description                       |
| ------------------- | -------------------- | --------------------------------- |
| `crds/data/mongodb` | create, read, update | Manage MongoDB credentials        |
| `crds/data/mysql`   | read                 | Read-only access to MySQL secrets |

<Callout icon="lightbulb">
  Vault policies are defined in HCL and loaded from local files. Capabilities include `create`, `read`, `update`, `delete`, among others.
</Callout>

## 1. Create the `app` Policy

Create a file at `/home/vault/app-policy.hcl`:

```hcl theme={null}
path "crds/data/mongodb" {
  capabilities = ["create", "read", "update"]
}

path "crds/data/mysql" {
  capabilities = ["read"]
}
```

## 2. Enable KV v2 and Apply the Policy

Use your root token to enable the KV engine and load the policy:

```bash theme={null}
