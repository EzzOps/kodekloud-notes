# Prompt template expects a variable named `question`
prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant.
    Answer the following question: {question}
    """
)

llm = ChatOpenAI()
output_parser = StrOutputParser()

# Compose the chain
chain = prompt | llm | output_parser

# A list of input dictionaries; each dict maps the prompt variable `question`
questions = [
    {"question": "Tell me about The Godfather Movie"},
    {"question": "Tell me about Avatar Movie"}
]

# Batch execution: the runtime will unpack the list and execute the chain for each item,
# typically in parallel (concurrency settings may depend on the runtime and client).
response = chain.batch(questions)

# `response` is a list where each element corresponds to one input in `questions`
print(response[0])  # Answer for the first question
print(response[1])  # Answer for the second question
```

<Callout icon="lightbulb">
  Ensure each element in the batch is a dictionary whose keys exactly match the prompt template variable names (for example, use `{"question": "..."}` if the template refers to `{question}`).
</Callout>

## Key points (quick reference)

| Concept           | Details                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| Input format      | A list of dictionaries, e.g. `[{ "question": "..." }, { "question": "..." }]`                                     |
| Invocation method | `chain.batch(inputs_list)`                                                                                        |
| Return type       | A list of outputs aligned with input order                                                                        |
| Behavior          | Runtime typically parallelizes invocations; actual concurrency depends on runtime/client settings and rate limits |

## Measuring performance: single vs batched runs

To compare single synchronous execution time versus batched execution time, measure wall-clock time for both approaches. The snippet below runs each input individually (synchronously) and then runs the same inputs via `chain.batch(...)`.

```python theme={null}
import time

# Prepare inputs
questions = [
    {"question": "Tell me about The Godfather Movie"},
    {"question": "Tell me about Avatar Movie"}
]

# Single synchronous runs (run each input individually)
start = time.perf_counter()
single_responses = [chain.run(q) for q in [d["question"] for d in questions]]
single_elapsed = time.perf_counter() - start

# Batched run
start = time.perf_counter()
batch_response = chain.batch(questions)
batch_elapsed = time.perf_counter() - start

print(f"Single-run total time: {single_elapsed:.2f}s")
print(f"Batch-run total time:  {batch_elapsed:.2f}s")
```

Note: Depending on the chain API in your environment, you may pass single-run inputs as dictionaries (e.g., `chain.run({"question": "..."})`) or directly as a string when the chain accepts a single positional argument. Use the form that matches your LangChain runtime version.

<Callout icon="warning">
  Batching and concurrency increase throughput but also increase parallel API usage. Be mindful of rate limits, concurrency caps, costs, and downstream system limits when issuing large batches.
</Callout>

## Practical considerations and tips

* Validate input keys: confirm that each dictionary includes exactly the keys referenced by the prompt template.
* Batch size: tune batch sizes to balance latency, throughput, and rate limits.
* Error handling: decide how to handle per-item failures (e.g., retries, partial failures, logging). The runtime may surface errors per-item or for the whole batch depending on implementation.
* Idempotency & costs: repeated or retried batches can increase cost—track requests and consider idempotency keys if supported.

## Summary

Batching with `chain.batch(...)` lets you send multiple prompt-variable dictionaries at once so the runtime can execute them in parallel (subject to concurrency and rate limits). It returns a list of outputs in the same order as the inputs. Use batching to dramatically improve throughput when running many similar invocations.

Further topics you may explore: runnable pass-through, more advanced LCEL concepts, and runtime-specific concurrency configuration.

## Links and references

* [LangChain Documentation](https://langchain.com/docs/)
* [OpenAI API](https://platform.openai.com/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-1386-422b-98ad-3342dfc6aab3/lesson/8dffe6ae-3a79-440a-a04c-7397040ebc9a" />
</CardGroup>


# LCEL Demo 4

Source: https://notes.kodekloud.com/docs/LangChain/Introduction-to-LCEL/LCEL-Demo-4/page

Explains LCEL RunnablePassthrough usage to forward inputs or inject and compute runtime keys in LangChain pipelines with examples and best practices

As LCEL (LangChain Expression Language) pipelines grow, you frequently need to pass values through unchanged or inject/transform inputs at specific points. `RunnablePassthrough` is the LCEL primitive for this: it can act as a transparent pipe that forwards data unchanged or as an injector that adds/overrides keys in the runtime input.

This document provides concise, corrected examples that illustrate the common patterns for using `RunnablePassthrough`, plus guidance and best practices.

## Overview

* Purpose: Pass through input unchanged, or inject/modify runtime keys.
* Typical uses: preserve existing call signatures, insert context/configuration, or compute values before downstream runnables.
* Works well inside LCEL chains built with prompts, LLMs, and parsers.

## Basic prompt -> LLM -> output parser chain

Example showing a simple chain: Prompt → LLM → Output Parser.

```python theme={null}
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant on {topic}.
Answer the following question: {question}
""")

llm = ChatOpenAI()
output_parser = StrOutputParser()
