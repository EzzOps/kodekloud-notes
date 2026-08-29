# List ServiceAccounts in the argo-events namespace
kubectl -n argo-events get sa

# Create the new ServiceAccount
kubectl create sa workflow-trigger-sa -n argo-events

# Verify it was created
kubectl -n argo-events get sa
```

Expected output after creation:

```text theme={null}
NAME                 SECRETS   AGE
argo-events-sa       0         40m
default              0         40m
workflow-trigger-sa  0         1s
```

***

## 2. Create Role and RoleBinding for Argo Workflows

Create a Role in the `argo` namespace that grants the minimum permissions the Sensor needs for Argo Workflows, and a RoleBinding that binds the `workflow-trigger-sa` ServiceAccount from the `argo-events` namespace to that Role.

Manifest to apply:

```yaml theme={null}
# sensor-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: submit-workflow-role
  namespace: argo
rules:
  - apiGroups: ["argoproj.io"]
    resources: ["workflows"]
    verbs: ["create", "get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: trigger-workflow-binding
  namespace: argo
subjects:
  - kind: ServiceAccount
    name: workflow-trigger-sa
    namespace: argo-events
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: submit-workflow-role
```

Apply the manifest:

```bash theme={null}
kubectl apply -f https://gist.github.com/sidd-[SECRET_REDACTED]/[AWS_SECRET_ACCESS_KEY]/sensor-rbac.yaml
```

Expected apply output:

```text theme={null}
role.rbac.authorization.k8s.io/submit-workflow-role created
rolebinding.rbac.authorization.k8s.io/trigger-workflow-binding created
```

<Callout icon="lightbulb">
  If you see an error like "unknown command 'apply' for 'kubectl1'", it likely indicates an alias or PATH issue (for example, `k` pointing to an unexpected binary). Use the full `kubectl` binary or fix the alias so `k` maps to `kubectl`.
</Callout>

***

## 3. Update the Sensor to Use the ServiceAccount

Edit your Sensor manifest to set `spec.template.serviceAccountName` to the ServiceAccount you created (`workflow-trigger-sa`). Below is a minimal Sensor snippet showing where to configure this:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook
  namespace: argo-events
spec:
  template:
    serviceAccountName: workflow-trigger-sa
  dependencies:
    - name: my-webhook-dep
      eventSourceName: webhook
      eventName: my-webhook
  triggers:
    - template:
        name: hello-workflow-trigger
        argoWorkflow:
          source:
            resource:
              apiVersion: argoproj.io/v1alpha1
              kind: Workflow
              metadata:
                generateName: hello-kodekloud-
                namespace: argo
              spec:
                entrypoint: cowsay
                templates:
                  - name: cowsay
                    container:
                      image: rancher/cowsay
                      command: ["cowsay"]
                      args: ["Hello Kode Kloud from ArgoEvents!!"]
```

Apply the updated Sensor manifest or edit the resource directly:

```bash theme={null}
kubectl apply -f sensor-updated.yaml -n argo-events
# or edit in place
kubectl edit sensor webhook -n argo-events
```

After updating, the Sensor will use `workflow-trigger-sa` when creating Workflows in the `argo` namespace.

***

## 4. Trigger the Sensor and Confirm Workflow Creation

Trigger the webhook event source (example using curl):

```bash theme={null}
curl -d '{"message":"hello"}' -H "Content-Type: application/json" -X POST http://localhost:13000/push
```

You should receive a success response from the event source (for example, `success`). Then check logs to confirm the event flow:

Example event source logs:

```text theme={null}
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, time=2025-10-25T11:12:45Z, msg="Succeeded to publish an event"
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, time=2025-10-25T11:12:59Z, msg="Successfully dispatched the request to the event bus"
```

Example Sensor logs:

```json theme={null}
{"level":"info","ts":"2025-10-25T11:12:42.920827Z","msg":"Sensor started.","sensorName":"webhook-sensor"}
{"level":"info","ts":"2025-10-25T11:13:00.188816Z","msg":"Successfully processed trigger 'hello-workflow-trigger'","sensorName":"webhook-sensor","triggerName":"hello-workflow-trigger","triggerType":"ArgoWorkflow"}
```

Verify the Workflow exists in the `argo` namespace:

```bash theme={null}
kubectl -n argo get wf
```

Describe the Workflow to inspect labels and the ServiceAccount used by the creator:

```bash theme={null}
kubectl -n argo describe wf <workflow-name>
```

You should see labels like `workflow.argoproj.io/creator` and evidence that the Workflow was submitted by the `workflow-trigger-sa` ServiceAccount.

Check the Workflow pod logs to confirm the job ran successfully (example cowsay output):

```text theme={null}
hello-kodekloud-xxxxx: < Hello Kode Kloud from ArgoEvents!! >
hello-kodekloud-xxxxx: -------------------------------
hello-kodekloud-xxxxx:         \   ^__^
hello-kodekloud-xxxxx:          \  (oo)\_______
hello-kodekloud-xxxxx:             (__)\       )\/\
hello-kodekloud-xxxxx:              ||----w |
hello-kodekloud-xxxxx:              ||     ||
```

***

## Summary / Event Flow

* The webhook EventSource receives the HTTP POST and publishes the event to the event bus.
* The Sensor subscribes to the event bus, evaluates dependencies, and triggers the Argo Workflow.
* The Sensor uses the configured `spec.template.serviceAccountName` (`workflow-trigger-sa`) to submit the Workflow into the `argo` namespace.
* The Role and RoleBinding in the `argo` namespace grant the ServiceAccount the necessary permissions to create and read Argo Workflows.

This setup ensures your Sensor submits Workflows securely using a limited, purpose-built ServiceAccount instead of the cluster default ServiceAccount.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/742cc217-3558-4a27-868c-e15f28ecf1c4" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/cafc7b5f-8bda-414a-824d-a36b02e5344c" />
</CardGroup>


# Demo Create a MinIO Sensor

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Create-a-MinIO-Sensor/page

Guide to creating an Argo Events Sensor that listens to MinIO bucket events and sends HTTP POSTs to an inspection endpoint like httpdump.app

In this lesson you'll create an Argo Events Sensor that invokes an HTTP endpoint whenever MinIO bucket events occur. We use an HTTP trigger to POST to a test endpoint (httpdump.app) so you can inspect the received request and payload.

For background, Sensors support HTTP triggers among many other trigger types. See the official Argo Events sensors documentation: [https://argoproj.github.io/argo-events/sensors/](https://argoproj.github.io/argo-events/sensors/)

<Frame>
  <img alt="A screenshot of the Argo Events documentation page for &#x22;HTTP Trigger&#x22; with a left-side user guide menu and top navigation bar. The central diagram shows various event sources feeding into Argo Events, which then trigger serverless targets like OpenFaaS, Kubeless, Knative and Nuclio." />
</Frame>

Overview

* Goal: When an object is created or removed in a specified MinIO bucket, the EventSource publishes an event to the event bus. The Sensor listens for that event and performs an HTTP POST to a configured endpoint.
* Test target: use an HTTP dump service (httpdump.app) to inspect requests made by the Sensor.

Sensor manifest example

* This Sensor listens for an event published by an EventSource named `minio` (event name `example`) and posts to an HTTP dump URL. The trigger uses POST and a simple retry strategy (3 attempts, 3s between retries).

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: minio
spec:
  dependencies:
    - name: test-dep
      eventSourceName: minio
      eventName: example
  triggers:
    - template:
        name: http-trigger
        http:
          url: https://httpdump.app/inspect/ee487aa0-994f-4b9f-83dd-a65e668ccfc8
          payload: null
          method: POST
      retryStrategy:
        steps: 3
        duration: "3s"
```

Notes on the manifest

* dependencies: describes which EventSource and event name satisfy the Sensor.
* http.url: replace the example URL with the dump URL you create at httpdump.app.
* payload: when set to `null`, the Sensor sends an empty request body. You can instead provide a JSON payload or use payload parameters to inject event data.
* retryStrategy: controls retries for transient failures.

Create a test endpoint on httpdump.app

* Use httpdump.app (or similar services) to create a unique dump URL. The page shows a curl example and the generated dump endpoint you should paste into the Sensor spec.

<Frame>
  <img alt="A browser screenshot of the httpdump.app webpage showing a &#x22;Waiting for incoming requests...&#x22; message and a highlighted example curl command. The page displays a generated dump URL and instructions for POSTing JSON to that endpoint." />
</Frame>

EventSource manifest (MinIO)

* The EventSource listens to bucket notifications from MinIO and forwards events to the Argo Events bus. Example:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: minio
spec:
  minio:
    example:
      endpoint: minio.argo.svc.cluster.local:9000
      bucket:
        name: argo-events-bucket
      insecure: true
      accessKey:
        name: minio-creds
        key: accesskey
      secretKey:
        name: minio-creds
        key: secretkey
      events:
        - s3:ObjectCreated:Put
        - s3:ObjectRemoved:Delete
status:
  conditions:
    - type: Deployed
      status: "True"
      lastTransitionTime: "2025-10-25T11:27:04Z"
    - type: SourcesProvided
      status: "True"
      lastTransitionTime: "2025-10-25T11:27:04Z"
```

Quick field guide

| Resource            | Purpose                                      | Example field                     |
| ------------------- | -------------------------------------------- | --------------------------------- |
| EventSource (minio) | Listens for MinIO bucket notifications       | `events: [s3:ObjectCreated:Put]`  |
| Sensor              | Evaluates dependencies and executes triggers | `triggers[].http.url`             |
| HTTP dump endpoint  | Destination to inspect POST requests         | `https://httpdump.app/dumps/<id>` |

How the flow works

1. Upload or delete a file in the configured MinIO bucket (`argo-events-bucket`).
2. MinIO emits a bucket notification; the EventSource receives it and publishes the event to the event bus.
3. The Sensor evaluates its dependency (`test-dep`) and, once satisfied, executes the HTTP trigger.
4. The Sensor performs an HTTP POST to the configured httpdump URL (with the configured payload or empty body if `payload: null`).

Test with curl

* You can directly POST test JSON to your dump URL to see how the endpoint receives requests:

```bash theme={null}
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"Marcel","password":"supersecret","this is a":"test"}' \
  https://httpdump.app/dumps/6758c612-9d34-486f-b82a-63c0a7dc4054
```

Example logs

* EventSource logs (show initialization, credential retrieval, client setup, and event publication):

```text theme={null}
namespace=argo-events, eventSourceName=minio, eventName=example, level=info, time=2025-10-25T11:32:53Z, msg=starting minio event source...
namespace=argo-events, eventSourceName=minio, eventName=example, level=info, time=2025-10-25T11:32:53Z, msg=retrieving access and secret key...
namespace=argo-events, eventSourceName=minio, eventName=example, level=info, time=2025-10-25T11:32:53Z, msg=setting up a minio client...
namespace=argo-events, eventSourceName=minio, eventName=example, level=info, time=2025-10-25T11:32:53Z, msg=started listening to bucket notifications...
namespace=argo-events, eventSourceName=minio, eventName=example, level=info, time=2025-10-25T11:32:53Z, msg=Succeeded to publish an event
```

* Sensor logs (show dependency evaluation and trigger execution):

```text theme={null}
namespace=argo-events, sensorName=minio, level=info, time=2025-10-25T11:33:02Z, msg=starting sensor server
namespace=argo-events, sensorName=minio, level=info, time=2025-10-25T11:33:02Z, msg=Sensor started.
namespace=argo-events, sensorName=minio, triggerName=http-trigger, level=info, time=2025-10-25T11:33:02Z, msg=Dependency expression for trigger http-trigger: test-dep
namespace=argo-events, sensorName=minio, triggerName=http-trigger, level=warn, time=2025-10-25T11:33:02Z, msg=payload parameters are not specified. request payload will be an empty string
namespace=argo-events, sensorName=minio, triggerName=http-trigger, level=info, time=2025-10-25T11:33:02Z, msg=Making a http request...
namespace=argo-events, sensorName=minio, triggerName=http-trigger, level=info, time=2025-10-25T11:33:02Z, msg=Successfully processed trigger 'http-trigger'
```

Example dump output

* If `payload: null` the request body will be empty but headers and timing information are recorded by the dump service:

```text theme={null}
POST /dumps/6758c612-9d34-486f-b82a-63c0a7dc4054
Received at: 2025-10-25 11:32:48

Headers
Accept-Encoding: gzip
Content-Length: 0
Content-Type:
Host: httpdump.app
User-Agent: Go-http-client/2.0

Request Body
```

Best practices and security

<Callout icon="lightbulb">
  When testing, use ephemeral credentials and a disposable dump URL. For production, secure your triggers with authentication, TLS, and least-privilege credentials for MinIO.
</Callout>

<Callout icon="warning">
  Do not expose sensitive access keys or secret keys in public manifests. Use Kubernetes secrets and RBAC to restrict access to Argo Events resources.
</Callout>

Adaptations and next steps

* Replace the HTTP trigger with other Argo Events targets if you want to invoke serverless functions, message queues, or custom webhooks.
* Add payload parameters or a payload template to include event metadata (object key, bucket name, event type) in the POST request body.
* Expand retry configuration and add backoff strategies for more resilient integrations.

Links and references

* [Argo Events Sensors documentation](https://argoproj.github.io/argo-events/sensors/)
* [MinIO Documentation](https://min.io/docs/)
* [httpdump.app](https://httpdump.app/) - HTTP request inspection for testing

This demonstrates how to detect MinIO bucket events with Argo Events and invoke HTTP APIs via Sensors. You can extend the Sensor to send structured JSON payloads, headers, or authentication to fit your integration needs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/f4de18c8-0a1f-40ee-a08d-70d299f6fe9e" />
</CardGroup>
