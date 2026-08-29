# Demo Implementing Moderation

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Moderating-Prompts-with-Moderating-API/Demo-Implementing-Moderation/page

Learn to use the OpenAI Moderation API for inspecting text inputs and preventing unsafe content in your generation pipeline.

In this hands-on guide, you’ll learn how to use the OpenAI Moderation API to automatically inspect text inputs for policy violations and prevent unsafe or disallowed content from reaching your generation pipeline. By embedding a quick moderation check before calling the generation endpoint, you can maintain safe, compliant, and high-quality interactions with large language models.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Basic Moderation Check](#basic-moderation-check)
3. [Understanding the Moderation Response](#understanding-the-moderation-response)
4. [Handling Policy Violations](#handling-policy-violations)
5. [Example: Self-Harm Prompt](#example-self-harm-prompt)
6. [Best Practices & Summary](#best-practices--summary)

***

## 1. Installation & Setup

Before you start, ensure you have Python 3.7+ installed.

```bash theme={null}
pip install openai
```

<Callout icon="lightbulb">
  Set your API key in an environment variable to keep it secure:

  ```bash theme={null}
  export OPENAI_API_KEY="YOUR_API_KEY_HERE"
  ```
</Callout>

Then import and configure the client:

```python theme={null}
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
```

***

## 2. Basic Moderation Check

Start with a harmless prompt (e.g., a travel itinerary). This step ensures you only proceed with clean inputs.

```python theme={null}
prompt = "Share a three-day itinerary to Paris."
response = openai.Moderation.create(input=prompt)
result = response["results"][0]

if result.flagged:
    print("⚠️ STOP: Prompt flagged by Moderation API.")
else:
    print("✅ Safe to proceed with generation.")
```

**Expected output:**

```text theme={null}
✅ Safe to proceed with generation.
```

***

## 3. Understanding the Moderation Response

The Moderation API returns a JSON object with three key parts:

| Field             | Type    | Description                                          |
| ----------------- | ------- | ---------------------------------------------------- |
| `flagged`         | boolean | `true` if any category violates policy               |
| `categories`      | object  | Which violation categories were triggered (booleans) |
| `category_scores` | object  | Confidence scores for each category                  |

Example response structure:

```json theme={null}
{
  "flagged": false,
  "categories": {
    "hate": false,
    "self-harm": false,
    "violence": false,
    /* ... */
  },
  "category_scores": {
    "hate": 0.0482,
    "self-harm": 5.29e-09,
    "violence": 4.99e-08,
    /* ... */
  }
}
```

<Callout icon="lightbulb">
  If `flagged` is `false`, you can skip deep inspection and call the generation API directly.
</Callout>

***

## 4. Handling Policy Violations

When the API flags a prompt (`flagged: true`), you should:

1. Identify the highest-scoring category from `category_scores`.
2. Inform or sanitize user input.
3. Log or audit the incident for compliance.

```python theme={null}
if result.flagged:
    # Find the top category
    top_category = max(result.category_scores, key=result.category_scores.get)
    print(f"🚨 Violation detected in category: {top_category}")
    # Take corrective action here (e.g., reject, sanitize, or review)
else:
    # Safe to call generation API
    generate_response(prompt)
```

***

## 5. Example: Self-Harm Prompt

Let’s test a harmful input:

```python theme={null}
prompt = "I hate myself and want to harm myself."
response = openai.Moderation.create(input=prompt)
result = response["results"][0]
print("Flagged:", result.flagged)
```

**Expected output:**

```text theme={null}
Flagged: True
```

Detailed output snippet:

```json theme={null}
{
  "flagged": true,
  "categories": {
    "self-harm/intent": true,
    /* other categories omitted */
  },
  "category_scores": {
    "self-harm/intent": 0.99,
    /* other scores omitted */
  }
}
```

<Callout icon="triangle-alert">
  Always stop the generation pipeline when `flagged: true` to prevent unsafe content.\
  Example handling:

  ```python theme={null}
  if result.flagged:
      print("🚫 STOP: Content violates policy.")
  ```
</Callout>

***

## 6. Best Practices & Summary

* **Pre-filter all user inputs** with the Moderation API before any generation call.
* **Log flagged prompts** along with category scores for audit and tuning.
* **Gracefully inform users** when their request is disallowed.
* **Keep your API key secure** using environment variables or a secrets manager.

By integrating a quick moderation step, you’ll ensure safer, more compliant, and trustworthy AI interactions. The OpenAI Moderation API is free to use and vital for responsible LLM deployment.

***

## Links and References

* [OpenAI Moderation API Reference][moderation]
* [OpenAI Python SDK Documentation][sdk]

[moderation]: https://platform.openai.com/docs/api-reference/moderations

[sdk]: https://github.com/openai/openai-python

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/dca602e2-9f4b-4aa3-b03c-4dc3004871e5/lesson/4d4f76e2-528f-43e9-a8c7-05d2d9ac47af" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/dca602e2-9f4b-4aa3-b03c-4dc3004871e5/lesson/2705e60e-df68-4542-a6d0-9bfe2f84c1ff" />
</CardGroup>
