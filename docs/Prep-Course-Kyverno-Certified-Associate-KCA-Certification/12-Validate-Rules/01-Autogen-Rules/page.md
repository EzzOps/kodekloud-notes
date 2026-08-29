# Autogen Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Autogen-Rules/page

Explains Kyverno autogen which generates controller-specific Kubernetes validation rules from a single Pod-focused policy to reduce duplication and simplify image registry enforcement

This article expands on validation policies and introduces Kyverno's autogen feature — a powerful way to automatically generate controller-specific rules from a single Pod-focused policy. Autogen reduces repetition, minimizes errors, and keeps policies maintainable as new controllers or operators are introduced.

Let's follow Alex, a platform engineer who needs to ensure all application images come from the enterprise registry.

Alex’s requirement is simple: validate that container images are pulled only from `registry.domain.com/*`. But developers don't usually create Pods directly.

<Frame>
  <img alt="The image outlines a problem titled &#x22;The Pod Controller Maze,&#x22; where Alex's goal is to ensure all container images come from a trusted internal registry, but the challenge is that pods aren't usually created directly and are managed by controllers." />
</Frame>

Instead, workloads are created via Deployments, StatefulSets, DaemonSets, Jobs, CronJobs, and operator-managed resources. Each controller embeds the Pod spec at a different JSON path, so a naive approach requires separate rules for each controller type.

Manual approach (repetitive and error-prone)

Alex starts with a Pod-level validation rule:

```yaml theme={null}
