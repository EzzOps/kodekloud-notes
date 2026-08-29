# Slack Setup Intro

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Slack-Setup-Intro/page

Guide to creating and configuring a Slack app, connecting it to n8n, enabling app mention event subscriptions, and building an AI driven reply workflow

This guide walks through creating a Slack app, connecting it to n8n, and configuring the permissions and events needed for a simple mention-driven bot. If you already know how Slack apps and OAuth work, skip to the n8n sections — otherwise follow the steps in order to avoid common verification issues.

Prerequisites:

* Admin privileges in the target Slack workspace (required to install apps).
* A publicly reachable HTTPS endpoint for n8n (or a secure tunnel such as `ngrok`).
* An n8n instance running and accessible while you verify Slack Event Subscriptions.

1. Create the Slack App

* Sign in at the Slack API site: [https://api.slack.com](https://api.slack.com)
* Open Apps → Create New App.
* Name the app (example: n8nDemoBot) and select the development workspace, then click Create App.

<Frame>
  <img alt="This image shows the Slack API webpage, highlighting productivity features and options to get started or explore samples for building Slack apps." />
</Frame>

Choose your workspace and hit Create App.

<Frame>
  <img alt="The image shows a Slack API interface with a pop-up window for naming a new app and selecting a workspace for development. The background lists existing app names." />
</Frame>

2. Add Bot Token Scopes (OAuth & Permissions)
   Open the app configuration → OAuth & Permissions and add the bot token scopes the bot needs. Scopes define what the bot can read and do in the workspace.

| Bot token scope      | Purpose                                          |
| -------------------- | ------------------------------------------------ |
| `app_mentions:read`  | Receive events when the bot is mentioned         |
| `chat:write`         | Send messages as the app                         |
| `channels:read`      | Read public channel information                  |
| `groups:read`        | Read private channel/group information (if used) |
| `users.profile:read` | Read basic profile fields                        |
| `users:read`         | Read basic user information                      |

<Frame>
  <img alt="The image shows a Slack app's OAuth settings page, including bot token scopes with &#x22;app_mentions:read&#x22; to view direct mentions in conversations. There is an option to add a new OAuth scope." />
</Frame>

3. Install the App and copy the Bot Token

* Install the app into your workspace (you must be an admin or have install permissions).
* After installation, Slack issues a Bot User OAuth Token (starts with `xoxb-`). Copy it — you’ll use this token to create an n8n Slack credential.

<Frame>
  <img alt="The image shows the Slack API page focused on OAuth & Permissions, featuring options for token rotation and OAuth token generation, along with navigation links on the left side for various settings and features." />
</Frame>

<Callout icon="warning">
  Make sure you are an admin to install the app into the Slack workspace. Treat the Bot User OAuth Token as a secret — do not share it publicly.
</Callout>

4. Create a Slack credential in n8n (Slack Trigger)

* In n8n, add a Slack Trigger node (select the Trigger node type, not an Action).
* Use the Bot User OAuth Token you copied to create or paste a new Slack credential in n8n.
* Save and allow n8n to test the credential — a successful connection shows a green confirmation.

<Frame>
  <img alt="The image shows a configuration screen for setting up a Slack API connection in the n8n workflow automation tool, prompting the user for an access token." />
</Frame>

5. Enable Event Subscriptions and verify the Request URL
   Slack Event Subscriptions must point to an n8n webhook URL so Slack can POST events (like `app_mention`) to your workflow.

* In the Slack app, open Event Subscriptions → Enable Events.
* Copy the webhook Request URL from the Slack Trigger node in n8n. n8n typically provides a test (staging) URL and a production URL — use the test URL for development.

<Frame>
  <img alt="The image shows a Slack API page for setting up event subscriptions, with options to enable events and various settings and features listed on the left sidebar." />
</Frame>

<Callout icon="note">
  The Slack Request URL must be publicly reachable over HTTPS. If your n8n instance is running locally or behind a firewall, use a secure tunnel (for example, `ngrok` at [https://ngrok.com](https://ngrok.com)) or expose n8n with a valid TLS endpoint. Ensure n8n is running and reachable while completing the verification step.
</Callout>

* Paste the n8n webhook URL into Slack’s Request URL field and enable events.
* Slack will send a `url_verification` request (includes a `challenge` field) and expects your endpoint to echo the challenge. In n8n, click Execute Step on the Slack Trigger node so n8n can respond to Slack’s verification request.
* After executing the trigger, return to Slack and click Retry. Slack should verify the URL.

6. Subscribe to bot events

* On the same Event Subscriptions page, add the bot events you need. For mention-driven bots add the `app_mention` event.
* Save the changes.

7. Add the app to channels you want it to monitor

* In Slack, open the target channel → Channel details → Integrations (or Members) → Add apps and add your app (n8nDemoBot) to that channel.

8. Configure the Slack Trigger node to listen to a specific channel

* In the Slack Trigger node in n8n you can select the channel:
  * From the selection list
  * By channel ID (`C0998J1QP46`) copied from channel details
  * By URL
* After choosing the channel, click Execute Step on the Slack Trigger so it is actively listening for events.

<Frame>
  <img alt="The image shows a user interface for setting up a Slack Trigger in an automation tool, with options to configure webhook URLs and other parameters like triggering on bot/app mentions. The &#x22;Execute step&#x22; button is visible at the top right." />
</Frame>

9. Test by mentioning the bot

* In the configured Slack channel, mention the bot, for example: `@n8n-demo-bot hello`.
* When Slack delivers the `app_mention` event, the Slack Trigger node will receive a payload that contains useful fields.

Common event fields you will receive:

| Field           | Description                           | Example             |
| --------------- | ------------------------------------- | ------------------- |
| `event.type`    | Event type                            | `app_mention`       |
| `event.user`    | ID of the user who mentioned the bot  | `U12345678`         |
| `event.text`    | Message text                          | `hello`             |
| `event.channel` | Channel ID where the mention occurred | `C0998J1QP46`       |
| `event.ts`      | Event timestamp                       | `1622631234.000200` |

A simplified example payload (trimmed for clarity):

```json theme={null}
{
  "event": {
    "type": "app_mention",
    "user": "U12345678",
    "text": "hello",
    "channel": "C0998J1QP46",
    "ts": "1622631234.000200"
  }
}
```

<Frame>
  <img alt="The image shows a configuration interface for a Slack trigger within a workflow application, displaying webhook URLs and settings for connecting with a Slack workspace. There is also an output log detailing an app mention event with user and message information." />
</Frame>

10. Build the reply workflow in n8n

* Connect follow-up nodes after the Slack Trigger to process the message.

* Example flow:
  1. Slack Trigger (receives `app_mention`)
  2. AI Agent node (generates a reply using the Slack message text as input)
  3. Slack node (sends the AI-generated message back to the channel)

* Configure the AI Agent node:
  * Map the Slack `event.text` to the agent input.
  * Choose a chat model (e.g., GPT-4o Mini or other supported model).
  * Optionally enable memory for conversational context. Using the Slack channel ID as the session or conversation ID keeps context scoped per-channel.

* Configure the Slack node to post the reply:
  * Use the Slack credential you created.
  * Set Resource → Message, Operation → Send.
  * Provide the channel ID (or pick from the list) for the destination.
  * Map the agent’s response to the Message Text field.
  * Optionally toggle off “Include link to n8n workflow” to prevent Slack from appending the “Posted by n8n workflow” note.

To inspect or test the agent output during development, execute the upstream nodes and then Execute Step on the Slack node to post the mapped text.

<Frame>
  <img alt="The image shows a workflow interface for n8n, with a Slack integration setup. It displays parameters for sending a message to a Slack channel and the successful execution of a node." />
</Frame>

Result

* After execution, your bot should reply in the channel, for example: “Hello, how can I assist you today?”
* This completes the basic end-to-end setup: Slack app with correct scopes, Event Subscriptions verified to the n8n webhook, a Slack Trigger that receives `app_mention` events, an AI agent that generates a reply, and a Slack node that posts back to the channel.

Advanced notes and next steps

* You can expand permissions or add richer message composition (blocks, attachments) in the Slack message node.
* Attach external tools or actions to the AI agent for tool-enabled workflows.
* Consider token rotation and secure storage of credentials for production.
* Review Slack rate limits and backoff strategies if your bot will be highly active.

<Frame>
  <img alt="The image shows a workflow in n8n involving a Slack trigger, an AI agent, and Slack post message, integrated with an OpenAI chat model and a memory tool." />
</Frame>

Links and references

* Slack API: [https://api.slack.com](https://api.slack.com)
* n8n: [https://n8n.io](https://n8n.io)
* ngrok: [https://ngrok.com](https://ngrok.com)
* OpenAI (models & docs): [https://openai.com](https://openai.com)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/3344ec6a-9398-48d6-b9a3-3b3e0009ef38" />
</CardGroup>
