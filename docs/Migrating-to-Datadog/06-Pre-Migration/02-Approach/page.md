# Approach

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Approach/page

Practical phased migration guide for moving observability to Datadog covering access prerequisites, agent and integration setup, validation, feedback loops, and risk management.

This article outlines a practical, phased approach to migrating observability from one platform to another (for example, to Datadog). We recommend a staged migration that reduces risk, allows incremental validation, and captures learnings that scale across teams.

Quick comparison of migration strategies:

| Strategy          | When to use                                                | Pros                                                                          | Cons                                                               |
| ----------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Phased approach   | Large environments, multiple teams, complex integrations   | Safer rollout, smaller blast radius, iterative validation, reusable artifacts | Longer overall timeline                                            |
| Big-bang approach | Small, simple environments or when cutover window is fixed | Faster full migration                                                         | Higher risk, harder to diagnose missed telemetry and config issues |

<Frame>
  <img alt="The image compares two approaches: the &#x22;Phased Approach,&#x22; which is safer and slower with features moved one at a time, and the &#x22;Big-Bang Approach,&#x22; which involves a full, fast switch with higher risk and less planning." />
</Frame>

<Callout icon="lightbulb">
  For most organizations, a phased migration is the recommended pattern. It enables feedback-driven improvements, reduces risk, and produces repeatable artifacts (charts, config, documentation) that accelerate subsequent teams.
</Callout>

Most migration tasks (agent rollout, integrations, telemetry validation) are similar regardless of approach; the difference is how and when you cut over traffic and retire the old platform. Below we walk through a validated sequence you can adapt to either strategy.

## Initial access and prerequisites

Before installing agents or flipping integrations, gather access and artifacts so engineering teams aren’t blocked.

1. Obtain platform and identity access
   * Identity and access management (IAM) and identity governance systems (for example, [Microsoft Entra ID (Azure AD)](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis) or [AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)). IGA vendors may include tools such as [SailPoint](https://www.sailpoint.com/).
   * Create or request service accounts, roles, and permissions required to install agents and configure platform integrations.
2. Collect installer artifacts and libraries
   * Helm charts or Kubernetes manifests for cluster deployments.
   * Agent packages for VMs, containers, or serverless runtimes.
   * Language-specific instrumentation libraries and SDKs for application code.
3. Prepare environment-specific credentials
   * Cloud account access, API keys, and any secrets needed to onboard telemetry (metrics, traces, logs, and profiling).

<Callout icon="warning">
  Request IAM roles and service account permissions early. Missing privileges are a common cause of migration delays—apply least privilege principles and document required scopes for onboarding.
</Callout>

Make these requests early so platform engineers and application teams can proceed without delays.

<Frame>
  <img alt="The image shows an approach diagram, featuring an engineer accessing IAM, platform packages, and environment, each with specific examples like roles, Helm charts, and cloud accounts." />
</Frame>

## Setting up the environment

Start in a development environment and iterate until telemetry is correct. For Datadog, typical tasks include:

* Deploy the Datadog Agent:
  * Kubernetes: install via Helm chart or DaemonSet.
  * Containers: run the agent as a sidecar or daemon container.
  * VMs: install with package installers (apt, yum) or agent images.
* Enable and configure integrations:
  * Metrics, logs, traces/APM, and continuous profiling.
  * Configure Prometheus-style scrapes for services exposing `/metrics`.
* Tune collection concerns:
  * Log filters and processors to reduce noise and cost.
  * Metric collection intervals and custom tags for better grouping.
  * Trace sampling rules to control ingestion volume.

Use development to validate collection, refine configuration, and confirm ingestion into the new platform before promoting changes to staging and production.

<Frame>
  <img alt="The image illustrates an approach where telemetry data flows from development environments like Kubernetes, Virtual Machines, and Serverless into Datadog, which includes logs, metrics, traces, and profiles, with validation by end users." />
</Frame>

## Validation and feedback loop

A structured validation loop ensures issues are caught early and fixes are distributed as shared artifacts:

* Allow time for telemetry to arrive and stabilize in the platform (metrics graphs, log indices, traces).
* Run user acceptance tests and have engineers validate dashboards, alerts, and traces.
* Capture and prioritize feedback (missing spans, unexpected metrics, noisy logs).

Feedback workflow example:

* Engineers report issues (e.g., missing spans, incorrect metrics, noisy logs).
* Platform team investigates, implements configuration fixes, adds filters, and updates documentation.
* Platform team publishes the fixes and reusable templates (Helm values, config snippets, alert rules) for downstream teams.

<Frame>
  <img alt="The image depicts a flowchart showing communication between engineers and other teams with a platform team. Engineers encounter issues like errors and high CPU usage, while other teams focus on enhancing communication, fixing bugs, and improving documentation." />
</Frame>

That’s it for this article. Thanks for reading and good luck with your observability migration.

## Links and references

* [Datadog documentation](https://docs.datadoghq.com/)
* [Helm](https://helm.sh/)
* [Prometheus overview](https://prometheus.io/docs/introduction/overview/)
* [Microsoft Entra ID (Azure AD)](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)
* [AWS IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-to-datadog/module/3287c1cc-cc8d-4c6d-8ec0-824c87c9eb1b/lesson/8fe0e8e3-3694-4f06-850e-f423c23a8be1" />
</CardGroup>
