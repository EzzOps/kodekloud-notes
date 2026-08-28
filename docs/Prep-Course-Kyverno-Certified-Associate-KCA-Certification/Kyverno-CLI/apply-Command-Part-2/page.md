# apply Command Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-CLI/apply-Command-Part-2/page

Using kyverno apply to produce PolicyReport output, test policies against live clusters, validate PolicyExceptions, and supply Values files for accurate local policy evaluation.

In the previous lesson we covered the basic Kyverno `apply` workflow: testing a single policy against a single resource for quick local feedback. This article expands on that foundation and shows how to get machine-readable reports, evaluate policies against live clusters, honor PolicyExceptions, and supply external context for accurate local evaluation.

<Frame>
  <img alt="The image illustrates a process of local testing using &#x22;kyverno apply,&#x22; showing a flow from policy to resource, with options for generating a formal report and testing policies in running resources." />
</Frame>

Reporting: produce a PolicyReport for automation and CI/CD

By default `kyverno apply` prints a human-readable summary. For CI pipelines, dashboards, or automated tooling you usually want the same structured `PolicyReport` resource that the in-cluster Kyverno controller emits.

Use `--policy-report` (short `-p`) to output a full `PolicyReport` YAML to stdout:

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml --policy-report
