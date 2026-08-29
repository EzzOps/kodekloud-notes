# Demo Match Statements

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Demo-Match-Statements/page

Demonstrates Kyverno match blocks to enforce non-empty env label on Pods and Deployments, and how to scope the rule to specific namespaces

This guide demonstrates how Kyverno `match` blocks control which resources a policy evaluates. We'll enforce that Pods and Deployments include a non-empty `env` label using a ClusterPolicy, then refine the rule to target a specific namespace.

## Policy: require an `env` label

Create the following ClusterPolicy to validate that `metadata.labels.env` exists and is non-empty for Pods and Deployments:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-label-env
spec:
  validationFailureAction: enforce
  rules:
    - name: check-label-env
      match:
        any:
          - resources:
              kinds:
                - Pod
                - Deployment
      validate:
        message: "The label `env` is required."
        pattern:
          metadata:
            labels:
              env: "?*"
```

The key parts:

* `match` selects which resources Kyverno evaluates (here: kinds Pod and Deployment).
* `validate.pattern` enforces the presence and a non-empty value for `metadata.labels.env`.

> **lightbulb** The `?*` pattern in Kyverno matches any non-empty string, ensuring the `env` label exists and is not empty.

> **warning** This policy uses `validationFailureAction: enforce`, which will block resource creation or updates that don't meet the rule. Use `audit` if you prefer non-blocking checks.

## Apply the policy

Apply the policy manifest and verify the ClusterPolicy is ready:

```bash theme={null}
kubectl apply -f check-label.yaml
kubectl get cpol check-label-env
