# Demo Any and All Statements

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Demo-Any-and-All-Statements/page

Explains Kyverno ClusterPolicy match.any and match.all filters to apply OR or AND resource matching and enforce Pod label validation

In this lesson we explore Kyverno ClusterPolicy resource filters: `any` (logical OR) and `all` (logical AND). These filters let you target resources (for example, Pods) using flexible or strict matching logic and enforce validation rules such as required labels.

What you'll do:

* Create a ClusterPolicy that uses `match.any` (logical OR).
* Test the policy by creating Pods that match one or both conditions.
* Update the policy to use `match.all` (logical AND) and re-run tests to observe the difference.

> **lightbulb** The `any` filter behaves like a logical OR: the rule applies if at least one condition matches. The `all` filter behaves like a logical AND: the rule applies only if every condition matches.

> **warning** These policies use `validationFailureAction: enforce`, which means matching requests will be blocked by the admission webhook if validation fails. Apply policies cautiously in production clusters.

***

## Step 1 — Policy using `any` (logical OR)

Create a policy file named `check-label.yaml` with the following content. This ClusterPolicy enforces that when a Pod matches *either* selector (`type: database` OR `purpose: testing`), it must have an `app` label — otherwise the creation is rejected.

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
        any:
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

Apply the policy and confirm it's ready:

```bash theme={null}
kubectl apply -f check-label.yaml
