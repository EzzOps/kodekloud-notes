# Retries and Error Handling

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Additional-Info/Retries-and-Error-Handling/page

Guide to implementing error handling and retries for n8n AI workflows using Error Trigger, logging errors to Google Sheets, notifying maintainers, and using retries and fallback models for resilience.

In this guide we'll cover pragmatic error handling and retry strategies for AI-driven workflows built in n8n. The example workflow is a Telegram-triggered AI email agent that:

* fetches recent news (via Perplexity),
* composes an email using an Anthropic chat model,
* sends the email, and
* appends a record to Google Sheets.

This tutorial shows how to centralize production failures with an Error Trigger workflow, persist error details for auditability, notify maintainers, and improve resilience with retries and fallback models.

<Frame>
  <img alt="The image shows a workflow diagram in n8n, with a Telegram trigger connected to an AI agent, which further branches out to append a row in a sheet and send a message in Gmail." />
</Frame>

Overview

* Use an Error Trigger workflow to capture failures from production executions.
* Persist error payloads to a Google Sheet (or a database) for auditing.
* Notify the team (Slack, email, PagerDuty) so maintainers can respond quickly.
* Add node-level retries and a fallback LLM to handle transient or provider-specific outages.

Benefits:

* Faster detection and triage of failures
* Reduced manual monitoring overhead
* Resilient AI agents that can failover automatically

Setting up the Error Workflow

1. Create a new workflow (for example, “Error Logger Demo”).
2. Add an Error Trigger node. The Error Trigger captures payload information about failures from other workflows that are running in production.

<Frame>
  <img alt="The image shows an interface for an &#x22;Error Trigger&#x22; node with sections for parameters and settings. It includes a message about triggering when there's an error in another workflow and options related to data execution." />
</Frame>

3. Link this Error Trigger to your original workflow:
   * Open the original workflow’s Settings (three dots in the top-right).
   * Under Error Workflow, choose the workflow you created (e.g., `Error Logger Demo`) and save.

<Frame>
  <img alt="The image shows a workflow settings panel for a Telegram Email News Agent, including options for execution order, error workflow, timezone, and saving execution details. It also includes various toggle and dropdown options for configuring the workflow settings." />
</Frame>

<Callout icon="lightbulb">
  The Error Trigger only captures failures from production executions. Manual runs won’t fire the error workflow — toggle the original workflow to production to test real error forwarding.
</Callout>

Observing an Error Payload

When the original workflow is running in production and a node fails, the Error Trigger workflow receives a payload describing the failed execution. The payload includes useful fields such as:

* failing node name (and sub-node, if applicable)
* error message and stack
* workflow id and URL
* execution timestamp

You can inspect the payload in the Error Logger Demo Executions to identify the exact failing node and the reason for failure.

<Frame>
  <img alt="The image shows a software interface with an &#x22;Error Trigger&#x22; highlighted. It includes information about an error in a sub-node called &#x22;Simple Memory&#x22; within the workflow." />
</Frame>

Common example: a Simple Memory node may fail if it expects a JSON session ID from a Chat Trigger but the workflow was switched to a Telegram trigger, so the session field is missing.

<Frame>
  <img alt="The image shows a user interface with a Telegram trigger and an AI agent setup. There is an error message indicating an issue in the sub-node 'Simple Memory' with no session ID found." />
</Frame>

Persisting Errors to Google Sheets

To keep an audit trail, add a Google Sheets node to your Error Logger Demo workflow and configure it to Append Row. Map fields from the Error Trigger payload to your sheet columns so you have an easily searchable log.

Example column mapping:

| Column        | Example Expression / Source                       |
| ------------- | ------------------------------------------------- |
| Timestamp     | `{{$now}}`                                        |
| Workflow      | `{{$json["workflowId"]}}`                         |
| URL           | workflow URL field from the Error Trigger payload |
| Node          | name of the failing node (e.g., `Simple Memory`)  |
| Error Message | the error string from the payload                 |

Note: Wrap field expressions like `{{$now}}` or `{{$json["workflowId"]}}` in backticks when placing them in documentation or table cells to avoid MDX parsing issues.

Map these values in the Google Sheets node, then run the step to confirm the row is appended.

<Frame>
  <img alt="The image displays an interface for appending rows in a workflow sheet, showing parameters and settings for mapping column modes and input details on the left, with an error message related to &#x22;Simple Memory.&#x22;" />
</Frame>

After execution, the sheet will contain a new row with the error details for easy reference.

<Frame>
  <img alt="The image shows a Google Sheets document titled &#x22;Demo Error Log&#x22; with columns for Timestamp, Workflow, URL, Node, and Error Message, containing one entry about an error in &#x22;Simple Memory.&#x22;" />
</Frame>

Notifying Maintainers

Persisting the error is useful, but push notifications help maintainers act quickly. Add a notification node (Slack, Gmail, PagerDuty, etc.) after the Sheets append node and include the workflow URL and error message.

Example Slack message template (place this in the Slack node’s message field):

```text theme={null}
Error Occurred in Workflow: {{$json["URL"]}}
Error Message: {{$json["Error Message"]}}
```

Select the appropriate channel and bot, then execute to verify delivery. Slack is one easy option—use whatever service your team prefers.

Retries and Fallback Models

Many production failures are transient: network hiccups, temporary API rate limits, or brief provider outages. Implement the following to increase reliability:

* Node-level retries:
  * On critical nodes (AI Agent, HTTP Request, etc.), enable "Retry on Fail" in the node settings.
  * Recommended starting point: Number of Tries = 3 with a small delay between attempts.
* Fallback LLMs:
  * Configure a fallback model in your AI Agent node (e.g., if Anthropic fails, try OpenAI).
  * This ensures the agent can continue serving requests when a primary provider is down or out of quota.

Recommended retry strategy (example):

|                     Scenario | Node setting                            |
| ---------------------------: | --------------------------------------- |
| Transient network/API errors | Retries = 3, Delay = 5s                 |
|        Rate-limited provider | Retries = 5, Exponential backoff        |
|      Long-running operations | Retries = 2, Delay = longer (e.g., 30s) |

Putting It All Together

* Centralize production failures with an Error Trigger workflow.
* Persist key fields (timestamp, workflow, URL, node, error) to a sheet or database for audit and analysis.
* Send notifications to on-call or maintainers with actionable information (workflow URL + error).
* Harden critical nodes with retries and configure fallback LLMs to reduce downtime.

These steps help you detect, triage, and automatically mitigate many production issues in AI-driven workflows.

Further reading and references

* [n8n Error Trigger documentation](https://docs.n8n.io/nodes/nodes-library/nodes/ErrorTrigger/)
* [n8n Workflows - Settings](https://docs.n8n.io/getting-started/workflows/#workflow-settings)
* [Google Sheets API / n8n Google Sheets node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/)
* [Slack API / n8n Slack node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.slack/)

<Callout icon="warning">
  Avoid logging sensitive PII or secrets in plain text to shared sheets or public channels. Mask or redact sensitive fields before persisting or notifying.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/ec8c9063-8504-4153-b9d6-b95d35c600c9/lesson/22c4a7c3-4c82-4e39-978c-2ec0449a791d" />
</CardGroup>
