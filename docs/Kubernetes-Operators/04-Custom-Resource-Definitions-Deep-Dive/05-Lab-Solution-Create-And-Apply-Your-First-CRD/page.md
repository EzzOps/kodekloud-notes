# Lab Solution Create And Apply Your First CRD

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Lab-Solution-Create-And-Apply-Your-First-CRD/page

Guide to creating and applying a Kubernetes CRD with OpenAPI v3 schema for a Widget kind, demonstrating server side validation using valid and invalid custom resources

This lesson walks through creating a Kubernetes CustomResourceDefinition (CRD) for a Widget kind, applying it to a cluster, and validating the schema by creating both a valid and an invalid Widget. You will learn how to:

* Define a CRD with an OpenAPI v3 schema for server-side validation.
* Apply the CRD and wait until it is established.
* Create a namespace and a sample custom resource (CR).
* Observe schema validation rejecting invalid CRs.

Relevant links:

* [Kubernetes Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [OpenAPI v3 schema for CRD validation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation)

## 1) Edit the CRD

Open `widget-crd.yaml` (for example, in VS Code) and add a `shortName` and an OpenAPI v3 `schema` under the version you serve. The example below demonstrates:

* `shortNames: [wj]` so `kubectl get wj` works.
* `spec` schema requiring `size` and `color`.
* `size` constrained by an enum: `small`, `medium`, `large`.
* `replicas` with `minimum`, `maximum`, and a `default`.

Save the file after making these changes.

```yaml theme={null}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: widgets.training.example.com
spec:
  group: training.example.com
  scope: Namespaced
  names:
    plural: widgets
    singular: widget
    kind: Widget
    shortNames: [wj]
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          required: ["spec"]
          properties:
            spec:
              type: object
              required: ["size", "color"]
              properties:
                size:
                  type: string
                  enum: ["small", "medium", "large"]
                color:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
                  default: 1
```

<Callout icon="lightbulb">
  Using `shortNames` (for example `wj`) makes commands like `kubectl get wj` possible and more convenient.
</Callout>

## 2) Apply the CRD and wait until it is established

Apply the CRD to the cluster and wait until the API server marks it as `Established`. This ensures the new resource kind is served by the API.

```bash theme={null}
$ kubectl apply -f ~/labs/widget-crd.yaml
customresourcedefinition.apiextensions.k8s.io/widgets.training.example.com created
```

Wait for the CRD to become Established:

```bash theme={null}
$ kubectl wait --for=condition=Established crd/widgets.training.example.com --timeout=60s
customresourcedefinition.apiextensions.k8s.io/widgets.training.example.com condition met
```

Verification commands:

* `kubectl get crd widgets.training.example.com -o yaml`
* `kubectl api-resources | grep widget`

## 3) Create a namespace for the demo

Create a dedicated namespace to isolate demo resources:

```bash theme={null}
$ kubectl create namespace widget-demo
namespace/widget-demo created
```

## 4) Create a sample Widget (valid CR)

Create `widget-sample.yaml` with valid values that conform to the CRD schema:

```yaml theme={null}
apiVersion: training.example.com/v1
kind: Widget
metadata:
  name: blue-widget
  namespace: widget-demo
spec:
  size: medium
  color: blue
  replicas: 3
```

Apply the CR and list it using the short name:

```bash theme={null}
$ kubectl apply -f widget-sample.yaml
widget.training.example.com/blue-widget created

$ kubectl -n widget-demo get wj
NAME          AGE
blue-widget   10s
```

To display stored spec values with JSONPath:

```bash theme={null}
$ kubectl -n widget-demo get widget blue-widget -o jsonpath='{.spec.size} {.spec.color} {.spec.replicas}'
medium blue 3
```

Quick reference: CR fields and purpose

| Field                | Purpose                              | Example                   |
| -------------------- | ------------------------------------ | ------------------------- |
| `apiVersion`         | Identifies the CRD group and version | `training.example.com/v1` |
| `kind`               | Resource kind defined by the CRD     | `Widget`                  |
| `metadata.name`      | Name of the CR                       | `blue-widget`             |
| `metadata.namespace` | Namespace to create the CR in        | `widget-demo`             |
| `spec.size`          | Size constrained by enum             | `medium`                  |
| `spec.color`         | Free-form color string               | `blue`                    |
| `spec.replicas`      | Integer with min/max/default         | `3`                       |

## 5) Apply a deliberately invalid Widget to see validation

To demonstrate server-side schema validation, create `bad-widget.yaml` that violates the `size` enum:

```yaml theme={null}
apiVersion: training.example.com/v1
kind: Widget
metadata:
  name: bad-widget
  namespace: widget-demo
spec:
  size: huge
  color: blue
  replicas: 1
```

Apply it and observe the validation error:

```bash theme={null}
$ kubectl apply -f bad-widget.yaml
Error from server: error when creating "bad-widget.yaml": admission webhook "validation.k8s.io" denied the request: validation failed: spec.size in body should be one of [small medium large]
```

Kubernetes rejects this object because `size: huge` is not one of the allowed enum values defined in the CRD.

<Callout icon="warning">
  If you update your CRD schema after CRs already exist, be careful: removing fields or tightening validation can cause existing objects to fail validation. Prefer adding new fields or using a migration strategy.
</Callout>

## Summary and next steps

* You created a namespaced CRD with an OpenAPI v3 schema and a `shortName` for convenience.
* You applied a valid CR and confirmed it is stored by the API.
* You verified that server-side validation prevents invalid CRs from being created.

Next recommended steps:

* Add additional validation (patterns, `maxLength`, nested object validation) to the CRD schema as needed.
* Implement a controller for the Widget kind to reconcile and act on Widget objects.
* Read more: [Extending the Kubernetes API with CRDs](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/aa3ba4e5-e368-4686-be2b-2d16b5843fd8" />
</CardGroup>
