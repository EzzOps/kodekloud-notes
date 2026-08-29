# .env (Development)
OPENAI_API_KEY=anyrandomtext
LLM_ENDPOINT="http://localhost:11434/v1"
MODEL=llama3:2:1b
```

> **lightbulb** Ollama does **not** validate `OPENAI_API_KEY` locally. Feel free to use a placeholder value while testing.

Then initialize your OpenAI client in code as usual:

```javascript theme={null}
import OpenAI from "openai";
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.LLM_ENDPOINT,
});
```

## 2. Production Environment Setup

When you’re ready to go live, sign in to the [OpenAI dashboard](https://platform.openai.com/account/api-keys) to create an API key. Update your `.env` as follows:

```bash theme={null}
# .env (Production)
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX
LLM_ENDPOINT="https://api.openai.com/v1"
MODEL=gpt-3.5-turbo
```

> **triangle-alert** Keep your real `OPENAI_API_KEY` secure. Never commit it to source control or expose it in client-side code.

### Configuration Comparison

| Environment | OPENAI\_API\_KEY    | LLM\_ENDPOINT               | MODEL           |
| ----------- | ------------------- | --------------------------- | --------------- |
| Development | `anyrandomtext`     | `http://localhost:11434/v1` | `llama3:2:1b`   |
| Production  | Your OpenAI API key | `https://api.openai.com/v1` | `gpt-3.5-turbo` |

No changes to your application code are required—just swapping environment variables.

## 3. Next Steps

1. Generate or rotate your OpenAI API keys via the [OpenAI dashboard](https://platform.openai.com/account/api-keys).
2. Deploy your application, ensuring the production `.env` is configured.

![The image outlines two next steps: generating API keys in OpenAI and using these keys with an application.](https://kodekloud.com/kk-media/image/upload/v1752883671/notes-assets/images/Running-Local-LLMs-With-Ollama-OpenAI-Compatibility-for-Ollama/openai-api-keys-application-steps.jpg)

## References

* [Ollama Documentation](https://ollama.com/docs)
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/79e199ae-16bb-46eb-9d10-c3e8cb75991c)


# Section Introduction

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Section-Introduction/page

This article focuses on using the Ollama REST API for programmatic access to local LLMs over HTTP.

In the previous article, you explored Ollama’s core features—installing the CLI, pulling models, and running large language models locally. Now, we’ll shift our focus to programmatic access: the **Ollama REST API**, which lets you interact with your local LLMs over HTTP instead of typing commands in a terminal.

> **lightbulb** * Ensure you’ve installed the Ollama CLI and configured at least one local model (for example, `ollama pull llama2`).
  * Have your API base URL and authentication token ready if you’ve set up access controls.

## What You’ll Learn

* **Ollama REST API Overview**: Why and when to use the API over the CLI
* **Key Endpoints**: Create, list, and chat operations you’ll rely on
* **Request & Response Flow**: Emulate a conversational experience via HTTP
* **Hands-On Lab**: Practice making real API calls
* **AI App Architecture**: Fundamentals of integrating locally hosted LLMs
* **Python Demo**: Build a simple application with the [OpenAI Python client][1] powered by Ollama
* **OpenAI Compatibility**: How Ollama mirrors the [OpenAI API][2] for seamless production switch-overs

![The image is a slide outlining topics to be covered about the Ollama REST API, including its introduction, available endpoints, and interaction methods.](https://kodekloud.com/kk-media/image/upload/v1752883672/notes-assets/images/Running-Local-LLMs-With-Ollama-Section-Introduction/ollama-rest-api-topics-slide.jpg)

This section will guide you through every step, from sending your first `POST /v1/chat/completions` request to handling streamed responses in your application.

![The image is a slide titled "What We'll Cover," outlining topics related to building AI applications using Ollama, creating an app with the OpenAI Python client, and OpenAI compatibility.](https://kodekloud.com/kk-media/image/upload/v1752883673/notes-assets/images/Running-Local-LLMs-With-Ollama-Section-Introduction/ai-applications-ollama-openai.jpg)

Let’s dive in and start building!

***

## References

[1]: https://github.com/openai/openai-python

[2]: https://platform.openai.com/docs/api-reference

- [Watch Video](https://learn.kodekloud.com/user/courses/running-local-llms-with-ollama/module/8df2f2d5-d3c5-433d-b5f5-f553b040b2e7/lesson/095c0b79-d309-4fc4-a278-6d071d5dc1d5)
