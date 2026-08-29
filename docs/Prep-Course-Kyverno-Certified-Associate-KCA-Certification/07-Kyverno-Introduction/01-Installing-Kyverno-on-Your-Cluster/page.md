# Optional
exceptions:
  - path/to/exception.yaml
variables: values.yaml
results:
  # Assertions follow here...
  ...
```

Concrete example with results

```yaml theme={null}
apiVersion: cli.kyverno.io/v1alpha1
kind: Test
metadata:
  name: my-policy-test-suite
# --- INPUTS ---
policies:
  - policy.yaml
resources:
  - good-pod.yaml
  - bad-pod.yaml
exceptions:
  - exception.yaml  # Optional
variables: values.yaml  # Optional

# --- EXPECTED OUTPUTS ---
results:
  - policy: my-policy          # Name of the policy under test
    rule: my-rule             # Name of the specific rule in the policy
    resource: good-pod        # Resource filename (or resource identifier)
    result: pass              # Expected result: pass, fail, skip, or warn

  - policy: my-policy
    rule: my-rule
    resource: bad-pod
    result: fail
```

Notes on fields

* `policies` and `resources` are file paths (relative or absolute) the runner reads.
* `variables` points to a values file if your policies use substitutions.
* The `results` list is the core: each entry maps a `policy`, `rule`, and `resource` to an expected `result`.

Testing validate rules

* For validation-style rules, asserting the evaluation outcome (`pass`, `fail`, `skip`, or `warn`) is usually sufficient:

```yaml theme={null}
# --- EXPECTED OUTPUTS ---
results:
  - policy: my-validation-policy
    rule: check-labels
    resource: good-pod
    result: pass
```

Testing mutate and generate rules

* For mutate rules, you must verify the actual mutation. Use `patchedResource` with the expected post-mutation YAML.
* For generate rules, use `generatedResource` to assert the exact generated resource content.
* The test runner performs a deep comparison between actual and expected files, making assertions precise for complex transformations.

Examples:

```yaml theme={null}
# Mutate example
results:
  - policy: mutate-policy
    rule: add-label
    resource: input-pod
    result: pass
    patchedResource: expected-pod-after-mutate.yaml

# Generate example
results:
  - policy: generate-policy
    rule: create-config
    resource: source-pod
    result: pass
    generatedResource: expected-generated-configmap.yaml
```

<Callout icon="warning">
  When asserting mutated/generated resources, ensure your expected YAML files account for defaulted fields and ordering differences. Use exact, deterministic fixtures to avoid false negatives.
</Callout>

Running the test suite

1. Place:
   * `kyverno-test.yaml` (or `.yml`)
   * policy files
   * resource fixtures
   * expected `patchedResource`/`generatedResource` files
2. Run the CLI from the directory (use `.` for current directory):

```bash theme={null}
kyverno test .
```

Sample CLI output

```bash theme={null}
$ kyverno test .
Loading test (kyverno-test.yaml) ...
Loading values/variables ...
Loading policies ...
Loading resources ...
Loading exceptions ...
Applying 1 policy to 1 resource ...
Checking results ...

| ID | POLICY               | RULE               | RESOURCE        | RESULT | REASON |
|----|----------------------|--------------------|-----------------|--------|--------|
| 1  | disallow-latest-tag  | require-image-tag  | Pod/myapp-pod   | Pass   | Ok     |
| 2  | disallow-latest-tag  | validate-image-tag | Pod/myapp-pod   | Pass   | Ok     |

Test Summary: 2 tests passed, 0 tests failed
```

Why integrate `kyverno test` in CI/CD?

* Detect regressions when policies change.
* Provide deterministic, automated verification for policy libraries.
* Improve confidence for policy maintainers and reduce manual verification effort.

<Frame>
  <img alt="The image contains a summary of three key points related to formal test suites for policies: the goal of creating a suite, the significance of the kyverno-test.yaml file, and the concept of declarative testing." />
</Frame>

Recap

* `kyverno test` is a declarative framework to assert policy behavior across resources and scenarios.
* The `kyverno-test.yaml` file defines inputs (policies, resources, exceptions, variables) and expected outputs (results).
* Use simple `result` assertions for validate rules; use `patchedResource`/`generatedResource` to verify mutate and generate rules.
* Add `kyverno test` into CI/CD pipelines to automatically catch regressions and give policy authors confidence when changing policies.

Links and references

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kyverno CLI reference: [https://kyverno.io/docs/kyverno-cli/](https://kyverno.io/docs/kyverno-cli/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/bc8afdcd-5b51-4efb-8c55-55461a1d242e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/e1ffade5-13b7-4ce8-a881-187e47441680" />
</CardGroup>


# Installing Kyverno on Your Cluster

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Installing-Kyverno-on-Your-Cluster/page

Instructions for installing Kyverno on Kubernetes with Helm, explaining standalone versus high availability modes, installation commands, verification steps, and RBAC and resource setup.

Now that we understand Kyverno's architecture, let's install it.

The recommended method is to use Helm — the Kubernetes package manager. The Kyverno Helm chart packages all required Kubernetes resources, sensible production defaults, and simplifies upgrades and configuration. Using the chart avoids manually creating many YAML manifests for deployments, services, and RBAC.

<Frame>
  <img alt="The image is an infographic about installing Kyverno with Helm, highlighting Helm as a package manager for Kubernetes, and describing its benefits such as bundling resources, managing complexity, and easy management." />
</Frame>

Installation modes

* Standalone — single replica of each Kyverno controller. Best for learning, development, or small test clusters because it consumes fewer resources.
* High availability (HA) — multiple replicas of each controller. Required for production to ensure policy enforcement continues if a controller instance fails.

<Frame>
  <img alt="The image illustrates two installation options: Standalone Installation, ideal for learning and development with a single controller copy, and High Availability Installation, suitable for production with multiple controller copies for reliability." />
</Frame>

<Callout icon="warning">
  For production use, deploy Kyverno in high availability mode so multiple controller replicas can handle failures and maintain continuous policy enforcement.
</Callout>

Quick install (standalone)
We'll perform a simple standalone install using Helm. These three commands add the Kyverno chart repo, refresh your local index, and install Kyverno into the `kyverno` namespace:

```bash theme={null}
