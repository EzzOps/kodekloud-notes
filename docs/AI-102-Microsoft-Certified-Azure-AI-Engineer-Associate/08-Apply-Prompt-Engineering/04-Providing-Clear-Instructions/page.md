# Providing Clear Instructions

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Apply-Prompt-Engineering/Providing-Clear-Instructions/page

Guidelines for writing clear, structured prompts—using primary, supporting, and grounding content, cues, and explicit output formats to improve AI response relevance and usability.

In this lesson we explain how clear, well-structured instructions (prompts) improve the quality of an AI model's output. Clear prompts reduce ambiguity and help the model produce focused, relevant, and actionable responses.

Why this matters: vague prompts yield generic results. For example, a prompt like "write a product description for a new smart thermostat" gives the model little context. The output may be correct, but it often lacks differentiating features, technical benefits, and a clear audience focus.

To get richer results, provide specifics about capabilities, intended users, tone, and desired format. For example, mentioning AI features, energy-optimization algorithms, and voice-assistant integration will prompt the model to generate a more detailed and compelling product description.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Providing Clear Instructions&#x22; showing an orange prompt box requesting a smart thermostat product description and a blue quoted box containing the generated product copy. The footer shows &#x22;© Copyright KodeKloud.&#x22;" />
</Frame>

Takeaway: more detailed prompts lead to more informative, engaging, and customized outputs.

## Structure your prompt: primary, supporting, and grounding content

Organizing the prompt into clear sections makes it easier for the model to follow intent and preserve context. Use separators (hyphens, hashes, or labeled headers) to mark sections when your prompt includes multiple documents or long text.

* Primary content: the main input or core idea (e.g., course delivery formats, deadlines, or product specifications). This is the context the model uses to perform the requested task.
* Supporting content: clarifying examples, data, user preferences, or industry context that enrich the primary content.
* Grounding content: constraints or scope-defining elements (timeframe, audience, required length) that keep answers focused and relevant.

When primary content is missing or unclear, outputs can become off-topic or incomplete.

<Frame>
  <img alt="A dark-blue presentation slide titled &#x22;Primary, Supporting, and Grounding Content&#x22; with a teal callout reading &#x22;Primary content to be summarized, translated, etc.&#x22; and a bordered text box describing course delivery formats (live sessions, recorded videos, hands-on labs), a call for expert instructors, and upcoming proposal deadlines." />
</Frame>

## Use cues to control behavior

Cues are short phrases or directives that specify tone, structure, or intent. They tell the model not just what to produce but how to present it. Examples:

* "Summarize the reviews above."
* "Generate bullet points for a product roadmap."
* "Explain in simple terms for non-technical stakeholders."

Cues are especially helpful when precision or format matters—reports, code snippets, or documented procedures benefit from explicit cues.

Here’s an example: two customer reviews praise food and atmosphere but complain about slow service. Adding the cue "summarize the reviews above" shifts the model from narrative to analytical mode and produces a concise list of common complaints.

<Frame>
  <img alt="A slide titled &#x22;Cues&#x22; showing two sample restaurant reviews that praise the food/atmosphere but complain about slow service and excessive wait times. A summary box below lists those as the most common complaints." />
</Frame>

Use summarization and directive cues to surface the most important information.

## Request structured outputs explicitly

When you need machine-readable or copy/paste-ready results, ask for a specific format (table, CSV, JSON, Markdown). Specify column names or field keys so the model knows exactly what to produce.

<Frame>
  <img alt="A presentation slide titled &#x22;Requesting Output Composition&#x22; showing a prompt on the left and a three-column table on the right listing six programming languages, their primary usage, and popularity ranks. The languages shown are Python, JavaScript, Java, C#, Swift, and Go." />
</Frame>

When to use each structured format:

| Format         | Use case                                   | Example prompt                                                                     |
| -------------- | ------------------------------------------ | ---------------------------------------------------------------------------------- |
| Markdown table | Human-readable documentation or README     | "Provide a markdown table with columns: Language, Primary usage, Popularity rank." |
| CSV            | Data import into spreadsheets or pipelines | "Output CSV rows with columns: product\_id, name, price\_usd."                     |
| JSON           | APIs, automation, or tooling               | "Return a JSON array of objects with keys: title, description, tags."              |

The more explicit your format request (column names, types, field order), the more predictable and immediately usable the output will be.

## Practical tips and final checklist

* Start with a clear primary content block that includes the essential context.
* Add supporting details: examples, metrics, or user personas.
* Add grounding constraints: timeframes, audience, length, or exclusions.
* Add explicit cues: desired style, structure, or output format.
* When needed, request machine-readable output and list the exact columns/keys.

<Callout icon="lightbulb">
  Practical tips: start with a clear primary content block, add supporting details and grounding constraints, and finish with explicit cues and output format requirements (e.g., "Provide a markdown table with these columns: Language, Use Case, Popularity").
</Callout>

## Links and references

* [Prompting best practices — OpenAI Guides](https://platform.openai.com/docs/guides/prompting)
* [Designing prompts for structured outputs (guide)](https://platform.openai.com/docs/guides/completion/structured-output)
* [Practical prompt engineering patterns — blog posts and templates](https://github.com/dair-ai/Prompt-Engineering-Guide)

By structuring prompts with primary/supporting/grounding content and explicit cues, you consistently get higher-quality, more actionable outputs from AI models.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/d00afd7f-6d8d-4be7-a3f1-5523f484ea72/lesson/8100d689-87ec-4191-851a-9f8f76d1f859" />
</CardGroup>
