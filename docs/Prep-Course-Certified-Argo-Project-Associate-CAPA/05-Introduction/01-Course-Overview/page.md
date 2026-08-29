# cluster-workflow-template.yaml
apiVersion: argoproj.io/v1alpha1
kind: ClusterWorkflowTemplate
metadata:
  name: global-utility-templates
spec:
  templates:
    - name: global-cowsay
      inputs:
        parameters:
          - name: message
      container:
        image: rancher/cowsay
        command: ["cowsay"]
        args: ["{{inputs.parameters.message}}"]
```

Because ClusterWorkflowTemplate is cluster-scoped, metadata does not include a namespace.

Referencing a ClusterWorkflowTemplate from a namespaced Workflow requires setting the clusterScope flag to true.

Example: calling a single template from a ClusterWorkflowTemplate via templateRef (clusterScope: true)

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: use-single-cluster-template-
spec:
  entrypoint: my-custom-workflow
  templates:
    - name: my-custom-workflow
      steps:
        - - name: first-step
            templateRef:
              name: global-utility-templates   # ClusterWorkflowTemplate name
              template: global-cowsay          # template name inside the ClusterWorkflowTemplate
              clusterScope: true               # required when referencing a cluster-scoped template
            arguments:
              parameters:
                - name: message
                  value: "I called this from a ClusterWorkflowTemplate!"
```

Example: running the whole ClusterWorkflowTemplate via workflowTemplateRef (clusterScope: true)

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: run-whole-cluster-template-
  namespace: argo
spec:
  arguments:
    parameters:
      - name: message
        value: "Hello from a ClusterWorkflowTemplate!"
  workflowTemplateRef:
    name: global-utility-templates
    clusterScope: true
```

> **lightbulb** When referencing cluster-scoped templates (ClusterWorkflowTemplate), always set clusterScope: true in templateRef or workflowTemplateRef. ClusterWorkflowTemplates are not namespaced, so this flag tells Argo the reference is to a cluster-level resource.

## Quick comparison

|                       Resource |       Scope      |   Typical user  | Use case                                       |
| -----------------------------: | :--------------: | :-------------: | :--------------------------------------------- |
|               WorkflowTemplate | Namespace-scoped | App/team owners | Reusable templates within a team namespace     |
|        ClusterWorkflowTemplate |  Cluster-scoped  |  Platform teams | Centralized templates shared across namespaces |
|         Workflow (templateRef) | Namespace-scoped |    Developers   | Import single templates into complex workflows |
| Workflow (workflowTemplateRef) | Namespace-scoped |      Anyone     | Execute a stored template as a full workflow   |

## Links and References

* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [Kubernetes API Concepts](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* [Argo Workflows Templates Reference](https://argoproj.github.io/argo-workflows/workflow-templates/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/a1959e6c-b723-4274-8009-79ea570a924c)


# Course Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Introduction/Course-Overview/page

A lab-focused course preparing learners for Certified Argo Project Associate covering Argo CD, Workflows, Rollouts, Events, and exam readiness on Kubernetes

Welcome to the Certified Argo Project Associate course.

I'm Barahalikar Siddharth, and I’ll guide you through the Argo ecosystem on Kubernetes — focusing on practical, hands-on skills that matter to employers and real-world cloud-native teams.

Why this course matters:

* Argo CD and other Argo projects are widely used at companies like Adobe, Tesla, and NVIDIA.
* GitOps is now a core pattern for scalable, auditable deployments.
* This course emphasizes labs and practice so you can learn by doing and recover from mistakes confidently.

> **lightbulb** This course is lab-focused. Expect guided exercises, break/fix scenarios, and mock exams designed to mirror real certification tasks.

Course modules at a glance:

| Module                  | Key Topics                                                                                                              | Example/Outcome                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Argo CD                 | GitOps principles, installation, app management via UI/CLI, reconciliation & health checks, Helm support, multi-cluster | Manage Git-backed app syncs and declarative deployments |
| Argo Workflows          | Workflow authoring (DAGs, steps), artifacts, CLI/UI usage, data processing patterns                                     | Submit and monitor reproducible workflows               |
| Argo Rollouts           | Blue/Green, Canary, progressive delivery, AnalysisTemplates, Prometheus integration                                     | Implement safe canary rollouts with automated analysis  |
| Argo Events             | Event-sources, sensors, triggers (webhooks, queues)                                                                     | Trigger workflows from events for automation            |
| Certification Readiness | Mock exams, exam tips, common pitfalls                                                                                  | Prepare for the Certified Argo Project Associate exam   |

We begin with Argo CD, covering GitOps fundamentals, the differences between traditional CI/CD and GitOps workflows, deployment models, and the surrounding tooling. You will install Argo CD, configure it, and manage applications from both the web UI and the CLI — including syncing manifests, managing secrets, and understanding reconciliation loops and health checks.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cosmic-cow-recursive-
spec:
  entrypoint: cosmic-cow
  templates:
  - name: cosmic-cow
    steps:
    - - name: wisdom-check
        template: check-wisdom
      - name: enlightened
        template: cosmic-enlightenment
        when: "{{steps.wisdom-check.outputs.result}} == \"enlightened\""
      - name: confused
        template: cosmic-cow
        when: "{{steps.wisdom-check.outputs.result}} == \"confused\""
  - name: check-wisdom
    script:
      image: python:3.8-alpine
      command: [python]
      source: |
        import random
        result = "enlightened" if random.randint(0, 1) == 0 else "confused"
        print(result)
  - name: cosmic-enlightenment
    container:
      image: rancher/cowsay
      command: [sh, -c]
      args: ["cowsay", "✨COSMIC ENLIGHTENMENT ACHIEVED! The bovine oracle"]
```

<Frame>
  <img alt="A slide titled &#x22;ArgoCD Architecture&#x22; showing a flow diagram where GitHub, a user (via UI/CLI), and the ArgoCD service (octopus mascot) interact to pull manifests and sync them to a Kubernetes cluster. A small circular video of a presenter appears in the bottom-right corner." />
</Frame>

You will also explore advanced Argo CD topics:

* Reconciliation loops and automated drift correction
* Health checks and resource status reporting
* Fully declarative setups and Git sinks/sources
* Helm chart and Kustomize deployments
* Multi-cluster application management and access controls

Next, we cover Argo Workflows. This section teaches core concepts and architecture, installing and using the argo CLI, authoring workflows (steps, DAGs), handling artifacts, and patterns for batch or streaming data processing. Labs include submitting workflows and inspecting pod-level logs and outputs.

Installation example (replace the version tag with your desired release):

```bash theme={null}
ARGO_WORKFLOWS_VERSION="vX.Y.Z"
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/$ARGO_WORKFLOWS_VERSION/install.yaml"
argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml
```

> **lightbulb** Replace ARGO\_WORKFLOWS\_VERSION with the release tag you want to install (for example, "v3.4.8"). The sample `hello-world.yaml` run demonstrates a basic workflow submission and live watch.

<Frame>
  <img alt="A presentation slide titled &#x22;Argo Workflows for Data Processing&#x22; showing feature cards for Orchestration, Dependencies, Scaling, and a fourth item describing what Argo handles. A small circular video thumbnail of a presenter appears in the bottom-right corner." />
</Frame>

After Argo Workflows, we move to Argo Rollouts. This module covers rollout concepts, architecture, and the tooling to implement progressive delivery strategies such as blue/green and canary. You’ll learn how to configure traffic routing, integrate metrics providers, and automate promotion or rollback via AnalysisRuns and AnalysisTemplates.

<Frame>
  <img alt="A presentation slide titled &#x22;Architecture&#x22; showing an Argo Rollouts diagram with a Rollout containing Canary and Stable ReplicaSets, an AnalysisRun linked to Prometheus, and traffic split (20%/80%) from Ingress → Service. There's also a small circular video overlay of an instructor in the lower-right." />
</Frame>

Example AnalysisTemplate for measuring a success-rate metric in Prometheus:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: api-performance-check
spec:
  args:
  - name: service-name
  - name: namespace
  metrics:
  - name: check-success-rate
    provider:
      prometheus:
        address: http://prometheus.kube-prometheus-stack.svc.cluster.local:9090
        query: |
          sum(rate(http_requests_total{service_name="{{args.service-name}}",namespace="{{args.namespace}}",code!~"5.*"}[2m]))
          /
          sum(rate(http_requests_total{service_name="{{args.service-name}}",namespace="{{args.namespace}}"}[2m]))
    count: 3
    interval: 20s
    failureLimit: 1
    successCondition: result >= 0.99
```

Argo Events introduces event-driven automation for triggering Workflows and Rollouts. You’ll configure event sources and sensors, connect producers (webhooks, message queues, cloud events), and create end-to-end pipelines that react to external signals.

<Frame>
  <img alt="A browser window showing the &#x22;Argo Workflow Trigger&#x22; documentation with a left-hand user guide menu and a diagram in the main content area. A small circular video overlay of a presenter appears in the bottom-right corner." />
</Frame>

Certification readiness is covered with targeted mock exams, walkthroughs of common tasks, and exam strategy. These practice tests are designed to mimic the question styles you’ll see in the Certified Argo Project Associate exam so you can build confidence and identify areas for review.

<Frame>
  <img alt="A presenter wearing a black &#x22;KodeKloud&#x22; T-shirt sits at a desk next to a slide titled &#x22;Certified Argo Project Associate.&#x22; The slide lists topics like ArgoCD, Argo Workflows, Argo Rollouts, Argo Events, and Certification Readiness." />
</Frame>

Community and continued learning

* Join KodeKloud forums to discuss labs, share solutions, and ask instructors questions.
* Take advantage of community labs and contributed examples to extend your learning.

<Frame>
  <img alt="A screenshot of the KodeKloud community/forum page showing category links on the left, category tiles and recent topics in the center and right. A circular video inset of a presenter appears in the bottom‑right corner." />
</Frame>

Are you ready to become a Certified Argo Project Associate and advance your cloud-native and DevOps career? Enroll, practice the labs, and use the mock exams to measure progress — we’ll guide you step-by-step.

Links and references

* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* [Argo Rollouts documentation](https://argoproj.github.io/argo-rollouts/)
* [Argo Events documentation](https://argoproj.github.io/argo-events/)
* [GitOps Principles](https://www.gitops.tech/)
* [Helm](https://helm.sh/)
* [Prometheus](https://prometheus.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/c88c4a06-cdc7-4152-b2aa-a1fb02589846/lesson/37456d07-6b5b-4b45-a5cf-654fbe881941)
