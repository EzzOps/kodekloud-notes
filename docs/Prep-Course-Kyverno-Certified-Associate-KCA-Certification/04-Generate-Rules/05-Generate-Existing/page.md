# Generate Existing

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Generate-Rules/Generate-Existing/page

Explains Kyverno's generateExisting feature that retroactively runs generate rules on existing resources to remediate drift and enforce baseline policies across current namespaces.

In this lesson we cover the `generateExisting` field — a Kyverno feature that lets generate rules run retroactively against resources that already exist in the cluster. This is useful when you have policies that apply only to future creations, but you also need to remediate past drift and enforce a baseline across all existing resources.

Let's check in with Alex, who has just encountered a common real-world scenario. He is proud of his new policies: all namespaces created after installing Kyverno are secure. But a security auditor found a compliance gap: the older namespaces that existed before the policy was added never triggered the generate rule, so they are missing the standard NetworkPolicy. Current policies only run when a new namespace is created.

<Frame>
  <img alt="The image illustrates a compliance gap scenario involving two characters, Alex and a Security Auditor, discussing network policy issues and existing namespaces." />
</Frame>

How can Kyverno be told to evaluate existing namespaces and apply the generate rule just once to bring the cluster to compliance?

<Frame>
  <img alt="The image addresses &#x22;Alex's Compliance Gap,&#x22; showing a figure labeled Alex, accompanied by a question regarding running a Kyverno rule on existing resources." />
</Frame>

The solution is `generateExisting`. When set to `true` in a rule's `generate` block, Kyverno immediately scans matching existing resources and generates any missing resources once at policy creation time. After that initial catch-up, the rule continues to behave like a normal generate rule and only reacts to future creations.

<Frame>
  <img alt="The image presents a solution feature called &#x22;generateExisting&#x22; related to Kyverno, indicating it applies a generate rule retroactively. There's a diagram showing the flow from the &#x22;generateExisting&#x22; field." />
</Frame>

Key behavior and best practices

* Default: `generateExisting` is `false` unless explicitly set.
  ```yaml theme={null}
  generateExisting: false
  ```
* When a policy includes `spec.rules[*].generate.generateExisting: true`, Kyverno:
  * Performs a one-time scan across the cluster for existing resources that match the rule.
  * Generates the configured resource(s) for matches found at that time.
  * Continues as a normal generate rule for subsequent creations.
* Use per-rule placement (`spec.rules[*].generate.generateExisting`) so you can mix retroactive and forward-looking generate rules within the same policy.

Recommended quick summary

| Topic            | Summary                                                                      |
| ---------------- | ---------------------------------------------------------------------------- |
| Purpose          | Apply generate rules to resources that already exist to remediate past drift |
| Default behavior | `generateExisting` is `false` by default                                     |
| Placement        | Use `spec.rules[*].generate.generateExisting` for per-rule control           |
| When it runs     | One-time scan at policy creation + normal behavior thereafter                |

Example: Retroactively generate a default-deny NetworkPolicy in every existing Namespace
This ClusterPolicy matches all Namespaces and generates a `NetworkPolicy` named `default-deny` inside each namespace that exists when the policy is applied. The `generateExisting: true` is set inside the rule's `generate` block.

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-default-deny
spec:
  rules:
  - name: generate-existing-networkpolicy
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      generateExisting: true
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny
      # Use the namespace of the matched Namespace resource
      namespace: "{{request.object.metadata.name}}"
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

When applied, Kyverno immediately scans for all existing Namespaces and creates the `default-deny` NetworkPolicy in each, closing the compliance gap and enforcing a consistent security baseline.

<Callout icon="lightbulb">
  Historically, `generateExisting` was configured at the policy top-level (deprecated). The correct placement is inside each rule's `generate` block (`spec.rules[*].generate.generateExisting`), which allows per-rule retroactive behavior while keeping other rules forward-looking.
</Callout>

Deprecated (old) placement — you may encounter this in older docs or examples:

```yaml theme={null}
