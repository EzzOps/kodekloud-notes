# pod-bad-resource.yaml
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
  - name: my-container
    image: nginx
EOF
```

Expected rejection (admission webhook denies the request)

```text theme={null}
Error from server: error when creating "STDIN": admission webhook "validate.kyverno.svc-fail" denied the request:

resource Pod/default/bad-pod was blocked due to the following policies

all-containers-need-requests-and-limits:
  check-container-resources: 'validation error: All containers must have CPU and memory resource requests and limits defined. Rule check-container-resources failed at path /spec/containers/0/resources/limits/'
```

Why it was rejected

* The policy pattern requires `limits.memory`, `limits.cpu`, `requests.memory`, and `requests.cpu` to be present and non-empty for every container.
* The example pod lacked the `resources` block entirely, so Kyverno denied creation and returned the policy message.

Create a Pod that complies with the policy

pod-good-resource.yaml:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: good-pod
spec:
  containers:
    - name: my-container
      image: nginx
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "200m"
          memory: "256Mi"
```

Apply the good pod

```bash theme={null}
kubectl apply -f pod-good-resource.yaml
```

Expected output

```bash theme={null}
pod/good-pod created
```

Explanation

* The pod was created successfully because each container included all four resource fields (`requests.cpu`, `requests.memory`, `limits.cpu`, `limits.memory`) and each value matched the `?*` requirement (non-empty string).

Best practices and summary

* Use `- name: "*"` to apply a pattern to every element in a list (e.g., every container).
* Use `?*` on string fields to require that they exist and are non-empty without enforcing a specific format.
* Use `validationFailureAction: enforce` to actively block invalid resources; use `audit` to log violations without blocking during policy rollout.
* This pattern avoids per-container rules and enforces resource declarations cluster-wide with a single, maintainable policy.

Links and references

* [Kyverno documentation](https://kyverno.io/docs/)
* [Kubernetes admission controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [Kubernetes resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/8ae5a794-f7d4-4fcf-ab65-8f6c8a1ff2af)


# Deny Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Deny-Rules/page

Explains Kyverno deny rules for context aware admission control, blocking deletes of CI/CD managed ConfigMaps while exempting cluster admins.

So far, we've validated resources by inspecting their content with `pattern` and `anyPattern`. Those approaches are great when the decision depends only on the resource's shape or fields.

But what if the decision to allow or block depends on additional context — who is making the request and what operation they're performing? For that we need a more powerful mechanism: deny rules.

Alex's new challenge highlights this limit of pattern-based validation. He must prevent developers from deleting a set of ConfigMaps that are managed by the CI/CD system. The decision must consider the resource, the user, and the operation (DELETE) — all at once.

<Frame>
  <img alt="The image displays a challenge titled &#x22;Alex's Next Challenge,&#x22; where the task is to prevent developers from deleting specific ConfigMaps managed by a CI/CD system." />
</Frame>

In other words, Alex needs conditional logic with access to the admission request context. Deny rules provide exactly that.

Key conceptual shift:

* `pattern` describes what a good resource looks like; if it matches, Kyverno allows the request.
* `deny` describes what constitutes a forbidden situation; if a deny condition evaluates to true, Kyverno blocks the request.

> **lightbulb** Deny rules evaluate the admission request context — for example, `request.userInfo.username`, `request.operation`, or anything inside `request.object`. If a deny condition becomes true, Kyverno denies the request.

Deny rules may reference admission request variables and JMESPath expressions to look at real-time values such as `request.operation`, `request.userInfo.username`, or fields inside `request.object`.

<Frame>
  <img alt="The image shows a table explaining 'deny' sub-rules, contrasting pattern and deny rule types, their conditions, and goals. It highlights how deny rules can use variables like request.userInfo.username and request.operation." />
</Frame>

How deny rules are constructed

* Place a `deny` block inside the rule's `validate` section.
* Inside `deny`, define `conditions`.
* Choose the logical grouping: `any` (OR) or `all` (AND).
  * `any` denies the request if any single condition is true.
  * `all` denies only if every condition is true.
* Each condition has a `key`, an `operator`, and a `value`.
* Keys and values can reference admission request variables using JMESPath.

Table: Pattern vs Deny — quick comparison

|     Concept | Pattern (allow-by-match)    | Deny (block-by-condition)                                   |
| ----------: | --------------------------- | ----------------------------------------------------------- |
|     Purpose | Define valid resource shape | Define forbidden request conditions                         |
|   Evaluates | `request.object` fields     | `request.object`, `request.operation`, `request.userInfo.*` |
|       Logic | Match → allowed             | Condition true → denied                                     |
| Typical use | Ensure resource compliance  | Block operations by role, action, or runtime context        |

Example: deny conditions that inspect ConfigMap fields

```yaml theme={null}
validate:
  message: "Main message if any condition fails."
  deny:
    conditions:
      any:
        - key: "{{request.object.data.team}}"
          operator: Equals
          value: "eng"
          message: "ConfigMaps for team 'eng' are protected."
        - key: "{{request.object.data.unit}}"
          operator: Equals
          value: "green"
```

If the ConfigMap's `data.team` equals `"eng"` or `data.unit` equals `"green"`, the condition becomes true and Kyverno denies the request.

Practical policy: block deletes for CI/CD-managed ConfigMaps (except cluster-admin)

Alex needs to prevent deletes for ConfigMaps labeled as managed by the CI/CD system, but still allow cluster admins to perform deletes. The solution combines `match`, `exclude`, and `deny`:

* `match` limits which resources the rule considers.
* `exclude` prevents certain actors (e.g., cluster admins) from being affected.
* `deny` inspects the admission request (for example, `request.operation`) and blocks as needed.

Example cluster policy:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: deny-deletes-for-managed-resources
spec:
  rules:
    - name: block-deletes
      # Only consider resources with this label
      match:
        resources:
          selector:
            matchLabels:
              app.kubernetes.io/managed-by: kyverno
      # Ignore requests made by cluster admins
      exclude:
        clusterRoles:
          - cluster-admin
      validate:
        message: "Deleting this managed resource is not allowed."
        deny:
          conditions:
            any:
              - key: "{{request.operation}}"
                operator: Equals
                value: "DELETE"
```

Flow summary

1. `match` restricts the rule to resources labeled `app.kubernetes.io/managed-by=kyverno`.
2. `exclude` ensures requests from the `cluster-admin` role are ignored.
3. `deny` evaluates `request.operation`. If it equals `DELETE`, the deny condition becomes true and Kyverno denies the request.

Result: a non-admin user attempting to delete a CI/CD-managed ConfigMap will be blocked.

Empty `deny` (an unconditional deny)

A common pattern is to use an empty `deny` block. This is an unconditional deny: if a request reaches that rule (after `match` and `exclude`), Kyverno will block it immediately.

```yaml theme={null}
