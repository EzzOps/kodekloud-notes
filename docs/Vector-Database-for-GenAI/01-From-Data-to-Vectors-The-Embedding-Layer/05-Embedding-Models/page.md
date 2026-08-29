# Optional: recreate DB folder each run for a clean demo.
if Path(DB_PATH).exists():
    import shutil
    shutil.rmtree(DB_PATH)

db = lancedb.connect(DB_PATH)

texts = [c["text"] for c in chunks]
sections = [c["section"] for c in chunks]

# Encode and normalize embeddings
vectors = model.encode(texts, normalize_embeddings=True)

rows = [
    {"section": sections[i], "text": texts[i], "vector": vectors[i].tolist()}
    for i in range(len(texts))
]

if TABLE_NAME in db.table_names():
    db.drop_table(TABLE_NAME)

tbl = db.create_table(TABLE_NAME, data=rows)
print("Rows in table:", tbl.count_rows())
```

You should see the row count equal to the number of chunks created (for example, 10).

## 6) Define search utilities

Create two helper functions:

* `search_policy(question, k)` — performs a vector search in LanceDB and returns top-k hits as a pandas DataFrame
* `pretty_print_results(question, k, preview_chars)` — prints results with section context and distance score

```python theme={null}
def search_policy(question: str, k: int = 3) -> pd.DataFrame:
    qvec = model.encode(question, normalize_embeddings=True).tolist()
    df = (
        tbl.search(qvec)
        .limit(k)
        .to_pandas()
    )
    cols = [c for c in df.columns if c in ("section", "text", "_distance", "score")]
    return df[cols]

def pretty_print_results(question: str, k: int = 2, preview_chars: int = 500) -> None:
    print("Question:", question)
    results = search_policy(question, k)
    for i, row in results.iterrows():
        section = row.get("section", "")
        text = row.get("text", "")
        dist = row.get("_distance", None)
        print("\n--- Match", i + 1, "---")
        if dist is not None:
            print("Distance:", float(dist))
        print("Section:", section)
        print(text[:preview_chars])
```

Notes:

* Using `normalize_embeddings=True` ensures cosine similarity is computed as a simple dot product in many vector DBs.
* The `_distance` field returned by LanceDB is typically the computed metric (lower is closer depending on configuration).

## 7) Example queries

Try a few representative questions to demonstrate semantic search behavior.

* Example: "What is the cabin baggage weight limit?"

```python theme={null}
pretty_print_results("What is the cabin baggage weight limit?", k=2, preview_chars=600)
```

Sample output:

```plaintext theme={null}
Question: What is the cabin baggage weight limit?

--- Match 1 ---
Distance: 0.8290877342242142
Section: 3) Baggage policy
### 3.1 Cabin baggage (carry-on)
- **1 cabin bag** per passenger, max **7 kg**
- **Max dimensions:** **55 x 40 x 23 cm**
- **1 personal item** allowed (laptop bag/handbag) that fits under the seat

### 3.2 Checked baggage (included allowance)
- **Economy:** **1 piece up to 23 kg**
- **Business:** **2 pieces up to 32 kg each**

--- Match 2 ---
Distance: 1.103027927395791
Section: 7) Pets in cabin (training demo policy)
- Allowed pets: **small dogs and cats only**
- Must travel in an approved carrier that fits under the seat
- **Max combined weight (pet + carrier):** **8 kg**
```

The top match is the baggage policy chunk. The second match references pet weight (pet + carrier), which can be returned because embeddings capture semantic relationships — sometimes leading to plausible but different interpretations.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface displaying a Python script related to a text embedding project. It includes details on baggage policies and training demos for cabin pets, with sections for cabin baggage and checked baggage rules." />
</Frame>

Try additional queries:

```python theme={null}
pretty_print_results("If I cancel 30 hours before departure, what refund do I get?", k=2, preview_chars=600)
pretty_print_results("How can I contact Kodekloud Airlines support?", k=2, preview_chars=600)
pretty_print_results("What is the unaccompanied minor service fee?", k=2, preview_chars=600)
pretty_print_results("Can I take a dog in the cabin if my pet + carrier is 10 kg?", k=2, preview_chars=600)
```

A sample cancellation-related query should return the ticket change and cancellation policy as the top match; ambiguous queries can return multiple sections that are semantically related.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface with a code cell displaying results for a text embedding query related to airline ticket changes and cancellations. The sidebar lists various files in a project directory." />
</Frame>

## 8) Notes on behavior and limitations

* Embeddings provide semantic matching, not exact keyword/string matching: paraphrases and related concepts can match.
* Retrieval quality depends on chunking strategy, model selection, and the currency of the embedded document.
* Ambiguous queries may return plausible but incorrect sections. Combining retrieval with a downstream RAG (Retrieval-Augmented Generation) pipeline, intent classification, or rule-based filters can improve precision.
* If the source document changes, re-embed the affected chunks and update the vector store to reflect the latest content.

Quick summary table: pros/cons

| Topic                | Advantages                                   | Considerations                                                                            |
| -------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Chunking by headings | Captures natural semantic boundaries         | Short headings may produce sparse chunks — tune the minimum length                        |
| all-MiniLM-L6-v2     | Small, fast, effective for semantic search   | Not specialized for domain-specific vocabulary; consider larger or tuned models if needed |
| LanceDB              | Lightweight local vector DB with search APIs | For production, consider managed/vector DBs with sharding and persistence policies        |

## 9) Wrap-up and resources

What we covered:

* Loading a Markdown policy document
* Chunking by headings for semantic units
* Encoding chunks with a SentenceTransformer
* Storing vectors in LanceDB
* Performing semantic search and displaying top matches

Embedding documents into a vector database simplifies semantic retrieval and enhances search experiences across knowledge bases and documentation.

Further reading and references:

* SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)
* LanceDB: [https://lancedb.ai/](https://lancedb.ai/)
* RAG (Retrieval-Augmented Generation) concepts: [https://learn.kodekloud.com/user/courses/fundamentals-of-rag](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

Thank you for following this demo — feel free to reuse and adapt the code for other policy or documentation search tasks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/606856c7-cc12-4621-8f63-832f40219703" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/ce6905e0-6e04-4c7c-ac86-cd4562240a15" />
</CardGroup>


# Embedding Models

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/From-Data-to-Vectors-The-Embedding-Layer/Embedding-Models/page

Explains embedding models and retrieval-augmented workflows for converting text and other modalities into vectors, indexing in vector databases, and retrieving context for semantic search and RAG.

Welcome back.

In this lesson we'll walk through a real-world embedding use case and explain the end-to-end flow for retrieval-augmented systems.

End-to-end embedding retrieval flow — high level:

1. A user sends a natural language query (e.g., "hello") to an assistant such as [ChatGPT](https://chat.openai.com/) or [Claude](https://www.anthropic.com/claude).
2. The query text is converted into a numeric vector (an embedding) by an embedding model.
3. That query embedding is compared against a persisted index of document embeddings in a vector database (or other retrieval store).
4. The system retrieves the closest matching documents or passages and passes them as context to the language model.
5. The model combines the retrieved context with its reasoning to generate the final response shown to the user.

* Typically, documents and long-lived content are pre-embedded and stored; queries are embedded at request time.
* Retrieval quality depends on the embedding model, index structure (ANN, exact), and similarity metric (cosine similarity, dot product).

<Frame>
  <img alt="The image is a flowchart depicting the embedding process, showing how user input is processed by ChatGPT or Claude to produce an output, which is then converted into a vector representation and stored in a vector database for comparison." />
</Frame>

Key architecture responsibilities and components

* Embedding model: a neural network that maps natural language (or other modalities) into numeric vectors. This can be a dedicated embedding model or an embedding endpoint provided by a larger LLM.
* Vector database / index: persists embeddings and supports fast nearest-neighbor search (ANN indexes like HNSW, IVFPQ, IVF+PQ, or in-memory FAISS).
* Query-time workflow: embed the incoming text, query the vector index for nearest neighbors, and return the retrieved content to the model as additional context.
* Monitoring and lifecycle: some systems also embed model outputs for analytics, conversational memory, or to detect drift; plan for privacy, retention, and reindexing strategies.

What embedding models do — encoding semantics
The model does not "understand" text like a human. Instead, it converts text into coordinates in a high-dimensional vector space so that semantically similar items are near each other.

Example (illustrative values):

* "The cat sleeps" → \[0.23, −0.45, ...]
* "A feline resting" → \[0.25, −0.44, ...]

Although the wording differs, the two vectors are close in embedding space; downstream search recognizes their semantic relationship even when keywords differ.

<Frame>
  <img alt="The image explains the AI language understanding process, showing how human language phrases are converted into numerical vectors using an embedding model, which helps AI recognize similar meanings with different words." />
</Frame>

Types of embedding models and common use cases

| Model Type               | Typical Use Case                                                                 | Example applications                                        |
| ------------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Text embeddings          | Semantic search, RAG (retrieval-augmented generation), clustering, summarization | Document search, FAQ matching, conversational memory        |
| Image / video embeddings | Visual similarity, image retrieval, clustering of visual assets                  | Reverse image search, deduplication, visual recommendations |
| Audio embeddings         | Speaker identification, semantic search across audio, clustering                 | Podcast search, keyword spotting, speaker diarization       |

Choosing the right model

* Match modality: use a text model for text, an image model for images, and so on.
* Precision vs. cost: larger embeddings or higher-dimensional vectors can increase retrieval fidelity but also storage and compute costs.
* Indexing strategy: ANN indexes (HNSW, IVF) balance search speed and accuracy for large corpora; FAISS and Milvus are common choices.
* Metric: cosine similarity and dot product are most common for text embeddings—pick the metric your embedding model was trained with.

Practical tips

* Pre-embed static content to reduce query latency.
* Normalize vectors (L2 normalization) when using cosine similarity if required by your index.
* Periodically re-embed or reindex when your embedding model changes or when the corpus evolves.
* Monitor recall and precision of retrieved results; use relevance feedback to improve prompts or embeddings.

<Callout icon="lightbulb">
  Embeddings are numeric representations of meaning. When designing systems, choose an embedding model aligned to your data modality (text, image, audio), plan for storage and indexing costs, and implement a reindexing strategy to handle model updates and data drift.
</Callout>

Links and references

* [Vector databases and similarity search (overview)](https://en.wikipedia.org/wiki/Nearest_neighbor_search)
* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Milvus: [https://milvus.io/](https://milvus.io/)
* Pinecone: [https://www.pinecone.io/](https://www.pinecone.io/)
* Annoy: [https://github.com/spotify/annoy](https://github.com/spotify/annoy)

That concludes this lesson. Further sections will explore specific text, image/video, and audio embedding models and show example integration patterns for common vector stores.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/47c71900-9efe-47e3-ac4c-502d14eafd06/lesson/9d3ed682-ed2d-4085-9ca6-e60e62d6d8d4" />
</CardGroup>
