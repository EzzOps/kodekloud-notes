# Demo Create A Deployment From Spec

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Create-A-Deployment-From-Spec/page

Explains how to construct a Kubernetes Deployment in Go for a WebApp operator, covering labels, pointer replicas, pod template, and the deploymentFor helper.

The reconciler can now fetch the WebApp custom resource. Next, we need to build the desired Deployment object in Go. At this stage the helper only constructs the in-memory Deployment object — it does not yet call the Kubernetes API. This section focuses on the shape of the Deployment the controller will want to create.

<Frame>
  <img alt="The image is a slide with the title &#x22;Create A Deployment From Spec&#x22; on the left and the word &#x22;Demo&#x22; on the right. It also includes a copyright notice for KodeKloud." />
</Frame>

## Add imports

Open the controller file and add imports for the built-in Kubernetes types we’ll use. These provide the Deployment, Pod template types, and metadata helpers.

```go theme={null}
package controller

import (
    "context"

    "k8s.io/apimachinery/pkg/runtime"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/log"

    webappv1 "github.com/kodekloud/webapp-operator/api/v1"
    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
)
```

## Reconcile skeleton and helper signature

Keep the Reconcile skeleton that reads the WebApp resource. We’ll add a helper named `deploymentFor` that builds the Deployment object for a given `*webappv1.WebApp`.

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    log.Info("fetched WebApp", "image", webapp.Spec.Image, "replicas", webapp.Spec.Replicas)
    return ctrl.Result{}, nil
}

func deploymentFor(w *webappv1.WebApp) *appsv1.Deployment
```

## Build labels

Use a Go map to hold labels that will be applied to both the Deployment selector and the pod template. The selector and template labels must match so the Deployment can find and manage its Pods.

```go theme={null}
func deploymentFor(w *webappv1.WebApp) *appsv1.Deployment {
    labels := map[string]string{"app": w.Name}
    // ...
}
```

> **warning** Ensure the Deployment selector and the Pod template labels are identical. If they differ, the Deployment will not manage the Pods you expect.

## Replicas as a pointer

Kubernetes expects `spec.replicas` to be an optional pointer (`*int32`). Create a local variable, then pass its address into the Deployment spec.

```go theme={null}
func deploymentFor(w *webappv1.WebApp) *appsv1.Deployment {
    labels := map[string]string{"app": w.Name}
    replicas := w.Spec.Replicas
    // ...
}
```

> **lightbulb** `replicas` must be passed as a pointer (e.g., `Replicas: &replicas`) because the API type defines it as `*int32`. Using a plain numeric literal will cause compile-time errors.

## Build the Deployment struct

Create the `appsv1.Deployment` struct literal with metadata, selector, and a Pod template. The Pod template contains a `corev1.PodSpec` with a single container named `web`. The container image comes from the WebApp spec and we expose port 80 inside the Pod.

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
            Selector: &metav1.LabelSelector{MatchLabels: labels},
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{Labels: labels},
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Name:  "web",
                        Image: w.Spec.Image,
                        Ports: []corev1.ContainerPort{{
                            ContainerPort: 80,
                        }},
                    }},
                },
            },
        },
    }
}
```

This helper establishes the first clear connection between your custom resource and a built-in Kubernetes workload: the WebApp tells the operator which image and replica count it wants, and the helper translates that into a Deployment object.

## Types used

| Type                | Purpose                                               | Example                           |
| ------------------- | ----------------------------------------------------- | --------------------------------- |
| `appsv1.Deployment` | Represents the Kubernetes Deployment object           | `&appsv1.Deployment{ ... }`       |
| `corev1.PodSpec`    | Describes the Pod template spec inside the Deployment | `corev1.PodSpec{Containers: ...}` |
| `metav1.ObjectMeta` | Metadata for name, namespace, labels, etc.            | `metav1.ObjectMeta{Name: w.Name}` |

## Build and verify

Run `go build ./...` in your module root. A clean build (no compiler errors) verifies imports, field names, and pointer usage. If the build fails, check for:

* Missing imports (e.g., `metav1`, `appsv1`, `corev1`)
* Incorrect field names or types
* Passing a non-pointer where a pointer is required

At this stage the helper constructs the desired Deployment but does not yet contact the API server. The helper answers: "If this WebApp exists, what Deployment object should represent it?" In a subsequent step you will call `deploymentFor` from `Reconcile` and create or update the Deployment via the controller-runtime client.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/3543a4ee-9bd9-4ac6-9b3b-f53eb8ad77e1)
