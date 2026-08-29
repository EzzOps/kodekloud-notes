# Prompt Structure Components

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/System-Prompts-for-AI-Agent-Building/Prompt-Structure-Components/page

Guide for designing AI agent prompts and configurations covering role, goals, tools, operational protocols, safety, testing, and storage best practices.

This guide breaks down the core components used to define an AI agent. Use these sections as a checklist when designing system prompts and agent configurations.

## 1. Role definition

* Define the agent's identity and domain expertise (for example, "You are a Kubernetes expert with deep knowledge of cluster operations").
* State experience level and scope of authority to set user expectations and constrain behavior.

## 2. Goal statement

* Clearly state the agent’s primary objective (for example, "Your goal is to help users manage their Kubernetes cluster").
* A concise goal guides decision-making and keeps outputs aligned with user intent.

## 3. Operational protocols

* Describe how the agent begins work (initial assessment), the execution strategy (step-by-step process), and troubleshooting flows.
* Include validation rules: how the agent verifies actions, when it asks clarifying questions, and when it escalates or stops.
* Define expected step boundaries (what to attempt and what to avoid).

## 4. Safety guidelines

* Specify risk-management constraints (for example: minimize disruption, operate in read-only mode by default, favor small incremental changes).
* Enumerate forbidden actions and contextual constraints (e.g., do not delete resources without explicit confirmation).

## 5. Tool descriptions

* For each tool the agent can access, define:
  * Purpose and typical use cases.
  * Inputs and outputs (data formats and example payloads).
  * Interaction patterns with other tools.
  * Example usage snippets.
* Ensure tools are unambiguous and mutually compatible to avoid overlap.

## 6. Best practices

* Start simple: define a basic role and purpose first, then add tools and complexity.
* Avoid assigning multiple overlapping tools to the same agent to reduce ambiguity.
* Be explicit—spell out behaviors and constraints; do not rely on implicit assumptions.

## 7. Behavior guidelines

* Provide concrete rules for runtime behavior, such as:
  * “Always confirm destructive changes before applying.”
  * “Log each action and its rationale.”
  * “Ask for missing information or clarification.”
* Use examples to illustrate allowed vs. disallowed behaviors.

## 8. Structure for clarity

* Use numbered sections, bullet lists, and short paragraphs so models can parse instructions reliably.
* Explicit, structured prompts produce more predictable behavior from LLMs.

## 9. Iterate and redefine

* Treat agent definition as iterative:
  * Create an initial prompt, test with real queries, analyze outputs, and refine.
  * Schedule regular reviews and A/B tests to detect regressions or drift.

## 10. Advanced technique: use another model to improve prompts

* Use a second LLM (for example, [ChatGPT](https://chat.openai.com/) or [Claude](https://www.anthropic.com/product/claude)) to:
  * Review and improve your system prompt.
  * Suggest clearer role statements and tool descriptions.
  * Propose alternative phrasing or edge cases to handle.
* Always validate suggestions—models can hallucinate plausible-sounding but incorrect recommendations.

<Frame>
  <img alt="A slide titled &#x22;Advanced Technique: Use Another Model&#x22; showing a woman and a friendly robot interacting via a large chat window. The chat bubble displays a sample agent prompt asking to improve a prompt's effectiveness." />
</Frame>

<Callout icon="lightbulb">
  Always review and validate outputs from any model used to refine prompts. Models can produce plausible-sounding but incorrect recommendations (hallucinations).
</Callout>

## Share common prompts across agents

Store reusable system prompts centrally to simplify updates and maintain consistency across agents. Common approaches:

* Inline in the agent definition — fast for experiments.
* ConfigMap — reusable and non-sensitive prompts.
* Secret — for sensitive prompts (store base64-encoded values).

If storing prompts in a Secret, include a base64-encoded system message. Example Secret:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: my-agent-secret
  namespace: kagent
data:
  # Replace the value with the base64-encoded prompt, for example: echo -n "your-prompt" | base64
  system-message: `base64-encoded-prompt`
```

To reference stored prompts from a declarative agent configuration, point `systemMessageFrom` to a ConfigMap or Secret. Example snippets:

```yaml theme={null}
