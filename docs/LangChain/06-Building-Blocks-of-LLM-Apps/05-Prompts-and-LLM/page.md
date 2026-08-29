# Suppose the LLM returned this ISO-8601 date string:
llm_date_str = "2026-07-16"

# Convert to a date object and compute difference
date_from_llm = date.fromisoformat(llm_date_str)
today = date.today()

delta = today - date_from_llm
print(f"Days between: {abs(delta.days)}")
```

Notes for Python example:

* Prefer `date.fromisoformat()` for `YYYY-MM-DD`. It raises `ValueError` for invalid formats, which you should catch and handle.
* For timestamps with time and timezone, use `datetime.fromisoformat()` or a robust parser like `dateutil.parser.isoparse()`.

Example: parse a date string in JavaScript and compute days difference

```javascript theme={null}
const llmDateStr = "2026-07-16";
// Parse as UTC midnight to avoid local timezone interpretation of "YYYY-MM-DD"
const dateFromLLM = new Date(llmDateStr + "T00:00:00Z");
const today = new Date();

const msPerDay = 24 * 60 * 60 * 1000;
const diffDays = Math.abs(Math.round((today - dateFromLLM) / msPerDay));
console.log(`Days between: ${diffDays}`);
```

Notes for JavaScript example:

* Appending `"T00:00:00Z"` forces UTC parsing for `YYYY-MM-DD` inputs and avoids off-by-one-day errors from local timezone offsets.
* For more complex datetime handling, consider a library like `luxon` or `date-fns`.

Key practices for reliably consuming LLM output

| Area           | Recommendation                                                           | Example / Tools                                           |
| -------------- | ------------------------------------------------------------------------ | --------------------------------------------------------- |
| Output schema  | Request a strict format (e.g., `JSON` with explicit keys)                | Prompt: `Return {"date": "YYYY-MM-DD", "reason": "..."} ` |
| Validation     | Use schema validation and type checks                                    | `jsonschema`, `pydantic`, `zod`                           |
| Date parsing   | Prefer ISO-8601; specify exact format in prompt                          | `date.fromisoformat()`, `dateutil`, `luxon`               |
| Error handling | Provide safe fallbacks and clear error messages                          | Retry, ask the model to reformat, or reject input         |
| Security       | Never trust unvalidated LLM output in security- or safety-critical flows | Sanitize before executing or storing                      |

<Callout icon="warning">
  Do not execute or evaluate code, commands, or markup produced by an LLM without strict validation. Treat LLM output as untrusted data: validate structure, types, ranges, and content before use.
</Callout>

Example prompt patterns you can use to force structured output

* Minimal JSON schema prompt:
  ```{"date":"2026-07-16","summary":"No text provided to analyze; awaiting input."} theme={null}
  Return a JSON object with keys: "date" (YYYY-MM-DD), "summary" (short string).
  ```
* JSON schema with validation hints:
  ```{"date":"2026-07-16", "status":"pending"} theme={null}
  Return JSON: {"date":"YYYY-MM-DD", "status":"one of [approved, denied, pending]"}
  ```

References and further reading

* JSON Schema: [https://json-schema.org/](https://json-schema.org/)
* Python date handling (`datetime`): [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
* ISO 8601 date format overview: [https://en.wikipedia.org/wiki/ISO\_8601](https://en.wikipedia.org/wiki/ISO_8601)
* JavaScript Date pitfalls and timezone handling: [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global\_Objects/Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)

By specifying explicit output formats, validating responses, and normalizing values, you make LLM-driven applications more robust, predictable, and secure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-9de9-4865-aabf-bc71786440b2/lesson/cf17e488-e86d-494b-b410-6e89b4f47212" />
</CardGroup>


# Prompts and LLM

Source: https://notes.kodekloud.com/docs/LangChain/Building-Blocks-of-LLM-Apps/Prompts-and-LLM/page

Guide to prompt engineering and how prompts interact with large language models, covering design elements, best practices, limitations, and evaluation.

A prompt is the instruction or input you give a large language model (LLM) to get a desired response. It defines both the syntax and semantics of the request: what the model should do, what context to consider, and any constraints on the output. Well-crafted prompts help the model understand intent and produce responses that are relevant, accurate, and coherent.

Prompts can be used in many interaction styles:

* Single-turn Q\&A (one input, one output).
* Completion tasks (continue a partial text).
* Multi-turn conversations (iteratively refining requests and replies).

The discipline of designing these inputs—choosing the right words, structure, context, and constraints—is called prompt engineering. This document covers the essentials of prompt engineering and how it relates to LLMs, without diving into advanced techniques.

<Frame>
  <img alt="The image is a diagram titled &#x22;Prompt Engineering&#x22; showing a prompt icon with an explanation: &#x22;Instruction or language the LLM can understand.&#x22;" />
</Frame>

Prompt design: key elements

* Instruction: A clear directive of the desired task (e.g., "Summarize the following report in two paragraphs.").
* Context: Relevant information, documents, or examples the model should use.
* Constraints: Output format, length limits, style, or safety rules (e.g., JSON output only).
* Demonstrations: Few-shot examples showing input → desired output (helps when you need specific structure).
* Role or persona: Framing the model as an expert or role (e.g., "You are a senior data scientist.").

Table — Prompt elements and examples

| Element            | Purpose                   | Example                                             |
| ------------------ | ------------------------- | --------------------------------------------------- |
| Instruction        | Directs the task          | `Translate the text to French.`                     |
| Context            | Provides supporting data  | `Article: "..."`                                    |
| Constraints        | Enforces format or limits | `Return a JSON object with keys: summary, keywords` |
| Example (few-shot) | Shows desired mapping     | `Input: "Bug report" → Output: "5-line summary"`    |
| Role               | Provides tone/persona     | `You are an expert UX writer.`                      |

<Callout icon="lightbulb">
  Clear, concise prompts with explicit output constraints (format, examples, length) consistently produce more reliable model responses. Use few-shot examples when you need a strict or unusual output structure.
</Callout>

Crafting the right prompt matters: small changes in wording, ordering, or context can significantly affect the model’s output quality. After defining a prompt, the next core component is the LLM itself.

What is an LLM?
An LLM (Large Language Model) is the "brain" of language-based applications. Trained on massive datasets, LLMs can understand, generate, and interact in natural languages. They take prompts as inputs and perform tasks like translation, summarization, question answering, classification, and content generation.

Typical LLM capabilities:

* Text generation and completion
* Summarization and paraphrasing
* Question answering over provided context
* Translation between languages
* Instruction execution (e.g., code generation, data transformation)

<Frame>
  <img alt="The image illustrates the functions of a Large Language Model (LLM) with icons representing abilities such as translating, summarizing, answering, and creating." />
</Frame>

Why LLM outputs can feel human-like
Because of their size and training data, LLMs often produce text that resembles human-authored content. For many tasks, model-generated output can be difficult to distinguish from expert writing and—when prompted carefully—can match or exceed human clarity and completeness on specific tasks.

<Frame>
  <img alt="The image compares text generated by a &#x22;Large Language Model (LLM)&#x22; and an &#x22;Expert Writer&#x22; on the topic of sports, showing near-identical content beneath their respective icons." />
</Frame>

Best practices for prompt engineering

* Start with a clear instruction and measurable constraints (e.g., "Produce 3 bullet points").
* Provide context/contextual documents for factual tasks (e.g., relevant paragraphs or data).
* Use few-shot examples when structure matters.
* Specify format explicitly (e.g., JSON, Markdown, CSV).
* Iterate and test—small wording changes often produce big differences.
* Add safety constraints and content filters when exposing models to public inputs.

Common pitfalls and limitations

* Ambiguous prompts yield inconsistent or vague outputs.
* Models can "hallucinate" confidently—generate plausible but incorrect facts.
* Sensitive or private information should not be passed to third-party models without review.
* Overly long or noisy context can dilute the model’s ability to prioritize relevant facts.

<Callout icon="warning">
  LLMs may produce incorrect or fabricated information. Always validate model outputs against trusted sources for critical or factual tasks, and implement guardrails for sensitive use cases.
</Callout>

Evaluation and iteration

* Evaluate outputs with metrics relevant to your use case (accuracy, BLEU/ROUGE for translation/summarization, human review).
* Use automated checks for format and basic correctness (e.g., schema validation for JSON).
* Maintain a feedback loop: collect user corrections and refine prompts and examples.

Links and references

* [LangChain](https://python.langchain.com/en/latest/) — integration utilities and prompt templates.
* [OpenAI Prompting Guide](https://platform.openai.com/docs/guides) — best practices and examples.
* [Prompt Engineering Resources](https://github.com/dair-ai/Prompt-Engineering-Guide) — community-curated techniques.

Summary
Prompts are the primary interface to LLMs; good prompt engineering combines clear instructions, well-structured context, explicit constraints, and iterative testing. Pair these techniques with rigorous validation to build reliable, useful language applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-9de9-4865-aabf-bc71786440b2/lesson/38ac00b4-6dbd-46dc-981c-4f8e22e3801f" />
</CardGroup>
