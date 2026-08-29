# Weaviate Vector Database

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Landscape/Weaviate-Vector-Database/page

Overview of Weaviate, an open source vector database offering hybrid semantic and keyword search, multimodal support, modular embedding integrations, and self hosted or managed deployment options

Welcome back. In this lesson we introduce Weaviate — an open-source vector database optimized for semantic (vector) search, multimodal data, and hybrid ranking.

Weaviate is available under the BSD-3-Clause license, which allows you to run, modify, and redistribute it — including in commercial projects. In addition to the self-hosted distribution, Weaviate Cloud Service (WCS) provides a managed, serverless option if you prefer a hosted experience with minimal operations.

Core capabilities

| Feature               | What it does                                                                              | Example / Benefit                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Hybrid search         | Combines lexical (keyword) and semantic (vector) search into a single ranked result set   | Return exact matches while surfacing semantically similar items for more relevant results |
| Multimodal support    | Stores and searches text, images, audio, and structured data in a unified schema          | Build search across product catalogs, documentation, and images                           |
| Real-time indexing    | Near real-time reflection of inserts, updates, and deletes without long batch re-indexing | Fresh search results immediately after data changes                                       |
| Modular vectorization | Pluggable embedding/vectorizer modules (hosted or external)                               | Use OpenAI, Cohere, Hugging Face, or your own models for embeddings                       |

> **lightbulb** Weaviate's modular modules let you experiment with different embedding providers and models, preventing vendor lock‑in and enabling custom model integration.

How hybrid search works

When you submit a query, Weaviate executes both a keyword-style (lexical) search and a vector (semantic) similarity search. It then merges results using a ranking fusion strategy to produce a single, ranked list that balances exact term matches with conceptual similarity. This hybrid approach is especially valuable when you need results that respect both precise terminology and broader meaning.

Real-world usage

Weaviate is commonly used to power semantic search and knowledge retrieval systems. For example:

* Tech-directory or marketplace platforms use Weaviate to let users find conceptually similar tools even when the query terms don't exactly match catalog entries.
* Documentation assistants and internal knowledge bases combine keyword search for specific terms with vector search to find contextually relevant passages and related topics.

Deployment options

| Deployment Model | Description                                                                                                   | When to use                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Self-hosted      | Deploy with Docker, Docker Compose, or Kubernetes (Helm). Full control over configuration and data residency. | Security-sensitive environments, custom infra, compliance requirements |
| Managed (WCS)    | Weaviate Cloud Service provides a managed, serverless experience                                              | Rapid onboarding, minimal ops, or when you prefer a hosted solution    |

Who is Weaviate for?

Weaviate is a strong choice if you need:

* An open-source, extensible vector database with hybrid search and multimodal capabilities.
* Flexibility to self-host for full infrastructure and data control.
* A managed cloud option (WCS) for quick deployment without heavy operational overhead.
* Pluggable embedding modules so you can use hosted providers or integrate your own models.

<Frame>
  <img alt="The image is an infographic detailing the features and target users of Weaviate, an open-source vector database for semantic search, highlighting its core features, hybrid search pipeline, and deployment flexibility." />
</Frame>

Getting started recommendations

* Evaluate locally: Start with the open-source distribution to prototype on your own infrastructure and validate your schema, embedding pipeline, and query patterns.
* Scale or simplify ops: If you prefer a managed experience, migrate to Weaviate Cloud Service (WCS) to offload operational tasks.
* Choose a vectorizer: Test multiple embedding providers or models (OpenAI, Cohere, Hugging Face, or custom modules) to find the best trade-off for accuracy, cost, and latency.

Alternatives and comparison

Milvus is another popular open-source vector database. Compare both solutions on:

* Performance and scale characteristics
* Supported embedding integrations and modules
* Operational complexity (self-hosted vs managed options)
* Feature set for multimodal or hybrid search

Links and references

* Weaviate: [https://weaviate.io](https://weaviate.io)
* Weaviate Cloud Service (WCS): [https://weaviate.io/wcs](https://weaviate.io/wcs)
* OpenAI: [https://openai.com](https://openai.com)
* Cohere: [https://cohere.ai](https://cohere.ai)
* Hugging Face: [https://huggingface.co](https://huggingface.co)

That is it for this lesson on Weaviate.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/4fee20e9-5def-4971-b7a9-9363aaeb73c2/lesson/24250c52-b4d0-4f6f-949d-72bd1d8c4164)
