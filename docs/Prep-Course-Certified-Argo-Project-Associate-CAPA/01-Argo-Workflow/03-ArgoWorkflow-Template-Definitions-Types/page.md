# submit workflow.yml to the 'argo' namespace
argo submit -n argo workflow.yml
```

The Argo UI is available if your Argo server is exposed; it provides a visual representation of templates, DAGs, and steps.

<Callout icon="warning">
  The `entrypoint` must match one of the template names defined under `templates`. If it does not, the workflow will fail to start.
</Callout>

## Practical tips and best practices

* Use `generateName` for recurring or CI-driven workflow submissions to avoid manual name management.
* Keep templates small and reusable — compose complex workflows from simple building blocks (container/script/steps/dag).
* Use `resources` and `resourceLimits` to avoid noisy scheduling and to communicate expected resource usage.
* Version control your workflow manifests alongside application code or infrastructure repositories for traceability.

## Quick reference: spec fields

| Field              | Description                                  |
| ------------------ | -------------------------------------------- |
| entrypoint         | Name of the template to execute first        |
| templates          | List of named templates used by the workflow |
| arguments          | Pass parameters into templates and workflows |
| volumes            | Shared volumes available to templates        |
| serviceAccountName | Service account used by workflow pods        |

## Links and references

* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* [Argo Workflows UI](https://argoproj.github.io/argo-workflows/ui/)
* [Argo CLI documentation](https://argoproj.github.io/argo-workflows/cli_workflows/)
* [Kubernetes CRDs](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [Kubernetes Pod and container specs](https://kubernetes.io/docs/concepts/workloads/pods/)

Notes:

* The `container` section within a template maps directly to a Kubernetes container spec and supports `env`, `volumeMounts`, and `resources`.
* Always ensure the `entrypoint` value matches a defined template name under `templates`.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/efefd18f-5e64-43db-8805-c1f80550fa30" />
</CardGroup>


# ArgoWorkflow Template Definitions Types

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/ArgoWorkflow-Template-Definitions-Types/page

Overview of Argo Workflows template types, explaining definitions and invokers like container, script, resource, HTTP, plugin, steps, and DAG

In this lesson/article we will learn about template types in Argo Workflows.

Templates can be thought of like functions: they define the instructions to execute. The spec of a workflow includes an entrypoint field that specifies the "main" template — the template executed first.

There are nine template types in total, split into two categories: template definitions and template invokers. Below is a brief overview of each.

<Frame>
  <img alt="A presentation slide titled &#x22;Template Types&#x22; showing two sections: &#x22;Template Definitions&#x22; (01 Container, 02 Script, 03 Resource, 04 Suspend, 05 Container Set, 06 HTTP, 07 Plugin) and &#x22;Template Invokers&#x22; (01 Steps, 02 DAG). The slide has a KodeKloud copyright at the bottom." />
</Frame>

Container template (definition)

* The container template is the most common template type. It schedules a Kubernetes container and its spec follows the same container fields as a Kubernetes Pod container (image, command, args, env, resources, volume mounts, etc.). Use it whenever you want to run a container image directly.

Script template (definition)

* The script template is a convenience wrapper around a container. It provides the same container fields (image, command) and adds a source field where you can embed a script directly. Argo writes the source into a file inside the container and executes it using the provided command.

<Callout icon="lightbulb">
  When using a script template, make sure the command you provide runs the interpreter (for example, `python`) and that the image includes that interpreter. The script content is placed into a file and executed inside the container.
</Callout>

Example script template:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: random-number-
spec:
  entrypoint: random-number
  templates:
  - name: random-number
    script:
      image: python:3.6-alpine
      command: [python]
      source: |
        import random
        i = random.randint(100, 2000)
        print(i)
```

Resource template (definition)

* Use resource templates to create, apply, delete, or patch Kubernetes resources from within an Argo workflow. The manifest to manage is provided inline in the manifest field.

Example that creates a ConfigMap:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: k8s-resource-
spec:
  entrypoint: k8s-resource
  templates:
  - name: k8s-resource
    resource:
      action: create
      manifest: |
        apiVersion: v1
        kind: ConfigMap
        metadata:
          generateName: dev-env-
        data:
          key: value
```

Suspend template (definition)

* A suspend template pauses workflow execution. You can suspend for a duration (using the duration field) or indefinitely until a manual resume. Resuming can be done via the CLI, the API, or the UI.

Example suspend template and resume command:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: delay-
spec:
  entrypoint: delay
  templates:
  - name: delay
    suspend:
      duration: "20s"
```

CLI resume (example):

```bash theme={null}
argo -n argo resume delay-xyzb
```

ContainerSet template (definition)

* The containerSet template runs multiple containers in the same pod (useful when you want sidecars or co-located containers that share volumes and localhost networking). The field is containerSet and contains an array of containers.

Example:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: container-set-template-
spec:
  entrypoint: main
  templates:
  - name: main
    containerSet:
      containers:
      - name: a
        image: rancher/cowsay
        command: [cowsay]
        args: ["Container A!!!!"]
      - name: b
        image: rancher/cowsay
        command: [cowsay]
        args: ["Container B!!!!"]
```

HTTP template (definition)

* An HTTP template performs HTTP(S) requests. The response body is automatically exported into the template's result output parameter. You can specify the URL, method (defaults to GET), headers, and body.

Example:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: http-template-example-
spec:
  entrypoint: fetch-todo-item
  templates:
  - name: fetch-todo-item
    http:
      url: "https://x.y.com/todos/1"
      method: "GET"
      headers:
      - name: "Content-Type"
        value: "application/json"
```

Plugin template (definition)

* Plugin templates let Argo workflows use executor plugins, extending behavior without modifying Argo core. Built-in and third-party plugins are supported. In the example below, the ArgoCD plugin is used to trigger a sync of applications, so no container is executed; Argo connects to an ArgoCD server and performs the action.

Example using the ArgoCD plugin:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: argocd-example-
spec:
  entrypoint: main
  templates:
  - name: main
    plugin:
      argocd:
        serverUrl: https://my-argocd.com/
        actions:
        - sync:
            project: highway-animation
            apps:
            - highway-animation
            - health-check-app
```

Template invokers

* Steps and DAG templates are the two invoker types. They don't execute work themselves but define how other templates (definitions) are invoked and composed into a workflow. Use Steps for sequential/parallel step-based flows and DAG for dependency-based execution graphs.

With these template types you can express a wide variety of orchestration patterns — from simple container tasks to complex multi-resource automation and integrations with other systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/d43f266a-9efa-44ed-8ab2-da20a2986461" />
</CardGroup>
