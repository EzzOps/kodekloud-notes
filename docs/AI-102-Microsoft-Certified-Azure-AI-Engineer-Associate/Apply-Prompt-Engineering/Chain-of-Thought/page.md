# Chain of Thought

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Chain-of-Thought/page

Describes chain-of-thought prompting that elicits step-by-step reasoning from models to improve accuracy, transparency, and explainability.

Chain-of-thought is a prompt-engineering technique that asks a model to expose intermediate reasoning steps before presenting a final answer. Asking for this explicit decomposition encourages the model to build a logical progression, which often improves accuracy, transparency, and explainability.

This lesson uses a concise example: ask the model which subject is "easy to understand but hard to master," and instruct it to break down its thinking before answering. Modern LLMs (for example, ChatGPT-4.5) often include an analysis or reasoning section showing how they arrived at a conclusion when prompted for a chain-of-thought.

Step-by-step CoT workflow:

1. Define evaluation criteria.
2. Identify candidate subjects that match both ends of the spectrum.
3. Compare candidates against the criteria with concrete examples.
4. Draw a reasoned conclusion based on the comparison.

Step one in chain-of-thought is

<Frame>
  <img alt="A dark-themed slide titled &#x22;Chain of Thought&#x22; that shows a prompt asking a model to break down its reasoning and a sample question about which subject is easy to understand but hard to master. A small illustration of a thinking woman with a question mark accompanies the text." />
</Frame>

define the criteria used to evaluate possible answers. For "easy to understand", the model looks for subjects that are intuitive, require few prerequisites, and are quick to grasp. For "hard to master", the model favors subjects that demand deep expertise, involve complex problems, or require many years of practice. Defining these criteria gives the model a clear framework to evaluate options and compare candidates objectively.

<Frame>
  <img alt="A presentation slide titled &#x22;Step 1: Defining the Criteria&#x22; that lists traits for &#x22;easy to understand&#x22; (intuitive, minimal prerequisites, quick to grasp) and &#x22;hard to master&#x22; (deep complexities, years of expertise, advanced problem‑solving). Below the text is a seesaw-style graphic visually balancing &#x22;Easy&#x22; and &#x22;Mastery.&#x22;" />
</Frame>

With criteria in place, the model next identifies candidate subjects that plausibly fit both ends of the spectrum. Using the evaluation framework, the model shortlists candidates such as:

* Mathematics: basic arithmetic is straightforward, but higher-level fields involve abstraction and technical depth.
* Chess: rules are simple to learn, while grandmaster-level play requires long-term pattern recognition and strategic nuance.
* Music theory: basic chords and notation are accessible, but professional composition and performance demand deep theoretical and practical skill.

<Frame>
  <img alt="A presentation slide titled &#x22;Step 2: Identifying Subjects&#x22; that lists three subjects—Mathematics, Chess, and Music Theory—with short descriptors about basic vs. advanced difficulty. The bottom of the slide shows three colorful circular icons labeled for each subject." />
</Frame>

Next, the model compares and analyzes each candidate against the defined criteria to determine which subject best fits "easy to understand but hard to master." This step should give concrete examples of early, accessible learning milestones and advanced challenges.

Comparison summary (examples of "Easy to Learn" vs "Hard to Master"):

| Subject      | Easy to Learn                                | Hard to Master                                                              |
| ------------ | -------------------------------------------- | --------------------------------------------------------------------------- |
| Mathematics  | Basic arithmetic, elementary problem solving | Abstract branches (topology, real analysis), research-level problem solving |
| Chess        | Piece movements, basic tactics               | Deep opening theory, endgame technique, long-term planning                  |
| Music theory | Major/minor scales, basic chords             | Composition, advanced harmony, virtuoso performance                         |

<Frame>
  <img alt="A presentation slide titled &#x22;Step 3: Comparing Complexity&#x22; showing a three-column table that compares subjects (Mathematics, Chess, Music Theory) with examples of what's &#x22;Easy to Learn&#x22; versus &#x22;Hard to Master.&#x22; Below the table are abstract icons and a standing woman illustration, suggesting analysis or reflection." />
</Frame>

Based on that analysis, the model draws a reasoned conclusion. In this example, mathematics is the strongest candidate: nearly everyone learns basic math early in life, yet advancing into higher mathematics demands abstract thinking, sophisticated problem solving, and often many years of dedicated study.

<Frame>
  <img alt="A presentation slide titled &#x22;Step 4: Conclusion&#x22; stating the final answer that mathematics is easiest to understand but hardest to master. It includes a brief why (everyone knows numbers but higher math needs deep abstraction), plus a stair-like graphic, some formulas, and the numbers &#x22;123.&#x22;" />
</Frame>

This four-step chain-of-thought workflow—define criteria, identify candidates, compare complexity, and conclude—demonstrates how prompting a model to show intermediate reasoning can produce more transparent, logical, and explainable responses.

Example prompt to elicit chain-of-thought:

```text theme={null}
Question: Which subject is easiest to understand but hardest to master?
Instructions: First, list the evaluation criteria for "easy to understand" and "hard to master." Second, identify 3 candidate subjects and explain why each fits those criteria. Third, compare them and give your conclusion with the strongest reasons.
Provide your step-by-step reasoning before the final answer.
```

Benefits of using Chain-of-Thought prompts:

* Improves transparency and traceability of model outputs.
* Helps catch flawed reasoning earlier by exposing intermediate steps.
* Useful for tasks that require planning, multi-step calculations, or justification.

Potential pitfalls and limitations:

* Long chains can still include incorrect or misleading intermediate steps — always verify critical conclusions.
* Explicit CoT may increase token usage and response length.
* Some models may decline to show internal chain-of-thought; consider using "explain your reasoning" style prompts that produce structured analyses.

<Callout icon="lightbulb">
  Chain-of-thought prompts often improve reasoning and explainability. However, longer chains can still contain incorrect steps—verify any critical conclusions and cross-check with trusted sources.
</Callout>

Further reading and references:

| Resource                                                                        | Description                                                      |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [Prompt engineering overview](https://en.wikipedia.org/wiki/Prompt_engineering) | Concepts and best practices for crafting prompts.                |
| [Chain-of-thought research paper summary](https://arxiv.org/abs/2201.11903)     | Academic literature describing CoT and its effects on reasoning. |
| [OpenAI best practices](https://platform.openai.com/docs/guides/prompting)      | Practical guidelines for prompting large language models.        |

With that, this lesson on chain-of-thought prompt engineering is complete — use the pattern (define → identify → compare → conclude) to get clearer, more explainable model responses.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/8349e322-1406-4fc3-8d8d-da1c456045e7" />
</CardGroup>
