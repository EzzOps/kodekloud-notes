# reason: for tools
# message: for humans
```

Core condition types to keep in most controllers

* Ready — Does the resource meet the requested state (e.g., deployment has required ready replicas)?
* Progressing — Is the controller still moving toward that state (e.g., during a rollout)?
* Degraded — Has the controller observed a problem that blocks normal operation?

These three lights provide a focused view without turning `status` into a crowded control panel.

<Frame>
  <img alt="The image explains three condition types using traffic lights: &#x22;Ready&#x22; (green), &#x22;Progressing&#x22; (yellow), and &#x22;Degraded&#x22; (red), each associated with a question about system status. A note suggests asking steady questions instead of keeping a diary." />
</Frame>

> **lightbulb** Keep condition types steady and focused: they should ask continuous health questions (Ready, Progressing, Degraded), not log every event or reconcile step.

Design guidance and best practices

* Keep condition types stable and few. They are part of your API's contract and are used by alerts, dashboards, and other controllers.
* Make `Reason` predictable and machine-friendly; use `Message` for human context.
* Only update `LastTransitionTime` when the condition value actually changes.
* Populate `ObservedGeneration` so users can detect stale status.

A single resource can show multiple lights at once. Conditions are not a single giant state machine — they answer independent questions. For example, during a rollout:

* `Progressing` can be `True` while `Ready` is `False`.
* In steady state, `Ready` can be `True` while `Degraded` is `False`.

<Frame>
  <img alt="The image shows a diagram explaining two conditions: &#x22;Rollout&#x22; with progress lights indicating &#x22;Progressing&#x22; (True) and &#x22;Ready&#x22; (False), and &#x22;Steady state&#x22; with lights indicating &#x22;Ready&#x22; (True) and &#x22;Degraded&#x22; (False)." />
</Frame>

> **warning** Do not overload conditions with transient or debug-level events. Conditions should answer steady-state health questions, not act as a message log.

Keep the dashboard small and pragmatic. For a typical web app controller, the three lights (Ready, Progressing, Degraded) give operators and tools the context they need without forcing them to interpret raw gauges alone.

Next demo: we’ll start with the simplest gauge — ready replicas — and show how to map that measurement into the `Ready` condition. Good status design makes controllers and clusters easier to understand, debug, and operate.

Links and further reading

* [Kubernetes API Conventions: Conditions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#condition-typing)
* [metav1.Condition Go type reference](https://pkg.go.dev/k8s.io/apimachinery@v0.29.0/pkg/apis/meta/v1#Condition)
* [Golang course reference used above](https://learn.kodekloud.com/user/courses/golang)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/c310be49-f2da-42f5-9e9f-9a67c26b5d7b)


# Demo Emit Events From Reconcile

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Demo-Emit-Events-From-Reconcile/page

Explains adding controller-scoped Kubernetes events using an EventRecorder and controllerutil.CreateOrUpdate during reconciliation to record Deployment create and update actions

The WebApp custom resource already reports a numeric `status` value that reflects what the controller observes now. Events answer a related but distinct question: what did the controller just do? In this lesson we keep the existing status behavior and add Kubernetes events whenever the controller creates or updates the child `Deployment`.

Events are valuable because they appear in places Kubernetes users already inspect when debugging — for example, in `kubectl describe` output. If a WebApp was accepted by the API server but the controller changed something during reconciliation, an event explains the recent action without requiring users to tail controller logs.

Below we walk through the minimal changes required to emit informative, controller-scoped events from the reconciler.

> **lightbulb** The manager owns the event broadcaster. Reconciler instances should accept an `EventRecorder` from the manager so events show which controller reported the action (don't create your own recorder directly).

## Overview — what you will change

* Add the `record` package to imports and add a `Recorder` field to the reconciler struct.
* Obtain a named `EventRecorder` from the manager in `cmd/main.go` and pass it to the reconciler.
* Replace the manual get-or-create `Deployment` flow with `controllerutil.CreateOrUpdate`, using the returned operation to emit events describing created/updated/unchanged state.

## Imports and Reconciler fields

Consolidate imports and include the Client-Go `record` package and controller util helpers. The reconciler accepts an `EventRecorder` so events are linked to the controller that reported them.

```go theme={null}
package controller

import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "k8s.io/client-go/tools/record"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    logf "sigs.k8s.io/controller-runtime/pkg/log"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

    webappv1 "github.com/kodekloud/webapp-operator/api/v1"
)

type WebAppReconciler struct {
    client.Client
    Scheme   *runtime.Scheme
    Recorder record.EventRecorder
}

// +kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps/status,verbs=get;update;patch
```

## Wiring the recorder in cmd/main.go

Obtain an `EventRecorder` from the manager and pass it into the reconciler when you register it. This makes events annotated with the controller name and ensures they’re visible in standard debugging interfaces.

```go theme={null}
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
    Scheme: scheme,
    // ...
})
if err != nil {
    // handle err
}

recorder := mgr.GetEventRecorderFor("webapp-controller")

if err = (&controller.WebAppReconciler{
    Client:   mgr.GetClient(),
    Scheme:   mgr.GetScheme(),
    Recorder: recorder,
}).SetupWithManager(mgr); err != nil {
    // handle err
}
```

## Reconcile: use controllerutil.CreateOrUpdate and emit events

Use `controllerutil.CreateOrUpdate` to simplify the get-or-create logic for the Deployment. The function reads the live object into your pointer (if present), calls a mutate function to set desired state, and persists any changes. The returned `op` indicates whether the object was created, updated, or unchanged, which is ideal for emitting human-friendly events.

A concise, clarified `Reconcile` implementation:

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Build an empty Deployment object with just name + namespace.
    dep := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      webapp.Name,
            Namespace: webapp.Namespace,
        },
    }

    // Create or update the Deployment. The mutate function sets desired fields.
    op, err := controllerutil.CreateOrUpdate(ctx, r.Client, dep, func() error {
        // Desired deployment derived from the WebApp spec helper.
        desired := deploymentFor(&webapp)

        // Copy fields the controller owns.
        if dep.Labels == nil {
            dep.Labels = make(map[string]string)
        }
        for k, v := range desired.Labels {
            dep.Labels[k] = v
        }

        dep.Spec.Selector = desired.Spec.Selector
        dep.Spec.Replicas = desired.Spec.Replicas

        // If the Deployment has not been created yet, copy the full pod template.
        if dep.CreationTimestamp.IsZero() {
            dep.Spec.Template = desired.Spec.Template.DeepCopy()
        } else {
            // For existing deployments, only update fields we own on the pod template
            // (for example, labels or container image if owned). This keeps changes minimal.
            dep.Spec.Template.Labels = desired.Spec.Template.Labels
            dep.Spec.Template.Spec.Containers = desired.Spec.Template.Spec.Containers
        }

        // Ensure ownership is set so garbage collection works and events attach to the WebApp.
        if err := controllerutil.SetControllerReference(&webapp, dep, r.Scheme); err != nil {
            return err
        }
        return nil
    })
    if err != nil {
        return ctrl.Result{}, err
    }

    // Record an event describing what happened to the deployment.
    switch op {
    case controllerutil.OperationResultCreated:
        r.Recorder.Event(&webapp, corev1.EventTypeNormal, "Created", "Created Deployment for WebApp")
        log.Info("Deployment created", "webapp", webapp.Name)
    case controllerutil.OperationResultUpdated:
        r.Recorder.Event(&webapp, corev1.EventTypeNormal, "Updated", "Updated Deployment for WebApp")
        log.Info("Deployment updated", "webapp", webapp.Name)
    case controllerutil.OperationResultNone:
        // No change; optional event or skip.
        log.V(1).Info("Deployment already up-to-date", "webapp", webapp.Name)
    }

    // Service management (left as create-if-missing as before).
    svc := serviceFor(&webapp)
    if err := controllerutil.SetControllerReference(&webapp, svc, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.Create(ctx, svc); err != nil && !apierrors.IsAlreadyExists(err) {
        return ctrl.Result{}, err
    }

    // Optionally update status with current information from the Deployment.
    // Example: copy ReadyReplicas into status if desired.
    // (Status update logic omitted here for brevity; ensure you patch the status subresource.)

    return ctrl.Result{}, nil
}
```

### Key points about the mutate function

* controller-runtime performs the read (populate `dep` from the API server) and the write (persist changes) around your mutate function.
* The mutate function expresses which fields the operator owns and must maintain. In this example, labels, selector, and replicas are owned and synchronized from the WebApp spec.
* Use `CreationTimestamp.IsZero()` to detect initial creation; it’s safe to copy the entire pod template only on first create. On updates, prefer changing only owned fields to avoid overwriting user-managed configuration.

## Operation result → Event mapping

| Operation result         | Event type       | Message                                 |
| ------------------------ | ---------------- | --------------------------------------- |
| `OperationResultCreated` | `Normal`         | "Created Deployment for WebApp"         |
| `OperationResultUpdated` | `Normal`         | "Updated Deployment for WebApp"         |
| `OperationResultNone`    | (none / verbose) | No event, controller can log at V-level |

These events appear in `kubectl describe webapp <name>` and similar tooling, helping users understand recent controller actions without reading logs.

## Why events matter here

* `CreateOrUpdate` returns an `op` that precisely indicates whether the Deployment was created, updated, or unchanged. Emitting events based on `op` provides concise, human-readable context in the resource history.
* Events surface in standard Kubernetes debugging workflows, giving operators immediate insight into controller activity (for example, when a WebApp triggers a Deployment update).

## References

* [kubectl describe — Documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)
* controller-runtime: `controllerutil.CreateOrUpdate` and `SetControllerReference` methods
* client-go: `tools/record.EventRecorder` for emitting events

This demo continues from this point: the reconciler carefully updates only the fields it owns on the `Deployment` while leaving other fields stable, and emits events to make those actions visible to cluster users.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/7bc676fd-b40a-4ab9-aeb1-a2cda22fd5bc)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/7bb75dc4-045a-4a2c-a776-11137edeeb69)
