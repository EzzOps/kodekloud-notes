# Single generation request
result = ollama.generate(
    model='gemma3:latest',
    prompt='Tell me a funny joke about Python'
)

# The client returns a dictionary. Print the textual response.
print(result['response'])
```

Run it:

```bash theme={null}
(venv) jeremy@LEGION:/mnt/c/Users/jerem/Projects/ollama-test$ python main.py
Okay, here's a joke about Python:
Why did the Python cross the road?
... To get to the other side... and then try to `import` it!
```

Why use this pattern? The `generate` call is ideal for one-shot prompts — you send a single prompt and receive a single response, useful for tasks like summarization, code generation, and short Q\&A.

## 4) Context-aware chat loop

For multi-turn conversations you should accumulate the message history and use the chat API. Save this as `chat_main.py` (or merge into `main.py`).

```python theme={null}
import ollama

messages = []

while True:
    user_input = input("You: ")
    # Exit on '/exit' or an empty line
    if user_input.strip().lower() in ('/exit', ''):
        print("Exiting chat.")
        break

    # Append the user's message
    messages.append({'role': 'user', 'content': user_input})

    # Send the conversation history to the Ollama chat endpoint
    response = ollama.chat(model='gemma3:latest', messages=messages)

    # Extract assistant content and display it
    assistant_content = response['message']['content']
    print("Bot:", assistant_content)

    # Keep the assistant message in the history for context
    messages.append({'role': 'assistant', 'content': assistant_content})
```

Example usage:

* Type a prompt when asked (for example: "Tell me a funny joke about Python").
* Continue the conversation; the `messages` list preserves the full exchange so the model can reference earlier turns.
* Enter `/exit` or press Enter on an empty line to quit.

Why this structure?

* The `generate` example demonstrates single-shot usage.
* The chat loop shows how to preserve conversational context by appending `{'role': 'user'|'assistant', 'content': ...}` entries to a `messages` list and sending that full history each time.

## File summary

| Filename       | Purpose                                                             |
| -------------- | ------------------------------------------------------------------- |
| `main.py`      | Single-shot generation example using `ollama.generate()`            |
| `chat_main.py` | Multi-turn chat example using `ollama.chat()` and a `messages` list |

<Callout icon="warning">
  Make sure your Ollama server is running locally before executing these scripts. The Python client communicates with the background Ollama process via HTTP and will fail if the server is not available. Also replace `gemma3:latest` with the model name you have installed.
</Callout>

Final reminders

* Keep your virtual environment activated while installing and running the scripts.
* Monitor available models with `ollama list` and update the `model=` parameter accordingly.
* Use the chat pattern to maintain conversational state when building bots, assistants, or multi-turn tools.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/18c192ac-9730-42f7-9dbf-6c67f9ceeb61/lesson/6d22a31f-589a-4a33-958b-420ee5bdcc6f" />
</CardGroup>


# RAG Architecture Deep Dive

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Introduction/RAG-Architecture-Deep-Dive/page

A practical deep dive into Retrieval-Augmented Generation covering architecture, ingestion, retrieval, generation, challenges, and production patterns for building evidence-grounded LLM systems.

This article provides a focused, practical deep dive into Retrieval-Augmented Generation (RAG): why it matters, how it works, and the production tradeoffs and patterns you should know when building RAG systems.

## Why RAG?

RAG solves key limitations of standalone large language models (LLMs) and conventional search:

* Knowledge cutoff: LLMs are trained on data up to a fixed date and can’t natively access newer information.
* Hallucination risk: Without grounding, LLMs may produce fluent but incorrect answers.
* No private data access: Public LLMs don’t access internal documents unless those documents are ingested.
* Static knowledge base: LLMs can’t incorporate real-time updates or dynamic data without an external retrieval step.

<Frame>
  <img alt="The image highlights reasons for using RAG, mentioning knowledge cutoff dates, hallucination risk, lack of private data access, and a static knowledge base." />
</Frame>

Traditional LLMs are powerful but limited by training data and the lack of live access to private or current information.

<Frame>
  <img alt="The image presents a flowchart discussing the limitations of traditional language models, highlighting issues like fixed cutoff and no access to internal data, leading to confident but incorrect answers to queries beyond the model's knowledge." />
</Frame>

When an LLM answers beyond its knowledge, it can produce confident but incorrect answers (hallucinations). RAG reduces this risk by combining document retrieval with grounded generation.

## RAG mental model

Think of RAG as a research assistant that:

1. Finds the most relevant source material.
2. Extracts the most useful excerpts.
3. Writes an answer that is explicitly grounded in that evidence.

Core phases:

* Retrieval: Search your knowledge base using semantic similarity (often in combination with keywords).
* Augmentation: Select, rank, and assemble the most relevant document chunks.
* Generation: The LLM composes answers conditioned on the retrieved evidence.

<Frame>
  <img alt="The image is a diagram titled &#x22;RAG Mental Model: Your AI Research Assistant,&#x22; highlighting the features &#x22;Impeccable Memory&#x22; and &#x22;Machine Speed.&#x22;" />
</Frame>

## RAG pipeline — high level

At a high level, RAG is composed of three systems that work together:

| Component         | Purpose                                                                       | Example technologies                      |
| ----------------- | ----------------------------------------------------------------------------- | ----------------------------------------- |
| Knowledge base    | Stores documents, logs, configs as semantic representations (embeddings)      | `S3`, `Google Drive`, `DB`, `PDFs`        |
| Retrieval system  | Performs similarity search over embeddings to find relevant chunks            | `FAISS`, `Pinecone`, `Weaviate`, `Milvus` |
| Generation system | LLM consumes the user query + retrieved context to produce grounded responses | `OpenAI`, `Anthropic`, self-hosted LLMs   |

<Frame>
  <img alt="The image illustrates &#x22;The RAG Pipeline,&#x22; consisting of three components: Knowledge Base, Retrieval System, and Generation System, with the Knowledge Base described as storing semantic document representations." />
</Frame>

## Document ingestion and vector storage

Ingestion steps (practical):

1. Chunk documents into smaller passages (chunking).
2. Convert each chunk to an embedding vector that captures semantic meaning.
3. Store embeddings and metadata in a vector database for fast similarity search.

Chunking tradeoffs:

* Smaller chunks: higher retrieval precision, less surrounding context.
* Larger chunks: more context, but retrieval may be less focused if only a piece is relevant.

<Callout icon="lightbulb">
  Balance chunk size to suit your use case. For conversational QA, a few paragraphs per chunk often work; for step-by-step procedures, preserve steps with slightly larger chunks.
</Callout>

## Query processing and similarity search

Basic flow:

* Convert user query into a query embedding.
* Perform similarity search between query embedding and stored embeddings (commonly cosine similarity).
* Return the top-K most similar chunks as candidate context.

<Frame>
  <img alt="The image illustrates a query retrieval process where a user asks about Q3 sales performance, and the system responds with sales data, outlining steps such as query embedding, similarity search, and top K results." />
</Frame>

Example pseudocode (conceptual):

```python theme={null}
