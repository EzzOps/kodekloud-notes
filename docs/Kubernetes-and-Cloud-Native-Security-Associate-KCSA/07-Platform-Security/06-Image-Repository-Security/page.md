# Server certificate files on disk
ls /etc/kubernetes/pki/
# apiserver.crt   apiserver.key   etcd-server.crt   etcd-server.key   kubelet.crt   kubelet.key
```

### 3.2 Client-Side Certificates

| Client                    | Certificate File         | Key File                 |
| ------------------------- | ------------------------ | ------------------------ |
| Administrator (`kubectl`) | `admin.crt`              | `admin.key`              |
| Kube-Scheduler            | `scheduler.crt`          | `scheduler.key`          |
| Kube-Controller-Manager   | `controller-manager.crt` | `controller-manager.key` |
| Kube-Proxy                | `kube-proxy.crt`         | `kube-proxy.key`         |

```bash theme={null}
# Client certificate files on disk
ls /etc/kubernetes/pki/
# admin.crt   admin.key   scheduler.crt   scheduler.key   controller-manager.crt   controller-manager.key   kube-proxy.crt   kube-proxy.key
```

#### Inter-Service Authentication

* **API Server → etcd**: The API server acts as a client to etcd. You can reuse `apiserver.crt/key` or use a dedicated pair.
* **API Server → Kubelet**: When the API server calls kubelet’s HTTPS endpoint, it presents a client certificate (either its serving cert or a separate client cert).

In each mTLS handshake, both parties authenticate and establish an encrypted channel, ensuring data integrity and confidentiality.

***

## 4. Certificate Authority and Signing Strategy

You need a CA to sign every server and client certificate. Kubernetes supports:

* A **single CA** for all components
* **Multiple CAs** (e.g., one CA for etcd, another for the rest)

In this walkthrough, we’ll use a single CA:

* **CA Public Certificate**: `ca.crt`
* **CA Private Key**: `ca.key`

> **triangle-alert** Never store `ca.key` on nodes that aren’t fully secured. Loss of the CA key compromises your entire cluster.

### 4.1 CA-Managed Certificate Hierarchy

1. Generate the CA key and certificate (`ca.key`/`ca.crt`).
2. For each server and client:
   * Generate a CSR (Certificate Signing Request).
   * Sign the CSR with the CA key, specifying the proper Extended Key Usages (`serverAuth` or `clientAuth`).
3. Distribute the signed certificates and corresponding keys to each component.

***

## 5. References and Further Reading

* [Kubernetes TLS Bootstrapping](https://kubernetes.io/docs/reference/command-line-tools-reference/kubeadm/kubeadm-init/#certificate-configuration)
* [Understanding TLS in Kubernetes](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
* [etcd Security](https://etcd.io/docs/v3.4/op-guide/security/)

| Resource                    | Description                             |
| --------------------------- | --------------------------------------- |
| Kubernetes Official Docs    | Deep dive into components and TLS setup |
| Certificate Management (CA) | Best practices for CA hierarchies       |
| mTLS in Distributed Systems | Benefits of mutual TLS in microservices |

By following these steps, you’ll ensure that every interaction within your Kubernetes cluster is both encrypted and authenticated, delivering a robust security posture for your applications and infrastructure.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/bcccc856-d8a2-4b5f-9f08-c880a46fa7ca)


# Image Repository Security

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Image-Repository-Security/page

This article explains how to secure container images, including naming conventions, using secure registries, and configuring Pods for private repositories.

In this lesson, you’ll learn how to secure container images by:

* Understanding image naming conventions
* Working with secure image registries
* Configuring Pods to pull from private repositories

Previously, we deployed Pods running web apps, databases, and caches. Let’s begin with a simple Pod definition that uses the official nginx image:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx
```

## Understanding Image Names

Docker interprets `image: nginx` as `library/nginx` under the hood. The full naming convention is:

```text theme={null}
[registry]/[user-or-namespace]/[repository]:[tag]
```

* Omit the registry → defaults to Docker Hub (`docker.io`)
* Omit the namespace → defaults to `library` (the official account)

> **lightbulb** Specifying:

  ```yaml theme={null}
  image: library/nginx
  ```

  is equivalent to:

  ```yaml theme={null}
  image: docker.io/library/nginx
  ```

You can also pull from other public registries. For example, Google’s registry hosts Kubernetes test images:

```yaml theme={null}
image: gcr.io/kubernetes-e2e-test-images/dnsutils
```

### Common Public Registries

| Registry                 | URL       | Use Case                        |
| ------------------------ | --------- | ------------------------------- |
| Docker Hub               | docker.io | Default public images           |
| Google Artifact Registry | gcr.io    | Google-hosted Kubernetes images |
| Quay.io                  | quay.io   | CI/CD and enterprise images     |

## Using a Private Registry

For in-house applications, you can host your own registry or use a managed solution:

| Provider                 | Link                                                                                                                 |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| AWS ECR                  | [https://aws.amazon.com/ecr/](https://aws.amazon.com/ecr/)                                                           |
| Azure Container Registry | [https://azure.microsoft.com/services/container-registry/](https://azure.microsoft.com/services/container-registry/) |
| Google Artifact Registry | [https://cloud.google.com/artifact-registry](https://cloud.google.com/artifact-registry)                             |

To pull from a private registry, follow these steps:

1. **Authenticate locally** (for pushing and testing)
   ```bash theme={null}
   docker login private-registry.io
   # Username: registry-user
   # Password: ********
   # WARNING! Your password will be stored unencrypted in ~/.docker/config.json.
   # Login Succeeded
   ```

> **triangle-alert** Avoid committing `~/.docker/config.json` to version control.\
  Store credentials securely (e.g., using a secrets manager).

2. **Create a Kubernetes Secret** of type `docker-registry` so worker nodes can pull the image:
   ```bash theme={null}
   kubectl create secret docker-registry regcred \
     --docker-server=private-registry.io \
     --docker-username=registry-user \
     --docker-password=registry-password \
     --docker-email=registry-user@org.com
   ```

3. **Reference the Secret** in your Pod spec under `imagePullSecrets`:
   ```yaml theme={null}
   apiVersion: v1
   kind: Pod
   metadata:
     name: internal-app-pod
   spec:
     containers:
       - name: internal-app
         image: private-registry.io/apps/internal-app
     imagePullSecrets:
       - name: regcred
   ```
   When this Pod is scheduled, the kubelet uses the Secret to authenticate and pull the private image.

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/616e31b2-8442-4d08-906e-f23f831a8b0b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/913962b3-08a6-483d-aa5d-9aca945afd44)
