# Demo Template Script

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Template-Script/page

Explains an Argo Workflows script template that runs an inline Python script in a container, captures stdout as template output, and demonstrates generateName and entrypoint usage

In this lesson we examine a script template example in Argo Workflows. This workflow demonstrates a simple script template that runs a short Python script inside a container image. The script's stdout is captured and exposed as the template output (`outputs.result`), allowing later steps to consume the result.

What this workflow demonstrates

* Using `metadata.generateName` to create a unique workflow name with the prefix `random-number-`.
* Defining a single `entrypoint` (`random-number`) that uses a script template.
* Supplying an inline script via the `source` field; the script runs inside the specified container image.
* Capturing the script stdout and exposing it as the template output.

Example Workflow (YAML)

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

Fields explained

| Field                 | Purpose                                                                                                       | Example                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------- |
| metadata.generateName | Create a unique workflow name using a fixed prefix                                                            | `random-number-`            |
| spec.entrypoint       | The template that starts execution                                                                            | `random-number`             |
| script.image          | Container image that runs the script                                                                          | `python:3.6-alpine`         |
| script.command        | Command invoked to execute the script                                                                         | `[python]`                  |
| script.source         | Inline script text written to a file and executed inside the image; stdout is captured as the template output | The Python code shown above |

How the script template works

* The text in `script.source` is written into a temporary file inside the container.
* The container executes the script using the specified `command` and `image`.
* Anything printed to stdout by the script is captured by Argo and made available as `outputs.result`, which you can reference in later templates using standard Argo templating.

Run the workflow

* From the Argo Web UI: paste the YAML and submit. Optionally switch to the Graph view to see a single node representing the `random-number` template.
* From the cluster using kubectl:

```bash theme={null}
kubectl apply -f random-number-workflow.yaml
```

* Using the Argo CLI (if installed):

```bash theme={null}
argo submit --watch random-number-workflow.yaml
```

View logs and outputs

* In the UI, open the workflow, click the node, then click Logs to inspect stdout.
* With the Argo CLI, you can stream logs (replace the workflow name as appropriate):

```bash theme={null}
argo logs <workflow-name> --follow
```

Example node output (the workflow prints a randomly chosen integer):

```text theme={null}
1728
```

<Frame>
  <img alt="A browser screenshot of the Argo Workflows web UI showing a single completed workflow node labeled &#x22;random-number-7krn6&#x22; with a green checkmark. The top toolbar shows buttons like Resubmit, Delete, Logs, Share, and a vertical icon sidebar runs down the left." />
</Frame>

<Callout icon="lightbulb">
  The stdout of a script template is captured and available as the template output (`outputs.result`). Reference it in subsequent templates using Argo's templating syntax to pass values between steps.
</Callout>

Further reading and references

* [Argo Workflows documentation](https://argoproj.github.io/argo-workflows/)
* [Script templates (Argo Workflows)](https://argoproj.github.io/argo-workflows/workflow-templates/#script-templates)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/20d37ece-f531-40a2-90eb-c0a6a63a280f" />
</CardGroup>
