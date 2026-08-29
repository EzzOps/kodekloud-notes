# Example: steps pattern (array-of-arrays)
spec:
  entrypoint: workflow-steps
  templates:
  - name: workflow-steps
    steps:
      # Phase 1: sequential single step (build)
      - - name: build
          template: build

      # Phase 2: parallel steps (test-a and test-b)
      - - name: test-a
          template: test-a
        - name: test-b
          template: test-b

      # Phase 3: sequential single step (deploy)
      - - name: deploy
          template: deploy
```

DAG example with explicit dependencies:

```yaml theme={null}
# Example: dag pattern
spec:
  entrypoint: workflow-dag
  templates:
  - name: workflow-dag
    dag:
      tasks:
        - name: build
          template: build

        - name: test-a
          template: test-a
          dependencies: [build]

        - name: test-b
          template: test-b
          dependencies: [build]

        - name: deploy
          template: deploy
          dependencies: [test-a, test-b]
```

Tasks whose dependencies are satisfied will run immediately, letting Argo maximize parallelism safely.

> **lightbulb** Use Steps for straightforward, mostly linear pipelines. Choose DAGs when explicit dependency control and multiple concurrent paths are required.

Templates: reusable building blocks

Templates are the modular units of Argo Workflows. Define them once and reuse across workflows. Common template types:

| Template Type | Description                                                                | When to use                                           |
| ------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| container     | Runs a container image; specify `image`, `command`, `args`, `resources`    | Most tasks: builds, tests, CLI tools                  |
| script        | Inline script in Python/Bash/etc.                                          | Small, self-contained logic without a dedicated image |
| resource      | Create/patch/delete Kubernetes resources and optionally wait for readiness | Provisioning CRDs, applying manifests                 |
| suspend       | Pause execution for manual approval or an external signal                  | Human-in-the-loop approvals or manual gating          |

<Frame>
  <img alt="The image outlines four reusable workflow building blocks: Containers, Script, Resources, and Suspend, with descriptions for each." />
</Frame>

WorkflowTemplates and ClusterWorkflowTemplates

WorkflowTemplates provide namespaced, reusable definitions. Use them to create a library of platform tasks. For cluster-wide reuse, use ClusterWorkflowTemplate.

Example WorkflowTemplate (kaniko build):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: build-and-push
spec:
  templates:
    - name: kaniko-build
      inputs:
        parameters:
          - name: repo
      container:
        image: gcr.io/kaniko-project/executor
        args:
          - "--destination={{inputs.parameters.repo}}"
```

Parameters make templates flexible. Pass values at runtime or wire outputs from earlier steps into other templates. For example, a `deploy` template can accept a `namespace` parameter to operate across environments.

Artifacts: reliable file passing between steps

Because each step runs in its own pod with an isolated filesystem, you must use artifacts to pass files between steps. Typical flow:

* Step A writes a file (e.g., `/tmp/artifact.tar`) and declares it as an output artifact.
* Argo uploads that artifact to the configured artifact repository (S3, GCS, MinIO).
* Step B declares the artifact as an input and Argo downloads it into the pod before the step runs.

<Frame>
  <img alt="The image is a flowchart illustrating how data is passed between steps using artifacts, with a process from step A (Output Artifact) to step B (Consume) via &#x22;artifact.tar,&#x22; involving tools like S3, Google Cloud Storage, and MinIO." />
</Frame>

Producer/consumer artifact example

Producer template snippet (writes `/tmp/msg.txt` and exposes it as an output artifact):

```yaml theme={null}
# Producer template: writes /tmp/msg.txt and uploads as artifact "message"
outputs:
  artifacts:
    - name: message
      path: /tmp/msg.txt
# (This would be defined inside a template's container/script block that creates /tmp/msg.txt)
```

Consumer template snippet (declares `message` as an input artifact and reads it):

```yaml theme={null}
# Consumer template: declares input artifact "message" and uses it in the container
inputs:
  artifacts:
    - name: message
      path: /tmp/msg.txt
container:
  image: alpine
  command: [cat, /tmp/msg.txt]
```

Configure artifact backends via the artifact repository ConfigMap in the argocd/argo namespace (or your Argo namespace). For local demos use MinIO; for production use S3, GCS, or another supported backend.

Artifacts are ideal for build outputs, test results, generated configs, or any files that subsequent steps require.

Argo Events: external triggers and event-driven automation

Argo Events extends Argo Workflows to react to external events and trigger Workflows (or other actions).

<Frame>
  <img alt="The image illustrates the architecture of event-driven automation using Argo Events, showing a flow from the event source to a sensor and then a trigger." />
</Frame>

Argo Events components

* EventSource: connects to external event streams (Git, webhooks, S3, message queues) and listens for events.
* Sensor: filters and transforms events, extracting parameters (for example, trigger only on pushes to `main` and pass the commit SHA).
* Trigger: performs an action—commonly submits an Argo Workflow.

Example use cases

* Git push triggers a build and deploy pipeline.
* File uploaded to S3 triggers a data processing workflow.
* Creation of a CRD triggers infra provisioning workflows.
* Cron-like schedules trigger nightly cleanup or reporting workflows.

<Frame>
  <img alt="The image illustrates event-driven automation use cases with Argo Events, including scenarios like Git push triggering build pipelines and file uploads leading to data processing." />
</Frame>

Combined architecture

Together, Argo Events + Argo Workflows provide a fully event-driven automation platform. Declare what should happen when an event occurs; the system manages execution, retries, artifacts, and observability.

<Frame>
  <img alt="The image illustrates a process of event-driven automation using Argo Events and Argo Workflows, resulting in a fully event-driven platform automation system." />
</Frame>

Key takeaways

* Workflows are a better fit than scripts for complex platform automation—especially when you need parallelism, retries, and observability.
* Use Steps for simple, mostly linear pipelines; use DAGs when you need explicit dependency graphs and complex concurrency.
* Templates and WorkflowTemplates make automation reusable and parameterizable across teams and environments.
* Artifacts provide reliable file transfer between isolated pods and are essential for build/test artifacts and generated configurations.
* Argo Events adds event-driven capabilities so your automation reacts to external triggers (Git, webhooks, object stores, message queues).

<Frame>
  <img alt="The image outlines four key takeaways about workflows: they are preferable to scripts for complex automation, use DAGs for complex graphs, templates enhance reusability, and artifacts facilitate data transfer between steps." />
</Frame>

Further reading and references

* Argo Workflows documentation: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Argo Events documentation: [https://argoproj.github.io/argo-events/](https://argoproj.github.io/argo-events/)
* MinIO: [https://min.io/](https://min.io/)
* AWS S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Google Cloud Storage: [https://cloud.google.com/storage/](https://cloud.google.com/storage/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/12ee1a17-ba58-41bc-a43d-b7091cd52324)


# Cost for Platforms What Drives Spend and How to Reduce It

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-Architecture-and-Infrastructure/Cost-for-Platforms-What-Drives-Spend-and-How-to-Reduce-It/page

Explains Kubernetes cloud cost drivers, using OpenCost for visibility, and practical strategies to attribute, optimize, and reduce platform spending

This lesson explains the financial side of running Kubernetes: what causes cloud spend, how to make that spend visible, and how to reduce it systematically. By the end you'll have a practical framework and tools to answer: Where is our cloud spend going? Who is spending it? And what can we do to reduce it?

<Frame>
  <img alt="The image outlines five learning objectives related to Kubernetes cost management, including identifying cost drivers, using OpenCost, analyzing spending, implementing cost optimization, and understanding cost management." />
</Frame>

## What actually drives Kubernetes costs?

Consider this real example: a mid-sized SaaS provider saw its monthly Kubernetes cloud bill jump from $30,000 to $120,000 in a year. The cloud invoice showed a large EC2 line item, but the platform team couldn't map those dollars to namespaces, teams, or workloads — so they couldn't tell whether the spend was justified or wasteful.

<Frame>
  <img alt="The image highlights a problem labeled &#x22;Cloud Bill Surprise,&#x22; with subpoints on &#x22;Unplanned Scaling&#x22; and &#x22;K8s Infrastructure.&#x22;" />
</Frame>

<Frame>
  <img alt="The image presents a problem statement regarding resource consumption by engineering teams, highlighting questions about which teams and workloads were responsible and whether the usage was justified or wasteful, with a total EC2 cost of $84,000." />
</Frame>

The operational solution is to introduce namespace-level cost allocation so teams and finance can map cloud dollars to platform constructs. With that visibility you can systematically eliminate unused capacity and right-size resources where it matters most.

<Frame>
  <img alt="The image outlines a solution involving namespace-level cost allocation to identify spending, and using insights to optimize resources and eliminate unused capacity." />
</Frame>

## Major cost categories (and where to focus)

Kubernetes cloud spend generally falls into three primary categories. Prioritize efforts where dollars are concentrated to get the highest ROI.

| Category        | Typical share of spend | What to focus on                                                                                                    |
| --------------- | ---------------------: | ------------------------------------------------------------------------------------------------------------------- |
| Compute (nodes) |                 60–70% | Pay-for-provisioned capacity. Address over-provisioned pods, right-size requests/limits, and use autoscaling.       |
| Storage         |                 15–25% | Persistent volumes, snapshots, and storage class choices (SSD vs HDD). Clean up stale snapshots and unused volumes. |
| Network         |                 10–20% | Egress and cross-region transfer can be costly. Optimize data movement patterns and caching.                        |

<Frame>
  <img alt="The image outlines the factors driving Kubernetes costs, categorized into Compute (60-70% of total spend), Storage (15-25% of total spend), and Network (10-20% of total spend), detailing specific cost contributors for each category." />
</Frame>

The single largest cost driver is provisioned capacity you do not actually use — the gap between what you pay for (node capacity) and what workloads consume. In many organizations that utilization gap represents 40–60% waste. Closing that gap is the highest-leverage optimization.

<Frame>
  <img alt="The image illustrates the cost drivers of Kubernetes, highlighting the gap between paid node capacity and actual workload consumption, with an emphasis on reducing the utilization gap to optimize costs." />
</Frame>

## The visibility gap: cloud bill vs platform usage

The cloud bill shows dollars by account, service, and line item — not by namespace, team, or workload. That mismatch is the visibility gap: finance sees charges, platform engineers see Kubernetes constructs, and neither can easily attribute dollars to business units.

Typical questions to answer:

| Question                               | Example                                            |
| -------------------------------------- | -------------------------------------------------- |
| How much is a team costing us?         | Payments team: `team=payments`                     |
| Which namespace wastes the most?       | Look for low-efficiency namespaces in cost reports |
| Over-provisioned or under-provisioned? | Compare requested resources vs actual usage        |

Bridging this gap requires a tool that understands cloud pricing and Kubernetes resource models. OpenCost is one such open-source solution.

<Frame>
  <img alt="The image illustrates a &#x22;visibility problem&#x22; between cloud billing at the infrastructure level and Kubernetes usage at the platform level, highlighting OpenCost as a bridging solution." />
</Frame>

> **lightbulb** [OpenCost](https://opencost.io) is an open-source, vendor-neutral project (CNCF incubating) that maps Kubernetes usage to cloud pricing so you can attribute dollars to namespaces, labels, and pods.

## OpenCost overview: how it works and what it provides

OpenCost runs inside Kubernetes as a set of pods. It scrapes usage from the Kubernetes Metrics API or Prometheus, overlays cloud pricing, and produces dollar-based allocations.

<Frame>
  <img alt="The image is a slide titled &#x22;OpenCost: Kubernetes Cost Visibility,&#x22; highlighting OpenCost as an open-source, vendor-neutral, CNCF incubating project." />
</Frame>

<Frame>
  <img alt="The image illustrates &#x22;OpenCost: Kubernetes Cost Visibility,&#x22; showing a Kubernetes Cluster with an OpenCost Pod, alongside Metrics API and Pricing data components detailing per-hour node costs, per-GB storage costs, and data transfer costs." />
</Frame>

What OpenCost gives you (three core capabilities):

1. Cost allocation by namespace or label
   * Attributes node, storage, and network costs to namespaces/labels according to pod consumption. Example: if a node costs $1,000/month and a team's pods consume 10% of that node, the team is allocated $100/month.

2. Resource-efficiency metrics
   * Shows CPU/memory utilization vs requests so you can surface over-provisioned (waste) and under-provisioned (risk) workloads.

3. Real-time and historical data
   * Time-series cost trends and anomaly detection (e.g., sudden spikes or month-over-month growth).

<Frame>
  <img alt="The image shows a dashboard of OpenCost displaying Kubernetes cost visibility, with a cost allocation chart for the last 7 days by namespace, indicating zero cost for various resources." />
</Frame>

## How OpenCost calculates costs

OpenCost follows a simple three-step model to turn metrics into dollars:

1. Get cloud pricing
   * Derive per-CPU-hour and per-GB-hour node costs (and storage/network rates) using cloud provider pricing.

2. Measure pod resource usage
   * Collect actual CPU/memory usage. OpenCost charges the higher of the pod's request or its actual usage so both waste and risk are visible.

3. Aggregate by namespace or label
   * Sum pod-level costs into namespace/label totals (for example, all pods labeled `team=payments`).

The result is a concrete allocation such as: the Payments namespace costs \$2,400/month — which closes the visibility gap and enables finance and engineering to act.

<Frame>
  <img alt="The image illustrates cost allocation by namespace, highlighting a monthly expense of $2,400 for the &#x22;team-payments&#x22; namespace, with roles for Finance in allocating cloud costs and Engineering Leadership in identifying costly workloads." />
</Frame>

## Efficiency metric and the target zone

OpenCost computes efficiency as actual usage divided by requests. Interpretations:

* Over-provisioned: Low efficiency (e.g., 12.5%). Large waste — you're paying for far more than you need.
* Right-sized: Efficiency \~60–80% — the recommended target zone balancing cost and headroom for spikes.
* Under-provisioned: Efficiency >100% (e.g., 240%) — the pod is using more than requested and may cause throttling or OOM kills.

Aim for the 60–80% band. Below 50% indicates significant waste; above 90% suggests little headroom and higher operational risk. The right-sizing workflow looks like: profile usage, set requests near the 95th percentile, and target the 60–80% efficiency band.

<Frame>
  <img alt="The image compares three scenarios of CPU usage efficiency: over-provisioned with low efficiency, right-sized with balanced efficiency, and under-provisioned with high efficiency but potential risks." />
</Frame>

<Frame>
  <img alt="The image is a cost-efficiency spectrum comparing requested versus used efficiency, categorized into zones: &#x22;Wasted Money&#x22; (below 50%), &#x22;Target Zone&#x22; (60-80%), and &#x22;High Risk&#x22; (90%+), with the tool OpenCost used to show namespace placement on this spectrum." />
</Frame>

> **warning** Be careful when right-sizing: aggressive reductions can cause production outages. Always validate changes in a staging or canary environment and combine metrics with business context.

## How to reduce costs — an operational roadmap

Cost reduction is continuous. Organize efforts across short, medium, and long horizons and prioritize by dollar impact (start with compute/node costs).

| Horizon                  | Actions                                                                                                                                    | Typical impact                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| Quick wins (this week)   | Right-size requests from observed usage; kill idle dev environments; move non-critical batch jobs to HDD                                   | 20–40% reductions are common                 |
| Medium-term (this month) | Use spot/preemptible instances for tolerant workloads; tune HPA/VPA and cluster autoscaler                                                 | Significant recurring savings                |
| Long-term (quarter-plus) | Build cost-accountability (show teams their costs, set budget alerts); implement quotas and guardrails; embed efficiency into architecture | Cultural and architectural savings over time |

<Frame>
  <img alt="The image outlines cost reduction strategies categorized into quick wins, medium-term, and long-term approaches, each with specific tactics for optimizing resources and saving costs." />
</Frame>

Prioritize your top-dollar namespaces first (e.g., the ten costliest). Often, the biggest ROI comes from right-sizing those namespaces and removing idle nodes.

## Combine visibility with governance

Visibility plus governance creates sustainable cost control:

* Visibility (OpenCost): maps dollars to teams and workloads.
* Governance: quotas, limits, and automated policies prevent runaway consumption.
* Culture: show teams their costs and give them the tools to self-optimize.

When combined, these elements enable continuous cost optimization instead of reactive firefighting.

This concludes the module covering architecture, resources, multi-tenancy, governance, storage, networking, and cost.

## Links and references

* OpenCost: [https://opencost.io](https://opencost.io)
* Amazon EC2 docs: [https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/989346de-0207-4837-af11-bf456d188972/lesson/36ec1768-6ce1-430d-962a-e8359f9c6c1d)
