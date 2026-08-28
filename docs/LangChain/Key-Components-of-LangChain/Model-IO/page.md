# Initialize the chat model
llm = ChatOpenAI(temperature=0.0)

# Create an in-memory conversation buffer (short-term memory)
memory = ConversationBufferMemory()

# Create a conversation chain that automatically uses the memory
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

# Interact; memory keeps the conversation context for this session
conversation.predict(input="Hi, I'm Alice.")
conversation.predict(input="What did I tell you my name was?")
```

This pattern is appropriate when you only need memory during an active session. If the process restarts, the in-memory buffer is lost.

## Pattern for long-term memory

For long-term memory use the following pattern:

1. Extract and persist important snippets or facts during interactions to an external store (e.g., `SQLite`, `Redis`, or a vector DB).
2. At the start of a new session (or before answering a query), retrieve the most relevant items from that store.
3. Inject these retrieved items as context (or build a retrieved context) into the prompt so the LLM can use them when generating a response.

This lets memory survive process restarts and scale across multiple users or sessions while keeping the prompt size manageable.

<Callout icon="lightbulb">
  Short-term memory exists only while a session or process runs. To retain information across sessions, persist it externally (for example `SQLite`, `Redis`, or a vector database). Retrieve and include only the most relevant items to fit within the model's context window.
</Callout>

<Callout icon="warning">
  Be mindful of privacy, security, and data retention when storing user data. Persisted memory may contain sensitive information—apply appropriate encryption, access controls, and retention policies.
</Callout>

## Design considerations

When designing memory for your application, consider:

* Token/context limits: Only include the most relevant history to avoid exceeding the model's context window. Use summarization or windowed buffers to limit tokens.
* Relevance and retrieval: Use embeddings and vector retrieval (or similarity search) to find the most useful past items to include in a prompt.
* Privacy and compliance: Avoid storing unnecessary sensitive data. Implement encryption, anonymization, and deletion policies as needed.
* Cost and latency: External retrieval adds latency and cost. Cache frequently-used retrievals and balance recall depth with performance.

## Links and references

* LangChain course: [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)
* Mastering Generative AI with OpenAI: [https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai)
* SQLite: [https://www.sqlite.org/](https://www.sqlite.org/)
* Redis: [https://redis.io/](https://redis.io/)
* Vector databases and retrieval: [https://learn.kodekloud.com/user/courses/vector-database-for-genai](https://learn.kodekloud.com/user/courses/vector-database-for-genai)

These resources will help you choose the right memory pattern and persistence mechanism for your LLM application.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/5bedac05-3eaa-4d0d-9892-e05b80c528fb/lesson/87a18942-f7f0-43fa-a0c4-ceed571b426d" />
</CardGroup>


# Model IO

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Model-IO/page

Explains Model I/O for LLMs, covering prompt templating, output parsing, schema validation and safety for reliable integrations.

Model I/O is the central module that mediates between your application and a large language model (LLM). It has two primary responsibilities:

* Preparing the prompt (input) sent to the model.
* Parsing and validating the model's raw output so your application can safely consume it.

Prompt engineering matters: a short, informal prompt rarely produces consistent, production-grade responses. Well-designed prompts use templates, explicit formatting, and constraints so the model “speaks the same language” as your system—using the syntax, semantics, and conventions that steer the LLM toward the desired output.

<Frame>
  <img alt="The image is a diagram illustrating a process involving a user generating a detailed prompt, which is processed by a model I/O to provide an accurate response via a language model, emphasizing syntax and semantics." />
</Frame>

Typically, an LLM returns plain text. Model I/O converts that text into structured, validated outputs (for example, JSON objects, typed models, or domain-specific schemas) so downstream code can act on results deterministically.

Key responsibilities at a glance:

| Responsibility                 |                                                    Why it matters | Example                                                                      |
| ------------------------------ | ----------------------------------------------------------------: | ---------------------------------------------------------------------------- |
| Prompt templating & formatting |    Produces consistent, high-quality inputs that reduce ambiguity | Use templates with placeholders and explicit instructions: see example below |
| Response parsing & validation  |   Converts free text into structured types and enforces contracts | Parse JSON or apply schema validation (e.g., JSON Schema, Pydantic, Zod)     |
| Safety & constraints           | Limits harmful or out-of-scope outputs and reduces hallucinations | Add guardrails in prompts and validate outputs before use                    |

<Callout icon="lightbulb">
  Model I/O is where most prompt-engineering and output-parsing logic lives. Investing effort here yields more predictable LLM behavior and safer, more maintainable integrations.
</Callout>

Common patterns and examples

* Prompt templates — Use templating to inject variables and to enforce structure (roles, instructions, response format).
* Output formats — Prefer strict, machine-readable formats (JSON, YAML, CSV) when possible and document the schema in the prompt.
* Validation — Run schema validation immediately after parsing to catch and handle malformed or unexpected outputs.

Prompt template example (JavaScript-style template)

```text theme={null}
You are a helpful assistant. Given the following user query, return a JSON object with keys "intent", "entities", and "response". Only output valid JSON.

User query:
"{user_query}"
```

Prompt template example (system + user) — this is commonly used with chat-style LLM APIs:

```text theme={null}
System: You are an assistant that answers in JSON only.

User: Extract the intent and entities from the message and provide a brief response.
Message: "{message}"
```

Output parsing example (Python)

```python theme={null}
