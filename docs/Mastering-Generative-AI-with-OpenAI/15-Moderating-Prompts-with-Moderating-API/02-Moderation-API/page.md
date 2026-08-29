# Moderation API

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Moderating-Prompts-with-Moderating-API/Moderation-API/page

The OpenAI Moderation API detects harmful content in user inputs to ensure compliance and protect users before processing with a language model.

The OpenAI Moderation API helps you detect policy-violating, harmful, or unsafe content in user inputs before sending them to a language model. Integrating this check early in your pipeline ensures compliance, protects end users, and maintains the integrity of your application.

## How the Moderation Endpoint Works

When you submit a prompt to the Moderation API, it returns a JSON payload with three primary sections:

| Field            | Type    | Description                                                          |
| ---------------- | ------- | -------------------------------------------------------------------- |
| flagged          | boolean | `true` if any policy violation is detected; `false` otherwise        |
| categories       | object  | A map of violation categories (e.g., `hate`, `self_harm`) to boolean |
| category\_scores | object  | Confidence scores (0.0–1.0) for each category                        |

### Example Request

```bash theme={null}
curl https://api.openai.com/v1/moderations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Your text to check for policy violations"
  }'
```

### Example Response

```json theme={null}
{
  "id": "modr-XXXXX",
  "model": "text-moderation-004",
  "results": [
    {
      "flagged": false,
      "categories": {
        "hate": false,
        "harassment": false,
        "self_harm": false
      },
      "category_scores": {
        "hate": 0.01,
        "harassment": 0.02,
        "self_harm": 0.00
      }
    }
  ]
}
```

<Callout icon="lightbulb">
  Use the confidence values in `category_scores` to prioritize human review of borderline cases.
</Callout>

## Integrating Moderation into Your Application Workflow

Adopt a secure, four-step flow to vet user inputs before content generation:

1. Receive the user prompt.
2. Call the Moderation API.
   * If `flagged` is `true`, return an error:\
     “Your request violates our content policy and cannot be processed.”
   * If `flagged` is `false`, continue.
3. Invoke the Generation API.
4. Return the generated response to the end user.

```python theme={null}
