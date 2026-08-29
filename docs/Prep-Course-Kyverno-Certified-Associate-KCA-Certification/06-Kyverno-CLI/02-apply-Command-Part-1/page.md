# apply Command Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-CLI/apply-Command-Part-1/page

Guide to using the Kyverno CLI and kyverno apply to locally validate Kubernetes policies and manifests for fast feedback, enforcement simulation, and CI integration.

In the introduction we saw Alex's frustration with the slow feedback loop: edit YAML, apply to a cluster, then wait to discover the resource is non-compliant. This lesson fixes that by letting you validate policies and manifests locally — fast.

What is the Kyverno CLI?

The Kyverno CLI is a standalone command-line tool for authoring, testing, and validating Kyverno policies and Kubernetes resources outside of a cluster. It runs the same evaluation engine as the in-cluster Kyverno admission controller, so you can get accurate, instant feedback on your workstation or inside CI/CD.

<Frame>
  <img alt="The image features a text box with an explanation of the Kyverno CLI as a standalone, command-line tool for interacting with Kyverno policies and resources outside of a cluster." />
</Frame>

Key benefit: local policy testing and "shift left"

One of the most valuable features — and the focus of this lesson — is the CLI's ability to test policies against one or more resources entirely locally. You do not need cluster access to check whether a manifest complies with a policy. This reduces debugging time, avoids failed deploys, and is ideal for adding checks to CI pipelines.

<Frame>
  <img alt="The image displays key features of Kyverno CLI, including local policy testing, instant feedback, CI/CD integration, and &#x22;shift left&#x22; for compliance checks. Each feature is briefly described with associated icons." />
</Frame>

Installation

Install the Kyverno CLI using the method that best fits your platform and workflow:

| Method                | Platform                   | Command / Link                                                              |
| --------------------- | -------------------------- | --------------------------------------------------------------------------- |
| Homebrew              | macOS / Linux (Homebrew)   | `brew install kyverno`                                                      |
| kubectl plugin (krew) | Any OS with kubectl + krew | `kubectl krew install kyverno` (enables `kubectl kyverno`)                  |
| Arch Linux (AUR)      | Arch Linux                 | `yay -S kyverno-git` — see `https://aur.archlinux.org/packages/kyverno-git` |
| Manual download       | Any                        | Releases: `https://github.com/kyverno/kyverno/releases`                     |
| Build from source     | Any (Go required)          | Clone and build: `https://github.com/kyverno/kyverno` — run `make build`    |

For this lesson we'll assume the `kyverno` executable is on your PATH (or you run `kubectl kyverno` if installed via krew).

The command we'll master: kyverno apply

`kyverno apply` simulates the Kyverno admission controller locally. It accepts policy files and one or more resource manifests, evaluates resources against the rules, and prints a concise summary indicating pass/fail status.

<Frame>
  <img alt="The image discusses the core command 'kyverno apply', explaining that it simulates how the Kyverno admission controller evaluates a resource." />
</Frame>

Basic usage

```bash theme={null}
kyverno apply <path-to-policy.yaml> --resource <path-to-resource.yaml> --resource <path-to-resource2.yaml>
```

Simple test case: a single policy and a pod manifest

Create two local files:

1. `policy.yaml` — ClusterPolicy that enforces every Pod to have `metadata.labels.purpose: production`.
2. `pod.yaml` — Pod manifest that initially omits labels.

policy.yaml:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-purpose-label
spec:
  rules:
    - name: require-purpose-label
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        failureAction: Enforce
        message: "You must have label `purpose` with value `production`."
        pattern:
          metadata:
            labels:
              purpose: production
```

pod.yaml (initial, missing labels):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
spec:
  containers:
    - name: nginx
      image: nginx:1.12
```

Run the CLI to verify the pod against the policy.

Failing run (when the label is missing):

```bash theme={null}
$ kyverno apply policy.yaml --resource pod.yaml
Applying: 3 policy rule(s) to 1 resource(s)...
policy require-purpose-label -> resource default/Pod/my-app-pod failed:
1 - require-purpose-label validation error: You must have label `purpose` with value `production`. rule require-purpose-label failed at path /metadata/labels/
pass: 0, fail: 1, warn: 0, error: 0, skip: 0
```

Why does the output say "Applying: 3 policy rule(s)..." when the file only defines one rule?

Kyverno generates Autogen Rules for related controllers (Deployments, StatefulSets, Jobs, CronJobs, etc.) based on your Pod rule. This ensures coverage for resources created by controllers without requiring you to write duplicate rules. The CLI reports each generated rule when evaluating.

> **lightbulb** Kyverno's Autogen Rules expand a single Pod rule into additional rules for common controllers (Deployments, StatefulSets, Jobs, CronJobs, etc.), which is why a single policy can appear as multiple evaluated rules.

Fix the manifest and re-run

Alex adds the required label to his Pod:

pod.yaml (updated):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  labels:
    purpose: production
spec:
  containers:
    - name: nginx
      image: nginx:1.12
```

Passing run (after adding the label):

```bash theme={null}
$ kyverno apply policy.yaml --resource pod.yaml
Applying: 3 policy rule(s) to 1 resource(s)...
pass: 1, fail: 0, warn: 0, error: 0, skip: 0
```

Command output overview

| Field | Meaning                                                               |
| ----- | --------------------------------------------------------------------- |
| pass  | Number of resources that passed all evaluated rules                   |
| fail  | Number of resources that failed at least one rule                     |
| warn  | Number of resources that triggered a warning rule                     |
| error | Any internal errors during evaluation                                 |
| skip  | Rules or resources skipped (e.g., when policy conditions don't match) |

Wrap up

Using `kyverno apply` lets you shift left: validate policies and manifests locally for immediate feedback, integrate checks into CI/CD, and reduce the cycle time and frustration of trial-and-error cluster deployments. In this lesson we covered the basic `kyverno apply` workflow and demonstrated a simple enforcement policy. The CLI supports many additional flags and advanced scenarios (multiple policies, globbing, JSON/summary outputs) that you'll see in the next lesson.

<Frame>
  <img alt="The image is a summary diagram with four points explaining the goals and benefits of using a CLI tool for testing policies and resources, emphasizing fast feedback, validation commands, workflow, and CI/CD integration. Each point is color-coded and numbered, highlighting different aspects of the tool's functionality and advantages." />
</Frame>

Links and references

* Kyverno CLI GitHub Releases: `https://github.com/kyverno/kyverno/releases`
* Kyverno repository: `https://github.com/kyverno/kyverno`
* Homebrew: `https://brew.sh`
* krew (kubectl plugin manager): `https://krew.sigs.k8s.io`

In the next lesson we'll explore advanced `kyverno apply` flags, multi-file testing, automated CI integration, and output formats for scripting and reporting.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/2e4cf05e-71c7-4191-8513-3a1a48870887)
