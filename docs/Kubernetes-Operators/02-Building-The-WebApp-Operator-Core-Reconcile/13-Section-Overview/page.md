# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Section-Overview/page

Building a Kubernetes operator reconcile loop that turns a WebApp custom resource into a Deployment, Service, and ConfigMap, with Kubebuilder workflow and development commands.

When you apply a WebApp custom resource to a Kubernetes cluster, the API server will persist that object—but by itself it does not create pods, Deployments, Services, or ConfigMaps.

```yaml theme={null}
apiVersion: apps.example.com/v1
kind: WebApp
metadata:
  name: my-webapp
spec:
  image: nginx:1.25
  replicas: 3
  port: 80
```

A custom resource is a declarative record: it states your intent. A controller is the program that reads that record and turns it into real Kubernetes objects. This section closes the gap between the stored intent and the actual resources that run in the cluster.

If you used [Kubebuilder](https://book.kubebuilder.io/) to scaffold your project, the scaffold will include a watches-like registration which tells the manager which kinds to reconcile. For example:

```text theme={null}
kind: WebApp
watches: kind WebApp
```

From this point, the scaffold begins doing the operator work: one WebApp object will translate into three concrete child resources:

* a Deployment to run pods
* a ClusterIP Service to provide stable networking on port 80
* a ConfigMap to hold a simple default welcome page

The WebApp spec includes two primary fields: `image` and `replicas`. `image` determines the container image the Deployment runs. `replicas` determines how many pods the Deployment maintains. With those sensible defaults in place, the reconcile loop can focus on its core job: read the WebApp spec, construct the desired child objects, create any missing children, and attach ownerReferences so Kubernetes garbage-collects them when the WebApp is deleted.

<Frame>
  <img alt="The image contains two labeled sections: one for a Kubernetes Service with type &#x22;ClusterIP&#x22; and port &#x22;80,&#x22; and another for a ConfigMap with the description &#x22;A simple default&#x22; and &#x22;Welcome page.&#x22;" />
</Frame>

Think of this as the first working iteration of the operator, not the final product. The essential reconciliation path is:

1. Fetch the WebApp custom resource.
2. Build the desired child objects (Deployment, Service, ConfigMap).
3. Create any children that are missing or update those that drift from the desired state.
4. Attach ownerReferences so the WebApp remains the single source of truth and Kubernetes handles cleanup.

To iterate on the operator locally you will use a few common Go and make targets. Each command touches a different part of the operator toolchain:

| Command                | Purpose                                                  | Example output or effect                   |
| ---------------------- | -------------------------------------------------------- | ------------------------------------------ |
| `make generate`        | Regenerate helper code (deepcopy, clientsets, informers) | Updates generated Go files                 |
| `make manifests`       | Convert controller markers into CRD YAML                 | Produces CRD in `config/crd`               |
| `go build ./...`       | Compile the manager and validate imports                 | Ensures code compiles                      |
| `go run ./cmd/main.go` | Run the controller manager locally                       | Starts reconciliation against your cluster |

> **lightbulb** Run these commands in sequence while developing and testing your operator:

  ```bash theme={null}
  $ make generate
  $ make manifests
  $ go build ./...
  $ go run ./cmd/main.go
  ```

  Each command validates a different layer of the operator: code generation, CRD manifest creation, compilation, and runtime behavior.

As you expand the operator, you can add status fields, events, richer spec fields, validation, webhooks, finalizers, metrics, and packaging. These are natural extensions that increase robustness and observability, but they are not required to get the basic reconcile loop working.

<Frame>
  <img alt="The image is a diagram titled &#x22;Room to Grow – Later&#x22; showing the central concept &#x22;WebApp Operator&#x22; with related features like Events, Validation, Finalizers, Status, Richer fields, and Webhooks." />
</Frame>

For now, keep the scope small and concrete: apply a single WebApp, and the operator will create a Deployment, a Service, and a ConfigMap that are owned by that WebApp. The reconcile loop you design will be responsible for making that mapping reliable and observable.

Links and References

* [Kubebuilder Book](https://book.kubebuilder.io/)
* [Go Documentation](https://go.dev/doc/)
* [Kubernetes Concepts: Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/e63eb55f-382e-4f05-a748-edcddbf19a55)
