# Using Prompt Engineering

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Using-Prompt-Engineering/page

How to design structured prompts and system messages to elicit more relevant, actionable, and prioritized responses from language models, with examples and a practical checklist.

Prompt engineering improves the quality, relevance, and actionability of responses from a general-purpose language model. In this lesson we examine how an out-of-the-box model behaves and how small, structured prompts produce much richer results.

## Out-of-the-box behavior

A general-purpose AI model trained on diverse public data will answer valid questions, but often with broad, surface-level responses. When prompts lack context and constraints, the model returns generic suggestions rather than prioritized, personalized guidance.

Example user question:

```text theme={null}
what are some tips for saving money on groceries?
```

An uncustomized model typically replies with high-level suggestions such as:

* Plan meals
* Create a shopping list
* Buy in bulk
* Choose store-brand products

These are correct but not tailored, prioritized, or actionable. To get useful, expert-like responses we need to provide purpose and structure—this is prompt engineering.

## What is prompt engineering?

Prompt engineering shapes a model’s output by defining role, intent, constraints, and expected format. The two primary components are:

* System message (define role and expertise)
* User prompt (specify the task, constraints, and desired format)

Example system message and a specific user prompt:

```json theme={null}
// System message
"You are a financial expert who specializes in household budgets and grocery savings. Provide practical, prioritized strategies and explain trade-offs."

// User prompt
"Provide a prioritized top-10 list of grocery-saving strategies for a family of four, including estimated monthly savings, implementation difficulty (1–5), and one example shopping tactic per item."
```

<Callout icon="lightbulb">
  A clear system message gives the model purpose and focus. A specific user prompt supplies constraints and the expected format, which together produce more useful and actionable responses.
</Callout>

With this structure, the AI produces practical, prioritized suggestions—e.g., planning weekly menus around sale items, combining bulk buys with perishability considerations, and using coupons and cashbacks. The output becomes actionable because the model understands intent, scope, and the desired format.

<Frame>
  <img alt="An infographic titled &#x22;Using Prompt Engineering&#x22; that diagrams training data feeding a language model which powers an AI app. It also shows a sample system/user prompt and a completion response giving prioritized strategies to cut grocery expenses." />
</Frame>

## Practical prompt-engineering checklist

Use this checklist to convert a vague request into a high-quality prompt:

| Component      | Purpose                                           | Example                                                                |
| -------------- | ------------------------------------------------- | ---------------------------------------------------------------------- |
| System message | Define role/expertise and tone                    | "You are a personal finance advisor."                                  |
| Context        | Provide background about the user or scenario     | "Family of four, two adults, two children, urban area."                |
| Constraints    | Limits on format, length, or assumptions          | "Top-10 list, 1–2 sentence explanation each."                          |
| Metrics        | If relevant, ask for estimates or comparisons     | "Include estimated monthly savings and difficulty level."              |
| Output format  | Specify JSON/table/bulleted list for easy parsing | "Return a Markdown table with columns: strategy, savings, difficulty." |

## Example: Before vs After

Before (vague prompt):

```text theme={null}
How can I save money on groceries?
```

After (engineered prompt):

```text theme={null}
System: "You are an experienced frugal-living advisor."
User: "Create a prioritized top-10 list of grocery-saving strategies for a family of four. For each strategy, include: estimated monthly savings (USD), implementation difficulty (1-5), one example shopping tactic, and any trade-offs. Present results as a Markdown table."
```

The “after” prompt yields a prioritized, comparable, and actionable result that the user can implement immediately.

## Tips for more advanced prompts

* Break complex requests into step-by-step subtasks (decomposition).
* Provide examples of the desired output format (few-shot prompting).
* Limit or require reasoning chains when needed, e.g., “Show calculations.”
* Use role-play to shift tone or level of expertise (e.g., “Act as a nutritionist and cost analyst.”)

## Links and references

* [Kubernetes Docs — Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (example knowledge resource)
* [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/prompting) (practical prompting patterns)
* [Prompt Engineering Best Practices (blog)](https://www.prompting.guide/) (examples and templates)

Prompt engineering is not just about finding the right words; it's about setting intent, supplying structure, and guiding the model to act with purpose. In the next sections we will break down more strategies and demonstrate examples that show the measurable impact of good prompts.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/c7f1cdb3-496d-4f65-851a-630bce4e6061" />
</CardGroup>
