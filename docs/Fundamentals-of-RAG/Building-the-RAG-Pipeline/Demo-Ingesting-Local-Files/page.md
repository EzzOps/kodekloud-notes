# Demo Ingesting Local Files

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Building-the-RAG-Pipeline/Demo-Ingesting-Local-Files/page

Minimal demo ingesting local .md and .txt files into Chroma with Ollama embeddings and LLM, performing chunking, semantic search, prompt building, citation, and simple CLI commands.

This guide demonstrates a minimal, practical retrieval-augmented generation (RAG) pipeline using Ollama for embeddings and generation and Chroma for vector storage and search. We move from an in-memory demo to ingesting files from disk, showing a simple end-to-end flow:

* Read .md/.txt files from a `data/` folder.
* Chunk documents into paragraph-style pieces.
* Embed chunks with Ollama and persist embeddings in Chroma.
* At query time embed the user question, retrieve top-k similar chunks from Chroma, build a prompt that forces the model to answer only from the returned context, and include citations.

This example is intentionally simple (no batching, no BM25 or fancy optimizations) to keep it easy to extend.

Below we walk through the important pieces of `app_v2.py`. The full script is included in the sections below.

***

## Prepare example data

Create a `data` directory with a couple of small documents:

```bash theme={null}
(.venv) jeremy@MACSTUDIO BookSearch % mkdir -p data
(.venv) jeremy@MACSTUDIO BookSearch % cat > data/oncall.md <<'EOF'
