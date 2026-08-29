# Example embedding vector (truncated)
[0.2, 0.8, -0.3, 0.5, ...]
```

Each dimension can capture latent semantic features (for example “animalness”, “size”, “maturity”, “domestication”). Related terms cluster near each other in this vector space.

A simple analogy: imagine two darts thrown at a board. If they land in the same place and point the same way, the throwers were thinking similarly. In vector terms, similarity examines the direction (angle) between vectors rather than raw magnitude.

<Frame>
  <img alt="The image explains how to calculate similarity, using an example of &#x22;automobile&#x22; and &#x22;car&#x22; with nearly identical meanings, depicted with a similarity score of 1.0 and an angle of approximately 0 degrees." />
</Frame>

The standard numerical measure for directional similarity is cosine similarity:

```text theme={null}
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)
```

Here, A · B is the dot product and ||A|| is the vector norm (magnitude). Values close to 1 indicate vectors pointing in the same direction (high semantic similarity), values near 0 indicate orthogonality (little relation), and values near -1 indicate opposite directions (opposite meanings).

You can compute cosine similarity easily in Python:

```python theme={null}
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Example (small synthetic vectors)
vec_cat = np.array([0.9, 0.1, 0.0])
vec_kitten = np.array([0.88, 0.12, -0.01])
vec_dog = np.array([0.7, 0.2, 0.1])

print(cosine_similarity(vec_cat, vec_kitten))  # close to 1.0
print(cosine_similarity(vec_cat, vec_dog))     # lower than cat/kitten
```

<Frame>
  <img alt="The image explains how to calculate similarity using vectors, highlighting that opposite meanings have a 180-degree angle with a similarity of approximately -1.0, using &#x22;hot&#x22; and &#x22;cold&#x22; as examples." />
</Frame>

Why this matters: similarity calculations are the core of retrieval. If retrieved documents are irrelevant or only weakly related, the language model receives poor context and may generate incorrect or confidently wrong answers (hallucinations). Accurate similarity scoring improves the relevance of retrieved context, which in turn strengthens factual grounding for RAG systems.

<Frame>
  <img alt="The image displays a search query &#x22;How do I train my puppy?&#x22; with three document results showing their similarity scores. Document 2, &#x22;Puppy obedience and behavior basics,&#x22; has the highest similarity score of 0.94." />
</Frame>

High-quality similarity transforms retrieval into reliable context for generation. Poor similarity produces weak or misleading context and degrades model outputs.

<Frame>
  <img alt="The image contrasts the effects of poor versus good similarity in document retrieval, highlighting improved context and trustworthy results with good similarity." />
</Frame>

Quick reference — interpreting cosine similarity scores:

| Cosine similarity range | Interpretation                                              |
| ----------------------- | ----------------------------------------------------------- |
| 0.8 — 1.0               | Very high semantic similarity (near-synonyms, same concept) |
| 0.5 — 0.8               | Moderate similarity (related topics, overlapping concepts)  |
| 0.0 — 0.5               | Weak or tangential relation                                 |
| -1.0 — 0.0              | Opposite or unrelated meanings                              |

For more on embeddings and cosine similarity, see:

* [Vector embeddings overview](https://en.wikipedia.org/wiki/Word_embedding)
* [Cosine similarity explanation](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Retrieval-augmented generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

Key takeaways:

* Similarity calculations measure semantic closeness, not string equality.
* Embeddings map text into vectors that capture meaning; similar meanings occupy similar directions in vector space.
* Cosine similarity compares vector directions and is robust to differences in document length.
* Retrieval quality determines RAG quality: good similarity → better context → more accurate model answers.

> **lightbulb** Focus on semantic meaning rather than exact keywords. Proper embeddings plus cosine-based retrieval are fundamental to building reliable, well-grounded RAG systems.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/918af3c5-7cd1-42a2-9fc7-92c19a962982)


# Understanding Embedding Models

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Understanding-Embedding-Models/page

Explains embedding models and how vector representations of text enable semantic search and retrieval augmented generation, plus trade offs in model selection, storage, and practical workflows

In this lesson you’ll learn what embedding models are, how embeddings are generated, and why they are essential to retrieval-augmented generation (RAG) and semantic search systems.

## Keyword search vs. semantic search

Traditional keyword search is like a digital Control-F: it finds literal text matches but ignores meaning. A search for "car" misses "automobile" or "vehicle"; "physician" may miss content that uses "doctor". Because keyword search ignores intent and context, users often must guess the precise phrasing to get relevant results.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Embedding Models&#x22; with two points: &#x22;Context and intent are ignored&#x22; and &#x22;Users must guess exact terms.&#x22;" />
</Frame>

Semantic search solves this by matching meaning instead of exact tokens — enabling search systems to return relevant results even when different words or phrasing are used.

<Frame>
  <img alt="The image is a graphic about &#x22;Embedding Models,&#x22; focusing on &#x22;Semantic Search&#x22; that emphasizes understanding meaning beyond literal text. It includes an icon of a magnifying glass over a list." />
</Frame>

## What is an embedding?

An embedding is a numerical vector representation of text: an array of floating-point numbers (often hundreds or thousands of dimensions) that encodes semantic meaning. In this high-dimensional vector space, similar concepts cluster together: for example, "dog" and "cat" are close, while "dog" and "car" are farther apart. This arrangement enables efficient similarity comparisons between text items.

<Frame>
  <img alt="The image explains embeddings, showing how text is converted into numerical vectors and describes semantic distance, indicating that words with similar meanings are closer in the vector space." />
</Frame>

Embeddings use vector mathematics to quantify similarity. Common measures include:

* Cosine similarity: dot product of normalized vectors, often used to measure angle (semantic closeness) between vectors.
* Dot product: raw inner product useful for some models/indexes.

Higher similarity scores indicate closer semantic meaning (e.g., a higher score between "dog" and "cat" than between "dog" and "car").

## How are embeddings created?

Typical production flow for generating embeddings:

* Tokenize raw text into subword units.
* Feed tokens into a neural network trained on large corpora.
* Produce a dense vector that captures semantic relationships across tokens and context.

<Frame>
  <img alt="The image is a flowchart describing how embeddings are created, with four steps: Text Input, Tokenization, Neural Network, and Vector Output." />
</Frame>

Practical example — generating embeddings with the OpenAI Python client:

```python theme={null}
from openai import OpenAI

client = OpenAI()
embedding = client.embeddings.create(
    input="The quick brown fox jumps over the lazy dog",
    model="text-embedding-3-large"
)
