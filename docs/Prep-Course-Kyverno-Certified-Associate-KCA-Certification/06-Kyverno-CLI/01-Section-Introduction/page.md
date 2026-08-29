# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-CLI/Section-Introduction/page

Explains using the Kyverno CLI to shift validation left, enabling local policy validation, mutation, and testing to catch Kubernetes configuration errors before applying to clusters.

So far, our journey with Kubernetes has focused on what happens inside a running cluster. We've applied admission policies, managed resources in the background, and generated compliance reports.

But what if we could catch configuration errors earlier—before resources ever reach the cluster API server? Moving testing and validation earlier in the development lifecycle is commonly called "shifting left," and it's exactly what the Kyverno CLI enables.

In this lesson you will learn how the Kyverno CLI helps developers validate resources locally and get faster feedback, reducing friction between platform teams and application developers.

Let's put ourselves in Alex's shoes again, but

<Frame>
  <img alt="The image features an illustration with a person holding a wrench in front of a large monitor displaying coding elements, accompanied by gears. On the right, there is a ring with the text &#x22;Kyverno CLI,&#x22; set against a white background with the heading &#x22;Shifting Lift.&#x22;" />
</Frame>

this time he is a developer.

The platform team has done a great job deploying Kyverno policies to the cluster. But Alex's new deployment keeps getting blocked by those policies.

Alex writes a manifest for his application and, confident it's correct, runs:

```bash theme={null}
kubectl apply -f deployment.yaml
```

A short time later the API server returns an error: Kyverno's admission controller has denied the request.

```text theme={null}
Error from server: admission webhook "validate.kyverno.svc" denied the request: resource validation failed
```

<Frame>
  <img alt="The image illustrates a workflow problem faced by &#x22;Alex&#x22; while writing a 'deployment.yaml' file and running 'kubectl apply', resulting in an error due to a webhook denial." />
</Frame>

Now Alex must read the error, switch back to his editor, attempt a fix, and push the change again. This reactive cycle creates a slow feedback loop because validation happens too late in his workflow.

There has to be a better way: how can Alex test this deployment locally before it ever touches the cluster? The Kyverno CLI was built to solve this exact problem by allowing validation, mutation, and testing of resources outside the cluster.

To solve Alex's slow feedback loop and empower developers, this lesson will teach you how to use the Kyverno CLI effectively.

<Callout icon="lightbulb">
  Shifting validation left lets developers catch policy violations locally, shorten development cycles, and reduce failed deployments. The Kyverno CLI provides local `validate`, `apply` (for mutation + validation), and `test` commands to run policy checks before kubectl ever talks to the API server.
</Callout>

First, we'll cover the basics: what the CLI is for and how to install it. Next, we'll focus on the most common developer use case: `kyverno apply`, which lets you validate and mutate manifests locally—directly addressing Alex's problem. Finally, for policy authors and maintainers, we'll explore `kyverno test`, which enables formal test cases and unit-testing practices for your policy-as-code repository.

Below is a quick learning agenda of the lesson:

| Topic                                    | Why it matters                                                                    | Example / Command                                                                                      |
| ---------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| What is Kyverno CLI                      | Understand capabilities: validate, mutate, test locally                           | N/A                                                                                                    |
| Install Kyverno CLI                      | Get the CLI on your workstation for offline checks                                | `curl -sSL https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_amd64.tar.gz` |
| Validate & Mutate (`kyverno apply`)      | Fast feedback for developers — validate and apply policy-driven mutations locally | `kyverno apply . --resource deployment.yaml`                                                           |
| Unit tests for policies (`kyverno test`) | CI-friendly tests for policy authors and reviewers                                | `kyverno test ./policies --policy policy.yaml`                                                         |

<Callout icon="warning">
  If you rely only on cluster admission for validation, developers will encounter errors late in the cycle. Use `kyverno apply` and `kyverno test` locally and in CI to prevent repeated failed deployments.
</Callout>

<Frame>
  <img alt="The image outlines a learning agenda with three key topics: understanding the CLI and installation, validating resources with &#x22;kyverno apply,&#x22; and creating test cases with &#x22;kyverno test.&#x22;" />
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/55014898-9a75-4e98-a230-99fa7027c349" />
</CardGroup>
