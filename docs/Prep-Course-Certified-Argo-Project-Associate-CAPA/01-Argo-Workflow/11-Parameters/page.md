# Parameters

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Parameters/page

Explains using parameters in Argo Workflows to pass values into templates, perform parameter substitution in container args, and override values at submission via CLI or parameter files.

Let's talk about input parameters in [Argo Workflows](https://argoproj.github.io/argo-workflows/).

This lesson shows a workflow spec that accepts a parameter named `message` and passes it into a container command by referencing the template input parameter.

Example workflow:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cowsay-
spec:
  entrypoint: cowsay
  arguments:
    parameters:
      - name: message
        value: "workflow arguments value"
  templates:
    - name: cowsay
      inputs:
        parameters:
          - name: message
      container:
        image: rancher/cowsay
        command: [cowsay]
        args: ["{{inputs.parameters.message}}"]
```

What this workflow defines:

* A top-level default parameter under `spec.arguments` named `message` with the value `"workflow arguments value"`.
* A template called `cowsay` that declares an input parameter `message`.
* The container runs the `cowsay` command and passes the parameter into `args` using Argo parameter substitution: `{{inputs.parameters.message}}`.

<Callout icon="lightbulb">
  When referencing parameters inside YAML template fields, use the substitution syntax exactly as shown: . Put the substitution inside quotes (for example, args: ) so the YAML parser treats it as a string and the braces are handled correctly.
</Callout>

How parameter wiring works (quick reference):

| Field                             | Purpose                                                                   | Example                                             |
| --------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------- |
| spec.arguments                    | Workflow-level default parameter values; can be overridden at submit time | `- name: message value: "workflow arguments value"` |
| templates\[].inputs.parameters    | Declare parameters a template expects                                     | `- name: message`                                   |
| template container args / command | Use parameter substitution to pass values into the container              | `args: ["{{inputs.parameters.message}}"]`           |

Overriding the default parameter values at runtime can be done with the [Argo CLI](https://argoproj.github.io/argo-workflows/).

* Submit the workflow and override a single parameter from the CLI:

```bash theme={null}
