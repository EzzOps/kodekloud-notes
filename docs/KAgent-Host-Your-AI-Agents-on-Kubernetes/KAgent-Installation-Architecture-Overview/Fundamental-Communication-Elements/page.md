# Verify the key is available in the environment
echo $OPENAI_API_KEY
# Example output (truncated for security):
# sk-kkAI-7f4db864d4a30df42264af74c22f4f1c5bf51...
```

## Quick comparison

| Installation Method | Best for                               | Key command                                                                                                                                                                                   |        |
| ------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| CLI installer       | Local testing, quick installs          | \`curl -fsSL [https://raw.githubusercontent.com/kagent-dev/kagent/refs/heads/main/scripts/get-kagent](https://raw.githubusercontent.com/kagent-dev/kagent/refs/heads/main/scripts/get-kagent) | bash\` |
| Helm chart          | Production or cluster-managed installs | `helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent`                                                                                                                             |        |

***

## CLI-based installation

Follow these steps to install kagent using the kagent CLI installer.

1. Install the kagent CLI (the installer fetches the latest stable binary):

```bash theme={null}
curl -fsSL https://raw.githubusercontent.com/kagent-dev/kagent/refs/heads/main/scripts/get-kagent | bash
```

Example installer output:

```text theme={null}
Downloading https://cr.kagent.dev/v0.7.7/kagent-linux-amd64
Verifying checksum... Done.
Preparing to install kagent into /usr/local/bin
kagent installed into /usr/local/bin/kagent
```

2. Confirm the installed kagent version:

```bash theme={null}
kagent version
```

Example output:

```json theme={null}
{"backend_version":"unknown","build_date":"2025-12-11","git_commit":"bfe15ba","kagent_version":"0.7.7"}
```

3. Inspect available CLI commands and flags:

```bash theme={null}
kagent --help
```

Trimmed sample output (top-level commands and flags):

```text theme={null}
kagent is a CLI and TUI for kagent

Usage:
  kagent [flags]
  kagent [command]

Available Commands:
  add-mcp        Add an MCP server entry to kagent.yaml
  bug-report     Generate a bug report
  build          Build a Docker images for an agent project
  completion     Generate the autocompletion script for the specified shell
  dashboard      Open the kagent dashboard
  deploy         Deploy an agent to Kubernetes
  get            Get a kagent resource
  help           Help about any command
  init           Initialize a new agent project
  install        Install kagent
  invoke         Invoke a kagent agent
  mcp            MCP (Model Context Protocol) server management
  run            Run agent project locally with docker-compose and launch chat interface
  uninstall      Uninstall kagent
  version        Print the kagent version

Flags:
      --config string           config file (default is $HOME/.kagent/config.yaml)
  -h, --help                    help for kagent
      --kagent-url string       KAgent URL (default "http://localhost:8083")
  -n, --namespace string        Namespace (default "kagent")
  -o, --output-format string    Output format (default "table")
      --timeout duration        Timeout (default 5m0s)
  -v, --verbose                 Verbose output
```

4. Ensure the `kagent` namespace exists (this creates it if absent):

```bash theme={null}
kubectl create namespace kagent --dry-run=client -o yaml | kubectl apply -f -
```

5. Install kagent into the `kagent` namespace. The installer will use the `OPENAI_API_KEY` environment variable (no additional flag required for the key):

```bash theme={null}
kagent install -n kagent
```

Example confirmation:

```text theme={null}
kagent installed successfully
```

6. Verify the deployed pods in the `kagent` namespace:

```bash theme={null}
kubectl get pods -n kagent
```

Example output (trimmed):

```text theme={null}
NAME                                                   READY   STATUS    RESTARTS   AGE
argo-rollouts-conversion-agent-6b75f48f84-skzsc        1/1     Running   0          40s
cilium-debug-agent-5c7798b559-9bbzh                    1/1     Running   0          40s
cilium-manager-agent-5dc4964899-2vkn4                  0/1     Running   0          40s
helm-agent-66d7fd5fb8-dvbr6                            0/1     Running   0          40s
kagent-controller-6886fc4f5c-wn2xm                     1/1     Running   0          97s
kagent-grafana-mcp-5cc85fd598-hw6bk                    1/1     Running   0          97s
kagent-kmcp-controller-manager-76645f577f-n2r5v        1/1     Running   0          97s
kagent-querydoc-5f6fd94c98-64kxn                       1/1     Running   0          97s
kagent-tools-56c49d7d4d-6h8zg                          1/1     Running   0          97s
kagent-ui-59d5bbd564-r7j5q                             1/1     Running   0          97s
kgateway-agent-d97c5f7d-5qg2c                          0/1     Running   0          40s
observability-agent-55d64bd489-987hm                   1/1     Running   0          40s
promql-agent-56c56b98bd-xvlzw                          0/1     Running   0          39s
```

### Uninstalling kagent (CLI)

To remove the kagent installation created via the CLI:

```bash theme={null}
kagent uninstall -n kagent
```

Example output:

```text theme={null}
Warning: kagent release not found, skipping uninstallation
Warning: kagent-crds release not found, try to delete crds directly
Successfully deleted CRD agents.kagent.dev
Successfully deleted CRD modelconfigs.kagent.dev
Successfully deleted CRD toolservers.kagent.dev

kagent uninstalled successfully
```

***

## Helm-based installation

Helm is a common method for installing kagent in production environments. The recommended sequence is: install CRDs first, then install the application Helm chart.

1. Install the kagent CRDs from the public Helm OCI chart:

```bash theme={null}
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds \
  --namespace kagent \
  --create-namespace
```

Example output (trimmed):

```text theme={null}
Pulled: ghcr.io/kagent-dev/kagent/helm/kagent-crds:0.7.7
Digest: sha256:[SECRET_REDACTED]
I1215 09:13:10.543041 47158 warnings.go:110] "Warning: unrecognized format \"int64\""
NAME: kagent-crds
LAST DEPLOYED: Mon Dec 15 09:13:10 2025
NAMESPACE: kagent
STATUS: deployed
REVISION: 1
```

2. Verify the CRDs are present:

```bash theme={null}
kubectl get crd | grep kagent
```

Example output:

```text theme={null}
agents.kagent.dev                      2025-12-15T09:13:10Z
mcpservers.kagent.dev                  2025-12-15T09:13:10Z
memories.kagent.dev                    2025-12-15T09:13:10Z
modelconfigs.kagent.dev                2025-12-15T09:13:10Z
remotemcpservers.kagent.dev            2025-12-15T09:13:10Z
toolservers.kagent.dev                 2025-12-15T09:13:10Z
```

3. Install the kagent Helm chart. Pass the OpenAI API key via Helm values so components can use it. The exact value key name may vary by chart — one common pattern is `openai.apiKey`. Replace with the correct key for your chart if different:

```bash theme={null}
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --namespace kagent \
  --set openai.apiKey="$OPENAI_API_KEY"
```

4. Verify Helm releases:

```bash theme={null}
helm list -n kagent
```

Example output:

```text theme={null}
NAME        NAMESPACE   REVISION   UPDATED                                 STATUS    CHART                 APP VERSION
kagent      kagent      1          2025-12-15 09:14:04.750303641 +0000 UTC deployed  kagent-0.7.7
kagent-crds kagent      1          2025-12-15 09:13:10.339038232 +0000 UTC deployed  kagent-crds-0.7.7
```

5. Confirm services and pods are running:

```bash theme={null}
kubectl get svc -n kagent
kubectl get pods -n kagent
```

Example services (trimmed):

```text theme={null}
service/kagent-controller                  8083/TCP
service/kagent-grafana-mcp                8000/TCP
service/kagent-querydoc                   8080/TCP
service/kagent-tools                      8084/TCP
service/kagent-ui                         8080/TCP
service/kgateway-agent                    8080/TCP
service/observability-agent               8080/TCP
service/promql-agent                      8080/TCP
```

<Callout icon="warning">
  When removing kagent, uninstall the application release first and remove CRDs separately. Deleting CRDs before removing dependent resources can leave orphaned resources or break uninstall workflows.
</Callout>

### Uninstalling Helm release and CRDs

1. Uninstall the kagent release:

```bash theme={null}
helm uninstall kagent -n kagent
```

Example output:

```text theme={null}
release "kagent" uninstalled
```

2. Uninstall the CRDs Helm release:

```bash theme={null}
helm uninstall kagent-crds -n kagent
```

Example output:

```text theme={null}
release "kagent-crds" uninstalled
```

3. Confirm the namespace no longer contains kagent resources:

```bash theme={null}
kubectl get pods -n kagent
```

Example output:

```text theme={null}
No resources found in kagent namespace.
```

***

## Conclusion

This lesson covered how to install and uninstall kagent using:

* the kagent CLI (quick installer + `kagent install`), and
* Helm charts (install CRDs first, then the application chart).

Choose CLI for quick experimentation and Helm for production/cluster-managed deployments. After installation, you can explore the kagent UI, interact with deployed agents, and configure providers via the kagent configuration.

## Links and references

* [OpenAI](https://openai.com)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Helm Documentation](https://helm.sh/docs/)
* kagent project: [https://github.com/kagent-dev/kagent](https://github.com/kagent-dev/kagent)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/a40af8f9-4f17-4356-84f4-fa13a1b94071" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/f9250211-acaa-4e98-8a39-e674eeb3783c" />
</CardGroup>


# Fundamental Communication Elements

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/Fundamental-Communication-Elements/page

Defines core elements and flow for agent-to-agent communication including agent cards, messages and parts, tasks with streaming, artifacts as deliverables, discovery, transport, and authentication

Below is a clearer, more structured explanation of the core elements used in A2A (agent-to-agent) communication. The sequence follows discovery → messaging → long-running work → deliverables so you can map each technical diagram to the corresponding definitions and examples.

Agent Card
An Agent Card is essentially a "business card" for an AI agent. It tells other agents:

* Who the agent is (name, description, provider)
* Where to reach it (URL / endpoint)
* What it can do (capabilities and skills)
* How to authenticate (security requirements)

Capabilities can include features like streaming, push notifications, or state transition history. Skills are detailed entries that list name, id, description, tags, examples, and supported input/output modes — effectively the agent's advertised abilities.

<Frame>
  <img alt="A slide titled &#x22;Fundamental Communication Elements&#x22; showing an &#x22;Agent Card&#x22; described as &#x22;like a business card for an AI agent.&#x22; Below it are four colored boxes listing: Who the agent is (name/description/provider), Where to find it (URL/endpoint), What it can do (skills/capabilities), and How to authenticate (security requirements)." />
</Frame>

Example Agent Card (Kubernetes-focused agent):

```json theme={null}
{
  "name": "k8s_a2a_agent",
  "description": "An example A2A agent that knows how to use Kubernetes tools.",
  "url": "http://127.0.0.1:8083/api/a2a/kagent/k8s-a2a-agent/",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "get-resources-skill",
      "name": "Get Resources",
      "description": "Get resources in the Kubernetes cluster",
      "tags": ["k8s", "resources"],
      "examples": [
        "Get all resources in the Kubernetes cluster",
        "Get the pods in the default namespace"
      ],
      "inputModes": ["text"],
      "outputModes": ["text"]
    }
  ]
}
```

<Callout icon="lightbulb">
  Agent discovery returns the Agent Card so other agents know how to connect, which capabilities are available, and what authentication is required. Exposing accurate capabilities and skill metadata improves automated routing and orchestration in multi-agent systems.
</Callout>

Messages and Parts
Messages are the basic units that agents exchange. Each message typically includes metadata (sender, unique ID) and a list of parts. A part contains the actual content and can be one of:

* text (plain user or system text)
* file (binary content encoded as Base64 with a MIME type)
* structured data (JSON payloads)

Example message parts:

```json theme={null}
{
  "type": "text",
  "text": "Get the pods in default namespace"
}
```

```json theme={null}
{
  "type": "file",
  "mimeType": "application/json",
  "data": "base64-encoded-content"
}
```

```json theme={null}
{
  "type": "data",
  "data": {
    "namespace": "default",
    "resourceType": "pods"
  }
}
```

Artifacts
Artifacts are the tangible outputs produced by agents. Unlike messages (which are transient communication), artifacts are deliverables: reports, structured results, files, images, or any persistent output. Artifacts have unique IDs, names, and parts (using the same parts schema as messages).

<Frame>
  <img alt="A presentation slide titled &#x22;Fundamental Communication Elements&#x22; highlighting element 03 labeled &#x22;Artifact.&#x22; It defines an artifact as &#x22;actual results or deliverables from an agent&#x22; and includes a blue note that it's a real output, not just a message." />
</Frame>

Example artifact (pod listing):

```json theme={null}
{
  "taskId": "task-001",
  "status": { "state": "completed" },
  "artifacts": [
    {
      "artifactId": "artifact-001",
      "name": "Pod List",
      "parts": [
        {
          "type": "text",
          "text": "Found 3 pods:\n- pod-1\n- pod-2\n- pod-3"
        }
      ]
    }
  ]
}
```

Common artifact types and examples:

| Artifact Type     | Typical Use Case                             | Example                                           |
| ----------------- | -------------------------------------------- | ------------------------------------------------- |
| Text artifact     | Human-readable reports                       | `Finished analysis: 12 issues found`              |
| Data artifact     | Structured output for machine consumption    | `{"reservationId":"abc123","status":"confirmed"}` |
| File artifact     | Images, documents, or binary outputs         | Base64-encoded image bytes                        |
| Mixed (Text/Data) | Aggregated outputs (e.g., list of resources) | `["pod-1","pod-2","pod-3"]`                       |

<Frame>
  <img alt="A presentation slide titled &#x22;Real-World Examples&#x22; showing four rounded cards labeled Text Artifact, Data Artifact, File Artifact, and Text/Data Artifact. Each card lists an example: a completed report, a booking confirmation, a generated image, and a list of Kubernetes resources." />
</Frame>

Artifacts can also be streamed incrementally as they are produced (useful for large or long-running tasks).

Tasks
Tasks model long-running or multi-step work that originates from a message. Tasks have well-defined lifecycles (submitted → working → completed/failed/canceled). While a task executes, it may stream status updates and partial artifacts before delivering final artifacts.

Example task lifecycle with streaming partial results then final results:

```json theme={null}
// Initial task submission
{
  "taskId": "task-789",
  "status": { "state": "submitted" }
}

// Update while working (streaming partial artifact)
{
  "taskId": "task-789",
  "status": { "state": "working", "message": "Processing your request..." },
  "artifacts": [
    {
      "artifactId": "artifact-1",
      "name": "Partial Results",
      "parts": [{"type": "text", "text": "Found 2 pods so far..."}]
    }
  ]
}

// Final result
{
  "taskId": "task-789",
  "status": { "state": "completed" },
  "artifacts": [
    {
      "artifactId": "artifact-2",
      "name": "Final Results",
      "parts": [{"type": "text", "text": "Found 3 pods total"}]
    }
  ]
}
```

End-to-end Example
This short flow demonstrates discovery → message → task updates → artifact results.

```http theme={null}
