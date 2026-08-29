# Embeddings model
ollama pull nomic-embed-text

# LLM model (Llama 3.3 in this example)
ollama pull llama3.3:latest
```

Note: The model names are examples; use the models available in your Ollama environment.

> **lightbulb** Different versions of the Ollama Python client or model endpoints may expect either `prompt=` or `input=` when calling `ollama.embeddings(...)`. The demo code below tries both to remain compatible across versions.

Warning about re-running the demo

> **warning** When you re-run the demo, Chroma's `add()` may raise an exception if the same `id` already exists in the collection. The demo handles this by catching the error and continuing — this is safe for quick iterations.

Create the application: app\_v1.py
Below is a compact and corrected version of the demo application. It includes:

* Helper functions for embeddings and generation that handle Ollama client variations.
* A Chroma collection getter using a persistent path and cosine similarity.
* Two subcommands: `init` (quick environment checks) and `demo` (index one tiny document, retrieve, and answer a question).

```python theme={null}
# app_v1.py
import argparse
from pathlib import Path
import sys

import chromadb
import ollama

CHROMA_PATH = Path("./.chroma")
COLLECTION_NAME = "hello_rag"
LLM_MODEL = "llama3.3:latest"
EMBED_MODEL = "nomic-embed-text"


def _embed(text: str) -> list[float]:
    """
    Use Ollama embeddings. Some versions expect 'prompt=' and others 'input='.
    Try both for compatibility.
    """
    try:
        return ollama.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]
    except TypeError:
        return ollama.embeddings(model=EMBED_MODEL, input=text)["embedding"]


def _generate(prompt: str) -> str:
    out = ollama.generate(model=LLM_MODEL, prompt=prompt, stream=False)
    return out.get("response", "")


def _get_collection():
    """
    Create or get a persistent Chroma collection. Use cosine space for similarity.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def cmd_init():
    print("=== Init: environment check ===")

    # 1) Quick embedding check
    emb = _embed("hello world")
    print(f"Embedding length: {len(emb)} (OK)")

    # 2) Quick LLM generation check
    resp = _generate("Reply with: RAG ready.")
    print(f"LLM said: {resp.strip()}")

    # 3) Quick Chroma check
    col = _get_collection()
    print(f"Chroma collection: {col.name} (OK)")

    print("Init complete ✅")


def cmd_demo():
    print("=== Demo: the tiniest RAG you can run ===")

    # 0) One tiny 'document' in memory (no files yet)
    doc_text = (
        "Runbook: Payments Service\n"
        "- SLO: p95 latency 200ms; error rate <0.1%\n"
        "- Rollback: run scripts/rollback.sh\n"
        "- Escalation: page #oncall and notify SRE.\n"
    )
    doc_id = "doc-1"
    print("Indexing 1 tiny in-memory doc...")

    # 1) Store in Chroma with our own embedding
    col = _get_collection()
    doc_emb = _embed(doc_text)
    try:
        col.add(
            ids=[doc_id],
            documents=[doc_text],
            embeddings=[doc_emb],
            metadatas=[{"source": "in-memory-demo"}],
        )
    except Exception as e:
        # If you rerun, the id might already exist - safe to ignore for this demo
        print(f"(note) add() raised {e!r}; continuing")

    # 2) Ask a question
    question = "What is the p95 latency target?"
    print(f"\nQ: {question}")

    # 3) Retrieve by semantic similarity (top 1)
    q_emb = _embed(question)
    result = col.query(
        query_embeddings=[q_emb],
        n_results=1,
        include=["documents", "metadatas", "distances"],
    )

    # Extract the returned context
    ctx = result["documents"][0][0]
    dist = result["distances"][0][0]
    src = result["metadatas"][0][0].get("source", "unknown")
    print(f"\nRetrieved context (dist={dist:.3f}, source={src}):\n\n{ctx}\n---\n")

    # 4) Ground the LLM on that context (simple prompt enforcing context use)
    prompt = (
        "You are a helpful assistant. Answer the QUESTION using ONLY the CONTEXT. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"CONTEXT:\n{ctx}\n\n"
        f"QUESTION: {question}\n"
        "FINAL ANSWER:"
    )
    answer = _generate(prompt)
    print("Answer:\n", answer.strip())
    print("\nDemo complete ✅")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Hello RAG (lesson): simple Ollama + Chroma demo."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="Check Ollama (LLM+embeddings) and Chroma reachability")
    sub.add_parser("demo", help="Index one doc and answer one question")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        cmd_init()
    elif args.cmd == "demo":
        cmd_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
```

Run the demo

1. Run the init check:

```bash theme={null}
python app_v1.py init
```

Expected output (example):

```text theme={null}
=== Init: environment check ===
Embedding length: 768 (OK)
LLM said: RAG ready.
Chroma collection: hello_rag (OK)
Init complete ✅
```

2. Run the tiny RAG demo:

```bash theme={null}
python app_v1.py demo
```

Expected output (example):

```text theme={null}
=== Demo: the tiniest RAG you can run ===
Indexing 1 tiny in-memory doc...

Q: What is the p95 latency target?

Retrieved context (dist=0.369, source=in-memory-demo):

Runbook: Payments Service
- SLO: p95 latency 200ms; error rate <0.1%
- Rollback: run scripts/rollback.sh
- Escalation: page #oncall and notify SRE.
---
Answer:
The p95 latency target is 200ms.

Demo complete ✅
```

What this demonstrates

* Ollama (local) can produce embeddings and generate text for grounding answers.
* ChromaDB persists embeddings and returns semantically similar documents.
* Minimal RAG flow: query → embed → retrieve → LLM (grounded on retrieved context) → answer.

Next steps

* Chunk and ingest larger documents from the `data/` folder with overlap-aware chunking.
* Improve prompt engineering and retrieval strategies (e.g., hybrid search, reranking).
* Evaluate retrieval accuracy and build hallucination mitigation strategies.
* Consider model selection and latency trade-offs for production deployments.

Links and references

* [Ollama](https://ollama.com)
* [ChromaDB](https://www.trychroma.com)
* [Project Gutenberg](https://www.gutenberg.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/d536d16b-ddcc-4d4a-bbdb-477dda1c4d34/lesson/cfe1623a-10bf-48f5-addb-55440b7faead)


# Demo Hybrid Retrieval BM25 Chroma Ollama

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Building-the-RAG-Pipeline/Demo-Hybrid-Retrieval-BM25-Chroma-Ollama/page

Shows how to build a local hybrid RAG pipeline combining BM25 keyword search, Chroma vector search, Reciprocal Rank Fusion, and Ollama LLM for source-grounded question answering.

Welcome back.

In this lesson we build a practical hybrid RAG (Retrieval-Augmented Generation) pipeline that combines BM25 keyword search with semantic vector search (ChromaDB), fuses results using Reciprocal Rank Fusion (RRF), and uses an Ollama LLM to produce grounded answers. The pipeline ingests a folder of `.txt` documents (for example, Project Gutenberg books), chunks them, indexes chunks into ChromaDB, persists tokenized chunks for BM25, and executes hybrid queries that blend both retrieval signals to produce a final, source-attributed answer.

We use a local Ollama instance for both embeddings and the LLM so everything can run locally.

Highlights

* Chunk and index plain-text books for retrieval.
* Build a BM25 index for exact keyword matches.
* Build a vector index (ChromaDB) for semantic matches using Ollama embeddings.
* Fuse BM25 and vector rankings via RRF to improve robustness.
* Ask queries that return concise, source-grounded answers from an Ollama chat model.

Overview of the approach

* Read `.txt` files from a folder.
* Chunk the documents and store per-chunk metadata.
* Create a BM25 corpus (tokenized chunks, persisted as pickle files).
* Embed chunks with Ollama and upsert into a persistent Chroma collection.
* On query: run BM25 to get top keyword hits and run Chroma vector search for semantic hits. Merge lists with RRF, fetch fused chunks, construct context, and ask an Ollama chat model to produce a concise answer that cites sources.

We demonstrate this with a public-domain text: Frankenstein by Mary Shelley. I added `Frankenstein.txt` to the `data` folder (Project Gutenberg eBook).

<Frame>
  <img alt="The image shows a Visual Studio Code window displaying the text from the Project Gutenberg eBook of &#x22;Frankenstein; Or, The Modern Prometheus&#x22; by Mary Wollstonecraft Shelley. It includes information about the eBook's usage rights, author, release date, and language." />
</Frame>

Callouts — quick setup and warning

> **lightbulb** Before running the pipeline, install the required Python packages and ensure you have a running local Ollama instance and the Ollama models you plan to use.

> **warning** Ollama models must be installed locally and served by an Ollama daemon. This demo assumes Ollama is reachable on the default local socket. If Ollama is not running or models are missing, embedding and LLM calls will fail.

Prerequisites

* Python 3.8+.
* Local Ollama installed and running with:
  * an embedding model (e.g., `nomic-embed-text`)
  * an LLM (e.g., `llama:3.3:latest`)
* Chroma will store a local persistent collection in `.chroma/`.

Install Python dependencies:

```bash theme={null}
pip install chromadb ollama rank-bm25 tqdm
```

Key files

* `hybrid_rag.py` — single script demonstrating the full pipeline.
* `data/frankenstein.txt` — example corpus (Project Gutenberg).

Architecture and component mapping

| Component          | Purpose                             | Example / CLI                  |
| ------------------ | ----------------------------------- | ------------------------------ |
| Keyword retriever  | Fast exact-term matching            | `rank-bm25`                    |
| Semantic retriever | Conceptual/semantic similarity      | `ChromaDB + Ollama embeddings` |
| Fusion             | Merge rankings from both retrievers | `Reciprocal Rank Fusion (RRF)` |
| LLM                | Generate final grounded answer      | `Ollama chat model`            |

Below is the `hybrid_rag.py` script presented in logical chunks: imports & constants, embedding helpers, utilities, RRF fusion, ingest, BM25 loader, ask function, and CLI.

Note: keep each code block intact when assembling the full file.

Imports and constants

```python theme={null}
#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import pickle
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from tqdm import tqdm
import chromadb
from rank_bm25 import BM25Okapi
import ollama

CHROMA_DIR = Path(".chroma")
COLLECTION_NAME = "books"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama:3.3:latest"
TOP_K = 5

INDEX_DIR = Path("index")
INDEX_DIR.mkdir(exist_ok=True)
BM25_CORPUS_PKL = INDEX_DIR / "bm25_corpus_tokens.pkl"
BM25_IDS_PKL = INDEX_DIR / "bm25_ids.pkl"
```

Embedding helper wrappers

```python theme={null}
def _embed(text: str, model: str = EMBED_MODEL) -> List[float]:
    """Support both prompt= and input= depending on Ollama client version."""
    try:
        return ollama.embeddings(model=model, prompt=text)["embedding"]
    except TypeError:
        return ollama.embeddings(model=model, input=text)["embedding"]

def _generate(prompt: str, model: str = LLM_MODEL, temperature: float = 0.2) -> str:
    resp = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )
    return resp["message"]["content"].strip()
```

File reading, chunking, and tokenization utilities

```python theme={null}
def read_text_files(root: Path) -> Dict[str, str]:
    """Read all .txt files under root (or a single .txt file)."""
    files = []
    if root.is_file() and root.suffix.lower() == ".txt":
        files = [root]
    else:
        files = list(root.rglob("*.txt"))
    out: Dict[str, str] = {}
    for f in files:
        try:
            out[str(f)] = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            out[str(f)] = f.read_text(encoding="latin-1", errors="ignore")
    return out

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """Simple sliding-window chunker. Tune chunk_size and overlap for your use case."""
    text = re.sub(r"\s+", " ", text).strip()
    chunks: List[str] = []
    i = 0
    while i < len(text):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def tokenize(s: str) -> List[str]:
    """Very simple tokenizer for BM25 demo: split on alphanumerics and lowercase."""
    return re.findall(r"[a-zA-Z0-9]+", s.lower())
```

Reciprocal Rank Fusion (RRF) merge

```python theme={null}
def rrf_merge(list_a: List[str], list_b: List[str], k: int = 60, topn: int = 5) -> List[str]:
    """
    Reciprocal Rank Fusion for two ranked lists of IDs.
    Each list should be ordered from most relevant to least.
    """
    scores = defaultdict(float)
    for lst in [list_a, list_b]:
        for rank, id_ in enumerate(lst):
            scores[id_] += 1.0 / (k + rank + 1)
    return [x for x, _ in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)][:topn]
```

Ingest function — chunk, embed, upsert to Chroma, and save BM25 data

```python theme={null}
def ingest(dir_path: str, embedding_model: str = EMBED_MODEL):
    src = Path(dir_path)
    docs = read_text_files(src)
    if not docs:
        raise SystemExit(f"No .txt files found under: {src}")

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    all_ids, all_metadatas, all_docs = [], [], []
    bm25_tokens, bm25_ids = [], []

    print(f"[ingest] Reading and chunking {len(docs)} file(s)...")
    for file_path, text in docs.items():
        chunks = chunk_text(text)
        for idx, ch in enumerate(chunks):
            uid = f"{file_path}::chunk-{idx}"
            all_ids.append(uid)
            all_docs.append(ch)
            all_metadatas.append({"source": file_path, "chunk": idx})
            bm25_tokens.append(tokenize(ch))
            bm25_ids.append(uid)

    print(f"[ingest] Embedding {len(all_docs)} chunks with Ollama ({embedding_model})...")
    embeddings = []
    for ch in tqdm(all_docs):
        e = _embed(ch, model=embedding_model)
        embeddings.append(e)

    print("[ingest] Upserting into Chroma...")
    # batched add to avoid payload limits
    BATCH = 256
    for i in range(0, len(all_ids), BATCH):
        collection.add(
            ids=all_ids[i : i + BATCH],
            embeddings=embeddings[i : i + BATCH],
            documents=all_docs[i : i + BATCH],
            metadatas=all_metadatas[i : i + BATCH],
        )

    print("[ingest] Writing BM25 corpus tokens...")
    with open(BM25_CORPUS_PKL, "wb") as f:
        pickle.dump(bm25_tokens, f)
    with open(BM25_IDS_PKL, "wb") as f:
        pickle.dump(bm25_ids, f)

    print("[ingest] Done.")
```

Load BM25 index (tokens and ids)

```python theme={null}
def _load_bm25() -> Tuple[BM25Okapi, List[str]]:
    if not BM25_CORPUS_PKL.exists() or not BM25_IDS_PKL.exists():
        raise SystemExit("BM25 index files not found. Run ingest first.")
    with open(BM25_CORPUS_PKL, "rb") as f:
        tokens = pickle.load(f)
    with open(BM25_IDS_PKL, "rb") as f:
        ids = pickle.load(f)
    bm25 = BM25Okapi(tokens)
    return bm25, ids
```

ask function — run BM25 and vector searches, fuse, fetch, and query LLM

```python theme={null}
def ask(
    query: str,
    llm_model: str = LLM_MODEL,
    embedding_model: str = EMBED_MODEL,
    k_each: int = 6,
    final_k: int = 5,
):
    # BM25 side
    bm25, bm25_ids = _load_bm25()
    q_tokens = tokenize(query)
    scores = bm25.get_scores(q_tokens)
    # Get top indices and map to IDs
    bm25_top_idx = list(reversed(sorted(range(len(scores)), key=lambda i: scores[i])))[:k_each]
    bm25_top_ids = [bm25_ids[i] for i in bm25_top_idx]

    # Vector side (Chroma)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)
    q_emb = _embed(query, model=embedding_model)
    vec = collection.query(query_embeddings=[q_emb], n_results=k_each)
    vec_ids = [doc_id for doc_id in vec["ids"][0]]

    # Merge via RRF
    fused_ids = rrf_merge(bm25_top_ids, vec_ids, topn=final_k)

    # Fetch fused docs for context
    got = collection.get(ids=fused_ids)
    id_to_doc = dict(zip(got["ids"], got["documents"]))
    id_to_meta = dict(zip(got["ids"], got["metadatas"]))

    # Build context with simple headers
    sections = []
    for _id in fused_ids:
        meta = id_to_meta[_id]
        src = Path(meta["source"]).name
        sections.append(f"Source: {src} [chunk {meta['chunk']}]\n{id_to_doc[_id]}")
    context = "\n\n---\n\n".join(sections)

    # System/user prompt: force the model to use only the provided context.
    system = (
        "You are a concise assistant for a retrieval-augmented CLI.\n"
        "Answer ONLY using the provided context. If the answer is not present, say you don't know."
    )
    user = f"Context:\n\n{context}\n\nQuestion: {query}"

    resp = ollama.chat(
        model=llm_model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        options={"temperature": 0.2},
    )
    answer = resp["message"]["content"].strip()

    # Print the answer and the sources
    print("\n=== Answer ===\n")
    print(answer)
    print("\n=== Sources ===")
    for _id in fused_ids:
        m = id_to_meta[_id]
        print(f"{Path(m['source']).name} (chunk {m['chunk']})")
```

Here's a screenshot showing the code in editor as we prepare the ask function and the LLM call.

<Frame>
  <img alt="The image shows a Visual Studio Code interface with Python code. It includes a function definition and an autocomplete suggestion box." />
</Frame>

CLI entry point — argparse for `ingest` and `ask`

```python theme={null}
def main():
    p = argparse.ArgumentParser(description="Hybrid RAG CLI: BM25 + Chroma + Ollama")
    sp = p.add_subparsers(dest="cmd", required=True)

    p_ing = sp.add_parser("ingest", help="Ingest .txt files into Chroma and build BM25 index")
    p_ing.add_argument("--dir", required=True, help="Folder or .txt file")
    p_ing.add_argument("--embed-model", default=EMBED_MODEL, help="Embedding model for Ollama")

    p_ask = sp.add_parser("ask", help="Ask a question against the ingested corpus")
    p_ask.add_argument("--query", required=True, help="Query string")
    p_ask.add_argument("--llm", default=LLM_MODEL, help="LLM model for Ollama")
    p_ask.add_argument("--embed-model", default=EMBED_MODEL, help="Embedding model for Ollama")
    p_ask.add_argument("--k-each", type=int, default=6, help="Top-K to fetch from each retriever")
    p_ask.add_argument("--final-k", type=int, default=5, help="Final top-K after RRF fusion")

    args = p.parse_args()
    if args.cmd == "ingest":
        ingest(args.dir, embedding_model=args.embed_model)
    else:
        ask(
            args.query,
            llm_model=args.llm,
            embedding_model=args.embed_model,
            k_each=args.k_each,
            final_k=args.final_k,
        )

if __name__ == "__main__":
    main()
```

Usage examples

* Ingest a folder (e.g., the `data` folder with `frankenstein.txt`):

```bash theme={null}
python hybrid_rag.py ingest --dir data
```

Expected ingest output (example):

```bash theme={null}
[ingest] Reading and chunking 1 file(s)...
[ingest] Embedding 673 chunks with Ollama (nomic-embed-text)... 100%
[ingest] Upserting into Chroma...
[ingest] Writing BM25 corpus tokens...
[ingest] Done.
```

* Ask a question:

```bash theme={null}
python hybrid_rag.py ask --query "Who is Robert Walton writing to?"
```

Example output:

```text theme={null}
=== Answer ===

Robert Walton is writing to his sister, Mrs. Saville, in England.

=== Sources ===
frankenstein.txt (chunk 23)
frankenstein.txt (chunk 607)
frankenstein.txt (chunk 36)
frankenstein.txt (chunk 608)
frankenstein.txt (chunk 335)
```

Notes about behavior and best practices

* Why hybrid retrieval? BM25 excels at precise keyword matching (high precision for exact terms). Embedding-based retrieval (semantic search) excels at recall for conceptually related content. Blending both often yields more robust retrieval in realistic applications.
* RRF is a simple, effective fusion strategy to combine two ranked lists into a single ordered result set.
* The prompt instructs the LLM to "Answer ONLY using the provided context" to reduce hallucinations. In practice, fine-tune prompts, retrieval sizes (`k_each` and `final_k`), and chunk sizes to balance precision and recall.
* Chunk size and overlap are tunable knobs. For a local demo, a chunk size of \~800 characters with a 150-character overlap worked well; adjust based on your documents and the model context window.

Testing the system

* Try open-ended queries, e.g., "When does Victor animate the creature?" — the system will either find a grounded answer in the retrieved chunks or reply "I don't know" when the context lacks a definitive answer.
* Add more books (e.g., Sherlock Holmes) to the `data/` directory and re-run `ingest` to build a multi-document corpus. Hybrid retrieval will return relevant chunks across documents.

Summary
This pipeline demonstrates a practical hybrid RAG setup using:

* Local embeddings via Ollama,
* Persistent semantic store via ChromaDB,
* Keyword retrieval via BM25,
* Fusion via RRF,
* Final response generation via an Ollama chat model instructed to use only the retrieved context.

Links and References

* [Ollama — Local LLMs & Embeddings](https://ollama.com)
* [ChromaDB — Vector Database](https://www.trychroma.com)
* [Okapi BM25 (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25)
* [Project Gutenberg](https://www.gutenberg.org)

The repository for this lesson includes the full `hybrid_rag.py` script and example `data/` files so you can run it locally and extend it for your own document corpora.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/d536d16b-ddcc-4d4a-bbdb-477dda1c4d34/lesson/de05ab2d-04a5-4516-ad8c-acc77bc5afec)
