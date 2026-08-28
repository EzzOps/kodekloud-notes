# kube-apiserver.service
ExecStart=/usr/local/bin/kube-apiserver \\
  --advertise-address=${INTERNAL_IP} \\
  --allow-privileged=true \\
  --apiserver-count=3 \\
  --authorization-mode=Node,RBAC \\
  --bind-address=0.0.0.0 \\
  --client-ca-file=/var/lib/kubernetes/ca.pem \\
  --enable-admission-plugins=Initializers,NamespaceLifecycle,NodeRestriction,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota \\
  --enable-swagger-ui=true \\
  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
  --etcd-certfile=/var/lib/kubernetes/kubernetes.pem \\
  --etcd-keyfile=/var/lib/kubernetes/kubernetes-key.pem \\
  --etcd-servers=https://127.0.0.1:2379 \\
  --event-ttl=1h \\
  --experimental-encryption-provider-config=/var/lib/kubernetes/encryption-config.yaml \\
  --kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
  --kubelet-client-certificate=/var/lib/kubernetes/kubernetes.pem \\
  --kubelet-client-key=/var/lib/kubernetes/kubernetes-key.pem \\
  --kubelet-https=true \\
  --runtime-config=api/all \\
  --service-account-key-file=/var/lib/kubernetes/service-account.pem \\
  --service-cluster-ip-range=10.32.0.0/24 \\
  --service-node-port-range=30000-32767 \\
  --v=2
```

The configuration includes several certificate-related options, securing communication channels between various Kubernetes components. In upcoming sections, we will take a deeper look at SSL/TLS certificates and their role in ensuring secure interactions.

## Verifying the Deployment

For clusters set up with kube-admin tools, the Kube API Server is deployed as a pod in the kube-system namespace. To inspect these pods, run:

```bash theme={null}
kubectl get pods -n kube-system
```

Expected output may include:

```plaintext theme={null}
NAMESPACE      NAME                                        READY   STATUS    RESTARTS   AGE
kube-system    coredns-78fcdf6894-hwrq9                    1/1     Running   0          16m
kube-system    coredns-78fcdf6894-rzhjr                    1/1     Running   0          16m
kube-system    etcd-master                                 1/1     Running   0          15m
kube-system    kube-apiserver-master                       1/1     Running   0          15m
kube-system    kube-controller-manager-master              1/1     Running   0          15m
kube-system    kube-proxy-lzt6f                            1/1     Running   0          16m
kube-system    kube-proxy-zm5qd                            1/1     Running   0          15m
kube-system    kube-scheduler-master                       1/1     Running   0          15m
kube-system    weave-net-29z42                             2/2     Running   1          16m
kube-system    weave-net-snm1l                             2/2     Running   1          16m
```

For non-kube-admin setups, you can examine the container command options directly within the pod manifest. Here’s an excerpt from a pod definition:

```yaml theme={null}
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --advertise-address=172.17.0.32
    - --allow-privileged=true
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --disable-admission-plugins=PersistentVolumeLabel
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
    - --insecure-port=0
    - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
    - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
    - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
    - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
    - --requestheader-allowed-names=front-proxy-client
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --requestheader-extra-headers-prefix=X-Remote-Extra-
    - --requestheader-group-headers=X-Remote-Group
    - --requestheader-username-headers=X-Remote-User
```

Another way to review the active API Server configuration is by checking the systemd service file on the master node:

```bash theme={null}
cat /etc/systemd/system/kube-apiserver.service
```

An example excerpt from this file might be:

```bash theme={null}
[Service]
ExecStart=/usr/local/bin/kube-apiserver \\
  --advertise-address=${INTERNAL_IP} \\
  --allow-privileged=true \\
  --apiserver-count=3 \\
  --audit-log-maxage=30 \\
  --audit-log-maxbackup=3 \\
  --audit-log-maxsize=100 \\
  --audit-log-path=/var/log/audit.log \\
  --authorization-mode=Node,RBAC \\
  --bind-address=0.0.0.0 \\
  --client-ca-file=/var/lib/kubernetes/ca.pem \\
  --enable-admission-plugins=Initializers,NamespaceLifecycle,NodeRestriction,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota \\
  --enable-swagger-ui=true \\
  --etcd-cafile=/var/lib/kubernetes/ca.pem \\
  --etcd-certfile=/var/lib/kubernetes/kubernetes.pem \\
  --etcd-keyfile=/var/lib/kubernetes/kubernetes-key.pem \\
  --etcd-servers=https://10.240.0.10:2379,https://10.240.0.11:2379,https://10.240.0.12:2379 \\
  --event-ttl=1h \\
  --experimental-encryption-provider-config=/var/lib/kubernetes/encryption-config.yaml \\
  --kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
  --kubelet-client-certificate=/var/lib/kubernetes/kubernetes.pem \\
  --kubelet-client-key=/var/lib/kubernetes/kubernetes-key.pem \\
  ...
```

## Quick Reference Table

Below is a summary of some key Kubernetes components involved in the Kube API Server workflow:

| Component       | Role                                                                                   | Command/Action Example                            |
| --------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| kubectl         | CLI tool to send API requests                                                          | `kubectl get nodes`                               |
| Kube API Server | Central component for processing, authenticating, and validating requests              | Processes API requests and interacts with etcd    |
| Scheduler       | Monitors API Server for unassigned pods and assigns them to worker nodes               | Automatically assigns node to newly created pods  |
| Kubelet         | Runs on worker nodes to manage pod lifecycle and communicate status back to API Server | Interacts with container runtime to deploy images |
| etcd            | Distributed key-value store used for saving cluster configuration                      | Stores all cluster state data                     |

## Summary

In this article, we provided an overview of the Kube API Server, its interactions with other essential components, and various methods to inspect its configuration—both through pod manifests and systemd service files. In subsequent sections, we will delve deeper into certificate management, including SSL/TLS configurations, to reinforce secure communications within your Kubernetes cluster.

<Callout icon="lightbulb">
  For a deeper understanding of Kubernetes and its components, explore the [Kubernetes Documentation](https://kubernetes.io/docs/).
</Callout>

This concludes our discussion on the Kube API Server.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/3c985954-dc27-4664-817d-bb2606967352" />
</CardGroup>


# Kube Controller Manager

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Kube-Controller-Manager/page

This guide covers the Kube Controller Managers role, configuration, and importance in managing controllers within a Kubernetes cluster.

Welcome to this comprehensive guide on the Kube Controller Manager, a vital component in Kubernetes responsible for managing a variety of controllers within your cluster. Understanding its role and configuration is crucial for ensuring a resilient and well-orchestrated Kubernetes environment.

## Overview

In Kubernetes, a controller acts like a department in an organization—each controller is tasked with handling a specific responsibility. For instance, one controller might monitor the health of nodes, while another ensures that the desired number of pods is always running. These controllers constantly observe system changes to drive the cluster toward its intended state.

The Node Controller, for example, checks node statuses every five seconds through the Kube API Server. If a node stops sending heartbeats, it is not immediately marked as unreachable; instead, there is a grace period of 40 seconds followed by an additional five minutes for potential recovery before its pods are rescheduled onto a healthy node.

### Example: Checking Node Statuses

```bash theme={null}
kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
worker-1     Ready    <none>   8d    v1.13.0
worker-2     Ready    <none>   8d    v1.13.0
```

In the case where a node fails to recover, the output might look like this:

```bash theme={null}
kubectl get nodes
NAME         STATUS     ROLES    AGE   VERSION
worker-1     Ready      <none>   8d    v1.13.0
worker-2     NotReady   <none>   8d    v1.13.0
```

Another essential controller is the Replication Controller, which ensures that the specified number of pods is maintained by creating new pods when needed. This mechanism reinforces the resilience and reliability of your Kubernetes cluster.

<Frame>
  ![The image illustrates a Kubernetes architecture with master and worker nodes, showing components like ETCD cluster, controller-manager, and kube-scheduler, alongside container ships.](https://kodekloud.com/kk-media/image/upload/v1752869721/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kube-Controller-Manager/frame_20.jpg)
</Frame>

All core Kubernetes constructs—such as Deployments, Services, Namespaces, and Persistent Volumes—rely on these controllers. Essentially, controllers serve as the "brains" behind many operations in a Kubernetes cluster.

## How Controllers Are Packaged

All individual controllers are bundled into a single process known as the Kubernetes Controller Manager. When you deploy the Controller Manager, every associated controller is started together. This unified deployment simplifies management and configuration.

## Installing and Configuring the Kube Controller Manager

To install and view the Kube Controller Manager, follow these steps:

1. Download the Kube Controller Manager from the Kubernetes release page.
2. Extract the binary and run it as a service.
3. Review the configurable options provided, which allow you to tailor its behavior.

### Downloading the Controller Manager

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-controller-manager
```

### Sample Service Configuration

Below is an example of a service file (`kube-controller-manager.service`) used to run the Controller Manager:

```bash theme={null}
ExecStart=/usr/local/bin/kube-controller-manager \
    --address=0.0.0.0 \
    --cluster-cidr=10.200.0.0/16 \
    --cluster-name=kubernetes \
    --cluster-signing-cert-file=/var/lib/kubernetes/ca.pem \
    --cluster-signing-key-file=/var/lib/kubernetes/ca-key.pem \
    --kubeconfig=/var/lib/kubernetes/kube-controller-manager.kubeconfig \
    --leader-elect=true \
    --root-ca-file=/var/lib/kubernetes/ca.pem \
    --service-account-private-key-file=/var/lib/kubernetes/service-account-key.pem \
    --service-cluster-ip-range=10.32.0.0/24 \
    --use-service-account-credentials=true \
    --v=2
```

This configuration includes additional options for the Node Controller, such as node monitor period, grace period, and eviction timeout. Additionally, you can control which controllers are enabled through the `--controllers` flag.

<Callout icon="lightbulb">
  By default, all controllers are enabled. You can selectively enable or disable controllers by using the syntax `foo` to enable and `-foo` to disable. For example, `--controllers=*,-tokencleaner` will disable the `tokencleaner` controller.
</Callout>

### Example of Specifying Controllers

```bash theme={null}
--controllers stringSlice       Default: [*]
A list of controllers to enable. '*' enables all on-by-default controllers, 'foo' enables the controller named 'foo', '-foo' disables the controller named 'foo'.
All controllers: attachdetach, bootstrapsigner, clusterrole-aggregation, cronjob, csrapproving,
csrcleaner, csrsigning, daemonset, deployment, disruption, endpoint, garbagecollector,
horizontalpodautoscaling, job, namespace, nodeipam, nodelifecycle, persistentvolume-binder,
persistentvolume-expander, podgc, pv-protection, pvc-protection, replicaset, replicationcontroller,
resourcequota, root-ca-cert-publisher, route, service, serviceaccount, serviceaccount-token, statefulset,
tokencleaner, ttl, ttl-after-finished
Disabled-by-default controllers: bootstrapsigner, tokencleaner
```

## Viewing the Controller Manager in Action

Depending on your cluster setup, the Controller Manager may run as a pod in the `kube-system` namespace (if set up using kubeadm) or as a system service. In kubeadm-based clusters, you can inspect the pod definition located in the `/etc/kubernetes/manifests` directory.

### Service Configuration Example (Non-Kubeadm Environments)

```plaintext theme={null}
[Service]
ExecStart=/usr/local/bin/kube-controller-manager \
  --address=0.0.0.0 \
  --cluster-cidr=10.200.0.0/16 \
  --cluster-name=kubernetes \
  --cluster-signing-cert-file=/var/lib/kubernetes/ca.pem \
  --cluster-signing-key-file=/var/lib/kubernetes/ca-key.pem \
  --kubeconfig=/var/lib/kubernetes/kube-controller-manager.kubeconfig \
  --leader-elect=true \
  --root-ca-file=/var/lib/kubernetes/ca.pem \
  --service-account-private-key-file=/var/lib/kubernetes/service-account-key.pem \
  --service-cluster-ip-range=10.32.0.0/24 \
  --use-service-account-credentials=true \
  --v=2
Restart=on-failure
RestartSec=5
```

### Checking the Running Process

To verify that the Kube Controller Manager is running and to inspect its active options, execute the following command on the master node:

```plaintext theme={null}
ps -aux | grep kube-controller-manager
```

An example output might be:

```plaintext theme={null}
root       1994  2.7  5.1 154360 105024 ?        Ssl  06:45   1:25 kube-controller-manager --address=127.0.0.1 --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt --cluster-signing-key-file=/etc/kubernetes/pki/ca.key --controllers=*,bootstrapsigner,tokencleaner --kubeconfig=/etc/kubernetes/controller-manager.conf --leader-elect=true --root-ca-file=/etc/kubernetes/pki/ca.crt --service-account-private-key-file=/etc/kubernetes/pki/sa.key --use-service-account-credentials=true
```

<Frame>
  ![The image illustrates a Kubernetes controller architecture, showing various controllers like Deployment, Namespace, and Node, with monitoring and timeout settings.](https://kodekloud.com/kk-media/image/upload/v1752869722/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kube-Controller-Manager/frame_150.jpg)
</Frame>

## Conclusion

This guide has provided an in-depth look at the Kube Controller Manager, detailing its critical functions in managing controllers, monitoring system changes, and ensuring the desired state within your Kubernetes cluster. By understanding and properly configuring the Controller Manager, you play a key role in maintaining a robust and scalable environment.

Stay tuned for more lessons to further enhance your Kubernetes expertise!

For additional details, you might find these resources useful:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/bc592fc3-8645-4c16-a189-7132c6c357e4" />
</CardGroup>
