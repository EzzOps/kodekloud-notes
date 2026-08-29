# Chat Completions

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Chat-Completions/page

This guide explains migrating to the modern chat completions API for enhanced conversational experiences with OpenAI models.

Unlock richer conversational experiences by switching from legacy completions endpoints to the modern `chat.completions.create` interface. This guide walks you through migrating your code, customizing your client, leveraging message roles, and fine-tuning parameters for GPT-3.5-Turbo, GPT-4, and beyond.

***

## Why Migrate from Legacy Endpoints

OpenAI’s older `completions.create` and `Completion.create` endpoints stopped receiving updates as of July 2023. The new chat completions API supports structured conversations with roles, function calls, and more control over model behavior.

> **triangle-alert** Avoid using legacy calls: they no longer receive feature updates and may be removed in future releases.

### Legacy Usage Examples

```python theme={null}
