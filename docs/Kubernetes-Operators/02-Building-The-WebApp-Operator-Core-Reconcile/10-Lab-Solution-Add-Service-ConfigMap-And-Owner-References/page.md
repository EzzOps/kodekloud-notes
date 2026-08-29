# Lab Solution Add Service ConfigMap And Owner References

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Lab-Solution-Add-Service-ConfigMap-And-Owner-References/page

Explains building a Kubernetes controller that creates Deployment Service and ConfigMap children with owner references for a WebApp custom resource

This lab completes Section Four (MVP). The WebApp controller will create three child resources for each WebApp instance:

* Deployment
* Service
* ConfigMap

Each child resource will have an owner reference pointing back to the WebApp custom resource, enabling Kubernetes to garbage collect the children when their parent is deleted.

Imports used by the controller:

```go theme={null}
package controller

import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
)
```

Note the RBAC markers required by kubebuilder for the WebApp controller:

```go theme={null}
// kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps,verbs=get;list;watch;
// kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps/status,verbs=get;
// kubebuilder:rbac:groups=webapp.kodekloud.com,resources=webapps/finalizers,verbs=update
```

Overview of the reconcile pattern

* Build the desired child object from the parent WebApp spec.
* Set the WebApp as the owner of the child via `controllerutil.SetControllerReference`.
* Try to `Get` the existing child.
  * If not found, `Create` the child.
  * If found, optionally `Update` if desired state differs.
* Return any real errors encountered.

> **lightbulb** This pattern — build desired, set controller reference, get current, create-if-missing — is repeated for each child type (Deployment, Service, ConfigMap). Once you understand it for one resource, it applies to the others.

Start by setting the owner reference on the Deployment before attempting to create it:

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
}
```

The controller must check `SetControllerReference` for an error and return it if present.

Handling errors and checking for existing Deployment:

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
    if err != nil && !apierrs.IsNotFound(err) {
        log.Error(err, "retrieving Deployment", "name", desiredDeploy.Name)
        return ctrl.Result{}, err
    }
    // If apierrs.IsNotFound(err) then create the Deployment (handled later)
}
```

Add the Service helper

* The Service helper returns a pointer to a `corev1.Service`.
* The Service selector must match the Pod template labels in the Deployment so traffic routes correctly.
* Use `corev1.ServiceTypeClusterIP` and expose port 80 / target port 80.
* Use `intstr.FromInt(80)` (or `intstr.FromInt32(80)`) to wrap the numeric target port.

Example signature and skeleton:

```go theme={null}
func deploymentFor(w *webappv1.WebApp) *appsv1.Deployment {
    return &appsv1.Deployment{
        Spec: appsv1.DeploymentSpec{
            Template: corev1.PodTemplateSpec{
                // Pod template spec goes here
            },
        },
    }
}
```

Service helper (full example includes metadata, labels and ports):

```go theme={null}
func serviceFor(w *webappv1.WebApp) *corev1.Service {
    labels := map[string]string{"app": w.Name}

    return &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      w.Name,
            Namespace: w.Namespace,
            Labels:    labels,
        },
        Spec: corev1.ServiceSpec{
            Type:     corev1.ServiceTypeClusterIP,
            Selector: labels,
            Ports: []corev1.ServicePort{
                {
                    Port:       80,
                    TargetPort: intstr.FromInt(80),
                },
            },
        },
    }
}
```

Add the ConfigMap helper

* The ConfigMap name should be the WebApp name suffixed with `-config`.
* The data is a Go map where the key is `welcome.html` and the value contains a small HTML string that can include the WebApp name.

Example ConfigMap helper:

```go theme={null}
func configMapFor(w *webappv1.WebApp) *corev1.ConfigMap {
    return &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name:      w.Name + "-config",
            Namespace: w.Namespace,
        },
        Data: map[string]string{
            "welcome.html": "<html><body><h1>Welcome to " + w.Name + "</h1></body></html>",
        },
    }
}
```

Wiring all children in Reconcile

* For each child type: build desired, set controller reference, get current, create if missing, and return errors when they happen.
* This keeps the controller simple and consistent.

Example code for wiring the Service (pattern applies also to Deployment and ConfigMap):

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // ... fetch WebApp as shown previously ...

    // Service
    desiredSvc := serviceFor(&webapp)
    if err := controllerutil.SetControllerReference(&webapp, desiredSvc, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    foundSvc := &corev1.Service{}
    err = r.Get(ctx, types.NamespacedName{Name: desiredSvc.Name, Namespace: desiredSvc.Namespace}, foundSvc)
    if apierrors.IsNotFound(err) {
        log.Info("creating Service", "name", desiredSvc.Name)
        if err := r.Create(ctx, desiredSvc); err != nil {
            return ctrl.Result{}, err
        }
    } else if err != nil {
        return ctrl.Result{}, err
    }

    // Repeat same pattern for Deployment and ConfigMap (build desired, set owner, get, create-if-missing)

    return ctrl.Result{}, nil
}
```

Setup the controller with the manager:

```go theme={null}
func (r *WebAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&webappv1.WebApp{}).
        Named("webapp").
        Complete(r)
}
```

Build and run the controller locally (before touching the cluster):

```bash theme={null}
go build ./...
make run
```

Open another terminal and verify created resources by label:

```bash theme={null}
kubectl -n webapp-demo get deploy,svc,cm -l app=site
```

Check that owner references were added to each child. Each child should report `kind: WebApp` with `controller: true`.

Sample WebApp CR to create:

```yaml theme={null}
kind: WebApp
metadata:
  name: site
  namespace: webapp-demo
spec:
  image: nginx:1.27
  replicas: 2
```

Verify ownerReferences via jsonpath:

```bash theme={null}
$ kubectl -n webapp-demo get deploy site -o jsonpath='{.metadata.ownerReferences[0].kind}'; echo
WebApp
$ kubectl -n webapp-demo get svc site -o jsonpath='{.metadata.ownerReferences[0].kind}'; echo
WebApp
$ kubectl -n webapp-demo get cm site-config -o jsonpath='{.metadata.ownerReferences[0].kind}'; echo
WebApp
```

A full check showing the `controller` flag (example):

```bash theme={null}
$ kubectl -n webapp-demo get deploy site -o jsonpath='{.metadata.ownerReferences[0].controller}'; echo
true
$ kubectl -n webapp-demo get svc site -o jsonpath='{.metadata.ownerReferences[0].controller}'; echo
true
```

Quick reference: resource responsibilities

| Resource Type | Purpose                                     | Example name pattern |
| ------------- | ------------------------------------------- | -------------------- |
| Deployment    | Runs the pods for the WebApp                | `w.Name`             |
| Service       | Routes traffic to pods (ClusterIP port 80)  | `w.Name`             |
| ConfigMap     | Stores static assets such as `welcome.html` | `w.Name + "-config"` |

Links and references

* [Kubernetes Owner References](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)
* [Controller Runtime SetControllerReference](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil)
* [Kubebuilder RBAC markers](https://book.kubebuilder.io/reference/markers/crd.html)

> **warning** Ensure your controller has the proper RBAC permissions for creating and updating Deployments, Services, and ConfigMaps. Missing RBAC rules will surface as permission-denied errors when the controller attempts resource operations.

This pattern — repeated for Deployment, Service, and ConfigMap — makes the controller predictable and easy to extend. Later sections will build on this by adding updates, status updates, and more advanced reconciliation logic.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/fb45983a-b0f1-4da4-931e-25fd2ebe8e73)
