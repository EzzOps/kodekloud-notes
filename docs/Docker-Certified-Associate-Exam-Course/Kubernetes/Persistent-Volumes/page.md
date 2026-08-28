# pvc-selector.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  selector:
    matchLabels:
      name: my-pv
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

```yaml theme={null}
# pv-with-label.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
  labels:
    name: my-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: <volume-id>
    fsType: ext4
```

<Frame>
  ![The image illustrates the concept of "Binding" in Kubernetes, showing various colored blocks labeled "PV" and "PVC" with icons representing storage. It also highlights key factors like "Sufficient Capacity," "Access Modes," "Volume Modes," and "Storage Class."](https://kodekloud.com/kk-media/image/upload/v1752874020/notes-assets/images/Docker-Certified-Associate-Exam-Course-Persistent-Volume-Claims/kubernetes-binding-pv-pvc-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  A PVC binds to only one PV and vice versa. If a PV is larger than the requested size, the leftover space remains unused and cannot be shared.
</Callout>

<Frame>
  ![The image illustrates the concept of binding in Kubernetes, showing the relationship between Persistent Volumes (PV) and Persistent Volume Claims (PVC), with conditions like "Pending" and criteria such as "Sufficient Capacity" and "Access Modes."](https://kodekloud.com/kk-media/image/upload/v1752874021/notes-assets/images/Docker-Certified-Associate-Exam-Course-Persistent-Volume-Claims/kubernetes-binding-pv-pvc-diagram-2.jpg)
</Frame>

## Step-by-Step: Creating a PersistentVolumeClaim

1. **Define the PVC**\
   Save the following manifest as `pvc-definition.yaml`:

   ```yaml theme={null}
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: myclaim
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 500Mi
   ```

2. **Apply the PVC**
   ```bash theme={null}
   kubectl apply -f pvc-definition.yaml
   ```

3. **Verify Status**

   ```bash theme={null}
   kubectl get pvc myclaim
   ```

   ```plaintext theme={null}
   NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES
   myclaim   Pending
   ```

   Once a matching PV is available, the PVC transitions to `Bound`:

   ```bash theme={null}
   kubectl get pvc myclaim
   ```

   ```plaintext theme={null}
   NAME      STATUS   VOLUME    CAPACITY   ACCESS MODES
   myclaim   Bound    pv-vol1   1Gi        RWO
   ```

<Callout icon="lightbulb">
  If your cluster supports dynamic provisioning, you can skip creating a PV manually. Just specify a `storageClassName` in the PVC.
</Callout>

## Reclaim Policies

When a PVC is deleted, the PV’s reclaim policy determines what happens to the underlying storage:

| Reclaim Policy   | Behavior                                                          | Use Case                                 |
| ---------------- | ----------------------------------------------------------------- | ---------------------------------------- |
| Retain (default) | PV and data are kept intact                                       | Manual cleanup or data recovery          |
| Delete           | PV and its data are deleted automatically                         | Ephemeral workloads or test environments |
| Recycle          | Data is scrubbed (basic `rm -rf /thevolume/*`) and made available | Shared test space (deprecated in v1.22)  |

To set a reclaim policy, include it in the PV spec:

```yaml theme={null}
spec:
  persistentVolumeReclaimPolicy: Delete
```

## Cleaning Up

Remove the PVC when you no longer need it:

```bash theme={null}
kubectl delete pvc myclaim
```

Depending on the reclaim policy, the PV will either be deleted, retained, or recycled.

## Links and References

* [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
* [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
* [AWS Elastic Block Store (EBS)](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/78581ed8-6a56-4ad9-a421-867cd399fd46" />
</CardGroup>


# Persistent Volumes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Persistent-Volumes/page

This article explains Persistent Volumes in Kubernetes, detailing their benefits, configuration, and how to create them for different storage backends.

Persistent Volumes (PVs) decouple storage management from Pod lifecycle, providing a cluster-wide pool of storage resources that administrators provision and developers consume via Persistent Volume Claims (PVCs). This approach centralizes configuration, improves security boundaries, and simplifies updates.

## Why Use Persistent Volumes?

When you embed volume definitions in every Pod spec, any change to storage (capacity, filesystem, reclaim policy) requires updating all manifests. PVs solve this by:

* Centralizing storage configuration in a single object
* Allowing administrators to manage capacity, access modes, and reclaim policy
* Letting developers request storage without knowing backend details

<Frame>
  ![The image illustrates the concept of Persistent Volumes (PVs) and Persistent Volume Claims (PVCs) in a Kubernetes environment, showing the relationship between data volumes and claims.](https://kodekloud.com/kk-media/image/upload/v1752874022/notes-assets/images/Docker-Certified-Associate-Exam-Course-Persistent-Volumes/kubernetes-persistent-volumes-claims.jpg)
</Frame>

## PersistentVolume Object Overview

| Field                                | Description                                                                                                          |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `spec.capacity.storage`              | Total volume size (e.g., `1Gi`, `10Gi`)                                                                              |
| `spec.accessModes`                   | How Pods can mount the volume:<br />- `ReadWriteOnce` (RWO)<br />- `ReadOnlyMany` (ROX)<br />- `ReadWriteMany` (RWX) |
| `spec.persistentVolumeReclaimPolicy` | Action when a PVC is deleted:<br />- `Retain`<br />- `Delete`<br />- `Recycle`                                       |
| `spec.<storageBackend>`              | Backend-specific settings (e.g., `hostPath`, `awsElasticBlockStore`, `nfs`)                                          |

## 1. Creating a HostPath PersistentVolume

Below is a minimal PV definition that uses a node’s local filesystem (`hostPath`). This is helpful for testing but **not recommended for production**.

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-hostpath-1
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/data
  persistentVolumeReclaimPolicy: Retain
```

<Callout icon="triangle-alert">
  The `hostPath` backend binds storage to a specific node’s filesystem. For highly available or multi-node clusters, use cloud volumes or networked storage solutions.
</Callout>

Save this manifest as `pv-hostpath.yaml` and apply:

```bash theme={null}
kubectl apply -f pv-hostpath.yaml
```

Verify creation:

```bash theme={null}
kubectl get pv
```

Expected output:

```text theme={null}
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   AGE
pv-hostpath-1    1Gi        RWO            Retain           Available           10s
```

## 2. Creating a Cloud-Backed PersistentVolume

Replace the `hostPath` section with cloud provider settings. Example: AWS EBS

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-ebs-1
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: <aws-volume-id>
    fsType: ext4
  persistentVolumeReclaimPolicy: Delete
```

Apply and verify as before:

```bash theme={null}
kubectl apply -f pv-ebs.yaml
kubectl get pv
```

<Callout icon="lightbulb">
  Adjust the backend section for other cloud providers (GCE, Azure) or network filesystems (NFS, CSI drivers) by consulting the [Kubernetes Storage Concepts](https://kubernetes.io/docs/concepts/storage/).
</Callout>

## Next Steps

Once PVs are available, developers create Persistent Volume Claims (PVCs) to request specific capacity and access modes. Kubernetes binds PVCs to matching PVs, making storage consumption seamless within Pod specs.

***

## Links and References

* [Persistent Volumes | Kubernetes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [Persistent Volume Claim | Kubernetes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
* [Storage Classes | Kubernetes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
* [AWS EBS Volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/b920a910-e89e-477f-be56-458178c4b45d" />
</CardGroup>
