# pv-definition.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 500Mi
  gcePersistentDisk:
    pdName: pd-disk
  fsType: ext4
```

### PersistentVolumeClaim Definition

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-volume
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage
  resources:
    requests:
      storage: 500Mi
```

### Pod Definition Referencing the PVC

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: mysql
spec:
  containers:
    - image: mysql
      name: mysql
      volumeMounts:
        - mountPath: /var/lib/mysql
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: data-volume
```

***

## Dynamic Provisioning with StorageClasses

Dynamic provisioning simplifies the process by automatically creating PVs when you define a PVC and reference a StorageClass. This eliminates the need to manually provision PVs.

### StorageClass Definition

```yaml theme={null}
# sc-definition.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

### PVC Definition Using Dynamic Provisioning

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-volume
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage
  resources:
    requests:
      storage: 500Mi
```

### Pod Definition Referencing the Dynamically Provisioned PVC

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: mysql
spec:
  containers:
    - image: mysql
      name: mysql
      volumeMounts:
        - mountPath: /var/lib/mysql
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: data-volume
```

***

## Using StatefulSets with Shared Storage

StatefulSets support scenarios where multiple replicas share the same volume. If you reference a common PVC within a StatefulSet, all replicas will attempt to access the same storage. This setup works if your underlying storage supports multi-reader or multi-writer capabilities.

### Shared Storage StatefulSet Example

```yaml theme={null}
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: data-volume
      volumes:
        - name: data-volume
          persistentVolumeClaim:
            claimName: data-volume
```

<Callout icon="triangle-alert">
  Ensure that your storage solution supports concurrent access if you plan to share the same volume across multiple Pods.
</Callout>

***

## Separate Volumes for Each Pod Using VolumeClaimTemplates

For scenarios like MySQL replication where each Pod requires dedicated storage, a volume claim template allows Kubernetes to automatically create a unique PVC for each Pod in a StatefulSet.

### Step 1: Define the StorageClass

```yaml theme={null}
# sc-definition.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

### Step 2: Create a StatefulSet with a VolumeClaimTemplate

```yaml theme={null}
# statefulset-definition.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: data-volume
  volumeClaimTemplates:
    - metadata:
        name: data-volume
      spec:
        accessModes:
          - ReadWriteOnce
        storageClassName: google-storage
        resources:
          requests:
            storage: 500Mi
```

In this configuration, Kubernetes provisions a unique PVC for each Pod automatically based on the volume claim template. This ensures that every Pod receives its dedicated storage. Additionally, StatefulSets maintain stable storage even if a Pod is rescheduled; the associated PVC and underlying PV remain intact and are reattached to the new Pod instance.

***

That concludes our discussion on storage in StatefulSets. For more information on Kubernetes storage concepts, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/cb16c9a3-1608-48cf-bfd5-2465f64b4f93/lesson/3d2aab8c-5ddc-40fd-927e-be49550c8f9b" />
</CardGroup>


# Volume Driver Plugins in Docker

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/State-Persistence/Volume-Driver-Plugins-in-Docker/page

This article explains Docker volume driver plugins for data persistence and highlights third-party options for external storage solutions.

Docker leverages storage drivers to manage images and containers, while volume driver plugins handle data persistence. Unlike storage drivers, volumes need to be explicitly created and are managed by these dedicated plugins.

<Callout icon="lightbulb">
  The default volume driver plugin, "local," creates volumes on the Docker host and stores data at `/var/lib/docker/volumes`.
</Callout>

Several third-party volume driver plugins further expand Docker's storage capabilities by enabling volume creation on external storage solutions. Popular plugins include:

* Azure File Storage
* Convoy
* DigitalOcean Block Storage
* Blocker
* Google Compute Persistent Disks
* ClusterFS
* NetApp
* RexRay
* Portworx
* VMware vSphere storage

<Callout icon="lightbulb">
  Certain volume drivers support multiple storage providers. For instance, the RexRay storage driver can provision storage on various platforms such as AWS EBS, S3, EMC storage arrays like Isilon and ScaleIO, Google Persistent Disk, and OpenStack Cinder.
</Callout>

When running a Docker container, you can specify a volume driver—such as RexRay for AWS EBS—to provision a cloud-based volume. This approach ensures that your data remains safe even after the container exits.

Below is an example command that demonstrates how to run a Docker container with a specified volume driver:

```bash theme={null}
docker run -it \
  --name mysql \
  --volume-driver rexray/ebs \
  --mount src=ebs-vol,target=/var/lib/mysql \
  mysql
```

This command creates a container named "mysql" and attaches a volume provisioned from Amazon EBS, ensuring persistent data storage in the cloud.

While this article focuses on Docker volume driver plugins, remember that Kubernetes also offers robust solutions for managing persistent storage through its volume mechanisms. For more details on persistent storage in Kubernetes, refer to [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/cb16c9a3-1608-48cf-bfd5-2465f64b4f93/lesson/133c8da6-8e20-43da-b161-03f1b9d6f787" />
</CardGroup>
