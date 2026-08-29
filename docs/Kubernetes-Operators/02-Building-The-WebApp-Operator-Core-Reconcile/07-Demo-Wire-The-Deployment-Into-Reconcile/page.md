# Demo Wire The Deployment Into Reconcile

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Wire-The-Deployment-Into-Reconcile/page

Explains wiring a Kubernetes controller to create and manage a child Deployment using a get-or-create pattern and owner references.

The deployment helper describes the desired state for a child Deployment. In the Reconcile loop, we must:

* construct that desired Deployment,
* set an owner reference so the parent WebApp controls the child,
* look up whether the child already exists, and
* create it if it does not (the get-or-create pattern).

Below we walk through the imports and the Reconcile wiring step-by-step.

## Minimal imports (starting point)

Start with the minimal imports you already had for the controller:

```go theme={null}
package controller

import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
)
```

These are required to reference the Kubernetes Deployment and core types in Go. Next we expand imports to handle error recognition, namespaced lookups, and owner references.

## Expanded imports (recognize not-found and build lookup keys)

Add the API error helper and types so the controller can detect "not found" and form lookup keys:

```go theme={null}
package controller

import (
	"context"

	appsv1    "k8s.io/api/apps/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	corev1    "k8s.io/api/core/v1"
	metav1    "k8s.io/apimachinery/pkg/apis/meta/v1"
	ctrl       "sigs.k8s.io/controller-runtime"
	logf       "sigs.k8s.io/controller-runtime/pkg/log"
)
```

These additions let you call `apierrors.IsNotFound(err)` and work with metadata types.

## Final import set (needed by Get/Create and setting owner refs)

We add `types`, `controllerutil`, `runtime`, and the controller-runtime `client` so the Get/Create and SetControllerReference code compiles and runs:

```go theme={null}
package controller

import (
    "context"

    appsv1             "k8s.io/api/apps/v1"
    apierrors          "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/types"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
    corev1             "k8s.io/api/core/v1"
    metav1             "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    ctrl               "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    logf               "sigs.k8s.io/controller-runtime/pkg/log"
)
```

These imports do not create resources by themselves; they enable the Get/Create and owner-setting code to compile.

<Callout icon="lightbulb">
  Always keep imports minimal but explicit. Add `apierrors` to check for `IsNotFound` and `controllerutil` to set owner references. This makes your controller resilient to the common "get or create" reconciliation pattern.
</Callout>

## Wiring the Deployment in Reconcile

After you fetch the WebApp resource inside Reconcile, call the deployment helper and set the controller reference on the desired Deployment. The helper returns an `*appsv1.Deployment` representing the state you want in the cluster.

* `desiredDeploy` is the desired child object.
* `controllerutil.SetControllerReference` sets the owner reference so garbage collection and ownership semantics work.

Example Reconcile skeleton with these steps:

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    log.Info("fetched WebApp", "image", webapp.Spec.Image, "replicas", webapp.Spec.Replicas)

    desiredDeploy := deploymentFor(&webapp)
    if err := controllerutil.SetControllerReference(&webapp, desiredDeploy, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    // Continue with lookup and conditional create...
}
```

The scheme tells controller-runtime how Go types map to Kubernetes API resource kinds. The SetControllerReference call follows the standard Go error pattern: functions return an `error` value which you must check.

## Lookup (get-or-create) and create-if-missing

Declare an empty `found` Deployment and query the API server using a NamespacedName made from the desired deployment's namespace and name. If the Get returns a "not found" error, create the desired Deployment. Otherwise, if another error occurred, return it.

Complete Get-or-create pattern:

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    log.Info("fetched WebApp", "image", webapp.Spec.Image, "replicas", webapp.Spec.Replicas)

    desiredDeploy := deploymentFor(&webapp)
    if err := controllerutil.SetControllerReference(&webapp, desiredDeploy, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    found := &appsv1.Deployment{}
    err := r.Get(ctx, types.NamespacedName{Name: desiredDeploy.Name, Namespace: desiredDeploy.Namespace}, found)
    if apierrors.IsNotFound(err) {
        log.Info("creating Deployment", "name", desiredDeploy.Name)
        if err := r.Create(ctx, desiredDeploy); err != nil {
            return ctrl.Result{}, err
        }
    } else if err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

This pattern avoids creating duplicates and keeps the first reconcile loop simple. You can add update/drift-repair logic later to reconcile spec differences.

<Callout icon="warning">
  When calling `SetControllerReference`, ensure the `owner` and `object` types are valid and the `scheme` includes the owner type. Otherwise `SetControllerReference` will return an error and reconciliation should stop.
</Callout>

## Example deployment helper

We intentionally keep the Deployment shape consistent with the WebApp spec. The helper returns a Deployment configured with labels, replicas, and a Pod template using the WebApp image.

```go theme={null}
func deploymentFor(w *webappv1.WebApp) *appsv1.Deployment {
    labels := map[string]string{"app": w.Name}
    replicas := w.Spec.Replicas

    return &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      w.Name,
            Namespace: w.Namespace,
            Labels:    labels,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: labels,
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: labels,
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  "webapp",
                            Image: w.Spec.Image,
                            Ports: []corev1.ContainerPort{{ContainerPort: 80}},
                        },
                    },
                },
            },
        },
    }
}
```

This keeps the Deployment consistent with the WebApp resource and makes it straightforward to compare and reconcile later.

## Build and test locally

After wiring the controller, run a local build to ensure there are no compile-time errors, then run the manager and apply the sample WebApp manifest:

```bash theme={null}
$ go build ./...
$ make
```

Run the manager (attached to the first terminal), then in another terminal apply the sample:

```bash theme={null}
$ kubectl apply -f config/samples/webapp_v1_webapp.yaml
$ kubectl get deploy -l app=webapp-sample
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
webapp-sample    2/2     2            2           24s
```

Seeing the Deployment named `webapp-sample` confirms the parent WebApp created the child workload successfully.

## Repetition and pattern reuse

The same get-or-create pattern is repeated for other child objects such as ConfigMaps and Services. Repetition is useful because most reconciler code follows this pattern:

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    log.Info("fetched WebApp", "image", webapp.Spec.Image, "replicas", webapp.Spec.Replicas)
    desiredDeploy := deploymentFor(&webapp)
    if err := controllerutil.SetControllerReference(&webapp, desiredDeploy, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    
    found := &appsv1.Deployment{}
    err := r.Get(ctx, types.NamespacedName{Name: desiredDeploy.Name, Namespace: desiredDeploy.Namespace}, found)
    if apierrors.IsNotFound(err) {
        log.Info("creating Deployment", "name", desiredDeploy.Name)
        if err := r.Create(ctx, desiredDeploy); err != nil {
            return ctrl.Result{}, err
        }
    } else if err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

Table — Common reconciliation checks

| Check       | Purpose                                        | Example                                                   |
| ----------- | ---------------------------------------------- | --------------------------------------------------------- |
| Exists?     | Determine if the child resource already exists | `r.Get(ctx, namespacedName, found)`                       |
| Not found   | Create the child if missing                    | `if apierrors.IsNotFound(err) { r.Create(ctx, desired) }` |
| Other error | Fail reconciliation with error                 | `return ctrl.Result{}, err`                               |

## Links and references

* [controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [Kubernetes API conventions](https://kubernetes.io/docs/reference/using-api/api-concepts/)
* [OwnerReferences and garbage collection](https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/)

This wiring — importing the right helpers, creating a desired object, setting the controller reference, and using a safe get-or-create pattern — is the core of many Kubernetes reconciler implementations.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/4768a5b9-ac1f-4c3d-8f13-242b213b1ff7" />
</CardGroup>
