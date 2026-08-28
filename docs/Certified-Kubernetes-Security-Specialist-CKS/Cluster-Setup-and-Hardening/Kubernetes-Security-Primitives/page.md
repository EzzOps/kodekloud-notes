# kubelet.service file snippet
ExecStart=/usr/local/bin/kubelet \\
  --container-runtime=docker \\
  --image-pull-progress-deadline=2m \\
  --kubeconfig=/var/lib/kubelet/kubeconfig \\
  --network-plugin=cni \\
  --register-node=true \\
  --v=2 \\
  --cluster-domain=cluster.local \\
  --file-check-frequency=0s \\
  --healthz-port=10248 \\
  --cluster-dns=10.96.0.10 \\
  --http-check-frequency=0s \\
  --sync-frequency=0s \\
```

Starting with version 1.10, many parameters previously passed via command-line flags have been migrated into a dedicated Kubelet configuration file. This file, known as the Kubelet configuration, simplifies deployment and management.

Below is an updated example demonstrating how to configure the Kubelet service to use a remote container runtime:

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.20.0/bin/linux/amd64/kubelet
```

```bash theme={null}
# kubelet.service file snippet
[Unit]
Description=kubelet

[Service]
ExecStart=/usr/local/bin/kubelet \\
  --container-runtime=remote \\
  --image-pull-progress-deadline=2m \\
  --kubeconfig=/var/lib/kubelet/kubeconfig \\
  --network-plugin=cni \\
  --register-node=true \\
  -v=2 \\
  --cluster-domain=cluster.local \\
  --file-check-frequency=0s \\
  --healthz-port=10248 \\
  --cluster-dns=10.96.0.10 \\
  --http-check-frequency=0s \\
  --sync-frequency=0s
```

```yaml theme={null}
# kubelet-config.yaml file snippet
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDomain: cluster.local
fileCheckFrequency: 0s
healthzPort: 10248
clusterDNS:
  - 10.96.0.10
httpCheckFrequency: 0s
syncFrequency: 0s
```

When initiating the Kubelet service, specify the path to the configuration file using the `--config` flag. Notice that parameters are defined using camel case (e.g., `httpCheckFrequency`) rather than the command-line flag style (`http-check-frequency`). Also, note that if the same parameter is set in both the command line and the configuration file, the command-line value takes precedence.

<Callout icon="lightbulb">
  Although `kubeadm` does not install the Kubelet, it can manage Kubelet configuration files across worker nodes during the `kubeadm join` process.
</Callout>

To inspect the running Kubelet process and view its configuration settings, check the process details and the configuration file contents. For example:

```bash theme={null}
ps -aux | grep kubelet
```

```bash theme={null}
# Example output of /var/lib/kubelet/config.yaml
apiVersion: kubelet.config.k8s.io/v1beta1
clusterDNS:
- 10.96.0.10
clusterDomain: cluster.local
cpuManagerReconcilePeriod: 0s
evictionPressureTransitionPeriod: 0s
fileCheckFrequency: 0s
healthzBindAddress: 127.0.0.1
healthzPort: 10248
httpCheckFrequency: 0s
imageMinimumGCAge: 0s
kind: KubeletConfiguration
nodeStatusReportFrequency: 0s
nodeStatusUpdateFrequency: 0s
rotateCertificates: true
runtimeRequestTimeout: 0s
staticPodPath: /etc/kubernetes/manifests
streamingConnectionIdleTimeout: 0s
```

***

## Kubelet Security

Ensuring that the Kubelet only responds to authenticated requests from the kube-apiserver is critical for the security of your cluster. By default, the Kubelet serves on two distinct ports:

1. **Port 10250:** Provides full API access.
2. **Port 10255:** Offers a read-only API for metrics and system data.

By default, anonymous access is permitted to these APIs. For example, running the following command returns a list of pods running on a node:

<Frame>
  ![The image shows a table listing Kubelet ports 10250 and 10255, describing their API access levels: full access and unauthenticated read-only access, respectively.](https://kodekloud.com/kk-media/image/upload/v1752871367/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Kubelet-Security/frame_370.jpg)
</Frame>

```bash theme={null}
curl -sk http://localhost:10250/pods
```

You can also access additional endpoints (e.g., `/logs/syslog`) for node system log inspection. The Kubelet API exposes multiple functions, including node health checks, metrics, port forwarding, and command execution in containers.

The service running on port 10255, however, provides unauthenticated, read-only access. This poses a security risk because anyone with network access could potentially view sensitive data.

***

### Securing the Kubelet

To enhance security, every request to the Kubelet must be properly authenticated and authorized before being processed.

#### 1. Disabling Anonymous Authentication

By default, the Kubelet treats unauthenticated requests as anonymous, using the credentials `system:anonymous` and group `system:unauthenticated`. To disable anonymous access, update the Kubelet service configuration using the `--anonymous-auth=false` flag:

```bash theme={null}
# kubelet.service snippet
ExecStart=/usr/local/bin/kubelet \\
...
--anonymous-auth=false \\
...
```

Alternatively, you can configure this setting within the Kubelet configuration YAML file:

```yaml theme={null}
# kubelet-config.yaml snippet
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous:
    enabled: false
```

Disabling anonymous authentication is best practice. Once disabled, ensure you enable a supported authentication mechanism.

#### 2. Certificate-Based Authentication

Certificate-based authentication provides secure access by using a pair of certificates. Configure the Kubelet to use the CA certificate with the `--client-ca-file` parameter in the service file or within the Kubelet configuration:

```bash theme={null}
# kubelet.service snippet
ExecStart=/usr/local/bin/kubelet \\
    --client-ca-file=/path/to/ca.crt \\
```

```yaml theme={null}
# kubelet-config.yaml snippet
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  x509:
    clientCAFile: /path/to/ca.crt
```

When performing API calls (for example, with curl), include the client certificate and key since the kube-apiserver is treated as a client from the Kubelet’s perspective. Below is an example configuration for the kube-apiserver service:

```bash theme={null}
# Example command lines and configuration snippets
ExecStart=/usr/local/bin/kubelet \\
    --client-ca-file=/path/to/ca.crt \\

curl -sk https://localhost:10250/pods/ --key kubelet-key.pem --cert kubelet-cert.pem

# Example kube-apiserver.service snippet
[Service]
ExecStart=/usr/local/bin/kube-apiserver \\
    --kubelet-client-certificate=/path/to/kubelet-cert.pem \\
    --kubelet-client-key=/path/to/kubelet-key.pem \\
```

<Callout icon="triangle-alert">
  If neither certificate-based nor token-based authentication explicitly rejects a request, the Kubelet will fallback to treating it as anonymous. Always ensure your authentication mechanisms are correctly configured.
</Callout>

#### 3. Authorization

After authenticating requests, the Kubelet determines what actions or API resources a user can access. By default, the authorization mode is set to `AlwaysAllow`, meaning all requests are permitted. To secure the Kubelet, configure the authorization mode to `Webhook` so the Kubelet consults the API server to determine if a request should be allowed:

```bash theme={null}
# kubelet.service snippet
ExecStart=/usr/local/bin/kubelet \\
  ...
  --authorization-mode=Webhook \\
  ...
```

```yaml theme={null}
# kubelet-config.yaml snippet
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authorization:
  mode: Webhook
```

#### 4. Managing the Read-Only Port (10255)

The read-only port (10255) can expose sensitive metrics without authentication. It is advisable to disable this port if not explicitly needed. You can disable it by setting the port value to zero in either the service file or configuration file:

```bash theme={null}
curl -sk http://localhost:10255/metrics
```

```bash theme={null}
# kubelet.service snippet
ExecStart=/usr/local/bin/kubelet \\
  ...
  --read-only-port=10255 \\
  ...
```

```yaml theme={null}
# kubelet-config.yaml snippet
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
readOnlyPort: 0
```

Disabling the read-only port enhances security by preventing unauthorized access to node metrics and other system data.

***

## Summary

In this lesson, we reviewed critical aspects of securing the Kubelet:

* Disable anonymous authentication by setting `--anonymous-auth=false` or configuring it within the YAML file.
* Implement a secure authentication mechanism with certificate-based authentication by setting the `clientCAFile` parameter.
* Configure authorization using the `Webhook` mode so that the API server validates requests.
* Disable the read-only port (10255) by setting it to zero if unauthenticated access is not desired.

By applying these security measures, your Kubelet will be significantly more resilient to unauthorized access. Now, proceed to the labs and practice implementing Kubelet security in your Kubernetes environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/eac6dac8-4481-4138-96ef-a2135f20e05e/lesson/da297ecd-2762-48ed-9eb7-c6556bb9658d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/eac6dac8-4481-4138-96ef-a2135f20e05e/lesson/3d54f860-f552-48a2-8ac2-886bacd00893" />
</CardGroup>


# Kubernetes Security Primitives

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Cluster-Setup-and-Hardening/Kubernetes-Security-Primitives/page

This article provides an overview of critical security measures in Kubernetes, focusing on securing cluster hosts, API server access, intra-cluster communications, and network policies.

Welcome to our comprehensive guide on Kubernetes security primitives. As Kubernetes has become the industry standard for hosting production-grade applications, ensuring robust security practices is more important than ever. This article provides a high-level overview of critical security measures in Kubernetes, with detailed explorations to follow in subsequent posts.

## Securing the Cluster Hosts

Before diving into the intricacies of Kubernetes security, it is essential to secure the underlying infrastructure. Ensure that all hosts in your Kubernetes cluster are protected by:

* Disabling root access and password-based authentication.
* Enabling SSH key-based authentication.
* Implementing additional security measures to protect the physical or virtual infrastructure hosting Kubernetes.

<Callout icon="triangle-alert">
  If the underlying infrastructure is compromised, the security of the entire Kubernetes cluster is at risk.
</Callout>

## Kubernetes API Server: The Entry Point

At the core of Kubernetes operations lies the kube API server. Users interact with the cluster through the `kubectl` utility or direct API calls. This interaction is crucial because it governs nearly all cluster operations. Therefore, two fundamental questions arise:

1. Who can access the cluster?
2. What actions can they perform?

### Authentication

Access to the API server is regulated by robust authentication mechanisms. Kubernetes supports multiple methods, including:

* Static files with user IDs and passwords
* Tokens
* Certificates
* Integrations with external providers such as LDAP
* Service accounts for machine-to-machine communications

These diverse approaches ensure that every connection is verified, offering flexibility and security simultaneously.

<Frame>
  ![The image is a slide titled "Authentication" listing access methods: username/password, username/tokens, certificates, LDAP, and service accounts.](https://kodekloud.com/kk-media/image/upload/v1752871371/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Kubernetes-Security-Primitives/frame_120.jpg)
</Frame>

### Authorization

Once users or services are authenticated, authorization mechanisms determine their permitted actions on the cluster. Kubernetes primarily uses Role-Based Access Control (RBAC) to map users to groups with specific permissions. Other authorization modules available include:

* Attribute-Based Access Control (ABAC)
* Node Authorization
* Webhook-based authorization

These systems work together to ensure that every action within the cluster is scrutinized and allowed only if it aligns with the defined permissions.

<Frame>
  ![The image lists types of authorization: RBAC, ABAC, Node Authorization, and Webhook Mode, under the heading "Authorization: What can they do?"](https://kodekloud.com/kk-media/image/upload/v1752871373/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Kubernetes-Security-Primitives/frame_140.jpg)
</Frame>

## Securing Intra-Cluster Communications

A critical element of Kubernetes security involves securing communications between various cluster components. All interactions between components—such as the etcd cluster, kube controller manager, scheduler, API server, and worker node components (including kubelet and kube-proxy)—are protected using TLS encryption.

<Callout icon="lightbulb">
  Detailed instructions on setting up certificates for secure communications will be provided in a dedicated section.
</Callout>

<Frame>
  ![The image illustrates the relationship between Kubernetes components using TLS certificates, centered around the Kube ApiServer, connecting to ETCD Cluster, Kubelet, Kube Proxy, Kube Controller Manager, and Kube Scheduler.](https://kodekloud.com/kk-media/image/upload/v1752871374/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Kubernetes-Security-Primitives/frame_160.jpg)
</Frame>

## Network Policies Within the Cluster

By default, pods within a Kubernetes cluster can communicate freely with one another. To restrict unwanted access and tighten security, network policies can be implemented. These policies enable you to control traffic flow between pods and are an integral part of securing inter-application communications within the cluster.

<Frame>
  ![The image illustrates network policies using a diagram of four devices, each containing colored circles and interconnected by dashed lines.](https://kodekloud.com/kk-media/image/upload/v1752871375/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Kubernetes-Security-Primitives/frame_190.jpg)
</Frame>

## In Summary

This article has provided an overview of the key security primitives in Kubernetes:

* Securing cluster hosts
* Strong authentication and authorization methods for the API server
* Using TLS encryption for intra-cluster communications
* Implementing network policies for pod-to-pod communication

We will explore these topics in much greater detail in upcoming articles. Stay tuned as we dive deeper into each security aspect to help you ensure that your Kubernetes environment remains secure and resilient.

For more Kubernetes best practices and security tips, continue following our in-depth guides and tutorials.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/eac6dac8-4481-4138-96ef-a2135f20e05e/lesson/c4389944-7651-4660-98bb-d454889d71af" />
</CardGroup>
