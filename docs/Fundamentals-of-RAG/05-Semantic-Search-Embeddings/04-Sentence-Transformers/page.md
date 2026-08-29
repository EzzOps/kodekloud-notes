# Sentence Transformers

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Sentence-Transformers/page

Explains Sentence Transformers that convert sentences into fixed-length semantic vectors enabling semantic search, efficient retrieval, and integration with retrieval-augmented generation.

In this lesson we explain Sentence Transformers and how they convert text into meaning vectors (embeddings) for semantic search and retrieval.

Start with two sentences that express the same idea:

* "The cat sat on the mat."
* "A feline rested on the rug."

On the surface these use different words, but semantically they’re equivalent: mat ↔ rug, cat ↔ feline, sat ↔ rested. Simple keyword or bag‑of‑words search would treat these as very different strings because token overlap is small. Sentence Transformers map entire sentences to fixed-length vectors so semantically similar sentences lie close together in vector space.

<Frame>
  <img alt="The image illustrates two sentences with the same meaning using different words: &#x22;cat sat mat&#x22; and &#x22;feline rested rug.&#x22; It highlights that keyword searches may not recognize their similarity." />
</Frame>

Instead of matching exact tokens, Sentence Transformers represent meaning as numerical vectors. This enables search by meaning — semantic search — rather than search by shared words.

<Frame>
  <img alt="The image discusses &#x22;Sentence Transformers&#x22; and highlights their ability to understand the meaning of sentences by representing them as numerical vectors that maintain semantic relationships." />
</Frame>

Sentence Transformers specialize in encoding entire sentences or short passages into single, fixed-length vectors that are optimized for similarity matching and retrieval — a core capability for retrieval-augmented systems.

<Frame>
  <img alt="The image illustrates a five-step journey in text analysis including &#x22;Keyword Search,&#x22; &#x22;Embeddings,&#x22; &#x22;Sentence Transformers,&#x22; &#x22;Similarity Matching,&#x22; and &#x22;RAG Systems,&#x22; each with a brief description of their role." />
</Frame>

Key differences from token-level embeddings:

* A single fixed-length vector represents an entire sentence or passage (not one vector per token).
* They build on contextual transformer encoders (BERT, RoBERTa, etc.) and add pooling plus a siamese/bi-encoder setup so pairs of texts can be compared efficiently.
* Because inputs are encoded independently, document embeddings can be precomputed and stored for fast retrieval at scale.

<Callout icon="lightbulb">
  Precompute and index document embeddings when possible. That greatly reduces latency at query time: encode the query on the fly and perform a fast nearest-neighbor lookup against the precomputed vectors.
</Callout>

Under the hood: the typical bi-encoder (dual-encoder) architecture

* Query encoder: encodes a user query into a semantic embedding at request time.
* Document encoder: converts documents into embeddings that can be precomputed and indexed.
* Similarity metric: usually cosine similarity (or inner product) is used to find nearest neighbors.

During training, models are optimized so semantically similar sentences produce embeddings that are nearby. Common fine-tuning tasks include Natural Language Inference (NLI), paraphrase detection, and Semantic Textual Similarity (STS).

<Frame>
  <img alt="The image outlines three tasks for fine-tuning through similarity: Natural Language Inference, Paraphrase Detection, and Semantic Textual Similarity." />
</Frame>

Fine-tuning task summary:

* Natural Language Inference (NLI): label pairs as entailment, contradiction, or neutral so the model learns entailment/contradiction relationships.
* Paraphrase detection: determine whether two sentences convey the same meaning with different wording.
* Semantic Textual Similarity (STS): predict a continuous similarity score for sentence pairs.

Popular Sentence Transformer models (trade-offs: speed vs. accuracy vs. multilingual support)

| Model                               | Best for                 | Notes                                                        |
| ----------------------------------- | ------------------------ | ------------------------------------------------------------ |
| `all-MiniLM-L6-v2`                  | General semantic search  | Fast and efficient; strong speed/accuracy balance.           |
| `multi-qa-MiniLM-L6-cos-v1`         | QA and FAQ retrieval     | Tuned for question-answer style retrieval tasks.             |
| `all-mpnet-base-v2`                 | High-accuracy similarity | Higher accuracy at the cost of more compute and latency.     |
| `distiluse-base-multilingual-cased` | Multilingual search      | Supports many languages; heavier than single-language minis. |

<Frame>
  <img alt="The image lists four popular sentence transformer models with descriptions of their features and uses: all-MiniLM-L6-v2, multi-qa-MiniLM-L6-cos-v1, all-mpnet-base-v2, and distiluse-base-multilingual-cased." />
</Frame>

How Sentence Transformers fit into a retrieval-augmented pipeline

1. Encode user query: the query encoder produces a query embedding.
2. Vector search: perform nearest-neighbor search against precomputed document embeddings stored in a vector database or ANN index.
3. Return top-k documents: optionally re-rank results and pass them to a large language model for final response generation.

Because embeddings capture semantic relationships, the system can surface documents that are relevant even when they don’t share the same keywords. For example, a query about "symptoms of bad spark plugs" can match documents describing "engine misfires and rough idle" if their vectors are close.

<Frame>
  <img alt="The image shows a query similarity comparison with the query &#x22;Symptoms of bad spark plugs&#x22; having a similarity score of 0.89 to &#x22;Engine misfires and rough idle causes.&#x22; Other options include &#x22;How to change oil filter&#x22; and &#x22;Common ignition system problems.&#x22;" />
</Frame>

Example similarity scores (illustrative):

* "Engine misfires and rough idle causes" → 0.89 (highly related)
* "Common ignition system problems" → 0.81 (related)
* "How to change oil filter" → 0.32 (unrelated)

Because similarity is continuous, you can rank results, apply thresholds, or combine vector scores with lexical scores (hybrid search).

Performance and operational considerations

* Precompute embeddings for static corpora to minimize query latency.
* Use approximate nearest neighbor (ANN) indices (HNSW, Faiss, Milvus, Pinecone, etc.) for fast retrieval at scale.
* Balance vector dimensionality and model size against query throughput and memory cost.

<Callout icon="warning">
  Be mindful of compute and storage: larger models produce higher-quality embeddings but require more memory and slower inference. For large document collections, ANN indices and shard/replica strategies are essential to meet latency and throughput targets.
</Callout>

Why Sentence Transformers matter for modern search

* They capture semantic meaning beyond token overlap, handling synonyms and paraphrases automatically.
* Multilingual models enable cross-language retrieval.
* Precomputable document embeddings plus fast ANN indices enable large-scale, low-latency semantic search.
* They integrate easily into retrieval pipelines and pair effectively with LLMs for retrieval-augmented generation (RAG).

<Frame>
  <img alt="The image illustrates why certain features are essential for modern search, highlighting capturing true meaning, enabling multilingual search, and working fast at scale." />
</Frame>

Summary

Sentence Transformers are neural encoders that turn sentences or short passages into fixed-length semantic vectors. Using a dual-encoder architecture and training on similarity tasks (NLI, paraphrase detection, STS), they place similar meanings close together in vector space. This enables retrieval by meaning rather than keyword matching, making them a foundational component of semantic search and retrieval-augmented systems.

<Frame>
  <img alt="The image summarizes the concept of neural models used to convert sentences into semantic vectors, explaining how they work through dual-encoder models and their importance in improving understanding and relevance in information retrieval systems." />
</Frame>

Sentence Transformers provide a compact, human-like representation of meaning as vectors — efficient, effective, and essential for modern intelligent retrieval.

Links and references

* [Hugging Face — Sentence Transformers models and docs](https://www.sbert.net/)
* [Faiss — Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
* [Vector search overview — Pinecone](https://www.pinecone.io/learn/vector-search/)
* [KNN and ANN basics — Milvus documentation](https://milvus.io/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/0a57999a-f47f-4fd5-977b-a4d9618099d5" />
</CardGroup>
