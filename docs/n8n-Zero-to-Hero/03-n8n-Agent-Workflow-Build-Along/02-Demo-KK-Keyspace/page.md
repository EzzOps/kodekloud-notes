# Demo KK Keyspace

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-Agent-Workflow-Build-Along/Demo-KK-Keyspace/page

Guide showing how to connect n8n workflows to KodeKloud KK Keyspace and call LLMs using the OpenAI Message a Model node or HTTP Request cURL import.

In this lesson you'll get hands-on with calling large language models (LLMs) from n8n using KodeKloud's KK Keyspace — an all-in-one AI playground that lets you create API keys for multiple models (for example GPT-4o, GPT-4.1, Claude Sonnet 4, Gemini 2.5, and Grok 3). KK Keyspace is accessible on different subscription tiers; the AI and Business plans provide the most extensive model access.

<Frame>
  <img alt="The image shows a subscription plan comparison table from KodeKloud, detailing features and differences between the &#x22;Free, Standard and Pro Plan&#x22; and the &#x22;AI Plan,&#x22; including credits, token limits, and support features." />
</Frame>

To open the playground visit `https://kodekloud.com/ai-playground/kk-keyspace`. Once you have the correct subscription and access, click **Launch Now → Start Playground** to reach the dashboard where you can create API keys, pick available models, and view example requests.

This article demonstrates two practical ways to call a GPT-4.1 model through KK Keyspace from an n8n workflow:

1. Use n8n’s built-in OpenAI "Message a Model" node with a custom KK Keyspace credential.
2. Use n8n’s HTTP Request node by importing a cURL example from the KK Keyspace docs.

***

## Method 1 — OpenAI "Message a Model" node (with a KK Keyspace credential)

Steps:

1. Add a trigger node (for example, a Chat Trigger). Example payload for a chat trigger:

```json theme={null}
{
  "sessionId": "4299aa7d109f4f83a5ef646ae7a779fcd",
  "action": "sendMessage",
  "chatinput": "hello"
}
```

2. Add the OpenAI "Message a Model" node to the workflow.
3. Create a new credential (for example, `KK Keyspace Demo`) and configure:
   * Base URL: paste the KK Keyspace base URL shown in your KK Keyspace dashboard.
   * API Key: paste the API key you created in the KK Keyspace dashboard.
   * Save the credential.

> **lightbulb** If a red compatibility warning appears in the n8n UI after entering a custom base URL, it is usually a harmless UI incompatibility caused by supplying a non-default base URL. You can still use the credential and execute the node.

4. In the "Message a Model" node:
   * Set **Model selection** to "By ID".
   * Enter the model ID manually (KK Keyspace model IDs may not appear in the built-in provider list). For GPT-4.1 use:

```text theme={null}
openai/gpt-4.1
```

* Map the trigger's chat input variable into the node message field so the user's prompt is sent to the model.

5. Execute the node to see the response in the node output, for example:

> "Hello! How can I help you today?"

<Frame>
  <img alt="The image shows a software interface for configuring a workflow in a platform called n8n, with parameters set for messaging a model using OpenAI’s API. The input is &#x22;hello,&#x22; and the output message is &#x22;Hello! How can I help you today?&#x22;" />
</Frame>

You can continue the conversation by sending additional messages through the trigger and mapping them to the "Message a Model" node. This method is straightforward when you want to use n8n’s OpenAI abstractions while pointing them at a custom (KK Keyspace) endpoint.

***

## Method 2 — HTTP Request node (import a cURL from KK Keyspace docs)

Use this approach when you prefer direct HTTP calls or need request options that the built-in node doesn’t expose.

1. Add a Manual Trigger (Trigger Manually) and attach an HTTP Request node.
2. In the KK Keyspace documentation, switch the example request to **cURL** and copy the example cURL command.
3. In the n8n HTTP Request node, click **Import cURL** and paste the cURL — n8n will populate the method, URL, headers, and body fields automatically.

<Frame>
  <img alt="The image shows an interface for creating a workflow in n8n, featuring nodes for receiving chat messages and sending messages to a model. The workflow appears to be part of a demo project named &#x22;KodeKey Demo&#x22;." />
</Frame>

4. Review and refine the imported configuration. You can move the `Authorization` header into the dedicated Authentication fields or keep it under Headers; n8n often places Authorization and Content-Type in the Headers section on import.

<Frame>
  <img alt="The image shows a HTTP Request configuration screen in a workflow application, where a POST method is set with a specific URL and header parameters for authorization." />
</Frame>

5. Execute the HTTP Request. A typical JSON body for a chat completion looks like:

```json theme={null}
{
  "model": "openai/gpt-4.1",
  "messages": [
    {
      "role": "user",
      "content": "In a single sentence, why should someone choose KodeKloud over other platforms to learn DevOps?"
    }
  ]
}
```

The response JSON will contain the model completion. Example output:

> "Someone should choose KodeKloud because it offers highly interactive, hands-on labs and real-world scenario-based exercises that accelerate practical skills development beyond traditional video-based courses."

Example cURL (redacted API key)

```bash theme={null}
curl https://kodekey.ai.kodekloud.com/v1/chat/completions \
  -H "Authorization: Bearer Sk-kkAI-REDACTED" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-4.1","messages":[{"role":"user","content":"In a single sentence, why should someone choose KodeKloud over other platforms to learn DevOps?"}]}'
```

> **warning** Never commit or expose your API keys publicly (for example in Git repositories or logs). Redact or inject secrets via n8n credentials and environment variables.

***

## Method comparison

| Method                                            | Best for                                                            | Pros                                                                               | Cons                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| OpenAI "Message a Model" node (custom credential) | Quick integration when using n8n abstractions                       | Simple configuration, uses n8n node features, easier mapping of conversation state | May require manual model ID entry for non-default endpoints    |
| HTTP Request node (Import cURL)                   | Full control over request shape or using provider-specific features | Exact parity with provider examples, easily customize headers/body                 | Requires handling authentication and response parsing manually |

***

## Summary

* KK Keyspace provides a quick path to obtain API keys and access multiple LLMs without immediately using each model provider’s billing account.
* In n8n you can:
  * Use the OpenAI "Message a Model" node with a custom KK Keyspace credential (set Base URL and API Key).
  * Or import a cURL from KK Keyspace docs into an HTTP Request node to run direct API calls.
* Both methods let you route chat input from triggers into a model and use the model responses in your workflows.

## Links and references

* KK Keyspace (AI Playground): `https://kodekloud.com/ai-playground/kk-keyspace`
* OpenAI Platform: [https://platform.openai.com/](https://platform.openai.com/)
* Anthropic: [https://www.anthropic.com/](https://www.anthropic.com/)
* n8n Documentation: [https://docs.n8n.io/](https://docs.n8n.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/6045516d-9973-433b-8ce3-99f78a1b3c15/lesson/a9be43ae-7cec-4921-a2fd-b76ca1652c11)
