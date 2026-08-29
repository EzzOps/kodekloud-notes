# Lab Solution Install The CRD And Run The Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Lab-Solution-Install-The-CRD-And-Run-The-Operator/page

Installing a Kubernetes CRD and running a Kubebuilder operator locally, generating code and manifests, building the manager, and verifying controller registration and sample custom resource

In this lesson you'll install the CustomResourceDefinition (CRD) into your cluster and run the operator locally using the initial Kubebuilder-generated reconcile stub. The focus is on wiring the build pipeline, registering the CRD with the API server, and confirming that the manager starts cleanly and that the controller is registered. The reconciler still returns an empty result in this lab, so no child resources are created yet — later you can extend it to create a Deployment, Service, and ConfigMap.

Work from the WebApp operator project root directory. Every Make target reads the local Makefile and project files, so running commands from elsewhere may fail.

<Callout icon="lightbulb">
  Always run the commands from the operator project root so `make` targets, generated code, and file paths resolve correctly.
</Callout>

## 1) Verify the API types

Open the WebApp types file (usually under `api/v1` or similar) and confirm `spec` and `status` fields are present. The starter project includes `Image` and `Replicas` on `WebAppSpec`. Confirm these fields and their kubebuilder markers are present:

```go theme={null}
// WebAppSpec defines the desired state of WebApp
type WebAppSpec struct {
	// +kubebuilder:validation:Required
	Image string `json:"image"`

	// +kubebuilder:default=1
	Replicas int32 `json:"replicas,omitempty"`
}

// WebAppStatus defines the observed state of WebApp.
type WebAppStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "make" to regenerate code after modifying this file
}
```

Also ensure your file contains the resource markers for the API root, object, and the status subresource when applicable. These markers drive CRD generation.

## 2) Controller reconcile stub

This lab keeps the Kubebuilder-generated reconcile stub. It returns an empty result and no error, so the controller registers and the manager starts, but no child resources are created yet.

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	// TODO(user): your logic here
	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *WebAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&webappv1.WebApp{}).
		Named("webapp").
		Complete(r)
}
```

The controller being registered with the manager is sufficient for compilation and for the manager to start a worker for the `WebApp` kind.

## 3) Boilerplate and package imports

Ensure your controller package includes the standard license header, package declaration, and necessary imports (context, runtime, Kubernetes client packages etc.). For example:

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
	"k8s.io/apimachinery/pkg/runtime"
	// other imports...
)
```

If you modify imports or types, re-run generation to update deepcopy and other generated files.

## 4) Build pipeline: generate, manifests, build

Run these Make targets to produce generated code, the CRD YAML, and the manager binary:

* `make generate` — runs `controller-gen` to regenerate deepcopy, conversions, and other generated code to reflect your types and kubebuilder markers.
* `make manifests` — renders the CRD YAML and RBAC manifests from your Go markers.
* `make build` — compiles the manager binary.

Summary of common build commands:

| Make target | Purpose                                         | Example          |
| ----------- | ----------------------------------------------- | ---------------- |
| `generate`  | Regenerate deepcopy and other generated Go code | `make generate`  |
| `manifests` | Render CRD and RBAC YAMLs from markers          | `make manifests` |
| `build`     | Compile the operator/controller binary          | `make build`     |

Example invocation of `make generate` in the lab environment:

```bash theme={null}
$ make generate "/home/student/work/labs/bin/controller-gen" object:headerFile="hack/boilerplate.go.txt",year=2026 paths="."
```

## 5) Install the CRD

Apply the generated CRD YAML into your Kubernetes cluster with:

```bash theme={null}
$ make install
```

Then verify the CRD exists:

```bash theme={null}
$ kubectl get crd webapps.webapp.kodekloud.com
```

A successful response confirms the CRD was applied and registered in the API server.

## 6) Run the controller locally

Start the manager locally to verify the operator connects to the API server and the controller registers. The demos used `make run`, but running the main package directly allows customizing probe and metrics ports. The example below disables the metrics endpoint and moves the health probe to port `:8082`:

```bash theme={null}
$ go run ./cmd/main.go --health-probe-bind-address=:8082 --metrics-bind-address=0
```

Expected startup log snippets:

```bash theme={null}
2026-06-05T19:53:31+00:00 INFO    setup    Starting manager
2026-06-05T19:53:31+00:00 INFO    starting server {"name": "health probe", "addr": "[::]:8082"}
2026-06-05T19:53:31+00:00 INFO    Starting EventSource    {"controller": "webapp", "controllerGroup": ""}
2026-06-05T19:53:31+00:00 INFO    Starting Controller    {"controller": "webapp", "controllerGroup": ""}
2026-06-05T19:53:31+00:00 INFO    Starting workers    {"controller": "webapp", "controllerKind": "WebApp", "worker count": 1}
```

The "Starting workers" line indicates the manager successfully registered the controller and started its worker(s).

## 7) Apply sample namespace and CR

Create the demo namespace and apply the sample WebApp CustomResource. Because the reconciler is currently a no-op, the CR will be accepted by the API server but will not trigger creation of child resources.

Apply the namespace and sample resource:

```bash theme={null}
$ kubectl apply -f webapp-demo-namespace.yaml
namespace/webapp-demo created

$ kubectl apply -f webapp-sample.yaml
webapp.webapp.kodekloud.com/site created
```

Verify the CR's spec fields using JSONPath. The sample resource sets `image: nginx` and `replicas: 2`:

```bash theme={null}
$ kubectl -n webapp-demo get webapp site -o jsonpath='{.spec.image}'
nginx

$ kubectl -n webapp-demo get webapp site -o jsonpath='{.spec.replicas}'
2
```

These checks confirm:

* the CRD is installed,
* the API server accepted and stored the CustomResource,
* and your operator is running and watching the API server.

## 8) Summary

After completing this lab you have the operator scaffolding wired up and validated:

* Types and generated code are present and up-to-date.
* CRD YAML was generated and registered in the API server.
* Manager started locally and exposes probes as configured.
* Controller is registered and worker(s) started.
* A sample WebApp CustomResource was accepted and can be queried.

Next steps: implement the reconcile function to perform desired actions (e.g., create a Deployment, Service, and ConfigMap based on the `WebApp` spec), add status updates, and include appropriate RBAC rules for the created resources.

## Links and references

* [Kubernetes Concepts: Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* [Kubebuilder Book](https://book.kubebuilder.io/)
* [controller-runtime documentation](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/a59c9831-1bc2-49c9-86c4-15fa3b632341" />
</CardGroup>
