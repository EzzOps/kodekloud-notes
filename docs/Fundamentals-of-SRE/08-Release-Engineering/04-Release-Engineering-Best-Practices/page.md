# Release Engineering Best Practices

Source: https://notes.kodekloud.com/docs/Fundamentals-of-SRE/Release-Engineering/Release-Engineering-Best-Practices/page

Practical release engineering best practices to enable safe, automated, and observable deployments using progressive delivery, artifact management, CI/CD, secrets rotation, rollback testing, and continuous communication

In this final lesson we bring together the concepts from the module to describe practical, repeatable patterns for safe releases. Release engineering’s objective is simple: enable change, and make change safe. It sits at the intersection of development speed, operational safety, and executive patience—helping teams deliver features quickly without increasing risk.

A sobering statistic to keep in mind: roughly 70% of outages are caused by changes. Release engineering reduces that risk by making changes predictable, observable, and reversible. The best compliment is that releases are so uneventful nobody notices them.

<Frame>
  <img alt="A presentation slide titled &#x22;Release Engineering for SRE&#x22; with a Venn diagram showing Development Speed, Operational Safety, and Executive Patience overlapping to produce &#x22;Safe Releases.&#x22; Bulleted points state &#x22;70% of outages caused by changes,&#x22; define release engineering as making change safe, and set the goal as &#x22;boring releases.&#x22;" />
</Frame>

## Core principles of safe release engineering

* Automate everything. Any manual step is a future outage vector.
* Use progressive delivery. Validate changes with a small percentage of traffic (e.g., 1%) before full rollout.
* Practice fast, tested rollbacks. If rollback is slower than deployment, the rollback process needs improvement.
* Always verify deployments with smoke tests to get quick feedback.
* Communicate relentlessly—silent deployments tend to become noisy incidents.

<Callout icon="lightbulb">
  Apply automation to policy, approvals, and rollbacks. Automated “safety nets” (canaries, health checks, automatic rollbacks) let you move fast with confidence.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Core Principles&#x22; showing five rounded-card principles—Automate everything; Progressive delivery; Easy, tested rollbacks; Always verify; and Communicate relentlessly—each with a short explanatory note. The slide is copyrighted by KodeKloud." />
</Frame>

## Deployment strategies — choose the right approach

Each strategy has trade-offs. Select the approach that matches your risk tolerance, infrastructure costs, and rollback needs.

| Strategy        | Pattern                                                | When to use                                            | Pros                                                       | Cons                                      |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------- | ----------------------------------------- |
| Blue–Green      | Maintain two identical environments and switch traffic | Critical systems needing near-zero error exposure      | Instant cutover; straightforward rollback                  | Requires duplicate infrastructure         |
| Canary          | Gradual rollout to a small subset of users             | User-facing features and metrics-driven validation     | Limits blast radius; observable behavior on real traffic   | Needs good traffic routing/metrics        |
| Feature flags   | Ship code behind toggles                               | A/B testing, incremental launches, operational control | Turn features on/off without deploys; reduces release risk | Technical debt from stale flags           |
| Rolling updates | Replace instances in small batches                     | Stateless services or safe stateful upgrades           | No duplicate infra required; steady migration              | Coordination needed for DB/schema changes |

Common guidance:

* Blue–Green is best when you can afford duplicate environments and need instant rollback.
* Canary deployments require solid monitoring and automated health gates.
* Feature flags decouple deployment and release — remove flags when stable.
* Rolling updates work well when instances are independent and stateless.

<Frame>
  <img alt="A slide titled &#x22;Deployment Strategies&#x22; showing a comparison table of Blue/Green, Canary, Feature Flags, and Rolling deployments with rows for approach, best-for, examples, and cautions." />
</Frame>

## Artifact repository management

Artifact repositories are the core of a trustworthy software supply chain. They store Docker images, packages, and binaries and provide the guarantees needed for safe, auditable releases.

Why they matter for SREs:

* Security: control what is deployable.
* Compliance: retain audit trails for every version.
* Performance: accelerate retrieval and reduce network variability.
* Disaster recovery: immutable artifacts enable rollbacks and re-deployments.

Best practices:

* Use enterprise registries for production (AWS ECR, Google Artifact Registry) instead of public registries for critical systems.
* Enforce lifecycle policies to limit storage while keeping recovery points.
* Apply strict access control: automation writes, humans read or approve where necessary.
* Make production images immutable and block overwrites.

<Frame>
  <img alt="A presentation slide titled &#x22;Artifact Repository Management&#x22; explaining why it matters for SREs, with four colored boxes: Security, Compliance, Performance, and Disaster Recovery. Each box notes a key goal: control deployments, maintain audit trails, ensure fast/reliable retrieval, and keep immutable backups of deployments." />
</Frame>

Public registries such as Docker Hub are convenient but subject to rate limits, retention policies, and varying security guarantees. For production, prefer cloud registries where you can apply lifecycle and access policies.

Example: create an ECR repository and apply a lifecycle policy to keep only the last 10 production images.

```bash theme={null}
