# Demo Hello RAG

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Building-the-RAG-Pipeline/Demo-Hello-RAG/page

Guide to building a minimal RAG pipeline using Ollama for embeddings and generation and ChromaDB for vector storage, indexing one in-memory document and producing grounded answers with local LLM

This guide walks you through building a minimal Retrieval-Augmented Generation (RAG) pipeline end-to-end using Ollama for embedding and generation and ChromaDB for vector storage and retrieval. The goal is a compact, runnable demo that indexes a single in-memory document, retrieves it by semantic similarity, and produces a grounded answer from a local LLM.

Goals

* Use Ollama for embeddings and LLM generation.
* Use ChromaDB (Chroma) for persistence and similarity search.
* Run a minimal RAG round trip with one in-memory document.

Key components

| Component   | Purpose                                        | Example / Notes                       |
| ----------- | ---------------------------------------------- | ------------------------------------- |
| Ollama      | Local embeddings + LLM generation              | [Ollama](https://ollama.com)          |
| ChromaDB    | Persistent vector store + retrieval            | [ChromaDB](https://www.trychroma.com) |
| Demo script | Index one doc, query, retrieve, and prompt LLM | `python app_v1.py demo`               |

Prerequisites / context

* A `data/` folder with Project Gutenberg text files (optional for this tiny demo). Example sources: [Project Gutenberg](https://www.gutenberg.org/).
* Ollama running locally. Start it with `ollama serve` if not running.
* Two Ollama models available locally: an embedding model and an LLM model (examples below).

Install dependencies
Create a Python virtual environment and install the required packages:

```bash theme={null}
python3 -m venv .venv
source .venv/bin/activate
pip install chromadb ollama
```

Pull the Ollama models you plan to use locally (examples shown):

```bash theme={null}
