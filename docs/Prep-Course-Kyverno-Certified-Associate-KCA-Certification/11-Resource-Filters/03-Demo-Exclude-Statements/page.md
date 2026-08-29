# Output:
kubectl get cpol check-label-app
# Example output:
# NAME             ADMISSION   BACKGROUND   READY   AGE   MESSAGE
# check-label-app  true        true         True    11s   Ready
```

Testing scenarios (with `match.any`):

1. Pod with `type=database` but no `app` label — should be blocked because it satisfies the first `any` condition.

```bash theme={null}
kubectl run my-pod --image=nginx --labels="type=database"
# Expected error:
# Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
# resource Pod/default/my-pod was blocked due to the following policies
#
# check-label-app:
#   check-label-app: 'validation error: The label app is required. rule check-label-app failed at path /metadata/labels/app/'
```

2. Pod with `purpose=testing` but no `app` label — should be blocked because it satisfies the second `any` condition.

```bash theme={null}
kubectl run my-pod2 --image=nginx --labels="purpose=testing"
# Expected error:
# Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
# resource Pod/default/my-pod2 was blocked due to the following policies
#
# check-label-app:
#   check-label-app: 'validation error: The label app is required. rule check-label-app failed at path /metadata/labels/app/'
```

Summary for `match.any`: matching either selector triggers validation.

***

## Step 2 — Switch to `all` (logical AND)

To require both selectors be present before enforcing the label, replace the `match.any` block with `match.all`. The effect: the rule applies only when the Pod matches *both* `type: database` and `purpose: testing`.

Updated `check-label.yaml` (key change: `all` instead of `any`):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-label-app
spec:
  validationFailureAction: enforce
  rules:
    - name: check-label-app
      match:
        all:
          - resources:
              kinds:
                - Pod
            selector:
              matchLabels:
                type: database
          - resources:
              kinds:
                - Pod
            selector:
              matchLabels:
                purpose: testing
      validate:
        message: "The label app is required."
        pattern:
          metadata:
            labels:
              app: "?*"
```

Apply the updated policy:

```bash theme={null}
kubectl apply -f check-label.yaml
# Output:
kubectl get cpol check-label-app
# Example output:
# NAME             ADMISSION   BACKGROUND   READY   AGE    MESSAGE
# check-label-app  true        true         True    11s    Ready
```

Re-run tests for the three scenarios with `match.all`:

1. Pod with only `type=database` (no `purpose`) — policy should NOT apply, Pod created successfully.

```bash theme={null}
kubectl run pod-only-type --image=nginx --labels="type=database"
# Expected output:
# pod/pod-only-type created
```

2. Pod with both `type=database` and `purpose=testing` but missing `app` — policy applies, creation blocked.

```bash theme={null}
kubectl run test-pod --image=nginx --labels="type=database,purpose=testing"
# Expected error:
# Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
# resource Pod/default/test-pod was blocked due to the following policies
#
# check-label-app:
#   check-label-app: 'validation error: The label app is required. rule check-label-app failed at path /metadata/labels/app/'
```

3. Pod with `type=database`, `purpose=testing`, and `app=testing` — all matching conditions satisfied and validation passes; Pod created.

```bash theme={null}
kubectl run test-pod-with-app --image=nginx --labels="type=database,purpose=testing,app=testing"
# Expected output:
# pod/test-pod-with-app created
```

***

## Quick comparison

| Filter      | Logical meaning                        | Example match that triggers validation                                   | Typical use case                                         |
| ----------- | -------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| `match.any` | OR — at least one condition must match | `type=database` OR `purpose=testing` (either label triggers enforcement) | Broad validation across multiple categories              |
| `match.all` | AND — every condition must match       | Both `type=database` AND `purpose=testing` must be present               | Narrow validation when multiple attributes must coincide |

***

## Summary

* `match.any` (OR): The rule applies if at least one listed resource filter matches the resource. Use this to enforce rules across multiple possible resource selector conditions.
* `match.all` (AND): The rule applies only when every listed resource filter matches the resource. Use this to target a narrow subset of resources that must satisfy every criterion.

References and further reading:

* Kyverno documentation — ClusterPolicy and match conditions: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kubernetes admission controllers: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

Use `any` when you want to validate resources that meet any of multiple criteria. Use `all` when validation should only apply to resources that satisfy every listed condition.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/2dc0b67f-8e06-499c-9741-fa03938d6c93)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/7c96b662-7cb5-4b17-b3d9-c7a08cb409c0)


# Demo Exclude Statements

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Demo-Exclude-Statements/page

Demonstrates a Kyverno ClusterPolicy that requires Pods in the monitoring namespace to have an env label while excluding Pods labeled team=operations

This lesson shows how to combine `match` and `exclude` statements in a Kyverno policy to enforce labels selectively.

Goal

* Require a Pod to have an `env` label when it is created in the `monitoring` namespace.
* Exempt Pods that have the `team=operations` label (those Pods are excluded from the policy).

Policy definition
Below is the ClusterPolicy that enforces this behavior. The `match` block narrows the policy scope to Pods in the `monitoring` namespace. The `exclude` block creates an exception for Pods with the `team: operations` label.

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-env-label
spec:
  rules:
    - name: check-env-label
      match:
        resources:
          kinds:
            - Pod
          namespaces:
            - monitoring
      exclude:
        resources:
          selector:
            matchLabels:
              team: operations
      validate:
        failureAction: Enforce
        message: "Pods in the monitoring namespace (except team=operations) must have the 'env' label."
        pattern:
          metadata:
            labels:
              env: "?*"
```

Apply the policy
Run the following to create the ClusterPolicy in your cluster:

```bash theme={null}
cat <<'EOF' | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-env-label
spec:
  rules:
    - name: check-env-label
      match:
        resources:
          kinds:
            - Pod
          namespaces:
            - monitoring
      exclude:
        resources:
          selector:
            matchLabels:
              team: operations
      validate:
        failureAction: Enforce
        message: "Pods in the monitoring namespace (except team=operations) must have the 'env' label."
        pattern:
          metadata:
            labels:
              env: "?*"
EOF
```

Expected response:

```text theme={null}
clusterpolicy.kyverno.io/require-env-label created
```

Verify the policy:

```bash theme={null}
kubectl get cpol require-env-label
```

Example output:

```text theme={null}
NAME               ADMISSION   BACKGROUND   READY   AGE   MESSAGE
require-env-label  true        true         True    10s   Ready
```

Create the `monitoring` namespace (if it doesn't exist):

```bash theme={null}
kubectl create namespace monitoring
```

Expected response:

```text theme={null}
namespace/monitoring created
```

Tests
Below are three tests demonstrating how `match` and `exclude` interact.

| Test                                                   | Command                                                                                    | Expected result                                                                           |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| 1 — Pod without `env` label (should be blocked)        | `kubectl run my-pod --image=nginx -n monitoring --restart=Never`                           | Denied by Kyverno validation webhook because the Pod matches `match` and is not excluded. |
| 2 — Pod with wrong label name (should also be blocked) | `kubectl run my-pod --image=nginx -n monitoring --restart=Never --labels=teams=operations` | Denied — label key must be `team`, so the Pod is not excluded.                            |
| 3 — Pod with `team=operations` (should be allowed)     | `kubectl run my-pod --image=nginx -n monitoring --restart=Never --labels=team=operations`  | Allowed — the `exclude` selector matches and the policy is not applied.                   |

Test 1 — Pod without `env` label (should be blocked)
Create a Pod in the `monitoring` namespace without the `env` label and without the `team` label. This Pod matches the `match` criteria and is not excluded, so the policy should deny it.

Attempt to create the Pod:

```bash theme={null}
kubectl run my-pod --image=nginx -n monitoring --restart=Never
```

Example denial from Kyverno webhook:

```text theme={null}
Error from server: admission webhook "validate.kyverno.svc" denied the request:
resource Pod/monitoring/my-pod was blocked due to the following policies
require-env-label:
  check-env-label: 'validation error: Pods in the monitoring namespace (except team=operations)
  must have the ''env'' label. rule check-env-label failed at path /metadata/labels/env/'
```

Test 2 — Pod with wrong label name (should also be blocked)
If you accidentally add the wrong label key (for example `teams=operations` instead of `team=operations`), the Pod will still be evaluated by the policy and denied:

```bash theme={null}
kubectl run my-pod --image=nginx -n monitoring --restart=Never --labels=teams=operations
```

Expected response (same denial as above):

```text theme={null}
Error from server: admission webhook "validate.kyverno.svc" denied the request:
resource Pod/monitoring/my-pod was blocked due to the following policies
require-env-label:
  check-env-label: 'validation error: Pods in the monitoring namespace (except team=operations)
  must have the ''env'' label. rule check-env-label failed at path /metadata/labels/env/'
```

Test 3 — Pod with `team=operations` (should be allowed)
Now create the Pod with the correct excluding label key `team=operations`. Because the `exclude` selector matches this Pod, the policy will not be applied to it and creation should succeed even though it lacks the `env` label.

```bash theme={null}
kubectl run my-pod --image=nginx -n monitoring --restart=Never --labels=team=operations
```

Expected response:

```text theme={null}
pod/my-pod created
```

You can confirm the Pod exists:

```bash theme={null}
kubectl get pods -n monitoring
```

Summary

* `match` narrows policy scope to specific resources (here: Pods in the `monitoring` namespace).
* `exclude` defines exceptions so matched resources with certain labels are skipped (here: `team=operations`).
* A Pod that matches `match` and is not excluded is validated by the `validate` rule and rejected if it doesn't meet the pattern.
* Label keys must be exact — typos like `teams` vs `team` will prevent exclusion and cause the policy to apply.

> **lightbulb** Use `kubectl run ... --restart=Never` to create an actual Pod (rather than a Deployment) for these tests. Also double-check label key names to ensure exclusions work as expected.

Links and References

* [Kyverno Documentation](https://kyverno.io/docs/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/overview/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/27d9b318-bbe8-4f38-89de-3da70c287145)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/4d9d404b-630f-4dc9-b9bc-9caaf8d36742)
