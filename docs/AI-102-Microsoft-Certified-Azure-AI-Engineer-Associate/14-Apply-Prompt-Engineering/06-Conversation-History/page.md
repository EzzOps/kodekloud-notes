# Conversation History

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Conversation-History/page

Explains using conversation history and few-shot examples to guide AI behavior, demonstrating email classification into Work Personal or Spam and providing best practices for prompt design

Conversation history is a core capability that makes AI interactions feel natural and context-aware. By preserving prior messages, models can produce coherent, relevant responses that reflect the ongoing topic, user tone, and previously provided examples. This lesson explains why conversation history matters and demonstrates a practical classification example using few-shot learning.

Why conversation history matters

1. Retaining previous messages preserves context and style\
   Conversation history lets the model remember the topic, user preferences, and previous instructions. This continuity helps the model avoid repetition, maintain the intended tone, and make context-aware decisions (for example, applying a previously set role or following a long-running task).

2. Few-shot learning with example exchanges guides behavior\
   Including a few representative user–assistant pairs in the history teaches the model the pattern you expect it to follow. Few-shot examples show the mapping from input to output, enabling the model to generalize to new, similar inputs without retraining.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Conversation History&#x22; showing a teal-outlined box with two bullet points. The bullets note that retaining previous messages helps maintain context and that user-defined (few-shot) examples guide the model's responses." />
</Frame>

> **lightbulb** Including many past messages helps preserve context, but models have token limits. For long histories, summarize earlier turns or select representative examples to keep the prompt concise and relevant.

> **warning** Avoid storing or sending sensitive personal data in conversation history. If you must retain private information, use secure storage and only include minimal, necessary context when calling the model.

Practical example: classification using conversation history and few-shot examples

Below is a short conversation history that sets a system instruction (the model's role) and provides three example user→assistant pairs. These few-shot examples demonstrate how to classify short, email-like messages into three labels: `Work`, `Personal`, or `Spam`. The final user message is a new item to classify; the model should follow the system instruction and the examples to pick the correct label.

```json theme={null}
[
  {"role": "system", "content": "You are an AI assistant that classifies emails into categories: Work, Personal, or Spam."},
  {"role": "user", "content": "Meeting scheduled for Monday at 10 AM."},
  {"role": "assistant", "content": "Work"},
  {"role": "user", "content": "Hey, want to grab dinner tonight?"},
  {"role": "assistant", "content": "Personal"},
  {"role": "user", "content": "Congratulations! You won a free vacation. Click here to claim."},
  {"role": "assistant", "content": "Spam"},
  {"role": "user", "content": "Client requested a project update by Friday."}
]
```

How this example works

* System instruction: defines the task and the allowed outputs (`Work`, `Personal`, `Spam`).
* Few-shot examples: three user→assistant pairs show the expected mapping from message text to label.
* Final input: the model uses the system instruction plus the examples to infer the correct category for the new message. In this case, "Client requested a project update by Friday." is best classified as `Work`.

Quick reference table

| Category | Typical signals                                               | Example                                         |
| -------: | ------------------------------------------------------------- | ----------------------------------------------- |
|     Work | Mentions projects, clients, deadlines, meetings               | `Client requested a project update by Friday.`  |
| Personal | Invitations, social plans, family messages, casual tone       | `Want to grab dinner tonight?`                  |
|     Spam | Promotional language, click-to-claim offers, suspicious links | `You won a free vacation. Click here to claim.` |

Best practices for using conversation history

* Start with a clear system instruction to define role, tone, and expected output format.
* Include 2–5 high-quality few-shot examples that represent the variety of inputs you expect.
* Keep examples concise and consistent in formatting to avoid introducing ambiguity.
* For long sessions, periodically summarize earlier turns to reduce token usage while preserving context.
* Always mask or omit sensitive data unless explicitly required and securely handled.

Summary

Combining a concise system instruction with a short history of representative examples lets you guide model behavior reliably. Conversation history provides context continuity, while few-shot examples teach the model the exact mapping or style you expect it to follow.

Links and references

* [OpenAI Prompting Best Practices](https://platform.openai.com/docs/guides/prompting)
* [Few-shot Learning Concepts (overview)](https://en.wikipedia.org/wiki/One-shot_learning#Few-shot_learning)
* [Token Limits and Context Windows](https://platform.openai.com/docs/guides/gpt)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/a2a27bba-6e9a-426d-9ffa-2dcd763b2781)
