# Demo Fetch The WebApp Object

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Fetch-The-WebApp-Object/page

Describes fetching the live WebApp custom resource in a Kubernetes controller reconcile loop, handling not-found errors, and registering the reconciler with the manager.

When a controller receives a Reconcile request it is given only the resource key (namespace + name), not the full custom resource object. The first step for a robust Kubernetes controller is to use that key to fetch the current WebApp object from the API server before making changes to any child resources.

Below is an example controller file showing the file header Kubebuilder generates and the imports used by the reconciler implementation.

```go theme={null}
/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
    "context"

    webappv1 "your-module-path/api/v1alpha1" // replace with your API module path

    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    logf "sigs.k8s.io/controller-runtime/pkg/log"
)
```

Why fetch the object?

* The Reconcile request provides `req.NamespacedName` (namespace + name). You must call the API to obtain the live object so your controller works against the current desired state.
* Fetching the object lets you inspect `webapp.Spec`, detect deletions, and avoid reconciling against stale or deleted resources.

Reconcile implementation (fetch and handle not-found)

* Obtain a logger from the context and store it in a real variable.
* Create an empty `webapp` variable of type `webappv1.WebApp` which the client will populate.
* Call the reconciler's `Get` with `req.NamespacedName` and a pointer to that variable.
* Treat "not found" as a normal condition (object deleted after the request was queued) using `client.IgnoreNotFound(err)`. Return real errors for other failure cases.

```go theme={null}
// For more details, check Reconcile and its Result here:
// https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.23.3/pkg/reconcile
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    // Create an empty WebApp object that will be populated by the client.
    var webapp webappv1.WebApp

    // Fetch the WebApp instance from the API server.
    if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
        // Ignore not-found errors (deleted after reconcile request). Return other errors.
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // TODO: your reconciliation logic here (e.g., ensure child resources reflect webapp.Spec)

    return ctrl.Result{}, nil
}
```

Quick summary of the core steps

| Step            | Purpose                                                  | Example / Notes                                    |
| --------------- | -------------------------------------------------------- | -------------------------------------------------- |
| Obtain logger   | Capture structured logger from context for the reconcile | `log := logf.FromContext(ctx)`                     |
| Allocate object | Prepare zero-valued CR instance to be populated          | `var webapp webappv1.WebApp`                       |
| Read from API   | Fetch live resource using the reconcile key              | `r.Get(ctx, req.NamespacedName, &webapp)`          |
| Handle missing  | Treat a deleted resource as a normal condition           | `return ctrl.Result{}, client.IgnoreNotFound(err)` |

Register the controller with the manager

* The generated `SetupWithManager` wires the reconciler to watch `webappv1.WebApp` objects. This ensures your reconciler gets called whenever the API server reports changes to those CRs.

```go theme={null}
// SetupWithManager sets up the controller with the Manager.
func (r *WebAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&webappv1.WebApp{}).
        Named("webapp").
        Complete(r)
}
```

> **lightbulb** Use `client.IgnoreNotFound(err)` to treat deleted objects as a normal condition. That prevents your controller from requeuing errors for resources that no longer exist.

Build and test locally

* Run the full project build to catch missing imports, typos, and invalid syntax before running the controller:

```bash theme={null}
go build ./...
```

* Start the manager and apply a sample WebApp manifest. Verify the controller logs show the expected fields (for example, `image` and `replicas`) — that indicates the initial reconcile step is functioning.

Useful links and references

* controller-runtime Reconcile docs: [https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.23.3/pkg/reconcile](https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.23.3/pkg/reconcile)
* Kubebuilder docs: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* controller-runtime client API: [https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.23.3/pkg/client](https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.23.3/pkg/client)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/a47e78e1-626a-4375-b8a2-3780e4560437)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/1e4a2132-3a94-4b40-ba14-c2a8046e2728)
