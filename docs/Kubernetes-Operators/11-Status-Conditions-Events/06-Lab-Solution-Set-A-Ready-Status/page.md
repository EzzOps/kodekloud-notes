# Lab Solution Set A Ready Status

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Lab-Solution-Set-A-Ready-Status/page

Explains how a Kubernetes operator copies a child Deployment's ReadyReplicas into a parent WebApp status using controller-runtime and r.Status().Update

This guide shows how to make a parent custom resource (WebApp) report the ready replica count of its child Deployment by copying the child's `ReadyReplicas` into the parent `status`. This is a common pattern for Kubernetes operators built with controller-runtime.

Summary of the change

* Read the live child Deployment from the API server.
* Copy `dep.Status.ReadyReplicas` into `webapp.Status.ReadyReplicas`.
* Persist that observation with `r.Status().Update(ctx, &webapp)`.

Why this matters

* The status subresource represents the controller's observed state. By updating `status` with the child's observed values, users can inspect the parent resource alone to determine runtime health without inspecting children directly.
* Use the status client (`r.Status()`) rather than `r.Update` to avoid unintentionally changing spec fields.

Compact, correct Reconcile implementation

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var w webappv1.WebApp
    // Read the parent WebApp instance
    if err := r.Get(ctx, req.NamespacedName, &w); err != nil {
        if apierrors.IsNotFound(err) {
            // WebApp was deleted — nothing to do.
            return ctrl.Result{}, nil
        }
        // Other errors should be retried by controller-runtime.
        return ctrl.Result{}, err
    }

    // Ensure desired child Deployment exists (deploymentFor constructs the desired Deployment).
    desiredDeploy := deploymentFor(&w)
    if err := controllerutil.SetControllerReference(&w, desiredDeploy, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.Create(ctx, desiredDeploy); err != nil && !apierrors.IsAlreadyExists(err) {
        return ctrl.Result{}, err
    }

    // Ensure Service exists (serviceFor constructs the desired Service).
    svc := serviceFor(&w)
    if err := controllerutil.SetControllerReference(&w, svc, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.Create(ctx, svc); err != nil && !apierrors.IsAlreadyExists(err) {
        return ctrl.Result{}, err
    }

    // Read the live child Deployment from the API server.
    var dep appsv1.Deployment
    if err := r.Get(ctx, client.ObjectKey{Name: w.Name, Namespace: w.Namespace}, &dep); err != nil {
        // If we cannot read the Deployment, return the error so controller-runtime will retry.
        return ctrl.Result{}, err
    }

    // If the observed ready replicas differ from what we report, update status.
    if w.Status.ReadyReplicas != dep.Status.ReadyReplicas {
        w.Status.ReadyReplicas = dep.Status.ReadyReplicas
        if err := r.Status().Update(ctx, &w); err != nil {
            return ctrl.Result{}, err
        }
    }

    return ctrl.Result{}, nil
}
```

Key flow and error handling details

* The controller first reads the parent WebApp instance. If it no longer exists, reconciliation ends.
* It then ensures the desired child Deployment and Service exist, creating them if necessary and setting owner references so garbage collection and controller-runtime can manage lifecycle.
* The live child Deployment is read from the API server and acts as the source of truth for `ReadyReplicas`.
* If reading the Deployment fails, the Reconcile returns the error, causing controller-runtime to retry. The controller cannot truthfully report readiness without reading the child.
* Status updates must use the status client: `r.Status().Update(...)`. The status subresource is for the controller's observed state and is distinct from spec fields that users edit.

> **lightbulb** Always use `r.Status().Update` (the status client) to change `.status` fields. Using `r.Update` modifies the whole object and is intended for spec changes.

Quick reference: API methods used

| Action        | Purpose                                           | Example                                                                    |
| ------------- | ------------------------------------------------- | -------------------------------------------------------------------------- |
| Read parent   | Load the custom resource being reconciled         | `r.Get(ctx, req.NamespacedName, &w)`                                       |
| Set owner     | Make the parent the controller/owner of the child | `controllerutil.SetControllerReference(&w, desiredDeploy, r.Scheme)`       |
| Create child  | Ensure Deployment/Service exist                   | `r.Create(ctx, desiredDeploy)`                                             |
| Read child    | Observe actual runtime state                      | `r.Get(ctx, client.ObjectKey{Name: w.Name, Namespace: w.Namespace}, &dep)` |
| Update status | Persist observed state on parent                  | `r.Status().Update(ctx, &w)`                                               |

Run and validate locally

1. Build and run your manager locally to validate compilation and behavior.
2. Sample manager logs (trimmed):

```log theme={null}
INFO	setup	Starting manager
INFO	starting server {"name": "health probe", "addr": "[::]:8081"}
INFO	Starting EventSource  {"controller": "webapp", "controllerKind": "WebApp", "source": {"kind source": "*v1.Deployment"}}
INFO	Starting EventSource  {"controller": "webapp", "controllerKind": "WebApp", "source": {"kind source": "*v1.WebApp"}}
INFO	Starting Controller  {"controller": "webapp", "controllerKind": "WebApp"}
INFO	Starting workers  {"controller": "webapp", "worker count": 1}
```

3. In another terminal, apply the sample WebApp and wait for the child Deployment to become available:

```bash theme={null}
kubectl apply -f ../webapp-site.yaml
kubectl -n webapp-demo wait --for=condition=Available deployment.apps/site --timeout=120s
```

Expected result

* The Deployment controller reports `ReadyReplicas` first. The WebApp controller reads that observed value and publishes it onto the parent WebApp status.
* After reconciliation, `webapp.status.readyReplicas` should match the Deployment's ready replica count (for example, `2`), allowing users to inspect the parent resource alone for availability information.

Additional references

* controller-runtime: [https://pkg.go.dev/sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* Kubernetes API concepts: [https://kubernetes.io/docs/concepts/overview/](https://kubernetes.io/docs/concepts/overview/)

Helper reminder

```go theme={null}
func deploymentFor(webapp *webappv1.WebApp) *appsv1.Deployment {
    // ... existing helper that builds the desired Deployment for the WebApp ...
}
```

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/dcda0b4e-c708-4217-8a7f-ee23d59556c1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/2a7ff1bc-0f91-4d58-8033-125baa0471dc)
