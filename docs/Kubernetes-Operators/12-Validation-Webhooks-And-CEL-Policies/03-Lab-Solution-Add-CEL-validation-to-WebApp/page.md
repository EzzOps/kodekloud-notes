# config/samples/bad-latest-webapp.yaml
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: bad-latest
  namespace: webapp-demo
spec:
  image: nginx:latest
```

```bash theme={null}
$ kubectl apply -f config/samples/bad-latest-webapp.yaml
The webapps "bad-latest" is invalid: ValidatingAdmissionPolicy 'webapp-validation' with binding 'webapp-validation-binding' denied request: spec.image must not use ':latest'
```

The API server denies the request with the image rule message — proof the CEL policy ran at admission-time.

2. Apply a WebApp with an acceptable image but invalid replicas (50):

```yaml theme={null}
# config/samples/bad-replicas-webapp.yaml
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
$ kubectl apply -f config/samples/bad-replicas-webapp.yaml
The webapps "bad-replicas" is invalid: ValidatingAdmissionPolicy 'webapp-validation' with binding 'webapp-validation-binding' denied request: spec.replicas must be between 1 and 10, got 50
```

The denial message includes the rejected replica count, thanks to the configured `messageExpression`.

3. Apply a WebApp that satisfies both rules (pinned image and valid replicas):

```yaml theme={null}
# config/samples/good-webapp.yaml
apiVersion: webapp.kodekloud.com/v1
kind: WebApp
metadata:
  name: good-webapp
  namespace: webapp-demo
spec:
  image: nginx:1.27
  replicas: 3
```

```bash theme={null}
$ kubectl apply -f config/samples/good-webapp.yaml
webapp.webapp.kodekloud.com/good-webapp created
```

Same CRD and controller — but the API server now prevents invalid desired state from entering the system, reducing wasted controller processing and improving feedback to API clients.

Inspecting policy status:

```bash theme={null}
$ kubectl get validatingadmissionpolicy webapp-validation -o jsonpath='{.status}'
```

When to use validating admission policies with CEL:

* Good for centralized, fast checks on object-local properties: image tag pinning, numeric bounds, required labels/annotations, simple string patterns.
* Not intended for complex business logic that requires cross-resource checks or external calls — those belong in controllers or external admission webhooks.

References:

* [Validating Admission Policy API (admissionregistration.k8s.io)](https://kubernetes.io/docs/reference/validation/)
* [Kubernetes Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [Common Expression Language (CEL) — specification](https://opensource.google/docs/cel/spec/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/06ac03ac-518a-4bc6-b2f8-6ed63fcb26d5/lesson/5de52805-a91c-4d75-b5f3-538d09c68779)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/06ac03ac-518a-4bc6-b2f8-6ed63fcb26d5/lesson/e511ca5d-b23f-4037-873e-9b377026af20)


# Lab Solution Add CEL validation to WebApp

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Validation-Webhooks-And-CEL-Policies/Lab-Solution-Add-CEL-validation-to-WebApp/page

Adds a Kubernetes ValidatingAdmissionPolicy using CEL to block images with latest tag and enforce WebApp replicas between 1 and 10

Validation is the API-server gatekeeper for writes to the cluster. In this lesson we add two WebApp validation rules at that gate using a ValidatingAdmissionPolicy backed by CEL expressions:

* Deny images that use the floating `:latest` tag.
* Deny explicit replica counts outside the supported range (1–10). The `replicas` field is optional for the WebApp API, so omission remains allowed.

These checks are implemented in two pieces:

1. A `ValidatingAdmissionPolicy` that describes which resources to match and contains the CEL expressions.
2. A `ValidatingAdmissionPolicyBinding` that attaches the policy and selects the enforcement action. Here the enforcement action is `Deny`, so any failed expression blocks the write before the object is stored.

> **lightbulb** A policy without a binding is like a rule written down but not posted at the door — it won't be enforced until it is bound.

## What this policy enforces

* Image rule: prevents images that explicitly end with `:latest`. The expression allows the `image` field to be omitted, or if present requires it not to end with `:latest`.
* Replicas rule: allows omitting `replicas`, or if present requires its value to be an integer between 1 and 10 inclusive.

Summary table

| Validation | Purpose                                         | CEL expression                                                                              |
| ---------: | ----------------------------------------------- | ------------------------------------------------------------------------------------------- |
|      Image | Deny images tagged `:latest`, allow omission    | `!has(object.spec.image) \|\| !object.spec.image.endsWith(':latest')`                       |
|   Replicas | Allow omission or require `1 <= replicas <= 10` | `!has(object.spec.replicas) \|\| (object.spec.replicas >= 1 && object.spec.replicas <= 10)` |

## ValidatingAdmissionPolicy

This resource matches `webapps.webapp.kodekloud.com/v1` on `CREATE` and `UPDATE` and contains the two CEL validations shown below:

```yaml theme={null}
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: webapp-validation
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
      - apiGroups: ["webapp.kodekloud.com"]
        apiVersions: ["v1"]
        operations: ["CREATE", "UPDATE"]
        resources: ["webapps"]
  validations:
    - expression: "!has(object.spec.image) || !object.spec.image.endsWith(':latest')"
      message: "image must not use the :latest tag"
    - expression: "!has(object.spec.replicas) || (object.spec.replicas >= 1 && object.spec.replicas <= 10)"
      message: "replicas must be between 1 and 10"
```

Notes:

* `failurePolicy: Fail` means the admission request is rejected on policy evaluation errors.
* The CEL `has()` check lets the field be optional; only present values are evaluated against the constraint.

> **warning** Ensure your cluster supports `ValidatingAdmissionPolicy` resources in `admissionregistration.k8s.io/v1` before applying these manifests. Cluster feature availability can vary by Kubernetes distribution and version.

## ValidatingAdmissionPolicyBinding

Bind the policy and set enforcement to `Deny` so failed validations block writes:

```yaml theme={null}
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: webapp-validation-binding
spec:
  policyName: webapp-validation
  enforcementAction: "Deny"
```

## Apply the policy and confirm

Apply the policy and binding, then verify both exist:

```bash theme={null}
$ kubectl apply -f webapp-policy.yaml
validatingadmissionpolicy.admissionregistration.k8s.io/webapp-validation created
validatingadmissionpolicybinding.admissionregistration.k8s.io/webapp-validation-binding created

$ kubectl get validatingadmissionpolicy webapp-validation
NAME                VALIDATIONS   PARAMKIND   AGE
webapp-validation   2             <unset>     20s

$ kubectl get validatingadmissionpolicybinding webapp-validation-binding
NAME                        POLICYNAME            PARAMREF   AGE
webapp-validation-binding   webapp-validation     <unset>    37s
```

These commands confirm both halves are in place and the binding is active.

## Test resources

Use the following example manifests to validate policy behavior.

1. Test: image with `:latest` should be rejected

```yaml theme={null}
