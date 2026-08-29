# Course Introduction

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Introduction/Course-Introduction/page

Hands-on course teaching deployment, management, and observability of AI agents on Kubernetes with KAgent, KMCP/MCP, system prompts, and integrations like Slack and AWS

The AI landscape is evolving quickly: agents are no longer limited to answering questions — they can take actions, connect to tools, and automate workflows. KAgent is a platform for running and managing these AI agents inside Kubernetes clusters. This course shows you how to design, deploy, and operate AI agents on Kubernetes using KAgent, KMCP/MCP, and related tooling.

You will learn practical, production-focused topics:

* How to install and operate KAgent in Kubernetes.
* How agents communicate using the A2A (agent-to-agent) protocol.
* How to build and run MCP servers and integrate them with agents.
* How to create system prompts, define agents declaratively, and debug agent behavior using observability tools like Jaeger.
* How to connect external tools and services (for example, Slack, AWS CloudWatch, Billing) to your agents.

> **lightbulb** Recommended prerequisites: basic Kubernetes knowledge (kubectl), familiarity with YAML manifests, and experience with Python or other scripting languages for building local integrations.

We begin with an overview of KAgent and a hands-on lab that walks you through the KAgent portal and agent lifecycle.

<Frame>
  <img alt="A dark-themed web dashboard titled &#x22;KAgent: Host Your AI Agents on Kubernetes&#x22; showing multiple cards for different AI agents (like argo-rollouts, cilium, helm) and menu options. A small circular video overlay of a person speaking appears in the bottom-right." />
</Frame>

This section gives you a bird's-eye view of the KAgent dashboard and how to interact with agents and tools through the UI. Next, we explain A2A — the secure agent-to-agent communication protocol that KAgent uses for agent interactions and orchestration.

We then cover KAgent architecture and installation: core components, controllers, sidecar agents, and recommended deployment patterns. After installation you will validate the deployment and inspect running pods.

<Frame>
  <img alt="A slide titled &#x22;Kagent&#x22; on the left lists topics like Kagent installation & architecture, KMCP installation & overview, system prompts, debugging, and creating AI agents. On the right, a man speaks into a microphone and gestures with his hands." />
</Frame>

Example: after a successful installation you should see the KAgent-related pods running in the `kagent` namespace:

```bash theme={null}
