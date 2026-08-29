# Persistent Volume Claims

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Persistent-Volume-Claims/page

This article explains Kubernetes Persistent Volume Claims and their binding process with Persistent Volumes for managing storage resources.

In Kubernetes, storage resources are decoupled from pods using Persistent Volumes (PV) and Persistent Volume Claims (PVC).

* A **PersistentVolume** (PV) is a cluster-level resource representing a piece of storage provisioned by an administrator.
* A **PersistentVolumeClaim** (PVC) is a user’s request for storage, specifying capacity, access modes, and optional selectors.

When a PVC is created, Kubernetes matches it to an available PV that meets its requirements and then binds them.

![The image illustrates the concept of Persistent Volume Claims (PVC) and Persistent Volumes (PV) in Kubernetes, showing a mapping between PVCs and PVs with different colors.](https://kodekloud.com/kk-media/image/upload/v1752874018/notes-assets/images/Docker-Certified-Associate-Exam-Course-Persistent-Volume-Claims/kubernetes-pvc-pv-mapping-diagram.jpg)

## How PV-PVC Binding Works

The binding process evaluates several criteria to find a suitable PV for a PVC:

* **Capacity**: PV storage ≥ PVC request
* **Access Modes**: e.g., `ReadWriteOnce`, `ReadOnlyMany`
* **Volume Mode**: e.g., `Filesystem` or `Block`
* **Storage Class**: must match if specified
* **Label Selectors** (optional): target specific volumes

### Using Label Selectors

You can refine binding with labels on both PVC and PV:

```yaml theme={null}
