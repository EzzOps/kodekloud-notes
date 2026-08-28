# /etc/systemd/system/kubelet.service
[Unit]
Description=Kubelet Service
After=network.target

[Service]
ExecStart=/usr/local/bin/kubelet \
  --container-runtime=remote \
  --image-pull-progress-deadline=2m \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --network-plugin=cni \
  --register-node=true \
  --cluster-domain=cluster.local \
  --cluster-dns=10.96.0.10 \
  --v=2

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

<Callout icon="lightbulb">
  With **kubeadm** (v1.10+), most flags migrate into `/var/lib/kubelet/config.yaml` and are maintained automatically during `kubeadm join`.
</Callout>

### Dedicated Config File

```yaml theme={null}
# /var/lib/kubelet/config.yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDomain: cluster.local
clusterDNS:
  - 10.96.0.10
fileCheckFrequency: 0s
httpCheckFrequency: 0s
syncFrequency: 0s
healthzPort: 10248
```

Add `--config=/var/lib/kubelet/config.yaml` to your service’s `ExecStart`. Command-line flags will always override the YAML settings.

***

## 2. Inspecting the Active Configuration

On any worker node, verify the kubelet invocation and configuration:

```bash theme={null}
ps aux | grep kubelet
# e.g. /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf \
#       --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf \
#       --config=/var/lib/kubelet/config.yaml \
#       --cgroup-driver=systemd \
#       --network-plugin=cni
```

```bash theme={null}
cat /var/lib/kubelet/config.yaml
# apiVersion: kubelet.config.k8s.io/v1beta1
# kind: KubeletConfiguration
# authentication:
#   anonymous:
#     enabled: false
#   x509:
#     clientCAFile: /path/to/ca.crt
# authorization:
#   mode: Webhook
# readOnlyPort: 0
# rotateCertificates: true
# staticPodPath: /etc/kubernetes/manifests
```

***

## 3. Kubelet API Endpoints

| Port  | Endpoint Type     | Access                     | Recommendation               |
| ----- | ----------------- | -------------------------- | ---------------------------- |
| 10250 | Secure API        | TLS + AuthN/AuthZ required | Keep enabled and locked down |
| 10255 | Read-only metrics | Unauthenticated, HTTP only | Disable in production        |

<Frame>
  ![The image shows a table titled "Kubelet" with two ports, 10250 and 10255, and their descriptions regarding API access.](https://kodekloud.com/kk-media/image/upload/v1752880767/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Securing-the-Kubelet/kubelet-ports-api-access-table.jpg)
</Frame>

Anyone with network access to port 10255 can scrape metrics:

```bash theme={null}
curl -s http://localhost:10255/metrics | head -n 5
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
# process_cpu_seconds_total 0.01
```

<Callout icon="triangle-alert">
  Port `10255` is unauthenticated and exposes sensitive metrics. It should always be disabled in production.
</Callout>

***

## 4. Authentication Configuration

By default, the kubelet permits anonymous requests (`system:anonymous`). Disable this to force clients to present credentials.

### Disable Anonymous Access

**Via flags** in your `systemd` unit:

```ini theme={null}
--anonymous-auth=false \
--client-ca-file=/path/to/ca.crt
```

**Or** in `/var/lib/kubelet/config.yaml`:

```yaml theme={null}
authentication:
  anonymous:
    enabled: false
  x509:
    clientCAFile: /path/to/ca.crt
```

### Certificate-Based Client Auth

1. Generate a CA and sign a kubelet-serving certificate.

2. Distribute the CA bundle with `--client-ca-file=/path/to/ca.crt`.

3. Test with:

   ```bash theme={null}
   curl -s --key kubelet-key.pem --cert kubelet-cert.pem \
     https://localhost:10250/pods
   ```

4. Ensure the **API Server** has credentials to call the kubelet:

   ```ini theme={null}
   # /etc/systemd/system/kube-apiserver.service
   --kubelet-client-certificate=/path/to/kubelet-client.crt \
   --kubelet-client-key=/path/to/kubelet-client.key
   ```

***

## 5. Authorization Modes

Out of the box, the kubelet uses `AlwaysAllow` (no authorization). Switch to `Webhook` to delegate decisions to the API Server.

```ini theme={null}
# Flags
--authorization-mode=Webhook
```

```yaml theme={null}
# config.yaml
authorization:
  mode: Webhook
```

Each kubelet request is then validated via the API Server’s SubjectAccessReview endpoint.

***

## 6. Disabling the Read-Only Port

To completely turn off port `10255`:

```ini theme={null}
# Flags
--read-only-port=0
```

```yaml theme={null}
# config.yaml
readOnlyPort: 0
```

<Callout icon="triangle-alert">
  Always set `readOnlyPort: 0` in production to prevent unauthenticated access to metrics.
</Callout>

***

## 7. Summary of Hardening Steps

| Security Aspect      | Recommended Setting             |
| -------------------- | ------------------------------- |
| Anonymous Auth       | `--anonymous-auth=false`        |
| TLS Client AuthN     | `clientCAFile: /path/to/ca.crt` |
| Authorization        | `--authorization-mode=Webhook`  |
| Read-Only Port       | `readOnlyPort: 0`               |
| Certificate Rotation | `rotateCertificates: true`      |

### Example Final `kubelet.service` Snippet

```ini theme={null}
ExecStart=/usr/local/bin/kubelet \
  --config=/var/lib/kubelet/config.yaml \
  --anonymous-auth=false \
  --client-ca-file=/path/to/ca.crt \
  --authorization-mode=Webhook \
  --read-only-port=0
```

### Example Final `config.yaml`

```yaml theme={null}
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous:
    enabled: false
  x509:
    clientCAFile: /path/to/ca.crt
authorization:
  mode: Webhook
readOnlyPort: 0
rotateCertificates: true
```

You’re now ready to apply these settings and secure the kubelet in your cluster!

***

## Links and References

* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [Kubelet Configuration Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
* [Kubeadm Configuration](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/ca772db3-53aa-44c1-b424-3d32a046b683/lesson/01b01297-c7b8-409c-b37e-10af456416fd" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/ca772db3-53aa-44c1-b424-3d32a046b683/lesson/3d54f860-f552-48a2-8ac2-886bacd00893" />
</CardGroup>


# Storage

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Cluster-Component-Security/Storage/page

This article discusses securing storage in Kubernetes, focusing on encryption, access control, policy enforcement, backup strategies, and monitoring for data integrity and security.

Securing storage is critical for maintaining data integrity, confidentiality, and availability in your Kubernetes clusters. Pods access storage through Persistent Volumes (PVs) and Persistent Volume Claims (PVCs). Misconfigurations can lead to unauthorized data exposure, interception of unencrypted traffic, or even permanent data loss.

<Frame>
  ![The image illustrates a Kubernetes storage setup with nodes and persistent volumes, highlighting a security risk due to misconfigured access leading to potential exposure of sensitive data.](https://kodekloud.com/kk-media/image/upload/v1752880768/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/kubernetes-storage-setup-security-risk.jpg)
</Frame>

<Callout icon="triangle-alert">
  Unencrypted or improperly scoped storage access can allow attackers to read, modify, or destroy sensitive data. Always review your storage configurations and access policies.
</Callout>

## Encrypting Data at Rest and in Transit

Encrypting both disk data and network traffic prevents unauthorized access and eavesdropping. Kubernetes natively supports etcd encryption, and most cloud providers offer disk-level encryption:

<Frame>
  ![The image shows icons representing three cloud storage services: AWS EBS, Azure Disk Storage, and Google Cloud Persistent Disk, under the title "Using Encryption."](https://kodekloud.com/kk-media/image/upload/v1752880769/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/using-encryption-cloud-storage-icons.jpg)
</Frame>

| Provider                     | Encryption Feature                                            | Reference                                                                                                  |
| ---------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| AWS EBS                      | Customer-managed keys for EBS volumes                         | [https://aws.amazon.com/ebs](https://aws.amazon.com/ebs)                                                   |
| Azure Disk Storage           | Server-side encryption with platform or customer-managed keys | [https://azure.microsoft.com/services/managed-disks/](https://azure.microsoft.com/services/managed-disks/) |
| Google Cloud Persistent Disk | CMEK/Customer-supplied encryption keys                        | [https://cloud.google.com/persistent-disk](https://cloud.google.com/persistent-disk)                       |

To enable encryption on AWS EBS via a custom StorageClass:

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: encrypted-ebs
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  encrypted: "true"
```

<Callout icon="lightbulb">
  Ensure your cloud IAM policies grant permissions to use the specified encryption keys.
</Callout>

## Role-Based Access Control (RBAC) for Storage

Restrict access to StorageClasses, PVs, and PVCs using Kubernetes RBAC. Define granular roles and bind them to users or service accounts.

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pvc-reader
rules:
  apiGroups: [""]
  resources: ["persistentvolumeclaims"]
  verbs: ["get", "list"]
```

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pvc-binding
  namespace: default
subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pvc-reader
  apiGroup: rbac.authorization.k8s.io
```

By scoping roles to namespaces and specific verbs (`get`, `list`, `create`, `delete`), you minimize the blast radius of compromised credentials.

## StorageClasses and Policy Enforcement

StorageClasses let you standardize storage parameters—such as encryption, IOPS, and backup policies—across your cluster.

<Frame>
  ![The image illustrates the concept of storage in Kubernetes, showing nodes within a cluster, storage classes, persistent volumes, and features like encryption, IOPS limits, and backup policies.](https://kodekloud.com/kk-media/image/upload/v1752880770/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/kubernetes-storage-concept-diagram.jpg)
</Frame>

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: secure-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  encrypted: "true"
  iops: "3000"
```

Key benefits:

* Decouple storage parameters from application manifests
* Enforce organizational policies (encryption, throughput, retention)
* Simplify provisioning for developers

## Backup and Disaster Recovery

Implement automated backups and cross-cluster replication to guard against data loss, corruption, and ransomware.

<Frame>
  ![The image is a presentation slide titled "Implementing Backup and Disaster Recovery" featuring the Velero logo and a list of use cases related to backup and disaster recovery.](https://kodekloud.com/kk-media/image/upload/v1752880771/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/implementing-backup-disaster-recovery-velero.jpg)
</Frame>

| Tool     | Description                                              | Link                                           |
| -------- | -------------------------------------------------------- | ---------------------------------------------- |
| Velero   | Open source backup, restore, and disaster recovery       | [https://velero.io](https://velero.io)         |
| Portworx | Enterprise-grade storage management and DR               | [https://portworx.com](https://portworx.com)   |
| OpenEBS  | Containerized storage with snapshot and clone features   | [https://openebs.io](https://openebs.io)       |
| Kasten   | Policy-driven backup and mobility for Kubernetes volumes | [https://www.kasten.io](https://www.kasten.io) |

## Monitoring Storage Health and Security

Track storage metrics and access patterns to detect anomalies early. Use Prometheus for data collection and Grafana for visualization.

<Frame>
  ![The image shows a Kubernetes monitoring dashboard with metrics on clusters, nodes, namespaces, workloads, pods, and containers, using Prometheus and Grafana.](https://kodekloud.com/kk-media/image/upload/v1752880773/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/kubernetes-monitoring-dashboard-prometheus-grafana.jpg)
</Frame>

Important metrics:

* Volume latency and throughput
* PVC capacity versus usage
* I/O error rates
* Unauthorized mount or delete attempts

Integrate alerting rules to notify on threshold breaches or suspicious activity.

## Summary

<Frame>
  ![The image illustrates a Kubernetes storage setup, showing nodes within a cluster accessing a persistent volume, with emphasis on using RBAC for access control, regular backups, and data encryption at rest.](https://kodekloud.com/kk-media/image/upload/v1752880774/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Storage/kubernetes-storage-setup-rbac-backups.jpg)
</Frame>

In this lesson, you learned how to:

* Encrypt data at rest and in transit
* Enforce RBAC for storage resources
* Standardize storage parameters with StorageClasses
* Automate backups and disaster recovery
* Monitor storage metrics and access patterns

For deeper dives, see the [Kubernetes Storage Concepts](https://kubernetes.io/docs/concepts/storage/) and the [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/overview/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/ca772db3-53aa-44c1-b424-3d32a046b683/lesson/676d9ab1-8a6f-48ca-9b46-3f9502ab9981" />
</CardGroup>
