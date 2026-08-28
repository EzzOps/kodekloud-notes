# Success! Enabled the kv-v2 secrets engine at: crds/
```

## 2. Read from an Empty Path

If no data exists at `crds/mysql`, Vault returns an error:

```bash theme={null}
vault kv get crds/mysql
# Error reading crds/mysql: no value found at crds/mysql
```

## 3. Storing Secrets

### 3.1 Create the First Version

Store only a username:

```bash theme={null}
vault kv put crds/mysql username=root
# Key              Value
# ---              -----
# created_time     2021-08-31T11:17:38.755927206Z
# deletion_time    n/a
# destroyed        false
# version          1
```

### 3.2 Update with a Password

Add a password to create version 2:

```bash theme={null}
vault kv put crds/mysql username=root password=12345
# Key              Value
# ---              -----
# created_time     2021-08-31T11:19:45.645227215Z
# deletion_time    n/a
# destroyed        false
# version          2
```

### 3.3 Add an API Key

You can append fields anytime (creates version 3):

```bash theme={null}
vault kv put crds/mysql username=root password=12345 apiKey=Vbdj794MHUH8945tojrjf3
# Key              Value
# ---              -----
# created_time     2021-10-03T13:10:55.084433408Z
# deletion_time    n/a
# destroyed        false
# version          3
```

## 4. Retrieve Secrets and Metadata

| Operation             | Command                            | Description                           |
| --------------------- | ---------------------------------- | ------------------------------------- |
| Fetch data & metadata | `vault kv get crds/mysql`          | Shows both secret values and metadata |
| Fetch only metadata   | `vault kv metadata get crds/mysql` | Displays metadata and version history |

### 4.1 Fetch Both Data and Metadata

```bash theme={null}
vault kv get crds/mysql
# ====== Metadata ======
# Key              Value
# ---              -----
# created_time     2021-10-03T13:10:55.084433408Z
# deletion_time    n/a
# destroyed        false
# version          3
#
# ======= Data =======
# Key              Value
# ---              -----
# apiKey           Vbdj794MHUH8945tojrjf3
# password         12345
# username         root
```

### 4.2 Fetch Only Metadata

```bash theme={null}
vault kv metadata get crds/mysql
# ==== Metadata ====
# Key                   Value
# ---                   -----
# cas_required          false
# created_time          2021-10-03T13:10:55.084433408Z
# current_version       3
# delete_version_after  0
# max_versions          10
# oldest_version        1
# updated_time          2021-10-03T13:10:55.084433408Z
#
# ==== Version 1 ====
# Key              Value
# ---              -----
# created_time     2021-08-31T11:17:38.755927206Z
# deletion_time    n/a
# destroyed        false
```

## 5. Deleting Secrets

### 5.1 Soft Delete Latest Version

```bash theme={null}
vault kv delete crds/mysql
# Success! Data deleted (if it existed) at: crds/mysql
```

Reading now shows the deleted version’s metadata:

```bash theme={null}
vault kv get crds/mysql
# ====== Metadata ======
# Key              Value
# ---              -----
# created_time     2021-10-03T13:10:55.084433408Z
# deletion_time    2021-10-03T13:10:56.084433408Z
# destroyed        true
# version          3
```

<Callout icon="triangle-alert">
  Soft-deleted versions can be undeleted until permanently destroyed. To irreversibly remove versions, use `vault kv destroy`.
</Callout>

## 6. Using KV Engine Inside Kubernetes

If Vault is running in Kubernetes, exec into the pod to run the same commands:

```bash theme={null}
kubectl get pods
# NAME                                   READY   STATUS    RESTARTS   AGE
# vault-0                                1/1     Running   0          21m
kubectl exec -it vault-0 -- /bin/sh
/ # vault secrets enable -path=crds kv-v2
/ # vault kv put crds/mysql username=root password=12345
/ # vault kv get crds/mysql
```

<Callout icon="lightbulb">
  After adding secrets, configure authentication methods and attach policies so applications can securely access your KV paths. See [Vault Policies](https://www.vaultproject.io/docs/concepts/policies) for more details.
</Callout>

***

## Links and References

* [Vault Secrets Engines: KV](https://www.vaultproject.io/docs/secrets/kv)
* [Vault CLI Documentation](https://www.vaultproject.io/docs/commands)
* [Kubernetes Exec](https://kubernetes.io/docs/tasks/debug/debug-cluster/container-debug/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/19b7b7d0-fd54-4cc1-ba0d-d1134e2b333f" />
</CardGroup>


# Kubernetes Secrets its Drawbacks

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Kubernetes-Secrets-its-Drawbacks/page

This article reviews Kubernetes Secrets, their limitations, and how to securely manage sensitive data using HashiCorp Vault.

Welcome to the HashiCorp Vault series! In this lesson, we’ll review how Kubernetes stores sensitive data in Secrets, highlight key drawbacks, and prepare for a secure injection of dynamic secrets using Vault.

## Why Use Kubernetes Secrets?

Managing sensitive data—passwords, API tokens, SSH keys—is critical in any deployment. Kubernetes Secrets help you:

* Decouple credentials from application pods and container images
* Store sensitive values centrally in etcd (the Kubernetes key-value store)
* Consume secrets as mounted volumes or environment variables

| Mount Method    | Use Case                              | Example                  |
| --------------- | ------------------------------------- | ------------------------ |
| Volume mount    | Inject files (e.g., TLS certs)        | `volumes: - name: creds` |
| Environment var | Pass small values (e.g., DB password) | `env: - name: DB_PASS`   |

<Callout icon="triangle-alert">
  Kubernetes Secrets are only base64-encoded, not encrypted by default. Any user with API or etcd access can decode them.
</Callout>

Learn more in the [Kubernetes Secrets documentation][k8s-secrets].

## Creating a Generic Secret

Create a simple Secret in one command:

```bash theme={null}
kubectl create secret generic mysql-crds \
  --from-literal=password=s3cR3t!
```

Inspect it as YAML:

```bash theme={null}
kubectl get secret mysql-crds -o yaml
```

```yaml theme={null}
apiVersion: v1
data:
  password: czNjUjN0IQ==
kind: Secret
metadata:
  name: mysql-crds
  namespace: default
type: Opaque
```

Decode it easily:

```bash theme={null}
echo czNjUjN0IQ== | base64 -d
