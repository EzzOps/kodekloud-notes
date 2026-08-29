# Workflow 1 Your First Simple Email AI Agent

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Workflow-1-Your-First-Simple-Email-AI-Agent/page

Step-by-step guide to build and test an n8n AI agent that drafts and sends emails using OpenAI, session memory, and a Gmail integration.

This guide walks through building a simple email-sending AI agent in n8n. Follow the steps in order: add a trigger, inspect its output, connect an AI Agent, add memory and tools (Gmail), and test the flow end-to-end.

## 1) Add a Trigger Node

Open the workflow editor and add a trigger node. Trigger nodes start a workflow when an event occurs. Click the plus button in the top-right to view available triggers.

For this lesson choose the **When Chat Message Received** trigger (it starts the workflow whenever a chat message arrives). The simplest alternative is the Manual Trigger, which runs only when you click it.

<Frame>
  <img alt="The image shows a screenshot of the n8n workflow automation platform. There's a central area labeled &#x22;My Email Agent&#x22; with options for adding workflow steps and triggers on the right panel." />
</Frame>

A quick visual hint: trigger nodes display a lightning icon to differentiate them from regular nodes.

<Frame>
  <img alt="The image shows a screenshot of a workflow editor in n8n, displaying a simple automation with a trigger node for when a chat message is received. The interface includes options for editing and managing workflows." />
</Frame>

## 2) Inspect Trigger Output

Open the When Chat Message Received node to see its outputs — trigger nodes only have outputs (no inputs). n8n presents node data in three views: OUTPUT (readable), JSON, and Schema (typed fields useful for drag-and-drop).

Example OUTPUT view:

```text theme={null}
OUTPUT
  1 item
    A. sessionId    2c2a81b51e9a4958ac03e403b3589b37
    A. action       sendMessage
    A. chatInput    hello
```

Same data as JSON:

```json theme={null}
[
  {
    "sessionId": "2c2a81b51e9a4958ac03e403b3589b37",
    "action": "sendMessage",
    "chatInput": "hello"
  }
]
```

Use the Schema view if you want to drag structured fields (like `chatInput`) directly into downstream node parameters.

## 3) Add the AI Agent Node

Add an AI Agent node (AI → AI Agent). When you connect nodes, the previous node’s output becomes the next node’s input automatically. For example, the chat trigger’s output will populate the AI Agent’s input.

Small output snippet showing `sessionId`:

```text theme={null}
OUTPUT
sessionId
2c2a81b51e9a4958ac03e403b3589b37
```

There are three key configuration areas for the AI Agent node:

* LLM (Large Language Model) — choose which model processes user inputs.
* Memory — persistent context about prior conversation turns.
* Tools — external integrations the agent can call (e.g., Gmail).

Below are clear steps for each.

### LLM (Connect to OpenAI)

* From the LLM dropdown select an OpenAI Chat Model.
* Click **Create New Credential** and supply your OpenAI API key from the OpenAI Developer Platform: [https://platform.openai.com/](https://platform.openai.com/).
* Pick a model appropriate for your use case (for example, `gpt-4o-mini` or another OpenAI chat model).

### Memory (Keep Conversation Context)

Use Simple Memory if you want the agent to remember prior interactions within a session.

* Add a Simple Memory node and ensure it’s keyed to the session (so memory is stored per `sessionId`).
* Set the context window length (for example, `5`) to retain the last N interactions.
* Use an expression for the session key, for example: `{{ $json.sessionId }}`.

<Frame>
  <img alt="The image shows a workflow interface from n8n, featuring nodes for chat message receipt and interaction with an AI agent. The workspace displays how the nodes connect and process a chat input message." />
</Frame>

Memory behavior example:

* Without memory:
  * User: "Hello, my name is Mark."
  * User (next): "What is my name?"
  * Agent reply (no memory): apologizes for not having access to personal info.

* With Simple Memory attached:
  * User: "Hello, my name is Mark."
  * User (next): "What is my name?"
  * Agent reply: "Your name is Mark. How can I help you today, Mark?"

<Frame>
  <img alt="The image shows a workflow diagram in an automation tool, featuring a chat message trigger linked to an AI agent, utilizing OpenAI's chat model and a memory component. It includes an interface displaying chat input and the AI agent's response output." />
</Frame>

### Tools (Add Gmail to Send Email)

For an email agent, attach a Gmail node so the AI can send messages directly.

* Create or select Gmail credentials. n8n Cloud: OAuth2 recommended. Self-host: service account possible.
* Configure the Gmail node:
  * Tool Description: leave `Set Automatically` so the agent decides when to use Gmail.
  * Resource: `message`
  * Operation: `send`
  * Email Type: `text` (choose `html` for formatted content)
  * Message: choose `Determine by Model` so the AI constructs the body

<Frame>
  <img alt="The image shows a workflow setup in the n8n automation platform, illustrating a process involving chat message reception, AI agent processing, and integration with OpenAI and Gmail services. The interface includes a visual representation of steps and connections, indicating tasks like drafting an email for a marketing meeting." />
</Frame>

## 4) Passing Dynamic Input vs Fixed Input

You can supply the AI Agent with a fixed (literal) user message or an expression that pulls dynamic values from the previous node.

> **lightbulb** Fixed input is a literal, unchanging message (for example, "Please send an email"). Expression allows dynamic values from the previous node (for example, the chat message). Use Expression to pass the actual chat text into the AI Agent so it reacts to user input.

To pass chat content dynamically, switch the user message field to Expression and insert the chat variable:

```text theme={null}
{{ $json.chatInput }}
```

At runtime the actual chat text (e.g., "Send an email to my boss...") will populate the input.

## 5) System Message (Agent Role & Behavior)

Under Options → Add Option → System Message add a guiding prompt that defines the agent’s role. Example:

```text theme={null}
You are a helpful email assistant. Craft effective, succinct emails based on the user's instructions. Use the Send Email tool when the user asks to send an email.
```

For production, refine this system message to match tone, compliance, or company policy.

## 6) Example Conversation & Drafting Email

Try this conversation to see the full flow:

1. User: "Hello, my name is Mark." → agent stores the name in memory and replies.
2. User: "Send an email to my boss at [marconi@kodekloud.com](mailto:marconi@kodekloud.com) about the upcoming marketing meeting on 26th August 2025."

The agent may ask follow-ups (subject, recipient name). If you instruct it to draft subject and body, it could generate:

Subject:

```text theme={null}
Upcoming Marketing Meeting on August 26, 2025
```

Body:

```text theme={null}
Dear Boss's Name,

I hope this message finds you well.

I wanted to remind you about the upcoming marketing meeting scheduled for the 26th of August 2025. We will be discussing our strategies and plans for the upcoming quarter. Please let me know if there are any specific topics you would like to address during the meeting.

Looking forward to your input,
Mark
```

If placeholders (e.g., "Boss's Name") appear, provide the real name in chat (for example, "Mumshad"). The agent will update the draft and ask for confirmation before sending. When you confirm, the AI Agent will call the Gmail tool to send the message.

Note: Gmail may append an n8n attribution by default. To remove it open the Gmail node, go to Options → Add Options → `Append n8n Attribution` and toggle it off.

## 7) Useful Node Controls & Development Tips

* Node controls (top-right of each node):
  * Play button (Execute Step): runs just this node — useful for iterative testing.
  * Power button: deactivate/reactivate the node.
  * Bin icon: delete the node.

* Pin node data for development: in the trigger node’s top-right corner click **Pin** to reuse a snapshot of the trigger output (avoid re-triggering external APIs or consuming credits).

Example pinned output snapshot:

```text theme={null}
OUTPUT
1 item
  sessionId    2c2a81b51e9a4958ac03e403b3589b37
  action       sendMessage
  chatInput    yes
```

## 8) Activate, Public Chat & Debugging

* Activate workflow: toggle **Activate workflow** at the top to receive production requests. Activation provides a production chat URL that hits your workflow for each incoming message.
* Make chat publicly available: open the chat node and toggle **Make Chat Publicly Available** to get a public URL (may take a few seconds to spin up).

The public chat UI looks like this:

<Frame>
  <img alt="The image shows a webpage with a dark header saying &#x22;Hi there!&#x22; alongside a waving hand emoji, and a chat interface below asking how it can assist today." />
</Frame>

You can add authentication to the public chat and set an initial message, but this lesson keeps it simple.

### Debugging & Execution Views

* Editor view — build and edit workflows.
* Executions view — shows logs for runs (date, time, and run type). Test runs have a beaker icon.
* Copy to editor on an execution — import execution data into the editor for debugging. This reproduces the exact inputs/outputs for troubleshooting.

> **warning** Keep API keys and credentials secure. Monitor your OpenAI usage to avoid unexpected costs. For production use, apply rate limiting, logging, and appropriate permission controls on public endpoints.

## Quick Reference Table

| Concept        | Purpose                    | Example / Tip                                       |
| -------------- | -------------------------- | --------------------------------------------------- |
| Trigger        | Starts the workflow        | `When Chat Message Received`                        |
| AI Agent (LLM) | Processes user intent      | OpenAI chat model (set credentials)                 |
| Memory         | Persistent session context | `Simple Memory` with key `{{ $json.sessionId }}`    |
| Tool           | External action (email)    | Gmail node — Resource: `message`, Operation: `send` |
| System Message | Instructs agent behavior   | "You are a helpful email assistant..."              |

That completes this lesson on building your first simple email AI agent in n8n. A lab is available where you can recreate the same AI agent end-to-end and validate your setup.

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/e6a77d54-130e-4b6c-8e1a-dc4983cfbd44)
