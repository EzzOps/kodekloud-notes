# Download the argo CLI binary for Linux (v3.7.2), decompress, and install
curl -LO "https://github.com/argoproj/argo-workflows/releases/download/v3.7.2/argo-linux-amd64.gz"
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
sudo mv argo-linux-amd64 /usr/local/bin/argo

# Verify installation
argo version
```

Platform alternatives

* macOS: download the `darwin` binary for your architecture or install via Homebrew if the formula matches the desired release.
* Windows: download the Windows binary and add it to your PATH.

Basic `argo` CLI examples

* Submit a workflow:
  * `argo submit -n argo my-workflow.yaml`
* List workflows:
  * `argo list -n argo`
* View workflow logs:
  * `argo logs -n argo <workflow-name>`

## Links and references

* Argo Workflows documentation: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Argo Workflows releases: [https://github.com/argoproj/argo-workflows/releases](https://github.com/argoproj/argo-workflows/releases)
* Security and RBAC guidance: [https://argoproj.github.io/argo-workflows/security/](https://argoproj.github.io/argo-workflows/security/)

Use the official docs and release notes as your source of truth for manifests, version-specific flags, and recommended production configuration patterns.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/0a13d180-e46e-4316-b4dd-da2c1370cbb6)


# Introduction to Argo Workflows and Features

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Introduction-to-Argo-Workflows-and-Features/page

Overview of Argo Workflows, a Kubernetes-native engine orchestrating containerized CI/CD, data processing, and ML pipelines using DAGs, templates, and observability.

Argo Workflows is a container-native workflow engine for Kubernetes that orchestrates parallel and sequential jobs using containers. It lets you express complex multi-step processes as either a linear sequence of steps or a directed acyclic graph (DAG), where each step executes in its own container. Because Argo runs inside Kubernetes, it is lightweight, scalable, and cloud-agnostic — with no external orchestration dependency.

Argo is commonly used for CI/CD pipelines, data processing pipelines, and machine learning workflows that need to run directly on Kubernetes clusters. Its Kubernetes-native design gives you access to Kubernetes primitives (RBAC, namespaces, resource quotas, storage) while providing higher-level workflow constructs.

<Frame>
  <img alt="A presentation slide titled &#x22;Argo Workflows&#x22; listing four numbered features (container-native for Kubernetes, parallel multi-step workflows, good for CI/CD/data/ML, lightweight and cloud-agnostic). On the right is a screenshot of the Argo web UI showing a visual DAG of a CI/CD pipeline." />
</Frame>

## Key capabilities

Argo Workflows provides a rich set of features for running container-native workloads on Kubernetes:

* Declarative workflow definitions: author workflows with YAML manifests that describe steps, DAGs, templates, and inputs/outputs.
* Control-flow primitives: built-in support for conditional execution, loops, fan-in/fan-out, and parallel steps.
* Reusability & parameterization: define reusable WorkflowTemplate and ClusterWorkflowTemplate objects and pass parameters between templates.
* Visualization & observability: the Argo Server UI visualizes DAGs, provides per-step logs, and shows execution state for debugging.
* Execution control: timeouts, suspend/resume, retries, and backoff policies to control runtime behavior.
* Data passing and artifacts: first-class artifact support (S3, GCS, HTTP, and more) plus parameters and outputs for step-to-step data transfer.
* Concurrency & resource management: configure parallelism at workflow, template, and step levels to guard resource consumption.
* Long-running services: sidecars and daemon steps let you run background services alongside workflow steps.
* SDKs & clients: official Go and Python SDKs (and community SDKs for other languages) enable programmatic workflow control.
* Exit handlers & cleanup: onExit handlers, TTL strategies, and garbage-collection options help automate cleanup and teardown.

## Minimal declarative example

Below is a minimal Argo Workflow YAML that demonstrates the declarative style and a simple sequence of steps. Save this to a file (e.g., minimal-workflow\.yaml) and submit it with `argo submit` when you have an Argo controller running.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-argo-
spec:
  entrypoint: hello-sequence
  templates:
    - name: hello-sequence
      steps:
        - - name: step-1
            template: echo
            arguments:
              parameters:
                - name: msg
                  value: "Hello from step 1"
        - - name: step-2
            template: echo
            arguments:
              parameters:
                - name: msg
                  value: "Hello from step 2"

    - name: echo
      inputs:
        parameters:
          - name: msg
      container:
        image: alpine:3.17
        command: [sh, -c]
        args: ["echo {{inputs.parameters.msg}}"]
```

## Feature summary (quick reference)

| Feature area        | Use case                          | Example                                             |
| ------------------- | --------------------------------- | --------------------------------------------------- |
| Workflow types      | Sequential or DAG orchestration   | `spec.templates[].steps` or `spec.templates[].dag`  |
| Artifacts & storage | Share files between steps         | S3/GCS/HTTP artifact locations                      |
| Control flow        | Conditional logic, loops          | `when` clauses, `withItems`, `withParam`            |
| Observability       | UI and logs                       | Argo Server web UI + kubectl logs                   |
| Execution control   | Timeouts, suspend/resume, retries | `activeDeadlineSeconds`, `suspend`, `retryStrategy` |
| Reusability         | Templates and libraries           | `WorkflowTemplate`, `ClusterWorkflowTemplate`       |

## When to choose Argo Workflows

* You need Kubernetes-native orchestration with fine-grained control over containers and resources.
* Your workloads require parallelism, complex DAGs, or passing artifacts between steps.
* You want UI-based visualization of pipeline execution and per-step logs.
* You prefer declarative YAML workflow definitions that integrate with GitOps and CI/CD tooling.

> **lightbulb** Argo runs natively on Kubernetes, so you'll need a Kubernetes cluster (local or cloud) to run workflows and to use the [Argo Server / UI](https://argoproj.github.io/argo-workflows/) for visualization and control.

## Links and references

* Official Argo Workflows docs: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Argo GitHub repository: [https://github.com/argoproj/argo-workflows](https://github.com/argoproj/argo-workflows)
* Argo Python SDK: [https://github.com/argoproj-labs/argo-python-sdk](https://github.com/argoproj-labs/argo-python-sdk)

For hands-on practice, deploy a lightweight Kubernetes cluster (minikube, kind, or a cloud cluster), install Argo Workflows, and try submitting the minimal workflow above.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/4871ca99-4f8b-4d67-8df8-7f0d130d69f9)
