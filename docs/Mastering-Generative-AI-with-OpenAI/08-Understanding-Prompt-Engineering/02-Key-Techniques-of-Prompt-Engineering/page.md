# Key Techniques of Prompt Engineering

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Understanding-Prompt-Engineering/Key-Techniques-of-Prompt-Engineering/page

Master three core prompt engineering strategies to effectively guide large language models toward your specific needs.

Unlock the full potential of large language models (LLMs) by mastering three core prompt engineering strategies: zero-shot, one-shot, and few-shot prompting. Each technique offers a different balance between simplicity and control, helping you guide an LLM toward your exact needs.

## Prompt Engineering Techniques Overview

<Frame>
  ![The image illustrates three techniques used in prompt engineering: Zero Shot, One Shot, and Few Shot, each represented by icons within colored frames.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881546/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/prompt-engineering-techniques-icons-diagram.jpg)
</Frame>

When designing prompts, you can choose:

* **Zero-Shot Prompting**: Direct instruction, no examples.
* **One-Shot Prompting**: Single example to illustrate format or style.
* **Few-Shot Prompting**: Multiple examples demonstrating the pattern.

| Technique | Definition                            | Example Task                                    |
| --------- | ------------------------------------- | ----------------------------------------------- |
| Zero-Shot | Direct instruction without examples.  | `Summarize this article in 100 words.`          |
| One-Shot  | One sample input–output pair.         | `Example: “Hello → Hola”. Then translate “Hi”.` |
| Few-Shot  | Several input–output pairs in prompt. | Classifying animals by description.             |

<Callout icon="lightbulb">
  Choose zero-shot for quick tasks, one-shot when you need consistent formatting with minimal context, and few-shot for complex patterns or strict constraints.
</Callout>

***

## 1. Zero-Shot Prompting

<Frame>
  ![The image illustrates the concept of zero-shot prompting for a large language model, showing a task input leading to a response output.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881547/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/zero-shot-prompting-language-model.jpg)
</Frame>

In zero-shot prompting, you present only an instruction. The model draws on its pre-training to handle the request.

```plaintext theme={null}
Write a poem about love.
```

Because LLMs have processed vast amounts of text and code during training, they can perform many tasks right away:

<Frame>
  ![The image explains zero-shot prompting in large language models (LLMs), highlighting their training on diverse datasets to perform tasks without prior specific examples.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881548/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/zero-shot-prompting-llms-explained.jpg)
</Frame>

Common zero-shot tasks include:

* Translate a sentence from English to French.
* Summarize this article in 100 words.
* Answer: “What is the capital of Japan?”
* Write a Python function to reverse a string.

<Frame>
  ![The image shows examples of zero-shot prompting tasks, including writing a poem, translating a sentence, summarizing an article, answering a question, and writing code.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881549/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/zero-shot-prompting-examples-tasks.jpg)
</Frame>

<Callout icon="lightbulb">
  Zero-shot is fast to set up but may require more precise wording for specialized or nuanced tasks.
</Callout>

***

## 2. One-Shot Prompting

<Frame>
  ![The image explains "One-Shot Prompting" for Large Language Models (LLMs), highlighting how a single example can teach an LLM to perform a task. It includes a diagram and text detailing the concept and its current research status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881550/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/one-shot-prompting-llms-diagram.jpg)
</Frame>

One-shot prompting provides exactly one example to illustrate the desired output. The LLM uses that single sample as a template:

```plaintext theme={null}
Example: “Translate ‘Hello, world!’ to Spanish → ‘¡Hola, mundo!’”
Now translate ‘Good morning!’ to Spanish →
```

This approach often yields more consistent results than zero-shot:

* Write a short story about a detective solving a mystery.
* Describe symptoms and treatments for seasonal allergies.
* Provide steps to make a classic margherita pizza.

<Frame>
  ![The image shows examples of one-shot prompting with prompts and responses for writing a short story, discussing seasonal allergies, and making a margherita pizza.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881551/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/one-shot-prompting-examples-responses.jpg)
</Frame>

***

## 3. Few-Shot Prompting

<Frame>
  ![The image shows examples of few-shot prompting with inputs describing animals and corresponding outputs naming the animals: camel, cat, and giraffe.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881552/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Key-Techniques-of-Prompt-Engineering/few-shot-prompting-animal-examples.jpg)
</Frame>

Few-shot prompting includes several illustrative examples. By showing multiple input–output pairs, you help the LLM infer the pattern:

```plaintext theme={null}
Q: A tall mammal with a long neck, spotted coat → Answer: Giraffe
Q: A large aquatic mammal known for its intelligence and sonar → Answer: Dolphin
Q: A desert animal with humps for fat storage → Answer:
```

This technique typically achieves higher accuracy, especially when output format or domain knowledge is crucial.

<Callout icon="triangle-alert">
  Including many examples can increase token usage and latency. Keep your prompt concise to stay within model limits.
</Callout>

By experimenting with zero-, one-, and few-shot prompts—and refining your instructions and examples—you’ll identify the optimal strategy for any LLM-powered application.

***

## Links and References

* [OpenAI Prompt Engineering Guide](https://beta.openai.com/docs/guides/prompt-design)
* [Understanding Few-Shot Learning](https://en.wikipedia.org/wiki/Few-shot_learning)
* [Large Language Models Explained](https://arxiv.org/abs/2005.14165)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/8c96af76-fcd9-4bdf-a176-b7af1decdc5c/lesson/1bc4aeec-6b73-4b0f-a8b8-f4b0bbc2aaf6" />
</CardGroup>
