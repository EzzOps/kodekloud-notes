# Disallow :latest tags
!object.spec.image.endsWith(':latest')
```

```cel theme={null}
# Allow missing replicas, otherwise require 1..10
!has(object.spec.replicas) || (object.spec.replicas >= 1 && object.spec.replicas <= 10)
```

Enforcement modes

* `deny`: blocks requests that fail the CEL check.
* `warn`: allows the request but surfaces a warning to clients.
* `audit`: records violations (useful for monitoring and rollout).

Start with `warn` or `audit` when introducing a new policy to observe cluster impact before switching to `deny`.

<Frame>
  <img alt="The image shows two boxes titled &#x22;Warn&#x22; and &#x22;Audit&#x22; with brief descriptions under a section called &#x22;Softer Modes: Warn and Audit.&#x22; There is also a note about observing violations before fully enforcing." />
</Frame>

When to use CEL — and when not to
CEL is a strong fit for concise, object-local rules that can be expressed as pure predicates. It is not a general-purpose programming extension for the API server: do not attempt side effects, external network calls, or large workflows inside CEL.

<Callout icon="warning">
  Do not use CEL for checks that require external API calls, side effects, or complex business logic. For those cases, implement a custom validating webhook or another admission design that can perform network calls and richer processing.
</Callout>

<Frame>
  <img alt="The image outlines the boundaries of CEL, indicating it's a &#x22;Good fit&#x22; for clear expressions and object-local checks, but &#x22;Not a programming extension&#x22; for tasks involving side effects, external calls, or large workflows." />
</Frame>

Quick demo: apply a CEL-based validating admission policy for the webapp CRD

```bash theme={null}
$ kubectl apply -f webapp-policy.yaml
validatingadmissionpolicy/webapp-rules created
```

The objective is to have Kubernetes reject unsafe webapp requests before they are stored in the API server.

References and further reading

* CEL spec: [https://github.com/google/cel-spec](https://github.com/google/cel-spec)
* Kubernetes Admission Controllers overview: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* ValidatingAdmissionPolicy docs: [https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#validatingadmissionpolicy](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#validatingadmissionpolicy)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/06ac03ac-518a-4bc6-b2f8-6ed63fcb26d5/lesson/33941c74-e52c-489e-a74d-e752fc4a54cf" />
</CardGroup>


# Demo Add A CEL Validation Policy

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Validation-Webhooks-And-CEL-Policies/Demo-Add-A-CEL-Validation-Policy/page

How to add a Kubernetes ValidatingAdmissionPolicy using CEL to validate WebApp resources, enforcing image tag pinning and replica bounds at admission time

In this lesson we'll add admission-time validation for a custom WebApp resource by authoring a ValidatingAdmissionPolicy that evaluates CEL expressions. The WebApp controller itself does not change — instead the policy executes inside the API server and decides whether CREATE/UPDATE requests are allowed before objects are persisted.

Create the ValidatingAdmissionPolicy that targets the WebApp resource. Note the API version `admissionregistration.k8s.io/v1`, which is the Kubernetes API group that defines validating admission policies.

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
    - expression: "!object.spec.image.endsWith(':latest')"
      message: "spec.image must not use ':latest'"
    - expression: "!has(object.spec.replicas) || (object.spec.replicas >= 1 && object.spec.replicas <= 10)"
      message: "spec.replicas must be between 1 and 10"
      messageExpression: "'spec.replicas must be between 1 and 10, got ' + string(object.spec.replicas)"
```

<Callout icon="lightbulb">
  Using `failurePolicy: Fail` ensures that if the policy cannot be evaluated, or a validation fails, the API server will block the matching request rather than allowing it to proceed silently.
</Callout>

Policy fields — concise explanation:

* `matchConstraints.resourceRules` — scopes the policy so it only evaluates requests for the `webapps` resource in the `webapp.kodekloud.com/v1` API group during `CREATE` and `UPDATE` operations.
* `validations` — an array of CEL expressions that must evaluate to true for the request to be allowed. The incoming object is available in CEL as `object`.
  * First validation:
    * Expression: `!object.spec.image.endsWith(':latest')`\
      This denies requests where `spec.image` ends with `:latest`, enforcing pinned image tags.
  * Second validation:
    * Expression: `!has(object.spec.replicas) || (object.spec.replicas >= 1 && object.spec.replicas <= 10)`\
      Because `replicas` is optional in the CRD, this expression allows missing `replicas` but requires present values to be between 1 and 10.
    * `messageExpression` constructs a rejection message that embeds the actual invalid value for clearer errors.

Summary of validations:

|                                       Purpose | CEL expression                                                                              | Error message                                                               |
| --------------------------------------------: | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
|                  Disallow `:latest` image tag | `!object.spec.image.endsWith(':latest')`                                                    | `spec.image must not use ':latest'`                                         |
| Enforce replicas between 1 and 10 (or absent) | `!has(object.spec.replicas) \|\| (object.spec.replicas >= 1 && object.spec.replicas <= 10)` | `spec.replicas must be between 1 and 10` (enhanced via `messageExpression`) |

Next, create a ValidatingAdmissionPolicyBinding to activate the policy. The binding attaches the policy to evaluation and sets the validation action to `Deny`.

```yaml theme={null}
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: webapp-validation-binding
spec:
  policyName: webapp-validation
  validationActions: ["Deny"]
```

Apply the policy and its binding so the API server can begin evaluating matching WebApp CREATE and UPDATE requests:

```bash theme={null}
$ kubectl apply -f config/policy/webapp-policy.yaml
validatingadmissionpolicy.admissionregistration.k8s.io/webapp-validation created
$ kubectl apply -f config/policy/webapp-policy-binding.yaml
validatingadmissionpolicybinding.admissionregistration.k8s.io/webapp-validation-binding created
$ kubectl get validatingadmissionpolicy webapp-validation
NAME                VALIDATIONS   PARAMKIND   AGE
webapp-validation   2             <unset>     10s
$ kubectl get validatingadmissionpolicybinding webapp-validation-binding
NAME                      POLICYNAME         PARAMREF   AGE
webapp-validation-binding  webapp-validation   <unset>    9s
```

After the binding is observed by the admission plugin, the API server will evaluate matching WebApp CREATE and UPDATE requests using the policy before persisting them to etcd or sending them to any controller.

Test the policy with sample WebApp manifests:

1. Apply a WebApp that uses an unpinned image (`:latest`):

```yaml theme={null}
