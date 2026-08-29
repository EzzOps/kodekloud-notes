# What Is RAG

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Implement-Retrieval-Augmented-Generation-RAG-with-Azure-OpenAI-Service/What-Is-RAG/page

Describes Retrieval-Augmented Generation, combining LLMs with vectorized external knowledge to generate up-to-date, grounded answers with source citations.

Retrieval-Augmented Generation (RAG) combines large language models (LLMs) with external contextual data sources so that responses are both fluent and grounded in up-to-date information. This lesson uses a simple travel-assistant example to show the end-to-end flow and architecture.

Example scenario:
A user asks: "What are the top 10 places to visit in New York?" The request arrives at an AI application that orchestrates the process:

1. The application queries a contextual data source — typically a vectorized knowledge base of travel guides, web-scraped pages, or documents — to retrieve the most relevant documents.
2. Retrieved documents (or document excerpts) are combined with the user's prompt to form an augmented prompt.
3. The augmented prompt is sent to an LLM (for example, GPT-4 via the [Azure OpenAI Service](https://learn.microsoft.com/azure/cognitive-services/openai/)), which uses both its parametric knowledge and the retrieved, non-parametric context to generate a grounded answer.
4. The application can surface citations or source links from the retrieved documents to improve traceability and factuality.

<Frame>
  <img alt="A diagram titled &#x22;Retrieval-Augmented Generation (RAG)&#x22; showing how an AI app interacts with a vectorized contextual data store and a language model, plus training data, to generate responses. A sample prompt/response on the right illustrates the system giving travel recommendations (top NYC attractions) and citing sources." />
</Frame>

Key concepts shown in the diagram:

* LLM (parametric knowledge): general knowledge learned during pretraining, useful for fluency, reasoning, and broad knowledge.
* Vectorized contextual store (non-parametric knowledge): embeddings-backed index that retrieves up-to-date or domain-specific facts at query time.
* Orchestration layer: handles embedding queries, retrieval, ranking, prompt assembly (prompt + retrieved context), and invoking the LLM.
* Grounding and citations: the final LLM output can include explicit citations from the retrieved documents, increasing trustworthiness.

> **lightbulb** RAG separates a model’s static, pretrained knowledge from dynamic external knowledge stored in a vector database. This modularity lets you update or extend the system’s knowledge by re-indexing or refreshing external documents without retraining the model.

Why use RAG?

* Keeps answers current with external sources.
* Improves factual accuracy by grounding model outputs.
* Enables domain specialization with curated corpora (legal, medical, product manuals).
* Allows scaling: smaller models plus targeted retrieval can match or beat larger models on certain tasks.

Comparison: parametric vs non-parametric knowledge

| Resource Type                 | Role in RAG                                                                  | Example                                              |
| ----------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------- |
| Parametric (LLM)              | Stores general language patterns and world knowledge learned during training | GPT-4 provides fluent summarization and reasoning    |
| Non-parametric (Vector store) | Stores and returns up-to-date, domain-specific documents at query time       | Travel guides, product docs, knowledge base articles |

Typical RAG orchestration (high-level pseudo-code)

```python theme={null}
