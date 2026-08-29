# The Operator Pattern Encoding Operational Knowledge

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/The-Operator-Pattern-Encoding-Operational-Knowledge/page

Explains Kubernetes Operator pattern that encodes operational runbook tasks into controllers and CRDs to automate application lifecycle, capabilities, and when to use Operators

The Operator pattern captures operational knowledge and encodes it as software. In practice, you take the runbook your SRE follows at 3 a.m. and turn it into a controller that runs continuously inside the cluster, automating tasks that would otherwise be manual and error-prone.

<Frame>
  <img alt="The image compares a &#x22;3 a.m. runbook&#x22; executed by hand with a Kubernetes cluster controller that runs continuously." />
</Frame>

Consider the lifecycle of a production database: installation, replication configuration, scheduled backups, monitoring a failed primary, and promoting a replica when needed. Those steps are often scattered across wikis, Helm charts, runbooks, and the knowledge in a long-serving engineer's head. An Operator captures this operational logic inside Kubernetes.

<Frame>
  <img alt="The image highlights the challenges of running a database, listing tasks like installing, configuring replication, scheduling backups, and promoting a failed primary." />
</Frame>

At its core, an Operator is just a Kubernetes controller paired with a Custom Resource Definition (CRD). You declare desired state in a custom resource (for example: "a three-node Postgres cluster, version 16, with daily backups") and the Operator's reconcile loop continuously drives the actual cluster state toward that desired state. This is the same control-loop pattern Kubernetes uses for Deployments and Services, extended to your application domain.

Example custom resource (simplified):

```yaml theme={null}
apiVersion: databases.example.com/v1alpha1
kind: PostgresCluster
metadata:
  name: my-db
spec:
  replicas: 3
  version: "16"
  backups:
    schedule: "0 2 * * *"
```

The reconcile loop reacts to observed state, executes the required operations (e.g., create StatefulSets, configure replication, schedule backups), updates status conditions, and ensures finalizers clean up resources on deletion.

History and community examples: CoreOS coined the "Operator" term in 2016. Projects like the original etcd Operator and the Prometheus Operator demonstrated that Operators can do more than install software—they can keep systems healthy over time. The Operator community later formalized Operator Capability Levels to describe maturity and functionality.

<Frame>
  <img alt="The image outlines the origins of a pattern named by CoreOS in 2016, featuring etcd and Prometheus, and includes a process from installation to maintenance." />
</Frame>

Operator capability levels (summary)

| Level | Focus             | Example capabilities                                        |
| ----- | ----------------- | ----------------------------------------------------------- |
| L1    | Basic install     | Provision CR-backed resources (Deployments, StatefulSets)   |
| L2    | Seamless upgrades | Rolling upgrades, version-aware reconciliation              |
| L3    | Full lifecycle    | Backups, restores, failure recovery, finalizers             |
| L4    | Deep insight      | Rich metrics, alerts, workload analysis                     |
| L5    | Autopilot         | Horizontal/vertical scaling, auto-tuning, anomaly detection |

<Frame>
  <img alt="The image illustrates a progression of operator capability levels from L1 to L5, including basic install, seamless upgrades, full lifecycle, deep insight, and autopilot." />
</Frame>

Most production Operators sit around Level 2 or 3. Achieving Levels 4 and 5 requires substantial investment in metrics, telemetry, and domain-specific automation logic.

To make these ideas concrete, the web-app Operator we’ll describe is intentionally small: it manages a Deployment, a Service, and a ConfigMap driven by a single custom resource. It demonstrates the important Operator mechanics — CRD definition, controller reconcile loop, status conditions, finalizers for cleanup, and admission webhooks for validation — without the extra complexity of stateful storage. Once you understand this simple example, applying the same pattern to stateful workloads is primarily a matter of adding domain logic (replication, backup orchestration, etc.) rather than learning new Kubernetes primitives.

Two practical points to keep in mind:

<Frame>
  <img alt="The image outlines when to use an operator in Kubernetes. It suggests using one for ongoing operational logic and not needing one for stateless apps, deployed using Deployment and Helm." />
</Frame>

<Callout icon="lightbulb">
  Use an Operator when your application requires ongoing operational automation that cannot be expressed easily with plain declarative objects or Helm charts. If your service is stateless and a Deployment plus a Helm chart suffice, an Operator is probably unnecessary.

  Remember: an Operator is production software — it needs tests, RBAC, monitoring, and updates. Extending the Kubernetes control plane carries the same responsibilities as operating any other controller.
</Callout>

This section examines the anatomy of an Operator — the CRD plus the controller — and prepares you to build and reason about Operators that encode operational knowledge reliably and repeatably.

Links and references

* [etcd Operator (CoreOS)](https://github.com/coreos/etcd-operator)
* [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
* [Kubernetes: Controllers and the control loop](https://kubernetes.io/docs/concepts/architecture/controller/)
* [Operator Framework](https://operatorframework.io/)
* [Helm](https://helm.sh/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/f89b1704-b63a-4ae8-8b47-2bbb57630e79" />
</CardGroup>
