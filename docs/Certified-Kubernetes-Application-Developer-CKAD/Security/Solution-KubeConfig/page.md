# Solution KubeConfig

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Solution-KubeConfig/page

Guide to inspecting and managing kubeconfig files, switching contexts, setting a custom default, and diagnosing and fixing client certificate mismatches for kubectl authentication.

In this lesson you'll learn how to inspect kubeconfig files, switch contexts, make a custom kubeconfig the default, and diagnose a common client-certificate mismatch that prevents kubectl from authenticating.

## Locate the default kubeconfig

Find the current home directory and inspect the default kubeconfig (usually \$HOME/.kube/config):

```bash theme={null}
root@controlplane ~ ➜ echo $HOME
/root

root@controlplane ~ ➜ ls -la $HOME/.kube
cache  config

root@controlplane ~ ➜ cat $HOME/.kube/config
apiVersion: v1
clusters:
- cluster:
    server: https://controlplane:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTi...
```

Quick summary from the default kubeconfig:

* Clusters defined: 1
* Users defined: 1
* Contexts defined: 1

<Frame>
  <img alt="A split-screen screenshot: the left side shows a quiz question asking &#x22;How many clusters are defined in the default kubeconfig file?&#x22; with multiple-choice answers, and the right side shows a terminal displaying the contents of a ~/.kube/config file (clusters, contexts, users) including a &#x22;kubernetes&#x22; cluster entry." />
</Frame>

<Callout icon="lightbulb">
  The value in current-context is the name of the context in use. The context lists which cluster and which user to use — the "user" entry is a reference name, not necessarily the actual system username.
</Callout>

## Inspect a custom kubeconfig file

Here is an example custom kubeconfig stored at `/root/my-kube-config`. It contains multiple clusters, contexts, and users:

```yaml theme={null}
apiVersion: v1
kind: Config

clusters:
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: development
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: kubernetes-on-aws
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: test-cluster-1
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

contexts:
- name: test-user@development
  context:
    cluster: development
    user: test-user

- name: aws-user@kubernetes-on-aws
  context:
    cluster: kubernetes-on-aws
    user: aws-user

- name: test-user@production
  context:
    cluster: production
    user: test-user

- name: research
  context:
    cluster: test-cluster-1
    user: dev-user

users:
- name: test-user
  user:
    client-certificate: /etc/kubernetes/pki/users/test-user/test-user.crt
    client-key: /etc/kubernetes/pki/users/test-user/test-user.key
- name: dev-user
  user:
    client-certificate: /etc/kubernetes/pki/users/dev-user/developer-user.crt
    client-key: /etc/kubernetes/pki/users/dev-user/developer-user.key
- name: aws-user
  user:
    client-certificate: /etc/kubernetes/pki/users/aws-user/aws-user.crt
    client-key: /etc/kubernetes/pki/users/aws-user/aws-user.key

current-context: test-user@development
```

From the file above you can extract the following:

| Item                          | Count / Value                                     |
| ----------------------------- | ------------------------------------------------- |
| Clusters defined              | 4                                                 |
| Contexts defined              | 4                                                 |
| `research` context user       | `dev-user`                                        |
| `aws-user` client-certificate | `/etc/kubernetes/pki/users/aws-user/aws-user.crt` |
| current-context               | `test-user@development`                           |

## Switch context using a specific kubeconfig file

To switch to a context defined in a non-default kubeconfig file without affecting your default config, include the `--kubeconfig` flag:

```bash theme={null}
root@controlplane ~ ❯ kubectl config use-context research --kubeconfig /root/my-kube-config
Switched to context "research".
```

You can confirm the change by viewing that kubeconfig or running kubectl commands with `--kubeconfig /root/my-kube-config`.

## Make the custom kubeconfig the default

If you'd prefer not to pass `--kubeconfig` every time, replace your default kubeconfig with the custom file:

```bash theme={null}
root@controlplane ~ ➜ mv /root/my-kube-config /root/.kube/config
```

After moving the file, kubectl will use it by default. Example output of `kubectl config view`:

```bash theme={null}
root@controlplane ~ › kubectl config view
apiVersion: v1
clusters:
- name: development
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
- name: kubernetes-on-aws
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
- name: test-cluster-1
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
contexts:
- name: aws-user@kubernetes-on-aws
  context:
    cluster: kubernetes-on-aws
    user: aws-user
- name: research
  context:
    cluster: test-cluster-1
    user: dev-user
- name: test-user@development
  context:
    cluster: development
    user: test-user
- name: test-user@production
  context:
    cluster: production
    user: test-user
current-context: research
kind: Config
preferences: {}
users:
- name: aws-user
  user:
    client-certificate: /etc/kubernetes/pki/users/aws-user/aws-user.crt
    client-key: /etc/kubernetes/pki/users/aws-user/aws-user.key
- name: dev-user
  user:
    client-certificate: /etc/kubernetes/pki/users/dev-user/developer-user.crt
    client-key: /etc/kubernetes/pki/users/dev-user/developer-user.key
- name: test-user
  user:
    client-certificate: /etc/kubernetes/pki/users/test-user/test-user.crt
    client-key: /etc/kubernetes/pki/users/test-user/test-user.key
```

## Diagnose and fix an authentication error (client-certificate mismatch)

With the current context set to `research`, running a kubectl command may produce an error indicating kubectl cannot read the client certificate referenced in the kubeconfig:

```bash theme={null}
root@controlplane ~ ➜ kubectl get nodes
error: unable to read client-cert /etc/kubernetes/pki/users/dev-user/developer-user.crt for dev-user
due to open /etc/kubernetes/pki/users/dev-user/developer-user.crt: no such file or directory
```

Investigate the actual files on disk:

```bash theme={null}
root@controlplane ~ » ls /etc/kubernetes/pki/users
aws-user  dev-user  test-user

root@controlplane ~ » ls /etc/kubernetes/pki/users/dev-user/
dev-user.crt  dev-user.csr  dev-user.key
```

Root cause: the kubeconfig references `/etc/kubernetes/pki/users/dev-user/developer-user.crt` and `/etc/kubernetes/pki/users/dev-user/developer-user.key`, but the files present are named `dev-user.crt` and `dev-user.key`. Update the kubeconfig to point to the correct certificate and key.

<Callout icon="warning">
  The kubectl config set-credentials command modifies the kubeconfig file kubectl is currently using (typically \$HOME/.kube/config). Back up that file before making changes.
</Callout>

Recommended fix — update the `dev-user` credential entry to reference the correct certificate and key:

```bash theme={null}
root@controlplane ~ ➜ kubectl config set-credentials dev-user \
  --client-certificate=/etc/kubernetes/pki/users/dev-user/dev-user.crt \
  --client-key=/etc/kubernetes/pki/users/dev-user/dev-user.key
```

Re-run the kubectl command to verify access:

```bash theme={null}
root@controlplane ~ ➜ kubectl get nodes
NAME          STATUS   ROLES    AGE   VERSION
controlplane  Ready    master   10m   v1.x.y
```

After correcting the client-certificate and client-key file paths in the kubeconfig, kubectl can authenticate as `dev-user` and access the cluster.

## Quick reference

| Action                                | Command / Notes                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| View current kubeconfig               | `kubectl config view`                                                                 |
| Switch context (default kubeconfig)   | `kubectl config use-context <context-name>`                                           |
| Switch context for specific file      | `kubectl config use-context <context-name> --kubeconfig /path/to/config`              |
| Update user credentials in kubeconfig | `kubectl config set-credentials <user> --client-certificate=<crt> --client-key=<key>` |
| Backup default kubeconfig             | `cp $HOME/.kube/config $HOME/.kube/config.bak`                                        |

## Links and references

* Kubernetes kubeconfig and contexts: [https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* kubectl config documentation: [https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config)
* Best practices for client certificate authentication: [https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/b537a52a-ab07-4df8-a866-4f067f581b90" />
</CardGroup>
