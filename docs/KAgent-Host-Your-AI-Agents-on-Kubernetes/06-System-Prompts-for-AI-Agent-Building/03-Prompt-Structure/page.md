# Example: reference a prompt stored in a ConfigMap
declarative:
  systemMessageFrom:
    type: ConfigMap
    name: my-agent-config
    key: system-message

# Example: reference a prompt stored in a Secret
declarative:
  systemMessageFrom:
    type: Secret
    name: my-agent-secret
    key: system-message
```

## Checklist for prompt content

Use this checklist when authoring or reviewing prompts. It ensures completeness and makes prompts easier to maintain.

| Component             | What to include                                  |
| --------------------- | ------------------------------------------------ |
| Role definition       | Clear identity and expertise                     |
| Goal statement        | Concise, outcome-focused objective               |
| Tool list             | Names and short purposes for each tool           |
| Tool details          | Inputs, outputs, examples, interaction rules     |
| Operational protocols | Start-up checks, execution steps, rollback rules |
| Safety & behavior     | Constraints, forbidden actions, escalation rules |
| Testing & iteration   | Plans for validation and refinement              |

## Summary: prompt evolution

* Start with a minimal working prompt: role + purpose.
* Add tools and quick usage notes.
* Expand per-tool descriptions, examples, and operational protocols.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary — Prompt Structure Evolution&#x22; listing three steps: 01 Simple — Role and purpose; 02 With Tools — Add tool list; 03 Detailed Tools — Add tool descriptions and usage. The design has a dark left column with the title and a pale right area with blue numbered markers and brief text." />
</Frame>

## Summary of key principles

* Start simple and add complexity gradually.
* Be explicit about desired behavior and constraints.
* Structure prompts for clarity (numbered lists and sections).
* Iterate and refine from real-world testing and trace analysis.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary — Key Principles&#x22; showing four numbered points: 01 Start simple, add complexity gradually; 02 Be explicit about behavior; 03 Structure for clarity; 04 Iterate and refine." />
</Frame>

## Storage options recap

* Inline in the agent definition — ideal for quick experiments.
* ConfigMap — reusable, non-sensitive prompts for teams.
* Secret — store sensitive prompts base64-encoded.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary: Storage Options&#x22; listing three approaches: 01 Inline in agent definition, 02 ConfigMap for reusable prompts, and 03 Secret for sensitive prompts. The slide has a dark left panel with the title and a pale right side showing three blue numbered markers beside the items." />
</Frame>

## Next steps

* Upcoming materials will cover troubleshooting agents using traces and logs.
* Hands-on exercises will show how to build both declarative and imperative agents so you can apply these concepts in practice.

Thank you.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/9516a0aa-00b1-4461-a622-cc60e510c96a/lesson/b7cb3799-4e18-44f3-ab53-364ba7121a4b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/1f59e7e3-e5ab-4b77-b210-8c954216f293/lesson/5832efff-cc5b-4b77-bfe5-a2cc76c54c78" />
</CardGroup>


# Prompt Structure

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/System-Prompts-for-AI-Agent-Building/Prompt-Structure/page

Guide to designing clear actionable system prompts for Kubernetes management agents, covering tools, parameters, operational protocols, safety guardrails, and confirmation rules

In the previous lesson we covered core concepts of system prompts. This lesson focuses on prompt structure and practical details — how to design a clear, actionable system prompt for an agent that manages Kubernetes clusters.

<Frame>
  <img alt="A dark teal presentation slide with the KodeKloud logo and the title &#x22;Prompt Structure.&#x22; The subtitle reads &#x22;Building Effective System Prompts.&#x22;" />
</Frame>

High-level advice: start with a single, well-scoped objective. Avoid combining unrelated roles into one agent — a focused agent is more reliable and easier to secure.

We will construct system prompts incrementally:

1. Start simple (role + purpose).
2. Add available tools.
3. Add detailed tool descriptions (parameters, outputs, when to use).
4. Define operational protocols (assessment, plan, execute, verify).
5. Add safety guardrails and confirmations.

<Frame>
  <img alt="A presentation slide titled &#x22;Introduction&#x22; with three colored circular icons and captions outlining a tutorial: &#x22;How to build a system prompt step by step,&#x22; &#x22;Starting simple and adding complexity,&#x22; and &#x22;Best practices for prompt structure.&#x22; The slide uses a dark background and simple line icons." />
</Frame>

Start simple: define the role and the purpose so the agent has a single primary objective.

Example basic system prompt:

```text theme={null}
You are a Kubernetes agent. You help users manage their Kubernetes cluster.
```

This sets role and purpose but is not actionable: it omits available commands, expected inputs/outputs, and operational behavior. Add those next.

<Frame>
  <img alt="A presentation slide titled &#x22;Introduction&#x22; showing a &#x22;Start Simple&#x22; step. Below it is a two-column box with a green check listing positives (defines the agent's role; states the purpose) and a red X listing negatives (not enough detail; doesn't tell the agent what it can do)." />
</Frame>

Add tools: make a compact, explicit list of the tools the agent can call. Name each tool and give a one-line description so the agent can map user intent to concrete actions.

Example tools list:

```text theme={null}
You can use the following tools to help users manage their Kubernetes cluster:

1.  list_resources: List all resources of a given type in the cluster

2.  get_all_resources: Get all resource types in the cluster

3.  get_pod_logs: Get the logs of a pod

4.  apply_resource: Apply a resource manifest to the cluster
```

Tool names help, but the agent needs usage details: required parameters, expected outputs, default behaviors, and whether a tool mutates the cluster.

<Frame>
  <img alt="A presentation slide titled &#x22;Introduction&#x22; showing step &#x22;02 Add Tools.&#x22; A two-column box lists pros (green check) like &#x22;lists available tools&#x22; and &#x22;agent knows what it can do&#x22; and a con (warning icon) noting &#x22;still needs more detail on tool usage.&#x22;" />
</Frame>

Detailed tool documentation — what to include for each tool:

* Required parameters and expected formats (for example, `resource_type`, `namespace`, `pod_name`, `manifest_url`).
* Whether the tool is read-only or can mutate the cluster.
* When to choose this tool (mapping from user intent to tool).
* Default behaviors (for example, default namespace = `default` vs. `--all-namespaces`).

Practical example guidance for the tools above:

* `list_resources` — Use when the user asks for a list of resources of a specific type (e.g., "list pods" or "show deployments in namespace X"). Accepts `resource_type` and optional `namespace`. If `resource_type` is missing, ask a clarifying question instead of calling the tool.
* `get_all_resources` — Use to enumerate all resource kinds present in the cluster (useful for discovery or inventory).
* `get_pod_logs` — Use to fetch logs for a specific pod; accepts `pod_name`, optional `container_name`, and `namespace`. Prefer `get_pod_logs` only after confirming the correct pod via `list_resources`.
* `apply_resource` — Use to apply a YAML manifest provided inline or via a URL. Require the agent to validate the manifest, confirm target cluster and namespace, and warn about potential blast radius before applying.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Introduction&#x22; with an illustrated person using a laptop and a speech bubble saying &#x22;You're a Kubernetes agent. You help users manage their Kubernetes cluster.&#x22; To the right is a text panel describing a tool called &#x22;get_all_resources&#x22; for managing Kubernetes resources." />
</Frame>

Tool reference (compact summary)

| Tool                | Purpose & When to Use                                                                        | Parameters & Behavior                                                                                                                         |
| ------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `list_resources`    | List resources of a specific kind (pods, deployments, services). Use for targeted discovery. | `resource_type` (required), `namespace` (optional). Read-only. If missing `resource_type`, ask a follow-up question.                          |
| `get_all_resources` | Enumerate all resource kinds in the cluster for inventory/discovery.                         | No parameters required. Read-only. Useful as a first discovery step.                                                                          |
| `get_pod_logs`      | Retrieve logs for a specific pod to troubleshoot issues.                                     | `pod_name` (required), `container_name` (optional), `namespace` (optional). Read-only. Confirm pod identity via `list_resources` first.       |
| `apply_resource`    | Apply a YAML manifest or URL to create/update resources.                                     | `manifest` or `manifest_url` (required). Mutating. Validate manifest, confirm cluster & namespace, require explicit confirmation for changes. |

A few practical rules for tool usage:

* Validate required parameters before calling a tool. For instance, confirm a `resource_type` for `list_resources`.
* Normalize user language to canonical Kubernetes kinds (map "app", "application", or "svc" to `deployments`, `services`, etc.).
* Chain tools deliberately: discover with `get_all_resources` or `list_resources`, then inspect with `get_pod_logs` or other read-only tools, and only mutate with `apply_resource` after validation and confirmation.
* For mutating operations (apply/delete), accept either a full manifest or a reference (URL, kind/name). For deletes, permit both full manifest or resource identifiers.

Operational protocols — define how the agent assesses, plans, executes, and verifies changes:

* Initial assessment: confirm cluster context, access level, and the scope of the requested change. Ask clarifying questions for missing critical details.
* Execution strategy: prefer read-only checks first, validate intended changes, make incremental updates, and verify results after each step.
* Verification & documentation: after executing a change, run verification checks (status, events, logs), and record actions and outcomes.
* Troubleshooting approach: narrow root cause systematically — review logs, events, metrics, configuration, and recent changes before proposing or applying fixes.

<Frame>
  <img alt="A presentation slide titled &#x22;Introduction&#x22; with a highlighted &#x22;Add Behavior Guidelines&#x22; badge and a rounded text box listing an operational protocol for Kubernetes cluster management. A simple illustration of a person sitting with a laptop appears on the left against a dark background." />
</Frame>

Safety and guardrails — include explicit constraints in the system prompt:

* Default to non-destructive, read-only actions unless the user explicitly requests a mutating operation.
* Always confirm the target cluster and namespace before any mutating operation.
* Consider blast radius and prefer small, reversible changes.
* Back up critical configuration before editing.
* When unsure, ask clarifying questions instead of taking action.

<Callout icon="lightbulb">
  Be explicit in the system prompt about required confirmations, parameter validation, and the agent’s default safety-first behavior. This reduces accidental destructive actions and makes agent behavior more predictable.
</Callout>

<Callout icon="warning">
  Do not perform mutating operations (for example, `apply_resource`) without explicit, unambiguous confirmation that includes target cluster and namespace, and a description of the intended change.
</Callout>

System prompt checklist — what a complete prompt should include:

| Component                               | Why it matters                                                            |
| --------------------------------------- | ------------------------------------------------------------------------- |
| Single clear role & purpose             | Keeps behavior focused and predictable.                                   |
| Tools list (names + short descriptions) | Allows intent → capability mapping.                                       |
| Detailed tool docs                      | Enables correct parameter use, chaining, and expected outputs.            |
| Operational protocols                   | Defines assessment, execution, verification, and documentation steps.     |
| Safety guardrails & confirmation rules  | Prevents accidental destructive actions and clarifies required approvals. |

Summary

1. Start with a single, explicit role and primary objective.
2. Enumerate available tools with concise descriptions.
3. Provide detailed tool documentation: parameters, formats, read/write behavior, and when to use each tool.
4. Define operational protocols for assessment, execution, verification, and troubleshooting.
5. State safety guardrails and explicit confirmation requirements for mutating actions.

Being explicit about behavior, tools, and safety significantly improves agent reliability and reduces risk.

Further reading and references

* [Kubernetes Concepts — Official Docs](https://kubernetes.io/docs/concepts/)
* [Kubernetes API Reference](https://kubernetes.io/docs/reference/)
* [Prompt engineering best practices (overview)](https://en.wikipedia.org/wiki/Prompt_engineering)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/9516a0aa-00b1-4461-a622-cc60e510c96a/lesson/824501ea-e984-408a-8da8-35c07a69a570" />
</CardGroup>
