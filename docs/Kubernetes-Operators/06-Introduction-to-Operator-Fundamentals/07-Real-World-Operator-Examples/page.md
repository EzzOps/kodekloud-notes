# Real World Operator Examples

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/Real-World-Operator-Examples/page

Overview of Kubernetes operator pattern with real examples showing how controllers use custom resources to manage lifecycle tasks for services like TLS, monitoring, databases, and Kafka

To fully understand the operator pattern, it helps to see how it appears in real tools people use every day.

Operators are not just a theoretical pattern — many teams rely on operators to run production platform services on Kubernetes. Think of an operator as a specialist technician: Kubernetes provides the building, rooms, and power; the operator encodes the specialist knowledge for installing, checking, repairing, and upgrading a particular piece of software. That specialist knowledge is what makes an operator so useful.

<Frame>
  <img alt="The image explains how operators are specialists in running platform services with Kubernetes, focusing on tasks like installing, checking, repairing, and upgrading specific machines. It highlights the operator's knowledge of particular machines in relation to platform services." />
</Frame>

<Callout icon="lightbulb">
  Operators encapsulate operational expertise (backups, upgrades, failover, certificate lifecycle, etc.) as controllers that reconcile Kubernetes custom resources with a running system. Use `CustomResourceDefinitions` and controllers to declare intent and let the operator maintain the implementation.
</Callout>

Cert-manager (TLS lifecycle)

* You create a `Certificate` custom resource to declare the TLS certificate you need.
* The cert-manager operator watches that `Certificate`, requests or renews the certificate from an issuer (for example ACME/Let's Encrypt), and stores the resulting key material in a `Secret`.
* Applications consume the `Secret` to enable HTTPS and mutual TLS.

<Frame>
  <img alt="The image shows a flowchart of the cert-manager process, which monitors and requests a certificate, then stores sensitive data as a secret to enable encrypted HTTPS connections." />
</Frame>

Prometheus Operator (monitoring configuration)

* Instead of hand-editing Prometheus scrape configuration files, you create higher-level resources like `ServiceMonitor` or `PodMonitor`.
* The operator watches these objects and updates Prometheus' configuration automatically so the monitoring system stays aligned with declared intent.

<Frame>
  <img alt="The image is a diagram illustrating how the Prometheus operator works, showing the process from creating a ServiceMonitor to updating the scrape configuration for metrics collection." />
</Frame>

Databases (stateful workloads)

* A PostgreSQL operator watches a `PostgresCluster` (or similarly named custom resource) and manages the full lifecycle of a database cluster: creating and reconciling `StatefulSet` objects, performing backups, orchestrating failover, and coordinating upgrades.
* A `StatefulSet` is the Kubernetes workload type used for pods that need

<Frame>
  <img alt="The image illustrates a Postgres operator setup, showing the creation of a Postgres cluster with replicas. It highlights the operator's role in handling statefulsets, backups, failover, and upgrades." />
</Frame>

stable network identity and persistent storage — properties databases commonly require. Operators handle the complexity of ensuring replicas, leader election, and persistent volumes are created and reconciled.

Strimzi provides a comparable pattern for Kafka. It exposes custom resources to describe Kafka clusters, topics, and users; its controllers then ensure the running Kafka infrastructure matches the declared configuration.

The operator pattern repeats across projects:

1. The user writes a custom resource such as `Certificate`, `ServiceMonitor`, a PostgreSQL cluster resource, or a Kafka cluster resource.
2. A controller (the operator) watches that resource and detects when the real system diverges from the declared state.
3. The controller creates or updates lower-level Kubernetes objects (for example `Deployment`, `StatefulSet`, `Service`, `ConfigMap`, `Secret`) and performs application-specific actions to reconcile the system.

<Frame>
  <img alt="The image depicts a three-step process for creating custom resources, where a controller monitors the resources and then creates real objects." />
</Frame>

Example: a beginner WebApp operator

* In this learning example the custom resource is `WebApp`.
* The controller reconciles the `WebApp` resource by creating a `Deployment`, a `Service`, and a `ConfigMap`.
  * `Deployment`: runs the application pods and manages rollouts.
  * `Service`: provides a stable network name and load-balancing.
  * `ConfigMap`: stores non-sensitive configuration consumed by pods.

This small WebApp operator demonstrates the same pattern used by mature projects such as cert-manager, the Prometheus Operator, Postgres operators, and Kafka (Strimzi) — but at a manageable scope so you can learn the approach step by step.

<Frame>
  <img alt="The image depicts a diagram illustrating a WebApp operator that creates and manages deployments, services, and configmaps within a course context by KodeKloud." />
</Frame>

Operator examples at a glance

| Operator / Project      |             Primary custom resources | Operator responsibilities                                            |
| ----------------------- | -----------------------------------: | -------------------------------------------------------------------- |
| cert-manager            |                        `Certificate` | Request/renew TLS certs from issuers, store in `Secret`              |
| Prometheus Operator     |       `ServiceMonitor`, `PodMonitor` | Generate Prometheus scrape configs and manage Prometheus instances   |
| Postgres operator       | `PostgresCluster` (varies by vendor) | Manage `StatefulSet`, backups, failover, upgrades                    |
| Strimzi (Kafka)         |   `Kafka`, `KafkaTopic`, `KafkaUser` | Provision and reconcile Kafka clusters, topics, and users            |
| Example WebApp operator |                             `WebApp` | Create `Deployment`, `Service`, `ConfigMap` and keep them reconciled |

Links and references

* [cert-manager](https://cert-manager.io/)
* [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
* [Prometheus](https://prometheus.io/)
* [PostgreSQL](https://www.postgresql.org/)
* [Strimzi for Kafka](https://strimzi.io/)
* [Kubernetes concepts: StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

<Callout icon="warning">
  When designing operators, be careful with permissions and automated actions: reconciliations that modify persistent state (databases, storage, certificates) require thorough testing, RBAC scoping, and clear upgrade/backup strategies.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/a90ed95f-08b2-4d55-bed5-3926da81cd6d" />
</CardGroup>
