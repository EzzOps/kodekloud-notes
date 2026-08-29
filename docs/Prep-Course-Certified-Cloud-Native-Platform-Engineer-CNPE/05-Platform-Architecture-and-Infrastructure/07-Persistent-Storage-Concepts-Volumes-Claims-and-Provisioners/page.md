# Dangerous — will delete in the current namespace (could be the wrong one)
kubectl delete deployment my-deployment

# Safer — specify the namespace explicitly
kubectl delete deployment my-deployment -n team-a
```

Without RBAC restrictions and careful workflows, accidental or mis-scoped commands can delete other teams’ resources.

<Frame>
  <img alt="The image lists &#x22;Four Failure Modes&#x22; with an emphasis on &#x22;Failure Mode 3: Accidental Deletion,&#x22; showing a person accidentally deleting a program and highlighting the absence of RBAC (Role-Based Access Control)." />
</Frame>

Failure mode 4 — network segmentation:
By default, pods can communicate with any other pod in the cluster via cluster IPs. There is no default network-level firewall between namespaces. If a pod is compromised, an attacker can reach databases, admin APIs, and other teams’ workloads—enabling lateral movement across the cluster.

<Frame>
  <img alt="The image lists four failure modes: secrets exposure, resource exhaustion, accidental deletion, and network segmentation, with a diagram illustrating potential network errors and attacker access in a shared cluster." />
</Frame>

In short: namespaces are not security boundaries. Kubernetes does not protect teams from each other by default—security, stability, and fairness require explicit configuration.

<Callout icon="lightbulb">
  Start with these minimum guardrails for a multi-team cluster: RBAC (least privilege), ResourceQuotas, and NetworkPolicies. These three reduce the most common cross-tenant risks.
</Callout>

## Why Kubernetes is not multi-tenant out of the box

* Network: by default all pods can reach all other pods using cluster IPs—no network segmentation.
* Resources: no per-namespace resource limits exist by default; a namespace can consume the entire cluster.
* RBAC: role-based access control must be explicitly configured. What a user can do depends entirely on your Role and ClusterRole bindings; some managed services apply broad defaults.

<Frame>
  <img alt="The image outlines the issues with default multi-tenancy in Kubernetes, highlighting communication, resource limit, and RBAC configuration concerns. It mentions how pods can communicate freely, lack of resource limits, and the necessity for explicit RBAC configuration." />
</Frame>

## Why organizations still share clusters

The primary reason organizations share clusters is cost efficiency. Running many clusters multiplies control plane, monitoring, upgrade, and operational overhead.

| Approach         | Isolation                  | Pros                                                      | Cons                                                                      |
| ---------------- | -------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------- |
| Cluster per team | Strong                     | Best isolation; minimal cross-tenant blast radius         | High cost, many control planes to manage, complex upgrades and monitoring |
| Shared cluster   | Moderate (with guardrails) | Cost-efficient; single control plane and monitoring stack | Requires discipline and tooling; misconfiguration can affect many teams   |

<Frame>
  <img alt="The image compares two types of cluster setups: &#x22;Cluster per Team,&#x22; which offers strong isolation but is expensive and operationally heavy, and &#x22;Shared Cluster,&#x22; which is cost-efficient and simpler but requires discipline and guardrails." />
</Frame>

This is a fundamental trade-off: isolation costs money; sharing requires discipline.

## Two main multi-tenancy models

Choose a model based on trust boundaries and compliance requirements. The two primary approaches are soft multi-tenancy and hard multi-tenancy.

Soft multi-tenancy

* Use case: internal teams within the same organization (semi-trusted tenants).
* Isolation mechanisms: namespaces, RBAC, NetworkPolicies, ResourceQuotas (Kubernetes-native objects).
* Advantages: simpler, cost-effective, single cluster, minimal extra tooling.
* Downsides: tenants share the Linux kernel and control plane—kernel or control plane vulnerabilities can affect all tenants.
* Typical recommendation: start here for internal teams where risk is manageable.

Hard multi-tenancy

* Use case: untrusted tenants (external customers), or strict compliance (healthcare, finance).
* Isolation mechanisms: separate clusters or virtual clusters (for example, `vcluster`).
* Advantages: stronger boundaries and contained blast radius.
* Downsides: higher cost and greater operational complexity.

<Frame>
  <img alt="The image compares &#x22;Soft Multi-Tenancy&#x22; and &#x22;Hard Multi-Tenancy&#x22; models, detailing their isolation methods, use cases, trust levels, advantages, and disadvantages." />
</Frame>

Decision rule: if tenants are internal teams in the same company, start with soft multi-tenancy. If tenants are external customers or you must meet strict compliance, adopt hard multi-tenancy.

<Frame>
  <img alt="The image compares soft and hard multi-tenancy models, highlighting their isolation methods, use cases, trust levels, and pros and cons. Soft multi-tenancy is used within organizations, while hard multi-tenancy offers more security for external customers." />
</Frame>

Most organizations will adopt soft multi-tenancy for internal teams. The remainder of this lesson focuses on practical guardrails and isolation mechanisms for that model.

## Isolation mechanisms (soft multi-tenancy layers)

Compare options by isolation strength, cost, and operational complexity. Start with the simplest model that satisfies your security and compliance requirements and add layers only as needed.

| Mechanism                           | Isolation level | Cost & Complexity                                                                                  | Typical use case                                                               |
| ----------------------------------- | --------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Namespace-only                      | Low             | Minimal cost; low complexity                                                                       | Small, trusted dev teams where mistakes have low impact                        |
| Namespace + RBAC + ResourceQuota    | Medium          | Kubernetes-native; moderate implementation effort                                                  | Recommended minimum for multi-team clusters (even non-production)              |
| Add NetworkPolicies                 | Medium–High     | Low operational cost but requires a CNI that supports NetworkPolicies (see `https://www.cni.dev/`) | Production clusters where pods should be segmented by tenant                   |
| Virtual clusters (e.g., `vcluster`) | High            | Medium–high; gives per-tenant API separation while sharing nodes                                   | Teams needing cluster-level resources or scoped admin without affecting others |
| Separate clusters                   | Highest         | Highest cost and operational overhead                                                              | External customers, strict compliance, or unacceptable shared blast radius     |

<Frame>
  <img alt="The image is a comparison chart of isolation mechanisms, detailing different approaches and their respective levels of isolation, cost, complexity, and suitability for various environments." />
</Frame>

Principle: start with the simplest model that satisfies your security and compliance requirements. Do not over-engineer isolation for a small, trusted development team—add controls as your risk profile grows.

## Next steps and references

* Kubernetes RBAC docs: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* NetworkPolicy / CNI: [https://www.cni.dev/](https://www.cni.dev/)
* Virtual clusters: `vcluster` — [https://github.com/loft-sh/vcluster](https://github.com/loft-sh/vcluster)

Use the guidance in this lesson to choose a tenancy model, implement the minimum guardrails (RBAC, ResourceQuota, NetworkPolicies), and iterate from there.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/473c5c5a-97c8-4094-8c6f-1c22e1dbfd25" />
</CardGroup>


# Persistent Storage Concepts Volumes Claims and Provisioners

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-Architecture-and-Infrastructure/Persistent-Storage-Concepts-Volumes-Claims-and-Provisioners/page

Explains Kubernetes persistent storage concepts including PersistentVolumes PersistentVolumeClaims StorageClasses provisioning methods access modes and guidance to match storage to workload performance availability and cost

This section shifts focus from compute topics—architecting the platform, sizing resources, isolating tenants, and governing usage—to the second pillar of platform engineering: storage.

By the end of this lesson you'll understand how PersistentVolumeClaims (PVCs), PersistentVolumes (PVs), and StorageClasses work together in Kubernetes. You will know how to provision storage (static vs dynamic), the three access modes and backend support for each, and how to match workload requirements to the right storage configuration for performance, availability, and cost.

<Frame>
  <img alt="The image lists learning objectives related to PersistentVolumes, PersistentVolumeClaims, and StorageClasses in Kubernetes, focusing on roles, provisioning, access modes, and backend support." />
</Frame>

Start with a real problem.

A startup deployed PostgreSQL in Kubernetes without persistent volumes. During a routine cluster upgrade the node was drained, the Postgres pod restarted on a different node, and the container filesystem was empty. Six hours of customer transactions were lost.

<Callout icon="warning">
  This is not a hypothetical risk—running stateful services on ephemeral container storage can and will lead to data loss during node maintenance, evictions, autoscaling, and failures.
</Callout>

<Frame>
  <img alt="The image illustrates data loss in a Kubernetes cluster when Postgres runs on ephemeral storage, highlighting the transition from an &#x22;Original Node&#x22; to an &#x22;Upgraded Node&#x22; which results in a loss of six hours of data. It emphasizes the importance of configuring persistent volumes." />
</Frame>

Why did this happen? Containers are disposable: when a pod is removed (crash, eviction, reschedule), the container runtime deletes the writable layer that contains any data written to the container filesystem. For example, a pod that had written 500 MiB will restart with 0 MiB unless that data was stored outside the ephemeral layer.

<Frame>
  <img alt="The image illustrates the lifecycle of a container with three states: active (running with local data), failure (pod crashed), and new pod (empty new instance), showing how containers lose data after crashes." />
</Frame>

This is by design: containers are stateless and replaceable. Stateless workloads—web servers, API frontends, functions—are fine with ephemeral storage. Stateful workloads—databases, message queues, file stores—require durable storage that survives pod replacement.

The solution is to attach external storage that outlives a pod. Kubernetes mounts that storage into the pod as a filesystem so the pod can be replaced while the data remains intact on the volume.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster with a compute layer containing an initial and new pod, connected to persistent volume storage, highlighting storage persistence despite pod changes." />
</Frame>

## Kubernetes storage stack (three layers)

Understanding which component creates and manages what is essential for platform teams and developers.

<Frame>
  <img alt="The image illustrates the Kubernetes Storage Stack, showing the relationship and flow between Pod, PersistentVolumeClaim (PVC), PersistentVolume (PV), and StorageClass." />
</Frame>

From bottom to top:

* StorageClass — A template or “menu entry” that defines how volumes are provisioned. It points to a CSI driver (the provisioner) and includes provider-specific parameters such as disk type, IOPS, encryption, and topology constraints. Platform teams create and manage StorageClasses for developers to choose from.

* PersistentVolume (PV) — A representation of an actual storage resource. PVs are either:
  * statically provisioned by admins (manually created), or
  * dynamically provisioned by a StorageClass when a PVC is requested.
    Cloud environments typically use dynamic provisioning.

* PersistentVolumeClaim (PVC) — A developer’s request for storage. The PVC declares size, access mode(s), and optionally a StorageClass name. Kubernetes attempts to find an existing matching PV or asks the StorageClass to provision one, then binds the PVC to that PV. A pod mounts the PVC as a directory (for example, /data).

Analogy: StorageClass is the menu, PVC is your order, PV is the dish, and the Pod consumes it. If a diner (pod) leaves, the dish (data) stays.

## Access modes

Access modes define how a volume may be mounted and how many nodes/pods can use it. Not all modes are supported by every backend.

* ReadWriteOnce (RWO): mount read-write by a single node (multiple pods on that node may share). Typical for block volumes and databases.
* ReadOnlyMany (ROX): mount read-only by many nodes. Good for distributing static assets across replicas.
* ReadWriteMany (RWX): mount read-write by many nodes. Requires a network filesystem or file-share CSI driver (NFS, EFS, Azure Files, etc.).

<Frame>
  <img alt="The image describes different access modes for mounting storage in a computer system, including ReadWriteOnce (RWO), ReadOnlyMany (ROX), and ReadWriteMany (RWX), along with their best usage scenarios and compatible storage types." />
</Frame>

Use access modes that match both workload behavior and backend capability — for example, databases typically need RWO; distributed file systems are required for RWX.

<Frame>
  <img alt="The image is a comparison of access modes &#x22;ReadWriteOnce,&#x22; &#x22;ReadOnlyMany,&#x22; and &#x22;ReadWriteMany,&#x22; detailing which nodes can mount them, what they are best for, and their storage types. It advises choosing access modes based on workload needs." />
</Frame>

Table: Access modes at a glance

| Access Mode         | Mounts per Node   | Typical use case                        | Typical backend                               |
| ------------------- | ----------------- | --------------------------------------- | --------------------------------------------- |
| ReadWriteOnce (RWO) | Single node (R/W) | Databases, single-replica StatefulSets  | Block storage (AWS EBS, GCP PD, Azure Disk)   |
| ReadOnlyMany (ROX)  | Many nodes (R/O)  | Read-only static content, config data   | Object mounts, read-only NFS exports          |
| ReadWriteMany (RWX) | Many nodes (R/W)  | Shared file systems, concurrent writers | NFS, EFS, Azure Files, CSI file-share drivers |

## Example PVC

A PVC declares size, accessModes, and optionally a `storageClassName`. Kubernetes will bind an existing PV or ask the StorageClass to provision a PV dynamically. If `storageClassName` is omitted, the cluster default StorageClass (if configured) will be used.

Correct example PVC:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

After creation the PVC status should move from `Pending` to `Bound`. If the PVC remains `Pending` inspect it:

```bash theme={null}
kubectl describe pvc <pvc-name>
```

Common reasons for `Pending`:

* StorageClass name typo or missing StorageClass.
* Insufficient capacity in the backend.
* StorageClass uses `volumeBindingMode: WaitForFirstConsumer` and no pod is scheduled that references the PVC yet.
* Requested access mode is not supported by available PVs or provisioner.

<Callout icon="lightbulb">
  If a PVC stays `Pending`, check the StorageClass, backend capacity, and `volumeBindingMode`. For multi-AZ clusters, prefer `WaitForFirstConsumer` to ensure volumes are provisioned in the consuming Pod's zone.
</Callout>

## StorageClass details

Platform teams define StorageClasses to expose curated storage offerings. Developers reference them by name in PVCs.

Example StorageClass:

```yaml theme={null}
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

Table: Key StorageClass fields

| Field               | Purpose                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| `provisioner`       | The CSI driver used to provision volumes (e.g., `ebs.csi.aws.com`).                                 |
| `parameters`        | Provider-specific options such as disk type, IOPS, encryption flags.                                |
| `reclaimPolicy`     | `Delete` (remove underlying storage when PVC deleted) or `Retain` (keep data after PVC deletion).   |
| `volumeBindingMode` | `Immediate` (provision on PVC creation) or `WaitForFirstConsumer` (delay until a Pod is scheduled). |

Notes on reclaim policies:

* Delete: good for ephemeral or reproducible data where storage lifecycle follows the PVC.
* Retain: use for critical data that must be preserved after PVC deletion (manual cleanup required).

volumeBindingMode considerations:

* `Immediate` may cause volumes to be provisioned in the wrong AZ/zone for multi-AZ clusters.
* `WaitForFirstConsumer` ensures volumes are created in the correct topology aligned to where the Pod will run.

## Choosing storage for workloads

Answer the question "Which storage should I use?" using four criteria: access mode, storage type, reclaim policy, and workload characteristics.

Suggested mappings:

| Workload                    | Access Mode   | Storage type                              | Reclaim policy                        |
| --------------------------- | ------------- | ----------------------------------------- | ------------------------------------- |
| Databases (Postgres, MySQL) | ReadWriteOnce | Fast SSD / provisioned IOPS block storage | `Retain`                              |
| Shared file systems         | ReadWriteMany | NFS, EFS, Azure Files (RWX-capable CSI)   | As appropriate (`Delete` or `Retain`) |
| Static content              | ReadOnlyMany  | Object-backed mounts or read-only NFS     | `Delete`                              |
| Batch jobs / ephemeral data | ReadWriteOnce | Cheap HDD or low-cost block               | `Delete`                              |

Name StorageClasses by use case (e.g., `fast-ssd`, `shared-nfs`, `bulk-hdd`) rather than by cloud provider. This keeps the platform portable and makes selection easier for developers.

<Frame>
  <img alt="The image shows a chart for matching workloads to storage types, outlining access modes, storage options, and reclaim policies for different applications like databases, shared files, static content, and batch jobs." />
</Frame>

## Five key takeaways

* PVCs request storage; PVs provide it. Developers create PVCs; platform teams manage StorageClasses—clear separation of concerns.
* Access modes dictate sharing semantics. Not every backend supports every mode.
* StorageClasses abstract provider details; name them by use case to help developers choose the right one.
* Match workload to storage: databases typically need SSD + `Retain`; batch jobs can use cheaper disks + `Delete`.
* Storage decisions affect both performance and cost—evaluate IO, throughput, durability, and availability when designing StorageClasses.

<Frame>
  <img alt="The image presents a list of five key takeaways about storage in Kubernetes, including topics like PVCs, access modes, StorageClasses, workload matching, and storage decisions." />
</Frame>

## Links and References

* Kubernetes Persistent Volumes: [https://kubernetes.io/docs/concepts/storage/persistent-volumes/](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* Kubernetes StorageClasses: [https://kubernetes.io/docs/concepts/storage/storage-classes/](https://kubernetes.io/docs/concepts/storage/storage-classes/)
* CSI (Container Storage Interface) docs: [https://kubernetes-csi.github.io/](https://kubernetes-csi.github.io/)
* AWS EBS CSI Driver: [https://github.com/kubernetes-sigs/aws-ebs-csi-driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
* NFS and RWX solutions: see cloud vendor docs for EFS (AWS), Azure Files, and GCP Filestore.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/d2d5c77a-9d9f-4a6e-9eb5-b6023f7842c4" />
</CardGroup>
