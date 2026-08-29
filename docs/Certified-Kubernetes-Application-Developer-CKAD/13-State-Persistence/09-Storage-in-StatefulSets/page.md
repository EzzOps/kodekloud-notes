# Storage in StatefulSets

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/State-Persistence/Storage-in-StatefulSets/page

This article explores storage in StatefulSets and explains persistent storage operations in Kubernetes, including provisioning methods and configurations for Pods.

In this article, we explore storage in StatefulSets and explain how persistent storage operates in Kubernetes. We begin with a review of persistent volumes (PV) and persistent volume claims (PVC) used with Pods, then dive into different provisioning methods and their use in StatefulSets.

***

## Persistent Volumes and Static Provisioning

Static provisioning involves a three-step process:

1. Create a PersistentVolume.
2. Create a PersistentVolumeClaim.
3. Reference the PVC in your Pod specification.

Below is an example of each configuration:

<Callout icon="lightbulb">
  For static provisioning, ensure that the PV capacity and access modes match the requirements of your applications.
</Callout>

### PersistentVolume Definition

```yaml theme={null}
