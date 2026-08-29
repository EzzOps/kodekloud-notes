# Python imports for the demo
import os
import numpy as np
import pandas as pd
import PyPDF2
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from sklearn.decomposition import PCA
import plotly.express as px
```

Quick reference — key components used:

| Component                | Purpose                              | Notes / Example                                                       |
| ------------------------ | ------------------------------------ | --------------------------------------------------------------------- |
| PDF loader               | Extract raw text from PDF pages      | Uses `PyPDF2`                                                         |
| Chunking                 | Split text into overlapping segments | Configurable `chunk_size` and `overlap`                               |
| Embeddings               | Convert chunks to vectors            | `SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")` |
| Vector DB                | Persist vectors + metadata           | `chromadb.PersistentClient(path="./chroma_data")`                     |
| Dimensionality reduction | Project to 3D for visualization      | `sklearn.decomposition.PCA(n_components=3)`                           |
| Visualization            | Interactive 3D scatter with previews | `plotly.express.scatter_3d`                                           |

1. PDF loading function
   This function reads a PDF and concatenates all page text into a single string. It is robust to pages without extractable text.

```python theme={null}
def load_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file (e.g., 'use_2025_budget.pdf' or './01-vector-visualise/use_2025_budget.pdf')

    Returns:
        Concatenated text from all pages.
    """
    text_parts = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

print("✅ PDF loading function defined.")
```

2. Chunking function
   We split the concatenated text into overlapping character-based chunks. Overlap preserves semantic continuity between adjacent chunks, which helps downstream tasks like retrieval and visualization.

```python theme={null}
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Full document text.
        chunk_size: Maximum characters per chunk (default 500).
        overlap: Character overlap between consecutive chunks (default 50).

    Returns:
        List of text chunks.
    """
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks

print("✅ Chunking function defined.")
```

3. ChromaDB setup and embedding function
   Create a persistent ChromaDB client that stores data on disk (`./chroma_data`). Configure the embedding function using the `all-MiniLM-L6-v2` sentence-transformers model (compact and fast). The first run will download the model weights.

```python theme={null}
# ChromaDB client (persists to disk in ./chroma_data)
client = chromadb.PersistentClient(path="./chroma_data")

# Embedding function using sentence-transformers (all-MiniLM-L6-v2)
# First run: downloads ~90MB model and loads weights (may take 1-2 minutes)
print("Loading embedding model (all-MiniLM-L6-v2)...")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create or get collection for our document chunks
collection_name = "doc_embeddings"
try:
    collection = client.get_collection(name=collection_name, embedding_function=ef)
    print(f"Using existing collection: {collection_name}")
except Exception:
    collection = client.create_collection(name=collection_name, embedding_function=ef)
    print(f"Created new collection: {collection_name}")

print("✔️ ChromaDB setup complete.")
```

<Callout icon="lightbulb">
  We store each chunk as the document text (and optionally other metadata) alongside its embedding in the vector database. This lets the visualization show a text preview when you hover over a point.
</Callout>

<Callout icon="warning">
  First-time model download and building the embedding index can take time and disk space. Persisting to `./chroma_data` helps avoid repeated downloads on subsequent runs.
</Callout>

4. Load the PDF, chunk it, and add chunks to ChromaDB
   Load the PDF, create overlapping chunks, and insert them into the ChromaDB collection. The snippet below clears the collection before insertion — useful while iterating. Comment out the deletion code if you want to append instead.

```python theme={null}
# Path to PDF (example file baked into the notebook environment)
PDF_PATH = "use_2025_budget.pdf"

# Load PDF and extract text
full_text = load_pdf_text(PDF_PATH)
print(f"Loaded {len(full_text)} characters from PDF.")

# Chunk the text (500 chars per chunk, 50 char overlap)
chunks = chunk_text(full_text, chunk_size=500, overlap=50)
print(f"Created {len(chunks)} chunks.")

# Optional: clear existing data if re-running (comment out to append)
try:
    client.delete_collection(collection_name)
    collection = client.create_collection(name=collection_name, embedding_function=ef)
except Exception:
    # If deletion fails (e.g., collection doesn't exist), continue
    pass

# Prepare IDs and metadata (index + preview)
ids = [f"chunk_{i}" for i in range(len(chunks))]
metadatas = [
    {"chunk_index": i, "preview": chunk[:80] + "..." if len(chunk) > 80 else chunk}
    for i, chunk in enumerate(chunks)
]

# Add chunks to ChromaDB (documents stored alongside embeddings)
collection.add(
    documents=chunks,  # stored as the document text for each item
    ids=ids,
    metadatas=metadatas
)

print(f"Added {len(chunks)} chunks to ChromaDB collection '{collection_name}'.")
```

Note: For a long PDF (188 pages) you may generate hundreds or thousands of chunks depending on `chunk_size` and `overlap`. Adjust chunking parameters to balance granularity and index size.

5. Retrieve embeddings and visualize (PCA → 3D scatter)
   Query the collection to fetch embeddings and metadata, reduce dimensionality with PCA to three components, and render an interactive 3D scatter using Plotly. Hovering shows chunk previews stored in the collection.

```python theme={null}
# Fetch embeddings, documents, and metadata from ChromaDB
results = collection.get(include=["embeddings", "documents", "metadatas"])
embeddings = np.array(results["embeddings"])
documents = results["documents"]
metadatas = results["metadatas"] or [{}] * len(documents)

# PCA: reduce embedding dimensionality (e.g., 384D -> 3D)
pca = PCA(n_components=3)
reduced = pca.fit_transform(embeddings)

# Build DataFrame for Plotly visualization
df = pd.DataFrame({
    "x": reduced[:, 0],
    "y": reduced[:, 1],
    "z": reduced[:, 2],
    "chunk_index": [m.get("chunk_index", i) for i, m in enumerate(metadatas)],
    "preview": [doc[:200] + "..." if len(doc) > 200 else doc for doc in documents],
})

# Interactive 3D scatter - color by chunk index (continuous colormap)
fig = px.scatter_3d(
    df,
    x="x",
    y="y",
    z="z",
    color="chunk_index",
    color_continuous_scale="Turbo",
    hover_data=["chunk_index", "preview"],
    title="Document Chunk Embeddings (PCA 3D)",
    labels={"x": "PC1", "y": "PC2", "z": "PC3", "chunk_index": "Chunk"},
)

fig.update_traces(marker=dict(size=5, opacity=0.85, line=dict(width=0)))
fig.update_layout(
    template="plotly_white",
    height=650,
    coloraxis_colorbar=dict(title="Chunk index"),
    scene=dict(
        bgcolor="rgb(248, 248, 252)",
        xaxis=dict(gridcolor="lightgray"),
        yaxis=dict(gridcolor="lightgray"),
        zaxis=dict(gridcolor="lightgray"),
    ),
)

fig.show()
print("✔️ Plotly 3D visualization complete. Hover over points to see chunk previews.")
```

The interactive plot displays each chunk as a point in 3D space (PCA-reduced). Hover to view the chunk index and a brief text preview pulled from the collection.

<Frame>
  <img alt="The image shows a Jupyter Notebook interface displaying a 3D plot of document chunk embeddings using PCA, with color-coded points representing chunk indices." />
</Frame>

What this visualization reveals

* Each point corresponds to a text chunk's embedding; embeddings encode semantic meaning.
* PCA compresses high-dimensional vectors to three principal components so you can visually inspect structure.
* Nearby points indicate semantically similar chunks; distant points indicate dissimilar content.
* Storing chunk text as `document`/metadata lets you validate what each point represents during exploration.

A few important clarifications

* Vector databases store embeddings (vectors). In this demo we intentionally store the chunk text alongside embeddings so the visualization can display previews — many vector DBs support this pattern.
* Dimensionality reduction (PCA, t-SNE, UMAP) is only used for visualization; original vectors remain high-dimensional in the database and should be used for real retrieval tasks.
* Visual clusters are a qualitative tool to inspect semantic grouping and to debug embedding/model behavior.

Further reading and references

* ChromaDB: [https://www.trychroma.com](https://www.trychroma.com)
* Sentence-Transformers (SBERT): [https://www.sbert.net](https://www.sbert.net)
* scikit-learn PCA: [https://scikit-learn.org/stable/modules/decomposition.html#pca](https://scikit-learn.org/stable/modules/decomposition.html#pca)
* Plotly Python docs: [https://plotly.com/python/](https://plotly.com/python/)

That concludes this demo on visualizing vectors stored in a vector database (ChromaDB). You should now have a clear example of how document text is converted into embeddings and how those vectors can be explored visually. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/1c5dbd37-2982-4a9e-8700-d12cff789f18" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/50209166-3f67-49d2-91bf-135f89b1ffa4" />
</CardGroup>


# Role of Vector Databases in GenAI

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Introduction-to-Vector-Databases-and-Generative-AI/Role-of-Vector-Databases-in-GenAI/page

Explains how vector databases support Retrieval-Augmented Generation by storing embeddings for fast semantic search, enabling LLMs to access up-to-date contextual knowledge in production.

Hello and welcome back.

Where do vector databases fit into generative AI (GenAI)? This short lesson explains their role with a practical Retrieval-Augmented Generation (RAG) flow and real-world production examples.

What is the pattern? Consider a RAG application — this might be a chatbot, a domain-specific query service, or any system that augments user prompts with external knowledge. The end-to-end flow looks like this:

1. User submits a prompt to the RAG application (example: "What is the current temperature in Berlin?").
2. The RAG system converts the prompt (or relevant parts of it) into an embedding and issues a similarity query against a vector database. The vector database stores dense embeddings of documents, telemetry, or records paired with metadata, and supports fast nearest-neighbor search to find semantically relevant items.
   * Common similarity search methods include HNSW, IVF, and PQ (used by FAISS, Milvus, Weaviate, etc.).
3. The vector database returns one or more context items — e.g., the latest sensor readings, a recent policy update, airline rules, or a healthcare document. In some architectures, very fresh signals (like live weather) may be fetched from a dedicated API, but many systems ingest those signals into the vector store so they become directly retrievable by RAG.
4. The RAG system sends the original prompt together with the retrieved context to a large language model (LLM) such as Claude, GPT, or Grok. The LLM synthesizes an answer using both the prompt and the retrieved context.
5. The synthesized response is returned to the user.

Key advantages and risks:

* Vector databases enable fast, semantically rich retrieval of context using dense embeddings, improving relevance and answer quality.
* Without a retrieval layer (or other up-to-date source), GenAI systems can return stale or irrelevant information.
* Vector stores are especially valuable in production for domains requiring current, authoritative context: policies, airline operations, healthcare, customer support, telemetry-driven systems, and knowledge bases.

<Callout icon="lightbulb">
  Vector databases are central to many RAG architectures: they provide scalable, low-latency semantic retrieval that LLMs rely on to produce accurate, context-aware responses.
</Callout>

Example production use cases

| Domain              | Typical use case                                                  | Why a vector DB helps                                             |
| ------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| Customer Support    | Chatbot that answers product questions using manuals and tickets  | Retrieves the most relevant docs by meaning, not just keywords    |
| Healthcare          | Clinical assistant referencing latest protocols and patient notes | Ensures responses reflect up-to-date, relevant clinical context   |
| Airlines / Travel   | Policy and compensation assistant for agents and passengers       | Quickly finds applicable rules and latest notices                 |
| Real-time Telemetry | Incident responder that uses recent sensor readings               | Combines historical docs with live telemetry stored as embeddings |

Architecture diagram

This diagram shows the RAG flow: user prompt → embedding + vector DB retrieval → context + prompt to LLM → response to user.

<Frame>
  <img alt="The image illustrates the role of vector databases in GenAI, showing a process where a user submits a prompt to a RAG application, which retrieves relevant context from a vector store and interacts with an LLM to provide a response back to the user." />
</Frame>

Further reading and references

* Vector databases and similarity search overview: [https://www.pinecone.io/learn/what-is-a-vector-database/](https://www.pinecone.io/learn/what-is-a-vector-database/)
* Retrieval-Augmented Generation (RAG) patterns and best practices: [https://www.pinecone.io/learn/rag/](https://www.pinecone.io/learn/rag/)
* Large language models (LLMs): [https://en.wikipedia.org/wiki/Large\_language\_model](https://en.wikipedia.org/wiki/Large_language_model)
* Popular vector search engines: FAISS, Milvus, Weaviate, Pinecone (search their official docs for deployment details)

That is it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/7de5e69c-79ee-4855-ab42-09691cbabc8a" />
</CardGroup>
