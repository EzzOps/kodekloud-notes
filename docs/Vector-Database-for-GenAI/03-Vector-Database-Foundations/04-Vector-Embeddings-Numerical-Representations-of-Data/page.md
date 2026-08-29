# Vector Embeddings Numerical Representations of Data

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Foundations/Vector-Embeddings-Numerical-Representations-of-Data/page

Explains vector embeddings and how text becomes numerical vectors, encoding semantics for similarity, enabling semantic search, clustering, and retrieval in vector databases

Welcome back.

Earlier we introduced the idea that a vector database stores vector embeddings. In this lesson we’ll explain what embeddings are, how they’re created, and why they’re useful for tasks like semantic search, clustering, and nearest-neighbor lookup. Understanding embeddings will clarify many downstream concepts in retrieval-augmented generation and similarity search.

High-level flow — how text becomes vectors:

* Start with raw input (single words like `apple`, `dog`, `cat`, or longer text such as sentences or documents).
* An embedding model translates text into numeric form so a machine can process and compare it.
* Popular embedding model families include [Word2Vec](https://en.wikipedia.org/wiki/Word2vec), sentence-transformers like [SBERT](https://www.sbert.net/), and embedding variants derived from the [GPT family](https://openai.com/research/gpt-4).
* The output is a fixed-length vector (for example, 768 or 1536 floating-point values). One vector per input item.

<Frame>
  <img alt="The image explains the process of converting simple words into vector embeddings using an embedding model, resulting in lists of numbers that represent each word." />
</Frame>

What a vector looks like

Each embedding is a list of numbers such as:

```Python theme={null}
[0.234, 0.891, -0.456, ...]
```

Vectors often contain hundreds or thousands of floating-point values. These numbers are not arbitrary: they are learned parameters that encode semantic and contextual properties of the input. Inputs with similar meaning map to vectors that lie near each other in the vector space.

Why convert text into vectors?

* Machines operate on numbers. Representing text as vectors enables mathematical comparison and indexing.
* Embedding models are trained so semantically similar items (for example, `dog` and `cat`) produce similar vectors; dissimilar items (for example, `apple` vs `dog`) produce vectors that are farther apart.
* Once numerical, items can be efficiently searched, clustered, or used in downstream models.

<Callout icon="lightbulb">
  Key idea: Embeddings map semantic meaning into geometry — similar meanings are close in vector space, enabling machines to compare and retrieve by similarity.
</Callout>

Where embeddings are used

Vectors are stored in a vector database and used for similarity-driven applications. When a user issues a query (for example in a semantic search interface or an AI assistant), the query is converted into an embedding. The system then retrieves stored vectors that are closest to the query embedding using a similarity metric—commonly cosine similarity or Euclidean distance. This is why results are semantically relevant rather than simple keyword matches.

<Frame>
  <img alt="The image illustrates the process of converting words into vector embeddings using an AI model. It shows input data as words like &#x22;Apple,&#x22; &#x22;Dog,&#x22; and &#x22;Cat,&#x22; which are processed by an embedding model (e.g., BERT, GPT) to produce numerical vectors stored in a vector database." />
</Frame>

A concrete, simplified example

Consider this toy mapping:

```text theme={null}
"dog"   -> [0.8, 0.2, 0.9]
"cat"   -> [0.7, 0.3, 0.8]
"apple" -> [0.1, 0.9, 0.2]
```

Here `dog` and `cat` are numerically close, while `apple` is distant. Real embeddings are much longer and capture nuanced relationships across many dimensions—for example synonyms, analogies, and topical similarity (e.g., “running shoes” ≈ “jogging sneakers”).

Embedding model overview

| Model Family                                            | Typical Dimensionality | Use Case                                                |
| ------------------------------------------------------- | ---------------------- | ------------------------------------------------------- |
| [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)      | `100–300`              | Lightweight word-level semantics, fast training         |
| [Sentence Transformers (SBERT)](https://www.sbert.net/) | `384–768`              | Sentence and paragraph embeddings for semantic search   |
| GPT-style embeddings                                    | `768–1536+`            | Rich contextual embeddings suited to retrieval for LLMs |

<Frame>
  <img alt="The image explains vector embeddings, highlighting the conversion of words into numerical vectors, and shows a vector database illustration with a magnifying glass." />
</Frame>

Summary

* Embeddings are numeric, fixed-length vectors learned from text (or other modalities) that encode semantic information.
* Similar meanings are nearby in vector space, which enables semantic search and similarity-based retrieval.
* Embedding models and vector databases together power modern retrieval systems and many GenAI applications.

Links and references

* [Word2Vec (Wikipedia)](https://en.wikipedia.org/wiki/Word2vec)
* [Sentence Transformers (SBERT)](https://www.sbert.net/)
* [GPT-4 research (OpenAI)](https://openai.com/research/gpt-4)
* [Notion AI](https://www.notion.so/product/ai)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/6b0ab643-f1da-4a9c-a967-b600c16b7483" />
</CardGroup>
