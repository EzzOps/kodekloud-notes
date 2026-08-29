# policy-1.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-replica-count
spec:
  rules:
    - name: validate-replica-count
      match:
        any:
          resources:
            kinds:
              - Deployment
      validate:
        failureAction: Enforce
        message: "Replica count for a Deployment must be greater than or equal to 2."
        pattern:
          spec:
            replicas: ">=2"
```

Key points:

* `failureAction: Enforce` blocks resources that don't meet the policy.
* `pattern.spec.replicas: ">=2"` lets Kyverno accept any numeric value >= 2 (no exact value required).

> **warning** If you match on `replicas`, Kyverno may warn about the `scale` subresource not being included in the policy. This is informational only and doesn't change validation behavior, but add `subresources` to your `match` block if you also want to handle scale subresource requests.

> **lightbulb** When using numeric operators in Kyverno `pattern` values, put the operator and the number in a string (for example `">=2"`). This enables comparison-style validation in patterns.

Apply the policy:

```bash theme={null}
kubectl apply -f policy-1.yaml
```

Expected output:

```plaintext theme={null}
Warning: You are matching on replicas but not including the scale subresource in the policy.
clusterpolicy.kyverno.io/validate-replica-count created
```

Try creating a Deployment that violates the policy (replicas = 1):

```bash theme={null}
kubectl create deployment bad-deployment --image=nginx --replicas=1
```

Expected admission error:

```plaintext theme={null}
error: failed to create deployment: admission webhook "validate.kyverno.svc-fail" denied the request:
resource Deployment/default/bad-deployment was blocked due to the following policies

validate-replica-count:
  'validation' error: Replica count for a Deployment must be greater than or equal to 2.
  rule validate-replica-count failed at path /spec/replicas/
```

Now create a compliant Deployment (replicas = 3):

```bash theme={null}
kubectl create deployment good-deployment --image=nginx --replicas=3
```

Expected output:

```plaintext theme={null}
deployment.apps/good-deployment created
```

This demonstrates how Kyverno's comparison operators allow enforcing minimum replica counts without requiring fixed replica values.

***

## 2) Disallow using the default namespace

This ClusterPolicy prevents Deployments from being created in the `default` namespace. It uses the not operator (`!`) in the `pattern` value to assert that `metadata.namespace` must not equal `default`.

```yaml theme={null}
# policy-2.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-default-namespace
spec:
  rules:
    - name: disallow-default-namespace
      match:
        any:
          resources:
            kinds:
              - Deployment
      validate:
        failureAction: Enforce
        message: >
          Using the 'default' namespace is not allowed.
        pattern:
          metadata:
            # This value asserts that metadata.namespace is NOT "default".
            namespace: "!default"
```

Notes:

* `pattern.metadata.namespace: "!default"` asserts that the namespace value must not be `default`.
* `failureAction: Enforce` blocks requests that attempt to create Deployments in the `default` namespace.

Apply the policy:

```bash theme={null}
kubectl apply -f policy-2.yaml
```

Expected output:

```plaintext theme={null}
clusterpolicy.kyverno.io/disallow-default-namespace created
```

If you try to create a Deployment without specifying a namespace (which defaults to `default`), it will be rejected:

```bash theme={null}
kubectl create deployment bad-deployment --image=nginx --replicas=1
```

Expected admission error:

```plaintext theme={null}
error: failed to create deployment: admission webhook "validate.kyverno.svc-fail" denied the request:
resource Deployment/default/bad-deployment was blocked due to the following policies

disallow-default-namespace:
  'validation' error: Using the 'default' namespace is not allowed.
  rule disallow-default-namespace failed at path /metadata/namespace/
```

To comply with the policy, create a different namespace and deploy there:

```bash theme={null}
kubectl create ns my-apps
kubectl create deployment bad-deployment --image=nginx --replicas=1 -n my-apps
```

Expected output:

```plaintext theme={null}
namespace/my-apps created
deployment.apps/bad-deployment created
```

Using the `-n` flag or specifying `metadata.namespace` in manifests ensures resources are placed into allowed namespaces.

***

## Summary

This lesson demonstrated two ways to use operators inside Kyverno `pattern` validations:

| Use case                    | Operator example | Behavior                                                      |
| --------------------------- | ---------------- | ------------------------------------------------------------- |
| Enforce minimum replicas    | `">=2"`          | Accepts any numeric replicas value greater than or equal to 2 |
| Disallow specific namespace | `"!default"`     | Rejects resources whose `metadata.namespace` equals `default` |

These pattern operators let you express flexible, readable validation rules without hardcoding exact values. Use comparison operators for numeric constraints and the not operator (`!`) to exclude specific values.

## Links and References

* Kyverno Documentation: [https://kyverno.io/](https://kyverno.io/)
* Kyverno Policy Examples: [https://kyverno.io/docs/writing-policies/](https://kyverno.io/docs/writing-policies/)
* Kubernetes Concepts — Namespaces: [https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/642241f1-910d-47ff-92b7-ea67b08b5a93)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/5c3fecdf-d399-457b-a46d-90b977b212b2)


# Demo Patterns Wildcards

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Demo-Patterns-Wildcards/page

Explains a Kyverno ClusterPolicy using wildcards to require non-empty CPU and memory requests and limits for every container in Pods, with examples and best practices.

In this lesson you'll learn how to use Kyverno pattern wildcards to enforce that every container in a Pod declares CPU and memory requests and limits. This is a common policy need to ensure predictable scheduling and resource accounting across a cluster.

Overview

* We create a ClusterPolicy named `all-containers-need-requests-and-limits` that enforces CPU and memory requests and limits for every container in a Pod.
* The policy uses Kyverno pattern wildcards to match any container and require that the resource fields exist and are non-empty.

ClusterPolicy (ensures every container in a Pod has non-empty CPU and memory requests and limits)

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: all-containers-need-requests-and-limits
spec:
  rules:
    - name: check-container-resources
      match:
        any:
          - resources:
              kinds:
                - Pod
      validationFailureAction: enforce
      validate:
        message: "All containers must have CPU and memory resource requests and limits defined."
        pattern:
          spec:
            containers:
              # Match every container in the pod. The `name` field is optional and shown
              # here only as a visual aid.
              - name: "*"
                resources:
                  limits:
                    # `?` requires at least one character and `*` means zero or more characters.
                    # Using them together as `?*` requires at least one character (i.e., a non-empty value).
                    memory: "?*"
                    cpu: "?*"
                  requests:
                    memory: "?*"
                    cpu: "?*"
```

How the pattern and wildcards work

* The policy targets Pod resources via `match` and applies a pattern to `spec.containers`.
* Using `- name: "*"` applies the pattern to every element in the `containers` list.
* The `?*` wildcard is applied to string fields to require presence and non-empty values (we are not validating format, only that some value exists).

Wildcard summary

| Wildcard | Meaning                                                                        |
| -------- | ------------------------------------------------------------------------------ |
| `*`      | Matches zero or more characters. Useful for optional/any content.              |
| `?`      | Matches exactly one character.                                                 |
| `?*`     | Combined usage — requires at least one character (ensures a non-empty string). |

> **lightbulb** In Kyverno patterns, using `?*` on a string field ensures the field is present and contains at least one character (examples: `100m`, `128Mi`). Use this when you need to validate presence without enforcing a specific value format.

> **warning** This policy uses `validationFailureAction: enforce`, so requests that violate the rule are rejected by the admission webhook. During development, consider `validationFailureAction: audit` if you want to observe violations without blocking resources.

Apply the policy

```bash theme={null}
kubectl apply -f enforce-containers.yaml
```

Expected output

```bash theme={null}
clusterpolicy.kyverno.io/all-containers-need-requests-and-limits created
```

Test a Pod that violates the policy (no resources defined)

pod-bad-resource.yaml:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
    - name: my-container
      image: nginx
```

Apply the bad pod (using stdin for demonstration)

```bash theme={null}
kubectl apply -f - <<EOF
