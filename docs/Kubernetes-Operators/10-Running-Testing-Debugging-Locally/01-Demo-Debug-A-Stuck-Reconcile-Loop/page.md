# Demo Debug A Stuck Reconcile Loop

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Running-Testing-Debugging-Locally/Demo-Debug-A-Stuck-Reconcile-Loop/page

Guides debugging a Kubernetes controller stuck reconcile loop caused by using metadata.resourceVersion in Deployment selectors, showing reproduction, log analysis, root cause, and fix to use stable selectors

A stuck controller is easiest to diagnose if you treat it like a detective case. The cluster leaves footprints; follow them from a noisy symptom to the root cause. This guide walks through a real example: reproduce the failure, collect evidence, locate the rejection in the API server, understand the root cause, and apply a targeted fix.

## Reconcile implementation (shortened)

Start with a representative Reconcile method (only the relevant parts are shown):

```go theme={null}
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	var webapp webappv1.WebApp
	if err := r.Get(ctx, req.NamespacedName, &webapp); err != nil {
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	desiredDeploy := deploymentFor(&webapp)
	selectorUsesResourceVersion := desiredDeploy.Spec.Selector.MatchLabels["rv"] != ""
	if err := controllerutil.SetControllerReference(&webapp, desiredDeploy, r.Scheme); err != nil {
		return ctrl.Result{}, err
	}

	foundDeploy := &appsv1.Deployment{}
	err := r.Get(ctx, types.NamespacedName{Name: desiredDeploy.Name, Namespace: desiredDeploy.Namespace}, foundDeploy)
	if apierrs.IsNotFound(err) {
		log.Info("creating Deployment", "name", desiredDeploy.Name)
		if err := r.Create(ctx, desiredDeploy); err != nil {
			return ctrl.Result{}, err
		}
	} else if err != nil {
		return ctrl.Result{}, err
	}

	// ...rest of reconcile...
	return ctrl.Result{}, nil
}
```

A single bad label in the controller can produce a noisy reconcile loop. The manager and controller processes may be running, but repeatedly failing reconciliation—like an engine running while a car is stuck in the mud.

## Example of a buggy helper that builds a Deployment

This helper injects the WebApp's `metadata.resourceVersion` into labels used for both the Deployment selector and the Pod template. Because `resourceVersion` changes on every write, the controller will generate a different selector on each pass:

```go theme={null}
func deploymentFor(webapp *webappv1.WebApp) *appsv1.Deployment {
	selectorLabels := map[string]string{"app": webapp.Name, "rv": webapp.ResourceVersion}
	templateLabels := map[string]string{"app": webapp.Name, "rv": webapp.ResourceVersion}
	replicas := webapp.Spec.Replicas

	return &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      webapp.Name,
			Namespace: webapp.Namespace,
			Labels:    map[string]string{"app": webapp.Name},
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: selectorLabels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: templateLabels,
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  "app",
							Image: webapp.Spec.Image,
						},
					},
				},
			},
		},
	}
}
```

Injecting a changing field into a selector or any API field that is immutable triggers repeated update attempts and API rejections.

## Reproduce and capture logs

Start the manager with debug logging and capture the output. The live terminal shows what is happening now; the saved file is your evidence bag to grep through later.

Example manager startup logs (captured):

```text theme={null}
2026-06-09T23:21:31+02:00 INFO  Starting EventSource  {"controller": "webapp", "controllerGroup": "webapp.kodekloud.com", "controllerKind": "WebApp", "source": "kind source: *v1.Service"}
2026-06-09T23:21:31+02:00 INFO  Starting EventSource  {"controller": "webapp", "controllerGroup": "webapp.kodekloud.com", "controllerKind": "WebApp", "source": "kind source: *v1.ConfigMap"}
2026-06-09T23:21:31+02:00 INFO  Starting EventSource  {"controller": "webapp", "controllerGroup": "webapp.kodekloud.com", "controllerKind": "WebApp", "source": "kind source: *v1.Deployment"}
2026-06-09T23:21:32+02:00 INFO  Starting Controller   {"controller": "webapp", "controllerGroup": "webapp.kodekloud.com", "controllerKind": "WebApp"}
2026-06-09T23:21:32+02:00 INFO  Starting workers      {"controllerKind": "WebApp", "worker count": 1}
```

Apply the sample CR so the controller has a single object to reconcile:

```bash theme={null}
$ kubectl apply -f config/samples/webapp_v1_webapp.yaml
webapp.webapp.kodekloud.com/demo created
$ kubectl get webapp demo -o custom-columns=NAME:.metadata.name,IMAGE:.spec.image,REPLICAS:.spec.replicas
NAME    IMAGE   REPLICAS
demo    nginx   2
$ kubectl get webapp demo -w -o custom-columns=NAME:.metadata.name,IMAGE:.spec.image,REPLICAS:.spec.replicas
```

Watch `metadata.generation` and `metadata.resourceVersion` side by side:

* `generation` reflects user intent (changes to spec).
* `resourceVersion` reflects cluster record changes.

If `generation` remains at 1 while `resourceVersion` keeps increasing, the controller is repeatedly writing the object—often a sign the controller is causing the writes.

Measure the noisy reconcile behavior with a quick grep of the operator log:

```bash theme={null}
$ grep -c 'Reconciling WebApp' /tmp/op.log; sleep 5; grep -c 'Reconciling WebApp' /tmp/op.log
5512
5822
```

Now search the debug log for Deployment updates or API errors (case-insensitive):

```bash theme={null}
$ grep -iE 'deployment|invalid|forbidden' /tmp/op.log | tail -20
```

You want to find API rejection messages such as "field is immutable" which indicate the controller attempted an invalid update.

<Frame>
  <img alt="The image shows a Visual Studio Code window with a terminal output displaying an error related to a Kubernetes deployment. The error message indicates an issue with an immutable field in a deployment configuration." />
</Frame>

## The failure in the logs

The top-level INFO logs look fine, but the debug/ERROR lines contain the root failure:

```text theme={null}
2026-06-09T23:24:41+02:00 INFO  updating Deployment  {"controller":"webapp","controllerGroup":"webapp.kodekloud.com","controllerKind":"WebApp","WebApp":{"name":"demo","namespace":"default"},"namespace":"default","name":"demo","reconcileID":"d453efbe-ce60-4993-84b1-d82a2e93d3ca","webapp":"default/demo"}
2026-06-09T23:24:29+02:00 ERROR update failed      {"controller":"webapp","controllerGroup":"webapp.kodekloud.com","controllerKind":"WebApp","WebApp":{"name":"demo","namespace":"default"},"namespace":"default","name":"demo","reconcileID":"d453efbe-ce60-4993-84b1-d82a2e93d3ca","error":"Deployment.apps \"demo\" is invalid: spec.selector: Invalid value: {matchLabels:{\"app\":\"demo\"}}: field is immutable"}
```

Root cause: the controller uses the changing `metadata.resourceVersion` in the Deployment selector. Since Kubernetes treats `spec.selector` as immutable after creation, each reconcile tries to update the selector to a new value and the API rejects it.

## Fix: make selectors stable

Stop feeding a changing value into a stable identity field. Remove `resourceVersion` (or any other constantly changing value) from the Deployment `spec.selector` and ensure the pod template labels are stable and match the selector.

Corrected helper (no `resourceVersion` in selector or pod labels):

```go theme={null}
func deploymentFor(webapp *webappv1.WebApp) *appsv1.Deployment {
	selectorLabels := map[string]string{"app": webapp.Name}
	templateLabels := map[string]string{"app": webapp.Name}
	replicas := webapp.Spec.Replicas

	return &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      webapp.Name,
			Namespace: webapp.Namespace,
			Labels:    map[string]string{"app": webapp.Name},
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: selectorLabels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: templateLabels,
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  "app",
							Image: webapp.Spec.Image,
						},
					},
				},
			},
		},
	}
}
```

## Apply the fix safely (recommended procedure)

1. Stop the manager.
2. Edit the controller code to remove changing values from selectors/template labels.
3. Rebuild and restart the manager.
4. Observe operator logs and the WebApp resource; the reconcile count should drop to normal levels.

If you prefer to recreate the Deployment after code changes, you can delete the problematic Deployment first and let the controller create a correct one after restart:

```bash theme={null}
$ kubectl delete deployment demo --ignore-not-found
deployment.apps "demo" deleted
$ kubectl get webapp demo -w -o custom-columns=NAME:.metadata.name,RV:.metadata.resourceVersion,GEN:.metadata.generation
NAME   RV      GEN
demo   12721   1
```

When the symptom (rapid reconciling with failing updates) stops and the controller performs normal reconciles, the case is closed.

<Callout icon="warning">
  Important: Never put a changing cluster-controlled value (such as `metadata.resourceVersion`) into a Deployment selector or any field that the API treats as immutable. Doing so will repeatedly trigger rejected updates and a tight reconcile loop.
</Callout>

## Quick triage checklist

| Symptom                                                                | Probable cause                                                                                 | Quick action                                                                                           |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Rapid reconcile count while `metadata.generation` unchanged            | Controller is updating resources repeatedly (e.g., using `resourceVersion` in selector/labels) | Search logs for API rejections (`field is immutable`, `invalid`) and inspect generated desired objects |
| Logs show `field is immutable` for `spec.selector`                     | Selector was changed by the controller after resource creation                                 | Remove dynamic values from selector; ensure pod template labels and selector are stable                |
| Controller INFO logs look normal, but resourceVersion keeps increasing | Controller is writing to the object on each reconcile                                          | Compare `generation` vs `resourceVersion`; trace what fields the controller sets                       |

## Root cause summary

<Callout icon="lightbulb">
  Root cause summary: never place a changing cluster-controlled value (like `metadata.resourceVersion`) into a Deployment selector (or any field that the API treats as immutable). Keep selectors stable and match them to pod template labels that do not change across reconciles.
</Callout>

The debugging pattern matters more than any single fix:

* Start with the symptom.
* Separate user intent (`generation`) from controller writes (`resourceVersion`).
* Measure the behavior.
* Search logs for API refusals.
* Be suspicious when a stable identity field is fed changing data.

## Links and references

* [Kubernetes API conventions – Object Metadata](https://kubernetes.io/docs/reference/using-api/api-concepts/#resources)
* [Deployments — Immutable fields](https://kubernetes.[SECRET_REDACTED]/#updating-a-deployment)
* Controller-runtime docs: [https://pkg.go.dev/sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/10f8df25-089f-4e04-af70-b608d1773818" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/245c1684-705c-4a53-9f56-897dfaf25c71/lesson/222c5ab1-448e-4fad-bbdf-909bc0daa420" />
</CardGroup>
