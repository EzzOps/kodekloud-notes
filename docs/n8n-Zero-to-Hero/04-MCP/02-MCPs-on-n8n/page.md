# MCPs on n8n

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/MCP/MCPs-on-n8n/page

Guide to using the Model Context Protocol in n8n to let AI agents call external tools like Gmail via MCP client and server with setup, transport, and troubleshooting steps

In this article we’ll explain how to use MCP (Model Context Protocol) inside n8n to let AI models call external tools (like Gmail) in a reusable, standardized way. You’ll get a practical, step-by-step walkthrough showing how to wire an MCP Client tool inside an AI Agent to an MCP Server Trigger that runs the actual tool in n8n.

At a high level, MCP (Model Context Protocol) standardizes how models discover and call external tools. Instead of building a custom integration per model or service, MCP defines a shared contract so the same connector can be reused across models and platforms — simplifying tool reuse, governance, and security in workflows.

<Frame>
  <img alt="The image shows a workflow interface of n8n with nodes labeled &#x22;When chat message received,&#x22; &#x22;AI Agent,&#x22; &#x22;OpenAI Chat Model,&#x22; and &#x22;Simple Memory,&#x22; indicating a setup involving AI and memory tools. The interface includes a sidebar with options like &#x22;Admin Panel,&#x22; &#x22;Templates,&#x22; and &#x22;Variables.&#x22;" />
</Frame>

## Why use MCP vs a direct API integration

MCP is about reuse and standardization. A direct API integration is usually one-to-one: you build an adapter per service and per model. MCP lets you expose tools through a common protocol so multiple models or agents can call the same tool without each needing a bespoke connector.

| Approach                     |                                                                                          When to use | Pros                                                                    | Cons                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| MCP (Model Context Protocol) | When multiple models/agents will share the same tools and you want a standard, discoverable contract | Reuse across models, consistent governance, fewer duplicated connectors | Requires implementing MCP server/client contract      |
| Direct API integration       |                                              When a single model/service needs a bespoke integration | Simple for single-use cases                                             | Duplication, harder to manage across models and teams |

## Example: AI chat that sends email via an MCP tool

This walkthrough shows how a chat-based AI (OpenAI chat model) can use an MCP Client tool to request sending an email, and how an MCP Server Trigger in n8n receives that request and executes a Gmail node.

High-level steps (we follow these in the same workflow for clarity):

1. Start with a chat trigger → AI Agent → memory (Simple Memory) flow.
2. Add an MCP Server (MCP Trigger node) to accept client calls.
3. Add an MCP Client tool to the AI Agent configuration and point it at the MCP Server URL.
4. Configure server transport (HTTP Streamable recommended) and authentication.
5. Run the workflow, send a chat prompt, and observe the server executing the Gmail action.

### 1) Add an MCP Server Trigger

Add the MCP Trigger node to act as your server endpoint. The trigger exposes a Test URL and a Production URL — functionally similar to webhooks — which the MCP Client will call.

<Frame>
  <img alt="The image displays an interface for configuring an MCP Server Trigger, featuring a Test URL, authentication options, and paths. The interface includes buttons for executing steps and copying the MCP URL." />
</Frame>

You can enable authentication on the MCP Server if you want production-grade security. For fast demos, you can use the Test URL without authentication — copy the Test URL to the clipboard; that is the endpoint the MCP Client will call.

<Callout icon="warning">
  Leaving your MCP Server unsecured (no authentication) is acceptable only for local demos. For any shared or production environment enable authentication and secure your endpoints.
</Callout>

### 2) Configure the MCP Client in the AI Agent

Open the AI Agent’s tool configuration and add an MCP Client. Paste the MCP Server Test URL into the client’s `endpoint` field so the client knows where to send tool calls.

<Frame>
  <img alt="The image shows a software interface for &#x22;MCP Client&#x22; with settings for parameters such as endpoint, server transport, authentication, and tools to include. The interface is divided into sections labeled &#x22;INPUT&#x22; and &#x22;OUTPUT.&#x22;" />
</Frame>

One critical client setting is the server transport. n8n previously recommended SSE (Server-Sent Events) for persistent connections, but SSE has been deprecated in favor of HTTP Streamable.

<Callout icon="lightbulb">
  SSE uses a persistent connection for server-to-client events. HTTP Streamable streams responses over chunked HTTP, allowing the client to start processing partial results as they arrive. For new n8n setups, choose HTTP Streamable.
</Callout>

* Set Server Transport to `HTTP Streamable`.
* If the MCP Server requires credentials, configure matching authentication on the MCP Client; otherwise set to `None` for demos.

### 3) Inform the model about the tool (system message)

Tell the model that a tool is available and when to use it:

```text theme={null}
You are a helpful email assistant with a tool attached. Use the tool to send emails when requested.
```

<Frame>
  <img alt="The image shows a user interface of an AI tool configuration panel, with settings for an AI agent, including a section for parameters and options. There are input data fields, a system message configuration, and an option to execute or view data." />
</Frame>

### 4) Run the flow and trigger the model

Execute the workflow and send a chat prompt to the agent. Example prompt:

"Hi, can you send an email to [marconi.zammo@codecloud.com](mailto:marconi.zammo@codecloud.com) regarding my appointment on Thursday from Jason."

When the model decides to use the tool, it will call the MCP Client, which forwards the request to your MCP Server Trigger. The server executes the configured tool — in this demo, a Gmail action that composes and sends the email using the Gmail node’s account.

<Frame>
  <img alt="The image shows a workflow diagram in a software tool that includes nodes like &#x22;AI Agent,&#x22; &#x22;OpenAI Chat Model,&#x22; and &#x22;MCP Server Trigger,&#x22; with a message waiting to trigger an event. There are also sidebar options for managing the workflow and user interactions." />
</Frame>

Demo logs showed the sent message was:

"Hello, I'm writing to confirm my appointment on Thursday. Best regards, Jason."

Because the system prompt was minimal, the email body was short. For production, expand the system prompt or add instruction-following steps so the model fills subject lines, recipient names, and message style appropriately.

## Troubleshooting and tips

* If the MCP Client can’t reach the server: verify the Test URL, confirm the server is active, and check any authentication settings.
* If partial responses are missing or delayed: confirm Server Transport is set to `HTTP Streamable` and your n8n instance supports it.
* For complex email generation: add fields in the system prompt or use a follow-up step to collect subject, salutation preferences, or signatures.

## Links and references

* n8n Documentation: [https://docs.n8n.io/](https://docs.n8n.io/)
* OpenAI Platform docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
* For the MCP spec and community resources, check your platform or vendor documentation that describes Model Context Protocol implementations.

For advanced MCP usage, consult the official MCP documentation and your provider’s guidelines to find available servers, client capabilities, and best practices for authentication and governance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/e2e9ccd6-d35a-4a9e-b758-7918221eedc3/lesson/4311ad91-a05a-4cf2-b807-cf0137a49dfe" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/e2e9ccd6-d35a-4a9e-b758-7918221eedc3/lesson/2428ca26-cff3-417a-bda9-9df2bf05ebae" />
</CardGroup>
