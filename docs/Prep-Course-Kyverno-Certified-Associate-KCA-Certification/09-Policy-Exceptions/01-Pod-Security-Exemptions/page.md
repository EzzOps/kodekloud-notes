# Pod Security Exemptions

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Policy-Exceptions/Pod-Security-Exemptions/page

Explains creating narrow Kyverno PolicyException to exempt specific Pod Security Standard controls for targeted workloads without weakening central policies

Previously we covered why and how policy exceptions are used. In this lesson we apply that knowledge to a concrete and common scenario: a critical monitoring agent must run as root, but the cluster enforces the Kubernetes Pod Security Standards (PSS) at the `restricted` level and blocks that behavior. Rather than weakening the central policy, we'll create a narrow, auditable exception that allows only the specific workload to run as root.

Scenario recap

* Alice runs a ClusterPolicy that enforces the official Kubernetes Pod Security Standards at the `restricted` level.
* One control in that profile—`Running as Non-root`—prevents containers from running as root.
* Alex needs a monitoring agent to run as root in a specific namespace (`delta`).
* Goal: create a scoped exception that targets only that control for the targeted workload(s) without modifying the global policy.

Cluster-level policy enforcing PSS (example)

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: psa
spec:
  rules:
    - name: restricted
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        failureAction: Enforce
        podSecurity:
          level: restricted
          version: latest
```

Why the Block Occurs

* The `restricted` profile includes a `Running as Non-root` control.
* Any Pod that tries to run containers as root will be rejected by this policy.
* We do not want to disable the control cluster-wide; we want a narrowly scoped exception.

Minimal PolicyException that targets a single PSS control

```yaml theme={null}
apiVersion: kyverno.io/v2
kind: PolicyException
metadata:
  name: delta-pss-exception
  namespace: policy-exception-ns
spec:
  exceptions:
    - policyName: psa
      ruleNames:
        - restricted
  match:
    any:
      - resources:
          namespaces:
            - delta
  # The new part:
  podSecurity:
    controlName: "Running as Non-root"
```

How this PolicyException works

* `match` selects resources in the `delta` namespace.
* `spec.exceptions` points to the `psa` policy and its `restricted` rule.
* `podSecurity.controlName` instructs Kyverno to ignore only the `Running as Non-root` control for the matched scope.
* Effect: only the specified control is ignored for resources in `delta`; the rest of the `restricted` profile still applies.

> **lightbulb** The `podSecurity` block in a PolicyException mirrors the `exclude` block you can add inside a `podSecurity` rule. This makes exceptions expressive and predictable, and easier to reason about when auditing policy changes.

Policy modification vs scoped exception

* Policy modification (not recommended for scoped needs)
  * Adding an `exclude` to the policy weakens enforcement for every resource matched by that policy.
  * Changes apply cluster-wide (or to all resources matched by the policy) and affect all teams.

* PolicyException (recommended)
  * Keeps the central policy intact.
  * Provides an auditable, separate object that grants a narrow allowance for a specific scope (namespace, image, etc.).
  * Supports separation of duties and easier review / rollback.

Comparison table

| Action                               | Scope                                    | Auditable                       | Use when                                                                  |
| ------------------------------------ | ---------------------------------------- | ------------------------------- | ------------------------------------------------------------------------- |
| Modify central policy with `exclude` | Cluster-wide or policy-matched resources | No (changes directly to policy) | You must permanently change enforcement for all matched resources         |
| Create `PolicyException`             | Narrow (namespace, images, labels, etc.) | Yes (exception object)          | A temporary or scoped allowance is needed for a specific workload or team |

Example of weakening the policy (not recommended if you only need a scoped exception)

```yaml theme={null}
