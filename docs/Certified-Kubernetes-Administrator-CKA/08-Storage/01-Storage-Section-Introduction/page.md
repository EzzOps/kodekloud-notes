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

```yaml theme={null}
# pvc-definition.yaml
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

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
    - image: alpine
      name: alpine
      command: ["/bin/sh", "-c"]
      args: ["shuf -i 0-100 -n 1 >> /opt/number.out;"]
      volumeMounts:
        - mountPath: /opt
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim
```

In this setup, the PVC binds to the manually created PV that refers to your existing Google Cloud persistent disk.

***

## Dynamic Provisioning with Storage Classes

Dynamic provisioning removes the need for manual storage pre-provisioning. When you create a PVC, the associated storage class automatically provisions the necessary PV using the defined provisioner.

First, create a storage class object that specifies the provisioner (in this case, Google Cloud's persistent disk):

```yaml theme={null}
# sc-definition.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

With the storage class in place, update your PVC to reference it for dynamic provisioning:

```yaml theme={null}
# pvc-definition.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: google-storage
  resources:
    requests:
      storage: 500Mi
```

The pod definition remains similar:

```yaml theme={null}
# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: random-number-generator
spec:
  containers:
    - image: alpine
      name: alpine
      command: ["/bin/sh", "-c"]
      args: ["shuf -i 0-100 -n 1 >> /opt/"]
      volumeMounts:
        - mountPath: /opt
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myclaim
```

When you create a PVC with a storage class specified, Kubernetes leverages the defined provisioner to dynamically generate a new persistent disk with the requested size, automatically creating and binding a PV to the PVC.

> **lightbulb** Using dynamic provisioning simplifies storage management by reducing manual tasks and minimizing potential configuration errors.

***

## Customizing Storage Classes

Storage classes in Kubernetes support various parameters, allowing you to fine-tune the provisioned storage to meet your application’s performance and reliability requirements. Many provisioners support custom parameters. For example, with the GCE provisioner, you can specify disk types and replication modes. This enables you to create multiple classes of service such as silver (standard disks), gold (SSD drives), and platinum (regional SSD drives).

Below are examples of customized storage class definitions:

```yaml theme={null}
# silver storage class: standard disk without replication
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: silver
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
```

```yaml theme={null}
# gold storage class: SSD disk without replication
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gold
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: none
```

```yaml theme={null}
# platinum storage class: SSD disk with regional replication
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: platinum
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
```

By specifying the appropriate storage class in your PVC definitions, you match the storage's performance and reliability to your application's needs.

***

## Summary

This lesson demonstrated how Kubernetes storage classes streamline persistent storage provisioning. Whether using static provisioning or dynamic provisioning, storage classes allow for more efficient management of storage resources, reducing manual efforts and enhancing scalability.

For further details on Kubernetes storage and dynamic provisioning, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/883f0aa9-3aa9-45a6-bd26-3a87ded1e00e/lesson/7db1e759-86c1-4d12-9b74-3cfd89ab9c5e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/883f0aa9-3aa9-45a6-bd26-3a87ded1e00e/lesson/b3c24fd3-ca54-4dda-9e1b-0265bcac84ff)


# Storage Section Introduction

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Storage/Storage-Section-Introduction/page

This guide explores essential Kubernetes storage concepts including persistent volumes, claims, access modes, and configuring applications for persistent storage.

Welcome to the Kubernetes Storage section! In this guide, we will explore essential storage concepts including persistent volumes (PV), persistent volume claims (PVC), and access modes. You'll also learn how to configure your applications for persistent storage in Kubernetes.

Kubernetes provides a versatile range of storage options that can adapt to different environments. This lesson specifically focuses on Kubernetes-native storage mechanisms, ensuring you understand the core concepts needed to integrate any third-party storage solutions with your cluster.

> **lightbulb** Make sure to review the Kubernetes documentation on storage for additional details and best practices.

Let's dive in and explore how to manage storage effectively in your Kubernetes deployments!

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/883f0aa9-3aa9-45a6-bd26-3a87ded1e00e/lesson/39018b67-0d20-4476-99bb-018e74f74747)
