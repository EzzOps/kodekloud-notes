# Build the controller
go build ./...

# Apply a sample WebApp YAML
kubectl apply -f config/samples/webapp_v1_webapp.yaml

# Verify the controller created the ConfigMap by label
kubectl get cm -l app=webapp-sample
```

Example output:

```bash theme={null}
$ kubectl apply -f config/samples/webapp_v1_webapp.yaml
webapp.webapp.kodekloud.com/webapp-sample created
$ kubectl get cm -l app=webapp-sample
NAME                     DATA   AGE
webapp-sample-config     1      20s
```

Summary
This pattern is reusable for other child types (Secrets, Services, etc.). The key steps are: construct the desired child object, set the owner reference so the parent controls lifecycle and ownership, Get the existing child, Create if missing, and return errors to allow controller-runtime to requeue and retry.

> **lightbulb** ConfigMaps are namespaced. Always set the child's `Namespace` to the parent's namespace and set the controller reference so garbage collection and ownership are handled correctly.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/1b686f11-43b3-42b9-b57b-2c3cca6a4dea)


# Demo Add The Service Builder

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Demo-Add-The-Service-Builder/page

Adds a Kubernetes Service builder and wires it into a WebApp controller reconcile loop so the controller creates and manages ClusterIP services routing port 80 to pods

The web app controller already creates a Deployment and a ConfigMap. The final child we need is a Service, which gives the pods a stable cluster-internal DNS name and a single network entry point for other components to reach the WebApp.

In this lesson we will:

* Add a helper named `serviceFor` that builds a `*corev1.Service` for a given `WebApp`.
* Wire that helper into the reconciler so the controller creates a Service when it does not exist.

Below are the authoritative code examples and the reconcile pattern used by the controller.

Why this matters: A Kubernetes Service provides stable networking for a set of pods selected by labels. A controller must construct the desired Service, attach an owner reference (so child resources are garbage-collected when the parent is removed), check if the Service already exists, and create it if the API returns `NotFound`. This is the same pattern used for ConfigMaps and Deployments.

Context — existing ConfigMap helper

```go theme={null}
func configMapFor(w *webappv1.WebApp) *corev1.ConfigMap {
	return &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name:      w.Name + "-config",
			Namespace: w.Namespace,
			Labels:    map[string]string{"app": w.Name},
		},
		Data: map[string]string{
			"welcome.html": "<h1>Hello from " + w.Name + "</h1>",
		},
	}
}
```

Add the Service helper

* Use the same `app` label as the other children so the Service can select the same pods.
* Set Service `Type` to `ClusterIP`.
* Expose port `80` and route it to container port `80` with TCP.

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
					Protocol:   corev1.ProtocolTCP,
				},
			},
		},
	}
}
```

> **lightbulb** The Service `selector` must exactly match the labels applied to the Deployment's Pod template. If these labels differ, the Service will be present but will not route traffic to any pods.

Wire the Service creation into Reconcile
Follow the same reconcile pattern used for the ConfigMap and Deployment:

1. Build the desired object (`serviceFor`).
2. Attach a controller owner reference with `controllerutil.SetControllerReference`.
3. Attempt to `Get` the object.
4. If `Get` returns `apierrors.IsNotFound`, `Create` the object.
5. Handle other errors appropriately.

Complete reconcile snippet (reads the `WebApp`, ensures ConfigMap and Service exist):

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	var webapp webappv1.WebApp
	if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
		if apierrors.IsNotFound(err) {
			// Resource not found; it might have been deleted after the reconcile request.
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	// Ensure ConfigMap
	desiredCM := configMapFor(&webapp)
	if err := controllerutil.SetControllerReference(&webapp, desiredCM, r.Scheme); err != nil {
		return ctrl.Result{}, err
	}

	foundCM := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: desiredCM.Name, Namespace: desiredCM.Namespace}, foundCM)
	if apierrors.IsNotFound(err) {
		log.Info("creating ConfigMap", "name", desiredCM.Name)
		if err := r.Create(ctx, desiredCM); err != nil {
			return ctrl.Result{}, err
		}
	} else if err != nil {
		return ctrl.Result{}, err
	}

	// Ensure Service
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

	// Continue with other reconcile steps (Deployment, status, etc.)
	return ctrl.Result{}, nil
}
```

Build and run the controller

```bash theme={null}
$ go build
$ make run
```

Typical startup logs

```text theme={null}
{"controller": "webapp", "controllerGroup": "webapp.kedloud.com", "controllerKind": "WebApp", "source": "*v1.WebApp"}
2026-06-07T11:02:28+02:00  INFO     Starting Controller
{"controller": "webapp", "controllerGroup": "webapp.kedloud.com", "controllerKind": "WebApp"}
2026-06-07T11:02:28+02:00  INFO     Starting workers
{"controller": "webapp", "controllerGroup": "webapp.kedloud.com", "controllerKind": "WebApp", "worker count": 1}
```

Apply your sample custom resource

```bash theme={null}
$ kubectl apply -f config/samples/webapp_v1_webapp.yaml
```

Verify the children were created
Use the `app` label to list the Deployment, Service, and ConfigMap created by a single `WebApp` resource:

```bash theme={null}
$ kubectl get deployments,services,configmaps -l app=<your-webapp-name>
```

If you see entries for the Deployment, Service, and ConfigMap, the controller successfully executed the reconcile pattern: build desired objects, attach owner references, check for existence, and create missing children.

Resources and references

* [Kubernetes Services overview](https://kubernetes.io/docs/concepts/services-networking/service/)
* [controller-runtime: OwnerReferences and controllerutil](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
* [Kubernetes Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

Summary table

| Resource Type | Purpose                            | Example / Note                                                     |
| ------------- | ---------------------------------- | ------------------------------------------------------------------ |
| Deployment    | Runs application pods              | `spec.template.metadata.labels = map[string]string{"app": w.Name}` |
| Service       | Stable network endpoint for pods   | `type: ClusterIP`, `ports: 80 -> targetPort 80`                    |
| ConfigMap     | Stores configuration/data for pods | `name: w.Name + "-config"`                                         |

This completes adding a Service builder and wiring it into the reconcile loop so the WebApp controller manages Service lifecycle along with its other children.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/f0f094bb-15eb-4a9a-987c-2c803c3d37c4)
