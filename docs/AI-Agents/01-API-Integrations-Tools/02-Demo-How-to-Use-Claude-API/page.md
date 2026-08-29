# python
import os
import requests

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "my_api_key")
URL = "https://api.anthropic.com/v1/messages"

payload = {
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, Claude"}
    ]
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

resp = requests.post(URL, json=payload, headers=headers)
resp.raise_for_status()
print(resp.json())
```

Message roles and structuring

Claude uses role-attributed messages that help maintain consistent behavior across a conversation. Use role separation to improve predictability and control.

| Role        | Purpose                                               | Example                                                              |
| ----------- | ----------------------------------------------------- | -------------------------------------------------------------------- |
| `system`    | Sets persona, global constraints, and output format   | `You are an expert research assistant. Be concise and cite sources.` |
| `user`      | End-user inputs, questions, or task prompts           | `Summarize this report and extract key metrics.`                     |
| `assistant` | Model-generated output (sent by the API in responses) | Generated content from the model                                     |

<Callout icon="lightbulb">
  Use a system message to define persona, constraints, and output format. This improves reliability, especially in agent pipelines.
</Callout>

Tool use and function calling

Claude supports structured function calling (tool use). Define tools with explicit parameter schemas so the model can safely decide when to call them. Typical tools include external APIs, database queries, calculators, or custom utilities. Use tight JSON schemas to reduce ambiguity and simplify downstream execution and verification.

Code, files, and Claude Code features

Claude Code extends Claude’s abilities for code reasoning and file interactions. You can upload files (PDF, CSV, code files) and reference them by ID in messages. Claude can parse, summarize, extract structured data, or run code analysis on uploaded artifacts.

Use cases:

* Extract tabular data from financial PDFs
* Perform QA across long documents
* Review source code and suggest fixes
  Files are handled as persistent objects, allowing agents to operate over them repeatedly without re-uploading.

<Frame>
  <img alt="The image illustrates &#x22;Claude Code + File Interactions,&#x22; highlighting its applications as a research assisting agent for converting financial PDFs into tabular data, and as a DevOps agent for analyzing logs for debugging." />
</Frame>

Model variants: Opus, Sonnet, Haiku

Choose a Claude model based on capability, context window size, latency, and cost trade-offs:

| Model  | Best for                                   | Notes                                                                             |
| ------ | ------------------------------------------ | --------------------------------------------------------------------------------- |
| Opus   | Highest capability and very large contexts | Suitable for massive documents and complex reasoning (very large context windows) |
| Sonnet | Balanced capability and cost               | Good general-purpose option for many agent tasks                                  |
| Haiku  | Low-latency, cost-efficient                | Optimized for short chats and high-throughput scenarios                           |

All models typically support streaming responses and batching. Select the model based on your workload, latency budget, and cost constraints.

<Frame>
  <img alt="The image is a comparison of three AI models—Opus, Sonnet, and Haiku—highlighting their key features and use cases, with Opus being the most powerful, Sonnet being cost-effective, and Haiku being the fastest. It also mentions support for streaming and batching, with varying pricing." />
</Frame>

Pricing and limits

Pricing and rate limits vary by model and account tier. Monitor token usage, request rates, and latency, particularly with large-context models like Opus. Use caching, summarization of long histories, and context window management to control costs and maintain performance.

Best practices for agent architectures

* Use a strong system message to define persona, format, and constraints.
* Keep roles separated (system vs user) to reduce prompt drift.
* Define tools with strict parameter schemas and validation.
* Prefer streaming and batching to reduce perceived latency in real-time apps.
* Implement caching and summarization to manage long-term context without exceeding token limits.
* Monitor token usage and latency; choose models according to workload needs.

<Frame>
  <img alt="The image outlines best practices for using the Claude API, including role separation, using system prompts, defining tool usage for agent workflows, and utilizing Claude Code and Files for structured tasks." />
</Frame>

How Claude compares to other LLM APIs

Claude differs from other providers (for example [OpenAI GPT-4](https://openai.com/product/gpt-4) and [Google Gemini](https://blog.google/technology/ai/introducing-gemini/)) in several important ways:

* Constitutional AI: Claude emphasizes internal critique and rule-guided behavior, which supports safer outputs compared with purely RLHF approaches.
* Native tool and file support: Claude provides built-in file handling and structured function calling, reducing the need for separate plugin layers.
* Message-first interface: The messages-based design maps naturally to agent architectures and long multi-turn workflows.

<Frame>
  <img alt="The image is a comparison table of features for three LLM APIs: Claude, OpenAI GPT-4, and Google Gemini, highlighting aspects like instruction tuning, tool use support, file handling, and alignment approach." />
</Frame>

While other providers may excel at ecosystem integrations or cloud-native services, Claude is particularly well-suited for safety-sensitive, agent-driven deployments that require robust alignment, long-context handling, and integrated tool/file interaction.

Links and references

* Anthropic: [https://www.anthropic.com](https://www.anthropic.com)
* Claude Shannon (background): [https://en.wikipedia.org/wiki/Claude\_Shannon](https://en.wikipedia.org/wiki/Claude_Shannon)
* Constitutional AI (Anthropic blog): [https://www.anthropic.com/blog/constitutional-ai](https://www.anthropic.com/blog/constitutional-ai)
* OpenAI GPT-4: [https://openai.com/product/gpt-4](https://openai.com/product/gpt-4)
* Google Gemini announcement: [https://blog.google/technology/ai/introducing-gemini/](https://blog.google/technology/ai/introducing-gemini/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/d2a91525-d4e7-4c2a-866a-e7a9d34b538c/lesson/8e8f54c6-489f-4bda-891e-039df69accff" />
</CardGroup>


# Demo How to Use Claude API

Source: https://notes.kodekloud.com/docs/AI-Agents/API-Integrations-Tools/Demo-How-to-Use-Claude-API/page

Tutorial for building a minimal Claude chat agent in Jupyter using the Anthropic Python SDK with installation, API key setup, code example, and troubleshooting tips.

Welcome back! In this lesson you'll learn how to create a minimal Claude-based chat agent in a Jupyter notebook using the official Anthropic Python package. Claude is a capable assistant for text and code tasks — it produces natural writing, has strong coding abilities, supports artifacts for visualization, and offers thoughtful analysis. That makes it a good fit for developers, writers, and analysts building interactive demos, research tools, or content assistants.

Before you begin, review the official docs at [docs.anthropic.com](https://docs.anthropic.com) to see available models, capabilities, and up-to-date API patterns and examples. The documentation lists models such as Claude Opus and Claude Sonnet and provides versioned guidance for SDK usage.

<Frame>
  <img alt="The image shows a webpage from Anthropic's developer guide, detailing different AI models like Claude Opus 4 and Claude Sonnet 4, along with their features. It also includes a table listing model names and APIs." />
</Frame>

Get started by opening a new notebook (for example, name it "ClaudeDemo") and follow the steps below.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface with an empty code cell and a &#x22;ClaudeDemo&#x22; file open." />
</Frame>

## Prerequisites

* Python 3.8+ (or a supported version for your `anthropic` SDK)
* A Claude API key from Anthropic
* Basic familiarity with Jupyter notebooks

## Installation

Install the official Anthropic package from PyPI:

```bash theme={null}
!pip install anthropic
```

## Setting the API Key

Store your Claude API key securely — the recommended approach is an environment variable such as `CLAUDE_API_KEY`. For quick demos you can use a placeholder or local config, but never commit real keys.

<Callout icon="lightbulb">
  Never commit API keys or other secrets to public repositories. Use environment variables, a secrets manager, or platform-provided secret stores in production.
</Callout>

<Callout icon="warning">
  Be aware of usage limits and billing. Running long conversations or repeated calls can incur cost—monitor your Anthropic account and set safeguards where appropriate.
</Callout>

## Minimal Claude Chat Agent (single Python cell)

The example below demonstrates a compact pattern for a Jupyter cell that:

* Initializes the Anthropic client,
* Sends a system-level prompt to define the assistant behavior,
* Maintains short-term message history,
* Runs an interactive loop for chatting.

Copy the whole block into a single notebook cell and run it.

```python theme={null}
