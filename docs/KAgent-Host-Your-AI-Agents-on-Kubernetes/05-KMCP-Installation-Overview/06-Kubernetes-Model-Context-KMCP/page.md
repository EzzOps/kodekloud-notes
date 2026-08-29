# /root/01-values-min.yaml
agents:
  argo-rollouts-agent:
    enabled: false
  cilium-debug-agent:
    enabled: false
  cilium-manager-agent:
    enabled: false
  cilium-policy-agent:
    enabled: false
  helm-agent:
    enabled: false
  istio-agent:
    enabled: false
  k8s-agent:
    enabled: true
  kgateway-agent:
    enabled: false
  observability-agent:
    enabled: false
  promql-agent:
    enabled: false

kmcp:
  enabled: true

kagent-tools:
  enabled: true

tools:
  grafana-mcp:
    enabled: false
  querydoc:
    enabled: false
```

Summary: the `kmcp` controller is enabled (`kmcp.enabled=true`) and minimal agents are enabled. The `kagent-tools` are also enabled.

| Key                        | Purpose                                            | Example |
| -------------------------- | -------------------------------------------------- | ------- |
| `kmcp.enabled`             | Enable KMCP controller functionality within KAgent | `true`  |
| `kagent-tools.enabled`     | Enables utility containers included with KAgent    | `true`  |
| `agents.k8s-agent.enabled` | Local k8s agent for cluster integrations           | `true`  |

## 2) Install KAgent (includes KMCP controller)

Install the KAgent Helm chart using the values file:

```bash theme={null}
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --namespace kagent \
  -f /root/01-values-min.yaml
```

Helm should pull the chart and install the release. Example Helm output:

```bash theme={null}
Pulled: ghcr.io/kagent-dev/kagent/helm/kagent:0.7.7
Digest: sha256:[SECRET_REDACTED]
```

### Expose the KAgent UI (local access)

Patch the `kagent-ui` Service to NodePort for local access (adjust `nodePort` as required):

```bash theme={null}
kubectl -n kagent patch svc kagent-ui -p '{"spec":{"type":"NodePort","ports":[{"name":"ui","port":8080,"targetPort":8080,"nodePort":30080}]}}'
```

<Callout icon="warning">
  Exposing services via NodePort opens them on each cluster node. For production clusters prefer LoadBalancer or Ingress solutions with proper authentication.
</Callout>

## 3) Verify pods and controller components

Check pods in the `kagent` namespace:

```bash theme={null}
kubectl get pods -n kagent
```

Example output:

```bash theme={null}
NAME                                              READY   STATUS    RESTARTS   AGE
k8s-agent-855bbb4fc4-x22vz                        1/1     Running   0          5m59s
kagent-controller-6886fc4f5c-xc4gq                1/1     Running   0          6m7s
kagent-kmcp-controller-manager-76645f577f-zncp9   1/1     Running   0          6m7s
kagent-tools-56c49d7d4d-bszs7                      1/1     Running   0          6m7s
kagent-ui-59d5bbd564-7p82q                         1/1     Running   0          6m7s
```

<Callout icon="lightbulb">
  Troubleshooting quick pointers:

  * Check pod status: `kubectl -n kagent get pods`
  * View recent events: `kubectl -n kagent get events --sort-by='.lastTimestamp'`
  * Tail controller logs: `kubectl -n kagent logs -l app.kubernetes.io/component=controller -f`
  * Primary docs: [https://kagent.dev](https://kagent.dev)
</Callout>

## 4) Confirm CRDs and API resources

List CRDs related to KAgent and KMCP:

```bash theme={null}
kubectl get crd | grep -E "kagent|kmcp"
```

Example CRDs present:

```bash theme={null}
agents.kagent.dev                     2025-12-15T11:03:27Z
mcpservers.kagent.dev                 2025-12-15T11:03:27Z
memories.kagent.dev                   2025-12-15T11:03:27Z
modelconfigs.kagent.dev               2025-12-15T11:03:27Z
remotemcpservers.kagent.dev           2025-12-15T11:03:27Z
toolservers.kagent.dev                2025-12-15T11:03:27Z
```

You can also confirm the MCP API resource registration:

```bash theme={null}
kubectl api-resources | grep -i mcp
```

Example API resources:

```bash theme={null}
mcpservers                      kagent.dev/v1alpha1        true    MCPServer
remotemcpservers                rmcps   kagent.dev/v1alpha1    true    RemoteMCPServer
```

Table — typical MCP-related CRDs:

| CRD                           | Description                                                    |
| ----------------------------- | -------------------------------------------------------------- |
| `mcpservers.kagent.dev`       | Defines an MCPServer deployment and transport settings         |
| `remotemcpservers.kagent.dev` | Remote MCPServer definitions for cross-cluster or remote hosts |
| `modelconfigs.kagent.dev`     | Model configuration artifacts used by tools and agents         |

## 5) Locate KMCP controller pod and deployment

Filter pods for the KMCP controller:

```bash theme={null}
kubectl get pods -n kagent | grep kmcp
```

Example:

```bash theme={null}
kagent-kmcp-controller-manager-76645f577f-zncp9   1/1     Running   0    5m3s
```

Check deployments in the `kagent` namespace to confirm the controller deployment name and status:

```bash theme={null}
kubectl get deployment -n kagent
```

Example:

```bash theme={null}
NAME                             READY  UP-TO-DATE  AVAILABLE  AGE
k8s-agent                         1/1    1           1          6m23s
kagent-controller                 1/1    1           1          6m31s
kagent-kmcp-controller-manager   1/1    1           1          6m31s
kagent-tools                      1/1    1           1          6m31s
kagent-ui                         1/1    1           1          6m31s
```

Tail controller logs to verify the KMCP controller has started and is reconciling:

```bash theme={null}
kubectl -n kagent logs -l app.kubernetes.io/name=kagent -f
```

Look for messages indicating the MCP controller has started, registered event sources, and is serving metrics.

Verify service accounts created by the KMCP controller:

```bash theme={null}
kubectl get serviceaccount -n kagent | grep kmcp
```

Example:

```bash theme={null}
kagent-kmcp-controller-manager  0  5m32s
```

## 6) What the KMCP controller manages

* The KMCP controller watches MCPServer custom resources and reconciles them into concrete Kubernetes objects (Deployments, Services, RBAC, etc.).
* Each MCPServer CR results in one or more pods running the defined MCP server image/configuration.
* The controller also updates MCPServer status conditions (e.g., whether the underlying pods are Ready).

## 7) MCPServer CRD structure (example)

Always verify CRD schema in your installed version. A high-level example of an MCPServer resource:

```yaml theme={null}
apiVersion: kagent.dev/v1alpha1
kind: MCPServer
metadata:
  name: example-mcp-server
  namespace: kagent
spec:
  deployment:
    image: ghcr.io/example/mcp-server:latest
    port: 3000
    cmd: "python"
    args: ["src/main.py"]
    env:
      API_KEY: "your-api-key-here"
  transportType: "stdio"
```

Notes about the main fields:

* `spec.deployment.image`: Container image for the MCP server.
* `spec.deployment.port`: Port the server listens on inside the container.
* `spec.deployment.cmd` / `args`: Command and arguments to start the server.
* `spec.deployment.env`: Environment variables (for example, LLM API keys).
* `spec.transportType`: Recommended transport for local KAgent servers is `stdio`. Some servers support `http`.

## 8) Lifecycle: what happens when you create an MCPServer

When you create an MCPServer CR:

1. KMCP controller detects the new CR and begins reconciliation.
2. The controller creates required Kubernetes resources (Deployment, Service, ConfigMaps, Secrets, etc.).
3. A pod (or pods) start using the configured image and arguments.
4. The MCPServer CR status will progress from unready to `True` once the pod(s) reach Ready.

## 9) Deploy a sample AWS API MCP server and verify

Apply the sample manifest (example file path):

```bash theme={null}
kubectl apply -f /root/aws-api-mcp-server.yaml
```

Verify the MCPServer resource and status:

```bash theme={null}
kubectl get mcpserver -n kagent
kubectl describe mcpserver aws-api-mcp-server -n kagent
```

During initialization the MCPServer's status may show `False` until the pod becomes Ready. Once the pod is Running and Ready, the MCPServer status will indicate success.

## 10) Common questions (FAQ)

| Question                                                         | Answer                                                                                                     |                                                       |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Are KMCP CRDs automatically installed in recent KAgent releases? | Yes. KMCP CRDs are bundled starting with KAgent v0.7+. Older versions may require manual CRD installation. |                                                       |
| What is the MCPServer API group/version?                         | `kagent.dev/v1alpha1` — always confirm using `kubectl api-resources`.                                      |                                                       |
| How do I confirm the MCPServer CRD is accessible?                | Use \`kubectl api-resources                                                                                | grep mcp`and`kubectl get crd mcpservers.kagent.dev\`. |
| What if `kubectl get mcpserver -A` returns "No resources found"? | Either there are no MCPServer resources created, or the CRD is not installed. Verify CRDs and namespaces.  |                                                       |

## 11) Next steps

This lesson completed the KMCP installation and basic exploration. The next lesson will show deploying additional AWS MCP servers and demonstrating integrations with model configs and tool servers.

## Links and references

* KAgent official site: [https://kagent.dev](https://kagent.dev)
* KAgent Helm releases (GitHub/OCI): [https://github.com/kagent-dev/kagent](https://github.com/kagent-dev/kagent)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/12b692c6-b1f0-4e05-84d2-ed2fc9f1985e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/63bc21ff-69b3-4bdf-9313-50b99a1d2f2d" />
</CardGroup>


# Kubernetes Model Context KMCP

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KMCP-Installation-Overview/Kubernetes-Model-Context-KMCP/page

KMCP is a toolkit and CLI for scaffolding, testing, and deploying MCP servers in Kubernetes, providing boilerplates, local inspection, CRD lifecycle and secret management.

Hello and welcome — this lesson explains the Kubernetes Model Context Protocol (KMCP) and how it accelerates building, testing, and running MCP (Model Context Protocol) servers in cloud-native environments like Kubernetes.

Before we dive into KMCP, it's helpful to understand the underlying protocol: MCP. MCP is an open protocol from Anthropic that standardizes how large language model (LLM) applications connect to external data sources and tools. Without a standard like MCP, each LLM integration becomes a bespoke adapter, adding development and maintenance burden.

<Callout icon="lightbulb">
  MCP acts as a universal adapter for LLMs. An MCP server exposes tools and data sources in a standard way so any LLM application that speaks MCP can discover and use them without bespoke integrations. See the MCP project for protocol details: [https://github.com/anthropic/mcp](https://github.com/anthropic/mcp)
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;What Is MCP?&#x22; showing three numbered cards with icons that list MCP benefits. The cards say: &#x22;Significantly speeds up integrations,&#x22; &#x22;Simplifies integrations,&#x22; and &#x22;Standardizes integrations.&#x22;" />
</Frame>

This standardization significantly speeds up, simplifies, and harmonizes integrations across tools and data sources.

<Frame>
  <img alt="A diagram titled &#x22;What Is MCP?&#x22; showing a central &#x22;Universal Adapter (MCP)&#x22; that standardizes connections. The left side lists inputs (database, cloud storage, web API, hardware sensor) and the right shows outputs (AI applications, tools, data sources) all linked through the MCP." />
</Frame>

## What is KMCP?

KMCP is a platform and toolset that:

* Accelerates local development of MCP servers with templates and boilerplates.
* Provides CLI tooling to scaffold, test, and deploy MCP servers.
* Manages MCP server lifecycle and secret handling in Kubernetes using CRDs and best practices.

In short: KMCP helps you bootstrap MCP projects, develop tools quickly, test locally (with an inspector/UI), and deploy/manage them as Kubernetes-native resources.

<Frame>
  <img alt="An infographic titled &#x22;KMCP Features&#x22; showing four colored panels across a timeline for Fast Development, Multiple Framework Support, Cloud‑Native Deployment, and Local Development. Each panel lists brief bullet points like built‑in boilerplates, FastMCP Python/MCP Go, Kubernetes lifecycle/secret management, and local MCP testing." />
</Frame>

Key KMCP capabilities:

* Project scaffolding and framework-specific templates (FastMCP for Python, MCP Go).
* Tool boilerplates to expose internal APIs or services to LLMs.
* Local development experience: build, run, and use the MCP Inspector to exercise tools.
* Kubernetes lifecycle management: deploy, update, delete, health checks, and secret management.
* Support for multiple transports (stdio, HTTP) and authorization integration (e.g., Keycloak).

## Typical KMCP development workflow

1. Initialize a project
2. Add tool boilerplates
3. Run locally for development and testing (MCP Inspector)
4. Test tools interactively using the inspector
5. Deploy to Kubernetes and manage lifecycle

<Frame>
  <img alt="An infographic titled &#x22;Development Workflow&#x22; showing five numbered steps: 01 Initialize Project, 02 Add Tools, 03 Run Locally, 04 Test with MCP Inspector, and 05 Deploy to Kubernetes. Below that a dark panel lists created artifacts such as project structure, a sample echo tool, a Dockerfile, and a kmcp.yaml configuration file." />
</Frame>

### Commands (quick reference)

|                                        Purpose | Command                                                     |
| ---------------------------------------------: | :---------------------------------------------------------- |
|          Initialize a Python project (FastMCP) | `kmcp init python my-mcp-server`                            |
|               Initialize a Go project (MCP Go) | `kmcp init go my-mcp-server --go-module-name my-mcp-server` |
|                     Add a new tool boilerplate | `kmcp add-tool my-tool --project-dir my-mcp-server`         |
| Run the MCP server locally (build + inspector) | `kmcp run --project-dir my-mcp-server`                      |
|                           Deploy to Kubernetes | `kmcp deploy --project-dir my-mcp-server`                   |

To scaffold a project:

* Python (FastMCP):

```bash theme={null}
kmcp init python my-mcp-server
```

* Go:

```bash theme={null}
kmcp init go my-mcp-server --go-module-name my-mcp-server
```

These commands create a project scaffold with:

* Example tool(s) (e.g., echo tool),
* Dockerfile for containerization,
* `kmcp.yaml` configuration,
* A test suite and recommended project structure.

### Add a tool boilerplate

```bash theme={null}
kmcp add-tool my-tool --project-dir my-mcp-server
```

### Run locally (with MCP Inspector)

```bash theme={null}
kmcp run --project-dir my-mcp-server
```

This builds and runs the container locally, starts the MCP server, and opens the MCP Inspector so you can list and invoke tools interactively.

### Deploy to Kubernetes

```bash theme={null}
kmcp deploy --project-dir my-mcp-server
```

KMCP handles Kubernetes manifests, CRD lifecycles, health checks, and secret injection based on your `kmcp.yaml` configuration.

## Project structure examples

FastMCP (Python) project layout:

```text theme={null}
FastMCP Python Project

my-mcp-server/
├─ src/
│  ├─ core/
│  ├─ tools/
│  └─ main.py
├─ tests/
├─ Dockerfile
├─ kmcp.yaml
├─ pyproject.toml
├─ .env.example
└─ README.md
