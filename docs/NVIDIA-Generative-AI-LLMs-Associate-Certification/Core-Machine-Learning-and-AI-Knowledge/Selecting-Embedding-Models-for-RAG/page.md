# Selecting Embedding Models for RAG

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Selecting-Embedding-Models-for-RAG/page

Selecting embedding models for RAG prioritizing semantic similarity to improve retrieval, with notes on tradeoffs and evaluation

Question 4.

A developer is selecting an embedding model for a [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) system.

Which of the following considerations is most important when choosing between different embedding models?

* The model's ability to capture semantic similarity between texts
* The number of parameters in the model
* Whether the model was trained on multiple languages
* The model's ability to generate natural language

Correct answer: the model's ability to capture semantic similarity between texts.

For RAG systems, the embedding model’s primary responsibility is to map text into vectors so that semantically related pieces of text are close in vector space. Retrieval then depends on similarity measures such as [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) or the [dot product](https://en.wikipedia.org/wiki/Dot_product) between a query embedding and stored document embeddings to surface relevant documents.

<Frame>
  <img alt="The image presents a question about choosing an embedding model for a RAG system, emphasizing the importance of capturing semantic similarity between texts as the key consideration." />
</Frame>

Why semantic similarity is primary

* Retrieval quality directly depends on how well embeddings encode meaning. If semantically similar texts are not close in embedding space, the retriever will systematically miss relevant documents regardless of model size or other properties.
* Similarity measures like cosine similarity and dot product assume a geometrically meaningful embedding space; the better the semantic geometry, the better retrieval performance.

<Callout icon="lightbulb">
  Focus your embedding evaluation on semantic retrieval metrics and nearest-neighbor behavior. Human judgments, retrieval metrics (recall\@k, MRR), and end-to-end RAG evaluations are more informative than raw model size or generation benchmarks.
</Callout>

Secondary considerations (when semantic quality is comparable)

* Multilingual support: Choose embeddings trained on diverse languages if your corpus or users are multilingual.
* Latency and cost: Larger models often yield higher-quality embeddings but at greater compute cost and higher latency. Balance embedding quality with operational constraints.
* Domain adaptation: Fine-tuning or contrastive training on domain-specific text can significantly improve retrieval for specialized corpora.
* Embedding dimensionality and index compatibility: Higher-dimensional embeddings may improve discrimination but increase storage and index complexity.

Comparison table: considerations and recommendations

| Consideration                         | Impact on RAG                           | Recommendation                                                                                              |
| ------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Semantic similarity quality           | Directly determines retrieval relevance | Prioritize models with empirically proven semantic retrieval performance (evaluate with recall\@k, MRR)     |
| Multilingual support                  | Enables cross-language retrieval        | Use multilingual embeddings if corpus or queries span languages                                             |
| Model size & latency                  | Affects throughput and cost             | Choose smallest model that meets retrieval quality requirements; benchmark latency in production conditions |
| Embedding dimensionality & index type | Affects storage, search speed, accuracy | Select dimension and index (e.g., HNSW) compatible with your vector DB (FAISS, Milvus)                      |
| Generation capability                 | Not needed for retrieval                | Leave generation to the downstream reader/generator model in the RAG pipeline                               |

Practical factors and tooling

* Vector stores and indexing: Ensure compatibility with your vector database and index type: [FAISS](https://github.com/facebookresearch/faiss), [Milvus](https://milvus.io/), and indexes like [HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world_graph).
* Evaluation: Benchmark embeddings with retrieval metrics such as `recall@k`, [mean reciprocal rank (MRR)](https://en.wikipedia.org/wiki/Mean_reciprocal_rank), and end-to-end RAG accuracy. Empirical tests on your domain are essential.
* Fine-tuning: If off-the-shelf embeddings underperform on your domain, consider contrastive fine-tuning or supervised embedding training.

<Callout icon="warning">
  Don’t assume larger or generative-capable models automatically make better embedding models. Focus on semantic retrieval performance and measure it in realistic scenarios before settling on a model.
</Callout>

Takeaway

* Prioritize embedding models that produce strong semantic similarity judgments for your specific domain and queries. After semantic quality, balance multilingual needs, latency/cost, and index/storage constraints. Finally, validate choices with targeted retrieval metrics and end-to-end RAG tests.

Links and references

* [Retrieval-Augmented Generation (RAG) — Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [Cosine similarity — Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Dot product — Wikipedia](https://en.wikipedia.org/wiki/Dot_product)
* [FAISS GitHub](https://github.com/facebookresearch/faiss)
* [Milvus](https://milvus.io/)
* [HNSW — Wikipedia](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world_graph)
* [Recall (information retrieval) — Wikipedia](https://en.wikipedia.org/wiki/Recall_\(information_retrieval\))
* [Mean reciprocal rank (MRR) — Wikipedia](https://en.wikipedia.org/wiki/Mean_reciprocal_rank)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/875d98e8-3b09-4f35-b877-2758b84443ca/lesson/2df7dd9b-70b7-40a5-843a-588e2600ab8f" />
</CardGroup>
