# Port-forward MinIO service (replace <minio-namespace> with the namespace where MinIO runs)
kubectl -n <minio-namespace> port-forward svc/minio 9000:9000

# Configure mc alias locally (example default MinIO credentials)
mc config host add minio http://localhost:9000 minio minio123

# Create a bucket for events
mc mb minio/argo-events-bucket
```

To check MinIO service presence in-cluster:

```bash theme={null}
# Replace <minio-namespace> with the namespace where MinIO is installed, e.g., "argo"
kubectl -n <minio-namespace> get svc
```

Example console output (truncated):

```text theme={null}
NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                AGE
argo-server   NodePort    10.98.122.61     <none>        2746:30774/TCP                         29h
httpbin       ClusterIP   10.103.119.102   <none>        9100/TCP                               29h
minio         NodePort    10.108.36.67     <none>        9000:30648/TCP,9001:30731/TCP          29h
```

## Create the Kubernetes Secret for MinIO credentials

Create a secret in the `argo-events` namespace so the EventSource can authenticate to MinIO. The simplest method is using kubectl:

```bash theme={null}
kubectl -n argo-events create secret generic minio-creds \
  --from-literal=accesskey=minio \
  --from-literal=secretkey=minio123
```

You should see:

```text theme={null}
secret/minio-creds created
```

Alternatively, if you want to apply YAML, use base64-encoded values:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: minio-creds
  namespace: argo-events
data:
  accesskey: bWluaW8=       # base64 for "minio"
  secretkey: bWluaW8xMjM=   # base64 for "minio123"
```

> **warning** Do not commit plain-text credentials to repositories. Use sealed secrets, HashiCorp Vault, or another secret management solution for production. Ensure RBAC limits who can read the `minio-creds` secret.

## EventSource manifest: MinIO listener

Below is a working EventSource YAML that registers a MinIO event source named `minio` with a configuration called `example`. It watches the `argo-events-bucket` bucket for object creation and deletion events, points at an in-cluster MinIO endpoint, and pulls credentials from the `minio-creds` secret.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: minio
  namespace: argo-events
spec:
  minio:
    example:
      bucket:
        name: argo-events-bucket
      endpoint: minio.argo.svc.cluster.local:9000
      events:
        - s3:ObjectCreated:Put
        - s3:ObjectRemoved:Delete
      insecure: true
      accessKey:
        name: minio-creds
        key: accesskey
      secretKey:
        name: minio-creds
        key: secretkey
```

Save this manifest as `eventsource-minio.yaml` (or a suitable name) and apply it:

```bash theme={null}
kubectl -n argo-events apply -f eventsource-minio.yaml
```

When the EventSource connects successfully, Argo Events will receive MinIO notifications for the configured events (e.g., PUT and DELETE) on the watched bucket and forward them to configured Sensors or other consumers.

## Test behavior and troubleshooting

* Upload or remove an object in `argo-events-bucket`. The MinIO server will emit a notification; Argo Events should receive it and generate a CloudEvent payload like the JSON example above.
* Check EventSource logs to verify connection and event receipt:

```bash theme={null}
# Replace <pod-name> with the event-source pod name if needed
kubectl -n argo-events logs deploy/eventsource-minio -c minio
```

* If you see authentication errors, re-check the secret keys and the MinIO endpoint and port.

Here is the MinIO console showing the newly created (empty) bucket:

<Frame>
  <img alt="A screenshot of the MinIO Object Store web console showing the &#x22;argo-events-bucket&#x22; bucket (empty) with sidebar navigation and upload/refresh controls. A small floating preview window at the top shows a GitHub Gist." />
</Frame>

## Next steps

* Create an Argo Events Sensor that subscribes to the `minio` EventSource and triggers an Argo Workflow, HTTP call, or other consumer when notifications arrive.
* Validate end-to-end by uploading/deleting objects and observing Sensor-triggered actions.
* Consider configuring retry/backoff and dead-lettering for production workflows.

> **lightbulb** Ensure the endpoint (service name, namespace, and port) is correct for your cluster (for example: minio.argo.svc.cluster.local:9000). Also make sure the credentials in the `minio-creds` secret match the MinIO server credentials.

## Links and references

* Argo Events documentation: [https://argoproj.github.io/argo-events/](https://argoproj.github.io/argo-events/)
* MinIO documentation: [https://min.io/docs/](https://min.io/docs/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* MinIO client (mc): [https://min.io/docs/minio/linux/reference/minio-mc.html](https://min.io/docs/minio/linux/reference/minio-mc.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/449de653-685b-462c-a0b7-0212d23309ad)


# Demo Trigger Conditions

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Trigger-Conditions/page

Explains Argo Events sensor trigger conditions, boolean expressions for dependencies, examples using MinIO and webhook, and RBAC considerations for workflow triggers.

Overview

Trigger conditions let you control which trigger templates execute based on the status of a sensor's dependencies in Argo Events. A sensor can declare multiple dependencies and multiple triggers; each trigger may include a boolean expression that references dependency names to determine when it should run.

This guide explains how condition expressions work, shows examples, and walks through a practical sensor that uses a MinIO event and a webhook to drive two triggers: one that submits an Argo Workflow and another that sends an HTTP request.

Relevant links and references

* [Argo Events — Sensors](https://argoproj.github.io/argo-events/sensors/)
* [Argo Workflows](https://argoproj.github.io/argo-workflows/)
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

Trigger conditions explained

* Conditions are boolean expressions referencing dependency names defined in the sensor's `dependencies` list.
* Supported operators: && (AND), || (OR). Parentheses are supported for grouping.
* If a trigger template omits `conditions`, it defaults to requiring all dependencies (implicit AND across all declared dependencies).

Operators summary

| Operator | Meaning  | Example        |    |                 |   |        |
| -------- | -------- | -------------- | -- | --------------- | - | ------ |
| &&       | AND      | `depA && depB` |    |                 |   |        |
|          |          |                | OR | \`depA          |   | depB\` |
| ( )      | Grouping | \`(depA        |    | depB) && depC\` |   |        |

Simple example: sensor with three dependencies and three triggers

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: example
spec:
  dependencies:
    - name: dep01
      eventSourceName: webhook-a
      eventName: example01
    - name: dep02
      eventSourceName: webhook-a
      eventName: example02
    - name: dep03
      eventSourceName: webhook-b
      eventName: example03
  triggers:
    - template:
        name: trigger01
        conditions: "dep02"
        http:
          url: http://abc.com/hello1
          method: GET
    - template:
        name: trigger02
        conditions: "dep02 && dep03"
        http:
          url: http://abc.com/hello2
          method: GET
    - template:
        name: trigger03
        conditions: "(dep01 || dep02) && dep03"
        http:
          url: http://abc.com/hello3
          method: GET
```

Example evaluations

* `conditions: "dep02"` — trigger runs when dependency `dep02` is satisfied.
* `conditions: "dep02 && dep03"` — trigger runs when both `dep02` and `dep03` are satisfied.
* `conditions: "(dep01 || dep02) && dep03"` — trigger runs when `dep03` is satisfied and at least one of `dep01` or `dep02` is satisfied.

Practical multi-dependency sensor (MinIO + webhook)

Below is a real-world sensor manifest that demonstrates two dependencies and two triggers:

* `hello-workflow-trigger` submits an Argo Workflow and only fires when the MinIO dependency is satisfied.
* `http-trigger` posts to an external HTTP endpoint and fires when either dependency is satisfied.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: multi-dependency-sensor-2
  namespace: argo-events
spec:
  dependencies:
    - name: test-dep
      eventSourceName: minio
      eventName: example
    - name: my-webhook-dep
      eventSourceName: webhook
      eventName: my-webhook
  triggers:
    - template:
        name: hello-workflow-trigger
        # Use a service account that has permission to create Workflows in the 'argo' namespace
        serviceAccountName: workflow-trigger-sa
        conditions: "test-dep"
        argoWorkflow:
          source:
            resource:
              apiVersion: argoproj.io/v1alpha1
              kind: Workflow
              metadata:
                generateName: hello-kodekloud-
                namespace: argo
              spec:
                entrypoint: whalesay
                templates:
                  - name: whalesay
                    container:
                      image: rancher/cowsay
                      command: ["cowsay"]
                      args: ["Triggering workflow from Argo Events"]
    - template:
        name: http-trigger
        conditions: "test-dep || my-webhook-dep"
        http:
          url: https://httpdump.app/inspect/ee487aa0-994f-4b9f-83dd-a65e668ccfc8
          method: POST
          payload: |
            {
              "bucket": "{{dependency.test-dep.data.notification.0.s3.bucket.name}}",
              "type": "{{dependency.test-dep.context.type}}"
            }
        retryStrategy:
          steps: 3
          duration: 3s
```

Notes about the workflow trigger and RBAC

* The workflow trigger sets `serviceAccountName: workflow-trigger-sa`. That service account must have RBAC permissions (Role/ClusterRole and corresponding RoleBinding/ClusterRoleBinding) that allow creating Workflows in the `argo` namespace.
* If the trigger uses the default service account (or a service account lacking permissions), the Workflow creation will fail with a permission error.

Testing the configuration

1. Expose the webhook event source locally (port-forward) and send a test event:

```bash theme={null}
kubectl -n argo-events port-forward svc/webhook-eventsource-svc 13000:13000
