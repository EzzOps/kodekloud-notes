# Demo Performing Text Processing and Analysis

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Performing-Text-Processing-and-Analysis/Demo-Performing-Text-Processing-and-Analysis/page

Demo notebook showing LLM-driven text processing tasks such as summarization, sentiment analysis, poetic translation, and text-to-structure conversion, with examples, code snippets, and best practices.

We're starting with a fresh Jupyter notebook to demonstrate common text-processing tasks using a chat-based LLM: summarization, bullets, sentiment analysis, translation, and converting plain text into structured formats. These small utilities show practical patterns for building reproducible prompts and integrating model outputs into downstream workflows.

<Frame>
  <img
    alt="A presentation slide with the centered title &#x22;Demo: Performing Text
Processing and Analysis&#x22; on a white background. A small &#x22;© Copyright
KodeKloud&#x22; notice appears in the
bottom-left."
  />
</Frame>

Overview: tasks and examples

| Task                          | Goal                                               | Example prompt type                    |
| ----------------------------- | -------------------------------------------------- | -------------------------------------- |
| Summarization                 | Produce concise or length-limited summaries        | 500-word summary, bullet points        |
| Sentiment analysis            | Classify text as Positive / Negative / Neutral     | Label customer reviews                 |
| Translation (tone-preserving) | Translate while keeping poetic or rhetorical tone  | French poem → English poetic rendering |
| Format conversion             | Convert semi-structured text to JSON / XML / JSONL | States → structured records            |

Setup

* Load your API key from an environment variable and define a helper that wraps the ChatCompletion API. Keep API keys out of source code and follow your organization’s secret management policies.

<Callout icon="lightbulb">
  Store sensitive credentials (like OPENAI\_API\_KEY) in environment variables or
  a secrets manager. Avoid hard-coding keys in notebooks.
</Callout>

```python theme={null}
