# Demo Failure Action

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Demo-Failure-Action/page

Describes Kyverno failureAction modes Enforce and Audit plus allowExistingViolations and emitWarning to control namespace label validation and update behavior in Kubernetes.

In this lesson/article we will explore the `failureAction` field in Kyverno policies and how it controls policy behavior for create and update requests.

We begin with a simple ClusterPolicy that requires every Namespace to include a `purpose: production` label:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-ns-purpose-label
spec:
  rules:
    - name: require-ns-purpose-label
      match:
        any:
          - resources:
              kinds:
                - Namespace
      validate:
        failureAction: Enforce
        message: "You must have label `purpose` with value `production` set on all new namespaces."
        pattern:
          metadata:
            labels:
              purpose: production
```

This is a `ClusterPolicy` (applies cluster-wide). The rule is a `validate` rule that:

* matches resources of kind `Namespace`
* rejects non-conforming resources because `failureAction` is `Enforce`
* returns the provided `message` when validation fails
* enforces the `pattern` that requires `metadata.labels.purpose` to equal `production`

Apply the policy:

```bash theme={null}
kubectl apply -f enforce-ns-label.yaml
