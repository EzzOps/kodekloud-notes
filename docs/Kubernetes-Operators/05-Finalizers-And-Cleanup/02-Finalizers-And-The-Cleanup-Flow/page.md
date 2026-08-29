# Finalizers And The Cleanup Flow

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Finalizers-And-Cleanup/Finalizers-And-The-Cleanup-Flow/page

Explains Kubernetes finalizers and cleanup flow so controllers reliably perform idempotent external resource cleanup before allowing object deletion, including patterns, pseudocode, and best practices.

Deleting a custom resource should not feel like pulling the power cord — it should feel like closing a ticket. Finalizers give controllers a reliable, visible opportunity to perform cleanup before Kubernetes removes the object from etcd.

Controllers get one last chance to finish the cleanup they own. If a controller only manages in-cluster children with proper ownerReferences, Kubernetes will garbage-collect those children automatically. But when the controller touches resources outside the cluster — external DNS records, cloud resources, or entries in third-party systems — the API server cannot infer how to undo that work. Finalizers solve this gap.

Creating a web app typically tells the controller to create or maintain certain resources. To delete that web app, a user runs:

```bash theme={null}
kubectl delete webapp site
```

The delete request changes the resource lifecycle: the API server sets a `deletionTimestamp` and puts the object into a Terminating state while finalizers remain. Controllers reconcile against that visible terminating object and perform any necessary cleanup before the API server finally removes the object.

<Frame>
  <img alt="The image is a diagram illustrating a Kubernetes concept, where a &#x22;WebApp&#x22; site manages &#x22;Deployment,&#x22; &#x22;Service,&#x22; and &#x22;ConfigMap&#x22; components under a hierarchy, with &#x22;ownerRef&#x22; connections denoting relationships. It emphasizes the lifecycle management aspects of &#x22;create&#x22; and &#x22;delete.&#x22;" />
</Frame>

If the controller must manage external resources, add a finalizer so the API server waits while the controller cleans up those outside resources.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster interacting with external components like DNS records, cloud resources, and other systems, highlighting that the API server cannot automatically manage these interactions." />
</Frame>

A finalizer is just a string in `metadata.finalizers`. For example:

```yaml theme={null}
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: site
  finalizers:
    - webapp.kodekloud.com/finalizer
```

While at least one finalizer remains, the API server keeps the resource visible (Terminating) and sets `deletionTimestamp`. Controllers must reconcile that object and perform cleanup before removing their finalizer.

When finalizers are present, reconcile follows two clear paths:

* Normal path (no `deletionTimestamp`): ensure resources (in-cluster and external) exist and that your controller's finalizer is attached before creating anything that requires cleanup later.
* Cleanup path (`deletionTimestamp` set): stop creating/updating normal children, perform cleanup of owned external resources, and remove only your controller's finalizer when cleanup succeeds.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Two Paths in Reconcile,&#x22; depicting decision paths based on whether &#x22;deletionTimestamp&#x22; is set, leading to a &#x22;normal path&#x22; or &#x22;cleanup path.&#x22; It includes steps to ensure the finalizer and create/update children and external work." />
</Frame>

Example reconcile pseudocode showing the two paths and where to add/remove the finalizer:

```go theme={null}
func Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
  var app webappv1.WebApp
  if err := r.Get(ctx, req.NamespacedName, &app); err != nil {
    return ctrl.Result{}, client.IgnoreNotFound(err)
  }

  // If not terminating: ensure finalizer and normal reconcile
  if app.ObjectMeta.DeletionTimestamp.IsZero() {
    if !hasFinalizer(&app) {
      addFinalizer(&app)
      r.Update(ctx, &app)
    }
    return r.normalReconcile(&app)
  }

  // Terminating: run cleanup, then remove finalizer
  if err := r.cleanupExternalResources(&app); err != nil {
    // Record error and requeue; leave finalizer so deletion is blocked
    return ctrl.Result{RequeueAfter: time.Minute}, err
  }
  removeFinalizer(&app)
  r.Update(ctx, &app)
  return ctrl.Result{}, nil
}
```

When implementing this pattern, follow these guidelines:

* Add your finalizer before creating external resources — don’t create external state without protecting deletion.
* Only remove your controller's finalizer once your cleanup has completed successfully.
* Make cleanup idempotent: if it runs multiple times (controller retries/crashes), it should safely treat already-deleted resources as success.
* Record failures in Status, Events, or Logs so operators can diagnose why an object remains Terminating.

If cleanup keeps failing, the resource will remain in Terminating. That is safer than silently leaking external resources, but it requires good observability so humans can take corrective action.

```bash theme={null}
kubectl get webapp site
