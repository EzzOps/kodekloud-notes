# Demo Report Readyreplicas In Status

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Status-Conditions-Events/Demo-Report-Readyreplicas-In-Status/page

Adding a readyReplicas status field to a WebApp CRD and updating the controller to copy Deployment ready replicas into WebApp.status while regenerating CRDs

The WebApp custom resource accepts a desired replica count in `spec`. The child Deployment reports how many replicas are actually ready, but that observed value was not surfaced on the parent `WebApp` resource. Today, an operator must inspect the child Deployment to see the observed `readyReplicas`.

This guide shows how to add an observed status field, `readyReplicas`, to the `WebApp` status and how to populate it from the child Deployment during reconciliation. The field belongs in `status` because it represents observed state rather than user intent.

Summary of changes

* Add `ReadyReplicas int32 `json:"readyReplicas,omitempty"`to`WebAppStatus\`.
* Ensure the `WebApp` type includes `Spec` and `Status` fields.
* In the reconciler, copy `Deployment.Status.ReadyReplicas` into `WebApp.Status.ReadyReplicas`.
* Only update the API server when the status value actually changes.
* Regenerate and install CRD manifests so the API server accepts the new status field.

Files touched

| File                               | Purpose                                                                             |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| `api/v1/webapp_types.go`           | Add `ReadyReplicas` to `WebAppStatus` and include `Spec`/`Status` on `WebApp`.      |
| `controllers/webapp_controller.go` | Read Deployment status and update `WebApp.Status.ReadyReplicas` when it changes.    |
| CRD manifests                      | Regenerate with `make manifests` so `readyReplicas` is persisted by the API server. |

1. Update the API type

Open the WebApp API (typically `api/v1/webapp_types.go`) and locate `WebAppStatus`. Initially the types looked like this:

```go theme={null}
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type WebAppSpec struct {
    // +kubebuilder:validation:Required
    Image string `json:"image"`
    // +kubebuilder:default=1
    Replicas int32 `json:"replicas,omitempty"`
}

type WebAppStatus struct {
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
type WebApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
}
```

Add `ReadyReplicas` as an `int32` field with the JSON name `readyReplicas`. Kubernetes replica counts use 32-bit integers, so the custom status field should use `int32`. The JSON tag controls the field name stored by the API server, which is why users will later read `status.readyReplicas`.

Replace the type definitions with:

```go theme={null}
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type WebAppSpec struct {
    // +kubebuilder:validation:Required
    Image string `json:"image"`
    // +kubebuilder:default=1
    Replicas int32 `json:"replicas,omitempty"`
}

type WebAppStatus struct {
    ReadyReplicas int32 `json:"readyReplicas,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
type WebApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   WebAppSpec   `json:"spec,omitempty"`
    Status WebAppStatus `json:"status,omitempty"`
}
```

2. Update the reconciler

The reconciler already ensures the child Deployment exists. After you have the existing Deployment in memory, copy its `Status.ReadyReplicas` into the `WebApp.Status.ReadyReplicas`. Only call `r.Status().Update` when the value changes to avoid unnecessary writes and extra reconcile traffic.

A concise, correct `Reconcile` implementation demonstrating these steps:

```go theme={null}
package controller

import (
    "context"

    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/types"
    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    ctrl "sigs.k8s.io/controller-runtime"

    webappv1 "github.com/example/webapp-operator/api/v1"
)

// Reconciler skeleton omitted (assume r.Client, r.Log, r.Scheme exist)

func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1) Fetch the WebApp
    var webapp webappv1.WebApp
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        if apierrors.IsNotFound(err) {
            // WebApp deleted, nothing to do
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, err
    }

    // 2) Build the desired Deployment from the WebApp
    deploy := deploymentFor(&webapp) // helper that returns *appsv1.Deployment

    // 3) Ensure the Deployment has the correct owner ref
    if err := ctrl.SetControllerReference(&webapp, deploy, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    // 4) Get existing Deployment or create it
    deployKey := types.NamespacedName{Name: deploy.Name, Namespace: deploy.Namespace}
    existingDeploy := &appsv1.Deployment{}
    if err := r.Get(ctx, deployKey, existingDeploy); err != nil {
        if apierrors.IsNotFound(err) {
            if err := r.Create(ctx, deploy); err != nil {
                return ctrl.Result{}, err
            }
            r.Log.Info("created Deployment", "name", deploy.Name)
            // After creating the deployment, we can requeue or return and wait for the Deployment
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, err
    }

    // 5) Copy observed ready replicas from Deployment status into WebApp status,
    //    but only update the API server if the value changed.
    if webapp.Status.ReadyReplicas != existingDeploy.Status.ReadyReplicas {
        webapp.Status.ReadyReplicas = existingDeploy.Status.ReadyReplicas
        if err := r.Status().Update(ctx, &webapp); err != nil {
            return ctrl.Result{}, err
        }
    }

    // 6) Continue with other reconciliation tasks (e.g., Service)
    svc := serviceFor(&webapp) // helper that returns *corev1.Service
    if err := ctrl.SetControllerReference(&webapp, svc, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }
    if err := r.Get(ctx, types.NamespacedName{Name: svc.Name, Namespace: svc.Namespace}, &corev1.Service{}); err != nil {
        if apierrors.IsNotFound(err) {
            if err := r.Create(ctx, svc); err != nil {
                return ctrl.Result{}, err
            }
        } else {
            return ctrl.Result{}, err
        }
    }

    return ctrl.Result{}, nil
}
```

Why the guard matters

* Status updates write to the API server and can trigger additional reconcile loops. Only updating when the observed value actually changes reduces noise and unnecessary API usage.

> **lightbulb** Use `r.Status().Update(ctx, &obj)` to write only the status subresource. This keeps observed state separate from the desired state in `spec`, which users edit.

If the status update fails, return the error so controller-runtime retries the reconcile.

3. Regenerate and install CRDs

Because the Go type is only the source of truth during code generation, regenerate the CRD manifests and install the CRD so the API server knows about the new field. The CRD schema must include `readyReplicas` before the API server will persist that field.

```bash theme={null}
$ make manifests
mkdir -p "/home/student/work/labs/060-003_demo_report_readyreplicas_in_status/webapp-operator/bin"
Downloading sigs.k8s.io/controller-tools/cmd/controller-gen@v0.20.1
"/home/student/work/labs/060-003_demo_report_readyreplicas_in_status/webapp-operator/bin/controller-gen" rbac:roleName=manager-role crd webhook paths="./.." output:crd:artifacts=config=config/crd/bases
$ make install
"/home/student/work/labs/060-003_demo_report_readyreplicas_in_status/webapp-operator/bin/controller-gen" rbac:roleName=manager-role crd webhook paths="./.." output:crd:artifacts=config=config/crd/bases
Downloading sigs.k8s.io/kustomize/kustomize/v5@v5.8.1
customresourcedefinition.apiextensions.k8s.io/webapps.webapp.kodekloud.com configured
```

4. Run the manager and verify

Start your manager locally, apply the namespace and a sample `WebApp`, and wait for the Deployment to become available. Once the Deployment controller reports ready replicas, the `WebApp` reconciler will copy that value into `status`.

For example, after the Deployment becomes available you can read:

```bash theme={null}
$ kubectl get webapp sample-webapp -o jsonpath='{.status.readyReplicas}'
2
```

That number came from the child Deployment, but it is now visible on the parent resource. The `WebApp` can answer this common operational question directly without requiring the operator to inspect the child Deployment.

References

* [Kubernetes API Conventions — Status Subresource](https://kubernetes.io/docs/reference/using-api/api-concepts/#spec-and-status)
* [controller-runtime: Status Writer](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/client#StatusWriter)
* [Kubebuilder Book](https://book.kubebuilder.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/715ddc8b-3997-4878-8900-2f710183ee13/lesson/0a9f4820-8012-4f05-bc2b-030ee38dd113)
