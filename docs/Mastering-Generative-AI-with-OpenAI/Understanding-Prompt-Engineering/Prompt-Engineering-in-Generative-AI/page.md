# Example usage
input_list = [2, 5, 8, 10, 3, 6]
result = sum_even_numbers(input_list)
print("Sum of even numbers:", result)
```

<Callout icon="lightbulb">
  Always review and test generated code for edge cases, performance, and security considerations before using it in production.
</Callout>

## Summary

We’ve covered the seven primary prompt types—explicit, conversational, instructional, context-based, open-ended, bias-mitigating, and code-generation. By selecting and refining these prompts, you can significantly improve LLM accuracy, relevance, and fairness. Experiment with each category to discover what works best for your applications.

## Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/8c96af76-fcd9-4bdf-a176-b7af1decdc5c/lesson/6a4d412c-f03b-4c18-b187-df2de1ea3bed" />
</CardGroup>


# Prompt Engineering in Generative AI

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Understanding-Prompt-Engineering/Prompt-Engineering-in-Generative-AI/page

This article discusses prompt engineering for guiding large language models to produce accurate and relevant outputs without altering model weights.

Prompt engineering is the art and science of crafting inputs (prompts) that guide large language models (LLMs) like GPT toward accurate, relevant, and controlled outputs—without changing the model weights or retraining on new data.

<Callout icon="lightbulb">
  Think of your prompt as code: precise instructions lead to reliable results. Combining technical understanding of model behavior with creative phrasing is key to reducing errors and maximizing output quality.
</Callout>

## Key Benefits of Prompt Engineering

| Benefit               | Description                                           | Example Prompt                                                           |
| --------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------ |
| Control Outputs       | Shape tone, style, and structure of the response      | “Translate this paragraph to French, preserving a formal register.”      |
| Reduce Hallucinations | Clarify context to avoid generating incorrect details | “Summarize the following news article factually without adding details.” |
| Enable Complex Tasks  | Chain multi-step instructions for workflow automation | “First outline the plot, then draft dialogue for Scene 2 in screenplay.” |

<Frame>
  ![The image explains prompt engineering, showing how it improves AI responses without altering the model or data, and highlights the risk of hallucinations from inadequate prompt engineering.](https://kodekloud.com/kk-media/image/upload/v1752881561/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Prompt-Engineering-in-Generative-AI/prompt-engineering-ai-responses-hallucinations.jpg)
</Frame>

## Why Clear Prompts Matter

Large language models interpret your prompt as a custom “programming language.” Vague or underspecified prompts often cause:

* Off-topic or irrelevant responses
* Fabricated facts and inaccuracies (hallucinations)
* Inconsistent formatting or style

Well-structured prompts help you:

* Achieve precise outputs (summaries, code, translations)
* Maintain factual accuracy across tasks
* Optimize results without fine-tuning the model

Next, we’ll dive into practical techniques—such as prompt templates, role prompting, and chain-of-thought—to maximize the reliability and relevance of your Generative AI workflows.

## Links and References

* [OpenAI Prompt Design Guide](https://platform.openai.com/docs/guides/completion/prompt-design)
* [GPT-3 Documentation](https://beta.openai.com/docs/)
* [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/8c96af76-fcd9-4bdf-a176-b7af1decdc5c/lesson/3b6b912f-e56c-48e3-8d55-f232444277f2" />
</CardGroup>
