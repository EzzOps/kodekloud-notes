# Overview of Chains

Source: https://notes.kodekloud.com/docs/LangChain/Implementing-Chains/Overview-of-Chains/page

Explains LangChain chain patterns, comparing 'stuff' and retrieval RAG workflows for combining documents, summarization, and choosing combine strategies like map_reduce and refine.

In this lesson we cover how to implement and choose between common chain patterns in LangChain for working with multiple documents and retrieval-augmented generation (RAG) workflows.

We focus on two built-in chain constructs:

* The "stuff" chain
* The "retrieval" chain

These building blocks are central when you need to combine multiple documents, summarize content, or answer questions over large collections.

<Callout icon="lightbulb">
  In this article, "stuff" refers to the approach that formats and injects multiple documents directly into a single prompt, while "retrieval" refers to the pattern that first fetches relevant chunks from a retriever (e.g., a vector store) before combining them for the LLM.
</Callout>

## What is a chain in LangChain?

A chain in LangChain is a pipeline that orchestrates one or more steps (prompts, LLM calls, retrievers, combiners) to produce a final output. Chains make it easier to standardize how you prepare context, call an LLM, and post-process results for tasks like summarization, extraction, and QA.

## 1) Stuff chain (combine by concatenation)

The StuffDocumentsChain (often called the "stuff" combiner) concatenates a list of documents, formats them into a single prompt, and sends that prompt to the LLM in a single call.

When to use:

* The combined size of all documents fits within the LLM’s context window.
* You prefer a straightforward, deterministic single-pass approach (e.g., summarization, extraction).

Advantages:

* Simple and fast: one LLM call with all context.
* Deterministic: model sees all provided content at once, which can help for faithful summarization or extraction.

Limitations:

* Not viable if the total tokens exceed the model's context window.
* Inefficient if many documents are irrelevant to the query.

Example usage:

```python theme={null}
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
