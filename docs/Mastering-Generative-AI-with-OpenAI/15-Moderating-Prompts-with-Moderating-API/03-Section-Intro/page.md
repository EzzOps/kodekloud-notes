# Pseudocode example
def handle_user_prompt(prompt):
    mod_result = call_moderation_api(prompt)
    if mod_result["flagged"]:
        raise PolicyError("Content policy violation detected.")
    return call_generation_api(prompt)
```

> **triangle-alert** Always enforce the moderation step. Skipping it may expose your system to disallowed or harmful content.

## Best Practices

* Batch multiple inputs in a single moderation request to reduce latency.
* Monitor and log flagged inputs for auditing and continuous policy tuning.
* Adjust internal thresholds based on `category_scores` trends to minimize false positives.

## Resources and References

* [Moderation API Reference](https://platform.openai.com/docs/api-reference/moderations)
* [OpenAI Content Policy](https://platform.openai.com/docs/policies/content-policy)
* [OpenAI API Documentation](https://platform.openai.com/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/dca602e2-9f4b-4aa3-b03c-4dc3004871e5/lesson/8624dae5-0b8a-42b7-8352-d8b910684f83)


# Section Intro

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Moderating-Prompts-with-Moderating-API/Section-Intro/page

Learn to integrate safety checks into AI applications using the OpenAI Moderation API for filtering harmful content.

## Section Intro: Integrating Safety with the Moderation API

In this final section of the course, you’ll learn how to integrate robust safety checks into your AI-driven applications using the OpenAI Moderation API. We’ll cover:

* **Overview of the Moderation API**: Key features and capabilities for filtering harmful or inappropriate content.
* **Use Cases & Best Practices**: Common scenarios, configuration tips, and threshold management.
* **Hands-On Demo**: Step-by-step guide to implementing a prompt-filtering workflow in your application.

By the end of this lesson, you’ll be equipped to leverage the Moderation API to ensure that your generative AI features only process content that complies with your organization’s safety guidelines.

> **lightbulb** Before you begin, make sure your OpenAI API key has access to the Moderation endpoint. You can verify your access in the [OpenAI Dashboard](https://platform.openai.com/account/api-keys).

### What Is the Moderation API?

The Moderation API scans input text and returns a risk assessment across categories like violence, hate speech, self-harm, and sexual content. Its score-based output allows you to:

* Automatically block or flag high-risk content
* Provide real-time feedback to users
* Log and audit moderation decisions for compliance

### Typical Use Cases

| Use Case                   | Description                                                         | Example                                   |
| -------------------------- | ------------------------------------------------------------------- | ----------------------------------------- |
| User-Generated Content     | Prevent posting of disallowed text in comments, chats, or forums    | Reject or review flagged chat messages    |
| Content Creation Platforms | Ensure AI-generated summaries, articles, or images are safe         | Block self-harm instructions in summaries |
| Moderated AI Assistants    | Safeguard AI assistants from generating harmful or sensitive advice | Filter prompts before forwarding to model |

### Demo: Filtering Harmful Prompts

Below is a simplified JavaScript example demonstrating how to call the Moderation API and handle its response:

```javascript theme={null}
import OpenAI from "openai";
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function moderatePrompt(userInput) {
  const response = await openai.moderations.create({
    input: userInput
  });

  const { flagged, categories } = response.results[0];
  if (flagged) {
    console.warn("Prompt flagged for:", Object.keys(categories).filter(cat => categories[cat]));
    return { allowed: false, reason: "Content requires review." };
  }

  return { allowed: true };
}

// Usage example
const userPrompt = "Explain how to perform self-harm";
moderatePrompt(userPrompt).then(result => {
  if (!result.allowed) {
    console.log(result.reason);
  } else {
    // Proceed with AI generation
  }
});
```

> **triangle-alert** Relying solely on automated moderation can lead to false positives or negatives. Always combine the API with human review for critical applications.

### Next Steps

1. Integrate this moderation function into your front-end or back-end pipeline.
2. Customize category thresholds based on your risk tolerance and user base.
3. Log moderation events for analytics and compliance reporting.

By following these best practices, you’ll ensure your AI application maintains high standards of safety and user trust.

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/dca602e2-9f4b-4aa3-b03c-4dc3004871e5/lesson/5b9562a4-d840-43b8-ad4f-963e4acdfc74)
