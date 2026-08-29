# Text Embedding Models

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/From-Data-to-Vectors-The-Embedding-Layer/Text-Embedding-Models/page

Overview of text embedding models, comparing BERT, SBERT, and OpenAI text-embedding-3, their uses and practical guidance for semantic search and RAG

Welcome back.

In this lesson we dive into one of the most widely used classes of models in NLP: text embedding models. These models convert text into dense vector representations that capture semantic meaning. “Dense” here means each vector component carries useful information so that the resulting vector encodes the overall semantics of words, sentences, or documents.

Where embeddings are used

* Semantic search and information retrieval — find relevant documents by semantic similarity rather than exact keywords.
* Question answering and retrieval-augmented generation (RAG) — retrieve supporting documents to improve generative answers.
* Document clustering and topic grouping — group similar documents or detect themes.
* Chatbots and conversational AI — maintain context and find relevant prior turns or knowledge.
* Recommendation systems — compute similarity between items and users using vector distances.

A familiar production example is Google Search, which uses models such as [BERT](https://arxiv.org/abs/1810.04805) to infer user intent instead of relying purely on keyword matching.

The three important text embedding models

1. [BERT](https://arxiv.org/abs/1810.04805) (Bidirectional Encoder Representations from Transformers)
   * Developer & release: Google AI, October 2018
   * Key idea: Transformer encoder trained with masked language modeling for true bidirectional context by attending to tokens on both sides during pretraining.
   * Typical embedding size: 768 dimensions for BERT-base (you can derive pooled sentence embeddings or token-level vectors depending on the application).
   * Pretraining data: \~3.3 billion words (BooksCorpus + English Wikipedia).
   * When to consider: foundational encoder for contextual representations and fine-tuning for downstream tasks.

2. Sentence-BERT (SBERT)
   * Developer & release: UKP Lab / Nils Reimers & Iryna Gurevych, August 2019
   * Key idea: Adapts BERT to produce meaningful fixed-size sentence embeddings using Siamese/triplet networks and pooling strategies so embeddings are suitable for cosine-similarity based retrieval.
   * Performance: Designed to be far more efficient than naive BERT pairwise comparisons—embeddings can be precomputed and compared with dot-product or cosine similarity.
   * When to consider: open-source, low-cost semantic search and clustering at scale.
   * More info: [https://www.sbert.net/](https://www.sbert.net/)

3. OpenAI text-embedding-3
   * Developer & release: OpenAI, January 2024
   * Key idea: Production-focused embedding model designed for rich, multilingual representations with managed API access.
   * Embedding size: 3072 dimensions (higher capacity for nuanced semantics).
   * Access: Available via API with cost-effective, production-ready options.
   * When to consider: modern RAG systems, AI search tools, and multilingual applications that prefer a managed embedding service.
   * Docs: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)

Comparison at a glance

| Model            | Developer & Release  | Key Strengths                                            |   Typical Embedding Size | Typical Use Cases                                  |
| ---------------- | -------------------- | -------------------------------------------------------- | -----------------------: | -------------------------------------------------- |
| BERT             | Google AI (Oct 2018) | Strong contextual representations; great for fine-tuning |                      768 | Foundation encoder, task-specific modeling         |
| SBERT            | UKP Lab (Aug 2019)   | Efficient sentence-level embeddings, precomputeable      | 768+ (varies by variant) | Semantic search, clustering, inexpensive retrieval |
| text-embedding-3 | OpenAI (Jan 2024)    | High-dimensional, multilingual, managed API              |                     3072 | Production RAG, AI search, multilingual semantics  |

Why embeddings matter
Text embeddings convert words, sentences, and documents into numeric vectors that capture semantic relationships. With these vectors you can efficiently perform nearest-neighbor search, measure semantic similarity, cluster content, and even observe vector arithmetic analogies (for example, relationships like “king − man + woman ≈ queen” illustrate semantic structure beyond keyword overlap).

<Frame>
  <img alt="The image compares three text embedding models: BERT, Sentence-BERT (SBERT), and OpenAI text-embedding-3, highlighting their release dates, developers, and key features. It also explains the importance of text embeddings in transforming words into numerical representations for machine understanding." />
</Frame>

Practical guidance (brief)

> **lightbulb** * Use SBERT or other open-source sentence-level models for efficient, offline embedding computation and low-cost semantic search where you can precompute vectors.
  * Use managed, high-dimensional embeddings such as OpenAI’s `text-embedding-3` for production RAG systems when you need robust multilingual support and a simple API.
  * Use BERT as a foundational encoder when you need to fine-tune models for task-specific representations or when building customized pipelines.

In production, these embeddings power systems such as [ChatGPT](https://openai.com/chatgpt), web search engines, and product search on platforms like Spotify. Next, we’ll explore image embedding models and compare how vision embeddings differ from text embeddings.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/f63353eb-6b3d-442e-ae8d-f7b9f6aea2d9)
