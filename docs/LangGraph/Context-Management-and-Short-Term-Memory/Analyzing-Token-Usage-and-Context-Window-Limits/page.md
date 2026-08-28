# Analyzing Token Usage and Context Window Limits

Source: https://notes.kodekloud.com/docs/LangGraph/Context-Management-and-Short-Term-Memory/Analyzing-Token-Usage-and-Context-Window-Limits/page

Explains LLM context window limits, token accumulation risks in conversations and workflows, and strategies for measuring and managing prompt size to prevent truncation and maintain coherence.

Why do token limits matter?

Large language models (LLMs) process text as tokens—subword units that represent parts of words, whole words, or punctuation. When you submit a prompt, it is tokenized and the model attends only to a fixed number of tokens at once. This capacity is called the context window (or token limit) and it matters because the model’s input plus its generated output must both fit inside that window.

<Frame>
  <img alt="The image illustrates the process of converting prompt text into tokens using a tokenizer, which are then processed by a model, highlighting the importance of token limits." />
</Frame>

Each model exposes a maximum token limit for a single request. That limit counts both:

* prompt tokens (system, instructions, user messages, retrieved documents), and
* response tokens (the text the model will generate).

If the combined input and output exceed the model’s window, the API may return an error or the system may silently drop (truncate) important context.

<Frame>
  <img alt="The image explains why token limits matter, showing how a &#x22;Context Window&#x22; defines the maximum token limit, composed of &#x22;Prompt (Input)&#x22; and &#x22;Response (Output).&#x22;" />
</Frame>

What happens as conversation history grows

Every message appended to a running conversation increases token usage. In systems that persist full conversation logs—especially multi-step agents or tool-enabled workflows—the prompt eventually grows toward the model’s limit. Real-world applications (tool outputs, search results, large document retrieval) accelerate this growth.

<Frame>
  <img alt="The image illustrates the importance of token limits with a cartoon robot on a phone screen and a conversation history showing user messages and AI replies." />
</Frame>

Context window: definition and variability

The context window is the hard limit on how many tokens a model can process in one request. For example, if a model supports an 8,000-token window and your prompt already uses 7,000 tokens, there are only about 1,000 tokens left for the model’s response.

Different models provide different window sizes: older/smaller models may allow a few thousand tokens, while newer models can support tens or hundreds of thousands. Even large windows fill up when conversations become long or when external documents are injected into prompts.

<Frame>
  <img alt="The image explains the concept of a &#x22;context window&#x22; in larger models, highlighting that context limits vary by model and show elements like long conversations and external documents contributing to a prompt for the next request." />
</Frame>

Why this matters for graph-based workflows

Graph-based workflows often chain multiple LLM calls, tool outputs, summaries, and user messages. If each result is appended to prompt history without curation, token counts grow quickly and unpredictably.

Treat conversation history as a managed memory system: decide what stays fully visible, what gets summarized, and what can be discarded.

<Frame>
  <img alt="The image compares two workflows: &#x22;LangGraph-Based Workflow&#x22; and &#x22;Prompt History,&#x22; showing a sequence of steps including &#x22;LLM Call,&#x22; &#x22;Tool Output,&#x22; &#x22;Summary,&#x22; and &#x22;User Message.&#x22;" />
</Frame>

Token accumulation and tool outputs

Tokens accumulate faster than many engineering teams expect. Each user message and assistant reply adds tokens; tool outputs such as search results or retrieved document chunks can add hundreds or thousands more. Appending everything without strategy leads to truncation or failures and degrades model responses because critical earlier context may be removed.

Designing memory and context policies prevents loss of intent and inconsistent responses.

<Frame>
  <img alt="The image illustrates a process where conversation history, consisting of user messages and AI replies, is managed by a memory system." />
</Frame>

Measuring token usage

Start by measuring tokens for every component in your prompt:

* system instructions
* examples or few-shot samples
* tool outputs or retrieved documents
* user messages and assistant replies

Token counts rarely equal word counts—tokenization rules vary by model/tokenizer—so always use the tokenizer for your target model (or its official estimator). Many frameworks provide token-estimation utilities; for example, LangChain and other libraries include helpers to approximate token usage.

<Callout icon="lightbulb">
  Tokenizers and token counts differ by model and tokenizer implementation. Always use the same tokenizer as the target model (or its official estimator) to measure tokens accurately.
</Callout>

<Frame>
  <img alt="The image is a diagram titled &#x22;Measuring Token Usage,&#x22; showing a prompt divided into sections: &#x22;System,&#x22; &#x22;Instructions,&#x22; &#x22;Examples,&#x22; and &#x22;User Message,&#x22; highlighting a high token section and suggesting to identify and shorten token-heavy parts." />
</Frame>

Consequences of exceeding the context window

When a prompt exceeds the context window, you can expect one of the following:

| Outcome              | What happens                                                           | Risk                                             |
| -------------------- | ---------------------------------------------------------------------- | ------------------------------------------------ |
| API error            | The request is rejected with an “input too large” error                | No response; you must reduce prompt size         |
| Automatic truncation | The system drops the oldest or least-priority tokens to fit the window | Important context may be lost without notice     |
| Silent degradation   | The assistant responds but lacks necessary prior context               | Misaligned, inconsistent, or incorrect responses |

<Callout icon="warning">
  Automatic truncation can remove crucial context (e.g., user constraints or earlier clarifications). Relying on uncontrolled truncation is risky—implement deliberate context-management policies instead.
</Callout>

<Frame>
  <img alt="The image illustrates what happens when context overflows, showing that earlier context is truncated and important parts may be removed, potentially leading to AI misalignment." />
</Frame>

Intentional handling of overflow

Build a context manager that applies structured strategies to preserve the most relevant information:

* prioritize recent or high-value messages
* compress long histories into concise summaries
* filter out low-importance or redundant content
* store long-term facts separately (a retrieval step can re-insert them as needed)

In graph workflows, insert dedicated nodes that trim, filter, or summarize history before each LLM call so that the prompt stays under the token cap while retaining critical information.

<Frame>
  <img alt="The image illustrates a process flow titled &#x22;What Happens When Context Overflows?&#x22; involving a &#x22;Context Manager&#x22; that uses structured strategies to filter &#x22;Conversation History&#x22; into a &#x22;Selected Context.&#x22;" />
</Frame>

Key takeaways

* Context windows are a hard token limit per request and include both input and output tokens.
* Conversations and agent workflows grow token usage quickly—tool outputs and document retrieval can add large numbers of tokens.
* Without active management, prompts will either exceed model limits and cause errors or be truncated, potentially losing critical context.
* Effective context management preserves crucial information while keeping prompts within token limits via trimming, filtering, and summarization.
* Workflow systems should include nodes that measure tokens and proactively reduce prompt size (e.g., by summarizing or pruning) before invoking an LLM.

<Frame>
  <img alt="The image displays a list of five key takeaways about managing context windows and prompt size in workflows. It highlights strategies such as trimming, filtering, and summarization to stay within token limits and maintain coherent conversations." />
</Frame>

Next steps

In the following lessons we'll cover practical techniques you can implement in LangGraph workflows: automated trimming, token-aware filtering, and incremental summarization patterns that keep agents coherent and scalable.

Further reading and references

* OpenAI: context length and best practices (model docs)
* LangChain: tokenizer and token-count helpers — [https://python.langchain.com/](https://python.langchain.com/)
* Tokenizer libraries and guides (Byte Pair Encoding, GPT tokenizers)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/372c4db3-b58a-4c3e-9e5e-851e67d45b06/lesson/05995ed3-9e58-46e9-bf8c-2ae90b212ba8" />
</CardGroup>
