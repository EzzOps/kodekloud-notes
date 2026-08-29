# Synchronous invocation (waits for the full response)
result = chain.invoke({"question": "Tell me about The Godfather Movie"})
print(result)
```

When to use `invoke`:

* Simpler workflows where latency is acceptable.
* When you must process the final, fully formed output atomically.
* Integrations that cannot easily handle partial/streamed responses.

## Streaming execution (stream)

Streaming yields text chunks progressively as the LLM generates tokens. This is ideal for live typing effects, improving perceived responsiveness, or updating a UI in real time. Note that streaming requires an LLM client that supports it (some clients need `streaming=True`).

```python theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.
Answer the following question: {question}
"""
)

# Enable streaming support if your client requires it
llm = ChatOpenAI(streaming=True)
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# Iterate over chunks as they arrive from the LLM
for chunk in chain.stream({"question": "Tell me about The Godfather Movie"}):
    print(chunk)
```

Best practices for streaming:

* Handle partial tokens and join chunks carefully if you need complete sentences.
* Provide visual indicators in your UI for streaming states (e.g., loading spinner, "typing…" animation).
* Fall back to `invoke` when streaming is not supported by the LLM client.

## Parallel / batch execution (batch)

Batch mode executes the same chain for multiple inputs, potentially in parallel (implementation-dependent). It returns a list of results matching the order of inputs.

```python theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.
Answer the following question: {question}
"""
)

llm = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# Prepare multiple inputs for batch processing
inputs = [
    {"question": "Tell me about The Godfather Movie"},
    {"question": "Give a short summary of 1984 by George Orwell"}
]

# Execute the chain in batch and print each result
results = chain.batch(inputs)
for r in results:
    print(r)
```

When to choose `batch`:

* High-throughput scenarios where you need to process many prompts.
* Workloads that can tolerate increased concurrency and API calls.
* Bulk processing where responses do not depend on each other.

<Callout icon="lightbulb">
  Streaming improves perceived responsiveness and enables typing-style UIs. Confirm your LLM client supports streaming and remember that chunks may contain partial words or tokens — plan to reassemble or display incremental content safely.
</Callout>

<Callout icon="warning">
  Batch/parallel execution increases concurrency and API usage. Monitor rate limits, quotas, and cost when using batch mode, and apply throttling or retries as needed.
</Callout>

## Quick comparison

| Execution Mode | Behavior                                                     | Best for                                                                                    |
| -------------: | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
|         invoke | Blocking call that returns the final output                  | Simple synchronous calls, transactional responses                                           |
|         stream | Yields incremental token/chunk updates                       | Live typing UI, low-latency perceived response                                              |
|          batch | Runs the chain over multiple inputs, returns list of outputs | High-throughput / bulk processing (`e.g.` `[{ "question": "..." }, { "question": "..." }]`) |

## Summary

* Use `invoke` for straightforward synchronous calls that return the final output.
* Use `stream` to receive incremental chunks during generation to enable live or typing UIs.
* Use `batch` to process multiple inputs at once and maximize throughput.

## Links and References

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [OpenAI API — Responses & Streaming](https://platform.openai.com/docs/guides/response-streaming)
* [LangChain — Chat Models & Streaming Patterns](https://github.com/langchain-ai/langchain)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/754457c5-1386-422b-98ad-3342dfc6aab3/lesson/73409062-5bca-4e9b-86cf-48d797f1050b" />
</CardGroup>


# LCEL Demo 3

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-3/page

Explains batching inputs for LangChain chains to run multiple prompt-variable dictionaries concurrently, boosting throughput while preserving input order and addressing concurrency limits and error handling.

This lesson explains batching: sending multiple inputs to a chain at once so the runtime can execute them concurrently. It builds on synchronous chain invocation and streaming output, and demonstrates how to provide a list of input dictionaries where each dictionary supplies the prompt variables for one invocation (for example, the `question` key used by the prompt).

Batching is useful for throughput optimization: the runtime unpacks your list and invokes the chain for each item (typically in parallel), returning a list of outputs that maintain the input order.

## How batching works (high level)

* Provide a list of dictionaries. Each dictionary maps prompt variable names to values (e.g., `{"question": "..."}`).
* Call `chain.batch(...)`. The runtime executes the chain once per dictionary in the list.
* The return value is a list of outputs in the same order as the input list.
* The runtime usually parallelizes these invocations, so large batches can complete in roughly the same time as a single invocation (subject to concurrency limits, API rate limits, and client/runtime settings).

## Example: prompt template + LLM + output parser + batch

The example below demonstrates:

1. Creating a chat prompt template that expects a `question` variable.
2. Composing the prompt with an LLM and an output parser.
3. Building a list of input dictionaries.
4. Executing the chain via `chain.batch(...)` to process inputs concurrently.

```python theme={null}
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import ChatOpenAI
