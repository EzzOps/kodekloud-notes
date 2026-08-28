# Workflow Orchestration DAGs Steps and Event Driven Automation

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Workflow-Orchestration-DAGs-Steps-and-Event-Driven-Automation/page

Explains using Argo Workflows and Argo Events to replace fragile scripts with declarative, parallel, retryable, observable Kubernetes-native automation for complex platform tasks.

Controllers continuously reconcile desired state, but many platform tasks are one-off: data migrations, multi-step environment setup, or ad-hoc provisioning. Imperative Bash scripts or simple CI jobs often lack the expressiveness, retries, observability, and parallelism required for these workflows.

This article explains why scripts fail for complex automation and how to use Argo Workflows and Argo Events to build resilient, declarative, and event-driven platform automation:

* Why scripts and pipelines break for complex platform automation.
* How to author Argo Workflows using Steps and DAG patterns.
* Building reusable WorkflowTemplates with parameters.
* Passing artifacts reliably between steps.
* Triggering workflows from external events with Argo Events.

<Frame>
  <img alt="The image lists two learning objectives: understanding script failures in complex automation and creating Argo Workflows with steps and DAG patterns." />
</Frame>

Problem scenario: a 50-line Bash script to provision a development environment

A platform team had a single Bash script that: created a namespace, applied RBAC, deployed monitoring agents, configured Ingress, and set up DNS. It ran sequentially even though many steps were independent. When a later step (DNS) timed out, the script failed entirely, requiring manual rollback and a full re-run.

<Frame>
  <img alt="The image illustrates a sequential workflow process for a script, detailing seven steps from initialization to potential failure, highlighting issues like no parallelism and lack of retries." />
</Frame>

Because Bash executed everything sequentially, independent steps that could have run concurrently extended the runtime (15 minutes vs 8). When the DNS step failed, there were no retries, backoff, or resumability—manual intervention was required.

<Frame>
  <img alt="The image illustrates a parallel workflow titled &#x22;From Sequential Script to Resilient Workflow,&#x22; detailing seven steps, including &#x22;Create Namespace,&#x22; &#x22;Apply RBAC,&#x22; &#x22;Deploy Monitoring,&#x22; &#x22;Configure Ingress,&#x22; and more, designed to complete in eight minutes." />
</Frame>

Common automation approaches and their limits

The slide shows three common approaches to platform automation: shell scripts, CI pipelines, and CronJobs. Each has limitations for complex orchestration.

<Frame>
  <img alt="The image highlights common limitations of scripts and pipelines, comparing shell scripts, CI pipelines, and CronJobs in terms of aspects like retries, visibility, dependencies, and event ties." />
</Frame>

Table: automation approaches at a glance

| Resource Type |                         Strengths | Limitations                                                                    |
| ------------- | --------------------------------: | ------------------------------------------------------------------------------ |
| Shell script  |     Fast to write for small tasks | Sequential by default, poor retries, limited observability                     |
| CI pipeline   | Integrates with repo/PR workflows | Often linear, limited artifact sharing between stages, varying retry semantics |
| CronJob       |          Good for scheduled tasks | Not event-driven, limited retry/resume support                                 |

Common problems with scripts/pipelines

* No explicit dependency graph (cannot express "run C after A and B" cleanly).
* Sequential execution for many implementations—independent tasks run one after another.
* Little or no retry/backoff/resume semantics.
* Poor observability into the exact failing step or current execution state.

For robust platform automation you need a workflow engine that is Kubernetes-native and declarative.

Why Argo Workflows?

Argo Workflows runs each step as a Kubernetes pod, so you gain all Kubernetes primitives—resource requests/limits, service accounts, RBAC, secrets, node affinity, and priority classes. Workflows are CRDs (YAML), so you can store them in Git for auditable, declarative automation.

<Frame>
  <img alt="The image is a diagram highlighting key elements of Argo Workflows in Kubernetes, featuring topics like Resource Limits, Service Accounts, RBAC, Secrets, and Node Affinity." />
</Frame>

Core capabilities

* DAGs and Steps: express dependencies and control parallelism.
* Retries and timeouts: set per-step retries with backoff, and per-step timeouts.
* Artifacts: share files between steps using S3, GCS, MinIO, etc.
* UI and CLI: visual graphs, logs, task timing and retries; CLI submission and monitoring.

<Frame>
  <img alt="The image outlines the key capabilities of Argo Workflows for Kubernetes-native orchestration, including DAGs and steps, retries and timeouts, artifact passing, and UI and CLI features." />
</Frame>

Expressing execution order: Steps vs DAGs

Argo supports two primary patterns to express execution order:

* Steps: a list-of-lists pattern where the outer list is sequential phases and each inner list contains steps that run in parallel. Best for mostly linear pipelines with some parallel groups.
* DAGs: explicit nodes with dependencies. Best for complex graphs with multiple concurrent paths and explicit dependency control.

Correct Steps example (array-of-arrays):

```yaml theme={null}
