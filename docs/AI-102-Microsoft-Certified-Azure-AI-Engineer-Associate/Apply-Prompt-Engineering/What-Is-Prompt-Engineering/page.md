# What Is Prompt Engineering

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/What-Is-Prompt-Engineering/page

A practical guide to prompt engineering teaching specificity, structured outputs, added context, and bias mitigation so generative AI yields more accurate, relevant, and fair responses.

Prompt engineering is the practice of designing clear, targeted inputs for generative AI so that models return more accurate, relevant, and usable outputs. It solves a common problem many developers and researchers face: good models can still produce vague or off-topic answers when given weak prompts.

Meet Rhea, an AI researcher who uses language models to help with projects ranging from drafting documentation to answering technical questions. Over time, she noticed that the quality of the AI's responses often depended less on the model itself and more on how she asked questions. Her mentor, Sam, gave a simple insight: treat the AI like an assistant you instruct, not a search engine. Specificity, structure, context, and fairness in prompts lead to better responses. By improving prompts, Rhea got more useful results without switching models or rewriting application code.

Below are four practical prompt-engineering techniques Rhea adopted, why they work, and concrete examples you can reuse.

1. Be specific — improve accuracy

* The problem: Generic prompts leave the model too many degrees of freedom and cause vague answers.
* The solution: Define the task, audience, constraints, and desired depth.

Example:

```text theme={null}
Generic:
Explain cloud computing.

Specific:
Explain cloud computing for a non-technical product manager. Cover cost considerations, scalability trade-offs, and basic security practices. Provide two one-paragraph examples showing different business use cases.
```

Why it helps: Specific prompts narrow scope and set expectations for length, tone, and content, producing more focused, actionable responses.

2. Structure your output — control format

* The problem: Free-form paragraphs are harder to scan, parse into UIs, or convert into documentation.
* The solution: Request an explicit format (bullets, numbered steps, tables, headings).

Example:

```text theme={null}
Prompt:
Act as a technical writer. Summarize the differences between SaaS, PaaS, and IaaS in a three-row table with columns: Definition, Typical Use Case, Key Benefits.
```

Why it helps: Structured output saves post-processing time and improves readability for users and downstream tools.

3. Add context — improve relevance

* The problem: Without background or role information, the model’s tone or depth may not match your needs.
* The solution: Provide a short role or system message and any necessary background.

Example:

```text theme={null}
System/role:
You are an AI tutor helping new developers understand cybersecurity basics.

User prompt:
Explain the concept of least privilege and give two practical steps a junior engineer should take to apply it.
```

<Callout icon="lightbulb">
  Provide a clear role or system message when you want consistent tone, depth, or domain expertise from the model. A one-line role often yields significantly better, more focused responses.
</Callout>

4. Address bias — encourage fairness

* The problem: Loaded or leading language in prompts can produce biased, unbalanced, or harmful outputs.
* The solution: Inspect and rephrase prompts to be neutral and inclusive. Ask for multiple perspectives when appropriate.

Example:

```text theme={null}
Biased:
Why are men better at tech?

Neutral:
What factors influence gender diversity in technology fields, and what steps can organizations take to improve inclusivity?
```

Why it helps: Neutral prompts reduce the chance of amplifying stereotypes and produce balanced, actionable recommendations.

<Frame>
  <img alt="A slide titled &#x22;Prompt Engineering&#x22; that shows how &#x22;Riya Provided Right Prompts&#x22; improves four areas: Improve Accuracy, Control Formatting, Enhance Context, and Reduce Bias. Each column compares an earlier vague prompt with a new, specific prompt and the resulting outcomes (clear responses, structured formatting, tailored suggestions, and balanced results)." />
</Frame>

These four practices produce outputs that are more thoughtful, actionable, and inclusive. They form a simple, repeatable prompt design loop: clarify intent → constrain format → add context → check for bias.

Prompt Engineering Techniques — At a Glance

| Technique         | Goal                                 | Example Prompt / Output                                                                                                     |
| ----------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Be specific       | Increase accuracy and relevance      | "Explain cloud computing for a non-technical product manager; include cost, scalability, security, and two short examples." |
| Structure outputs | Improve readability and parseability | "Summarize SaaS, PaaS, IaaS in a 3-row table with Definition, Typical Use Case, Key Benefits."                              |
| Add context       | Match tone and expertise level       | "You are an AI tutor... Explain least privilege and give two practical steps."                                              |
| Address bias      | Produce fair and balanced answers    | "What factors influence gender diversity in technology and how can companies improve inclusivity?"                          |

Recap — Four prompt-engineering strategies

* Be specific: Define the task, audience, constraints, and expected depth. Narrow prompts produce focused answers.
* Structure outputs: Ask for lists, tables, headings, or numbered steps to make responses easier to read and reuse.
* Add context: Use a role or short background to align tone, depth, and domain expertise.
* Address bias: Reword loaded language and request balanced perspectives.

Further reading and resources

* [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/prompt-design)
* [Hugging Face — Prompting Best Practices](https://huggingface.co/docs)
* [Responsible AI and Fairness Resources](https://www.microsoft.com/ai/responsible-ai)

With clear prompts, even basic models can deliver surprisingly intelligent and actionable results.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/248836b0-f738-43da-a8a6-5d6625c6dac4" />
</CardGroup>
