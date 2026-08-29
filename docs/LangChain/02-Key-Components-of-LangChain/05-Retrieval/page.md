# Pseudo-code: call LLM and parse JSON
raw = llm.generate(prompt)
# Expect the LLM to output a JSON string
data = json.loads(raw)
# Validate using Pydantic or JSON Schema
validated = MySchema.parse_obj(data)
```

Output parsing example (TypeScript + Zod)

```ts theme={null}
const result = await llm.call(prompt);
const parsed = JSON.parse(result);
const validated = MyZodSchema.parse(parsed);
```

Best practices

* Always ask the model to produce machine-parseable output (for example, explicitly request JSON).
* Provide an example of the desired response format in the prompt.
* Use structured schema validation libraries (Pydantic, Zod, Ajv) to enforce types and ranges.
* When possible, add sanity checks after parsing (length checks, required fields, enumerations).
* Log both raw LLM outputs and parsed/validated results to help debug parsing issues.

<Callout icon="warning">
  Never trust raw LLM output as authoritative. Always parse and validate outputs before using them in critical systems. Include fallback behavior for malformed or missing fields.
</Callout>

Further reading and references

* LangChain: [https://python.langchain.com/](https://python.langchain.com/) (for prompt templates and utilities)
* OpenAI Prompt Best Practices: [https://platform.openai.com/docs/guides/prompts](https://platform.openai.com/docs/guides/prompts)
* JSON Schema: [https://json-schema.org/](https://json-schema.org/)
* Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
* Zod (TypeScript): [https://github.com/colinhacks/zod](https://github.com/colinhacks/zod)

A dedicated section follows with concrete prompt template examples, formatting strategies, and common output-parsing patterns for this library.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-3eaa-4d0d-9892-e05b80c528fb/lesson/b1501cbe-c6d4-4305-ace8-1bdea97918d0" />
</CardGroup>


# Retrieval

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Retrieval/page

Explains retrieval pipelines for LLMs, covering offline ingestion, embeddings, vector databases, online similarity search, document splitting, metadata and best practices to improve relevant contextual responses.

Retrieval is the next essential building block for production-ready applications that use large language models (LLMs).

Why it matters: LLMs are trained on data up to a fixed cutoff and therefore can’t natively answer questions about documents or events created after that checkpoint. Retrieval bridges this gap by bringing relevant, external context into prompts so an LLM can reason over up-to-date, domain-specific content (PDFs, web pages, APIs, knowledge bases, etc.).

At a high level, a retrieval pipeline separates expensive, offline work from fast, online lookups. This separation reduces latency and cost while improving accuracy and relevance.

A typical retrieval pipeline has two phases:

1. Ingestion (offline / pre-processing)
   * Acquire data from sources: PDFs, XML, APIs, web pages, databases, and more.
   * Clean and transform documents, extract metadata, and split text into passages or chunks that are retrieval-friendly.
   * Convert each passage into a vector embedding using an embedding model (e.g., OpenAI embeddings, Hugging Face models).
   * Store embeddings and metadata in a vector database (e.g., FAISS, Pinecone, Weaviate) that supports efficient similarity search and filters.

2. Retrieval (online, per-request)
   * Encode the user query into an embedding.
   * Perform a nearest-neighbor search against the vector database to find the most relevant passages.
   * Retrieve and rank passages, then inject that context into the prompt sent to the LLM.

<Frame>
  <img alt="The image is a flowchart illustrating a data retrieval process from sources like PDF, XML, and APIs, which are loaded, transformed, embedded as numerical vectors, and stored in a vector database." />
</Frame>

Because ingestion is decoupled from runtime retrieval, you avoid re-querying raw sources for every prompt. This yields lower latency, reduced cost, and more consistent, reproducible results. Invest most engineering effort in the ingestion and indexing steps (document splitting, embedding selection, vector DB configuration, metadata design, and update strategies)—these determine retrieval relevance and downstream LLM quality.

Table: Retrieval pipeline phases at a glance

| Phase               | Purpose                                               | Key steps & common tools                                                                                                                                                |
| ------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ingestion (offline) | Prepare source data for efficient search              | Acquire sources; clean & split documents; enrich metadata; embed passages. Tools: `pdfminer`, `BeautifulSoup`, OpenAI/Hugging Face embeddings, FAISS/Pinecone/Weaviate. |
| Retrieval (online)  | Find and inject the most relevant context for a query | Embed query; run similarity search; retrieve & rank passages; construct prompt. Tools/APIs: vector DB query APIs, LLM prompt templates, filtering by metadata.          |

Best practices

* Document splitting: Use semantic-aware chunking (sliding windows, section-aware splits) so passages preserve complete facts and context.
* Embedding selection: Match the embedding model’s capabilities to your domain and query types. Re-embed only when necessary (e.g., model upgrades, significant content changes).
* Metadata design: Store document identifiers, section headings, source timestamps, and any domain-specific tags to enable filtering and provenance.
* Vector DB configuration: Tune index type, distance metric, and recall/latency trade-offs for your expected query patterns.
* Update strategy: Combine batch re-indexing with incremental updates for new or changed documents to keep latency and cost manageable.

Practical tips for better retrieval and LLM responses

* Use passage-level retrieval rather than whole-document retrieval to keep the injected context concise and focused.
* Apply simple reranking (BM25 or an LLM-based reranker) after vector similarity to improve precision.
* Include provenance and source links in the final LLM response so users can verify facts.
* Monitor retrieval quality via relevance metrics and user feedback loops, then iterate on splitting and embedding choices.

<Callout icon="lightbulb">
  Design the ingestion and update processes (batch updates, incremental indexes, and re-embedding strategies) carefully. Good document splitting, metadata, and embedding selection significantly improve retrieval relevance and downstream LLM responses.
</Callout>

Links and references

* [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
* [FAISS (Facebook AI Similarity Search)](https://github.com/facebookresearch/faiss)
* [Pinecone vector database](https://www.pinecone.io/)
* [Weaviate vector search engine](https://weaviate.io/)
* [Kubernetes Documentation — for deploying retrieval infra](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-3eaa-4d0d-9892-e05b80c528fb/lesson/82db88eb-654f-49a7-a8cb-ac4e95238331" />
</CardGroup>
