# Python-like pseudocode
def retrieve_and_rerank(query, vector_db, embedder, reranker, initial_k=50, final_k=5):
    # 1. Embed the query
    q_emb = embedder.embed_text(query)

    # 2. Initial retrieval from vector DB (fast)
    candidates = vector_db.search(q_emb, top_k=initial_k)  # returns list of (doc_id, doc_text, score)

    # 3. Re-rank: compute a more accurate relevance score for each candidate
    scored = []
    for doc_id, doc_text, _ in candidates:
        score = reranker.score(query, doc_text)  # cross-encoder or LLM scoring
        scored.append((doc_id, doc_text, score))

    # 4. Sort by the re-ranker score (descending) and return top results
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:final_k]
```

## Practical notes, patterns, and tuning tips

* Typical pattern: perform a relatively high-recall initial search (top 50–200) and re-rank to a small curated set (top 3–10).
* Re-rankers add latency and cost; apply them only to the limited candidate set from the vector DB.
* Choose initial\_k and final\_k to balance recall (ensure the right documents are in the candidate set) and precision (final ordering).
* Hybrid strategies: combine lexical filters (BM25) with vector search to improve recall for rare or exact-match queries.
* If latency is critical, consider lightweight neural re-rankers or distilling a re-ranker for faster inference.

## Common re-ranker approaches

* Cross-encoder models (e.g., BERT cross-encoders): jointly encode query and candidate text with cross-attention and output a scalar relevance score.
* LLM-based scoring: prompt an LLM to rate relevance or compute a scalar score via structured prompt engineering.
* Supervised neural rankers: fine-tune models on labeled relevance data for domain-specific improvements.
* Lightweight or distilled rankers: compressed models that approximate cross-encoder behavior with lower latency.

## When to re-rank vs. when not to

* Use re-ranking when final answer quality and precision are important (e.g., legal or medical retrieval, high-stakes Q\&A).
* Skip re-ranking when you need minimal latency and can tolerate lower precision (e.g., broad search UIs where approximate ordering is acceptable).

> **lightbulb** Re-rankers improve final result quality by using models that directly compare query and document text (rather than relying solely on vector similarity). Because they are costlier, they are typically run on a smaller candidate set returned by the vector database.

## Links and references

* [Retrieval-Augmented Generation (RAG) overview](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [Cross-encoder ranking (example BERT cross-encoders)](https://arxiv.org/abs/1901.04085)
* [Vector databases and ANN search — FAISS, Annoy, Milvus](https://en.wikipedia.org/wiki/Approximate_nearest_neighbor_search)
* [Tokenization basics and why it matters](https://huggingface.co/docs/tokenizers/)

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/0cc1ce90-bfcc-42e9-bb0b-dd5c33672504)


# Reducing LLM Memory Footprint During Deployment

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Reducing-LLM-Memory-Footprint-During-Deployment/page

Overview of reducing LLM memory during deployment using knowledge distillation, quantization, and pruning while preserving reasonable performance

Question seven: which technique is most effective for reducing the memory footprint of an LLM during deployment while maintaining reasonable performance?

Options:

* knowledge distillation to a smaller model
* running at higher temperatures
* increasing batch size
* extending the context window

Answer: knowledge distillation to a smaller model.

Knowledge distillation is a practical and widely used approach to compress large language models (LLMs) for deployment. In distillation, a smaller "student" model is trained to mimic the behavior of a larger "teacher" model by learning from the teacher’s outputs (often the softened probability distribution). Because the student has far fewer parameters, it requires less memory and compute at inference time while retaining much of the teacher’s capabilities.

<Frame>
  <img alt="The image presents a question about the most effective technique for reducing the memory footprint of large language models, with the answer being &#x22;knowledge distillation to a smaller model.&#x22; Additional text explains how this technique works." />
</Frame>

Why distillation is effective

* Parameter reduction: The student model has significantly fewer parameters, lowering RAM/VRAM requirements and enabling inference on less powerful hardware.
* Knowledge transfer: Training on the teacher’s soft targets (logits or softened probabilities) conveys nuanced behaviors that hard labels miss.
* Deployment benefits: Smaller models yield lower latency, reduced memory footprint, and easier horizontal scaling for serving many concurrent requests.

Quick comparison of options and memory impact

| Technique                      | Effect on memory footprint | Notes                                                                 |
| ------------------------------ | -------------------------: | --------------------------------------------------------------------- |
| Knowledge distillation         |      Significant reduction | Best single method to reduce model size while preserving performance. |
| Running at higher temperatures |               No reduction | `temperature` affects sampling randomness at inference only.          |
| Increasing batch size          |     Increases memory usage | Larger batches require more GPU memory.                               |
| Extending context window       |     Increases memory usage | Longer context scales memory linearly with sequence length.           |

Clarifications and trade-offs

* The inference-time sampling `temperature` does not change model size or memory usage. In distillation training, a distillation temperature (e.g., `T > 1`) is used to soften teacher logits — that is a training-time technique to improve knowledge transfer, not a memory optimization for inference.
* Increasing batch size or extending the context window increases memory usage rather than reducing it.
* Distillation usually introduces some performance loss compared to the original teacher. Selecting the student model’s capacity is a trade-off between resource savings and task accuracy.

Complementary memory-reduction techniques

* Quantization (e.g., 8-bit, 4-bit): reduce parameter precision to lower memory and speed up inference.
* Pruning: remove low-importance weights or neurons to shrink the model.
* Parameter-efficient fine-tuning (e.g., LoRA): add a small number of trainable parameters instead of fine-tuning the entire model.
* Model offloading / sharding: split model weights across devices or offload parts to CPU to run very large models with limited GPU memory.

Practical tips for deployment

* Combine distillation with quantization and pruning to maximize memory savings while maintaining acceptable performance.
* Validate distilled models on your target benchmarks and real-world inputs to detect degraded behavior early.
* Measure latency and throughput under realistic load (concurrency and batch size) to determine the best student size and precision level.
* Use progressive distillation or multi-stage compression when migrating from a very large teacher to a highly compact student.

> **lightbulb** Knowledge distillation is usually the most effective single technique for substantially reducing memory usage while keeping reasonable model performance—especially when combined with quantization or pruning.

> **warning** Be aware of the trade-offs: aggressive compression can harm accuracy. Evaluate distilled models on your target tasks to ensure acceptable performance.

Links and references

* [Distilling the Knowledge in a Neural Network (Hinton et al.)](https://arxiv.org/abs/1503.02531)
* [Quantization techniques overview](https://arxiv.org/abs/1712.05877)
* [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
* [Pruning neural networks: a survey of methods and results](https://arxiv.org/abs/1710.01878)

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/c38a11ff-1eea-4adc-afec-7ab9743ac1e2)
