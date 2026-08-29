# Using Language Specific SDKs

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-Apps-with-Azure-OpenAI-Service/Using-Language-Specific-SDKs/page

Explains using language-specific Azure OpenAI SDKs, shows a Python Flask integration, environment variable security, and tuning parameters for chat-based model deployments.

Using language-specific SDKs accelerates development by exposing idiomatic APIs and hiding low-level REST details. SDKs for Azure OpenAI provide consistent patterns across languages (for example, .NET and Python), making it easy to initialize clients, prepare requests, and handle responses while controlling model behavior with parameters like temperature and max\_tokens.

In this lesson we'll cover what makes SDKs developer-friendly and walk through a concise, corrected Python example that integrates Azure OpenAI into a simple Flask chatbot.

Why SDKs help

* Familiar languages: Use the SDK for the language you already know (Python, .NET, etc.).
* Predictable structure: The typical pattern is initialize client → build messages/params → call API → process response.
* Fine-grained control: Tune generation with parameters such as max\_tokens, temperature, and top\_p.
* Sync and async options: Choose synchronous or asynchronous clients depending on your app architecture.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Using Azure OpenAI SDK&#x22; with four numbered panels describing features: Available SDKs, Consistent Structure, Key Parameters, and Synchronous and Asynchronous APIs. It highlights support for multiple languages (e.g., .NET, Python), controls like max tokens/temperature, and sync/async API options." />
</Frame>

Quick SDK workflow

1. Import the SDK package for your language.
2. Initialize a client with your endpoint and credentials.
3. Build chat messages and set generation parameters (system prompt, user messages, temperature, max\_tokens, etc.).
4. Send the request (sync or async).
5. Process the response and integrate it into your application.

> **warning** Never hardcode secrets (API keys or endpoints) in source code. Use environment variables or a secure secrets manager.

> **lightbulb** Store your Azure endpoint and API key in environment variables or a secure secrets store. Never commit keys to source control.

Environment variables (recommended)

| Variable                  | Purpose                             | Example                                        |
| ------------------------- | ----------------------------------- | ---------------------------------------------- |
| AZURE\_OPENAI\_KEY        | Your Azure OpenAI API key           | `set AZURE_OPENAI_KEY="..."`                   |
| AZURE\_OPENAI\_ENDPOINT   | Your Azure OpenAI resource endpoint | `https://my-openai-resource.openai.azure.com/` |
| AZURE\_OPENAI\_DEPLOYMENT | Deployment name for the model       | `gpt-4o`                                       |

Python + Flask example (synchronous SDK)
Below is a compact single-file Flask app that demonstrates a typical synchronous integration using the azure.ai.openai package. It reads credentials from environment variables, initializes the OpenAIClient with AzureKeyCredential, forwards user input to a deployed model, and returns the assistant reply as JSON.

```python theme={null}
