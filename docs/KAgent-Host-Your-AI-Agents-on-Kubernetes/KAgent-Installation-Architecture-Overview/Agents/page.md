# Agents

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/Agents/page

Explains AI agent architecture, detailing instructions, tools, skills, and best practices for designing and managing agents in KAgent

In this lesson we cover agents and their architecture — a core component of KAgent. You’ll learn what agents are, how they’re structured, and how they use instructions, tools, and skills to act on behalf of users.

An AI agent is an application that interacts in natural language, typically backed by a large language model (LLM). Agents not only generate conversational responses but can also execute actions using callable capabilities. The main agent components are summarized below.

| Component          | Purpose                                                                          |
| ------------------ | -------------------------------------------------------------------------------- |
| Agent instructions | System-like prompt defining role, behavior, and constraints                      |
| Tools              | Callable functions that interact with external systems or the environment        |
| Skills             | Reusable capability descriptions or executable modules that guide agent planning |

## Agent instruction

Agent instructions act like a system prompt (similar to the system role in ChatGPT). They define the agent’s role, permitted actions, tone, and how to handle special situations (including collaboration with other agents).

Common elements of an agent instruction:

* Role definition (for example: "You are a Kubernetes agent that helps users manage cluster resources.")
* Response style (concise, verbose, formal, etc.)
* Allowed and disallowed actions
* Guidance for interacting with other agents or external systems

Example agent instruction (brief):

* You are a Kubernetes agent that helps users manage Kubernetes resources.
* Your responses should be clear and concise.
* Provide helpful information and guidance to users.

Primary goals of agent instructions:

* Define role and capabilities
* Help the agent interpret the environment and user intent
* Guide response style and decision-making

Quick recap — what an agent instruction enables:

1. Understand the task at hand.
2. Know which tools and skills are available.
3. Interpret the user's intent and produce an appropriate plan.

## Tools

Tools are the functions an agent can call to interact with external systems (e.g., cluster APIs, databases, third-party services). Tool definitions and descriptions are provided to the LLM along with the agent instruction so the model can choose which tool to call and with what inputs.

Typical example flow:

* User: "How many pods are failing in the payment namespace?"
* Agent sends the user query, agent instruction, and tool list (e.g., `list pods`, `get pod status`) to the LLM.
* LLM selects `list pods` with `namespace=payment`.
* Agent executes `list pods` and returns pod names.
* LLM decides to call `get pod status` for each pod.
* Agent runs `get pod status` for each pod, collects results.
* LLM aggregates the results, counts failing pods, formats a response, and returns it to the user.

<Callout icon="lightbulb">
  Design tool interfaces clearly: provide precise parameter schemas, expected outputs, and error semantics so the LLM can reliably choose and invoke the right tool.
</Callout>

Tool types in KAgent:

* Built-in tools: Provided by KAgent (examples: [Helm](https://helm.sh), [Argo Rollouts](https://argoproj.github.io/argo-rollouts/), gateway-related tools).
* MCP tools: External or third-party tools integrated via KAgent’s MCP mechanism (using KMCP or similar connectors).

## Skills

Skills are higher-level capabilities that make agent behavior goal-directed rather than purely reactive. They help the agent decide when and how to use tools to accomplish user goals.

* A skill can be a descriptive capability (metadata) or an executable component (container-based).
* Skills help map user intent to appropriate tool usage and planning strategies.
* Skills are reusable across multiple agents and are typically narrower and more focused than general system instructions.

<Frame>
  <img alt="A presentation slide titled &#x22;Skills — Characteristics&#x22; with three dark rounded boxes labeled &#x22;Wrapped functions,&#x22; &#x22;Reusable Prompt templates,&#x22; and &#x22;Synonym for a tool.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

Differences between tools and skills

* Tools are executable functions that produce direct output when invoked.
* Skills can be non-executable descriptions that guide planning or can be executable (container-based) capabilities.
* System instructions are global rules that are always active; skills are applied contextually and are typically task-specific.

<Frame>
  <img alt="A slide titled &#x22;Skills — Differences&#x22; showing a two-column comparison of &#x22;Tools&#x22; vs &#x22;Skills&#x22; and &#x22;System Instructions&#x22; vs &#x22;Skills.&#x22; Each column contains labeled boxes listing attributes like &#x22;Executable functions / Produce direct output&#x22; versus &#x22;Non-executable abilities / Guide task execution&#x22; and &#x22;Global rules / Always active&#x22; versus &#x22;Task-specific behavior.&#x22;" />
</Frame>

Skills are the building blocks that guide how an agent uses tools and plans actions. They help the LLM form a multi-step plan and decide which tools to call and when.

Example — same tool, different skills:

* Two agents (Troubleshooting Agent and Research Agent) both have access to a `DescribePod` tool:
  * Troubleshooting Agent (skill: incident resolution) uses `DescribePod` to inspect pod events, determine recovery actions, and possibly restart pods.
  * Research Agent (skill: information analysis) uses `DescribePod` to collect pod metadata, interpret it for insights, and answer analytical questions.

<Frame>
  <img alt="An infographic titled &#x22;Skills&#x22; showing two friendly robot agents — a Troubleshooting Agent and a Research Agent — linked by a central &#x22;Describe Pod&#x22; box. Each agent has a vertical flow of steps: the Troubleshooting Agent focuses on incident resolution and pod restart, while the Research Agent gathers pod details, interprets data, and answers queries." />
</Frame>

## Types of skills

KAgent supports two primary skill types:

1. A2A metadata skills — declarative descriptions that guide reasoning and mapping of user intent.
2. Container-based (executable) skills — packaged containers that provide runnable logic.

<Frame>
  <img alt="A slide titled &#x22;Types of Skills&#x22; showing two top categories (&#x22;A2A Skills Metadata&#x22; and &#x22;Container-Based Skills&#x22;) and a central &#x22;Actions-to-Actions Skills&#x22; area. Below that is a large &#x22;a2aConfig.skills&#x22; box with fields like Description, Examples, ID, and a &#x22;kagent&#x22; logo at the bottom." />
</Frame>

A2A metadata skills

* Structured descriptions of capabilities (not executable).
* Metadata fields commonly include: description, examples, ID, tags, input/output modes, and safety guidance.
* Use cases: guiding the LLM’s reasoning, mapping user phrasings to capabilities, and offering contextual examples.
* Typically defined under `a2aConfig.skills` with fields for `description`, `examples`, `id`, and `tags`.

Example A2A skill definition (declarative):

```yaml theme={null}
a2aConfig:
  skills:
  - id: get-resources-skill
    name: Get Resources
    description: Get resources in the Kubernetes cluster
    inputModes:
      - text
    outputModes:
      - text
    tags:
      - k8s
      - resources
    examples:
      - "Get all resources in the Kubernetes cluster"
      - "Get the pods in the default namespace"
      - "Get the services in the istio-system namespace"
      - "Get the deployments in the istio-system namespace"
      - "Get the jobs in the istio-system namespace"
      - "Get the cronjobs in the istio-system namespace"
      - "Get the statefulsets in the istio-system namespace"
```

Note: A2A skills are metadata-only; they do not contain executable logic.

Container-based (executable) skills

* Packaged as container images and include runnable logic, validation, and side-effectful operations.
* Referenced in agent config (for example via `spec.skills.reference` with an image URL) and loaded at runtime.
* Suitable when procedural steps or external side effects are required (for example: interacting with cloud APIs, running scripts, or performing automated remediation).

<Frame>
  <img alt="A slide titled &#x22;Types of Skills&#x22; comparing &#x22;A2A Skills Metadata&#x22; and &#x22;Container-Based Skills.&#x22; It shows five labeled boxes: Executable procedures, Callable behaviors, Validation steps, Reusable functions, and Direct execution." />
</Frame>

Container-based skill lifecycle:

1. Implement skill logic (scripts, entrypoint, resources).
2. Package into a container image.
3. Push the image to a container registry.
4. Reference the image in the agent configuration (`spec.skills.reference`).
5. Agent loads the container at runtime and exposes callable operations.

Benefits:

* Reusable and provider-agnostic (can be invoked by agents using OpenAI, Vertex AI, Azure OpenAI Service, Ollama, and others).
* Enables deterministic, testable procedures for complex or side-effecting operations.

## Best practices for skills

Follow these guidelines when designing skills to maximize discoverability, reliability, and maintainability:

* Single responsibility: each skill should represent one clear capability.
* Provide diverse, realistic examples: include multiple phrasings users might use to invoke the skill.
* Use descriptive tags: tags help organize and search skills across teams.
* Align skills with tools: ensure the skill’s described behavior matches the tool(s) the agent can call.
* Keep skills narrow and focused: prefer "generate PDF" or "generate docx" over a broad "document generator" to make behavior predictable and testable.

<Frame>
  <img alt="A slide titled &#x22;Best Practices for Skills&#x22; with three numbered cards. The cards advise defining one clear capability per skill, providing diverse realistic usage examples, and using descriptive tags for easy management." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Best Practices for Skills&#x22; showing five numbered cards across the page with brief tips for skill design. The fifth card is highlighted and reads &#x22;Keep each skill narrowly focused.&#x22;" />
</Frame>

## Skill management

Manage skills through a standard lifecycle to ensure versioning, reuse, and discoverability:

* Create the skill metadata or implementation.
* Containerize executable skills and push the image to a registry.
* Store skills in a centralized skill/agent registry that supports push/pull/versioning.
* Reference skills from agents and reuse across teams and agents.

A centralized registry simplifies sharing, version control, and governance of skills.

<Frame>
  <img alt="A flow diagram titled &#x22;Skill Management&#x22; showing steps from Skill Creation to Containerization, into a Skill Registry (built & pushed via AgentRegistry/Claude), and finally Agents that reuse those skills." />
</Frame>

<Callout icon="lightbulb">
  When possible, start with an A2A metadata skill to describe the capability and add container-based skills only for actions that require procedural logic, side effects, or external integration.
</Callout>

Links and references

* [ChatGPT](https://chat.openai.com)
* [Helm](https://helm.sh)
* [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
* [OpenAI](https://openai.com)
* [Vertex AI](https://cloud.google.com/vertex-ai)
* [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
* [Ollama](https://ollama.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/7d947e6a-6983-4a54-800b-c4637ce9a5ba" />
</CardGroup>
