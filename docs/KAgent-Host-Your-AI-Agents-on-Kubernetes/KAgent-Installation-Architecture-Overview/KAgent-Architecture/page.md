# Step 1: Discover Agent Card (Agent discovery endpoint)
GET http://127.0.0.1:8083/api/a2a/kagent/k8s-a2a-agent/.well-known/agent-card
# Server → Returns the Agent Card JSON shown earlier
```

```json theme={null}
# Step 2: Send Message
{
  "messageId": "msg-001",
  "role": "user",
  "parts": [
    {
      "type": "text",
      "text": "Get all pods in the default namespace"
    }
  ]
}
```

```json theme={null}
# Step 3: Agent responds with a Task update (working)
{
  "taskId": "task-001",
  "status": {
    "state": "working",
    "message": "Querying Kubernetes cluster..."
  }
}
```

```json theme={null}
# Step 4: Agent sends final Artifact (result)
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

Summary

* Agent discovery returns an Agent Card.
* Clients send Messages composed of Parts (text, files, structured data).
* Agents create Tasks for long-running work, stream status and partial Artifacts while working, and return final Artifacts when done.

Other important concepts

* Context: Groups related messages and tasks into sessions or conversations for consistent state.
* Transport: Use secure channels such as HTTPS. See: [HTTPS](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS)
* Format: Standardize on formats like JSON and JSON-RPC 2.0. See: [JSON](https://www.json.org/json-en.html) and [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
* Authentication: Prefer robust schemes such as OAuth 2.0 or API keys. See: [OAuth 2.0](https://oauth.net/2/)
* Agent discovery & extensions: Protocol-level mechanisms for how agents locate each other and how optional extensions are negotiated

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Other Important Concepts&#x22; listing items like Context, Format, Agent Discovery on the left and Transport and Authentication on the right. The items are shown as horizontal rounded boxes with teal accent bars." />
</Frame>

<Callout icon="warning">
  Security reminder: always authenticate and encrypt agent endpoints. Exposing discovery endpoints without proper authentication or TLS can leak capabilities and create attack surfaces.
</Callout>

References

* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* JSON: [https://www.json.org/json-en.html](https://www.json.org/json-en.html)
* JSON-RPC 2.0: [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification)
* OAuth 2.0: [https://oauth.net/2/](https://oauth.net/2/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/0bf2ea88-d093-4254-94ba-f063c806baec" />
</CardGroup>


# KAgent Architecture

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/KAgent-Architecture/page

Describes KAgent architecture that integrates LLM-driven autonomous agents, cloud-native tools, and a Kubernetes-native runtime to automate DevOps tasks, observability, and troubleshooting.

Welcome — this lesson explains the KAgent architecture, how its parts interact, and what each component is responsible for. KAgent brings together large language models (LLMs), a library of cloud-native tools, and an extensible framework so autonomous agents can plan, execute, and analyze operational tasks.

At a high level, KAgent converts LLM reasoning into concrete actions by running autonomous agents that chain tool calls, inspect results, and produce actionable outputs. This makes KAgent well suited for DevOps automation, debugging, and observability workflows.

Common use cases

* Diagnose multi-hop connectivity problems across services
* Troubleshoot application performance degradations
* Automate alert generation from Prometheus metrics ([Prometheus course](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana))
* Debug gateway and HTTPRoute configuration with a kgateway-specialized agent ([kgateway course](https://learn.kodekloud.com/user/courses/kgateway))
* Orchestrate progressive rollouts using progressive deployment tools

KAgent’s architecture is organized into three high-level areas:

* Tools: MCP-style functions agents call to interact with cloud-native systems. KAgent includes pre-built tools for progressive deployment, [Kubernetes](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial), and [Helm](https://learn.kodekloud.com/user/courses/helm-for-beginners).
* Agents: Autonomous units that plan multi-step operations, invoke tools, and produce results.
* Framework: A flexible runtime and control plane (built on the [Google ADK](https://learn.kodekloud.com/user/courses/google-adk)) that exposes a UI, CLI, and declarative management for agents and tools.

<Frame>
  <img alt="A dark-themed slide featuring the &#x22;kagent&#x22; logo and the heading &#x22;Main Components.&#x22; Below it are three labeled columns — Tools, Agents, and Framework — each with short bullet points describing features." />
</Frame>

Runtime architecture — four core components
Now let’s dig into the runtime architecture. You will typically see four main components: Controller, Engine (App), CLI, and Dashboard (kagent-ui). Each plays a specific role in managing and executing agents.

Controller

* KAgent’s controller is a Kubernetes-native controller implemented in Go.
* It owns and reconciles the custom resource definitions (CRDs) that declare agents, tools, and their configurations.
* Key responsibilities:
  * Manage agent lifecycle: create / update / delete agent resources.
  * Create and maintain Kubernetes resources required by agents (Jobs, Deployments, ConfigMaps, etc.).
  * Ensure cluster state converges to the declared resources.
* Future extensions may include an MCP server for centralized tool management and distribution.

Engine (App)

* The engine is the core execution runtime, implemented in Python.
* It runs agent conversation loops, executes the agent’s plan-action cycles, and orchestrates tool invocations.
* Built on the Google ADK, the engine leverages abstractions for agents, tools, and context propagation so ADK-compatible agents/tools interoperate with KAgent.
* Because of ADK compatibility, you can bring existing ADK agents/tools into KAgent with minimal changes.

<Frame>
  <img alt="A dark-themed diagram titled &#x22;Component Details&#x22; showing boxes for Controller, App/Engine, CLI, and Dashboard (UI), plus a flow from &#x22;kagent&#x22; to &#x22;Kagent Engine&#x22; above a Python logo. Below that is an &#x22;ADK Framework&#x22; box." />
</Frame>

Agent responsibilities (summary)

* Run the agent conversation loop and manage agent state.
* Produce plans, execute actions, and iterate based on tool outputs.
* Invoke, monitor, and manage tool executions required to complete tasks.
* Return structured responses to callers, the CLI, or the UI.
* Be extensible by adding controllers, custom agents, or new tools through ADK integration.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Component Details&#x22; showing four top-level components (Controller, App/Engine, CLI, Dashboard) and four info columns listing Responsibilities, Framework Foundation, ADK Framework Information, and Key Points with brief bullet items. The Responsibilities column notes things like running the conversation loop, executing agent logic, and managing tool calls." />
</Frame>

CLI

* The KAgent CLI provides a command-line entry point for the platform.
* It connects to the engine to manage resources, invoke agents, and inspect runs programmatically.
* Use cases:
  * Deploy and manage KAgent resources from CI/CD pipelines or scripts.
  * Invoke agents for ad-hoc troubleshooting and automation.
  * Integrate agent operations into automation tooling.

<Frame>
  <img alt="A presentation slide titled &#x22;Component Details&#x22; showing four component boxes (Controller, App/Engine, CLI — highlighted, Dashboard (UI)) and three panels below labeled Purpose, Use Case, and Key Points. The panels describe the CLI as a command-line alternative to the UI that connects to the engine, manages resources, and interacts with agents." />
</Frame>

kagent-ui (Dashboard)

* The kagent-ui dashboard is the web-based management and monitoring interface.
* Provides visual onboarding, run histories, agent configuration views, and operational telemetry.
* After installing KAgent in-cluster, you can port-forward the `kagent-ui` service to access the dashboard locally for management and debugging.

<Frame>
  <img alt="A dark-themed diagram titled &#x22;Component Details&#x22; with labeled boxes for Controller, App/Engine, CLI, and Dashboard (UI). Below, a &#x22;kagent Dashboard&#x22; feeds into a &#x22;Web Interface&#x22; that branches to &#x22;Manage&#x22; and &#x22;Work&#x22; boxes next to a small robot icon." />
</Frame>

<Callout icon="lightbulb">
  KAgent’s ADK foundation standardizes how agents, tools, and context are modeled. This interoperability allows you to run any ADK-compliant agent on KAgent with minimal adaptation — accelerating reuse across environments.
</Callout>

Component summary table

|    Component | Primary role                     | Implementation        | Typical responsibilities                               |
| -----------: | -------------------------------- | --------------------- | ------------------------------------------------------ |
|   Controller | Declarative resource management  | Go, Kubernetes-native | Manage CRDs, reconcile resources, lifecycle management |
| Engine (App) | Agent execution runtime          | Python, Google ADK    | Run agent loops, orchestrate tools, propagate context  |
|          CLI | Scriptable access and automation | CLI client            | Deploy resources, trigger agents, integrate with CI/CD |
|    kagent-ui | Visual management & monitoring   | Web dashboard         | Onboarding, run history, operational views             |

In summary, KAgent combines:

* A Kubernetes-native Go controller for declarative resource management,
* A Python-based engine built on the Google ADK to run agent logic and orchestrate tools,
* A CLI for automation and scripting, and
* A web dashboard (kagent-ui) for visual operation and monitoring.

This architecture enables flexible, extensible, LLM-driven automation for cloud-native operations and DevOps tasks.

Links and references

* [Kubernetes Basics](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)
* [Google ADK course](https://learn.kodekloud.com/user/courses/google-adk)
* [Prometheus course](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)
* [kgateway course](https://learn.kodekloud.com/user/courses/kgateway)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/89058a9e-1b22-418a-8ee0-3d34b6405c69" />
</CardGroup>
