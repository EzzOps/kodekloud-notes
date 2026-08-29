# Lab Solution Emit Events And Tune Requeue Behavior

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Lab-Solution-Emit-Events-And-Tune-Requeue-Behavior/page

Explains adding event emission and timed requeue to a Kubernetes controller to report child Deployment readiness, update custom resource status, and improve user visibility during reconciliation.

Events are a lightweight, standard Kubernetes mechanism to explain controller decisions (for example, why a child Deployment was created or updated). In this lesson we reuse the Kubernetes event system to report readiness progress from the controller so users inspecting the parent custom resource can see the controller's reasoning and progress without hunting through child resources or controller logs.

We already copy the observed ready replica count from the child Deployment into the WebApp status. Now we will emit short events describing whether the child Deployment is still converging or has reached the requested replica count. These events are attached to the WebApp custom resource so tools like `kubectl describe` show the controller’s progress messages directly on the parent object.

## Design overview

* The WebApp `spec` is the user's desired state (e.g., `replicas`).
* The child Deployment reports actual state through `status` (e.g., `dep.Status.ReadyReplicas`).
* The controller copies the observed number into the WebApp `status`.
* Events provide an additional layer: they describe the controller’s decision during each reconcile pass.
* Use a timed requeue (`RequeueAfter`) to schedule a follow-up check when the Deployment is converging instead of returning an error.

## Controller changes

1. Add an `EventRecorder` field to the reconciler.
2. Wire the recorder into the controller in `cmd/main.go` using the manager’s `GetEventRecorderFor`.
3. Emit events after observing and updating status, and use a timed requeue while waiting for readiness.

### Reconciler skeleton

Add the new imports and a `Recorder` field to the `WebAppReconciler`. Note the `record` and `time` imports; the reconciler will use a timed requeue.

```go theme={null}
package controller

import (
    "context"
    "time"

    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "k8s.io/apimachinery/pkg/util/intstr"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"

    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/record"
    logf "sigs.k8s.io/controller-runtime/pkg/log"

    webappv1 "github.com/kodekloud/webapp-operator/api/v1"
)

type WebAppReconciler struct {
    Client   client.Client
    Scheme   *runtime.Scheme
    Recorder record.EventRecorder
}
```

### RBAC rules

Make sure your RBAC markers include status access so the controller can update the WebApp status:

```go theme={null}
// +kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps/status,verbs=get;update;patch
```

| RBAC marker      | Purpose                                                                            |
| ---------------- | ---------------------------------------------------------------------------------- |
| `webapps`        | Basic CRUD operations on the custom resource                                       |
| `webapps/status` | Allows updating the resource status subresource (required to write observed state) |

## Wiring the recorder in main

The controller manager exposes an event recorder via `GetEventRecorderFor`. Supply that to the reconciler so it can emit events. The provided source name (for example, `webapp-controller`) appears in the events table and helps link events to the emitting controller.

```go theme={null}
package main

import (
    "os"

    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/healthz"

    "github.com/kodekloud/webapp-operator/controllers"
    // ...
)

func main() {
    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
        LeaderElectionReleaseOnCancel: true,
    })
    if err != nil {
        setupLog.Error(err, "Failed to start manager")
        os.Exit(1)
    }

    if err = (&controllers.WebAppReconciler{
        Client:   mgr.GetClient(),
        Scheme:   mgr.GetScheme(),
        Recorder: mgr.GetEventRecorderFor("webapp-controller"),
    }).SetupWithManager(mgr); err != nil {
        setupLog.Error(err, "Failed to create controller", "controller", "WebApp")
        os.Exit(1)
    }

    // +kubebuilder:scaffold:builder

    if err := mgr.AddHealthzCheck("healthz", healthz.Ping); err != nil {
        setupLog.Error(err, "Failed to set up health check")
    }

    if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
        setupLog.Error(err, "problem running manager")
        os.Exit(1)
    }
}
```

## Emitting events in Reconcile

Place the event emission after:

* You have ensured the child Deployment exists (created/updated if necessary).
* You have copied the observed Deployment state into the WebApp `status`.

This guarantees you use fresh observed data for the decision and attach the event to the correct parent object.

Create a local variable for the desired replica count to make the comparison explicit:

```go theme={null}
desiredReplicas := w.Spec.Replicas
```

Compare `dep.Status.ReadyReplicas` to `desiredReplicas`. If the Deployment has fewer ready replicas than requested, emit a `Warning`-type event that informs the user the controller is waiting, and schedule a follow-up check using `RequeueAfter` rather than returning an error. When the Deployment reaches the requested replicas, emit a `Normal`-type event to indicate readiness.

Here is the relevant portion of `Reconcile`. It assumes you have `w` (the WebApp) and `dep` (the child Deployment) already loaded and any create/update logic already performed.

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    // ... load WebApp into w, load or create Deployment into dep, create/update as needed ...

    // After updating or ensuring the Deployment exists and after copying observed state
    // into WebApp status, compare observed vs desired.
    desiredReplicas := w.Spec.Replicas

    if dep.Status.ReadyReplicas < desiredReplicas {
        // Attach the event to the WebApp so users don't have to inspect child resources.
        r.Recorder.Eventf(
            &w,
            corev1.EventTypeWarning,
            "WaitingForReplicas",
            "Waiting for Deployment %s to become ready: %d/%d replicas ready",
            dep.Name,
            dep.Status.ReadyReplicas,
            desiredReplicas,
        )

        // Schedule a follow-up check without returning an error (this is normal progress).
        return ctrl.Result{RequeueAfter: 15 * time.Second}, nil
    }

    // If we reach here, the Deployment has at least the requested replicas ready.
    r.Recorder.Eventf(
        &w,
        corev1.EventTypeNormal,
        "WebAppReady",
        "Deployment %s is ready: %d/%d replicas ready",
        dep.Name,
        dep.Status.ReadyReplicas,
        desiredReplicas,
    )

    // Continue with any remaining reconcile logic (e.g., services, final status update).
    svc := serviceFor(&w)
    if err := ctrl.SetControllerReference(&w, svc, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.Create(ctx, svc); err != nil && !apierrors.IsAlreadyExists(err) {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

Key notes about the event call:

* The first argument to `Eventf` is a pointer to the WebApp object; events are intentionally attached to the parent CR so users inspecting the CR see the messages first.
* Use `corev1.EventTypeWarning` to indicate a not-ready state that merits attention. In this context, “Warning” signals that the controller is waiting for readiness — it does not necessarily mean a reconcile failed.
* Use a short, stable `reason` (e.g., `WaitingForReplicas` or `WebAppReady`) and put formatted details in the message.
* Returning `nil` error with a non-zero `RequeueAfter` schedules a normal follow-up check, which is preferable to forcing an error retry path.

| Event field | Purpose / example                                                   |
| ----------- | ------------------------------------------------------------------- |
| `type`      | `corev1.EventTypeWarning` or `corev1.EventTypeNormal`               |
| `reason`    | Short stable label like `WaitingForReplicas` or `WebAppReady`       |
| `message`   | Human-friendly formatted message (supports `Eventf` placeholders)   |
| `object`    | Pass the parent CR pointer (so the event is attached to the WebApp) |

> **lightbulb** Attach events to the parent CR so users can inspect progress and decisions without needing to hunt for child resources or controller logs. Use a timed requeue to poll for readiness rather than treating a non-ready deployment as an error.

> **warning** Choose a requeue delay that balances responsiveness with controller load. Very frequent requeues can increase API server pressure; very slow requeues can delay progress visibility.

## Build and run

Build locally before starting the manager to catch missing imports or compile-time errors.

```bash theme={null}
$ make build
mkdir -p "/home/student/work/labs/060-008_lab_emit_events_and_tune_requeue_behavior/webapp-operator/bin"
Downloading sigs.k8s.io/controller-tools/cmd/controller-gen@v0.20.1
"/home/student/work/labs/060-008_lab_emit_events_and_tune_requeue_behavior/webapp-operator/bin/controller-gen" rbac:roleName=manager-role crd webhook paths="../.." output:crd:artifacts=config/crd/bases
go fmt ../..
go vet ../..
go build -o bin/manager cmd/main.go
```

Start the manager in the foreground. In a second terminal, apply the sample WebApp and watch progress. The sample requests two replicas. Use the Deployment wait to confirm the child workload becomes available, and inspect the parent WebApp `status` and `Events` for controller progress messages.

```bash theme={null}
$ kubectl apply -f ../webapp-site.yaml
$ kubectl -n webapp-demo wait --for=condition=Available deployment.apps/site --timeout=120s
$ kubectl -n webapp-demo get webapp site -o yaml
```

You should see `status.readyReplicas` updated on the WebApp and `kubectl describe` will show the `WaitingForReplicas` events followed by a `WebAppReady` event attached to the WebApp. For example:

```bash theme={null}
Ready Replicas: 2
Events:
  Type    Reason                   Age                From              Message
  ----    ------                   ----               ----              -------
  Warning WaitingForReplicas      48s (x4 over 48s)  webapp-controller Waiting for Deployment site to become ready: 0/2 replicas ready
  Warning WaitingForReplicas      38s                webapp-controller Waiting for Deployment site to become ready: 1/2 replicas ready
  Normal  WebAppReady             37s (x2 over 37s)  webapp-controller Deployment site is ready: 2/2 replicas ready
```

## Summary

* Status answers: “What does the controller observe now?” (observed values, e.g., `status.readyReplicas`).
* Events answer: “What important decision did the controller just report?” (human-friendly progress and reasoning).
* `RequeueAfter` bridges the gap by scheduling deliberate follow-up checks during normal convergence rather than using errors to retrigger reconciliation.

Together, status + events + timed requeues make custom resources easier to understand and debug when auditing controller behavior or troubleshooting application rollout progress.

## References

* Kubernetes Events and Troubleshooting: [https://kubernetes.io/docs/tasks/debug-application-cluster/events-custom-metrics-pipeline/](https://kubernetes.io/docs/tasks/debug-application-cluster/events-custom-metrics-pipeline/)
* Controller Runtime (sigs.k8s.io/controller-runtime): [https://pkg.go.dev/sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/344c359d-abf3-4286-a12f-710dbb68d656)
