# Or, if you place it at ~/.kube/config:
kubectl get pods
```

Both commands will yield:

```text theme={null}
No resources found.
```

***

## 4. Structure of a kubeconfig File

A kubeconfig has three top-level sections:

| Section  | Description                                                    |
| -------- | -------------------------------------------------------------- |
| clusters | Definitions of Kubernetes clusters (name, server URL, CA info) |
| users    | Credentials (client cert/key or token) for each user           |
| contexts | Mappings of user ↔ cluster, with optional namespace setting    |

<Frame>
  ![The image is a diagram of a KubeConfig file structure, showing clusters, contexts, and users in separate sections. It illustrates how different environments and roles are organized within the configuration.](https://kodekloud.com/kk-media/image/upload/v1752880746/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Client-Security-kubeconfig/kubeconfig-file-structure-diagram.jpg)
</Frame>

### 4.1 Minimal Example

```yaml theme={null}
apiVersion: v1
kind: Config

clusters:
- name: my-kube-playground
  cluster:
    server: https://my-kube-playground:6443
    certificate-authority: ca.crt

users:
- name: my-kube-admin
  user:
    client-certificate: admin.crt
    client-key: admin.key

contexts:
- name: my-kube-admin@my-kube-playground
  context:
    cluster: my-kube-playground
    user: my-kube-admin

current-context: my-kube-admin@my-kube-playground
```

***

## 5. Managing Multiple Clusters, Users, and Contexts

You can add as many entries as needed:

```yaml theme={null}
apiVersion: v1
kind: Config

clusters:
- name: my-kube-playground
  cluster:
    server: https://my-kube-playground:6443
    certificate-authority: ca.crt
- name: development
  cluster:
    server: https://dev.example.com:6443
    certificate-authority: dev-ca.crt
- name: production
  cluster:
    server: https://prod.example.com:6443
    certificate-authority: prod-ca.crt

users:
- name: my-kube-admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
- name: dev-user
  user:
    client-certificate: dev.crt
    client-key: dev.key
- name: prod-user
  user:
    client-certificate: prod.crt
    client-key: prod.key

contexts:
- name: my-kube-admin@my-kube-playground
  context:
    cluster: my-kube-playground
    user: my-kube-admin
- name: dev-user@development
  context:
    cluster: development
    user: dev-user
- name: prod-user@production
  context:
    cluster: production
    user: prod-user

current-context: my-kube-admin@my-kube-playground
```

### 5.1 Viewing and Switching Contexts

Use built-in commands to inspect or switch contexts:

| Command                                           | Description                               |
| ------------------------------------------------- | ----------------------------------------- |
| `kubectl config view`                             | Show merged config (defaults + overrides) |
| `kubectl --kubeconfig=my-config config view`      | View a specific file                      |
| `kubectl config use-context prod-user@production` | Switch current context to production      |

***

## 6. Setting a Default Namespace

Embed `namespace` in the context to avoid adding `-n` on every command:

```yaml theme={null}
contexts:
- name: admin@production
  context:
    cluster: production
    user: admin
    namespace: finance
```

Now `kubectl get pods` under this context defaults to the `finance` namespace.

***

## 7. Embedding Certificate Data Directly

Inline your certs and keys as base64 to avoid external files:

```yaml theme={null}
clusters:
- name: production
  cluster:
    server: https://172.17.0.51:6443
    certificate-authority-data: |
      [SECRET_REDACTED]...
users:
- name: admin
  user:
    client-certificate-data: |
      [SECRET_REDACTED]...
    client-key-data: |
      [SECRET_REDACTED]...
```

Generate and inspect base64 fields:

```bash theme={null}
# Encode files
cat ca.crt      | base64
cat admin.crt   | base64
cat admin.key   | base64

# Decode embedded data
echo "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t" | base64 --decode
```

<Callout icon="triangle-alert">
  Embedding secrets directly in your config can increase exposure risk. Always secure your files and consider encryption at rest.
</Callout>

***

## 8. Practice Exercises

1. Create a second context for a staging cluster.
2. Switch between contexts without retyping server flags.
3. Embed certificates and verify connectivity.
4. Troubleshoot an invalid certificate scenario.

***

## Links and References

* [Kubeconfig Overview](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Kubernetes Authentication](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/ca772db3-53aa-44c1-b424-3d32a046b683/lesson/c89e8c96-7640-44a8-a002-9d96c2f7a6f4" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/ca772db3-53aa-44c1-b424-3d32a046b683/lesson/e572aaf4-1736-4865-9dd1-b2e46aaaca04" />
</CardGroup>


# Client Security kubectl proxy port forward

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Cluster-Component-Security/Client-Security-kubectl-proxy-port-forward/page

This guide explores secure methods for accessing Kubernetes APIs and Services locally using kubectl proxy and kubectl port-forward.

In this guide, we explore how the `kubectl` CLI communicates with the Kubernetes API server and demonstrate two secure methods—**kubectl proxy** and **kubectl port-forward**—for accessing cluster APIs and Services locally. You’ll see how `kubeconfig` provides authentication, how to launch a local HTTP proxy, and how to forward ports from your machine to in-cluster endpoints.

## 1. Interacting with the Kubernetes API

By default, `kubectl` uses credentials in your `~/.kube/config` (kubeconfig) to authenticate against the API server:

```bash theme={null}
kubectl get nodes
```

Example output:

```plaintext theme={null}
NAME     STATUS   ROLES                  AGE    VERSION
master   Ready    control-plane,master   25h    v1.20.1
worker   Ready    <none>                 25h    v1.20.1
```

If you call the API directly over HTTPS without credentials, you’ll get a 403 error:

```bash theme={null}
curl https://<kube-api-server-ip>:6443 -k
```

```json theme={null}
{
  "kind": "Status",
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "code": 403
}
```

Supplying client certificates lets you authenticate:

```bash theme={null}
curl https://<kube-api-server-ip>:6443 -k \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```

This returns a list of available API paths:

```json theme={null}
{
  "paths": [
    "/api/",
    "/api/v1/",
    "/apis/",
    "/healthz/",
    "/metrics/"
  ]
}
```

### Comparison of Access Methods

| Method          | Command                   | Authentication | Use Case                                |
| --------------- | ------------------------- | -------------- | --------------------------------------- |
| kubectl CLI     | `kubectl get nodes`       | kubeconfig     | Standard cluster management             |
| Direct API Curl | `curl https://<api>:6443` | Client certs   | Scripting or debugging API interactions |
| kubectl proxy   | `kubectl proxy`           | kubeconfig     | Local HTTP proxy for API & services     |

## 2. Using `kubectl proxy`

The `kubectl proxy` command starts a local HTTP server (default port **8001**) that forwards requests to the API server using your `kubeconfig` credentials:

```bash theme={null}
kubectl proxy
