# test Command

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-CLI/test-Command/page

Describes using kyverno test to create declarative policy test suites with kyverno-test.yaml, asserting validation mutate and generate outcomes for automated CI CD regression detection.

The `kyverno test` command helps policy authors build automated, repeatable test suites for Kyverno policies. While `kyverno apply` is great for ad-hoc, developer-focused validation, `kyverno test` lets you assert expected behavior across many resources and detect regressions when policies change.

<Frame>
  <img alt="The image illustrates a role titled &#x22;Policy Author&#x22; and highlights the importance of ensuring policies are correct and avoiding breaks when making changes." />
</Frame>

Why unit tests for policies?

* Policy authors need confidence that policies:
  * Pass for valid resources.
  * Fail for invalid resources.
  * Are skipped for excluded resources.
* Manually running `kyverno apply` for many scenarios is error-prone and doesn't scale.
* `kyverno test` provides a declarative test runner to automate these checks in CI/CD pipelines.

<Frame>
  <img alt="The image shows a gear surrounded by circular arrows with a check mark and an X mark, labeled &#x22;Testing.&#x22;" />
</Frame>

Key difference: kyverno apply vs kyverno test

* `kyverno apply`: Imperative, ad-hoc. Use when you want to quickly check how a policy affects a resource during development.
* `kyverno test`: Declarative test framework. Use to assert expected outcomes (pass/fail/skip/warn or expected mutated/generated resources) and run those assertions automatically.

<Callout icon="lightbulb">
  Use `kyverno apply` for interactive debugging; use `kyverno test` to create reproducible assertions suitable for CI/CD and regression detection.
</Callout>

<Frame>
  <img alt="The image is a table comparing &#x22;kyverno apply&#x22; and &#x22;kyverno test&#x22; in terms of use case, question it answers, and workflow. It outlines differences between ad-hoc checks and structured test suites." />
</Frame>

Overview: kyverno-test.yaml (manifest)
The test runner looks for a manifest, conventionally named `kyverno-test.yaml` or `kyverno-test.yml`. This file declares inputs (policies, resources, optional exceptions and variables) and expected outputs (results). Place the manifest and related fixtures in a directory and run the CLI against that directory.

<Frame>
  <img alt="The image explains the &#x22;kyverno test&#x22; command, which uses a file named &#x22;kyverno-test.yaml&#x22; for execution." />
</Frame>

File structure at a glance

* Inputs
  * `policies`: list of policy file paths
  * `resources`: list of resource fixtures
  * `exceptions`: optional exception policies
  * `variables`: optional values file for substitutions
* Results
  * Declarative assertions tying a `policy`, `rule`, and `resource` to an expected `result` (pass/fail/skip/warn)
  * For mutate/generate rules, include `patchedResource` or `generatedResource` to compare the actual output to a file

Minimal example test manifest

```yaml theme={null}
apiVersion: cli.kyverno.io/v1alpha1
kind: Test
metadata:
  name: kyverno-test
policies:
  - path/to/policy.yaml
  - path/to/another-policy.yaml
resources:
  - path/to/good-resource.yaml
  - path/to/bad-resource.yaml
