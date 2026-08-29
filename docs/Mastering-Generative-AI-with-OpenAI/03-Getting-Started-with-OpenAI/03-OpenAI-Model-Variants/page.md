# OpenAI Model Variants

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Getting-Started-with-OpenAI/OpenAI-Model-Variants/page

OpenAI’s API offers various model families and variants optimized for specific use cases, balancing performance, cost, and accuracy.

OpenAI’s API provides a rich set of model families and variants, each optimized for specific use cases—from code completion to conversational AI. Choosing the right model can help you balance performance, cost, and accuracy.

## Model Families and Variants

A **model family** groups related variants by their primary function. Each **variant** carries a version identifier reflecting its training improvements and feature set. Below is a high-level overview:

| Model Family (Use Case)     | Variant            | Optimized For                           |
| --------------------------- | ------------------ | --------------------------------------- |
| Davinci (Natural Language)  | `text-davinci-002` | Instruction following                   |
|                             | `text-davinci-003` | Advanced NLU and generation             |
| Codex (Code Completion)     | `code-davinci-002` | Code autocomplete and synthesis         |
| GPT-3.5 (Chat & Completion) | `gpt-3.5-turbo`    | Low-latency chat and multi-turn support |

### GPT-3.5 Variants Overview

The GPT-3.5 series balances capability and cost with varying token limits and data cutoffs:

| Variant            | Max Tokens | Training Data Through | Primary Use Case       |
| ------------------ | ---------- | --------------------- | ---------------------- |
| `text-davinci-003` | 4,096      | June 2021             | Natural language tasks |
| `gpt-3.5-turbo`    | 4,096      | September 2021        | Chat-style interfaces  |

<Frame>
  ![The image is a table listing GPT-3.5 model variants, including their descriptions, maximum tokens, and training data. It categorizes models into "Chat" and "Word/Code Completion" types.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881517/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Model-Variants/gpt-3-5-model-variants-table.jpg)
</Frame>

<Callout icon="lightbulb">
  `gpt-3.5-turbo` is optimized for multi-turn dialogues and often delivers lower latency and cost for chat applications.
</Callout>

OpenAI continually refines these variants, improving response quality, speed, and cost-effectiveness.

## Fine-Tuning Models

Fine-tuning allows you to customize a base model on your domain-specific dataset. Benefits include:

* Domain-tailored responses with higher relevance
* Shorter prompts, reducing token usage and cost
* Faster inference, since context is baked into the model

<Frame>
  ![The image illustrates the process of model fine-tuning, showing a flow from custom data to a fine-tuned model that generates responses. It highlights benefits like higher quality results, token savings, and lower latency.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881519/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Model-Variants/model-fine-tuning-process-diagram.jpg)
</Frame>

### Fine-Tuning Workflow

1. Format your dataset in JSONL with prompt–completion pairs.
2. Upload data and create a fine-tuning job via the CLI or API.
3. Monitor training, evaluate performance, and deploy your custom endpoint.

<Callout icon="triangle-alert">
  Ensure your training data is clean, balanced, and representative. Low-quality data can degrade performance.
</Callout>

## Embeddings and Semantic Search

Embeddings convert text into vector representations for advanced applications:

| Use Case              | Description                                    |
| --------------------- | ---------------------------------------------- |
| Semantic Search       | Retrieve documents based on contextual meaning |
| Recommendation        | Suggest similar content or products            |
| Entity Classification | Categorize text into predefined classes        |

OpenAI’s `text-embedding-ada-002` model generates high-quality embeddings at scale.

<Frame>
  ![The image illustrates an embedding model process where the text "anatine amigos" is converted into a vector using the "text-embedding-ada-002" model.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881520/notes-assets/images/Mastering-Generative-AI-with-OpenAI-OpenAI-Model-Variants/anatine-amigos-text-embedding-vector.jpg)
</Frame>

## Other Model Families

OpenAI’s ecosystem extends beyond GPT and Codex:

* [DALL·E 2](https://platform.openai.com/docs/models/images/dall-e-2) – Image generation (beta)
* [Whisper 1](https://platform.openai.com/docs/models/speech-to-text) – Speech-to-text (beta)

***

## Links and References

* [OpenAI API Documentation](https://platform.openai.com/docs/)
* [Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
* [Embeddings Overview](https://platform.openai.com/docs/guides/embeddings)
* [DALL·E 2 Documentation](https://platform.openai.com/docs/models/images/dall-e-2)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/7cf291c5-4705-4a69-965a-b0ba7d2169c6/lesson/5aa8c7e7-7a43-413d-8d28-712048e7a136" />
</CardGroup>
