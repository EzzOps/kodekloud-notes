# Argo Workflow Specification

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Argo-Workflow-Specification/page

Explains Argo Workflows CRD, YAML structure, template types, container templates, submission methods, and best practices for authoring reusable Kubernetes automation pipelines.

In this lesson we examine the Argo Workflow specification and how to author reusable automation pipelines as Kubernetes custom resources.

Argo Workflows is implemented as a Kubernetes Custom Resource Definition (CRD), which lets you define complex CI/CD and automation pipelines using familiar YAML files. A workflow is a structured sequence of automated tasks that together accomplish a goal — commonly used in DevOps for application deployment, testing, and promotion.

Key components of an Argo Workflow manifest:

* Header: Kubernetes metadata (apiVersion, kind, metadata).
* spec: Describes workflow behavior and templates that perform work.

The following sections explain the structure, common template types, and how to submit a workflow.

## Workflow file structure

A typical workflow YAML contains the following top-level parts:

* Header: `apiVersion`, `kind`, and `metadata`.
* Metadata: you can specify `name` or `generateName`. Use `generateName` to avoid collisions when submitting the same manifest multiple times — Argo appends a unique suffix.
* spec: the core of the workflow. Important fields:
  * `entrypoint`: the name of the template that starts execution.
  * `templates`: a list of reusable templates. Templates describe tasks and can reference each other.

> **lightbulb** Use generateName when you want to submit the same workflow multiple times without name collisions. Each submission will get a unique suffix appended to the provided generateName.

## Template types (overview)

Templates are the building blocks of workflows. Argo supports several template types for different use cases:

| Template Type | Use Case                                | Notes                                                                                                         |
| ------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| container     | Run a container image                   | Maps directly to a Kubernetes container spec (`image`, `command`, `args`, `env`, `volumeMounts`, `resources`) |
| script        | Run inline scripts in various runtimes  | Useful for quick logic without building a container image                                                     |
| steps         | Define sequential steps                 | A list of templates executed in sequence                                                                      |
| dag           | Define directed acyclic graph execution | Supports complex dependency graphs and parallelism                                                            |
| resource      | Create or modify Kubernetes resources   | Useful for applying manifests or CRs as part of the workflow                                                  |

Templates can be composed — steps or dag templates reference container/script/resource templates to perform tasks.

## Container templates

Container templates accept the same fields as a Kubernetes Pod container spec. This means you can use:

* image
* command and args
* env and envFrom
* volumeMounts and volumes
* resources

Because the container template mirrors Kubernetes, you can use existing YAML knowledge when defining tasks.

Example container-template workflow:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cowsay-
spec:
  entrypoint: cowsay-template
  templates:
  - name: cowsay-template
    container:
      image: rancher/cowsay
      command: ["cowsay"]
      args: ["Argo Workflow!!!!"]
```

## Submitting a workflow

You can submit workflows with either the Argo UI or the CLI.

CLI example (submits to the `argo` namespace):

```bash theme={null}
