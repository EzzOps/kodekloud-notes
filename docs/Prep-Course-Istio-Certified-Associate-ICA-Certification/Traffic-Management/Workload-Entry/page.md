# Workload Entry

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Workload-Entry/page

Explains ServiceEntry and WorkloadEntry in Istio, showing how to register external services and workloads for routing, mTLS, telemetry and policy enforcement.

A concise, updated overview of ServiceEntry and WorkloadEntry in Istio, with examples and configuration notes.

A ServiceEntry declares services that are external to the Istio mesh (for example, external APIs or databases outside the Kubernetes cluster). A WorkloadEntry registers an external workload (for example, a VM or EC2 instance) so it can be treated as a first-class member of the mesh—receiving traffic, identity, and policy enforcement.

<Frame>
  <img alt="The image is a diagram illustrating the concept of a Service Entry in Istio, showing how external services are integrated into a Kubernetes mesh with nodes and Envoy proxies." />
</Frame>

Summary

* ServiceEntry: Adds external hosts to Istio’s service registry so mesh workloads can route to them.
* WorkloadEntry: Registers concrete endpoints (IP or DNS) and labels for external workloads so they can receive traffic and be governed by mesh features (mTLS, telemetry, and policies) just like pods.

Architecture example: registering an EC2 instance as a mesh workload so Istio treats it like an in-cluster pod.

<Frame>
  <img alt="The diagram illustrates an Istio control plane setup with two nodes, Node 01 and Node 02, showing workloads for &#x22;payment&#x22; and &#x22;identity&#x22; services, along with Envoy integration. An Amazon EC2 workload entry is indicated outside the nodes." />
</Frame>

Concept — what WorkloadEntry does

* Registers an external machine (VM/EC2) as part of the mesh.
* Lets Istio apply security (mTLS), policies, and telemetry to traffic to/from that workload when it participates in the mesh (typically via a sidecar).
* Uses labels for selection so Istio resources can target both pods and external endpoints uniformly.

WorkloadEntry basics

* A WorkloadEntry declares one or more endpoints (`address`) and labels. Those labels are used by selectors (for example, `ServiceEntry.workloadSelector` or `DestinationRule`) to route traffic to the external workload.
* Optionally include a `serviceAccount` to indicate the workload’s identity (used with mTLS when a sidecar is present).
* For full mesh behavior (mTLS, telemetry), the external workload typically requires a sidecar proxy or another mechanism to participate in the mesh.

Example 1 — Register a single IP as an external workload

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: WorkloadEntry
metadata:
  name: external-app-we
  namespace: backend
spec:
  address: 54.146.220.232
  labels:
    app: external
```

Map a logical host to the WorkloadEntry endpoints using ServiceEntry

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: external-app-se
  namespace: backend
spec:
  hosts:
    - app.internal.com
  ports:
    - number: 80
      name: http
      protocol: TCP
  resolution: STATIC
  workloadSelector:
    labels:
      app: external
```

How this works

* The ServiceEntry adds `app.internal.com` to Istio’s service registry so mesh workloads can discover it.
* `resolution: STATIC` indicates the mapping to endpoints is static (resolved via WorkloadEntry or manually defined endpoints).
* The `workloadSelector` picks resources (both pods and WorkloadEntry objects) with matching labels (`app: external`). Traffic to `app.internal.com` is routed to the endpoint(s) defined by matching WorkloadEntry(s).

Important detail

* `workloadSelector` labels can match both Kubernetes pods and WorkloadEntry resources. This enables uniform handling of in-cluster pods and external workloads.

Why choose WorkloadEntry over ServiceEntry alone?

* ServiceEntry only declares the host so the mesh can route outbound traffic to it. It does not integrate the host into the mesh for mTLS identity, policy enforcement, or richer telemetry.
* WorkloadEntry integrates the external workload into the mesh. When the workload runs a sidecar (or otherwise participates in mTLS/identity), it gains service identity, mutual TLS, richer metrics, logs, and tracing.

Comparison table

|             Feature |                 ServiceEntry                |                            WorkloadEntry                            |
| ------------------: | :-----------------------------------------: | :-----------------------------------------------------------------: |
|             Purpose |    Declare external services to the mesh    |        Register external workloads/endpoints as mesh members        |
|        mTLS support |                No (by itself)               |     Yes, when the workload participates (sidecar/serviceAccount)    |
|   Service discovery |            Adds host to registry            |                  Adds concrete endpoint(s) (IP/DNS)                 |
| Telemetry & metrics |           Limited (outbound only)           |          Rich telemetry when workload participates in mesh          |
|            Use case | Allow outbound routing to external services | Treat external VMs/VMs/instances like pods for policies and metrics |

Advanced WorkloadEntry example (service account + labels)

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: WorkloadEntry
metadata:
  name: details-svc
  namespace: default
spec:
  # Use of the service account indicates the workload has a sidecar
  # proxy bootstrapped with this service account. Pods with sidecars
  # will automatically communicate with the workload using Istio mTLS.
  serviceAccount: details-legacy
  address: vm1.vpc01.corp.net
  labels:
    app: details-legacy
    instance-id: vm1
```

Notes on configuration

* `serviceAccount` ties the external workload to a Kubernetes ServiceAccount identity. When configured correctly, Istio can use that identity for mutual TLS and policy enforcement.
* `address` may be an IP or a DNS name reachable from the mesh.
* Use labels to group or select workloads from `ServiceEntry.workloadSelector`, `DestinationRule`, or other Istio resources.
* Additional fields in `WorkloadEntry.spec` include `network`, `ports`, `weight`, and `locality` which help with routing, traffic-splitting, and multi-cluster/network topologies. Review the Istio reference for full details.

<Frame>
  <img alt="The image is a comparison table between &#x22;Service Entry&#x22; and &#x22;Workload Entry,&#x22; highlighting differences in purpose, use case, mTLS support, service discovery, and telemetry & metrics." />
</Frame>

Be prepared to explain

* What a WorkloadEntry does: registers external workloads/endpoints into the mesh.
* How it differs from a ServiceEntry: ServiceEntry enables routing to external hosts; WorkloadEntry integrates endpoints as first-class mesh members with identity and telemetry support.
* How `workloadSelector` enables unified selection of pods and external workloads.

<Callout icon="lightbulb">
  Use a ServiceEntry when you only need to enable routing to an external host. Use a WorkloadEntry when you want the external host to behave like a mesh workload (mTLS, telemetry, policies). Often both are used together: ServiceEntry to add the host to the registry and WorkloadEntry to register the concrete endpoints.
</Callout>

References

* Istio WorkloadEntry reference: [https://istio.io[AWS_SECRET_ACCESS_KEY]/workload-entry/](https://istio.io[AWS_SECRET_ACCESS_KEY]/workload-entry/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/77292246-0e9e-4099-af8f-5d8578127806" />
</CardGroup>
