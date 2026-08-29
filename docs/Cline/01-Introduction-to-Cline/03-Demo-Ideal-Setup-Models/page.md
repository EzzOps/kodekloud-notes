# hello.py
print("Hello, world!")
```

Because the model runs on your machine, no external API calls are involved.

Why run models locally?

* Experiment with custom checkpoints from [Hugging Face](https://huggingface.co/) or other model repos.
* Reduce development costs by avoiding paid hosted APIs while prototyping.
* Keep source code and prompts on-premises for privacy and compliance.

> **lightbulb** Running LLMs locally is a good option when organizational policies restrict sending code or data to hosted providers (like OpenAI or Anthropic). It also gives you full control over model versions and runtime settings.

## Ollama — another local runtime option

[Ollama](https://ollama.com/) is a popular local LLM runtime that exposes a server you can point Cline to. When you choose Ollama as the provider in Cline’s API settings, the UI will list models available in your local Ollama installation. Model behavior varies, so try a few models to find the best fit for Cline’s edit-and-suggest workflows.

Below is an example showing a model selected in Cline (e.g., `llama3.2:1b`) and using it to apply an edit to an existing file.

<Frame>
  <img alt="A dark-themed app screenshot showing a left sidebar with recent chat history and a settings pane. The settings show API configuration for &#x22;Ollama&#x22; with the model set to &#x22;llama3.2:1b&#x22; and other fields like base URL and request timeout." />
</Frame>

Example workflow with Ollama:

1. Switch Cline’s API provider to Ollama and choose a model (for example, `llama3.2:1b`).
2. Open `hello.py` in the editor or add it to the model context.
3. Issue an edit request, for example:

User request:

```text theme={null}
Change "Hello, world!" to "Hello, Jeremy"
```

Cline shows a diff-style suggestion:

```diff theme={null}
1- print("Hello, world!")
1+ print("Hello, Jeremy!")
```

After accepting and saving the suggestion, the file becomes:

```python theme={null}
# hello.py
print("Hello, Jeremy!")
```

Because the Ollama server runs locally, no outbound API cost is incurred.

Quick comparison: LM Studio vs Ollama

| Feature       | LM Studio                                 | Ollama                                              |
| ------------- | ----------------------------------------- | --------------------------------------------------- |
| Access method | GUI with built-in HTTP API                | CLI/runtime with HTTP API                           |
| Best for      | Visual model management, GPU settings     | Lightweight local serving, model management via CLI |
| Pros          | Easy model load/UI, model details visible | Quick to deploy, integrates with local tooling      |
| Cons          | GUI overhead, may require more resources  | Model compatibility varies, fewer GUI controls      |

Notes and troubleshooting

* Model output format: Some local models return slightly different response formats; if Cline’s change suggestions look incorrect, try another model or refine the prompt.
* Resource limits: Larger models require adequate GPU/CPU and memory. Monitor LM Studio/Ollama logs and system resources.
* Logs: Run Cline in developer mode to inspect request and response logs for debugging.
* Model compatibility: If edits are inconsistent, test different models (or smaller/larger variants) to find one that produces coherent edit suggestions.

Common issues and fixes

| Problem                     | Likely cause                                 | Fix                                                                          |
| --------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------- |
| Cline shows no models       | Incorrect base URL or service not running    | Verify LM Studio/Ollama server is running and use the correct base URL       |
| Timeouts or slow responses  | Model size or insufficient hardware          | Increase timeout in Cline settings, use a smaller model, or upgrade hardware |
| Incorrect suggestion format | Model response doesn't match expected schema | Try a different model or add clearer instructions in the prompt              |

> **warning** Running large models locally can consume significant GPU/CPU and memory. Ensure your machine meets the recommended requirements for the model you plan to run, and monitor logs and system resources to avoid crashes.

## Summary

Connecting Cline to local LLMs (LM Studio, Ollama, etc.) gives you the flexibility to:

* Experiment with custom or community models,
* Reduce or eliminate API costs during development,
* Keep sensitive code and data within your environment.

Set the API provider in Cline, point to the local base URL, choose a model, and invoke the model to create or edit files as you would with a hosted service — the main difference is that everything runs on your machine.

Links and references

* LM Studio — [https://lmstudio.ai/](https://lmstudio.ai/)
* Ollama — [https://ollama.com/](https://ollama.com/)
* Hugging Face model hub — [https://huggingface.co/](https://huggingface.co/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/07505364-dfb1-4691-8f55-ce69bc5e81ec/lesson/3ef49038-5539-4626-83ee-e7bec38b2d48)


# Demo Ideal Setup Models

Source: https://notes.kodekloud.com/docs/Cline/Introduction-to-Cline/Demo-Ideal-Setup-Models/page

Guide to selecting and comparing LLMs in an app, reading model cards, comparing token limits and pricing, switching providers, and deciding between personal API keys or cloud-hosted LLMs

This guide walks through an ideal workflow for selecting and comparing LLMs inside the app’s model browser. You’ll learn how to read model cards, compare token limits and pricing, switch providers, and decide when to use your own API keys or cloud-hosted LLMs.

## Quick overview: model capabilities and limits

When you open the model browser you’ll see a provider selector (e.g., Anthropic, Google, xAI) and a list of models. Each model card typically shows:

* Supported modalities (e.g., images)
* Browser access (the extension performs in-extension web browsing when supported)
* Prompt caching support
* Max output token limit (context window / provider limit)
* Pricing broken down by input tokens, cache writes, cache reads, and output tokens

Knowing these fields helps you pick the best trade-off between cost, speed, and capability.

<Frame>
  <img alt="A dark-themed app settings panel showing API provider and model selection, with &#x22;anthropic/claude-3.7-sonnet&#x22; highlighted among options like google/gemini-2.5-pro and x-ai/grok-3. The pane also displays model features and token pricing details." />
</Frame>

## Model comparison (consolidated)

Below is a concise comparison of the models shown in the examples. Use this table to quickly compare max output tokens and the four pricing dimensions so you can estimate cost for your workload.

| Model             |    Max output |               Input price |      Cache writes price |       Cache reads price |             Output price | Notes                                                                 |
| ----------------- | ------------: | ------------------------: | ----------------------: | ----------------------: | -----------------------: | --------------------------------------------------------------------- |
| Claude 3.7 Sonnet | 64,000 tokens |   \$3.00 / million tokens | \$3.75 / million tokens | \$0.30 / million tokens | \$15.00 / million tokens | High-capability model for quality-sensitive tasks                     |
| Gemini 2.5 Pro    | 65,536 tokens |   \$1.25 / million tokens | \$1.63 / million tokens | \$0.31 / million tokens | \$10.00 / million tokens | Good cost/quality balance for experimentation                         |
| Grok 3            |        Varies | Free (at time of capture) |                     N/A |                     N/A |                      N/A | Feature parity may vary by provider; may lack images/browsing/caching |

> **lightbulb** Prices and features change frequently. Always verify token limits and pricing in the UI before running production jobs.

## Feature parity and switching models

Many model cards list similar capabilities (images, browsing, prompt caching) and comparable token limits. For example, Gemini 2.5 Pro reports a slightly larger numeric max output (65,536 tokens) than some alternatives.

A typical workflow:

* Start with a lower-cost model (e.g., Gemini) for experimentation and iteration.
* If quality or features are insufficient, switch to a higher-capability model (e.g., Claude 3.7 Sonnet or GPT-4 variants) for critical tasks.
* Test the same prompt across models to measure quality differences vs cost.

Below is the editor/provider selection UI where you can pick providers and models:

<Frame>
  <img alt="A dark-themed code editor window with a left panel open showing an &#x22;API Provider&#x22; dropdown and a model selector highlighting &#x22;google/gemini-2.5-pro&#x22; plus its capabilities and pricing details. The rest of the screen is a large empty blue editor area." />
</Frame>

## Using your own API keys and cloud-hosted LLMs

If you have provider accounts, you can configure your own API keys in the extension to bill usage to your account. Common options:

* Enter an API key and optionally set a custom base URL.
* Keys are typically stored locally by the extension and used only to make API requests from your device.
* Add cloud-hosted options (Amazon Bedrock, LLM Studio, Ollama) by supplying region and credentials where required.

Using your own key can avoid double-billing through the app and may be cheaper depending on your provider plan.

Example UI excerpt (model + pricing summary) you may see when configuring a provider:

```text theme={null}
API Provider: Anthropic
Model: claude-opus-4-20250514
✓ Supports images
✓ Supports browser use
✓ Supports prompt caching
Max output: 8,192 tokens
Input price: $15.00 / million tokens
Cache writes price: $18.75 / million tokens
Cache reads price: $1.50 / million tokens
Output price: $75.00 / million tokens

(Your API key is stored locally and only used to make API requests from this extension.)
```

> **warning** Protect your API keys: only enter keys you control, verify local storage behavior, and avoid sharing sensitive credentials. When using cloud providers, follow their recommended credential and region configuration processes.

## Recommendations (practical checklist)

* Start with a lower-cost model to iterate quickly; only escalate to higher-capability models when necessary.
* Compare token limits and all four pricing dimensions (input, cache writes, cache reads, output) to estimate costs precisely.
* Add your own provider API key if you have one — this can reduce cost and centralize billing.
* Double-check feature availability (images, browsing, caching) in the UI before relying on a capability in production.
* Run short A/B tests across candidate models to measure quality vs cost trade-offs for your prompts.

## Links and references

* LLM Studio: [https://llm.studio](https://llm.studio)
* Ollama: [https://ollama.com](https://ollama.com)
* Amazon Bedrock: [https://aws.amazon.com/bedrock/](https://aws.amazon.com/bedrock/)
* Provider documentation (general): OpenAI, Anthropic, Google Cloud documentation

That covers how to read model cards, compare pricing and token limits, switch providers, and decide when to bring your own keys or use cloud-hosted LLMs.

- [Watch Video](https://learn.kodekloud.com/user/courses/cline/module/07505364-dfb1-4691-8f55-ce69bc5e81ec/lesson/93be9556-6476-40cb-8fe3-f19fe22b4b19)
