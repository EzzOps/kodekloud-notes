# Oncall Runbook
- Rollback: run scripts/rollback.sh
- Escalation: page #oncall
- SLO: p95 latency 200ms; error rate <0.1%
EOF

(.venv) jeremy@MACSTUDIO BookSearch % cat > data/slo.txt <<'EOF'
Service SLOs:
- latency p95: 200ms
- availability: 99.9%
- error rate: <0.1%
EOF
```

Now `data/` contains two short documents we will ingest.

***

## app\_v2.py — settings and imports

Below are the imports and the demo’s simple hard-coded settings. These values are easy to change for your environment.

```python theme={null}
# app_v2.py
from pathlib import Path
from typing import Iterator, List, Tuple

import argparse
import hashlib
import shutil
import sys

import chromadb
from chromadb.config import Settings
import ollama

CHROMA_PATH = Path("./.chroma")
COLLECTION_NAME = "hello_rag"  # keep same as v1 so the index persists
LLM_MODEL = "llama3.3:latest"
EMBED_MODEL = "nomic-embed-text"
TOP_K = 5
```

Callout with configuration summary:

| Setting           | Use                                                  |
| ----------------- | ---------------------------------------------------- |
| `CHROMA_PATH`     | Local persistence directory for Chroma (`./.chroma`) |
| `COLLECTION_NAME` | Collection name stored in Chroma (`hello_rag`)       |
| `LLM_MODEL`       | Ollama model used for generation (`llama3.3:latest`) |
| `EMBED_MODEL`     | Embedding model used (`nomic-embed-text`)            |
| `TOP_K`           | Default number of retrieval hits to use (5)          |

You can change `LLM_MODEL`, `EMBED_MODEL`, `TOP_K`, and the Chroma path as needed.

***

## Embedding & generation helpers (Ollama)

These helpers handle embeddings and text generation. The embedding helper supports both `prompt=` and `input=` parameter styles used by different Ollama client versions.

```python theme={null}
def _embed(text: str) -> List[float]:
    """Return an embedding vector for the given text. Support either prompt= or input=."""
    try:
        return ollama.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]
    except TypeError:
        return ollama.embeddings(model=EMBED_MODEL, input=text)["embedding"]

def _generate(prompt: str) -> str:
    """Generate text for a prompt using the chosen LLM model."""
    out = ollama.generate(model=LLM_MODEL, prompt=prompt, stream=False)
    return out.get("response", "")
```

<Callout icon="lightbulb">
  The `_embed` helper attempts both parameter styles to maintain compatibility across Ollama client versions. If you control the client, pick one style and simplify the helper.
</Callout>

***

## Chroma collection helper

Create or get a persistent Chroma collection. This example uses the duckdb+parquet implementation and a local persist directory.

```python theme={null}
def _get_collection():
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=str(CHROMA_PATH),
    )
    client = chromadb.Client(settings=settings)
    col = client.get_or_create_collection(name=COLLECTION_NAME)
    return col
```

***

## Simple paragraph-based chunking

The chunking strategy below splits documents into paragraphs and packs them greedily into chunks with optional overlap. Paragraph-based chunks are small, document-like, and work well for many short-doc corpora.

```python theme={null}
def _split_paragraphs(text: str) -> List[str]:
    parts = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n")]
    return [p for p in parts if p]

def make_chunks(text: str, max_chars: int = 800, overlap: int = 150) -> List[str]:
    """Greedy paragraph packer with overlap between chunks."""
    paras = _split_paragraphs(text)
    chunks, buf, total = [], [], 0

    for p in paras:
        # +2 approximates the newline chars we will add when joining
        if buf and total + len(p) + 2 > max_chars:
            chunk = "\n\n".join(buf)
            chunks.append(chunk)
            tail = chunk[-overlap:] if overlap > 0 else ""
            buf = [tail] if tail else []
            total = len(tail)
        buf.append(p)
        total += len(p) + 2

    if buf:
        chunks.append("\n\n".join(buf))

    return chunks
```

Tune `max_chars` and `overlap` for your documents. Paragraph packing keeps chunks coherent and readable by the model.

***

## Iterating files to ingest

Only `.txt` and `.md` files are considered. This helper walks a directory tree and yields matching files.

```python theme={null}
def _iter_files(root: Path) -> Iterator[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".txt", ".md"}:
            yield p
```

***

## Quick environment check (init)

A small command verifies embeddings, text generation, and Chroma connectivity. Run `python app_v2.py init` to validate your environment.

```python theme={null}
def cmd_init():
    print("== Init: quick environment check ==")
    emb = _embed("hello world")
    print(f"Embedding length: {len(emb)} (OK)")
    resp = _generate("Reply with: RAG ready.")
    print(f"LLM said: {resp.strip()}")
    col = _get_collection()
    print(f"Chroma collection: {col.name} (OK)")
    print("Init complete ✅")
```

***

## Semantic search helper

Embed the user question, query Chroma for the top-k results, and return hits with document text, metadata, and distance scores.

```python theme={null}
def _semantic_search(question: str, k: int = TOP_K):
    q_emb = _embed(question)
    col = _get_collection()
    res = col.query(
        query_embeddings=[q_emb],
        n_results=max(1, k),
        include=["documents", "metadatas", "distances"],
    )

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]

    hits = []
    for doc, meta, dist in zip(docs, metas, dists):
        hits.append({"text": doc, "meta": meta, "distance": float(dist)})
    return hits
```

***

## Build the prompt with citations

Format the retrieved chunks into a context block and construct a deterministic prompt that instructs the LLM to answer ONLY from that context and to cite the sources.

```python theme={null}
def _build_prompt(question: str, hits: list[dict]) -> Tuple[str, list[str]]:
    blocks = []
    citations = []
    for i, h in enumerate(hits, 1):
        blocks.append(f"Source {i}:\n{h['text']}\n")
        src = f"[{i}] {h['meta'].get('source', 'unknown')}#chunk-{h['meta'].get('chunk', 0)}"
        citations.append(src)

    ctx = "\n\n".join(blocks)
    prompt = (
        "You are a helpful assistant for DevOps teams. "
        "Answer the QUESTION using ONLY the CONTEXT. "
        "If the answer is not in the context, say you don't know. "
        "Cite sources in the form [1], [2], etc.\n\n"
        f"CONTEXT:\n{ctx}\n\n"
        f"QUESTION: {question}\n"
        "FINAL ANSWER:"
    )
    return prompt, citations
```

Returning the citation strings separately makes CLI printing and logging easier.

***

## Ingest command

This command ingests all `.md`/`.txt` files under a directory:

* Read files from disk
* Chunk documents
* Create deterministic chunk IDs based on file path + chunk content
* Embed chunks and add to Chroma, skipping duplicates

```python theme={null}
def cmd_ingest(dir_path: Path):
    col = _get_collection()

    to_add_ids = []
    to_add_docs = []
    to_add_metas = []
    to_add_embs = []

    total_chunks = 0
    for p in _iter_files(dir_path):
        text = p.read_text(encoding="utf-8")
        chunks = make_chunks(text)
        for i, chunk in enumerate(chunks):
            # deterministic id based on file path + chunk text
            digest = hashlib.sha256(f"{p}:{i}:{chunk}".encode("utf-8")).hexdigest()
            chunk_id = f"{p}#chunk-{i}-{digest[:8]}"
            meta = {"source": str(p), "chunk": i}

            # Skip if this id already exists
            try:
                existing = col.get(ids=[chunk_id])
                if existing and existing.get("ids"):
                    # id exists, skip
                    continue
            except Exception:
                # Some Chroma clients may raise if not found; ignore and proceed
                pass

            emb = _embed(chunk)
            to_add_ids.append(chunk_id)
            to_add_docs.append(chunk)
            to_add_metas.append(meta)
            to_add_embs.append(emb)
            total_chunks += 1

    if to_add_docs:
        col.add(
            ids=to_add_ids,
            documents=to_add_docs,
            metadatas=to_add_metas,
            embeddings=to_add_embs,
        )

    print(f"Ingestion complete. {total_chunks}/{total_chunks} chunks stored.")
```

<Callout icon="lightbulb">
  Deterministic chunk IDs allow safe re-ingestion: the script skips chunks already present in Chroma. If your Chroma client supports efficient upserts, you can swap the existence check for an upsert workflow.
</Callout>

***

## Ask command

At query time we run semantic search, build the prompt with the returned chunks, call the LLM, and print the model’s answer along with a list of cited sources.

```python theme={null}
def cmd_ask(question: str, k: int):
    hits = _semantic_search(question, k=k)
    if not hits:
        print("No results found. Did you run ingest?")
        return

    prompt, citations = _build_prompt(question, hits)
    answer = _generate(prompt)

    print("\n=== Answer ===")
    print(answer.strip())
    print("\n=== Sources ===")
    for s in citations:
        print(s)
```

***

## Stats and reset

Utilities to inspect and reset the local Chroma index:

```python theme={null}
def cmd_stats():
    col = _get_collection()
    try:
        count = col.count()
    except Exception:
        # Some Chroma clients may not support count(); fall back to unknown.
        count = "unknown"
    print(f"Chunks in collection: {count}")

def cmd_reset():
    if CHROMA_PATH.exists():
        shutil.rmtree(CHROMA_PATH)
        print(f"Removed {CHROMA_PATH} (index reset).")
    else:
        print("Nothing to reset.")
```

***

## CLI wiring (argparse)

The CLI wires the commands described above. This is the entrypoint for the script.

```python theme={null}
def main(argv=None):
    parser = argparse.ArgumentParser(description="Lesson: ingest local files and ask questions.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Quick environment check (Ollama + Chroma).")

    p_ingest = sub.add_parser("ingest", help="Ingest .txt/.md under a directory.")
    p_ingest.add_argument("--dir", type=Path, default=Path("data"))

    p_ask = sub.add_parser("ask", help="Ask a question over the ingested corpus.")
    p_ask.add_argument("q", type=str, help="Question string")
    p_ask.add_argument("-k", type=int, default=TOP_K, help="Top-k chunks to use")

    sub.add_parser("stats", help="Show number of chunks.")
    sub.add_parser("reset", help="Delete the local Chroma folder (.chroma).")

    args = parser.parse_args(argv)
    if args.cmd == "init":
        cmd_init()
    elif args.cmd == "ingest":
        cmd_ingest(args.dir)
    elif args.cmd == "ask":
        cmd_ask(args.q, args.k)
    elif args.cmd == "stats":
        cmd_stats()
    elif args.cmd == "reset":
        cmd_reset()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
```

***

## Quick demo (example commands and expected outputs)

Use these example commands to verify the workflow.

1. Initialize (environment check):

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py init
== Init: quick environment check ==
Embedding length: 768 (OK)
LLM said: RAG ready.
Chroma collection: hello_rag (OK)
Init complete ✅
```

2. Ingest local files:

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py ingest --dir data
Ingestion complete. 2/2 chunks stored.
```

3. Check stats:

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py stats
Chunks in collection: 2
```

4. Ask a question using top-k retrieval:

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py ask "How do I roll back the service?"
=== Answer ===
To roll back the service, you should run scripts/rollback.sh.
=== Sources ===
[1] data/oncall.md#chunk-0
```

5. Ask another question:

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py ask "What is our p95 latency target?" -k 3
=== Answer ===
Our p95 latency target is 200ms.
=== Sources ===
[1] data/slo.txt#chunk-0
[2] data/oncall.md#chunk-0
```

6. Reset the index, then ask (shows the behavior when there is no index):

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py reset
Removed ./.chroma (index reset).

(.venv) jeremy@MACSTUDIO BookSearch % python app_v2.py ask "How do I roll back the service?"
No results found. Did you run ingest?
```

Re-run `ingest` to rebuild the index and queries will work again.

***

## Command reference

| Command  |                                             Description | Example                                           |
| -------- | ------------------------------------------------------: | ------------------------------------------------- |
| `init`   | Quick environment check (embeddings, generator, Chroma) | `python app_v2.py init`                           |
| `ingest` |             Ingest `.md`/`.txt` files under a directory | `python app_v2.py ingest --dir data`              |
| `ask`    |                 Ask a question over the ingested corpus | `python app_v2.py ask "How do I roll back?" -k 3` |
| `stats`  |                 Show number of chunks in the collection | `python app_v2.py stats`                          |
| `reset`  |            Delete the local Chroma folder (`./.chroma`) | `python app_v2.py reset`                          |

***

## What we accomplished

* Replaced the tiny in-memory demo with a simple file-based ingestion pipeline.
* Implemented deterministic chunk IDs so re-ingests skip duplicates.
* Used top-k retrieval from Chroma to build a deterministic context for the LLM.
* Instructed the LLM to answer only from the provided context and to include citations.
* Kept the code intentionally minimal so you can extend it for batching, semantic chunking, richer metadata, or different embeddings/LLM providers.

<Callout icon="warning">
  This demo is for local testing and small datasets. For production, consider secure deployment of Ollama/Chroma, robust error handling, rate limits, batching, and privacy/PII considerations for ingested content.
</Callout>

***

## Next steps

* Improve chunking (semantic splits, sentence boundaries, or models like BERT-based splitters).
* Add update/delete semantics for documents (incremental ingestion).
* Add richer metadata (file paths, timestamps, tags) to improve retrieval filtering.
* Add batching and parallelization for embeddings and adds.
* Expose a small web UI to demo RAG in a browser.

***

## Links and references

* [Ollama](https://ollama.com)
* [Chroma](https://www.trychroma.com)
* Chroma docs: [https://www.trychroma.com/docs](https://www.trychroma.com/docs)

This completes the minimal file-based RAG demo using Ollama + Chroma.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/d536d16b-ddcc-4d4a-bbdb-477dda1c4d34/lesson/f8dc2114-60e4-4254-9838-5c940e8441e1" />
</CardGroup>


# Demo Testing your RAG System

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Building-the-RAG-Pipeline/Demo-Testing-your-RAG-System/page

Guide for testing and tuning a hybrid RAG pipeline using BM25 and vector retrieval, inspecting sources, adjusting chunking and retrieval budgets, and preventing hallucinations.

Now that the hybrid RAG pipeline (BM25 + vector store + LLM) is running, this guide shows how to test it, inspect retrieved sources, and tune the main knobs (chunking, retrieval budget, reranking) to improve accuracy and reduce hallucination.

<Frame>
  <img alt="The image contains the text &#x22;Testing your RAG System&#x22; and &#x22;Demo&#x22; with a modern design layout. It also includes a copyright notice for KodeKloud." />
</Frame>

Overview

* Run queries against the hybrid retriever (BM25 + vector store) and inspect which document chunks are returned as sources.
* Tune chunking parameters (size / overlap), per-retriever candidate counts (`k_each`), and `final_k` (how many merged candidates are passed to the LLM).
* Check for hallucinations by asking questions that cannot be answered from your corpus.
* Iterate: change one parameter at a time and re-run a fixed set of test queries to measure the effect.

Key helper functions (core snippets)
The following core functions are typical building blocks for a small hybrid RAG prototype:

* `read_text_files`: read `.txt` documents into a dict mapping filenames to text.
* `chunk_text`: split large documents into overlapping chunks to maintain context during retrieval.
* `tokenize`: simple tokenizer useful for building BM25 indices.
* `rrf_merge`: Reciprocal Rank Fusion to merge ranked results from multiple retrievers.

Example implementation:

```python theme={null}
