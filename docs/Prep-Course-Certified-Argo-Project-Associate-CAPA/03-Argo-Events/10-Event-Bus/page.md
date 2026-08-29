# Optional: to install Argo Workflows (if you will trigger Workflows from Events)
# kubectl create namespace argo
# kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/install.yaml
```

You should see output similar to the example below as Kubernetes creates CRDs, RBAC, ConfigMaps, and the controller deployment:

```bash theme={null}
namespace/argo-events created
customresourcedefinition.apiextensions.k8s.io/eventbus.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/eventsources.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/sensors.argoproj.io created
serviceaccount/argo-events-sa created
clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-admin created
clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-edit created
clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-view created
clusterrole.rbac.authorization.k8s.io/argo-events-role created
clusterrolebinding.rbac.authorization.k8s.io/argo-events-binding created
configmap/argo-events-controller-config created
deployment.apps/controller-manager created
```

## Verify installation

List all resources in the `argo-events` namespace:

```bash theme={null}
kubectl -n argo-events get all
```

When images are being pulled and the pod is scheduled, the controller pod may show `ContainerCreating` until the container is ready. Example output while the controller is still starting:

```bash theme={null}
NAME                                          READY   STATUS             RESTARTS   AGE
pod/controller-manager-59884fd695-kt5gm      0/1     ContainerCreating  0          10s

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/controller-manager   0/1     1            0           10s

NAME                                                DESIRED   CURRENT   READY   AGE
replicaset.apps/controller-manager-59884fd695        1         1         0       10s
```

## UI: Viewing EventSources and Sensors

Argo Events does not include a standalone web UI. If you install Argo Workflows and integrate it with Argo Events, the Argo Workflows UI can display EventSources and Sensors. Open the Argo Workflows UI and select the appropriate namespace (for example, `argo-events`) to view event-related resources.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a list of workflows with columns for name, namespace, start/finish times, duration and progress, plus a left-side filter panel. The top bar includes buttons to submit a new workflow and view completed workflows." />
</Frame>

When no EventSources are present, the Event Sources page shows an empty state and a button to create a new EventSource.

<Frame>
  <img alt="A web UI screenshot of the &#x22;argo-events&#x22; Event Sources page showing a message &#x22;No event sources&#x22; with explanatory text and a &#x22;+ CREATE NEW EVENTSOURCE&#x22; button. A left-side vertical icon menu and a browser address bar are also visible." />
</Frame>

The Sensors UI page also shows an empty state until sensors are created. The visual editor helps illustrate how sensors connect to triggers, the event bus, and other components.

<Frame>
  <img alt="A browser screenshot of the Argo Events &#x22;Sensors&#x22; page displaying a &#x22;No sensors&#x22; message and explanatory text, with a &#x22;+ CREATE NEW SENSOR&#x22; button at the top. The UI shows a left icon sidebar and the page title &#x22;argo-events&#x22; in the header." />
</Frame>

<Callout icon="lightbulb">
  If the controller pod remains in ContainerCreating or enters CrashLoopBackOff, inspect the pod events and logs with:

  * `kubectl -n argo-events describe pod <pod-name>`
  * `kubectl -n argo-events logs <pod-name>`
    These commands help identify scheduling, image pull, or runtime errors.
</Callout>

## Common resources created by the install

| Resource Type                                   | Purpose                                                      |
| ----------------------------------------------- | ------------------------------------------------------------ |
| CustomResourceDefinitions (CRDs)                | Define EventBus, EventSource, and Sensor custom resources    |
| ServiceAccount, ClusterRole, ClusterRoleBinding | RBAC for the controller to watch and manage resources        |
| ConfigMap                                       | Controller configuration (e.g., metrics, event bus settings) |
| Deployment / ReplicaSet / Pod                   | Controller manager that reconciles EventSources and Sensors  |

## Troubleshooting checklist

* Confirm the controller pod is scheduled and not pending:
  * `kubectl -n argo-events get pods`
* If `ContainerCreating`, check node space and image pull errors:
  * `kubectl -n argo-events describe pod <pod-name>`
* If the pod crashes repeatedly, view logs for stack traces:
  * `kubectl -n argo-events logs <pod-name>`
* Verify CRDs were created successfully:
  * `kubectl get crd | grep argo`

## Next steps

* Wait for the `controller-manager` pod to reach READY state before creating EventSources and Sensors.
* Create EventSource and Sensor manifests to connect your external events to triggers (e.g., Webhook, cron, Kafka) and test end-to-end behavior.
* If using Argo Workflows, create a Workflow template and configure a Sensor trigger to submit workflows on events.

## Links and references

* Argo Events (project): [https://argoproj.github.io/argo-events/](https://argoproj.github.io/argo-events/)
* Argo Workflows (project): [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/8deb0625-970f-4706-a9bb-95f3a15a5590" />
</CardGroup>


# Event Bus

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Event-Bus/page

Overview of Argo Events EventBus using NATS or JetStream, covering managed versus external deployments, configuration examples, persistence, security, and production best practices.

Let's dive into the EventBus and the components around it.

Think of the EventBus as the central highway or nervous system for your events. It is a publish/subscribe system that lets different parts of your infrastructure communicate without tight coupling: event sources publish events to the EventBus and sensors (or other consumers) subscribe to those events. This decoupling enables many producers and many consumers to coexist and evolve independently.

Under the hood, Argo Events uses NATS technologies as the transport layer for the EventBus:

* Historically NATS Streaming (STAN) has been used.
* JetStream is the newer NATS offering and provides advanced streaming and durability features.

See the official Argo Events documentation for the CRD reference and the NATS docs for transport specifics:

* [Argo Events — EventBus CRD](https://argoproj.github.io/argo-events/)
* [NATS Documentation (JetStream & STAN)](https://nats.io/)

<Callout icon="lightbulb">
  Argo Events supports two general EventBus deployment modes: a managed (native) mode where Argo Events installs and manages a NATS cluster for you, and an external mode where Argo Events connects to an existing NATS/JetStream cluster you already operate.
</Callout>

## What the EventBus spec configures

The EventBus Custom Resource (CRD) declares whether Argo Events should:

* install and manage a NATS cluster (native/managed), or
* connect to an already-running NATS/JetStream cluster (external/existing).

Typical configuration areas in the EventBus spec:

|        Resource area | Purpose                                                                |
| -------------------: | ---------------------------------------------------------------------- |
|                 Mode | Choose managed (native) or external (existing)                         |
|     Replication / HA | Number of NATS replicas to run for resilience                          |
|       Authentication | Token-based auth, TLS, or no-auth for quick tests                      |
|          Persistence | Disk-backed storage for durable messaging (recommended for production) |
| Network / Connection | URLs, ports, TLS and secret references for external clusters           |

Below are representative examples for both managed and external modes. These snippets are illustrative—consult your Argo Events release docs for the exact CRD fields supported by your version.

### Native (managed) example

This instructs Argo Events to create and manage a NATS Streaming or JetStream cluster for you. Typical fields set here include replica count, authentication, and persistence.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: my-eventbus
spec:
  native:
    replicas: 3
    # Authentication: token, or "none" for simple test clusters
    auth:
      type: token
      token: my-nats-token
    # Persistence: enable disk storage for durability
    persistence:
      enabled: true
      # Typical storage class and size for durable message storage
      storage:
        size: 10Gi
        storageClassName: standard
    # (Optional) resources, image or other native-specific fields...
```

Notes:

* Running at least three replicas is a common high-availability pattern for production clusters.
* Persistence (disk-backed storage) prevents message loss if NATS instances restart; in-memory-only clusters can lose messages on crash/restart.

<Callout icon="lightbulb">
  Always enable persistence and select an appropriate storageClass and size for production. If you plan to use JetStream, persistent storage is required to meet durability guarantees.
</Callout>

### External / existing cluster example

If you already run a NATS or JetStream cluster, configure the EventBus to connect to it by supplying connection endpoints and any TLS/auth settings required.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: my-external-eventbus
spec:
  # Use an existing external cluster rather than creating one natively
  existingNats:
    url: "nats://nats.example.com:4222"
    # Optional TLS configuration or authentication information:
    tls:
      enabled: true
      # references to Kubernetes secrets for certs/keys would go here
    auth:
      type: token
      token: "external-nats-token"
```

Notes:

* Use this mode when you operate a centralized messaging layer shared across teams or already manage a hardened NATS/JetStream cluster.
* Ensure correct network routing, TLS certificates, and credentials so Argo Events can reliably connect to the external cluster.

## Managed vs External — quick comparison

| Mode                | When to use                                           | Key considerations                                                                                     |
| ------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Managed / native    | Single-tenant Argo Events deployments or quick setups | Argo manages lifecycle; convenient but you’re responsible for cluster sizing, persistence, and backups |
| External / existing | When a central messaging platform is already in place | Integrate with existing security, observability, and HA practices; network & TLS must be configured    |

## JetStream vs NATS Streaming (STAN)

* JetStream provides modern streaming semantics, richer retention and persistence options, and improved operator features.
* STAN is legacy NATS Streaming and may be present in older Argo Events setups; check compatibility of your Argo Events version.
* Prefer JetStream for production-grade durability and advanced streaming features when supported by your Argo Events release.

## Best practices

* Development / demos:
  * Use native mode with minimal replicas and optional no-auth for rapid iteration.
  * Persistence can be disabled for ephemeral test clusters.
* Production:
  * Use native mode with at least three replicas or connect to a hardened external NATS/JetStream cluster.
  * Enable persistence with an appropriate storageClass and capacity.
  * Secure the cluster with TLS and token-based auth (or more advanced auth mechanisms).
  * Use JetStream when you need durable message storage, advanced retention, or streaming guarantees—confirm Argo Events version support.
* Observability and operations:
  * Monitor NATS instance metrics and JetStream stream state.
  * Plan backups or retention policies for stored messages if they are business-critical.

## Links and references

* [Argo Events — Official Documentation](https://argoproj.github.io/argo-events/)
* [NATS: JetStream documentation](https://docs.nats.io/jetstream)
* [NATS Streaming (STAN) legacy docs](https://docs.nats.io/legacy/nats-streaming)

This covers the key concepts and configuration choices when setting up the EventBus in Argo Events. Adjust the example fields above to match the exact EventBus CRD for the Argo Events release you are running.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/219faf14-5ff0-4a36-b705-ef6956d8019d" />
</CardGroup>
