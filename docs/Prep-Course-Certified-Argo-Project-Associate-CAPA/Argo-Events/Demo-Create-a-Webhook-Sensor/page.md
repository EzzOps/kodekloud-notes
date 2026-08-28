# Demo Create a Webhook Sensor

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Demo-Create-a-Webhook-Sensor/page

Guide to creating an Argo Events webhook Sensor that triggers Argo Workflows or Kubernetes objects and explains RBAC service account setup and troubleshooting

In this lesson you'll create an Argo Events Sensor that listens to a webhook EventSource and triggers an Argo Workflow. Sensors can trigger many target resources — for example Argo Workflows, AWS Lambda, HTTP endpoints, or generic Kubernetes objects. If a built-in trigger doesn't meet your needs, Argo Events provides extension points to implement a custom trigger.

<Frame>
  <img alt="Screenshot of the Argo Events documentation page showing the &#x22;Architecture&#x22; section. It includes a central diagram of Event Source, Event Bus, and Sensor components with their controllers, and a left-hand navigation menu listing triggers (e.g., HTTP Trigger)." />
</Frame>

High-level flow: the EventSource receives an incoming webhook request, publishes an event to the EventBus, and a Sensor subscribed to that EventBus evaluates dependencies and, when satisfied, executes the configured trigger(s). Below is the "trigger a workflow" diagram for reference.

<Frame>
  <img alt="A screenshot of the &#x22;Argo Workflow Trigger&#x22; documentation page showing a left sidebar of user guide topics and a central diagram of various event sources sending events to an Argo Workflows trigger. The page header is green and the visible content includes a &#x22;Trigger a workflow&#x22; section." />
</Frame>

## Sensor concepts: dependencies and triggers

* A Sensor lists one or more dependencies. Each dependency references an EventSource by name and a named event defined in that EventSource (the event name).
* When a dependency is satisfied (an event is published), the Sensor evaluates any dependency expressions (if configured) and then executes the configured trigger(s).

Example dependency referencing the EventSource named `webhook` and the event `my-webhook`:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook-sensor
  namespace: argo-events
spec:
  dependencies:
    - name: my-webhook-dep
      eventSourceName: webhook
      eventName: my-webhook
  triggers:
    # triggers are defined below
```

<Callout icon="lightbulb">
  EventSource names and event names are defined in your EventSource manifest. Use `eventSourceName` to reference the EventSource metadata.name and `eventName` to reference the specific event key under `spec`.
</Callout>

How to find the eventSourceName and eventName

* The EventSource resource contains the top-level name (EventSource metadata.name) and under its `spec` you will see one or more events (each with its own name). Example (abridged):

```yaml theme={null}
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
      endpoint: /push
      method: POST
      port: "13000"
```

* In the Sensor dependency above, use `eventSourceName: webhook` and `eventName: my-webhook`. The Sensor will only react when that specific event is emitted.

## Triggering an Argo Workflow from a Sensor

Below is a Sensor trigger configured to submit an Argo Workflow when the dependency matches. The trigger uses the `argoWorkflow` trigger type and embeds the Workflow manifest as the `resource`.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook-sensor
  namespace: argo-events
spec:
  dependencies:
    - name: my-webhook-dep
      eventSourceName: webhook
      eventName: my-webhook
  triggers:
    - template:
        name: hello-workflow-trigger
        argoWorkflow:
          operation: submit
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
                      command: [cowsay]
                      args: ["Hello Kode Kloud from ArgoEvents!!"]
```

You can create the Sensor either by pasting the YAML into the Argo Events UI or by applying it with kubectl.

## Prepare to send an event to the webhook EventSource

1. Confirm the EventSource service exists in the `argo-events` namespace and get its service name and port.
2. Port-forward the EventSource service to localhost so you can POST to it.

Example commands:

```bash theme={null}
