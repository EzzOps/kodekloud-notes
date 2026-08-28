# photo-crd.yaml (v1alpha1) - simplified to illustrate missing constraints
spec:
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            quality:
              type: string
```

Too often teams treat CRD registration as a one-line step:

```bash theme={null}
$ kubectl apply -f crd.yaml
```

but a CRD is more than a registration; it's an API contract. The Kubernetes API server enforces this contract like a strict clerk validating filled forms: the CRD is the blank template and the Custom Resource (CR) is the completed form. If the template (CRD) is sloppy, every controller and user interacting with your API inherits those design problems.

You will start with the fundamentals: what a Custom Resource is at the API server level, and the difference between the resource (CR) and its definition (CRD).

<Frame>
  <img alt="The image depicts a concept where a Custom Resource Definition (CRD) is a first-class API object in Kubernetes, alongside Pods and Deployments, and shows &#x22;Sloppy CRD&#x22; being inherited by a &#x22;Sloppy controller.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Treat a CRD as a stable API contract, not a temporary convenience. Design the schema intentionally: names, required fields, allowed values, and update strategy matter.
</Callout>

## Reproducing the problem

* Dev cluster: permissive CRD allowed the invalid object.
* Staging cluster: CRD is stricter (or the same stricter server-side checks), so the same object is rejected.
* Result: you must perform a CRD version bump, migrate objects, and explain a breaking change to stakeholders.

<Callout icon="warning">
  Versioning a CRD and migrating existing resources can be a breaking change. Plan migration strategies (conversion webhooks, storage versioning) before changing schemas in production.
</Callout>

## Why permissive schemas fail

Permissive OpenAPI schemas let invalid or malformed objects be stored somewhere; when another cluster has more accurate validations (or the API server enforces additional checks such as CEL validations), those same objects will be blocked. The root cause is treating the CRD as an afterthought rather than as the authoritative API contract.

## Designing a robust CRD

When authoring a CRD, explicitly design:

* Structural schema: use `type: object` and `properties` to make the shape explicit.
* Required fields: prevent runtime panics and make controllers simpler.
* Defaults: populate sane defaults so clients don't need to supply every field.
* Enums and format checks: restrict values to known-good options.
* CEL validations: express rules OpenAPI cannot, enforced at admission time.
* Operational subresources and UX enhancements (status, scale, printer columns, shortNames).

Example structural schema with validations:

```yaml theme={null}
openAPIV3Schema:
  type: object                    # structural schema
  required:
    - size                        # required fields
  properties:
    size:
      type: string
      default: "1Gi"              # default
    quality:
      type: string
      enum:
        - "low"                   # enum
        - "high"
  x-kubernetes-validations:
    - rule: "self.size != ''"     # CEL
```

CEL (Common Expression Language) is evaluated by the API server at admission time and allows rules that OpenAPI cannot express (for example, cross-field validation or regex-like checks). Use CEL to catch invalid combinations early.

## Operational extras — improve usability

Small CRD additions greatly improve day-to-day usability for users and operators. The following table summarizes commonly-used operational settings and why they matter:

| Feature              | Benefit                                                  | Notes / Example                                               |
| -------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| `status` subresource | Allows controller to update status independently of spec | Avoids update conflicts between users and controllers         |
| `scale` subresource  | Enables `kubectl scale` and HPA integration              | Map `.spec.replicas` and `.status.replicas` appropriately     |
| Printer columns      | `kubectl get` shows useful columns                       | Example: add `quality` and `age` columns for quick visibility |
| `shortNames`         | Saves typing for users                                   | Example: `shortNames: ["ph"]` to allow `kubectl get ph`       |
| Defaults & enums     | Prevents invalid inputs and reduces client burden        | Defaults reduce required input, enums restrict values         |

Examples of expected operational interactions:

```bash theme={null}
# examples of operational expectations
kubectl scale photo vacation-2024 --replicas=3
kubectl get photo vacation-2024 -o wide  # shows printer columns
```

## Practical next steps in this lesson

* Manually author a CRD (no KubeBuilder scaffolding) to expose the fields you need, the `versions` block, and the OpenAPI v3 schema.
* Add required fields, defaults, enums, and CEL validations to ensure the API rejects bad input at apply time.
* Add `status` and `scale` subresources and printer columns for operational ergonomics.
* Learn version bumping and migration patterns so schema evolution is safe in production.

By the end of this article you will be able to read any CRD and judge whether it was designed well, and you will know how to improve or evolve it safely.

## Links and references

* [KubeBuilder Book](https://book.kubebuilder.io/)
* [Kubernetes CEL validation docs](https://kubernetes.io/docs/reference/using-api/validation/)
* [Kubernetes CustomResourceDefinition API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#customresourcedefinition-v1-apiextensions-k8s-io)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/9e1bfa29-8568-4c48-a821-9b0c05d3fc24" />
</CardGroup>


# Demo Add A Finalizer To WebApp

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Finalizers-And-Cleanup/Demo-Add-A-Finalizer-To-WebApp/page

Explains adding and using a Kubernetes finalizer in a WebApp operator controller to ensure cleanup before resource deletion, demonstrating reconcile patterns and controllerutil helper usage.

By default the WebApp delete flow in this operator relies solely on [owner references](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/). That works for in-cluster resources like Deployments, Services, and ConfigMaps because the [Kubernetes garbage collector](https://kubernetes.io/docs/concepts/architecture/garbage-collection/) will remove dependent objects automatically when their owner is deleted.

However, some cleanup tasks cannot be inferred by Kubernetes — for example, cleaning up external cloud resources, revoking credentials, or performing any operator-specific final work. For those cases you need a [finalizer](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) on the custom resource so the controller can run cleanup before the API server actually deletes the object.

The problem with the current behavior (before adding a finalizer) is demonstrated here: creating the WebApp and immediately deleting it completes quickly because nothing blocks the deletion.

```bash theme={null}
$ kubectl apply -f ../webapp-site.yaml
namespace/webapp-demo created
webapp.webapp.kodekloud.com/site created

$ kubectl -n webapp-demo delete webapp site
webapp.webapp.kodekloud.com "site" deleted from webapp-demo namespace
```

That fast disappearance prevents the controller from performing any needed cleanup. The solution is to add a finalizer string owned by the operator and implement the standard finalizer pattern in the controller's Reconcile logic.

<Callout icon="lightbulb">
  [controller-runtime helpers](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil) simplify adding, checking, and removing finalizers: each controller should only add and remove its own finalizer string. Using these helpers avoids manual metadata slice manipulation.
</Callout>

## Finalizer name and placement

Use a unique, domain-style finalizer string and declare it as a package-level constant so the controller uses a single canonical value everywhere.

```go theme={null}
import (
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

	webappv1 "github.com/kodekloud/webapp-operator/api/v1"
)

const webAppFinalizer = "webapp.kodekloud.com/finalizer"
```

For reference, the controller struct looks like:

```go theme={null}
type WebAppReconciler struct {
	client.Client
	Scheme   *runtime.Scheme
	Recorder record.EventRecorder
}
```

## The finalizer pattern in Reconcile

A well-structured Reconcile should clearly separate two paths:

1. Normal (non-deleting) path — ensure the finalizer is present.
2. Deletion path — perform cleanup and remove the finalizer so Kubernetes can finish deletion.

Key points:

* Only add the finalizer when the object is not being deleted (DeletionTimestamp == zero).
* When adding the finalizer, persist the object with `r.Update` and then requeue so the next reconcile will operate on the object with the updated `resourceVersion`.
* When deletion is in progress (DeletionTimestamp non-nil), only perform cleanup if your finalizer is present; then remove it and `Update` so the API server can complete deletion.

### Add finalizer during normal reconciliation

Check the DeletionTimestamp and add the finalizer if missing. Use `controllerutil.ContainsFinalizer` and `controllerutil.AddFinalizer` to avoid unnecessary updates.

```go theme={null}
if webapp.DeletionTimestamp.IsZero() {
    if !controllerutil.ContainsFinalizer(&webapp, webAppFinalizer) {
        controllerutil.AddFinalizer(&webapp, webAppFinalizer)
        if err := r.Update(ctx, &webapp); err != nil {
            return ctrl.Result{}, err
        }
        // Requeue to fetch the object with the updated finalizer/resourceVersion
        return ctrl.Result{Requeue: true}, nil
    }
    // Continue normal reconciliation when finalizer already present
}
```

### Deletion branch — perform cleanup, then remove finalizer

When the Resource's DeletionTimestamp is set the API server has accepted a delete request but is holding the object until all finalizers are removed. Act only if your finalizer is present; perform any required controller-specific cleanup, then remove your finalizer and `Update` the object so Kubernetes can finish deletion.

A full Reconcile example that demonstrates both branches:

```go theme={null}
package controllers

import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

    webappv1 "github.com/kodekloud/webapp-operator/api/v1"
)

const webAppFinalizer = "webapp.kodekloud.com/finalizer"

func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 1) Normal path: object not being deleted -> ensure finalizer exists
    if webapp.DeletionTimestamp.IsZero() {
        if !controllerutil.ContainsFinalizer(&webapp, webAppFinalizer) {
            controllerutil.AddFinalizer(&webapp, webAppFinalizer)
            if err := r.Update(ctx, &webapp); err != nil {
                return ctrl.Result{}, err
            }
            // Requeue so we operate on the updated object next pass
            return ctrl.Result{Requeue: true}, nil
        }
        // Continue with normal reconciliation (omitted here)
    }

    // 2) Deletion path: object is being deleted
    if !webapp.DeletionTimestamp.IsZero() {
        // Only act if our finalizer is present
        if controllerutil.ContainsFinalizer(&webapp, webAppFinalizer) {
            // Example placeholder: build a Deployment object reference or perform other cleanup
            dep := &appsv1.Deployment{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      webapp.Name,
                    Namespace: webapp.Namespace,
                },
            }

            // Perform cleanup here (e.g., delete external resources, revoke cloud resources)
            // In this demo, we'll log and consider cleanup done.
            ctrl.LoggerFrom(ctx).Info("running cleanup for WebApp", "name", webapp.Name)

            // Remove our finalizer and persist the object so Kubernetes can complete deletion
            controllerutil.RemoveFinalizer(&webapp, webAppFinalizer)
            if err := r.Update(ctx, &webapp); err != nil {
                return ctrl.Result{}, err
            }
            // After removing finalizer and successful update, the object will be deleted by the API server.
            return ctrl.Result{}, nil
        }
        // If our finalizer is not present, nothing for us to do; let deletion proceed.
    }

    return ctrl.Result{}, nil
}
```

<Callout icon="warning">
  Do not remove finalizers that you do not own. Always check `ContainsFinalizer` before calling `RemoveFinalizer` to avoid interfering with other controllers’ cleanup. Also return errors from `Update` so controller-runtime will retry on transient failures.
</Callout>

## Verify deletion completed

Once the controller has removed its finalizer and the API server finishes deletion, a subsequent get should return NotFound:

```bash theme={null}
$ kubectl -n webapp-demo get webapp site
Error from server (NotFound): webapps.webapp.kodekloud.com "site" not found
```

A `NotFound` response indicates the delete request completed successfully and the finalizer flow worked: your controller performed cleanup and released its finalizer so Kubernetes could complete deletion.

## Quick summary and checklist

| Step                       | Purpose                                                     | Example / Note                                                              |
| -------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------- |
| Add finalizer              | Ensure controller can run cleanup before deletion           | Use `controllerutil.AddFinalizer` when `DeletionTimestamp.IsZero()`         |
| Persist change & requeue   | Let next reconcile operate on updated resource              | Call `r.Update(ctx, &webapp)` then `return ctrl.Result{Requeue: true}, nil` |
| On delete, check ownership | Only perform cleanup if your finalizer is present           | `controllerutil.ContainsFinalizer(&webapp, webAppFinalizer)`                |
| Perform cleanup            | Delete external resources or perform operator-specific work | Idempotent cleanup is recommended                                           |
| Remove finalizer & update  | Allow API server to finish deletion                         | `controllerutil.RemoveFinalizer` + `r.Update`                               |

## References

* [Kubernetes finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)
* [Owners and dependents (ownerReferences)](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)
* [Kubernetes garbage collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/)
* [controller-runtime controllerutil helpers](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/6a375c4e-4bda-4d13-a58f-4d85961676cc/lesson/a26444ee-e070-4ef7-b784-86238646c77e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/6a375c4e-4bda-4d13-a58f-4d85961676cc/lesson/ba550e4e-3605-4f5a-9e99-715ab68812d8" />
</CardGroup>
