# Set the version you want to install
ARGO_WORKFLOWS_VERSION="v3.7.3"

# Create the argo namespace
kubectl create namespace argo

# Install the minimal quick-start (controller, server, minio, httpbin, CRDs, etc.)
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/quick-start-minimal.yaml"
```

Typical (condensed) output from applying the manifest:

```text theme={null}
namespace/argo created
customresourcedefinition.apiextensions.k8s.io/workflows.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workflowtemplates.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/cronworkflows.argoproj.io created
# ...additional CRDs and resources...
deployment.apps/argo-server created
deployment.apps/workflow-controller created
deployment.apps/minio created
deployment.apps/httpbin created
service/argo-server created
service/minio created
service/httpbin created
```

## 2. What the quick-start deploys

| Resource                                                | Purpose                           | Notes                                 |
| ------------------------------------------------------- | --------------------------------- | ------------------------------------- |
| Workflow Controller                                     | Executes workflow steps           | Core runtime for Argo Workflows       |
| Argo Server                                             | REST/gRPC API + web UI            | Provides the web UI and API endpoints |
| MinIO                                                   | S3-compatible artifact repository | Demo-only; for production use S3/GCS  |
| httpbin                                                 | Demo HTTP service                 | Useful for example workflows          |
| CRDs (Workflows, WorkflowTemplates, CronWorkflows, ...) | Custom resource definitions       | Required for Argo CRs to work         |

<Callout icon="lightbulb">
  MinIO provided in the quick-start is suitable for demos and testing. For production systems, configure Argo to use a durable artifact repository (S3/GCS) and supply appropriate credentials.
</Callout>

## 3. Expose the Argo Server (optional)

By default the `argo-server` Service is a ClusterIP. To access the UI from your workstation you can:

* Change the Service to NodePort, or
* Use kubectl port-forward, or
* Add an Ingress/LoadBalancer in cloud environments.

Interactive example: edit the service to NodePort:

```bash theme={null}
kubectl -n argo edit svc argo-server
# Change "type: ClusterIP" to "type: NodePort" and save
```

Verify services and pods:

```bash theme={null}
kubectl -n argo get svc
# Example:
# NAME         TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)
# argo-server  NodePort   10.98.122.61     <none>        2746:30774/TCP
# httpbin      ClusterIP  10.103.119.102   <none>        9100/TCP
kubectl -n argo get pods
# Example:
# NAME                                         READY   STATUS              AGE
# argo-server-68bc7d7567-4681c                 0/1     ContainerCreating   30s
# workflow-controller-5bb95ffc45-rp2fz        1/1     Running             30s
# minio-5cb4ff75c9-stmmw                       1/1     Running             29s
# httpbin-58d7595979-xndwm                    1/1     Running             29s
```

Wait until the `argo-server` pod is Running and Ready before continuing.

## 4. Install the Argo CLI

Download the matching `argo` CLI binary for your OS. The example below auto-detects macOS vs Linux; adjust the `ARGO_WORKFLOWS_VERSION` if needed.

```bash theme={null}
# Set the version you want to install
ARGO_WORKFLOWS_VERSION="v3.7.3"

# Detect OS (darwin or linux)
ARGO_OS="linux"
if [[ "$(uname -s)" == "Darwin" ]]; then
  ARGO_OS="darwin"
fi

# Download the compressed binary
curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/argo-${ARGO_OS}-amd64.gz"

# Uncompress
gunzip "argo-${ARGO_OS}-amd64.gz"

# Make executable and move to a directory in PATH
chmod +x "argo-${ARGO_OS}-amd64"
sudo mv "argo-${ARGO_OS}-amd64" /usr/local/bin/argo

# Verify installation
argo version
```

Expected (condensed) output:

```text theme={null}
argo: v3.7.3
  BuildDate: ...
  GitCommit: ...
```

## 5. Configure the CLI to talk to the Argo Server

If you exposed the Argo Server via NodePort (for example 2746 -> 30774), set environment variables so the CLI uses the Argo Server rather than the Kubernetes API. Adjust values for your environment:

```bash theme={null}
export ARGO_SERVER='localhost:30774'
export ARGO_HTTP1=true
export ARGO_INSECURE=true
export ARGO_BASE_HREF=''
export ARGO_TOKEN=''
export ARGO_NAMESPACE=argo   # namespace you installed Argo into
# export KUBECONFIG=...      # set if you need a specific kubeconfig
```

Test the connection by listing workflows:

```bash theme={null}
argo list
```

## 6. Access the web UI

* Open your browser to `https://localhost:<NODEPORT>` (e.g., [https://localhost:30774](https://localhost:30774)) if you used NodePort.
* Accept any self-signed certificate warnings (the quick-start ships with demo certificates).
* The UI shows an initial "Tell us what you want to use Argo for" dialog on fresh installs and an empty workflow dashboard.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI with a modal asking &#x22;Tell us what you want to use Argo for&#x22; and showing selectable tiles like Machine Learning, Data Processing, Stream Processing, CI/CD, Infrastructure Automation, and Other. The blurred dashboard and sidebar are visible in the background with a &#x22;No workflows&#x22; message." />
</Frame>

## 7. Next steps and common commands

* Submit example workflows from the Argo docs or local YAML files: `argo submit -n argo <workflow.yaml>`
* Inspect and manage workflows: `argo list`, `argo get <workflow>`, `argo logs -w <workflow>`
* Define reusable WorkflowTemplates and scheduled CronWorkflows.
* Replace the bundled MinIO with a production artifact store (S3/GCS) by updating the Argo config map and providing credentials.

Common commands:

| Task                 | Command                                |
| -------------------- | -------------------------------------- |
| Submit workflow      | `argo submit -n argo <workflow.yaml>`  |
| List workflows       | `argo list -n argo`                    |
| Get workflow details | `argo get -n argo <workflow-name>`     |
| Stream logs          | `argo logs -n argo -w <workflow-name>` |

That completes the installation and initial setup of Argo Workflows. You can now deploy and run example workflows via the CLI or the Web UI.

## Links and references

* Official documentation: [Argo Workflows](https://argoproj.github.io/argo-workflows/)
* Kubernetes docs: [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
* MinIO: [MinIO Documentation](https://min.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/24755975-b290-466e-b861-14fa52acf911" />
</CardGroup>


# Demo Parameters

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Demo-Parameters/page

Explains how to declare, pass, and override workflow level parameters in Argo Workflows with examples for template inputs and CLI or web UI submission

In this lesson you'll learn how to define and use workflow-level (global) parameters in Argo Workflows. Parameters declared under `spec.arguments.parameters` are available to the entire workflow and can be consumed by one or more templates. This pattern enables reusing a single workflow manifest while supplying different inputs at submit time.

Example: a minimal workflow that declares a global `message` parameter and passes it into a template to be used as the container argument:

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
      value: "a message from the workflow arguments section"
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

Key points

* Declare workflow-global parameters under `spec.arguments.parameters`.
* Inside a template, declare the same parameter name under `inputs.parameters` and reference it with `{{inputs.parameters.<name>}}`.
* Some fields also support direct workflow-level references using `{{workflow.parameters.<name>}}`.

<Callout icon="lightbulb">
  A common way to reference a workflow parameter inside a template is to declare the parameter under the template's `inputs.parameters` and then use the expression `{{inputs.parameters.<name>}}` in container args or other fields that accept template expressions. You can also reference workflow-level parameters directly using `{{workflow.parameters.<name>}}` in fields that accept template expressions.
</Callout>

Submit the workflow and watch the run (example using a public manifest URL):

```bash theme={null}
argo -n argo submit https://gist.githubusercontent.com/sidd-harth/d8e60353a95606b13f9c41f6fb59bf34/raw/66ae1738a05943a9ef7a220f3d49425d59993c90/workflow-2.yml --watch
```

Sample CLI output while the workflow is running:

```console theme={null}
Name:                 cowsay-tptgl
Namespace:            argo
ServiceAccount:       unset (will run with the default ServiceAccount)
Status:               Running
Created:              Fri Oct 24 06:35:15 +0000 (4 seconds ago)
Started:              Fri Oct 24 06:35:15 +0000 (4 seconds ago)
Duration:             4 seconds
Progress:             0/1
Parameters:
  message:            a message from the workflow arguments section

STEP           TEMPLATE   PODNAME         DURATION  MESSAGE
⟳ cowsay-tptgl  cowsay     cowsay-tptgl   4s
```

You can also inspect and interact with the run in the Argo Workflows web UI. The workflow graph shows the single `cowsay` node for this run:

<Frame>
  <img alt="A browser screenshot of the Argo Workflows web interface showing a workflow graph with a single node labeled &#x22;cowsay-tptgl.&#x22; Top action buttons (RESUBMIT, SUSPEND, STOP, TERMINATE, DELETE, LOGS, SHARE, WORKFLOW LINK) and a left-hand icon toolbar are visible." />
</Frame>

When the run finishes successfully, the workflow parameters are shown in the completed status and the container logs include the parameter value:

```console theme={null}
Name:                   cowsay-tptgl
Namespace:              argo
ServiceAccount:         unset (will run with the default ServiceAccount)
Status:                 Succeeded
Conditions:
  PodRunning            False
  Completed             True
Created:                Fri Oct 24 06:35:15 +0000 (38 seconds ago)
Started:                Fri Oct 24 06:35:15 +0000 (38 seconds ago)
Finished:               Fri Oct 24 06:35:52 +0000 (1 second ago)
Duration:               37 seconds
Progress:               1/1
Parameters:
  message:              a message from the workflow arguments section

STEP             TEMPLATE   PODNAME         DURATION   MESSAGE
✔ cowsay-tptgl     cowsay     cowsay-tptgl    26s
```

Logs from the `cowsay` container:

```console theme={null}
/ a message from the workflow arguments \
\ section                                 /
------------------------------------------
       ^   ^
      (oo)\_______
      (__) \       )\/\
           ||----w |
           ||     ||
```

Overriding the global parameter at submit time

* UI: Click Resubmit in the web UI and edit parameter values before resubmitting.
* CLI: Pass parameters inline with `-p` (or `--parameter`).

Example — override `message` via CLI:

```bash theme={null}
argo -n argo submit arguments-parameters.yaml -p message="with great power comes great responsibility" --watch
```

Submitting with an overridden parameter produces a run using the new message. Example running status after overriding via CLI:

```console theme={null}
Name:                   cowsay-ljb54
Namespace:              argo
ServiceAccount:         unset (will run with the default ServiceAccount)
Status:                 Running
Created:                Fri Oct 24 06:37:10 +0000 (3 seconds ago)
Started:                Fri Oct 24 06:37:10 +0000 (3 seconds ago)
Duration:               3 seconds
Progress:               0/1
Parameters:
  message:              with great power comes great responsibility

STEP            TEMPLATE   PODNAME         DURATION  MESSAGE
◉ cowsay-ljb54  cowsay     cowsay-ljb54    3s
```

Logs showing the overridden text:

```console theme={null}
cowsay-ljb54: time="2025-10-24T06:37:33 UTC" level=info msg="capturing logs" argo=true
cowsay-ljb54:
cowsay-ljb54:  / with great power comes great \
cowsay-ljb54:  \ responsibility               /
cowsay-ljb54:   ------------------------------
cowsay-ljb54:
cowsay-ljb54:        \   ^__^
cowsay-ljb54:         \  (oo)\_______
cowsay-ljb54:            (__)\       )\/\
cowsay-ljb54:                ||----w |
cowsay-ljb54:                ||     ||
cowsay-ljb54:
cowsay-ljb54: time="2025-10-24T06:37:34 UTC" level=info msg="sub-process exited" argo=true error="<nil>"
```

Parameter passing options at a glance

| Method                      | CLI example                                          | Notes                                                                                         |
| --------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Inline single parameter     | `-p message="goodbye world"`                         | Quick override for one or few values                                                          |
| Parameters file (YAML/JSON) | `--parameter-file params.yaml`                       | `params.yaml` can be a YAML or JSON map of key/value pairs                                    |
| Change entrypoint at submit | `--entrypoint print-message-caps -p message="HELLO"` | Useful when a manifest contains multiple templates and you want to run a different entrypoint |
| Web UI resubmit             | N/A                                                  | Edit parameters interactively and resubmit the workflow                                       |

Example parameter file (params.yaml):

```yaml theme={null}
message: goodbye world
```

CLI using parameter file:

```bash theme={null}
argo submit arguments-parameters.yaml --parameter-file params.yaml
```

Tips and references

* Reuse the same manifest by changing inputs and entrypoints at submit time—no need to edit the YAML file.
* For nested workflows or complex templates, prefer declaring template `inputs.parameters` and passing values via `spec.arguments.parameters` to keep intent explicit.
* See the official Argo Workflows documentation for more parameter patterns and expression usage: [Argo Workflows — Parameters and Artifacts](https://argoproj.github.io/argo-workflows/workflow-parameters/).

Further reading

* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/afa0672d-7cf5-4470-9f12-18e1394157a6" />
</CardGroup>
