# Storage Class

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Storage/Storage-Class/page

This article explores storage classes in Kubernetes, focusing on static and dynamic provisioning for effective storage resource management.

In this article, we explore how storage classes work in Kubernetes. We'll build on the basic concepts of creating PersistentVolumes (PVs), PersistentVolumeClaims (PVCs), and using PVCs within pod definitions. Understanding static and dynamic provisioning methods is essential for effective storage resource management in your Kubernetes environment.

***

> **lightbulb** Kubernetes storage classes simplify storage management by automating the provisioning process. Whether you use static provisioning or dynamic provisioning, the concepts remain similar, with dynamic provisioning offering automated PV creation.

## Static Provisioning

Static provisioning requires manual setup. First, you create the persistent disk on your cloud provider (for example, on Google Cloud), then you manually create the PV definition using the exact same disk name. Each application that requires storage needs you to pre-provision the disk and create the corresponding PV configuration.

Below are the YAML definitions for the PV, PVC, and Pod using static provisioning:

```yaml theme={null}
