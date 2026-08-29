# PolicyReport Schema

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Reporting/PolicyReport-Schema/page

Explains Kyverno PolicyReport schema and reports controller generating and interpreting policy evaluation results in Kubernetes

In the introduction, Alex faced a common visibility gap: resources created before policies existed were difficult to identify as non-compliant. Kyverno’s reporting system fills that gap by producing PolicyReport and ClusterPolicyReport resources that summarize policy evaluations across your cluster.

Before we look at how to inspect reports in a live cluster, first understand what a report is and how it’s generated.

Who creates reports?

The reports controller is the Kyverno component responsible for generating and updating PolicyReport and ClusterPolicyReport resources. It acts as the central record keeper and receives evaluation results from two primary sources: real-time admission reviews and periodic background scans.

Admission reviews (real-time)
This trigger runs whenever a resource is created or updated. Kyverno evaluates applicable policies during the admission request and the reports controller records an entry for any policy with `spec.admission` set to `true` (the default).

<Frame>
  <img alt="The image describes the &#x22;Reports Controller&#x22; focusing on &#x22;Trigger 1: Admission Reviews,&#x22; detailing the evaluation process of a resource during a CREATE or UPDATE request, and the capture of results from policies with specific admission settings." />
</Frame>

<Callout icon="lightbulb">
  By default, Kyverno policies evaluate both at admission (`spec.admission: true`) and in background scans (`spec.background: true`) unless you explicitly change those fields. Use admission evaluation for immediate enforcement and background scans for periodic compliance checks.
</Callout>

Background scans (periodic)
The second trigger is the background scan, which evaluates policies against resources that already exist in the cluster. Kyverno periodically re-evaluates resources for any policy with `spec.background` set to `true` and forwards those results to the reports controller.

<Frame>
  <img alt="The image outlines two triggers for &#x22;The Reports Controller&#x22;: &#x22;Admission Reviews&#x22; (real-time evaluations) and &#x22;Background Scans&#x22; (periodic scans of existing resources), including their purposes and methods." />
</Frame>

Consolidation by the reports controller
The reports controller merges results from both admission reviews and background scans into PolicyReport (namespaced) and ClusterPolicyReport (cluster-scoped) resources. This consolidation provides a single source of truth for policy compliance across your cluster.

<Frame>
  <img alt="The image is a diagram explaining how the Reports Controller consolidates results from &#x22;Admission Reviews&#x22; and &#x22;Background Scans&#x22; into &#x22;PolicyReport & ClusterPolicyReport&#x22; resources. It includes a description of the process." />
</Frame>

Report types

Which report type is used depends on the evaluated resource’s scope:

| Report type         | Scope          | Evaluated resource examples        |
| ------------------- | -------------- | ---------------------------------- |
| PolicyReport        | Namespaced     | `Pod`, `Deployment`, `Service`     |
| ClusterPolicyReport | Cluster-scoped | `Namespace`, `Node`, `ClusterRole` |

<Frame>
  <img alt="The image is a table comparing PolicyReport (Namespaced) and ClusterPolicyReport (Cluster-Scoped) types, detailing their kind, scope, applicable resources, and examples." />
</Frame>

What does a PolicyReport look like?

A PolicyReport is essentially a report card for a single Kubernetes resource. It has three primary sections:

* Scope: identifies the resource (kind, name, namespace).
* Results: an array with one entry per policy rule evaluated against that resource.
* Summary: aggregated counts for `pass`, `fail`, `warn`, `error`, and `skip`.

Example (truncated) PolicyReport:

```yaml theme={null}
apiVersion: wgpolicyk8s.io/v1alpha2
kind: PolicyReport
metadata:
  # ...
results:
  - policy: disallow-capabilities
    rule: disallow-capabilities
    result: pass
  - policy: disallow-host-namespaces
    rule: disallow-host-namespaces
    message: 'validation error: ...'
    result: fail
  # ...
scope:
  kind: Pod
  name: nginx-pod
  # ...
summary:
  error: 0
  fail: 2
  pass: 10
  skip: 0
  warn: 0
```

The results array is the most important section for troubleshooting: each element corresponds to a single rule evaluation and indicates the outcome.

Breaking down a single result entry

Each result entry contains the fields you’ll use to identify and prioritize violations:

* `policy`, `rule`: which policy and rule were evaluated.
* `result`: the evaluation outcome (`pass`, `fail`, `skip`, `warn`, `error`).
* `message`: human-readable description of the validation or error (critical for debugging).
* Additional optional fields: `category`, `severity`, `scored`, `source`, etc., which help with filtering and prioritization.

Example result entry:

```yaml theme={null}
- category: Pod Security Standards (Baseline)
  message: 'validation error: Sharing the host namespaces is disallowed...'
  policy: disallow-host-namespaces
  result: fail
  rule: host-namespaces
  scored: true
  severity: medium
  source: kyverno
```

Understanding result values

The possible outcomes provide context beyond binary pass/fail and support auditability:

| Result | Meaning                                                                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| pass   | The resource complies with the rule.                                                                                               |
| fail   | The resource violated the rule and is non-compliant.                                                                               |
| skip   | The rule did not apply (e.g., a precondition wasn't met or an exception applied). Not a pass or fail, but part of the audit trail. |
| warn   | A soft failure; violation is reported as a warning rather than enforced.                                                           |
| error  | An issue occurred while processing the rule (e.g., policy syntax or evaluation error). Indicates the need to debug the policy.     |

<Frame>
  <img alt="The image is a table explaining the core outcomes of rule evaluations, including results like &#x22;pass,&#x22; &#x22;fail,&#x22; &#x22;skip,&#x22; &#x22;warn,&#x22; and &#x22;error,&#x22; with brief descriptions for each." />
</Frame>

Recap

In this lesson you learned:

1. The reports controller consolidates evaluations from admission reviews (real-time) and background scans (periodic).
2. There are two report types that correspond to resource scope: namespaced PolicyReport and cluster-scoped ClusterPolicyReport.
3. A PolicyReport contains a summary and a results array; the results array is where you’ll analyze compliance issues.
4. The result values (`pass`, `fail`, `skip`, `warn`, `error`) provide an audit trail that indicates compliance, intentional skips, or policy processing errors.

<Frame>
  <img alt="The image is a summary list detailing four aspects of reporting: the reporter, report types, content, and the audit trail, each with a brief explanation. It features a gradient background and bullet points numbered from 01 to 04." />
</Frame>

Next steps

You now have the foundation to read and interpret PolicyReport resources. In the next lesson we will demonstrate how reports are generated in a cluster and how to query and filter PolicyReports and ClusterPolicyReports to prioritize remediation.

References

* Kyverno Reporting (official docs): [https://kyverno.io/docs](https://kyverno.io/docs)
* Kubernetes API conventions: [https://kubernetes.io/docs/reference/using-api/api-concepts/](https://kubernetes.io/docs/reference/using-api/api-concepts/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/360718cb-5ab8-44a1-bcd2-beae95ede7c9/lesson/061f97c9-92c2-404c-b49a-8988d2a07c10" />
</CardGroup>
