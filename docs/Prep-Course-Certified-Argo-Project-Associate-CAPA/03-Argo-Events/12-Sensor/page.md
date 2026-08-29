# Sensor

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/Sensor/page

Explains Argo Events Sensors, how they subscribe to EventBus, evaluate dependencies and conditions, and trigger actions with parameter mappings and example Sensor YAML and usage patterns.

Sensors are the decision-making components in Argo Events. They subscribe to an EventBus (NATS by default), evaluate incoming events against declared dependencies, and execute triggers when the required conditions are met.

This article explains what a Sensor does, details key spec fields, and walks through example Sensor specifications and usage patterns.

## What a Sensor does

* Subscribes to one or more sources on the EventBus.
* Waits until one or more specified events occur (individual or combinations).
* When dependencies and conditions are satisfied, executes one or more triggers (for example, starts a workflow, sends an HTTP request, or creates a Kubernetes resource).

## Sensor spec: key concepts

| Field / Concept | Purpose                                                                | Example                                                               |   |            |
| --------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------- | - | ---------- |
| `eventBusName`  | Which EventBus the Sensor listens to                                   | `default`                                                             |   |            |
| `dependencies`  | The "if" side: event sources + event names the Sensor waits for        | `eventSourceName: webhook`, `eventName: example-webhook`              |   |            |
| `triggers`      | The "then" side: actions to execute when dependency conditions are met | HTTP call, Kubernetes resource creation, workflow start               |   |            |
| `parameters`    | Map event payload fields into trigger templates                        | `src.dependencyName`, `src.dataKey`, `dest: spec.containers.0.args.0` |   |            |
| `conditions`    | Boolean expression controlling when an individual trigger runs         | `"X && Y"`, \`"(X                                                     |   | Y) && Z"\` |

For more background, see [Argo Events Sensors](https://argoproj.github.io/argo-events/sensors/).

## Example: WebhookSensor

Assume a Sensor named `webhook-sensor`. By default it uses the EventBus named `default`; you can override it with `spec.eventBusName`. Think of a Sensor as tuning into a radio channel (the EventBus) and listening for broadcasts (events). The Sensor spec centers around dependencies (the "if" side) and triggers (the "then" side).

### Dependencies

`dependencies` is the "if" part. The Sensor remains idle until the dependencies are satisfied.

Each dependency includes:

* `name`: a local identifier used to reference this event later in `parameters` or `conditions`.
* `eventSourceName`: the configured event source (for example, `webhook`).
* `eventName`: the specific event produced by the event source (for example, `example-webhook`).

### Triggers

`triggers` define the actions executed after dependencies/conditions are satisfied. Triggers support multiple adapters (HTTP, Kubernetes, Argo Workflows, etc.). In the example below the trigger creates a Kubernetes Pod via the Kubernetes API (`k8s.operation: create`) using an inline resource template.

### Parameters: mapping event data into trigger templates

`parameters` let you inject values from incoming events into trigger resource templates.

* `src` describes where to read data from: `dependencyName` and `dataKey` (a path inside the event payload, e.g., `body.message`).
* `dest` is the YAML/JSON path in the target template where the value will be injected; use numeric indices for arrays (for example, `spec.containers.0.args.0`).

> **lightbulb** When specifying destination paths for parameters, use numeric indices for array positions (for example, `.containers.0.args.0`). The textual description like "firstIndex" is conceptual — the actual path must use numbers.

### Sensor YAML example (creates a Pod that echoes a message from the event)

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook-sensor
  namespace: argo-events
spec:
  eventBusName: default
  dependencies:
  - name: test-dep
    eventSourceName: webhook
    eventName: example-webhook
  triggers:
  - template:
      name: webhook-sensor-pod-trigger
      k8s:
        operation: create
        source:
          resource:
            apiVersion: v1
            kind: Pod
            metadata:
              generateName: webhook-sensor-po-
              namespace: argo-events
            spec:
              containers:
              - name: webhook-sensor-container
                command:
                - echo
                args:
                - "webhook-sensor >>>> Default Message"
                image: busybox
      parameters:
      - src:
          dependencyName: test-dep
          dataKey: body.message
        dest: spec.containers.0.args.0
```

### Triggering the Sensor with an example POST

Use an HTTP POST to the webhook event source (adjust the URL/port to match your environment):

```bash theme={null}
curl --location 'http://localhost:12000/example' \
  --header 'Content-Type: application/json' \
  --data '{"message":"Message from the Payload"}'
```

After the Sensor creates the Pod, the container spec will show the injected argument:

```yaml theme={null}
containers:
- name: webhook-sensor-container
  args:
  - "Message from the Payload"
  command:
  - echo
  image: busybox
```

This demonstrates how event payload fields can be mapped into the resource template created by the Sensor.

## Trigger conditions (combining dependencies)

* A Sensor can declare multiple dependencies. By default (when `conditions` is omitted) all dependencies are required (logical AND).
* Use `conditions` on individual trigger templates to control when each trigger runs. Conditions support boolean expressions with `&&`, `||`, and parentheses.
* Reference dependencies by their `name` in the boolean expression.

### Example: multiple dependencies with condition-based triggers

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: example
spec:
  dependencies:
  - name: X
    eventSourceName: webhook-gateway
    eventName: payment-webhook
  - name: Y
    eventSourceName: webhook-gateway
    eventName: order-webhook
  - name: Z
    eventSourceName: warehouse-service
    eventName: stock-webhook
  triggers:
  - template:
      conditions: "X"  # trigger runs when dependency X has occurred
      name: process-payment
      http:
        url: http://api.svc.com/process-payment
        method: GET
  - template:
      conditions: "Y"
      name: process-order
      http:
        url: http://api.svc.com/process-order
        method: GET
  - template:
      conditions: "X && Y"
      name: reconcile-payment-order
      http:
        url: http://api.svc.com/reconcile
        method: POST
  - template:
      conditions: "X || Y"
      name: either-event
      http:
        url: http://api.svc.com/handle-either
        method: POST
  - template:
      conditions: "(X || Y) && Z"
      name: complex-condition
      http:
        url: http://api.svc.com/complex
        method: POST
```

Common condition patterns:

* `"X"` — trigger runs when X occurs
* `"Y"` — trigger runs when Y occurs
* `"X && Y"` — both X and Y must have occurred
* `"X || Y"` — either X or Y
* `"(X || Y) && Z"` — Z plus either X or Y

> **warning** If you omit `conditions`, the Sensor treats all listed dependencies as required (logical AND). Ensure you use straight quotes (") in YAML strings — avoid curly quotes.

## Summary

* Sensors listen to an EventBus, evaluate dependencies, and execute triggers when conditions are met.
* Use `parameters` to map event payload fields into trigger templates (remember numeric indices for arrays).
* Use `conditions` for flexible boolean logic across multiple dependencies to control individual triggers.

## Links and references

* [Argo Events — Sensors](https://argoproj.github.io/argo-events/sensors/)
* [Argo Events — EventSources](https://argoproj.github.io/argo-events/event-sources/)
* [Kubernetes Pods — Official Docs](https://kubernetes.io/docs/concepts/workloads/pods/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/e59f39b6-db40-43cc-bde2-5ce31557585b)
