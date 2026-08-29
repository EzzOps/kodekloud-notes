# Kyverno Architecture Part 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Kyverno-Architecture-Part-2/page

Overview of Kyverno internal architecture and controllers detailing admission, reports, background, and cleanup responsibilities for policy enforcement, reporting, asynchronous processing, and resource housekeeping.

Previously we covered how Kyverno integrates with the Kubernetes API server using webhooks. This article dives into Kyverno’s internal architecture: the controllers that implement policy enforcement, reporting, background processing, and cleanup. Kyverno is implemented as multiple focused controllers rather than a single monolith—each controller has a distinct responsibility and interacts with the API request flow in predictable ways.

## High-level controller responsibilities

* Admission Controller — the synchronous gatekeeper for API requests.
* Reports Controller — collects evaluation results and produces policy reports.
* Background Controller — executes deferred generate and mutate tasks asynchronously.
* Cleanup Controller — removes temporary or stale resources according to cleanup policies.

These controllers collaborate to keep the admission path fast while ensuring comprehensive policy enforcement, reporting, and housekeeping.

## Admission Controller

Think of the Admission Controller as the cluster’s front‑door security guard. It intercepts Create, Update, and Delete requests from the Kubernetes API server and performs synchronous policy checks and modifications before the objects are persisted.

When processing an admission request, the Admission Controller:

* Validates resources using `validate` rules (deny non-compliant resources).
* Applies `mutate` rules to inject defaults, labels, annotations, or sidecar changes.
* Verifies container images using `verifyImages` rules (ensure trusted registries and signatures).
* Validates policy and exception resources themselves to ensure they are well‑formed.
* Dynamically manages webhook registration and TLS certificates for secure, automated integration with the API server.

For non‑blocking follow-up actions (for example, generating supplemental resources or creating policy reports), the Admission Controller creates lightweight work tickets and hands them off to background controllers so the original API request is not delayed.

> **lightbulb** The Admission Controller handles synchronous checks and short mutations. For longer-running or cluster-wide changes (generate/mutate of existing resources, report aggregation), rely on Kyverno’s background controllers—these operate asynchronously to preserve admission performance.

<Frame>
  <img alt="The image is an infographic explaining the functions of an Admission Controller, detailing steps such as receiving requests, processing rules, managing webhooks, validating policies, and creating work for other controllers." />
</Frame>

## Reports Controller

The Reports Controller acts as the cluster’s compliance accountant. It collects the immediate results produced by admission events and augments them with its own background scans across the cluster to produce up‑to‑date policy reports.

Key behaviors:

* Consumes admission event tickets emitted by the Admission Controller.
* Performs periodic/background scans of cluster resources that predate policies (drift detection).
* Aggregates and stores findings into PolicyReports and ClusterPolicyReports for monitoring and auditability.

Reports give operators a combined view of immediate enforcement decisions and the historical or drift-based compliance posture.

<Frame>
  <img alt="The image outlines the functions of a &#x22;Reports Controller&#x22; as a compliance accountant, detailing how it creates policy reports, scans existing resources for policy violations, and provides a comprehensive view of cluster compliance." />
</Frame>

## Background Controller

The Background Controller processes work items that should not block the initial API admission path. When the Admission Controller defers an action—such as generating resources or mutating objects already in the cluster—it emits a ticket that the Background Controller consumes.

Typical responsibilities:

* Generate rules: create new resources in response to triggers (for example, automatically creating a default `NetworkPolicy` when a `Namespace` is created).
* Mutate rules: backfill or modify existing resources (for example, add labels or annotations to all Deployments that were created before a new policy).

Because these operations run asynchronously, they enable eventual consistency across the cluster without slowing down user requests.

> **warning** Generate and background mutate operations are asynchronous. Do not assume immediate, synchronous results from background work—tests and controllers should account for eventual consistency.

<Frame>
  <img alt="The image is an infographic about the &#x22;Background Controller,&#x22; explaining its roles to generate and mutate resources in a computing cluster. It describes generating new resources based on triggers and changing resources already in the cluster." />
</Frame>

## Cleanup Controller

The Cleanup Controller is responsible for removing temporary, obsolete, or otherwise unwanted resources according to cleanup policies. Cleanup policies are custom resources that define what to delete and on what schedule.

How it works:

* Reads CleanupPolicy resources that specify targets and schedules.
* Schedules cleanup jobs (via Kubernetes CronJobs or internal scheduling).
* Executes the cleanup tasks according to the configured schedule (hourly, daily, weekly, etc.).

This automated janitor helps prevent resource sprawl and keeps clusters tidy.

<Frame>
  <img alt="The image describes the Cleanup Controller, an automated janitor for managing cleanup policies, deleting old resources on a schedule, and managing Kubernetes CronJobs." />
</Frame>

## How the pieces fit together — API request flow

1. A request arrives from the Kubernetes API server and is sent to Kyverno’s Admission Controller.
2. The Admission Controller performs synchronous validations, mutations, and image verifications.
3. If follow-up work is required (generate/mutate existing resources, report generation), the Admission Controller creates work tickets.
   * Background Controller: picks up generate and mutate tickets to create or modify resources asynchronously.
   * Reports Controller: consumes admission event tickets and combines them with its background scans to produce PolicyReport objects.
   * Cleanup Controller: executes scheduled cleanup tasks defined by cleanup policies.

This division of labor preserves a fast admission path while ensuring enforcement, reporting, and maintenance tasks are completed reliably.

<Frame>
  <img alt="The image is an architecture diagram illustrating the flow and components of a system, including API server interactions, controllers, and policy management. It features components such as an Admission Controller, Mutating Admission, and Schema Validation, among others." />
</Frame>

## Controller summary and quick reference

| Controller            | Purpose                                        | Typical actions / example                                                       |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------- |
| Admission Controller  | Synchronous gatekeeper for API requests        | Validate, mutate, verify images, manage webhooks and certificates               |
| Reports Controller    | Compliance reporting and drift detection       | Consume admission tickets, run background scans, produce `PolicyReport` objects |
| Background Controller | Asynchronous generate/mutate processing        | Create resources via `generate` rules; backfill/mutate existing resources       |
| Cleanup Controller    | Scheduled removal of temporary/stale resources | Execute cleanup policies via Cron-like schedules                                |

## Links and references

* Kyverno documentation: [https://kyverno.io](https://kyverno.io)
* Kubernetes admission controllers and webhooks: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* PolicyReport API (Kubernetes): [https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#policyreport-v1alpha2-reporting](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#policyreport-v1alpha2-reporting)

Summary

* Admission Controller: synchronous gatekeeper—validates, mutates, and verifies images; manages webhooks and certificates.
* Reports Controller: aggregates admission results and background scans into policy reports.
* Background Controller: executes generate and mutate rules asynchronously for cluster-wide or pre-existing resources.
* Cleanup Controller: schedules and runs cleanup jobs to remove stale or temporary resources.

Together, these controllers enable Kyverno to enforce policies in real time while delegating longer-running or cluster‑wide tasks to specialized, resilient components.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/80d253dc-0b89-4337-99bb-fbbec3c94a0e)
