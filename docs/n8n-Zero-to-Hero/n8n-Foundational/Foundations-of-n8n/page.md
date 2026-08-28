# Foundations of n8n

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Foundational/Foundations-of-n8n/page

Introduction to n8n workflow automation covering nodes, AI agent architecture, triggers, data types, expressions, memory options and building reliable workflows with tools and error handling

Hey there — welcome.

This lesson covers the foundational concepts for n8n, the open source workflow automation tool that makes connecting apps, services, and AI agents simple.

What you'll learn:

* A short introduction to n8n and its building blocks (nodes).
* The architecture of AI agents and the API flow inside n8n.
* A demo use case (email → website flow).
* How input formats and expressions work in n8n.
* How n8n represents and handles common data types.

<Frame>
  <img alt="The image shows an agenda with five items related to n8n and automation processes, presented with a structured layout." />
</Frame>

Let’s dive in.

## What is n8n?

n8n (pronounced “n-eight-n”) is a free, open-source workflow automation platform (sometimes called “nodemation”). It’s designed to be a universal connector so you can visually compose workflows that pass data between apps, services, and AI models without heavy custom code.

Key SEO-friendly terms: n8n workflow automation, visual workflow builder, connect apps and services.

<Frame>
  <img alt="The image features a pink icon resembling a flowchart, accompanied by text describing n8n as a free and open workflow automation tool for connecting different apps and services." />
</Frame>

## Nodes: the building blocks

Everything in n8n is a node. Nodes come in two primary categories:

| Node Type | Role                                  | Example                                          |
| --------- | ------------------------------------- | ------------------------------------------------ |
| Trigger   | Starts workflows when an event occurs | Webhook, Email trigger, Chat trigger             |
| Action    | Performs work and returns output      | Send email, Call external API, Run LLM inference |

By connecting nodes you create reliable, repeatable automation flows.

## AI agents inside n8n

In n8n an AI agent is represented as a node. It integrates like any other node: it receives input, runs logic (via an LLM), optionally calls tools, and emits output downstream.

Three core elements of an n8n AI-agent node:

1. LLM (the model): e.g., [OpenAI](https://openai.com), [Anthropic (Claude)](https://www.anthropic.com), Meta Llama, or other models configured with API credentials.
2. Context window (short-term memory): prompt history or conversation context passed to the model.
3. Tools: external integrations the agent can call, such as Gmail, web scrapers, or other APIs.

Wire the agent node into the rest of the workflow (for example, sending results to [Slack](https://slack.com) or saving content to a CMS).

<Frame>
  <img alt="The image depicts a workflow architecture for n8n, showing an AI agent integrating with API tokens, LLMs, memory, tools, and nodes for event triggering and progression." />
</Frame>

## How it works — example flow

Typical step-by-step behavior:

1. A trigger provides user input (for example, a chat message or webhook).
2. The AI Agent node processes that input using the configured LLM and the provided context.
3. If required, the agent calls connected tools via APIs (for example, `Gmail` to read or send messages).
4. The agent returns a response that becomes the input for downstream nodes.

Editor visualization example:
chat trigger → AI Agent (GPT) → Gmail node → Slack node (notification)

### Default run logic (sequential execution)

When nodes are connected linearly, n8n executes them in order. If a node fails, the workflow will error by default unless you implement error handling (for example, enable “Continue On Fail”, add conditional logic, or configure dedicated error workflows).

<Frame>
  <img alt="The image depicts a flowchart titled &#x22;Default Run Logic,&#x22; illustrating a sequence of processes involving chat message receipt, video generation, captioning, and social media posting. Various steps are connected with directional arrows, showing the workflow progression." />
</Frame>

<Callout icon="warning">
  Design workflows with error handling and retries when calling external APIs. Use conditional nodes (`If`) and the `Continue On Fail` option to avoid full workflow failures on intermittent errors.
</Callout>

## Optional tools and conditionals

Tools attached to an AI agent are optional — the agent can decide whether to invoke them based on instructions and context. Add conditional `If` nodes to skip slow or unavailable APIs, and use retry logic or backoff strategies for robustness.

## Branching and parallel paths

A single trigger can branch into multiple independent paths. Branches run concurrently at the runtime level, and within each branch nodes execute sequentially. For example:

* Branch A: post to Slack
* Branch B: send email

Each branch proceeds through its own sequence of nodes.

<Frame>
  <img alt="The image displays a flowchart titled &#x22;Default Run Logic&#x22; that outlines a process involving chat message triggers, APIs, conditional logic, and message sending through Gmail and Slack." />
</Frame>

## Memory for AI agents

AI agents typically use two memory styles:

| Memory Type                       | Purpose                                                                  | Example / Technologies                                    |
| --------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------- |
| Context memory (short-term)       | Keeps immediate chat history and prompt state for coherent conversations | Pass chat messages in the prompt to the LLM               |
| Long-term searchable memory (RAG) | Stores documents as embeddings and retrieves relevant context            | Pinecone, Weaviate — Retrieval-Augmented Generation (RAG) |

Using a vector store plus RAG lets agents access external knowledge beyond the LLM’s training data, improving recall and accuracy for domain-specific queries.

<Frame>
  <img alt="The image depicts a diagram of memory types in an AI system, illustrating the interaction between an AI agent, OpenAI Chat Model, Simple Memory, and Pinecone Vector Store. It highlights context memory and retrieval-augmented generation (RAG) for stateless and stateful responses, and accessing external knowledge sources." />
</Frame>

## Inputs and outputs for nodes

Every node has an input and output. The input panel shows the payload received from the previous node; the output panel shows what the node returns (for example, the model's JSON response).

<Frame>
  <img alt="The image shows a split-screen interface for an AI chat application, illustrating an input message being processed and an output response generated in response. It includes sections for input variables, AI agent settings, and the resulting message output." />
</Frame>

## Data representations in n8n

n8n can display the same underlying data in multiple formats:

* Schema: a structured definition for fields.
* Table: spreadsheet-like rows and columns.
* JSON: the most common structured representation for programmatic access.
* Binary: files such as images, PDFs, and other blob data.

Use the representation that best matches the downstream consumer (APIs typically expect JSON; attachments use binary).

## Expressions and dynamic fields

Node fields accept:

* Static values (fixed strings), or
* Expressions that reference earlier nodes or runtime data.

Examples:

* Bracket notation: `{{ $json["chatInput"] }}`
* Dot notation: `{{ $json.user.name }}`

Use expressions to make your workflows dynamic and adapt values based on previous node outputs.

<Callout icon="lightbulb">
  When writing expressions or other snippets that contain braces or template syntax, wrap them in inline code or fenced code blocks so the MDX renderer does not attempt to evaluate them.
</Callout>

## Data types used in n8n

Common data types you’ll encounter:

| Type    | Description                      | Example                       |
| ------- | -------------------------------- | ----------------------------- |
| String  | Text values                      | `hello world`                 |
| Number  | Numeric values (ints and floats) | `42`, `3.14`                  |
| Boolean | True/false                       | `true` or `false`             |
| Array   | Ordered lists                    | `["James","Tony","Samantha"]` |
| Object  | Structured key/value data        | See example below             |

Array example:

```json theme={null}
[1, 2, 300, "alpha"]
```

Object example:

```json theme={null}
{
  "user": {
    "name": "Marconi",
    "email": "marconi@kodekloud.com"
  }
}
```

Access objects in expressions using dot or bracket paths, for example:

* `{{ $json.user.name }}`
* `{{ $json['user']['email'] }}`

## Community nodes

n8n has a vibrant community that builds connectors (community nodes). If an integration you need is not included by default, there’s a good chance someone in the community has implemented it.

## Quick recap

* Workflows are composed from nodes: triggers and actions.
* AI agents are implemented as nodes and can call external tools (Gmail, Slack, etc.).
* Nodes pass structured data: the output of one node becomes the input to the next.
* Key data types: strings, numbers, booleans, arrays, objects.
* Use expressions for dynamic values and combine short-term context with RAG/vector stores for more capable AI agents.

## Links and references

* [n8n Documentation](https://docs.n8n.io/)
* [OpenAI](https://openai.com)
* [Anthropic](https://www.anthropic.com)
* [Pinecone (Vector DB)](https://www.pinecone.io)
* [Retrieval-Augmented Generation (RAG) — Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/bb9d0021-2331-4d70-8853-4e4eb64070f3/lesson/28a3f8ee-80f5-486f-b0c0-b827417f6678" />
</CardGroup>
