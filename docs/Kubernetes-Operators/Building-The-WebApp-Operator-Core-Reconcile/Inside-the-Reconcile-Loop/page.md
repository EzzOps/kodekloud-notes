# First-version API
WebApp:
  spec:
    image: string
    replicas: int32
```

```yaml theme={null}
# API can grow later
WebApp:
  spec:
    image: string
    replicas: int32
    port: int32
```

The user writes a minimal desired state and the controller creates the child objects that make that state real.

<Frame>
  <img alt="The image illustrates a flowchart of a reconciliation process, where a user writes a small desired state, a controller creates children, and child objects make the state real." />
</Frame>

In Go, express this `spec` as fields on the `WebAppSpec` struct. The JSON struct tags determine the YAML/JSON field names users write in their manifests:

```go theme={null}
type WebAppSpec struct {
    Image    string `json:"image"`
    Replicas int32  `json:"replicas"`
}
```

Kubebuilder markers (Go comments processed by `controller-gen`) can add API-server behavior such as defaults and validation. Running `make manifests` converts those markers into the CRD OpenAPI schema that the API server enforces.

<Callout icon="warning">
  Remember to add kubebuilder validation and default markers if you expect defaults or input validation. Without them, the API server won't enforce constraints and invalid manifests could reach your controller.
</Callout>

Summary table — WebApp first-version contract:

| Field      | Type          | Meaning                                         | Default (controller-owned) |
| ---------- | ------------- | ----------------------------------------------- | -------------------------- |
| `image`    | `string`      | Container image to run in the Deployment        | n/a (required)             |
| `replicas` | `int32`       | Number of Pod replicas to maintain              | n/a (user-provided)        |
| Service    | (not in spec) | Operator creates a `ClusterIP` Service          | `ClusterIP` on port `80`   |
| ConfigMap  | (not in spec) | Operator creates a ConfigMap for a welcome page | Static welcome HTML        |

Next step: translate this design into controller and reconcile logic that instantiates the Deployment, Service, and ConfigMap. Implement the reconcile loop to:

1. Read the `WebApp` instance and its `spec`.
2. Construct desired child resources (Deployment, Service, ConfigMap) using the `spec` values and operator defaults.
3. Create or update child resources, set owner references, and ensure labels/selector consistency.
4. Requeue and reconcile until observed state matches desired state.

References:

* [Kubernetes Operators — Concepts](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
* [kubebuilder book](https://book.kubebuilder.io/)
* [controller-gen (kubebuilder marker docs)](https://book.kubebuilder.io/reference/markers.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/806a4312-3ca5-4ce7-aa47-7336e21a1324" />
</CardGroup>


# Inside the Reconcile Loop

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Inside-the-Reconcile-Loop/page

Explains the Kubernetes controller reconcile loop, level triggered reconciliation, idempotent design, fetching and handling deletions, requeue semantics, and managing desired versus actual child resources

Think of a thermostat on the wall.

You set it to seventy degrees — that's the desired state. The thermostat reads the room temperature — that's the actual state. If the two don't match, the thermostat turns the heat on or off, then checks again and again, forever.

<Frame>
  <img alt="The image illustrates a thermostat process on the wall, showing a desired state of 70 degrees, an actual state of 68 degrees, and an action to turn the heat on." />
</Frame>

Reconcile is exactly that loop applied to Kubernetes objects.

Your WebApp's spec is the set point; the cluster's actual state — the Deployment, Service, ConfigMap, Pods, and so on — is the room temperature. The controller closes that gap on every event, every resync, and every restart.

<Frame>
  <img alt="The image illustrates the Kubernetes control loop, showing the relationship between the Desired State, Controller, and Actual State." />
</Frame>

Reconcile is the heart of every controller you write. When implemented correctly, the rest of the operator becomes straightforward; when it's wrong, you'll be struggling with unpredictable behavior.

Here is the Reconcile signature provided by controller-runtime — it has two inputs and two outputs:

```go theme={null}
func (r *WebAppReconciler) Reconcile(
	ctx context.Context,
	req ctrl.Request,
) (ctrl.Result, error) {
	// ...
}
```

The `req` contains a `NamespacedName` (the key of the object that needs attention). Notice what it does not contain: neither the object itself nor the event that triggered the call. This is intentional.

Controllers in Kubernetes are level-triggered, not edge-triggered. You do not react to "a WebApp was created"; you react to "the WebApp named `foo` in namespace `bar` might need work — go look." Embracing this mental model is essential.

<Callout icon="lightbulb">
  Controllers are level-triggered: always reconcile to the current desired state by looking up the object by key, not by relying on the event payload.
</Callout>

<Frame>
  <img alt="The image contrasts edge-triggered and level-triggered concepts, suggesting that level-triggered is more important in the lesson." />
</Frame>

Every reconcile starts by answering three questions:

* What's the desired state?
* What's the actual state?
* What's the diff (what needs to change)?

A typical reconcile body follows these four steps:

1. Fetch the parent resource (the WebApp) from the cache using `r.Get` with the request's `NamespacedName`.
2. Compute the desired child objects (Deployment, Service, ConfigMap, etc.) from the WebApp spec.
3. Create or update those child objects so they match the desired state.
4. Update the WebApp's status to reflect the observed (actual) state.

<Frame>
  <img alt="The image outlines three questions for reconciliation: &#x22;Desired? What should exist,&#x22; &#x22;Actual? What does exist,&#x22; and &#x22;Diff? What needs to change.&#x22;" />
</Frame>

The first step — fetching the WebApp safely — is a small, important pattern. Use the API to get the object, and treat a not-found as a normal deletion case:

```go theme={null}
webapp := &webappv1.WebApp{}
if err := r.Get(ctx, req.NamespacedName, webapp); err != nil {
    if apierrors.IsNotFound(err) {
        // The WebApp was deleted. Owned children will be cleaned up by GC via OwnerReferences.
        return ctrl.Result{}, nil
    }
    // Any other error is a real problem (permissions, API server unreachable, etc.)
    return ctrl.Result{}, err
}
```

Notes:

* `webappv1` is the package generated from your CRD group/version.
* `apierrors` is `k8s.io/apimachinery/pkg/api/errors`; use `IsNotFound` to distinguish deletions from transient API errors.
* Owned children created with proper OwnerReferences are garbage-collected automatically. See the Kubernetes docs on OwnerReferences for details.

This fetch-and-bail pattern (under ten lines of Go) is the canonical approach to "fetch the parent and exit safely if it's gone."

The reconcile loop must be idempotent. The same WebApp will be reconciled many times — on creation, on spec changes, on periodic resyncs, after controller restarts, and after transient errors. If running reconcile twice yields a different result than running it once, you have a bug.

<Callout icon="warning">
  Idempotency is critical: ensure reconcile is safe to run repeatedly. Avoid relying on side-effects that make subsequent runs behave differently.
</Callout>

<Frame>
  <img alt="The image illustrates the concept of idempotency in loops, stating &#x22;Run twice == run once&#x22; and mentions the importance of handling creation, spec changes, re-sync, restarts, and errors. It emphasizes that if running twice doesn't equal running once, it's considered a bug." />
</Frame>

Return values from Reconcile control requeue behavior. Use these return patterns to express what should happen next:

| Return value                        | Meaning                                                   | When to use                                     |
| ----------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| `ctrl.Result{}, nil`                | Done for now; wait for the next event.                    | Normal completion — nothing pending.            |
| `ctrl.Result{RequeueAfter: d}, nil` | Requeue this request after duration `d`.                  | Polling/waiting for readiness or a timed retry. |
| `ctrl.Result{}, err`                | Error: triggers controller-runtime's exponential backoff. | Unexpected failures — let the framework retry.  |

Example returns in code:

```go theme={null}
return ctrl.Result{}, nil
return ctrl.Result{RequeueAfter: d}, nil
return ctrl.Result{}, err
```

When `r.Get` returns a not-found error, the resource was deleted. If you created children with `OwnerReference`, Kubernetes will garbage collect them, so you typically return without error:

```go theme={null}
return ctrl.Result{}, nil
```

If you need to perform work during deletion (for example, to clean up external resources), implement finalizers and handle that lifecycle explicitly — this will be covered in the finalizers and cleanup section.

In the next lesson you'll wire up the rest of the loop: computing desired child resources, performing create-or-update operations, and updating status to reflect observed state.

Links and references:

* [Kubernetes Concepts — Desired State and Controllers](https://kubernetes.io/docs/concepts/overview/working-with-objects/handlers-events/)
* [controller-runtime Reconcile docs](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [`k8s.io/apimachinery/pkg/api/errors`](https://pkg.go.dev/k8s.io/apimachinery/pkg/api/errors)
* [OwnerReferences and garbage collection](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/5377c550-a928-4c7d-bf1b-61df639cf1c4" />
</CardGroup>
