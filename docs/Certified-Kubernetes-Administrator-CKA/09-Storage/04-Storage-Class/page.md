# Storage Class

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Storage/Storage-Class/page

This article explores Kubernetes storage classes and their role in simplifying storage provisioning for applications.

In this lesson, we explore storage classes in Kubernetes and demonstrate how they simplify the process of storage provisioning for applications. Traditionally, administrators manually created PersistentVolumes (PVs) and PersistentVolumeClaims (PVCs) and mounted them to pods. This guide covers both static provisioning (manually creating disks and PVs) and dynamic provisioning using storage classes, making your Kubernetes storage management more efficient.

***

## Static Provisioning

With static provisioning, you manually create the underlying storage (for example, a [Google Cloud persistent disk](https://cloud.google.com/compute/docs/disks)) and then construct a PV that references that disk. Each time an application requires storage, you must provision a disk on Google Cloud and create the corresponding PV definition.

For example, to create a persistent disk on Google Cloud, you can use the following command:

```bash theme={null}
gcloud beta compute disks create \
  --size 1GB \
  --region us-east1 \
  pd-disk
```

Then, define your Kubernetes resources as follows:

```yaml theme={null}
