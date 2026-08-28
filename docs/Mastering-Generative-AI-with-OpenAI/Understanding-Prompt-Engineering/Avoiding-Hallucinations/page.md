# Avoiding Hallucinations

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Understanding-Prompt-Engineering/Avoiding-Hallucinations/page

This article explores hallucination in large language models and techniques to reduce it through prompt engineering and fine-tuning.

In this lesson, we define hallucination in LLMs and explore practical techniques—such as prompt engineering and fine-tuning—to reduce or eliminate it.

## What Is Hallucination?

Hallucination happens when a language model generates plausible-sounding but incorrect or ungrounded information. Instead of returning fact-based answers, the model “dreams up” details based on its training distribution rather than your prompt or real-world data.

<Frame>
  ![The image features a robot with a thought bubble and text explaining "hallucination" in the context of language models, describing it as producing output not grounded in reality.](https://kodekloud.com/kk-media/image/upload/v1752881541/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Avoiding-Hallucinations/robot-hallucination-language-models-explained.jpg)
</Frame>

## Example: When Hallucinations Occur

Consider this simple QA:

```text theme={null}
User: What weighs more, one kilogram of feathers or two kilograms of bricks?
Assistant: One kilogram of feathers weighs the same as two kilograms of bricks.
```

<Frame>
  ![The image shows a conversation about the weight comparison between 1 kilogram of feathers and 2 kilograms of bricks, highlighting an incorrect response about their weights.](https://kodekloud.com/kk-media/image/upload/v1752881543/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Avoiding-Hallucinations/weight-comparison-feathers-bricks-conversation.jpg)
</Frame>

The correct answer is that two kilograms of bricks weigh more. Here, the model lacked context or misapplied its internal distribution, producing a convincing but wrong reply.

## Strategies to Prevent Hallucination

<Callout icon="lightbulb">
  Providing explicit context and instructions up front can dramatically reduce model errors and hallucinations.
</Callout>

| Technique              | Description                                           | Use Case                            |
| ---------------------- | ----------------------------------------------------- | ----------------------------------- |
| Prompt Engineering     | Craft prompts with clear roles, context, and examples | Any API-based interaction           |
| Fine-Tuning            | Retrain on domain-specific or up-to-date data         | Industry-specific use (e.g., legal) |
| Retrieval Augmentation | Combine LLM with a vector database or document store  | Knowledge-base queries              |
| Pre-Training Expansion | Increase training corpus size and diversity           | Custom model development            |

<Callout icon="triangle-alert">
  Even the best prompts can’t replace real-world verification. Always cross-check critical facts.
</Callout>

<Frame>
  ![The image is a diagram explaining how to avoid AI hallucinations by using prompt engineering, larger datasets, and fine-tuning. It shows the relationship between AI models and textual datasets.](https://kodekloud.com/kk-media/image/upload/v1752881544/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Avoiding-Hallucinations/ai-hallucinations-prompt-engineering-diagram.jpg)
</Frame>

## Live Example: Adding Context

**Without context** the model may respond with an apology rather than an answer:

```text theme={null}
User: Who is the founder of Trailblazer Bikes?
Assistant: I’m sorry, but I don’t have information about a company called Trailblazer Bikes.
```

**With context provided first**, the model can answer accurately:

```text theme={null}
User: Trailblazer Bikes is based in Colorado and was founded by John Doe.
User: Based on the above, who is the founder of Trailblazer Bikes?
Assistant: According to the information you provided, Trailblazer Bikes was founded by John Doe in December 2021.
```

## Live Example: Handling Recent Events

LLMs trained up to 2021 lack awareness of later events:

```text theme={null}
User: Who won Best Original Song at the 95th Academy Awards in March 2023?
Assistant: I’m sorry, I don’t have data on events beyond September 2021.
```

By injecting updated facts, the model can respond correctly:

```text theme={null}
User: Here are the nominees and winners for Best Original Song at the 95th Academy Awards (March 2023), including “Naatu Naatu” from RRR as the winner.
User: Based on the above, who won Best Original Song?
Assistant: “Naatu Naatu” from the film RRR won Best Original Song at the 95th Academy Awards.
```

<Frame>
  ![The image shows a slide titled "Avoiding Hallucination" with a conversation about the winner of the original song at the 95th Academy Awards, highlighting the song "Naatu Naatu" from RRR as the winner.](https://kodekloud.com/kk-media/image/upload/v1752881545/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Avoiding-Hallucinations/avoiding-hallucination-naatu-naatu-academy-awards.jpg)
</Frame>

## Key Takeaway

Large language models may hallucinate when context is insufficient or outdated. By crafting precise prompts, supplying relevant data, and applying fine-tuning or retrieval augmentation, you’ll ensure your AI outputs are accurate, reliable, and grounded in real-world information.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/8c96af76-fcd9-4bdf-a176-b7af1decdc5c/lesson/a5082c3d-52b4-4ef7-9c79-1d28960189d7" />
</CardGroup>
