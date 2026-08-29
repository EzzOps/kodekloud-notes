# Error from server (NotFound): namespaces "blue" not found
```

### NamespaceAutoProvision

`NamespaceAutoProvision` (disabled by default) automatically creates a namespace if it doesn’t exist when you submit a request.

#### Viewing Enabled Admission Controllers

```bash theme={null}
kube-apiserver -h | grep enable-admission-plugins
```

On kubeadm-based clusters:

```bash theme={null}
kubectl exec kube-apiserver-control-plane -n kube-system -- kube-apiserver -h | grep enable-admission-plugins
```

#### Enabling an Admission Controller

Update the API server’s startup arguments:

```shell theme={null}
--enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
```

> **triangle-alert** Editing the `kube-apiserver` flags requires careful coordination. After changes, restart the API server or apply the updated control-plane manifest.

**Example (systemd service):**

```shell theme={null}
ExecStart=/usr/local/bin/kube-apiserver \
  --authorization-mode=Node,RBAC \
  --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision \
  …other flags…
```

**Example (kubeadm Pod manifest):**

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    image: k8s.gcr.io/kube-apiserver:v1.11.3
    command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
    …other flags…
```

Now, creating a Pod in a new namespace will auto-create it:

```bash theme={null}
kubectl run nginx --image=nginx --namespace=blue
kubectl get namespaces
# NAME          STATUS   AGE
# blue          Active   3m
# default       Active   23m
# kube-public   Active   24m
# kube-system   Active   24m
```

## NamespaceLifecycle Admission Controller

The **NamespaceLifecycle** plugin supersedes both `NamespaceExists` and `NamespaceAutoProvision`. It:

* Rejects requests to unknown namespaces
* Prevents deletion of critical system namespaces (`default`, `kube-system`, `kube-public`)

## Links and References

* [Kubernetes Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [Kubernetes RBAC Overview](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [kube-apiserver Command-Line Flags](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/fce29d1e-7bd6-43b5-b11e-863367854881)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/2df29ee2-5c77-4ab1-a3e3-8ce28aa498a4)


# Connectivity Mutual TLS

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Connectivity-Mutual-TLS/page

This article explains Mutual TLS (mTLS) for secure two-way authentication between client and server, including its handshake process and implementation in Kubernetes.

## Overview

Mutual TLS (mTLS) enhances standard TLS by providing two-way authentication between client and server. In this lesson, we’ll:

* Review one-way TLS (server-only authentication).
* Introduce mTLS handshake flows.
* Demonstrate how to generate certificates with OpenSSL.
* Explore securing pod-to-pod traffic in Kubernetes.

## Recap: One-Way TLS (Server Authentication)

When you visit an HTTPS website—like your online bank—the browser and server establish an encrypted channel using asymmetric and symmetric cryptography.

1. Client requests the server’s certificate.
2. Server sends its public certificate, signed by a trusted Certificate Authority (CA).
3. Browser verifies the certificate against its trust store (public keys of known CAs).
4. Browser generates a random symmetric key, encrypts it with the server’s public key, and sends it to the server.
5. Server decrypts the symmetric key with its private key.
6. Both parties use the symmetric key to encrypt application data.

> **lightbulb** One-way TLS ensures confidentiality and server authenticity but relies on application-layer credentials (usernames, passwords) to authenticate the client.

![The image illustrates the concept of a Certificate Authority (CA) with logos of various CAs, a secure online banking webpage, and a digital certificate for "my-bank.com."](https://kodekloud.com/kk-media/image/upload/v1752880876/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Connectivity-Mutual-TLS/certificate-authority-online-banking.jpg)

### TLS Handshake Steps

| Step | Description                                                                     |
| ---- | ------------------------------------------------------------------------------- |
| 1    | Client → Server: “Send me your certificate.”                                    |
| 2    | Server → Client: “[Server Certificate](https://letsencrypt.org/) signed by CA.” |
| 3    | Client: Validate certificate chain using CA public key from trust store.        |
| 4    | Client → Server: “Here’s a symmetric key, encrypted with your public key.”      |
| 5    | Server: Decrypt symmetric key with its private key.                             |
| 6    | Both: “All data now encrypted with this symmetric key.”                         |

## Mutual TLS (mTLS) Handshake

In mTLS, both sides present certificates. This is ideal for machine-to-machine communications—such as two services exchanging confidential data—without human credentials.

### Why Use mTLS?

| Benefit                      | Description                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------- |
| Strong Mutual Authentication | Both client and server verify each other’s identities.                          |
| Automated Trust Management   | Certificates can be rotated and validated automatically.                        |
| Defense in Depth             | Prevents unauthorized services from connecting, even if they know the endpoint. |

> **triangle-alert** Ensure your CA certificates are stored securely and rotated regularly to prevent unauthorized access.

### mTLS Handshake Sequence

| Step | Client → Server                                                        | Server → Client                          |
| ---- | ---------------------------------------------------------------------- | ---------------------------------------- |
| 1    | “Send me your certificate.”                                            |                                          |
| 2    |                                                                        | “Here’s my certificate. Now send yours.” |
| 3    | Validate server certificate via CA.                                    |                                          |
| 4    | “Here’s my certificate + encrypted symmetric key.”                     |                                          |
| 5    |                                                                        | Validate client certificate via CA.      |
| 6    | **Mutual authentication complete.**                                    | **Mutual authentication complete.**      |
| 7    | Both: Encrypt all further communication with the shared symmetric key. |                                          |

## Generating mTLS Certificates with OpenSSL

Below is a sample workflow to create a root CA, a server certificate, and a client certificate.

```bash theme={null}
