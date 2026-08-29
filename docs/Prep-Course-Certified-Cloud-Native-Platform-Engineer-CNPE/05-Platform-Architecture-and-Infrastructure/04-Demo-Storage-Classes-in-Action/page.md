# Scale frontend web down to 1 replica
kubectl scale deployment web -n team-frontend --replicas=1
# Scale cache up to 2 replicas
kubectl scale deployment cache -n team-data --replicas=2
```

Example responses:

```bash theme={null}
deployment.apps/web scaled
deployment.apps/cache scaled
```

Return to the [OpenCost UI](https://docs.opencost.io) and refresh. As Prometheus metrics are aggregated you should see namespace and deployment costs adjust to reflect the new requested resources and replica counts.

<Frame>
  <img alt="The image is a cost allocation dashboard from OpenCost displaying a pie chart and a table showing namespace daily costs, with details on CPU, GPU, RAM, PV, efficiency, and total cost." />
</Frame>

OpenCost API for automation

If you prefer automation or integration, OpenCost exposes an API you can query. Example: get compute allocation aggregated by namespace over the last hour and format results with `jq`:

```bash theme={null}
curl -sG "http://localhost:3904/allocation/compute?window=1h&aggregate=namespace" | \
jq -r '
  (.data[0] // {}) 
  | to_entries[]
  | {namespace: .key, cpuCost: .value.cpuCost, ramCost: .value.ramCost}
'
```

Sample JSON output (trimmed):

```json theme={null}
{
  "namespace": "kube-flannel",
  "cpuCost": 0.00271,
  "ramCost": 0.00018
}
{
  "namespace": "kube-system",
  "cpuCost": 0.02307,
  "ramCost": 0.00085
}
{
  "namespace": "opencost",
  "cpuCost": 0.00054,
  "ramCost": 0.00039
}
{
  "namespace": "team-backend",
  "cpuCost": 0.00543,
  "ramCost": 0.00091
}
{
  "namespace": "team-data",
  "cpuCost": 0.00764,
  "ramCost": 0.00041
}
{
  "namespace": "team-frontend",
  "cpuCost": 0.05045,
  "ramCost": 0.00676
}
```

Use cases for the API:

* Scheduled cost reports.
* CI/CD gates to prevent cost spikes from PRs.
* Automated alerts when request-to-usage ratios indicate overprovisioning.

Conclusion

For exploration and fast triage, the [OpenCost UI](https://docs.opencost.io) is convenient; for automation and programmatic workflows, use the API. Either way, OpenCost provides the visibility needed to identify overprovisioning, allocate cost to teams, and take concrete remediation steps like rightsizing requests or adjusting replica counts.

Links and references

* [OpenCost website](https://opencost.io)
* [OpenCost documentation (UI & API)](https://docs.opencost.io)
* [Prometheus](https://prometheus.io)
* jq: [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/4dfb9257-7cc3-4837-b314-207a8d758584" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/9d957351-7ded-4b48-a240-cd70699a17e1" />
</CardGroup>


# Demo Storage Classes in Action

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-Architecture-and-Infrastructure/Demo-Storage-Classes-in-Action/page

Guide to Kubernetes StorageClasses and dynamic volume provisioning, demonstrating PVC/PV lifecycle, reclaim policies Delete versus Retain, WaitForFirstConsumer behavior, and production best practices.

Every application that stores data needs storage. On Kubernetes, workloads request storage via PersistentVolumeClaims (PVCs), and the cluster provisions storage according to a StorageClass. Think of a StorageClass as a platform-provided menu of storage options: fast SSDs for databases, cheap spinning disks for archival data, cloud block volumes, or replicated storage for production workloads. Teams request the option they need and Kubernetes handles provisioning.

This guide shows how to:

* List and inspect StorageClasses
* Demonstrate dynamic provisioning using a StorageClass (`fast`)
* Compare reclaim behaviors (`Delete` vs `Retain`)
* Apply best practices for production clusters

Keywords: Kubernetes StorageClass, dynamic provisioning, reclaim policy, PVC, PV, WaitForFirstConsumer

## List available StorageClasses

Get the StorageClasses in the cluster:

```bash theme={null}
kubectl get sc
```

Example output:

```text theme={null}
NAME         PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE        ALLOWVOLUMEEXPANSION   AGE
archive      rancher.io/local-path   Retain          WaitForFirstConsumer     false                  16m
fast         rancher.io/local-path   Delete          WaitForFirstConsumer     false                  16m
local-path   rancher.io/local-path   Delete          WaitForFirstConsumer     false                  16m
```

Note: The cluster’s default StorageClass (if set) is indicated by an annotation/marker in some `kubectl get sc` output. If a PVC omits `storageClassName`, Kubernetes uses the default StorageClass automatically (if one exists).

<Callout icon="lightbulb">
  If a PVC does not set `storageClassName`, Kubernetes assigns the default StorageClass (if one exists). This behavior is important in production clusters to avoid unexpected storage types being provisioned.
</Callout>

## Inspect a StorageClass

To view details for the `fast` StorageClass:

```bash theme={null}
kubectl describe storageclass fast
```

Example output (trimmed):

```text theme={null}
Name:                  fast
IsDefaultClass:        No
Provisioner:           rancher.io/local-path
ReclaimPolicy:         Delete
VolumeBindingMode:     WaitForFirstConsumer
AllowVolumeExpansion:  <unset>
Parameters:            <none>
MountOptions:          <none>
Events:                <none>
```

Key StorageClass fields and what they mean:

| Field                  | Description                                                       | Typical Values / Notes                                                    |
| ---------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `Provisioner`          | The CSI/plugin responsible for creating volumes                   | e.g., `rancher.io/local-path`, `kubernetes.io/aws-ebs`, `ebs.csi.aws.com` |
| `ReclaimPolicy`        | What happens to the underlying PV/storage when the PVC is deleted | `Delete` (auto-remove), `Retain` (manual cleanup)                         |
| `VolumeBindingMode`    | When the PV is provisioned relative to Pod scheduling             | `Immediate` or `WaitForFirstConsumer` (prevents cross-zone leaks)         |
| `AllowVolumeExpansion` | Whether PVCs can request more capacity after creation             | `true` / `false`                                                          |
| `Parameters`           | Provisioner-specific options                                      | Varies per driver                                                         |

Volume binding mode note: `WaitForFirstConsumer` delays provisioning until a Pod using the PVC is scheduled — this avoids provisioning in the wrong zone/node and is highly recommended in multi-zone clusters.

## Demonstrate dynamic provisioning (fast StorageClass)

Create a PVC that requests 1Gi using the `fast` StorageClass.

Save this as `pvc-fast.yaml`:

```yaml theme={null}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
  namespace: storage
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
  resources:
    requests:
      storage: 1Gi
```

Apply the PVC:

```bash theme={null}
kubectl apply -f pvc-fast.yaml
