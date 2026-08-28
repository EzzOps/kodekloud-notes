# EKS EBSElastic Block Store

Source: https://notes.kodekloud.com/docs/AWS-EKS/EKS-Storage/EKS-EBSElastic-Block-Store/page

This guide explores attaching AWS Elastic Block Store volumes to Amazon EKS clusters, covering storage types, EBS CSI driver installation, and practical examples.

**Durable block storage for Kubernetes on AWS**

In this guide, we'll explore how to attach AWS Elastic Block Store (EBS) volumes to Amazon EKS clusters. Topics include ephemeral vs durable storage, EBS CSI driver installation, StorageClasses, and a StatefulSet practical example.

## Ephemeral vs Durable Storage

Kubernetes supports different storage options:

* `emptyDir`: creates a temporary directory on the node’s root disk. Data is lost when the Pod terminates.
* `PersistentVolume`: backed by durable storage outside the Pod lifecycle.

With a StatefulSet, each Replica can mount its own PersistentVolumeClaim (PVC). On Pod replacement, Kubernetes reattaches the same volume, preserving data.

<Frame>
  ![The image illustrates a Kubernetes StatefulSet with three pods, labeled as part of storage for an EKS cluster.](https://kodekloud.com/kk-media/image/upload/v1752862821/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/kubernetes-statefulset-three-pods-eks.jpg)
</Frame>

## Block Storage vs. File Storage

**Block storage** (EBS) provides raw device access, similar to adding a virtual hard drive. You format and manage the filesystem yourself.\
**File storage** (EFS, NFS) offers a network filesystem; you simply read and write files over the network.

<Frame>
  ![The image compares block storage and file storage, illustrating block storage as "plugging a hard drive" and file storage with icons for Elastic File System (EFS) and NFS.](https://kodekloud.com/kk-media/image/upload/v1752862822/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/block-storage-vs-file-storage-diagram.jpg)
</Frame>

| Storage Type  | AWS Service | Use Case                 | Characteristics                     |
| ------------- | ----------- | ------------------------ | ----------------------------------- |
| Block Storage | EBS         | Databases, stateful apps | Low-latency, formatable, AZ-bound   |
| File Storage  | EFS, NFS    | Shared file access       | POSIX-compliant, multi-AZ, scalable |

## Root Drive and Local Storage

Every EKS node boots from an EBS root volume. While this acts like local storage, it still operates within a single Availability Zone (AZ).

<Frame>
  ![The image illustrates the concept of Elastic Block Storage (EBS), showing a root hard drive connected to local storage within a node, represented by gears.](https://kodekloud.com/kk-media/image/upload/v1752862823/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/elastic-block-storage-root-drive-gears.jpg)
</Frame>

## Availability Zone Constraints

EBS volumes are AZ-specific. If a node mounts an EBS volume in AZ `us-east-1a` and terminates, a replacement node in AZ `us-east-1b` *cannot* attach that volume.

<Frame>
  ![The image illustrates a diagram of Elastic Block Storage (EBS) showing a connection between an EBS volume and a virtual machine (VM) within an availability zone, with a red cross indicating a disconnection.](https://kodekloud.com/kk-media/image/upload/v1752862824/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/ebs-volume-vm-connection-diagram.jpg)
</Frame>

<Frame>
  ![The image illustrates an Elastic Block Storage (EBS) setup within the "us-east-1" region, showing an autoscaler selecting a node with a DB instance and EBS volume in one of the availability zones.](https://kodekloud.com/kk-media/image/upload/v1752862825/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/ebs-setup-us-east-1-autoscaler-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  Pod scheduling may fail if the EBS volume cannot attach in a different AZ. Use proper `volumeBindingMode` or restrict node scheduling to the same AZ.
</Callout>

## EBS Volume Types and Performance

| Volume Type | Description                  | Use Case                               |
| ----------- | ---------------------------- | -------------------------------------- |
| gp2         | General Purpose SSD          | Cost-effective, standard workloads     |
| gp3         | Next-gen General Purpose SSD | Lower cost per GB, higher throughput   |
| io1/io2     | Provisioned IOPS SSD         | Latency-sensitive, high-IOPS databases |

EBS provides low-latency block storage within an AZ and scales up to multiple terabytes.

<Frame>
  ![The image illustrates three types of EBS volumes: gp2, gp3, and IO, highlighting their capacity to store terabytes of information and their characteristics such as common usage and faster throughputs.](https://kodekloud.com/kk-media/image/upload/v1752862827/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/ebs-volumes-gp2-gp3-io-diagram.jpg)
</Frame>

### Faster Local Storage

Instance store volumes (NVMe) offer the lowest latency but are *ephemeral*—data is lost on instance termination.

<Frame>
  ![The image shows a comparison of faster volumes, featuring NVMe Drives and Local Volume, each represented by an icon.](https://kodekloud.com/kk-media/image/upload/v1752862828/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/faster-volumes-nvme-local-comparison.jpg)
</Frame>

## Snapshots and Data Protection

EBS supports incremental snapshots to Amazon S3, enabling point-in-time backups and restores. This integration is ideal for disaster recovery and compliance.

## AWS EBS CSI Driver

Amazon EKS employs the [Container Storage Interface (CSI)](https://kubernetes-csi.github.io/docs/) to provision EBS volumes. Installing the AWS EBS CSI driver deploys:

1. **Controller (Deployment):** Manages lifecycle operations (Create/Delete) via AWS APIs
2. **Node DaemonSet:** Handles volume attachments and mounts on each node

<Frame>
  ![The image illustrates the Container Storage Interface (CSI) with a Kubernetes cluster, AWS CSI Driver, AWS EBS, and components like Controller and Driver.](https://kodekloud.com/kk-media/image/upload/v1752862829/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/csi-kubernetes-aws-ebs-diagram.jpg)
</Frame>

The driver includes predefined StorageClasses for different volume types and binding modes:

<Frame>
  ![The image illustrates the Container Storage Interface (CSI) with AWS CSI Driver, showing the interaction between storage classes, EBS volume, and a pod.](https://kodekloud.com/kk-media/image/upload/v1752862830/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/csi-aws-driver-storage-classes-diagram.jpg)
</Frame>

### Verifying the CSI Driver

Check the `kube-system` namespace to ensure the EBS CSI controller and node plugins are running:

```bash theme={null}
kubectl get pods -n kube-system
```

```plain theme={null}
NAME                    READY   STATUS    RESTARTS   AGE
aws-node-xxxxx          2/2     Running   0          90m
coredns-xxxxx           1/1     Running   0          100m
ebs-csi-controller-xxx  5/5     Running   0          45m
ebs-csi-node-xxx        3/3     Running   0          45m
```

Inspect the controller Pod for environment settings like `AWS_STS_REGIONAL_ENDPOINTS=regional`:

<Frame>
  ![The image shows a terminal window displaying details of a Kubernetes pod named "ebs-csi-controller" running in the "kube-system" namespace, including its status, IP address, and container information.](https://kodekloud.com/kk-media/image/upload/v1752862831/notes-assets/images/AWS-EKS-EKS-EBSElastic-Block-Store/kubernetes-pod-ebs-csi-controller-details.jpg)
</Frame>

## Default StorageClasses

After installation, list the StorageClasses:

```bash theme={null}
kubectl get storageclasses
```

```plain theme={null}
NAME                PROVISIONER            RECLAIMPOLICY   VOLUMEBINDINGMODE        ALLOWVOLUMEEXPANSION   AGE
gp2                 kubernetes.io/aws-ebs  Delete          WaitForFirstConsumer     false                  100m
gp3 (default)       ebs.csi.aws.com        Delete          WaitForFirstConsumer     true                   45m
gp3-encrypted       ebs.csi.aws.com        Delete          WaitForFirstConsumer     true                   45m
```

<Callout icon="lightbulb">
  `WaitForFirstConsumer` delays volume provisioning until a Pod is scheduled, ensuring the volume is created in the correct AZ.
</Callout>

At this point, no PersistentVolumes exist until PVCs are requested:

```bash theme={null}
kubectl get persistentvolumes --all-namespaces
```

```plain theme={null}
No resources found
```

## StatefulSet Example

Deploy a StatefulSet that requests a 16 Gi EBS volume via the `gp2` StorageClass:

```yaml theme={null}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: alpine
spec:
  selector:
    matchLabels:
      app: alpine
  serviceName: alpine
  replicas: 1
  template:
    metadata:
      labels:
        app: alpine
    spec:
      containers:
      - name: alpine
        image: public.ecr.aws/docker/library/alpine:latest
        command: ["sh", "-c", "sleep 1d"]
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      storageClassName: gp2
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 16Gi
```

Apply and verify the PVC:

```bash theme={null}
kubectl apply -f alpine-statefulset.yaml
kubectl get pvc
```

```plain theme={null}
NAME           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-alpine-0  Bound    pvc-7f223e3d-ee49-41ba-d46a-764ab5c14bdb  16Gi       RWO            gp2            30s
```

## Verifying the Mounted Volume

Connect to the Alpine Pod and confirm the `/data` mount:

```bash theme={null}
kubectl get pods
kubectl exec -it alpine-0 -- /bin/sh
```

```bash theme={null}
df -h /data
```

```plain theme={null}
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1   15.9Gi   24K  15.9Gi   0% /data
```

## Persistence Across Pod Restarts

Create a test file, delete the Pod, and ensure data persists:

```bash theme={null}
