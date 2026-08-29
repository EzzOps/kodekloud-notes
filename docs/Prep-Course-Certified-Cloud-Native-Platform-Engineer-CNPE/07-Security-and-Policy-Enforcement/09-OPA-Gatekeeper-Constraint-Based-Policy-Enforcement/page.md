# List all cluster policies and their status
kubectl get clusterpolicy

# Check policy reports (audit-mode violations)
kubectl get policyreport -A
kubectl get clusterpolicyreport

# Describe a PolicyReport for a specific namespace (example: payments)
kubectl describe policyreport -n payments

# Check Kyverno controller logs
kubectl logs -n kyverno deployment/kyverno
```

Common issues and how to troubleshoot:

* READY = false: usually indicates invalid policy YAML or a schema mismatch. Inspect `kubectl describe clusterpolicy <name>` and Kyverno logs.
* Policies not taking effect: verify `match` criteria are correct; it’s common for match scope to not include the resources you expect.
* No rejections while in `Enforce`: ensure the policy truly matches the resources and the pattern is correct.
* Webhook errors: check Kyverno controller health and logs; confirm webhook configurations and certificates.

## Key takeaways

<Frame>
  <img alt="The image contains key takeaways about Kyverno, highlighting its use of Kubernetes YAML, rule types (validate, mutate, generate), and a safe rollout strategy." />
</Frame>

* Kyverno uses pure Kubernetes YAML — no extra language required.
* One policy resource can include validate, mutate, and generate rules.
* Adopt a safe rollout: audit mode first, review `PolicyReport`s, then switch to enforce.
* Choose Kyverno when you need mutation or YAML-native policies; choose Gatekeeper when Rego’s expressiveness is required.
* Kyverno and Gatekeeper can coexist in the same cluster.

Further reading:

* Kyverno docs: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Gatekeeper: [https://open-policy-agent.github.io/gatekeeper/](https://open-policy-agent.github.io/gatekeeper/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/1a5a6874-6438-434c-a731-163beffe04ea)


# OPA Gatekeeper Constraint Based Policy Enforcement

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/OPA-Gatekeeper-Constraint-Based-Policy-Enforcement/page

Explains using OPA Gatekeeper ConstraintTemplates and Constraints to enforce Kubernetes admission policies with Rego examples, rollout best practices, and debugging tips.

Now let's build our first policy engine.

[Gatekeeper](https://open-policy-agent.github.io/gatekeeper/) is a Kubernetes-native policy engine built on top of Open Policy Agent. Gatekeeper uses a two-resource model—ConstraintTemplates and Constraints—to define and apply policies at the Kubernetes API server admission stage. This guide walks through the concepts, a practical Rego example, safe rollout practices, and debugging tips so you can write, test, and enforce policies reliably.

A real-world motivation: a healthcare company required HIPAA-compliant configurations across twelve namespaces. Their CI/CD pipeline scanned YAMLs, but developers could still run `kubectl apply` directly and bypass checks. In two months they logged three incidents: a pod missing encryption labels, a container running as root with direct patient-data access, and an unscanned image pulled from Docker Hub. Gatekeeper would have enforced these checks at the API server, preventing such resources regardless of how they were created.

<Frame>
  <img alt="The image features an illustration related to HIPAA compliance in a healthcare setting, mentioning issues like a pod without encryption labels and a container running as root. It also highlights CI/CD scripts, security concerns, and Docker Hub." />
</Frame>

## How Gatekeeper’s two-resource model works

Gatekeeper separates policy logic from policy instances:

* ConstraintTemplate: authored by the platform or security team. Contains the Rego policy logic and registers a new CRD (CustomResourceDefinition) when applied.
* Constraint: an instance of that CRD that specifies where the policy should be applied and supplies parameters.

Write the logic once in a ConstraintTemplate and create multiple Constraints with different parameters to apply the same policy across multiple scopes.

<Frame>
  <img alt="The image is a comparison between &#x22;ConstraintTemplate&#x22; and &#x22;Constraint&#x22; in the context of mutating vs. validating webhooks, highlighting the functions and features of each." />
</Frame>

## Example: Required labels policy (ConstraintTemplate + Constraint)

The following example shows a ConstraintTemplate that enforces required labels on a resource. Key points:

* `spec.crd` creates a new kind: `K8sRequiredLabels`.
* `spec.targets.rego` contains the Rego logic.
* Rego inputs to know:
  * `input.review` — the admissionReview object; the resource under validation/ mutation is `input.review.object`.
  * `input.parameters` — parameters provided by the Constraint.

ConstraintTemplate:

```yaml theme={null}
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := input.review.object
          required := input.parameters.labels
          label := required[_]
          not provided.metadata.labels[label]
          msg := sprintf("missing: %v", [label])
        }
```

Explanation:

* The `violation` rule iterates the `labels` parameter and checks whether each required label exists on the requested resource (`input.review.object.metadata.labels`).
* When a label is missing, the rule emits a violation message, and Gatekeeper will act according to the Constraint's `enforcementAction` (e.g., `deny`, `warn`, `dryrun`).

Now create a Constraint that uses the template. The `kind` must match the `K8sRequiredLabels` CRD registered by the template. The `enforcementAction` controls behavior:

* `dryrun`: record violations but allow the request.
* `warn`: allow the request, but return a warning to the caller.
* `deny`: reject the request.

Constraint:

```yaml theme={null}
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["team"]
```

With the constraint above, attempts to create a Namespace without the `team` label will be rejected with a helpful message:

```bash theme={null}
$ kubectl create ns test-ns
Error from server: admission webhook "constraint.gatekeeper.sh" denied the request: missing: "team"
```

## Recommended rollout strategy

A staged rollout prevents sudden breakage across clusters and teams:

1. Start with `enforcementAction: dryrun` — captures violations without blocking resources.
2. Move to `warn` — surfaces issues to users while still allowing requests.
3. Finally switch to `deny` — fully enforce the policy once remediation is complete.

> **lightbulb** Rollout checklist: apply the ConstraintTemplate, create Constraints in `dryrun` mode, monitor recorded violations and fix offending resources, switch to `warn` for visibility, then set `enforcementAction: deny` when remediation is complete.

> **warning** Important: Applying `deny` without a phased rollout can cause outages. Always run `dryrun` first and ensure teams have time to remediate violations before enforcing.

## Debugging Gatekeeper

* If a ConstraintTemplate fails to register, inspect its `status` for Rego syntax or schema errors.
* Use `kubectl get` and `kubectl describe` to inspect ConstraintTemplates, Constraints, and recorded violations.
* Gatekeeper records violations even when rejecting requests — violations appear in the Constraint status.
* Check the Gatekeeper controller logs for runtime errors, webhook connectivity issues, or other controller-side problems.

Common troubleshooting steps:

* Verify the ConstraintTemplate is Ready and has no Rego compile errors.
* Confirm the constraint `kind` exactly matches the CRD name created by the template.
* Ensure the Gatekeeper controller pods and webhook services are healthy and reachable by the API server.

## Useful commands and examples

| Operation                           | Command                                                                                          | Notes / Example Output                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| List ConstraintTemplates            | `kubectl get constrainttemplate`                                                                 | Example output: `k8srequiredlabels   True`          |
| List Constraints of a type          | `kubectl get k8srequiredlabels`                                                                  | Example output: `require-team-label  deny  12`      |
| Inspect violations for a constraint | `kubectl get k8srequiredlabels require-team-label -o jsonpath='{.status.violations[*].message}'` | Shows violation messages recorded on the constraint |
| Check Gatekeeper controller logs    | `kubectl logs -n gatekeeper-system deployment/gatekeeper-controller-manager`                     | Use to debug controller-side errors                 |

## Common issues

* Rego syntax errors or invalid schema in the ConstraintTemplate (check `kubectl describe constrainttemplate <name>` and `.status`).
* Misconfigured webhook or API server connectivity problems.
* Gatekeeper controller pods not running or crashing — check pod status and logs.

## Summary

Gatekeeper enforces policies using a clear two-resource model:

* ConstraintTemplates define Rego logic once and register a CRD.
* Constraints instantiate that CRD to define where and how to apply the logic using parameters.

Key Rego inputs for admission policies:

* `input.review` — the admissionReview object; `input.review.object` is the resource.
* `input.parameters` — values supplied by the Constraint.

Always follow a phased rollout: `dryrun` → `warn` → `deny`. Practice authoring ConstraintTemplates and Constraints, test them in `dryrun`, and monitor violations before enforcing to prevent surprises.

## Links and reference

* [Gatekeeper documentation](https://open-policy-agent.github.io/gatekeeper/)
* [Open Policy Agent (OPA) — Rego language docs](https://www.openpolicyagent.org/docs/latest/policy-language/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/f677c67f-5636-431f-9ce8-edca2d1c5c9d)
