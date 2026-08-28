# List namespace-scoped reports
kubectl get policyreport --all-namespaces

# List cluster-scoped reports
kubectl get clusterpolicyreport --all-namespaces

# Inspect a single report (replace <name> and <namespace>)
kubectl describe policyreport <name> -n <namespace>
```

Report types at a glance

| Resource Type       | Scope            | Typical Use                                                                                          |
| ------------------- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| PolicyReport        | Namespace-scoped | Details results for policies that apply within a namespace; useful for per-team or per-app reporting |
| ClusterPolicyReport | Cluster-scoped   | Aggregates results across the cluster; ideal for security/ops dashboards and compliance exports      |

How reporting solves Alex’s problems

* Logs → Reports: Audit-mode policies continue to allow developer workflows while emitting structured report entries that are easy to query and aggregate.
* Existing resources: Background scans evaluate the current state of resources and populate reports for pre-existing workloads, closing the visibility gap.
* Compliance artifacts: With reports stored as Kubernetes resources, you can generate formal compliance exports, drive dashboards, and automate notifications.

<Frame>
  <img alt="The image shows a challenge faced by Alex, who is seeking a consolidated view of a cluster's compliance state. There's a graphic of Alex with a speech bubble quoting the dilemma." />
</Frame>

Next steps in this lesson

1. Deep dive into the PolicyReport/ClusterPolicyReport schema and examples.
2. Demonstrate how Audit policies create report entries in real time.
3. Configure and run background scans to populate reports for all existing resources.
4. Export and aggregate reports for compliance dashboards and stakeholder reporting.

References and further reading

* [Kyverno Documentation - PolicyReport](https://kyverno.io/docs/writing-policies/reporting/)
* [Kubernetes API Concepts](https://kubernetes.io/docs/concepts/overview/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/360718cb-5ab8-44a1-bcd2-beae95ede7c9/lesson/58401c97-2b36-4ada-af97-0f40d3ef1d78" />
</CardGroup>


# Any and All Statements

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Any-and-All-Statements/page

Explains using Kyverno's any and all resource filters to combine matching criteria (OR and AND) with examples and evaluation behavior.

When writing Kyverno policies, you often need to express complex matching criteria. Earlier we learned how to combine filters like `kinds`, `names`, and `selector` within a single `resources` block — those are implicitly combined with logical AND. But what if you need to express alternatives (OR) or require that several independent filter blocks all match (AND)? Kyverno provides `any` and `all` for exactly this purpose.

This article explains how to use `any` (OR) and `all` (AND) resource filters in Kyverno policies, including examples and evaluation behavior so you can craft precise policy scopes.

## any (OR)

The `any` block implements logical OR. The rule matches if at least one of the filter blocks under `any` matches the resource or request.

Example: match either Deployments labeled `app: critical` OR any StatefulSet.

```yaml theme={null}
match:
  any:  # Match if Block 1 OR Block 2 is true
    - resources:  # Block 1: Critical Deployments
        kinds:
          - Deployment
        selector:
          matchLabels:
            app: critical
    - resources:  # Block 2: All StatefulSets
        kinds:
          - StatefulSet
```

Behavior:

* This policy applies to a Deployment that has the `app: critical` label, or to any StatefulSet (regardless of labels).
* Use `any` when multiple, different criteria should grant a match — for example, different resource types or different identity-based rules that share the same policy action.

## Combining different filter types under `any`

Under `any` you can mix different top-level filter types, such as `resources`, `clusterRoles`, `subjects`, etc. Kyverno evaluates the blocks in order and stops as soon as one block matches.

Example: match if the resource is a Deployment OR if the requesting user has the `cluster-admin` cluster role:

```yaml theme={null}
match:
  any:
    # Block 1: Matches based on the resource
    - resources:
        kinds:
          - Deployment
    # Block 2: Matches based on the cluster roles of the user
    - clusterRoles:
        - cluster-admin
```

Evaluation notes:

* If Block 1 matches (e.g., the object is a Deployment), Kyverno considers the rule matched and will not need to evaluate further blocks.
* If Block 1 does not match, Kyverno evaluates Block 2 and checks the requester's identity. If the requester has `cluster-admin`, the rule matches regardless of the resource type.

## all (AND)

The `all` block implements logical AND. The rule matches only if every filter block listed under `all` matches. Use `all` when you require multiple independent conditions to be true simultaneously.

Example: match only Deployments that both have the label `app: critical` AND are named `frontend-app`.

```yaml theme={null}
match:
  all: # Match if Block 1 AND Block 2 are true
    - resources: # Block 1: Is it a critical Deployment?
        kinds:
          - Deployment
        selector:
          matchLabels:
            app: critical
    - resources: # Block 2: AND is its name 'frontend-app'?
        kinds:
          - Deployment
        names:
          - "frontend-app"
```

Behavior:

* A Deployment must satisfy both conditions to match: it must have the `app: critical` label and be named `frontend-app`.
* If either block fails to match, the rule will not apply.

## Quick comparison table

| Operator | Logical meaning                           | When to use                                           | Example use case                                                    |
| -------- | ----------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------- |
| `any`    | OR — matches if any block is true         | Broaden scope to multiple alternative targets         | Apply one policy to either Deployments with a label OR StatefulSets |
| `all`    | AND — matches only if all blocks are true | Narrow scope to resources that meet multiple criteria | Enforce policy only for resources with a particular name and label  |

## Kyverno evaluation model

* Top-level `match` filters can be standard filters (like `resources`) or combinators (`any`/`all`).
* Kyverno evaluates the combinator blocks in sequence; for `any`, evaluation can short-circuit on the first match.
* The same combinator logic (`any`/`all`) is used in `exclude` blocks to define exceptions.

<Frame>
  <img alt="The image compares the usage of &#x22;any&#x22; (OR) and &#x22;all&#x22; (AND) in decision-making, emphasizing &#x22;any&#x22; as a broad rule and &#x22;all&#x22; as specific and strict." />
</Frame>

<Callout icon="lightbulb">
  A `match` block can contain direct filter blocks (for example, `resources`) or it can use `any`/`all` to combine multiple filter blocks. Use `any` when you want OR semantics and `all` when you want AND semantics.
</Callout>

The `exclude` block, which creates exceptions, uses the same `any`/`all` logic — the concepts explained here apply to it as well.

That's it for this lesson.

Further reading and references:

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kyverno match examples: [https://kyverno.io/docs/writing-policies/match-examples/](https://kyverno.io/docs/writing-policies/match-examples/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/8b35dfbd-8dd8-43c1-a34f-c6cc007a7493" />
</CardGroup>
