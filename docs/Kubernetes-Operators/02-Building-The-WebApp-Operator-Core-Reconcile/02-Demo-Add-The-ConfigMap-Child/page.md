# Demo Add The ConfigMap Child

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Add-The-ConfigMap-Child/page

Tutorial extending a WebApp controller to create a ConfigMap child, showing helper functions, owner reference setting, existence check, create-if-missing pattern, and error handling.

The WebApp controller in this tutorial already creates a Deployment. We will extend it to create a second child object: a ConfigMap.

A ConfigMap is a Kubernetes object for storing small pieces of configuration text, such as settings, file contents, or simple HTML that an application can read later. This demonstrates the common controller-runtime reconcile pattern: build the desired child object, set ownership, check if it exists, create it if missing, and return real errors so the controller requeues appropriately.

Quick links and references

* [Kubernetes ConfigMap](https://kubernetes.[AWS_SECRET_ACCESS_KEY]/)
* [controller-runtime documentation](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [Kubernetes API conventions](https://kubernetes.io/docs/reference/using-api/api-concepts/)

Imports
Add the following imports to the top of your controller file if they are not already present:

```go theme={null}
import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/types"
    webappv1 "your/module/api/v1" // replace with your actual module path
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
)
```

Helpers
Keep object construction logic in helper functions so Reconcile stays compact and easy to follow.

* `deploymentFor` constructs the desired Deployment for a given `WebApp`.
* `configMapFor` constructs the desired ConfigMap for a given `WebApp`.

Example helper implementations:

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
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: labels,
                },
                Spec: corev1.PodSpec{
                    // Pod spec details (containers, etc.) go here...
                },
            },
        },
    }
}

func configMapFor(w *webappv1.WebApp) *corev1.ConfigMap {
    return &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name:      w.Name + "-config",
            Namespace: w.Namespace,
            Labels:    map[string]string{"app": w.Name},
        },
        Data: map[string]string{
            // Note: show the HTML inside a code block or string literal to avoid MDX parsing issues.
            "welcome.html": "<h1>Hello from " + w.Name + "</h1>",
        },
    }
}
```

Why these fields?

| Field                  | Purpose                                          | Notes / Example                                                                                  |
| ---------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `ObjectMeta.Name`      | Identifies the child resource                    | We use `w.Name + "-config"` to make the relationship visible (e.g., `webapp-sample-config`).     |
| `ObjectMeta.Namespace` | Ensures child is namespaced with the parent      | ConfigMaps are namespaced; copy `w.Namespace`.                                                   |
| `Labels`               | Group related children for selectors and listing | Use a common label like `app: w.Name` so you can find all related children with `-l app=<name>`. |
| `Data`                 | Stores configuration content keyed by filename   | `{"welcome.html": "<h1>Hello from ...</h1>"}` — keep small strings or file contents here.        |

Setup the controller
Ensure `SetupWithManager` still registers the `WebApp` type:

```go theme={null}
func (r *WebAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&webappv1.WebApp{}).
        Named("webapp").
        Complete(r)
}
```

Call the helper from Reconcile
Update `Reconcile` to build the desired ConfigMap, set the owner reference, and create it if it's missing. The pattern:

1. Fetch the `WebApp` instance.
2. Build the desired child: `desiredCM := configMapFor(&webapp)`.
3. Set the controller reference so garbage collection and ownership work.
4. Attempt to `Get` the existing ConfigMap.
5. If `IsNotFound`, `Create` the ConfigMap.
6. Return real errors for other failures (so controller-runtime retries).

Example Reconcile (only the relevant parts for ConfigMap handling are shown):

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); apierrors.IsNotFound(err) {
        // The WebApp resource was deleted — nothing to do.
        return ctrl.Result{}, nil
    } else if err != nil {
        return ctrl.Result{}, err
    }

    // Build the desired ConfigMap (what we want in the cluster).
    desiredCM := configMapFor(&webapp)

    // Make the WebApp the controller/owner of the ConfigMap.
    if err := controllerutil.SetControllerReference(&webapp, desiredCM, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    // Check if the ConfigMap already exists.
    foundCM := &corev1.ConfigMap{}
    err := r.Get(ctx, types.NamespacedName{Name: desiredCM.Name, Namespace: desiredCM.Namespace}, foundCM)
    if apierrors.IsNotFound(err) {
        r.Log.Info("creating ConfigMap", "name", desiredCM.Name)
        if err := r.Create(ctx, desiredCM); err != nil {
            // Creation failed — requeue by returning the error.
            return ctrl.Result{}, err
        }
    } else if err != nil {
        // Some other error occurred while trying to Get — return it.
        return ctrl.Result{}, err
    }

    // This demo does not yet update existing children; it only creates missing children.
    return ctrl.Result{}, nil
}
```

<Callout icon="warning">
  Always set the controller reference (owner reference) on child objects. Without it, the garbage collector won't remove children when the parent is deleted, and the relationship won't be visible to controller-runtime's owner-based watches.
</Callout>

Error handling notes

* If `controllerutil.SetControllerReference` fails, return the error to requeue reconciliation.
* If `Get` returns `IsNotFound`, create the resource; if the `Create` call fails, return the error so the reconcile is retried.
* For any other `Get` error (API server unavailable, permission issues, etc.), return that error so controller-runtime retries.
* This initial implementation implements a create-if-missing pattern. You can extend it later to add update-and-repair behavior for existing children (compare desired vs found and patch/update as needed).

Build and test
Compile and run your controller to catch Go mistakes and test behavior:

```bash theme={null}
