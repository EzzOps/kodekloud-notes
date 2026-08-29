# WorkflowTemplates

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/WorkflowTemplates/page

Explains Argo WorkflowTemplates and ClusterWorkflowTemplates as reusable workflow recipes, how to define and reference them with templateRef or workflowTemplateRef to share and standardize CI/CD steps.

Think of a WorkflowTemplate as a reusable recipe for Argo Workflows. Instead of copying and pasting the same manifest (for example, a build step or a test container) into every workflow, define it once as a WorkflowTemplate and reference it from many workflows. This centralizes maintenance, enforces consistency, and reduces duplication.

<Frame>
  <img alt="A presentation slide titled &#x22;WorkflowTemplate&#x22; that defines it as &#x22;A reusable recipe for workflows, defined once and used across multiple workflows.&#x22; Below that is a boxed &#x22;Benefits&#x22; list of four points: a central version-controlled library, promotes consistency, cleaner/easier to manage, and reduces duplication and maintenance effort." />
</Frame>

> **lightbulb** A WorkflowTemplate stores common templates in a namespace so teams can share and reuse steps like functions from a library. Use templates to standardize CI/CD tasks such as builds, tests, and deployments.

## How to define a WorkflowTemplate

Defining a WorkflowTemplate is the same as defining a Workflow, except the resource kind is WorkflowTemplate. That tells Argo to store the definition as a reusable template rather than executing it immediately.

Example WorkflowTemplate (cowsay):

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: cowsay-template
  namespace: argo
spec:
  entrypoint: cowsay
  templates:
    - name: cowsay
      inputs:
        parameters:
          - name: message
      container:
        image: rancher/cowsay
        command: ["cowsay"]
        args: ["{{inputs.parameters.message}}"]
```

Create this resource with kubectl apply -f \<file> or via the Argo Workflows UI/CLI (for example, `argo template create <file>`).

## Reusing a WorkflowTemplate

Once a WorkflowTemplate exists in a namespace, you can reuse it in two primary ways:

* templateRef — call a single template from the WorkflowTemplate as a step inside a larger workflow (like importing a single function from a library).
* workflowTemplateRef — run the entire WorkflowTemplate as a complete workflow, using its specified entrypoint and arguments.

| Reuse Method        | When to use                                                                                     | Example                                                    |
| ------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| templateRef         | Use when you want a specific template (step) from the template library inside a larger workflow | `templateRef: { name: cowsay-template, template: cowsay }` |
| workflowTemplateRef | Use when you want to execute the whole WorkflowTemplate as a workflow                           | `workflowTemplateRef: { name: cowsay-template }`           |

Example: calling a single template from a WorkflowTemplate using templateRef

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: use-single-template-
spec:
  entrypoint: my-custom-workflow
  templates:
    - name: my-custom-workflow
      steps:
        - - name: first-step
            templateRef:
              name: cowsay-template      # name of the WorkflowTemplate
              template: cowsay           # name of the template inside the WorkflowTemplate
            arguments:
              parameters:
                - name: message
                  value: "I called this from another workflow!"
```

Example: running the whole WorkflowTemplate using workflowTemplateRef

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: run-whole-template-
  namespace: argo
spec:
  arguments:
    parameters:
      - name: message
        value: "Hello from a WorkflowTemplate!"
  workflowTemplateRef:
    name: cowsay-template
```

## ClusterWorkflowTemplate

A ClusterWorkflowTemplate is the cluster-scoped equivalent of WorkflowTemplate. It is not tied to a namespace and is available cluster-wide — a good fit for platform teams that must provide approved, central templates to multiple namespaces.

Example ClusterWorkflowTemplate:

```yaml theme={null}
