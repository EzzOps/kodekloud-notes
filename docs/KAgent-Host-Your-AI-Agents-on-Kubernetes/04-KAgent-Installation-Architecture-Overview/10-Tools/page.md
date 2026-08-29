# Tools

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/Tools/page

Overview of K-Agent tools, MCP integration, and agent-as-tool composition enabling Kubernetes-native agents to call built-in and external tools for cluster, monitoring, and cloud operations.

In K-Agent, tools are the explicit integrations an agent uses to interact with its environment. Tools can access cluster state, external services, or other agents—letting agents perform concrete actions rather than only reasoning.

Common examples of tools an agent might expose or call:

* List cluster resources (e.g., all pods in a namespace)
* Retrieve pod logs
* Describe a Service or other Kubernetes resource
* Query a monitoring system (Prometheus)
* Invoke cloud provider APIs (via MCP)

Example CLI-like commands that correspond to those tools:

```bash theme={null}
list pods
get pod logs
describe services
```

Built-in tools shipped with K-Agent include utilities for:

* Displaying pod logs and resource manifests
* Querying Prometheus metrics
* Generating or applying Kubernetes resources
* Troubleshooting helpers and diagnostics

Inspect the tools registry after installing K-Agent to see the full list of available built-in tools and their usage.

Tool type overview:

| Tool type          | Typical use case                               | Example                              |
| ------------------ | ---------------------------------------------- | ------------------------------------ |
| Built-in tools     | Cluster introspection and common ops           | `get pod logs`, `list pods`          |
| External/MCP tools | Access to cloud providers, external APIs       | AWS S3 queries, cloud metadata       |
| Agent-as-tool      | Delegate specialized translation or processing | A PromQL agent that produces queries |

Model Context Protocol (MCP)
K-Agent supports the Model Context Protocol (MCP) to register and expose external tools to agents. MCP provides a standard way to integrate third-party systems and cloud APIs so agents can call them as native tools. Using MCP you can:

* Import external tools into the agent runtime
* Enable agents to execute those tools
* Integrate third-party systems without modifying core K-Agent components

<Frame>
  <img alt="The image is a dark-themed diagram titled &#x22;Tools&#x22; showing two buttons (&#x22;Built-In Tools&#x22; and &#x22;MCP Tools&#x22;) above a labeled box &#x22;Model Context Protocol.&#x22; Inside the larger container are three labeled features: &#x22;Import external tools,&#x22; &#x22;Enable agent execution,&#x22; and &#x22;Integrate external systems.&#x22;" />
</Frame>

Hands-on exercises typically show installing MCP adapters for providers like AWS and then querying cloud resources so agents can use AWS data during execution.

Agents as tools
K-Agent also supports treating an agent itself as a callable tool. One agent can expose capabilities that other agents invoke, enabling specialization and composition. For example, you might run a dedicated PromQL agent that translates natural-language questions into PromQL; another agent calls the PromQL agent as a tool to obtain a valid query, then executes it.

* PromQL docs: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

Example composition YAML that references MCP tools and another agent:

```yaml theme={null}
