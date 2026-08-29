# Output
# clusterpolicy.kyverno.io/check-images created
```

Test: Pod that violates the policy
This Pod uses `busybox:latest` from the public registry and should be rejected:

```bash theme={null}
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: bad-image-pod
spec:
  containers:
    - name: my-app
      image: busybox:latest
EOF
```

Expected rejection from the admission webhook:

```text theme={null}
Error from server: error when creating "STDIN": admission webhook "validate.kyverno.svc" denied the request:
resource Pod/default/bad-image-pod was blocked due to the following policies
check-images:
  check-registry: 'validation failure: validation error: unknown registry. rule check-registry failed at path /image/'
```

The Pod is blocked because the container image does not match `trusted-registry.io/*`.

Test: Pod that satisfies the policy
This Pod uses images from the trusted registry for both an init container and a main container and should be accepted:

```bash theme={null}
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: good-image-pod
spec:
  initContainers:
    - name: init-container
      image: trusted-registry.io/init-image:v1
  containers:
    - name: main-container
      image: trusted-registry.io/my-app:v1
EOF
```

Expected successful creation:

```text theme={null}
pod/good-image-pod created
```

Quick reference table

| Field                     | Purpose                                            | Example                          |
| ------------------------- | -------------------------------------------------- | -------------------------------- |
| `list`                    | JMESPath to the array being iterated               | `request.object.spec.containers` |
| `pattern`                 | Pattern applied to each `element` during iteration | `image: "trusted-registry.io/*"` |
| `validationFailureAction` | What happens on validation failure                 | `Enforce`                        |
| `preconditions`           | Skip rule for certain operations                   | `key: "{{request.operation}}"`   |

Summary

* `foreach` iterates over lists using a JMESPath expression (for example, `request.object.spec.containers` or `request.object.spec.initContainers`) and applies the `pattern` to each `element`.
* Using `foreach` reduces duplication and simplifies rules that validate repeated elements.
* Combining `foreach` with `preconditions` and `validationFailureAction: Enforce` provides a robust approach to block noncompliant resources.

Links and references

* Kyverno foreach documentation: [https://kyverno.io/docs/writing-policies/foreach/](https://kyverno.io/docs/writing-policies/foreach/)
* JMESPath query language: [https://jmespath.org/](https://jmespath.org/)
* Kubernetes admission webhooks: [https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/decaf28b-10ff-4c9b-b107-b0156645592d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/a382ed07-7980-462f-a6d2-affbaccb313c" />
</CardGroup>


# Demo Patterns Anchors

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Demo-Patterns-Anchors/page

Explains Kyverno validation anchors with conditional, equality, and existence examples to enforce Pod policies such as hostPath restrictions and required container images.

This lesson demonstrates how to use anchors in Kyverno validate rules. Anchors let you express if-then style logic directly inside a policy `pattern`, making validation concise and declarative. We'll cover three anchor types with short policy examples and test Pods:

* Conditional anchors
* Equality anchors
* Existence anchors

<Callout icon="lightbulb">
  Anchors are a Kyverno pattern feature that let you express conditional validation without adding an extra configuration block. `failureAction: Enforce` blocks resource creation when validation fails.
</Callout>

***

## Quick reference: anchor types

| Anchor type                       | Purpose                                                                                                          | When to use                                                             |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Conditional anchors `( )`         | Express an if-then relationship where the path inside parentheses is the "if" and a sibling field is the "then". | When a specific object or property implies another requirement.         |
| Equality anchors `=`              | Assert that an object exists and then apply constraints to its children.                                         | When the mere presence of an object should constrain its fields.        |
| Existence anchors (list matching) | Require at least one element in a list to match a pattern.                                                       | When you need one list element (e.g., a container) to meet a condition. |

For full Kyverno anchor pattern syntax and examples, see the Kyverno documentation: [https://kyverno.io/docs/writing-policies/validation-patterns/](https://kyverno.io/docs/writing-policies/validation-patterns/)

***

## 1) Conditional anchors

Conditional anchors implement an if-then rule. The content inside parentheses is the "if" clause; a sibling key at the same hierarchy level is the "then" clause.

Policy intent:

* If a Pod mounts `/var/run/docker.sock` via a `hostPath` volume, then the Pod must include label `allow-docker=true`.
* `failureAction: Enforce` blocks non-compliant Pods.

Policy (ClusterPolicy):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: conditional-anchor-dockersock
spec:
  background: false
  rules:
    - name: disallow-dockersock-without-label
      match:
        resources:
          kinds:
            - Pod
      validate:
        failureAction: Enforce
        message: "If a Pod mounts /var/run/docker.sock via hostPath, it must have label allow-docker=true."
        pattern:
          (spec):
            (volumes):
              - (hostPath):
                  path: "/var/run/docker.sock"
          metadata:
            labels:
              allow-docker: "true"
```

How it works:

* The `(spec) -> (volumes) -> (hostPath)` path is the "if" condition — it matches when a `hostPath` volume with `path: /var/run/docker.sock` is present.
* The sibling `metadata.labels.allow-docker` is the "then" clause and must match `true` (string).

Apply the policy:

```bash theme={null}
kubectl apply -f conditional-anchor-dockersock.yaml
