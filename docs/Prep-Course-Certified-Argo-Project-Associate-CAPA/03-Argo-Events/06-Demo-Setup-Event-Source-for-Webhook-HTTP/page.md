# List services in argo-events
kubectl -n argo-events get svc

# Example service you should see:
# NAME                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)      AGE
# Port-forward the webhook EventSource service to localhost:13000
kubectl port-forward -n argo-events svc/webhook-eventsource-svc 13000:13000
```

Send a test payload (POST to `/push`):

```bash theme={null}
curl -d '{"message": "hello"}' \
  -H "Content-Type: application/json" \
  -X POST http://localhost:13000/push
```

Expected lightweight response:

```text theme={null}
success
```

## Inspecting logs and the event flow

* The EventSource pod logs will show the webhook receiving the request, validating the route, and publishing the event to the EventBus.
* The Sensor logs show subscription to the EventBus and then the attempt to execute the trigger when an event arrives.

Representative (abridged) log lines:

EventSource logs (abridged):

```text theme={null}
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, msg="route is activated"
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, msg="a request received, processing it..."
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, msg="Succeeded to publish an event"
namespace=argo-events, eventSourceName=webhook, eventName=my-webhook, level=info, msg="successfully dispatched the request to the event bus"
```

Sensor logs (abridged):

```text theme={null}
namespace=argo-events, sensorName=webhook-sensor, level=info, msg="Sensor started."
namespace=argo-events, sensorName=webhook-sensor, level=info, msg="Dependency expression for trigger hello-workflow-trigger: my-webhook-dep"
namespace=argo-events, sensorName=webhook-sensor, level=info, msg="Connected to NATS server."
namespace=argo-events, sensorName=webhook-sensor, level=error, msg="Create request failed" error="workflows.argoproj.io is forbidden: User \"system:serviceaccount:argo-events:default\" cannot create resource \"workflows\" in API group \"argoproj.io\" in the namespace \"argo\""
namespace=argo-events, sensorName=webhook-sensor, level=info, msg="Error: Failed to submit workflow: rpc error: code = PermissionDenied desc = workflows.argoproj.io is forbidden: User \"system:serviceaccount:argo-events:default\" cannot create resource \"workflows\" in the namespace \"argo\""
```

### Why the trigger failed

The Sensor attempted to create an Argo Workflow in the `argo` namespace, but the service account used by the Sensor (`system:serviceaccount:argo-events:default` in this example) does not have RBAC permissions to create `workflows.argoproj.io` in the `argo` namespace. This caused the PermissionDenied error in the Sensor logs.

> **warning** Ensure the service account configured for the Sensor (via spec.template.serviceAccountName or in the Sensor controller pod) has appropriate RBAC permissions to create the target resources (Argo Workflows or Kubernetes objects) in the target namespace.

## Solution outline (RBAC and service account)

Steps to resolve:

1. Create or select a service account that has a Role or ClusterRole with permissions to create/submit the target resource (e.g., `workflows.argoproj.io`) in the target namespace.
2. Create a RoleBinding or ClusterRoleBinding that binds the Role/ClusterRole to the service account.
3. Configure your Sensor to use that service account, for example via `spec.template.serviceAccountName: <name>`.
4. Re-trigger the webhook; the Sensor should now be able to submit the Workflow.

Quick RBAC reference:

| Resource Type                    | Use Case                                                      | Example                                                       |
| -------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| Role / RoleBinding               | Grant namespace-scoped permissions for Sensor service account | Grant `create` on `workflows.argoproj.io` in `argo` namespace |
| ClusterRole / ClusterRoleBinding | Grant cluster-scoped permissions if needed across namespaces  | Grant `create` on `workflows.argoproj.io` cluster-wide        |
| ServiceAccount                   | Token identity used by Sensor to act against the API server   | `create-pod-sa` used by Sensor template                       |

References:

* [Argo Events - Triggers](https://argoproj.github.io/argo-events/)
* [Argo Workflows](https://argoproj.github.io/argo-workflows/)
* [Kubernetes RBAC docs](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

## Kubernetes object trigger example (create a Pod)

Triggers can also create generic Kubernetes objects (Pods, Deployments, Jobs, etc.). For such triggers, grant the service account the required permissions for the relevant Kubernetes API resources.

<Frame>
  <img alt="A screenshot of the Argo Events documentation page titled &#x22;Kubernetes Object Trigger,&#x22; showing the left navigation menu, main explanatory text, and a diagram illustrating events triggering Kubernetes objects. The page has a green top header and a table of contents on the right." />
</Frame>

Example Sensor that specifies a service account and creates a Pod via the `k8s` trigger:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook
  namespace: argo-events
spec:
  template:
    serviceAccountName: create-pod-sa  # use a service account with privileges to create pods
  dependencies:
    - name: test-dep
      eventSourceName: webhook
      eventName: example
  triggers:
    - template:
        name: webhook-pod-trigger
        k8s:
          operation: create
          source:
            resource:
              apiVersion: v1
              kind: Pod
              metadata:
                generateName: hello-world-
              spec:
                containers:
                  - name: hello-container
                    image: busybox
                    command: ["/bin/sh", "-c"]
                    args: ["echo hello-world"]
      parameters:
        - src:
            dependencyName: test-dep
            # optionally map event data into the pod manifest via parameters
```

## Next steps

* Create a service account and bind the appropriate Role/ClusterRole to it (use RoleBinding or ClusterRoleBinding).
* Update your Sensor to reference the service account via `spec.template.serviceAccountName`.
* Re-submit the event to your webhook and watch the Sensor create the target resource (Workflow or Pod).
* Consult the Argo Events documentation for advanced trigger parameterization and transformations.

Useful links:

* [Argo Events Documentation](https://argoproj.github.io/argo-events/)
* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [Kubernetes kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/0793f959-c18e-4213-bc00-9f9077c539b8)


# Demo Setup Event Source for Webhook HTTP

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Setup-Event-Source-for-Webhook-HTTP/page

Guide to configuring an Argo Events webhook EventSource in Kubernetes, converting HTTP requests into CloudEvents envelopes, exposing and testing the service, and troubleshooting deployment and networking

This guide shows how to create an Argo Events EventSource that exposes an HTTP webhook, how the webhook maps to CloudEvents-style payloads, and how to verify the EventSource and Service inside your Kubernetes cluster. Use this tutorial to receive webhooks from external systems (GitHub, GitLab, CI/CD tools, custom services) and forward them into Argo's eventing pipeline.

Argo Events supports many sources (AWS SNS, SQS, Azure services, calendar events, GCP Pub/Sub, GitHub, GitLab, Bitbucket, MinIO, Kafka, and more). For this demo we use the webhook EventSource, which runs an HTTP server and transforms incoming requests into CloudEvents-style envelopes.

## CloudEvents envelope examples

A typical CloudEvents-style envelope produced by Argo Events contains a context and data section:

```json theme={null}
{
  "context": {
    "type": "type_of_event_source",
    "specversion": "cloud_events_version",
    "source": "name_of_the_event_source",
    "id": "unique_event_id",
    "time": "event_time",
    "datacontenttype": "type_of_data",
    "subject": "name_of_the_configuration_within_event_source"
  },
  "data": {
    "eventTime": "2025-10-25T10:45:36Z",
    "userPayload": { /* static payload available in the event source */ }
  }
}
```

When the webhook receives an HTTP request, the event payload typically includes the request headers and body:

```json theme={null}
{
  "context": {
    "type": "type_of_event_source",
    "specversion": "cloud_events_version",
    "source": "name_of_the_event_source",
    "id": "unique_event_id",
    "time": "event_time",
    "datacontenttype": "type_of_data",
    "subject": "name_of_the_configuration_within_event_source"
  },
  "data": {
    "header": { /* headers from the received HTTP request */ },
    "body": { /* payload received in the HTTP request body */ }
  }
}
```

Note: the exact structure may vary depending on how the EventSource is configured (e.g., static payloads, custom converters, or secret mappings).

> **lightbulb** The webhook EventSource listens on the configured port and endpoint. By default, Argo Events will create a Kubernetes Service that exposes the same port. If you want traffic from outside the cluster to reach the webhook, expose the Service using a suitable type for your environment (LoadBalancer, NodePort, Ingress, etc.).

## Prerequisites

* A Kubernetes cluster with kubectl configured to access it.
* Argo Events (controller, eventbus, etc.) installed into a namespace (commonly argo-events).
* Optional: an Ingress or LoadBalancer if you need external, public endpoints.

## Install Argo Events (if needed)

Apply the upstream manifests to install Argo Events and an example Sensor. Adjust URLs if you use local manifests:

```bash theme={null}
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/master/manifests/install.yaml
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/sensor.yaml
```

## Example EventSource manifest (webhook)

Below is an example EventSource that creates:

* A webhook listener on port 13000.
* An endpoint at /push which accepts only POST requests.
* A generated ClusterIP Service exposing port 13000.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: webhook
  namespace: argo-events
spec:
  service:
    ports:
      - port: 13000
        targetPort: 13000
  webhook:
    my-webhook:
      port: "13000"
      endpoint: /push
      method: "POST"
```

Key fields explained:

| Field                         | Purpose                                          | Example |
| ----------------------------- | ------------------------------------------------ | ------- |
| spec.service.ports.port       | Port exposed by the generated Kubernetes Service | 13000   |
| spec.webhook.\<name>.port     | Port the webhook server listens on (string)      | "13000" |
| spec.webhook.\<name>.endpoint | HTTP path to accept events on                    | /push   |
| spec.webhook.\<name>.method   | Restrict allowed HTTP methods (POST, GET, etc.)  | "POST"  |

Apply the manifest (for example save as webhook-eventsource.yaml):

```bash theme={null}
kubectl apply -f webhook-eventsource.yaml
```

If you created the EventSource via the Argo UI, the same resources are created in the selected namespace.

## Verify the EventSource and Service

List resources in the argo-events namespace to confirm the EventSource pod and Service are running:

```bash theme={null}
kubectl get all -n argo-events
```

Example output (trimmed for clarity):

```bash theme={null}
NAME                                             READY   STATUS    RESTARTS   AGE
pod/controller-manager-59884fd695-kt5gm         1/1     Running   0          16m
pod/eventbus-default-stan-0                     2/2     Running   0          9m
pod/eventbus-default-stan-1                     2/2     Running   0          9m
pod/eventbus-default-stan-2                     2/2     Running   0          9m
pod/webhook-eventsource-8jhxz-b99f96879-nw6pb   1/1     Running   0          24s

NAME                                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
service/eventbus-default-stan-svc      ClusterIP   None             <none>        4222/TCP,...      9m
service/webhook-eventsource-svc        ClusterIP   10.104.178.99    <none>        13000/TCP         24s

NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/controller-manager          1/1     1            1           16m
deployment.apps/webhook-eventsource-8jhxz   1/1     1            1           24s

NAME                                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/controller-manager-59884fd695          1         1         1       16m
replicaset.apps/webhook-eventsource-8jhxz-b99f96879    1         1         1       24s

NAME                                      READY   AGE
statefulset.apps/eventbus-default-stan    3/3     9m
```

This confirms:

* The webhook EventSource pod is running.
* A ClusterIP Service (service/webhook-eventsource-svc) exposes port 13000.

Additional useful commands:

* Inspect the EventSource resource:
  ```bash theme={null}
  kubectl -n argo-events get eventsources webhook -o yaml
  ```

* View cluster events:
  ```bash theme={null}
  kubectl -n argo-events get events
  ```

## Test the webhook locally (port-forward)

If you don't have a LoadBalancer or Ingress, port-forward to the Service/pod and test with curl:

1. Port-forward the Service (or pod) to localhost:
   ```bash theme={null}
   kubectl -n argo-events port-forward svc/webhook-eventsource-svc 13000:13000
   ```

2. In another terminal, POST a test payload:
   ```bash theme={null}
   curl -X POST http://localhost:13000/push \
     -H "Content-Type: application/json" \
     -d '{"message":"hello from curl"}'
   ```

3. Check the EventSource logs to see the incoming request being wrapped into a CloudEvents-style envelope:
   ```bash theme={null}
   kubectl -n argo-events logs -l app=webhook-eventsource
   ```

Replace the label selector with the exact Pod/Deployment name if needed.

## How the flow works

* External systems POST to http\://\<cluster-ip-or-loadbalancer>:13000/push (or your public ingress URL).
* The EventSource receives the request, wraps it into a CloudEvents-like envelope (context + data), and forwards the event onto the configured EventBus.
* Sensors in Argo Events consume these events and trigger Argo Workflows, notifications, or other actions.

In the Argo UI (Event Flow or Event Sources view) you should see the new "my-webhook" event source after creation.

## Quick troubleshooting

| Symptom                               | Check                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------- |
| No Service on expected port           | kubectl -n argo-events get svc - check service/webhook-eventsource-svc ports |
| POST returns 404                      | Confirm endpoint path (endpoint: /push) and HTTP method allowed              |
| Events not triggering Sensors         | Check EventBus health and Sensor configurations in the same namespace        |
| External webhooks can't reach cluster | Verify Ingress/LoadBalancer, firewall rules, and DNS routing                 |

> **warning** If you expose a webhook endpoint to the public internet, secure it: use TLS, require authentication or tokens, validate payloads, and restrict source IPs where possible. An unprotected webhook can be abused or flood your cluster with requests.

## Links and references

* [Argo Events Documentation](https://argoproj.github.io/argo-events/)
* [Argo Workflows UI](https://argoproj.github.io/argo-workflows/)
* [CloudEvents Specification](https://cloudevents.io)
* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/about-webhooks)

Use this pattern as a base to extend the webhook EventSource with authentication, custom converters, static payloads, or multiple endpoints per EventSource.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/976edf39-9b73-4480-9dcd-4c97e4ea3890)
