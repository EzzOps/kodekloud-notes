# Client Security kubeconfig

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Cluster-Component-Security/Client-Security-kubeconfig/page

This article explains how to use Kubernetes kubeconfig files to manage cluster endpoints and user credentials for easier interaction with kubectl.

In this lesson, we’ll explore how Kubernetes **kubeconfig** files let you store cluster endpoints and user credentials for `kubectl`, eliminating the need to retype flags every time you interact with your cluster.

## 1. Direct API Access with curl

If your API server is at `my-kube-playground:6443` and you’ve generated:

* CA certificate: `ca.crt`
* Client certificate: `admin.crt`
* Client key: `admin.key`

You can query the API directly:

```bash theme={null}
curl https://my-kube-playground:6443/api/v1/pods \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```

Response:

```json theme={null}
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/pods"
  },
  "items": []
}
```

## 2. Equivalent kubectl Commands

With `kubectl`, the same request requires these flags:

```bash theme={null}
kubectl get pods \
  --server https://my-kube-playground:6443 \
  --client-key admin.key \
  --client-certificate admin.crt \
  --certificate-authority ca.crt
```

Output:

```text theme={null}
No resources found.
```

Typing long flag lists is tedious. Let’s streamline this with a kubeconfig file.

<Callout icon="lightbulb">
  By default, `kubectl` looks for `~/.kube/config`. You can override with `--kubeconfig=PATH`.
</Callout>

## 3. Creating and Using a kubeconfig File

Save your cluster, user, and context definitions in a YAML file (e.g., `config`), then run:

```bash theme={null}
kubectl get pods --kubeconfig=config
