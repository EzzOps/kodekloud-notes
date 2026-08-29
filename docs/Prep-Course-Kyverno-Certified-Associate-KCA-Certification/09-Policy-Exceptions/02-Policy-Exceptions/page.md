# This makes the central policy weaker for all matched resources
clusterpolicy:
  validate:
    podSecurity:
      level: restricted
      version: latest
      exclude:
        - controlName: "Running as Non-root"
```

Equivalent scoped exception (preferred)

```yaml theme={null}
# This leaves the central policy intact and creates a scoped exception
exception:
  spec:
    exceptions:
      - policyName: psa
        ruleNames:
          - restricted
        podSecurity:
          controlName: "Running as Non-root"
```

Granular, container-level exceptions
Some PSS controls apply to the Pod as a whole (for example, `hostPath` restrictions). Others operate at the container level (for example, `Capabilities`). When a control applies to containers, Kyverno supports finer-grained exceptions using an `images` field so you can target only the containers that need the exemption.

Policy-level `exclude` example (applies at policy authoring time)

```yaml theme={null}
validate:
  podSecurity:
    level: restricted
    version: latest
    exclude:
      - controlName: Capabilities
        images:
          - nginx*
          - redis
```

Scoped PolicyException (recommended approach)

```yaml theme={null}
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
  podSecurity:
    controlName: Capabilities
    images:
      - nginx*
      - redis
```

Behavior notes

* With this exception, only containers whose image matches `nginx*` or `redis` will be exempted from the `Capabilities` control.
* Other containers in the same Pod (for example, an Ubuntu-based sidecar) still must comply with the `Capabilities` control.
* Use image patterns carefully to avoid accidentally broadening the exception.

> **warning** Keep exceptions as narrow, well-documented, and time-limited as possible. Exceptions expand risk when left open or when they are overly broad (for example, matching many image names or many namespaces).

Best practices and recap

* Prefer PolicyException to modifying a central PodSecurity rule when you need a scoped exemption.
* Use `controlName` for pod-wide exemptions (e.g., `Running as Non-root`).
* For container-level controls, add `images` to target only specific images and avoid exempting sidecars or unrelated containers.
* Make exceptions:
  * Narrow in scope (namespace, image, label selector).
  * Audited and documented (reason, owner, expiration).
  * Temporary when possible; review regularly.
* Document the business or technical reason for each exception and record its owner and planned removal date.

References and further reading

* [Kyverno PolicyException docs](https://kyverno.io/docs/writing-policies/policy-exception/)
* [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
* [Kyverno Pod Security support](https://kyverno.io/docs/writing-policies/policy-exception/#pod-security)

That concludes this lesson on creating Pod Security exceptions with Kyverno.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/26478d8e-69b0-4b48-bc9a-173ba8b28d7b/lesson/890acc40-3bb3-48e1-a455-1a44633dc0ba)


# Policy Exceptions

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Policy-Exceptions/Policy-Exceptions/page

Explains Kyverno PolicyException enabling, configuring, and using auditable namespace scoped exceptions to bypass specific policy rules for targeted resources without editing core policies.

Alex built a solid Kyverno security policy, but now it blocks a critical debugging tool. What should we do?

* Disable the policy? No — that opens a large security hole.
* Make the policy extremely complex with many excludes? No — that's hard to maintain.

Kyverno provides a better option: PolicyException resources. They let you grant a controlled, auditable "hall pass" for specific resources without changing core policies.

<Frame>
  <img alt="The image is discussing the question &#x22;Why Not Just Edit the Policy?&#x22; in the context of Kyverno, highlighting that Kyverno policies have features like match, exclude, and preconditions but questioning the need for a separate resource." />
</Frame>

Why not just edit the policy?

* Team boundaries: a central security team owns cluster policies. Application teams should not have to request edits for each exception. PolicyException lets app teams create exceptions in a controlled, auditable way without touching the core policy.
* Simplicity: adding many exclude blocks to policies creates long, hard-to-read policies. Exceptions keep the policy logic simple and make temporary or emergency exceptions explicit.

<Frame>
  <img alt="The image outlines roles in teamwork: the Policy Team defines security policies, the App Team manages applications and exceptions, and a PolicyException role requests exceptions without altering core policies." />
</Frame>

<Frame>
  <img alt="The image presents a visual guide titled &#x22;Clean and Simple,&#x22; highlighting three points: avoiding complex policies, readability through simpler policies with exceptions, and suitability for temporary or emergency access." />
</Frame>

Important prerequisite: PolicyExceptions are opt-in. Nothing will work unless you explicitly enable the feature on the Kyverno admission controller.

<Frame>
  <img alt="The image contains a warning message about policy exceptions being disabled by default, with instructions to configure the Kyverno admission controller before using them." />
</Frame>

To enable PolicyExceptions, set two flags in the Kyverno admission controller deployment:

* `--enablePolicyException` — enable the PolicyException feature (`true`).
* `--exceptionNamespace` — which namespace(s) may contain PolicyException resources.

Kyverno requires a namespace to control who can create exceptions. You can set `--exceptionNamespace` to `*` to allow exceptions from any namespace, but that is only appropriate in less restrictive environments.

> **lightbulb** Enable the feature by adding `--enablePolicyException=true` and set `--exceptionNamespace` (or `*`) in the Kyverno admission controller flags. The namespace value controls where PolicyException resources may be created.

<Frame>
  <img alt="The image provides instructions on enabling PolicyException in Kyverno Admission Controller Deployment by setting two flags: --enablePolicyException and --exceptionNamespace. It highlights a key point about allowing resources in all namespaces." />
</Frame>

Hands-on scenario

Alex faces a ClusterPolicy that disallows Pods from sharing host namespaces (`hostPID`, `hostIPC`, `hostNetwork`). This is a typical security rule, but a developer needs to run a debugging tool that must inspect host namespaces; the policy blocks it.

<Frame>
  <img alt="The image describes a challenge where a ClusterPolicy blocks pods from using host network or process ID namespaces, affecting a tool that requires access to the host's IPC namespace." />
</Frame>

Goal: create a PolicyException that allows the `important-tool` Deployment in the `delta` namespace to bypass the specific rule for debugging.

<Frame>
  <img alt="The image displays a goal description stating, &#x22;Create a PolicyException to allow only the important-tool Deployment in the delta namespace to bypass this rule.&#x22;" />
</Frame>

The ClusterPolicy we're up against (simplified):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-host-namespaces
spec:
  rules:
    - name: host-namespaces
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        failureAction: Enforce
        message: "Sharing host namespaces is disallowed."
        pattern:
          spec:
            hostPID: false
            hostIPC: false
            hostNetwork: false
```

Note: `failureAction: Enforce` means Kyverno will actively block any resource that violates the rule. That's why the debugging tool cannot be created.

PolicyException blueprint

A PolicyException is explicit and answers three questions:

1. Which policy and rule(s) to bypass? (`exceptions` block)
2. Which resource(s) get the exception? (`match` block)
3. (Optional) Under what extra conditions? (`conditions` block)

Annotated blueprint:

```yaml theme={null}
apiVersion: kyverno.io/v2
kind: PolicyException
metadata:
  name: <exception-name>
  namespace: <exception-namespace>
spec:
  # 1. WHICH policy and rule(s) to bypass?
  exceptions:
    - policyName: <name-of-policy-to-exempt>   # e.g., disallow-host-namespaces or "ns/policy" for namespaced policies
      ruleNames:
        - <name-of-rule-to-exempt>            # list individual rule names or use ["*"] to match all rules

  # 2. WHICH resource(s) get the exception?
  match:
    any:
      - resources:
          kinds:
            - Pod
            - Deployment
          namespaces:
            - my-namespace
          names:
            - my-app*         # wildcard is useful for matching generated Pod names

  # 3. (Optional) Under WHAT extra conditions?
  conditions:
    any:
      - key: "{{ request.object.metadata.labels['debug'] }}"
        operator: Equals
        value: "true"
```

Key details

* `policyName` targets the exact policy to bypass. For a namespaced policy use the format `namespace/policy-name`.
* `ruleNames` must list the rule names from the policy (or `["*"]` to bypass all rules).
* `match` supports the same selectors as Kyverno policies: `kinds`, `namespaces`, `names`, `labelSelector`, etc.
* `conditions` are optional extra checks evaluated against the admission request or object.

Putting the blueprint into practice

Alex's exception will live in the `delta` namespace (which must be allowed by `--exceptionNamespace`). Important: Kyverno autogenerates rules for controller resources when a rule targets Pods. If a ClusterPolicy validates Pods, Kyverno creates corresponding `autogen-...` rules for Deployments, StatefulSets, Jobs, etc. To exempt a Deployment and its Pods, you must exempt both the original rule and the autogen rule.

Final PolicyException to solve Alex's problem:

```yaml theme={null}
apiVersion: kyverno.io/v2
kind: PolicyException
metadata:
  name: delta-exception
  namespace: delta # Must be a namespace listed in --exceptionNamespace
spec:
  exceptions:
    - policyName: disallow-host-namespaces
      ruleNames:
        - host-namespaces
        - autogen-host-namespaces
  match:
    any:
      - resources:
          kinds:
            - Pod
            - Deployment
          namespaces:
            - delta
          names:
            - important-tool*
```

Why two rule names?

* `host-namespaces` is the original ClusterPolicy rule applying to Pods.
* `autogen-host-namespaces` is the automatically generated rule that applies to controller resources (Deployment, StatefulSet, Job, etc.). Exempting both ensures both the Deployment and the Pods it creates are covered.

Using wildcards and namespaced policies

* For a namespaced policy, specify the policy name as `namespace/policy-name`, for example:

```yaml theme={null}
policyName: "app-security/disallow-host-namespaces"
```

* To bypass all rules in a policy, use:

```yaml theme={null}
ruleNames:
  - "*"
```

Table: Common Kyverno admission controller flags for PolicyExceptions

| Flag                      | Purpose                                                | Example                                                  |
| ------------------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| `--enablePolicyException` | Enable PolicyException feature                         | `--enablePolicyException=true`                           |
| `--exceptionNamespace`    | Namespace(s) allowed to host PolicyException resources | `--exceptionNamespace=delta` or `--exceptionNamespace=*` |

> **warning** Setting `--exceptionNamespace=*` allows PolicyExceptions from any namespace. Use this only in trusted or non-production environments — wildcard exceptions increase risk.

Table: PolicyException core fields

| Field                   | Meaning                                                  | Example                                                                   |
| ----------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| `exceptions.policyName` | Policy to bypass (use `ns/name` for namespaced policies) | `disallow-host-namespaces`                                                |
| `exceptions.ruleNames`  | List of rule names in the policy or `["*"]`              | `["host-namespaces","autogen-host-namespaces"]`                           |
| `match`                 | Which resources receive the exception                    | `kinds: [Deployment, Pod], namespaces: [delta], names: [important-tool*]` |
| `conditions`            | Optional extra checks against the request/object         | `key: "{{ request.object.metadata.labels['debug'] }}"`                    |

Recap

* PolicyExceptions decouple temporary or special-case exceptions from core ClusterPolicies, improving maintainability and team autonomy.
* The feature is opt-in: enable it on the Kyverno admission controller with `--enablePolicyException` and restrict creation locations with `--exceptionNamespace`.
* A PolicyException explicitly identifies the policy and rule(s) to bypass, the target resources, and optional conditions.
* Remember to include autogen rule names when you need to exempt controller resources (Deployments, StatefulSets, Jobs) in addition to Pods.

<Frame>
  <img alt="The image outlines three key learning points about PolicyExceptions, including their role in decoupling exception logic from core policies, the need for container flags to enable the feature, and the specification of policy and resource bypass." />
</Frame>

Further reading and references

* Kyverno PolicyException docs: [https://kyverno.io/docs/writing-policies/policyexception/](https://kyverno.io/docs/writing-policies/policyexception/)
* Kyverno admission controller configuration: [https://kyverno.io/docs/installation/#admission-controller](https://kyverno.io/docs/installation/#admission-controller)

Now that you understand how PolicyExceptions work, you can create a controlled exception for Alex's `important-tool` deployment without changing the central security policy.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/26478d8e-69b0-4b48-bc9a-173ba8b28d7b/lesson/79e8a7d6-2f6b-4d40-a79f-4e35741befab)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/26478d8e-69b0-4b48-bc9a-173ba8b28d7b/lesson/3ecd3f0f-384a-4574-99b0-d4307cfcecca)
