# CEL Admission Policies

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Validation-Webhooks-And-CEL-Policies/CEL-Admission-Policies/page

Using CEL validating admission policies in Kubernetes to declaratively reject invalid or unsafe custom resource requests before persistence

Sometimes the safest reconcile loop is the one that never has to see a bad object. Validating admission policies let the API server reject unsafe requests before they are persisted, so your operator never has to reconcile invalid input.

<Frame>
  <img alt="The image illustrates the process of rejecting a bad web app request at admission using a validating admission policy before it is stored, ensuring the reconcile loop never sees it." />
</Frame>

Think of admission as the Kubernetes API server's front desk: every create or update request arrives there, gets checked, and only accepted objects proceed to storage and the reconciler. Validating admission policies express those checks using the Common Expression Language (CEL), a compact, safe expression language evaluated by the API server.

<Callout icon="lightbulb">
  CEL expressions are evaluated inside the API server: they are not compiled Go code and they do not call your operator. You can use CEL to write concise, declarative checks against the incoming object.
</Callout>

<Frame>
  <img alt="The image displays text explaining that the rule sheet uses the Common Expression Language (CEL) and indicates that it is not code, specifically not a Go function or operator call." />
</Frame>

Key objects in a validating admission setup

* Policy: defines match criteria and the CEL expressions (rules) that must evaluate true.
* Binding: enables a policy and chooses the enforcement action (deny, warn, audit).

Keeping Policy and Binding separate allows you to author reusable policies and enable them selectively via bindings.

| Resource | Purpose                                                             | Example                                           |
| -------- | ------------------------------------------------------------------- | ------------------------------------------------- |
| Policy   | Defines which requests to match and the CEL expressions to evaluate | `validatingadmissionpolicy/webapp-rules`          |
| Binding  | Turns a Policy on and selects the enforcement action                | `validatingadmissionpolicybinding/webapp-binding` |

<Frame>
  <img alt="The image illustrates a process where a &#x22;Binding&#x22; component with &#x22;Policy on&#x22; and &#x22;Enforcement: Deny&#x22; settings connects to a &#x22;Policy&#x22; component with rules and expressions." />
</Frame>

Matching CRDs and referencing object fields

* For a custom resource like a webapp, match typically targets API group `webapp.cloudnative.space`, version `v1`, and kind `WebApp` (or `webapp` depending on your CRD).
* Inside a CEL expression, use the built-in `object` variable to read the incoming object (for example `object.spec.image` or `object.spec.replicas`).
* Use `has(...)` to test for optional fields before evaluating them.

Practical rule examples and recommended CEL expressions

| Rule           | Purpose                                                             | CEL expression                                                                                     |
| -------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Image pinning  | Disallow moving tags like `:latest` so deployments are reproducible | `cel\n!object.spec.image.endsWith(':latest')\n`                                                    |
| Replica limits | Allow omitted replicas, but if provided require 1..10               | `cel\n!has(object.spec.replicas) \|\| (object.spec.replicas >= 1 && object.spec.replicas <= 10)\n` |

Examples above show typical, object-local validations that CEL is designed for.

Two short CEL examples:

```cel theme={null}
