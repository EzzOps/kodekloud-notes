# Create and activate a virtual environment
cd /root
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install sentence-transformers langchain langchain-community langchain-huggingface chromadb numpy
```

After installing dependencies, run the provided verification script to confirm everything is working:

```bash theme={null}
python3 /root/code/verify_environment.py
```

A successful verification prints messages confirming LangChain ↔ ChromaDB integration and basic vector similarity checks, for example:

```text theme={null}
LangChain-ChromaDB integration working

OpenAI configuration found
API Base: https://dev.kk-ai-keys.kodekloud.com/v1

Testing vector similarity operations...
Vector similarity test:
Similar docs similarity: 0.640
Different docs similarity: 0.132
Vector operations working correctly

All environment checks passed!
Your vector database lab environment is fully ready.

Environment Status: PERFECT
Results saved to: /root/markers/environment_verified.txt
```

## Understanding embeddings

Embeddings are the backbone of semantic search. Rather than working with individual keywords, embeddings convert text into dense numerical vectors where semantically similar texts are close in vector space. That enables the search engine to connect queries and documents that use different words but share meaning.

<Frame>
  <img alt="A screenshot of a dark-themed slide or document titled &#x22;Understanding Embeddings — The Foundation of Semantic Search&#x22; with bullet points explaining embeddings and how models learn meaning. A file/sidebar with Python filenames is visible on the right and a colorful cursor points near the heading." />
</Frame>

### Quick embedding example (Task 1)

This concise example demonstrates loading a sentence-transformers model, encoding a query and several documents, computing cosine similarity, and printing results. Normalizing embeddings (normalize\_embeddings=True) can improve cosine-similarity stability.

```python theme={null}
# task_1_understanding_embeddings.py
from sentence_transformers import SentenceTransformer, util
import os

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query = "forgot my password"
    docs = [
        "Password recovery: Use the 'Reset Password' link on login page",
        "Vacation policy: Request time off 2 weeks in advance",
        "Account security: Enable two-factor authentication",
        "Login help: Contact IT if you cannot access your account"
    ]

    # Encode query and documents
    query_emb = model.encode(query, convert_to_tensor=True)
    doc_embs = model.encode(docs, convert_to_tensor=True)

    # Compute cosine similarity scores
    scores = util.cos_sim(query_emb, doc_embs)[0]

    print(f"Query: '{query}'\n")
    print("Results (score > 0.3 = relevant):")
    for doc, score in zip(docs, scores):
        marker = "✅" if score.item() > 0.3 else " "
        print(f"{marker} [{score.item():.2f}] {doc}")

    print("\n🔎 Notice: Found 'Password recovery' and 'Login help'")
    print("    Even though the query didn't contain those exact words!")

    os.makedirs("/root/markers", exist_ok=True)
    open("/root/markers/task1_embeddings_complete.txt", "w").write("DONE")

if __name__ == "__main__":
    main()
```

Example output (abridged):

```text theme={null}
Query: 'forgot my password'

Results (score > 0.3 = relevant):
✅ [0.56] Password recovery: Use the 'Reset Password' link on login page
  [0.07] Vacation policy: Request time off 2 weeks in advance
✅ [0.31] Account security: Enable two-factor authentication
✅ [0.60] Login help: Contact IT if you cannot access your account

🔎 Notice: Found 'Password recovery' and 'Login help'
Even though the query didn't contain those exact words!
```

## Document chunking

Large documents should be split into smaller chunks for embedding for two reasons:

* Embedding models have context limits; extremely long texts can be truncated or produce noisy embeddings.
* Smaller, focused chunks preserve local context and improve retrieval accuracy.

However, naive splitting may cut sentences and lose meaning. Use overlapping chunks to preserve sentence continuity at boundaries. A common starting point is \~500 characters per chunk with \~100-character overlap; tune this for your documents and model.

<Frame>
  <img alt="A screenshot of a &#x22;Smart Document Chunking&#x22; guide that explains the overlap strategy and optimal settings (e.g., chunk size 500 chars, overlap 100 chars). A dark sidebar on the right lists Python files like task_1_understanding_embeddings.py." />
</Frame>

Example using LangChain's RecursiveCharacterTextSplitter:

```python theme={null}
# task_2_chunking.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

if __name__ == "__main__":
    long_text = "..."  # replace with actual document text
    chunks = chunk_document(long_text)
    for i, chunk in enumerate(chunks, start=1):
        print(f"📄 Chunk {i} ({len(chunk)} chars):\n{chunk[:200]}...\n")
    print("✅ Task 2 completed! Document chunking mastered.")
```

> **lightbulb** • Preserves sentence boundaries\
  • Maintains context with overlap\
  • Optimizes chunks for embedding models\
  • Can improve retrieval accuracy significantly

## Vector stores (ChromaDB)

Embeddings are vectors; we need a vector store to index and search them efficiently. ChromaDB is a production-ready vector database that supports fast similarity search and metadata filtering. LangChain integrates with ChromaDB to simplify storing and querying embeddings.

How vector search works (high-level):

1. Document → embed → store in DB
2. Query → embed → find similar embeddings
3. Return top-K results ranked by cosine similarity

### Create a Chroma vector store and index documents (Task 3)

This example shows how to initialize HuggingFace embeddings via LangChain, create Document objects, and build a Chroma vector store in a persistent temporary directory.

```python theme={null}
# task_3_build_vectorstore.py
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import tempfile
import os

def build_vectorstore(doc_texts):
    # Initialize embeddings (HuggingFace wrapper)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # Create Document objects (optional metadata can be added)
    documents = [Document(page_content=text) for text in doc_texts]

    # Persist vector store to a directory (use mkdtemp so the directory remains available
    # after this function returns; TemporaryDirectory would be removed on exit)
    temp_dir = tempfile.mkdtemp()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=temp_dir
    )
    # Ensure data is persisted to disk if the vectorstore supports it
    try:
        vectorstore.persist()
    except Exception:
        # Some vectorstore wrappers persist automatically; ignore if not applicable
        pass

    print(f"📚 Loaded {len(documents)} documents into vector store at {temp_dir}...")
    return vectorstore

if __name__ == "__main__":
    sample_docs = [
        "Remote work policy allows employees to work from home up to 3 days per week with manager approval.",
        "Work hours are flexible but core hours 10 AM to 3 PM are required.",
        "Health insurance covers employee and dependents with company paying 80% of premiums.",
    ]
    vs = build_vectorstore(sample_docs)
    print("✅ Vector store ready!")
```

## Semantic search — Bringing it all together

Now implement the search pipeline: convert the user query to an embedding, query the ChromaDB vector store for the top-K similar chunks, optionally filter by a score threshold, and return the best results.

<Frame>
  <img alt="A dark-themed screenshot of a slide or docs page titled &#x22;Semantic Search - Bringing It All Together,&#x22; explaining semantic vs. traditional search. It shows a pipeline of steps (embedding, vector search, retrieve chunks, rank & return) and a file/sidebar on the right." />
</Frame>

### Full search example (Task 4)

This example assumes you have a built `vectorstore` (as in Task 3). It shows how to run a similarity search, obtain scores, apply a threshold, and print filtered results.

```python theme={null}
# task_4_semantic_search.py
import tempfile
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

def build_search_engine(knowledge_base):
    # Initialize embeddings and documents
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    documents = [Document(page_content=text) for text in knowledge_base]

    # Create vector store in a temporary directory (searching is performed while directory exists)
    with tempfile.TemporaryDirectory() as temp_dir:
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=temp_dir
        )

        print("✅ Vector store ready!\n")

        # Search configuration
        search_query = "work from home policy"
        k = 3
        score_threshold = 0.5

        print(f"● Searching for: '{search_query}'")
        print(f"Returning top {k} results")
        print("-" * 28)

        # Basic similarity search (returns Documents)
        results = vectorstore.similarity_search(search_query, k=k)
        print("\n📚 Search Results:\n")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.page_content}\n")

        # Search with scores (returns list of (Document, score))
        # Note: when embeddings are normalized and the vector store returns cosine similarity,
        # higher scores indicate more similar results.
        results_with_scores = vectorstore.similarity_search_with_score(search_query, k=5)
        relevant_results = [(doc, score) for doc, score in results_with_scores if score >= score_threshold]

        print(f"\n🔎 Filtered Search (threshold > {score_threshold}):")
        print("-" * 40)
        if relevant_results:
            for i, (doc, score) in enumerate(relevant_results, 1):
                print(f"{i}. [{score:.2f}] {doc.page_content}\n")
        else:
            print("No results above the score threshold.")

if __name__ == "__main__":
    knowledge_base = [
        "Remote work policy allows employees to work from home up to 3 days per week with manager approval.",
        "Work hours are flexible but core hours 10 AM to 3 PM are required.",
        "Health insurance covers employee and dependents with company paying 80% of premiums.",
        # ... additional docs ...
    ]
    build_search_engine(knowledge_base)
```

Simulated example run summary:

```text theme={null}
Task 4: Semantic Search Implementation
=====================================
✅ Loading 12 documents into vector store...
✔ Vector store ready!

● Searching for: 'work from home policy'
Returning top 3 results
----------------------------

📚 Search Results:

1. Remote work policy allows employees to work from home up to 3 days per week with manager approval.

2. Work hours are flexible but core hours 10 AM to 3 PM are required.

3. Health insurance covers employee and dependents with company paying 80% of premiums.

🔎 Filtered Search (threshold > 0.5):
```

## Recap & next steps

In this lab we:

* Set up an environment for embeddings and vector search.
* Learned how embeddings capture semantic similarity beyond keywords.
* Implemented smart, overlapping document chunking.
* Built a ChromaDB-backed vector store and indexed document chunks.
* Implemented a semantic search pipeline that converts queries to embeddings, performs similarity search, and returns ranked, filtered results.

Next experiments to improve relevance and production-readiness:

* Try different embedding models (speed vs. accuracy tradeoffs).
* Tune chunk sizes and overlap parameters based on document structure.
* Persist vector stores to a stable location and design a scalable deployment.
* Add metadata filtering (document type, last-updated) and combine with a ranker or reranker for hybrid retrieval.

> **lightbulb** Next steps: experiment with model variants, tune chunking/thresholds, and add metadata filters (e.g., document type, last-updated) to further improve relevance.

## Tools & resources

| Resource                                    | Use case                                                     | Link                                                                                                                                   |
| ------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| sentence-transformers                       | Fast, high-quality embedding models such as all-MiniLM-L6-v2 | [https://www.sbert.net/](https://www.sbert.net/)                                                                                       |
| LangChain                                   | Orchestration utilities, text splitters, integration helpers | [https://python.langchain.com/](https://python.langchain.com/)                                                                         |
| langchain-community / langchain-huggingface | Community embeddings / HuggingFace integration for LangChain | [https://github.com/langchain-community/langchain-community-extras](https://github.com/langchain-community/langchain-community-extras) |
| ChromaDB                                    | Vector database for fast similarity search                   | [https://www.trychroma.com/](https://www.trychroma.com/)                                                                               |
| Hugging Face models                         | Additional embedding models to test                          | [https://huggingface.co/](https://huggingface.co/)                                                                                     |
| NumPy                                       | Numeric utilities and array support                          | [https://numpy.org/](https://numpy.org/)                                                                                               |

Further reading:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for deploying scalable services)
* [LangChain Documentation](https://python.langchain.com/)
* [ChromaDB Docs](https://www.trychroma.com/docs)

Happy building — with embeddings, you can transform keyword-limited search into meaning-aware discovery.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/d2a68b61-67f7-4b30-be4e-685640cb76e1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/38784c24-4ad0-4060-88bb-36f8de428f70)


# Practice Labs Build Stateful AI Workflows

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/Practice-Labs-Build-Stateful-AI-Workflows/page

Guide to building stateful AI workflows using LangGraph including nodes, routers, tool integrations and a research agent example

This guide walks through building stateful AI workflows using LangGraph and related tools. You'll set up a Python environment, create nodes that transform shared state, connect them into directed graphs, add routers for conditional routing, integrate tools (calculator and web search), and combine everything into a simple research agent.

Table of contents

* Environment setup
* Task overview
* Task 1 — Imports & minimal state
* Task 2 — Simple nodes
* Task 3 — Wiring nodes with edges
* Task 4 — Multi-step flow (outline → draft → review)
* Task 5 — Conditional routing (routers)
* Task 6 — Tool integration (calculator)
* Task 7 — Research agent: combining tools (DDGS + calculator + LLM)
* Architecture diagrams
* Integrating external systems with self-describing interfaces
* Further exploration
* Links & references

Environment setup

Prepare a virtual environment and install the runtime dependencies used in these examples: LangGraph, LangChain, an OpenAI wrapper, and the DuckDuckGo search client (`ddgs`). After installation, optionally run a verification script if you have one.

```bash theme={null}
cd /root
source /root/venv/bin/activate

pip install langgraph langchain langchain-openai ddgs
