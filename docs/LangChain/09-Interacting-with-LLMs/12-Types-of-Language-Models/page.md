# Check if OPENAI_API_KEY is set
echo "$OPENAI_API_KEY"
```

* If the command prints a value, your key is already set and you can continue.
* If it prints nothing, run the `export` command above (or set the key in your environment management tool).

In some managed KodeKloud workspaces the API key may already be configured. Confirm the variable before re-exporting.

Quick troubleshooting

* If you see import errors, confirm you installed the pinned versions.
* If you receive authentication or rate-limit errors from OpenAI, confirm your API key is valid and has sufficient quota.

Next steps

With the environment ready, proceed to the next lesson sections to:

* Build prompt-driven interactions using LangChain.
* Make model calls and inspect raw outputs.
* Parse, validate, and transform model responses for use in downstream application code.

Links and references

* [LangChain course on KodeKloud](https://learn.kodekloud.com/user/courses/langchain)
* [OpenAI API keys](https://platform.openai.com/account/api-keys)
* [python-dotenv (for local dev secrets)](https://pypi.org/project/python-dotenv/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/5f40ca43-ec72-4c68-a0df-06085674863e)


# Types of Language Models

Source: https://notes.kodekloud.com/docs/LangChain/Interacting-with-LLMs/Types-of-Language-Models/page

Comparison of Base LLMs and Chat models, explaining their differences, interaction patterns, use cases, and guidance for choosing between single-turn generation and multi-turn conversational models.

Large language models (LLMs) fall into two primary categories: Base LLMs and Chat models. This guide explains their differences, interaction patterns, and when to use each. It preserves the original conceptual order while improving clarity and SEO relevance for developers and product teams.

## Overview

* Base LLMs: General-purpose models trained to model and generate text from a single prompt.
* Chat models: LLM variants fine-tuned for conversational interaction, often using supervised dialogue data and reinforcement learning from human feedback (RLHF).

> **lightbulb** Use Base LLMs when you need single-turn generation (e.g., text completion, creative writing) and Chat models when you require multi-turn, stateful conversations (e.g., chatbots, assistants).

## 1) Base LLMs

Base LLMs are trained to predict and generate text given an input prompt. They are typically used for single-shot or few-shot tasks and are prompt-driven.

Key characteristics:

* Purpose: Text completion, generation of creative content (poems, stories), summarization, code generation, and one-off transformations.
* Interaction pattern: Stateless — you send a prompt and receive generated output. To provide context, you include it in the prompt itself.
* Decoding strategies: greedy decoding, sampling, top-k/top-p (nucleus) sampling, and beam search.
* Typical behavior: Given an incomplete sentence or prompt, the model predicts the next tokens to complete it.

Common use cases:

* Batch or single-request generation pipelines
* Bulk text transformations (e.g., summarizing many documents)
* Creative generation with controlled prompts

## 2) Chat models

Chat models are adapted from base LLMs and optimized for dialogue. They are trained and fine-tuned on conversational data and often further refined with RLHF to align responses with human preferences.

Key characteristics:

* Purpose: Multi-turn conversation, contextual assistance, and interactive agents.
* Interaction pattern: Stateful — the model accepts a sequence of structured messages that capture conversation history and returns a reply that continues the dialogue.
* Roles and persona: Messages include explicit roles such as `system`, `user` (or `human`), and `assistant` (or `ai`), enabling controlled personas and behavior.
* Training: Typically fine-tuned with supervised dialogue data and RLHF to produce helpful, safe, and aligned answers.

Example message structure (JSON-like):

```json theme={null}
[
  { "role": "system", "content": "You are a helpful assistant who answers concisely." },
  { "role": "user",   "content": "Summarize the difference between LLMs and chat models." }
]
```

Use cases:

* Customer support chatbots
* Assistants that maintain session state across turns
* Multi-step workflows and applications requiring follow-up questions

> **warning** Chat models can maintain context across many messages, but they can still hallucinate or produce unwanted outputs. Use system messages, prompt engineering, and moderation/safety layers to reduce risk.

## Side-by-side comparison

| Feature             |                                    Base LLMs | Chat models                                             |
| ------------------- | -------------------------------------------: | ------------------------------------------------------- |
| Interaction pattern |                     Stateless, single prompt | Stateful, structured message history                    |
| Best for            | Single-turn generation, bulk transformations | Multi-turn dialogue, assistants, chatbots               |
| Context management  |                       In-prompt context only | Conversation history via message sequence               |
| Persona control     |                           Prompt engineering | `system` role + role-based messages                     |
| Fine-tuning         |                    General language modeling | Dialogue fine-tuning and often RLHF                     |
| Common decoding     |                Greedy, sampling, beam search | Same decoding options, but tuned for dialogue coherence |

## Choosing the right model

* Pick a Base LLM when:
  * You need one-off text generation or batch processing.
  * You can package all context into a single prompt.
  * You require creative completions without multi-turn state.

* Pick a Chat model when:
  * You need to manage multi-turn interactions or maintain user session state.
  * You want to leverage role-based prompts (`system`, `user`, `assistant`) to set persona and behavior.
  * You need an assistant-style interface that may ask clarifying questions.

## Tools and further reading

* LangChain — orchestration and prompt tooling for LLM workflows: [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)
* Reinforcement learning from human feedback (RLHF) overview — improves alignment and response quality
* OpenAI-style chat message patterns and API best practices (see provider docs for message format and rate limits)

## Key takeaways

* Base LLMs excel at single-prompt generation and creative completions.
* Chat models are optimized for interactive, multi-turn conversations and support explicit roles and personas.
* Both paradigms are supported by modern tooling (e.g., LangChain) and can be chosen based on the specific application requirements.

In this lesson, you will learn how to interact with both Base LLMs and Chat models, and select the pattern that best fits your use case.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/ae260750-791b-496c-991f-0d0333f61e40/lesson/46332dc3-f81b-4b21-bd67-574c6a4de70a)
