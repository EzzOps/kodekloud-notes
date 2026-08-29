# Workflow 8 Fun Slack use case Let AI do your job

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Workflow-8-Fun-Slack-use-case-Let-AI-do-your-job/page

Guide to building an n8n workflow that lets an AI agent read Slack messages, reply as a user, and optionally fetch Google Docs for retrieval augmented responses.

In this lesson we build a practical n8n workflow that lets an AI agent reply on your behalf in Slack. We’ll reuse an existing workflow, add the required Slack permissions, configure n8n to use a user OAuth token, and optionally extend the agent with a simple Retrieval-Augmented Generation (RAG) tool (a Google Doc) so it can fetch project updates before replying.

High-level flow

1. Configure Slack OAuth scopes and reinstall the app.
2. Create an n8n Slack credential using the user OAuth token.
3. Update the Slack Trigger to capture all message events and ignore your own messages.
4. Configure the AI Agent in n8n (system prompt, model, memory).
5. Make the Send Message node reply dynamically to the originating channel and “Send as User”.
6. (Optional) Add a Google Docs tool so the agent can fetch project updates (RAG).

First, reconfigure the Slack app OAuth scopes and tokens as required.

<Frame>
  <img alt="The image shows a workflow in n8n, featuring a sequence that includes a Slack trigger, an AI agent with OpenAI chat model and memory, and a message sending action." />
</Frame>

What to change in the Slack App

* In the Slack API app settings, add the necessary bot token scopes and user token scopes. Typical scopes include read/history scopes for channels and groups plus chat write permissions so the app can read messages and post replies. The exact scopes depend on whether you need to operate in public channels, private groups, DMs, or multi-person DMs.
* After updating scopes, reinstall the app so the new permissions take effect. Slack will prompt you to reinstall when you add new scopes.
* To post messages that appear to come from a real user, you’ll generally need a user OAuth token. If you only use a bot token, you may be limited in sender customization unless `chat:write.customize` (or equivalent) is available and granted.

Recommended Slack scopes (examples)

| Token type | Common scopes                                                  | Purpose                                                       |
| ---------- | -------------------------------------------------------------- | ------------------------------------------------------------- |
| Bot token  | `chat:write`, `channels:history`, `groups:history`             | Post messages as the bot and read channel history for context |
| User token | `chat:write`, `channels:history`, `im:history`, `mpim:history` | Post as a user and read user-visible message events           |
| Optional   | `chat:write.customize`                                         | Customize the sender appearance when using bot tokens         |

Note: exact scopes depend on which Slack surfaces (public channels, private groups, DMs) you need to read from or write to. Reinstall your app after adding any scopes.

Create an n8n Slack credential (user OAuth token)

* After reinstalling the Slack app with the new scopes, copy the user OAuth token.
* In n8n, create or edit the Slack credential for your Slack nodes.
* Select the Access Token type and paste the user OAuth token, then save.

> **lightbulb** If you need to debug which token type is required, test with a dedicated test user in a staging workspace. Using a separate test account reduces the risk of accidental impersonation or policy violations.

Enable event subscriptions in your Slack app

* In [Slack API → Event Subscriptions](https://api.slack.com/apis/connections/events-api), enable “Subscribe to Events on behalf of users.”
* Add the message events your workflow should receive. For broad coverage, add:
  * `message.channels`
  * `message.groups`
  * `message.im`
  * `message.mpim`

<Frame>
  <img alt="The image shows a Slack API settings page for event subscriptions, detailing options to subscribe to bot events and events on behalf of users, along with required scopes for specific events." />
</Frame>

Reconfigure the n8n workflow
Below are the key node changes and recommended settings.

1. Slack Trigger node
   * Set the trigger event to “Any Event” or explicitly include the message events listed above so direct messages and other message types are captured.
   * Turn on “Watch all workspaces” if you want the trigger to fire for multiple workspaces.
   * Add username(s) or user ID(s) you want to ignore so the workflow does not trigger on your own messages. To find your Slack user ID: open your profile → click the three dots → Copy member ID. Paste that ID into the ignore list (one per line).

2. Agent node (AI)
   * Add a System Message to set the agent’s persona and behavior (tone, role, constraints).
   * Choose your chat model (the UI example shows GPT-5). Attach a memory strategy if desired (e.g., Simple Memory) to preserve context across conversations.
   * Example system prompt used in this demo:
     * “You are Marconi, a team member at KodeKloud. Your job is to impersonate Marconi and respond to his team members’ messages on his behalf. Sound friendly and natural in a typical tech working environment.”

<Frame>
  <img alt="The image shows a screenshot of an AI Agent setup interface with parameters for executing a step. It includes a system message instructing the AI to impersonate a team member named Marconi and respond to team messages." />
</Frame>

3. Send Message node (Slack send)
   * Make the Channel ID dynamic so replies go back to the same channel that triggered the workflow. Common n8n expressions include:

```javascript theme={null}
// Common property when using Slack Events API:
{{ $node["Slack Trigger"].json["event"]["channel"] }}

// Or, for payloads where channel is at the top level:
{{ $node["Slack Trigger"].json["channel"] }}
```

* Under Options, enable “Send as User” (or the option named similarly in your Slack node) and ensure the node uses the user OAuth credential so the message is posted as that user.
* If you must use a bot token and want to customize the sender, include `chat:write.customize` or the appropriate scope in the app configuration.

Testing the workflow

* Save changes, then trigger the workflow by sending a message from a different Slack account (colleague or test user).
* Expected flow: incoming message → Slack Trigger fires → Agent generates a reply → Send Message node posts the reply in the originating channel/DM.

Example interactions (demo)

* Trigger: “Hey, Marconi”\
  Agent reply (example): “Hey, what’s up? Need an update on anything AWS/Azure? Or is there something that can help unblock?”
* Trigger: “How was your weekend?”\
  Agent reply (example): “Kept it low-key, got some rest, did a bit of planning over the week. I also sketched out a couple of tweaks for the AWS EKS and the Azure pipeline that I’ll share after the standup.”

These examples show how the agent adopts a persona and responds conversationally. Adjust the system prompt to better match the preferred voice, tone, and allowed topics.

Adding simple RAG (Google Docs tool)
To make the agent more useful for factual, up-to-date answers, attach a retrieval tool that fetches current project information before the agent replies.

* Create a Google Doc with the project updates you want the agent to reference.
* In n8n, add a Google Docs node configured to perform a “Get” operation and provide the document URL; the node will fetch document content.
* In the AI Agent node, add a short tool instruction to the System Prompt, for example:
  * “Use the Google Doc tool when asked about project updates.”
* Keep the Google Docs node attached as a tool the Agent can call at runtime — do not attempt to manually transform the document in the flow for this demo. The agent will invoke the tool when needed.

RAG run-time sequence

1. Trigger fires on the incoming Slack message.
2. The Agent decides it needs the Google Doc tool.
3. The Google Docs node retrieves the latest document content.
4. The Agent composes a response incorporating retrieved updates and persona instructions.
5. The Send Message node posts the reply to the same channel/DM.

Example (fictional) response sourced from the Google Doc:
“A quick Azure project update: objective, interactive lab design done, 65% complete, ETA 15th of October, 2025.”

Use cases and considerations

* Use cases: internal tech support, FAQ bots, HR summaries, legal Q\&A, marketing briefs, customer support — anywhere conversational, up-to-date answers based on internal documents are helpful.
* Tuning: refine the system prompt, tool descriptions, and memory to align tone, accuracy, and privacy rules.
* Security & privacy: limit which documents and channels the agent can access. Audit tokens and scopes regularly.

> **warning** Always follow your organization’s policies and Slack’s terms of service when enabling an agent to impersonate a user. Do not use this functionality to misrepresent, deceive, or violate privacy or compliance requirements. This demo is for learning purposes — we do not recommend replacing your job with an AI agent.

That’s it for this lesson — a practical walkthrough of enabling a Slack-connected AI agent in n8n that can reply as a user and enrich replies with external document content.

Links and references

* [Slack Events API documentation](https://api.slack.com/apis/connections/events-api)
* [Google Docs](https://docs.google.com)
* [n8n Documentation](https://docs.n8n.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/8e4f69ef-7aaa-4369-a483-6bc5065050c3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/19a9f59c-f7a9-4df0-8b4b-799ed875ab52)
