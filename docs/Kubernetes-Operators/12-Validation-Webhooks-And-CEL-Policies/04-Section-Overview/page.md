# bad-latest.yaml
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: bad-latest
  namespace: webapp-demo
spec:
  image: nginx:latest
  replicas: 2
```

```bash theme={null}
$ kubectl apply -f bad-latest.yaml
The webapps "bad-latest" is invalid: ValidatingAdmissionPolicy 'webapp-validation' with binding 'webapp-validation-binding' denied request: image must not use the :latest tag
```

The denial happens at the API server before any controller reconciles the object.

2. Test: replicas outside allowed range should be rejected

```yaml theme={null}
# bad-replicas.yaml
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: bad-replicas
  namespace: webapp-demo
spec:
  image: nginx:1.27
  replicas: 50
```

```bash theme={null}
$ kubectl apply -f bad-replicas.yaml
The webapps "bad-replicas" is invalid: ValidatingAdmissionPolicy 'webapp-validation' with binding 'webapp-validation-binding' denied request: replicas must be between 1 and 10
```

3. Test: valid WebApp should be accepted

```yaml theme={null}
# shop.yaml
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: shop
  namespace: webapp-demo
spec:
  image: nginx:1.27
  replicas: 3
```

```bash theme={null}
$ kubectl apply -f shop.yaml
webapp.webapp.kodekloud.com/shop created
```

This demonstrates the policy blocks unsafe cases while allowing valid objects.

## Links and references

* [Kubernetes Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [ValidatingAdmissionPolicy API reference (admissionregistration.k8s.io)](https://kubernetes.io/docs/reference/generated/kubernetes-api/latest/)
* [Common Expression Language (CEL) for Kubernetes](https://kubernetes.io/docs/reference/strategy/expressions/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/06ac03ac-518a-4bc6-b2f8-6ed63fcb26d5/lesson/c541f201-dbde-4b6d-8b13-df799e55b753)


# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Validation-Webhooks-And-CEL-Policies/Section-Overview/page

Using Kubernetes ValidatingAdmissionPolicy with CEL to reject invalid WebApp resources by enforcing image tag immutability and replica count limits before controllers reconcile.

Kubernetes operators focus on reconciliation: creating child objects, reporting status, emitting events, and cleaning up external state when a custom resource is deleted. Those reconciliation behaviors occur after a WebApp custom resource already exists in the API server—typically after you run:

```bash theme={null}
kubectl apply -f webapp.yaml
```

Validating admission moves part of that safety boundary earlier, so Kubernetes can reject an invalid WebApp before it ever reaches the controller. The Kubernetes feature used here is ValidatingAdmissionPolicy: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionpolicy](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionpolicy)

A validating admission policy executes during admission—the API server step that inspects create and update requests before persisting them. Policies are written with CEL (Common Expression Language) to evaluate expressions against the object in the incoming request. For a custom resource like WebApp, the API server can evaluate fields such as `spec.image` and `spec.replicas` before the controller ever sees the object.

If a CEL expression evaluates to true, the API server may allow the request to continue. If it evaluates to false and the associated binding enforces `deny`, the API server rejects the request and returns the policy's validation message.

<Frame>
  <img alt="The image illustrates a decision process titled &#x22;The Verdict: Allow or Deny,&#x22; where &#x22;CEL evaluates&#x22; requests. If true, the request continues; if false, the API server rejects the request." />
</Frame>

A policy defines the validation logic, matching constraints, and the message returned on failure. A separate binding activates the policy and chooses the enforcement action and scope (namespaces, users, operations). This separation lets you stage policies in the cluster without affecting requests until a binding is applied.

For the WebApp API in this demo, we enforce two object-level checks using CEL:

* Images must not use the mutable `:latest` tag, because moving tags reduce repeatability and make rollouts unpredictable.
* Explicit replica counts must be within a supported range so extreme values are rejected before the controller begins reconciling.

Example CEL expressions for these checks:

```plaintext theme={null}
