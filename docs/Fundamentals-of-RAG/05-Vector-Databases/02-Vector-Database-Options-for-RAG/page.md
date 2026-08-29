# ingest_and_query.py
import os
import glob
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# --------- (A) Choose persistence location ---------
DB_DIR = Path("chroma_db")
DB_DIR.mkdir(exist_ok=True)

# Create a persistent client (data survives restarts)
# Note: PersistentClient is available in some chromadb versions.
# If your version expects chromadb.Client(...), adapt accordingly.
client = chromadb.PersistentClient(path=str(DB_DIR))  # loads existing DB if present

# --------- (B) Choose an embedding function ---------
# Use SentenceTransformers model for embeddings
embedding_fn = embedding_functions.SentenceTransformersEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# --------- (C) Get or create collection ---------
collection = client.get_or_create_collection(
    name="demo_texts",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}  # cosine is common for semantic search
)

# --------- (D) Simple chunker ---------
def chunk_text(text: str, max_chars: int = 1500, overlap: int = 200):
    """Split long text into overlapping chunks to improve recall."""
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        # move start forward, but keep 'overlap' characters overlapping
        start = end - overlap if (end - overlap) > start else end
    return [c for c in chunks if c]

# --------- (E) Read .txt files and prepare records ---------
DOCS_DIR = Path("data")
paths = sorted(glob.glob(str(DOCS_DIR / "*.txt")))

documents = []
metadatas = []
ids = []

for p in paths:
    file_id_base = Path(p).stem  # e.g., "beowulf"
    with open(p, "r", encoding="utf-8") as f:
        raw = f.read()

    # If text is long, chunk it; otherwise keep as a single chunk
    chunks = chunk_text(raw, max_chars=1500, overlap=200) if len(raw) > 1800 else [raw]

    for idx, ch in enumerate(chunks):
        uid = f"{file_id_base}__{idx:03d}"  # idempotent ID per file chunk
        documents.append(ch)
        metadatas.append({
            "source": os.path.basename(p),
            "chunk": idx
        })
        ids.append(uid)

if not ids:
    print("🚨 No .txt files found in ./data")
else:
    # --------- (F) Upsert into Chroma (idempotent) ---------
    # Upsert will add new records or replace existing records with same IDs.
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"✅ Ingested {len(ids)} records from {len(paths)} file(s).")

# --------- (G) Run a few demo queries ---------
def search(query_text: str, k: int = 4, where: dict = None):
    """
    Query the collection.
    - query_text: string to search
    - k: number of results to return
    - where: optional metadata filter dict, e.g. {"source": "beowulf.txt"}
    """
    res = collection.query(
        query_texts=[query_text],
        n_results=k,
        where=where  # optional metadata filter dict
    )

    print(f"\n🔎 Query: {query_text}")
    # robustly handle result structure
    ids_res = res.get("ids", [[]])[0]
    docs_res = res.get("documents", [[]])[0]
    metas_res = res.get("metadatas", [[]])[0]
    dists_res = res.get("distances", [[]])[0] if res.get("distances") else [None] * len(ids_res)

    for i in range(len(ids_res)):
        id_ = ids_res[i]
        meta = metas_res[i] if i < len(metas_res) else {}
        doc = docs_res[i] if i < len(docs_res) else ""
        dist = dists_res[i] if i < len(dists_res) else None
        dist_str = f"{dist:.4f}" if isinstance(dist, (int, float)) else "N/A"
        snippet = doc[:180].replace("\n", " ")
        print(f" • id={id_}  dist={dist_str}  source={meta.get('source')}\n   {snippet}...")

# Example queries
if ids:
    search("Describe how Beowulf defeats the monster's mother.", k=3)
    search("Who was Grendel, and why did he attack Heorot?", k=3)
    search("Why does Macbeth decide to kill Duncan?", k=3)
```

## Idempotency and duplicate handling

* Deterministic chunk IDs: we use `file_stem__{idx:03d}` so re-running ingestion with the same files won't create duplicate vectors.
* Use `collection.upsert(...)` for idempotent behavior: it inserts new IDs and replaces existing ones with the same identifier.
* If you want ingestion to fail on duplicate IDs, use `collection.add(...)`, which raises on duplicates.

## Running the script

1. Place plain-text files under `./data` (each book as a `.txt`).
2. Run:

```bash theme={null}
python ingest_and_query.py
```

The first run may take longer while embeddings are computed and the index is built.

Example (trimmed) terminal output:

```text theme={null}
✅ Ingested 5609 records from 5 file(s).

🔎 Query: Describe how Beowulf defeats the monster's mother.
 • id=beowulf__009  dist=0.2638  source=beowulf.txt
   ...and the monster retreats to his den, howling and yelling with agony and fury. The wound is fatal....
 • id=beowulf__002  dist=0.3854  source=beowulf.txt
   ...Rejoicing of the Danes (XIV). Hrothgar's Gratitude (XV). ...

🔎 Query: Who was Grendel, and why did he attack Heorot?
 • id=beowulf__118  dist=0.4706  source=beowulf.txt
   ...The torch of the firmament. He glanced 'long the building, and turned...
...
```

These results show which document chunks the vector search considers most similar. For human-readable, direct answers, pass the retrieved chunks to an LLM for synthesis and re-ranking.

## Production considerations and next steps

* Add an LLM-based re-ranker or QA system to synthesize precise answers from retrieved chunks.
* Improve chunking: use sentence- or token-aware splits (e.g., Hugging Face tokenizers) and retain character offsets.
* Enrich metadata: store title, author, chapter, and location offsets to enable more powerful `where` filters and provenance.
* Indexing and scaling: if you scale beyond a laptop, evaluate managed vector DBs, clustering, or distributed deployments for performance and reliability.
* Security & cost: consider encryption, access controls, and cost of hosted embeddings vs local compute.

## Links and references

* ChromaDB: [https://www.trychroma.com/](https://www.trychroma.com/)
* Sentence Transformers: [https://www.sbert.net/](https://www.sbert.net/)
* ChromaDB docs (API & persistence): [https://www.trychroma.com/docs](https://www.trychroma.com/docs)

This demo shows how to set up and experiment locally with ChromaDB and Sentence Transformers for semantic retrieval.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/82c322fa-a995-47c4-9843-0fc82d817821/lesson/f2681e74-90b7-4e3d-960d-ef99606a0f71)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/82c322fa-a995-47c4-9843-0fc82d817821/lesson/496efc31-7368-4b82-8526-b74a763ad712)


# Vector Database Options for RAG

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Vector-Databases/Vector-Database-Options-for-RAG/page

Comparison and guidance on choosing vector databases for RAG, covering local, self-hosted, and managed options, trade-offs, benchmarks, and practical recommendations

Choosing the right vector database for Retrieval-Augmented Generation (RAG) requires weighing trade-offs between latency, recall, cost, and operational complexity. This article summarizes evaluation criteria, compares the major options across the local → self-hosted → managed spectrum, and gives practical recommendations for prototypes and production systems.

> **lightbulb** When evaluating vector stores, focus on measurable goals: latency targets (ms), recall/QPS, dataset size (vectors), and operational constraints (team skills, budget). Benchmarks against a realistic workload quickly expose practical trade-offs.

## Key considerations

* Latency versus recall: Small latency improvements can be critical in production; sometimes sacrificing a fraction of recall yields orders-of-magnitude gains in response time.
* Hybrid search: Combine vector similarity, keyword matching, and metadata filters to improve retrieval relevance in real-world applications.
* Scale: From millions to billions of vectors, indexing time, memory, and cluster architecture requirements change substantially.
* Operations model: Decide between self-hosting (control, predictable costs) and managed services (lower ops overhead, higher ongoing cost).
* Ecosystem fit: Evaluate SDKs, client libraries, integrations, monitoring, and community/support resources.

Landscape overview: local → self-hosted → managed
Local and embedded options (great for development and small POCs) run on a developer machine or a small VM with minimal infrastructure. Self-hosted open-source systems offer control and customization but require operational responsibility. Managed cloud services minimize ops overhead and accelerate time-to-production at the expense of usage-based pricing and potentially less infrastructure control.

<Frame>
  <img alt="The image is a comparison chart titled &#x22;The Landscape at a Glance&#x22; featuring five self-hosted open-source platforms: Qdrant, Milvus, Weaviate, Vespa, and Elasticsearch/OpenSearch, emphasizing full control and customization." />
</Frame>

Managed options are typically easier to provision and maintain but come with usage-based pricing and potential vendor lock-in.

<Frame>
  <img alt="The image lists managed cloud services including Pinecone, Azure AI Search, Vertex AI Vector Search, AWS OpenSearch, and MongoDB Atlas, and mentions enterprise SLAs with usage-based pricing." />
</Frame>

A pragmatic path: start local/embedded for fast iteration, move to self-hosted for cost predictability and control, and adopt managed services when you need elastic scaling or want to offload operations.

## ChromaDB (local-first)

ChromaDB is a local-first vector store that embeds directly in your application process. It's ideal for quick prototyping, small POCs, and developer workflows because it provides RAG-friendly defaults and metadata filtering out of the box. As needs grow you’ll need to plan scaling and high-availability strategies beyond a single machine.

<Frame>
  <img alt="The image is a diagram showing a Venn diagram with blue, red, and yellow circles labeled &#x22;Local/Embedded: ChromaDB,&#x22; highlighting its use for POCs, small applications, and quick iteration cycles." />
</Frame>

## Local / embedded alternatives

* FAISS: Extremely fast library-level nearest neighbor search with in-process performance. You must provide persistence, sharding, and state management for durability and distribution.
* pgvector: Adds vector support to Postgres. Ideal when your application already uses Postgres — benefits include ACID semantics and familiar tooling.
* Redis (with RedisSearch/RedisVector): In-memory vectors can achieve sub-millisecond latency for small working sets. Expect higher RAM costs; a common pattern is Redis as a hot cache plus a cold vector store.

<Frame>
  <img alt="The image outlines three local/embedded alternatives—FAISS, pgvector, and Redis—highlighting their specific features such as speed, persistence, and ecosystem compatibility." />
</Frame>

## Self-hosted solutions

* Qdrant: Rust-based, memory-efficient, HNSW indexing, strong payload/metadata filtering, and developer-friendly APIs. Flexible deployment — self-host or use their hosted offering.
* Milvus: Built for large distributed clusters and billion-scale datasets. Choose Milvus when you truly require massive scale; expect significant operational work.
* Hybrid systems (Weaviate, Vespa, Elasticsearch/OpenSearch): Provide native hybrid search combining vector and keyword relevance, schema management, aggregations, and advanced filtering. Powerful for enterprise search but more complex to operate.

## Managed services

Managed vector databases (e.g., Pinecone) provide the fastest path to production: simple APIs, elastic scaling, built-in observability, and enterprise SLAs. Trade-offs include usage-based pricing, potential vendor lock-in, and egress or query costs.

<Frame>
  <img alt="The image describes a managed service called &#x22;Pinecone,&#x22; highlighting fast production, low operational overhead, and considerations for usage costs and data transfer. The central icon features multiple arrows pointing outward." />
</Frame>

## Cloud-provider-managed options

* Azure AI Search: Tight integration with the Azure ecosystem; a strong choice for Microsoft/.NET stacks and Azure-hosted workloads.

<Frame>
  <img alt="The image outlines &#x22;Azure AI Search&#x22; as a cloud provider managed option, emphasizing its integration with Azure and its suitability for Microsoft stack teams." />
</Frame>

* Vertex AI Vector Search: Google Cloud’s managed vector search offering designed for massive-scale deployments, often leveraging ANN libraries like ScaNN for efficient billion-vector operations.

<Frame>
  <img alt="The image is an informational graphic about &#x22;Vertex AI Vector Search&#x22; as a cloud provider managed option, highlighting its ScaNN-based massive-scale performance and suitability for Google Cloud Platform-native high-volume applications." />
</Frame>

* AWS OpenSearch and MongoDB Atlas: Offer integrated vector search alongside traditional text search and database features. Use them when you need hybrid retrieval patterns and are already committed to the provider.

## Decision guide

Map specific product requirements to the right technology track:

<Frame>
  <img alt="The image is a decision guide for selecting the appropriate vector database solution based on different use cases, including prototype development, production apps, large-scale deployment, enterprise search, and data proximity. Each use case is associated with specific technologies like ChromaDB, FAISS, pgvector, Milvus, and Elasticsearch." />
</Frame>

Use this quick table to align use cases to recommended choices:

| Use case                    | Recommended options                       | Why                                  |
| --------------------------- | ----------------------------------------- | ------------------------------------ |
| Rapid prototype / local POC | ChromaDB, FAISS                           | Minimal infra, fast iteration        |
| Production — quick path     | Pinecone, Azure AI Search, Vertex AI      | Low ops, SLA-backed scaling          |
| OSS production              | Qdrant (balanced), Milvus (massive scale) | Control, cost predictability         |
| SQL-centric apps            | Postgres + `pgvector`                     | Keep vectors near app data with ACID |
| Ultra-low-latency hot cache | Redis (RedisSearch/RedisVector)           | Sub-ms latency for hot working sets  |

## Pros and cons — quick summary

Local / Embedded

* Pros: Easy to set up, minimal cost, rapid iteration.
* Cons: Limited HA, manual scaling, single-machine constraints.

<Frame>
  <img alt="The image is a pros and cons diagram for &#x22;Local/Embedded&#x22; systems, highlighting easy setup, minimal cost, and rapid iteration as pros, and limited high availability, manual scaling, and single-machine constraints as cons." />
</Frame>

Self-hosted open-source

* Pros: Full control, predictable costs, no vendor lock-in.
* Cons: Operational burden, monitoring and upgrade overhead.

<Frame>
  <img alt="The image is a comparison of pros and cons for self-hosted open-source software (OSS). Pros include full control, predictable costs, and no vendor lock-in, while cons are operations burden, monitoring overhead, and upgrade management." />
</Frame>

Managed cloud

* Pros: Fast deployment, enterprise SLAs, elastic scaling.
* Cons: Ongoing usage costs, potential vendor lock-in, less infrastructure control.

Hybrid engines

* Best for ranking quality and rich filtering at scale. Expect additional complexity and a steeper learning curve.

## Cost and scaling gotchas

* Index build memory and time: Initial indexing can require 2–3× steady-state memory. Plan capacity and expect long build times on very large datasets.
* Recall vs latency tuning: Parameters such as `efConstruction`, `efSearch` (HNSW), and `nprobe` (IVF) affect accuracy and latency. Budget time for parameter sweeps and A/B testing.
* Hybrid query pricing: Managed services may bill hybrid or multi-stage queries per request — query costs can add up quickly.
* Backup & recovery, schema changes, model updates: Re-indexing is often required after schema or model changes; include re-ingestion costs in your plan.
* Ingestion and experimentation costs: Embedding generation, storage, and query tuning require compute and experimentation budgets.

> **warning** Re-indexing and embedding drift are real operational costs. If you retrain or update embeddings frequently, estimate the time and cost to re-ingest and validate results before committing to a solution.

## Recommendations (practical)

* Rapid POC: Start with ChromaDB and a small embedding model to validate the concept quickly.
* Fast route to production: Choose Pinecone, Azure AI Search, or Vertex AI to reduce operational overhead and speed delivery.
* OSS production: Pick Qdrant for balanced simplicity; use Milvus for genuine billion-scale workloads.
* All-SQL approach: Use Postgres + `pgvector` to keep vectors close to relational data.
* Cache-speed pattern: Use Redis for hot data plus a cold, cost-efficient vector store for bulk storage.

## Action plan (practical next steps)

1. Define requirements: latency targets (ms), recall goals, dataset size, cost constraints, and team skills.
2. Choose a track: local/embedded, self-hosted OSS, or managed service based on priorities.
3. Run experiments: benchmark recall vs. latency, tune search parameters, and measure costs.
4. Plan architecture: include re-ranking, hybrid filters, monitoring, backups, and disaster recovery.
5. Pilot & iterate: deploy a focused pilot with instrumentation and use observed metrics to guide the next steps.

<Frame>
  <img alt="The image is a flowchart illustrating an action plan titled &#x22;Next Steps,&#x22; which includes defining requirements, choosing a track, running experiments, planning architecture, and pilot & iterate." />
</Frame>

A short, well-instrumented pilot will surface trade-offs far more effectively than lengthy debates. Use objective benchmarks tied to your SLA and cost targets to make the final decision.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) — for self-hosted orchestration patterns.
* [Pinecone](https://www.pinecone.io/) — managed vector DB.
* [Qdrant](https://qdrant.tech/), [Milvus](https://milvus.io/), [Weaviate](https://weaviate.io/) — popular open-source vector stores.
* [pgvector](https://github.com/pgvector/pgvector) — Postgres extension for vectors.
* [Redis](https://redis.io/) — RedisSearch and vector capabilities.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/82c322fa-a995-47c4-9843-0fc82d817821/lesson/33b95e81-aa52-4796-a65e-8646b5aa2a8d)
