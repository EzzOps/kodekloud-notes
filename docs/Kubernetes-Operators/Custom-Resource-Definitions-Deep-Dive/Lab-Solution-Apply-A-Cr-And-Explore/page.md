# Lab Solution Apply A Cr And Explore

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Lab-Solution-Apply-A-Cr-And-Explore/page

Guide showing how to apply and inspect a Widget custom resource in Kubernetes using kubectl to view table, YAML, jsonpath, describe, and explain

This lesson is short and focused: applying a Custom Resource (CR) is the simpler half of the operator pattern, but it’s useful to understand how the API server exposes and validates CRs and how to inspect them with `kubectl`. Below I walk through the typical steps to apply a Widget CR and explore it using various `kubectl` commands.

## Setup

* The lab platform pre-applied the Widget Custom Resource Definition (CRD) from the previous lesson and provided a starter YAML file in your lab folder.
* The CRD enforces:
  * a `color` pattern (six-digit hex),
  * a `size` enum,
  * and exposes additional printer columns and a short name for convenience.
* The starter YAML includes a placeholder color of `"#000000"` — replace that with any valid 6-digit hex color (keep the quotes so YAML treats `#` as a literal, not a comment).

Open the starter file in your editor and update the color value. Example starter resource (edit the color as needed):

```yaml theme={null}
apiVersion: training.kodekloud.com/v1
kind: Widget
metadata:
  name: my-widget
  namespace: widget-demo
spec:
  size: medium
  # Replace the color below with any valid 6-digit hex color (keep the quotes).
  color: "#4287f5"
  replicas: 3
```

<Callout icon="lightbulb">
  Always quote a hex color in YAML (for example: `"#4287f5"`). Without quotes, `#` begins a comment and the value will be parsed incorrectly.
</Callout>

Apply the CR:

```bash theme={null}
kubectl apply -f ~/labs/widget-explore.yaml
```

Expected apply output:

```bash theme={null}
widget.training.kodekloud.com/my-widget created
```

That confirmation indicates the CRD schema validated your fields (the color matched the pattern and `size: medium` is in the enum).

## Five ways to view the same Widget

Below are common ways to inspect a CR with `kubectl`. Each method serves different uses: quick overviews, scripting, full object inspection, or troubleshooting.

| Method                          | Command                                                                           | Purpose / Example output                                                                                         |
| ------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Table view with printer columns | `kubectl -n widget-demo get widgets`                                              | Quick, human-readable table. Example: <br />`NAME        SIZE   COLOR` <br />`my-widget   medium #4287f5`        |
| Short name                      | `kubectl -n widget-demo get wg`                                                   | Uses the CRD short name (`wg`) for fewer keystrokes. Output is the same table as above.                          |
| Full object (YAML)              | `kubectl -n widget-demo get widget my-widget -o yaml`                             | Inspect the complete resource including metadata populated by the API server.                                    |
| jsonpath (single field)         | `kubectl -n widget-demo get widget my-widget -o jsonpath='{.spec.color}' && echo` | Machine-friendly single-field extraction; good for scripts. Example output: `#4287f5`                            |
| describe                        | `kubectl -n widget-demo describe widget my-widget`                                | Human-readable breakdown with an Events section for troubleshooting. Useful when a controller later adds events. |

### 1) kubectl get (table view with additional printer columns)

The CRD added Additional Printer Columns for `size` and `color`, so `kubectl get` shows those fields directly:

```bash theme={null}
kubectl -n widget-demo get widgets
```

Example output:

```text theme={null}
NAME        SIZE   COLOR
my-widget   medium #4287f5
```

These columns make custom resources feel like first-class Kubernetes types by surfacing key fields without inspecting the full YAML.

### 2) Short name (fewer keystrokes)

The CRD defined a short name `wg`, so you can use it instead of the full plural:

```bash theme={null}
kubectl -n widget-demo get wg
```

Output (identical to the previous):

```text theme={null}
NAME        SIZE   COLOR
my-widget   medium #4287f5
```

Short names are configured in the CRD's `spec.names.shortNames` and are convenient for interactive work and scripts.

### 3) Full object (YAML)

To inspect the full object, including server-populated metadata:

```bash theme={null}
kubectl -n widget-demo get widget my-widget -o yaml
```

Example (abridged to relevant parts):

```yaml theme={null}
apiVersion: training.kodekloud.com/v1
kind: Widget
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"training.kodekloud.com/v1","kind":"Widget","metadata":{"annotations":{},"name":"my-widget","namespace":"widget-demo"},"spec":{"color":"#4287f5","replicas":3,"size":"medium"}}
  creationTimestamp: "2026-05-27T14:03:21Z"
  generation: 1
  name: my-widget
  namespace: widget-demo
  resourceVersion: "241462"
  uid: bde801f3-ff1b-4a54-9e80-cde78f04676e
spec:
  color: '#4287f5'
  replicas: 3
  size: medium
```

Note the API server populated standard metadata fields (creationTimestamp, uid, resourceVersion, generation). Because this lab is CR-only (no controller installed), there is no `status` block yet — that will appear when a controller reconciles the CR and updates status.

### 4) jsonpath (machine-friendly single-field extraction)

For scripts or one-liners, jsonpath extracts a single field cleanly. Example — get only the `color`:

```bash theme={null}
kubectl -n widget-demo get widget my-widget -o jsonpath='{.spec.color}' && echo
```

Output:

```text theme={null}
#4287f5
```

This pattern is useful in shell scripts where you need a single value with no extra parsing.

### 5) describe (human-readable breakdown and events)

`kubectl describe` provides a friendly field-by-field summary and an Events section at the bottom:

```bash theme={null}
kubectl -n widget-demo describe widget my-widget
```

Example output (abridged):

```text theme={null}
Name:         my-widget
Namespace:    widget-demo
Labels:       <none>
Annotations:  <none>
API Version:  training.kodekloud.com/v1
Kind:         Widget
Metadata:
  Creation Timestamp:  2026-05-27T14:03:21Z
  Generation:          1
  Resource Version:    241462
  UID:                 bde801f3-ff1b-4a54-9e80-cde78f04676e
Spec:
  Color:      #4287f5
  Replicas:   3
  Size:       medium
Events:      <none>
```

When you later implement the controller that reconciles Widget resources, events from each reconcile or error will appear here — making `describe` the first place to look when something goes wrong.

## Extra: kubectl explain (auto-generated documentation)

`kubectl explain` reads the CRD's OpenAPI v3 schema and displays field descriptions you included in the CRD. This effectively becomes auto-generated documentation for your CR API.

Examples:

```bash theme={null}
kubectl explain widget.spec
kubectl explain widget.spec.color
```

Sample output for `widget.spec.color`:

```text theme={null}
GROUP: training.kodekloud.com
KIND: Widget
VERSION: v1
FIELD: color <string>
DESCRIPTION:
<empty>
```

If you add `description` fields to your CRD schema, they will appear here. Including descriptions in the CRD is valuable because `kubectl explain` surfaces them to users and scripts.

<Callout icon="warning">
  This lab contains only the CRD and CR (no controller). The API server validates and stores the object, but no controller will reconcile it or populate `status` until you implement one.
</Callout>

## Wrap-up

This walkthrough demonstrates the consumer side of the operator pattern:

* The CRD defines the shape, validation, and documentation for the resource.
* The API server treats custom resources like built-ins (populating metadata and enforcing schema).
* `kubectl` provides familiar tooling (get with printer columns, short names, describe, jsonpath, explain) to interact with CRs.

Next step: implement a controller that watches and reconciles Widget resources to observe status updates and events.

## Links and References

* [Kubernetes Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
* [Writing Kubernetes controllers](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-resources)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/dddf34b6-b714-4e34-a87a-2003f05cc735" />
</CardGroup>
