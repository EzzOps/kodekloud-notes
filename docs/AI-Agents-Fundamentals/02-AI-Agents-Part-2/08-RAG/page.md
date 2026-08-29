# Run the verification script
python3 /root/code/verify_environment.py
```

Example verification output:

```bash theme={null}
🔧 RAG Lab Environment Verification
===================================

📦 Checking Python Environment:
✅ Virtual environment is active

📦 Checking Required Packages:
✅ ChromaDB (vector database) available
✅ Sentence Transformers (embeddings) available
✅ LangChain (RAG framework) available
```

Once dependencies are confirmed, proceed to initialize the vector store and embedding model.

***

## Task 1 — Setup the vector store (ChromaDB)

Create a persistent ChromaDB client and a collection to store document embeddings. Load the sentence-transformers model `all-MiniLM-L6-v2` (384-d vectors) to embed document chunks and queries.

Example setup code (task\_1\_setup\_vectorstore.py):

```python theme={null}
# task_1_setup_vectorstore.py
from sentence_transformers import SentenceTransformer
import chromadb

print("=" * 50)

# 1: Initialize ChromaDB client for persistent storage
client = chromadb.PersistentClient(path="./chroma_db")
print("✅ ChromaDB client initialized")

# 2: Create or get collection named "techcorp_rag"
collection = client.get_or_create_collection(name="techcorp_rag")
print(f"✅ Collection '{collection.name}' ready")

# 3: Initialize embedding model for 384-dimension vectors
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded")

# test the setup
test_text = "Testing RAG setup"
test_embedding = model.encode(test_text)
print(f"✅ Test embedding created: {len(test_embedding)} dimensions")
```

Expected run summary:

```bash theme={null}
vocab.txt: 232kB [00:00, 9.61MB/s]
tokenizer.json: 466kB [00:00, 26.7MB/s]
special_tokens_map.json: 100%
config.json: 100%
(✅) Embedding model loaded
(✅) Test embedding created: 384 dimensions

=> SUCCESS! Your vector store is ready for RAG!
- ChromaDB initialized
- Collection: techcorp_rag
- Embedding model: all-MiniLM-L6-v2
- Vector dimensions: 384
```

This collection is your persistent RAG memory where company documents are stored as vectors for semantic retrieval.

***

## Task 2 — Document processing and smart chunking

Chunking strategy is critical for RAG quality. Prefer paragraph-based chunking with small overlaps so chunks preserve complete thoughts and transitions. This helps the LLM use coherent context without requiring large token budgets.

Example implementation (task\_2\_document\_processing.py):

```python theme={null}
# task_2_document_processing.py
from pathlib import Path
from typing import List
import os

def smart_chunk_document(text: str, max_paragraphs_per_chunk: int = 3, overlap_paragraphs: int = 1) -> List[str]:
    """
    Chunk text by paragraphs, grouping up to max_paragraphs_per_chunk paragraphs per chunk.
    Apply a small overlap so adjacent chunks share overlap_paragraphs to preserve continuity.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []
    chunks = []
    i = 0
    while i < len(paragraphs):
        prev_i = i
        end = min(i + max_paragraphs_per_chunk, len(paragraphs))
        chunk = "\n\n".join(paragraphs[i:end])
        chunks.append(chunk)
        # If we've reached the end, break
        if end >= len(paragraphs):
            break
        # advance with overlap: start next chunk overlap_paragraphs paragraphs before end,
        # but ensure progress to avoid infinite loops
        i = end - overlap_paragraphs
        if i <= prev_i:
            i = end

    return chunks

# Process documents
doc_dir = Path("/root/techcorp-docs")
total_chunks = 0
docs_processed = 0

for category_dir in doc_dir.iterdir():
    if category_dir.is_dir():
        print(f"\n📁 Processing {category_dir.name}:")
        for doc_file in category_dir.glob("*.md"):
            metadata = {
                "source": doc_file.name,
                "section": category_dir.name
            }

            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()

            chunks = smart_chunk_document(content, max_paragraphs_per_chunk=3, overlap_paragraphs=1)
            # Example: here you would encode chunks and add them to ChromaDB with metadata
            total_chunks += len(chunks)
            docs_processed += 1

print(f"\nProcessed {docs_processed} documents into {total_chunks} chunks.")
```

Notes:

* Paragraph-based chunking preserves semantics better than fixed-character slices.
* Make chunk size and overlap parameters configurable for tuning to prompt token limits.

***

## Task 3 — LLM integration

Connect a deterministic, production-ready LLM client (for example, GPT-4.1 Mini via an OpenAI-compatible client). Use conservative generation settings (low temperature, token limits) to reduce hallucination and produce concise answers.

Example code (task\_3\_llm\_integration.py):

```python theme={null}
# task_3_llm_integration.py
from langchain.chat_models import ChatOpenAI

# Initialize client (API key and base should be configured in your environment)
client = ChatOpenAI(model="openai/gpt-4.1-mini")
print("✅ OpenAI client initialized")

def test_generation(client):
    """Test basic LLM generation"""
    temperature = 0.3    # focused, lower chance of hallucination
    max_tokens = 500     # concise answers

    client.temperature = temperature
    client.max_tokens = max_tokens

    print(f"\n🔬 Testing openai/gpt-4.1-mini with temperature={temperature}")

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is RAG in AI? Answer in one sentence."},
    ]

    # Use client's chat completion method appropriate to your SDK (example below)
    response = client(messages)
    print("\n● Test Response:", response.content)
```

Example test output:

```bash theme={null}
🔬 Testing openai/gpt-4.1-mini with temperature=0.3

● Test Response: RAG (Retrieval-Augmented Generation) in AI is a technique that combines retrieval of relevant documents from a large dataset with generative models to produce more accurate and contextually informed responses.
```

With the LLM client verified, you can assemble a RAG prompt template and wire retrieval and generation together.

***

## Task 4 — Prompt engineering for RAG

Craft a prompt template that:

* Injects retrieved context chunks into the prompt,
* Explicitly instructs the model to answer only from the provided context,
* Requires a fixed fallback phrase when the context does not contain the answer to avoid hallucination.

Example prompt builder (task\_4\_prompt\_engineering.py):

```python theme={null}
# task_4_prompt_engineering.py
def create_rag_prompt(context_chunks, user_question):
    """
    Build a system and user prompt that forces the model to use only the provided context.
    If the information is not in the context, the model must say:
    "I don't have that information in the provided documents."
    """
    system_prompt = (
        "You are a helpful AI assistant. Answer the user's question using ONLY the information "
        "present in the provided context chunks. If the answer is not contained in the context, "
        "reply exactly: \"I don't have that information in the provided documents.\" "
        "Be concise and accurate."
    )

    # Build context section from retrieved chunks
    context_text = "Context from TechCorp documents:\n\n"
    for i, chunk in enumerate(context_chunks, 1):
        context_text += f"[Document {i}]\n{chunk}\n\n"

    # Create the user prompt with context and question
    user_prompt = f"""{context_text}
Question: {user_question}

Answer:"""

    return system_prompt, user_prompt

# Example test
context_chunks = ["TechCorp allows up to 3 days/week remote work.", "During emergencies, 100% remote may be authorized."]
system_prompt, user_prompt = create_rag_prompt(context_chunks, "How many days per week can employees work from home?")
print(system_prompt)
print(user_prompt)
```

<Callout icon="lightbulb">
  Design prompts that explicitly constrain the model to the retrieved context and provide a clear fallback phrase for missing information to prevent hallucinations.
</Callout>

Example generated answer (illustrative):

```text theme={null}
You can work from home up to 3 days per week.

Sources: remote-work-policy.md
```

***

## Task 5 — Complete RAG pipeline

Assemble the end-to-end pipeline:

1. Embed the user's query using the same embedding model that encoded document chunks.
2. Query ChromaDB for top-k most relevant chunks (semantic search).
3. Build a context-aware prompt from those chunks.
4. Send the system + user prompt to the LLM to generate an answer.
5. Return the answer along with source attributions (document metadata).

Example pipeline (task\_5\_complete\_rag.py):

```python theme={null}
# task_5_complete_rag.py
import os

def test_rag_pipeline(collection, embedding_model, llm_client, user_question, top_k=3):
    # 1. Embed the question
    q_emb = embedding_model.encode(user_question)

    # 2. Query the collection (ChromaDB query interface may vary)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["metadatas", "documents", "distances"]
    )

    # Extract chunks and sources
    retrieved_chunks = []
    sources = set()
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for i, doc_text in enumerate(docs):
        if not doc_text:
            continue
        retrieved_chunks.append(doc_text)
        meta = metadatas[i] if i < len(metadatas) else {}
        if meta.get("source"):
            sources.add(meta["source"])

    # 3. Build prompts
    system_prompt, user_prompt = create_rag_prompt(retrieved_chunks, user_question)

    # 4. Call LLM (example usage; adapt to your SDK)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = llm_client(messages)

    # 5. Return result with sources
    answer_text = response.content.strip()
    return answer_text, list(sources)

# Example orchestration
if __name__ == "__main__":
    try:
        # Assume collection, model, and client are initialized as in earlier tasks
        print(f"\n⏳ Database has {collection.count()} chunks ready")
        answer, sources = test_rag_pipeline(collection, model, client, "Can I work from home three days a week?")
        print("\nGENERATE: Creating answer...\n")
        print("ANSWER:")
        print(answer)
        print("\nSources:", ", ".join(sources))

        print("\n" + "=" * 50)
        print(" 🧪 RAG Pipeline Complete!")
        print(" - Retrieval: Semantic search working")
        print(" - Augmentation: Context injection ready")
        print(" - Generation: LLM producing answers")
        print(" - Citations: Sources included")
        print("=" * 50)

        # Create marker file
        os.makedirs("/root/markers", exist_ok=True)
        with open("/root/markers/task5_rag_complete.txt", "w") as f:
            f.write("TASK5_COMPLETE:RAG_PIPELINE_READY")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n✅ You've built a complete RAG system — from search to answers!")
```

Example run and result (illustrative):

```bash theme={null}
⏳ Database has 124 chunks ready

GENERATE: Creating answer...

ANSWER:
TechCorp's remote work policy embraces flexible work arrangements to promote work-life balance and productivity. It outlines a hybrid work model and remote work guidelines. During emergency situations such as severe weather or health emergencies, 100% remote work may be authorized; essential personnel are notified separately, and the business continuity plan is activated.

Sources: remote-work-policy.md, remote-work.md

============================================================
🎉 RAG Pipeline Complete!
- Retrieval: Semantic search working
- Augmentation: Context injection ready
- Generation: LLM producing answers
- Citations: Sources included
============================================================
```

This pattern ensures queries are answered using retrieved context and that sources are included for traceability and auditability.

***

## Practical considerations and next steps

* Tune chunking size and overlap to balance contextual completeness against token limits for your target LLM.
* Experiment with embedding models (quality vs. cost) and with LLM temperature/length settings.
* Add filters for document recency, confidentiality tags, or department-level access control.
* Implement caching, rate limiting, and logging for production usage.
* Consider connecting to HR systems or identity-aware access control when answers depend on user-specific entitlements.

<Callout icon="warning">
  Handle confidential or restricted documents with care. Ensure access controls and document classification are enforced before including sensitive content in embeddings or returning it in generated answers.
</Callout>

Suggested links and references:

* [ChromaDB Documentation](https://www.trychroma.com/)
* [Sentence Transformers Models](https://huggingface.co/sentence-transformers)
* [LangChain Documentation](https://python.langchain.com/)
* [OpenAI Platform](https://platform.openai.com/)

<Frame>
  <img alt="A hand-drawn diagram of a retrieval-augmented generation (R.A.G.) system showing documents (legal, customer support) feeding a vector database into an LLM that processes a user question and produces a generated answer. The sketch also labels it a &#x22;Simple Chat App&#x22; and shows an example question about remote work policy for international employees." />
</Frame>

The diagram above illustrates the simple chat app architecture: documents are embedded into a vector DB, relevant chunks are retrieved for a user question, and an LLM produces a grounded answer that includes source attributions.

You're now set up with a working RAG architecture — retrieval, augmentation, and generation — ready to iterate and adapt for your production use case.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/233fe08f-0873-4d3c-8230-b56e8d37d000" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/639fbac1-4ab8-495f-b8be-33720ed2cf49" />
</CardGroup>


# RAG

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/RAG/page

Explains Retrieval-Augmented Generation combining vector retrieval and context injection to provide accurate, up-to-date LLM answers from private documents with engineering guidance.

Instead of scanning 500 GB of documents into a model's context window, Retrieval-Augmented Generation (RAG) lets an AI assistant find and use only the most relevant content at query time. RAG combines semantic search over a vector database with prompt-time context injection so an LLM can generate accurate, up-to-date answers without retraining.

Example user question: "What's our remote work policy for international employees?"\
With RAG, the assistant locates the exact policy passages and uses them to produce a targeted, current response.

RAG can be understood as three sequential steps: Retrieval, Augmentation, and Generation.

## 1) Retrieval

* Convert documents and the incoming user question into vector embeddings.
* Compare the query embedding against stored document embeddings in a vector database using semantic similarity.
* Return the top-matched documents or document chunks (not simple keyword matches — the search finds semantically related passages).

Why embeddings and vector search? Because they let you find content that matches the meaning of the question (e.g., "remote work policy for international employees") even when the wording differs across documents.

## 2) Augmentation

Augmentation injects the retrieved text snippets into the model’s prompt at runtime. Typical augmentation steps:

* Select the top-k passages returned by the vector search.
* Optionally filter or re-rank passages by metadata, recency, or source trust.
* Insert these passages into a prompt template so the LLM can reference them while generating an answer.

<Callout icon="lightbulb">
  RAG usually avoids costly model fine-tuning: you provide retrieved context at runtime so a base LLM can generate accurate answers using up-to-date, private data without being retrained.
</Callout>

## 3) Generation

* The LLM receives a prompt that includes the user question plus the retrieved context.
* The model synthesizes information from those passages and its own knowledge to produce a coherent, accurate answer tailored to the query (for example, applying policy details to "international employees").

<Frame>
  <img alt="A hand-drawn diagram of a retrieval-augmented generation (RAG) pipeline: a user question is fed into an LLM which queries a vector database of legal and customer-support documents and then produces a generated answer." />
</Frame>

This matters because legal documents often contain long, structured paragraphs

that need to be preserved and intact, while conversational transcripts can be split at the sentence or paragraph level.

## Why RAG matters

* Extends an LLM’s effective knowledge beyond its training cutoff by supplying current documents at query time.
* Enables private, domain-specific answers without embedding proprietary data into model weights.
* Preserves context fidelity by surfacing the exact passages used to answer a question, improving traceability and trust.

## Calibrating and designing a RAG system

Getting reliable outputs requires careful design and iterative tuning. Key factors include chunking, retrieval size, scoring, and prompt templates.

| Design factor                        | Effect on results                                                            | Practical recommendation                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Chunk size & overlap                 | Too-small chunks lose context; too-large chunks reduce retrieval granularity | Use larger, structure-preserving chunks for legal/technical docs; use sentence/paragraph chunks for transcripts |
| Number of retrieved passages (k)     | Small k may miss relevant info; large k can introduce noise                  | Start with k=3–10 and tune by task / dataset                                                                    |
| Similarity scoring & normalization   | Affects ranking fairness across sources and lengths                          | Normalize by passage length and use re-ranking with metadata when needed                                        |
| Prompt templates & context injection | Determines how well the model uses the retrieved passages                    | Provide clear instructions and cite sources/footnotes in the prompt                                             |

Common engineering considerations:

* Preserve important structure (headings, numbered lists, dates) when chunking.
* Store metadata (source, timestamp, author) with embeddings for filtering and auditing.
* Use recency or source trust to weight retrievals when answers must favor the latest policy or authoritative documents.
* Evaluate with end-to-end metrics: precision/recall of retrieved passages, hallucination rate, and human feedback loops.

## Implementation resources

* Vector databases and similarity search: Pinecone, Weaviate, Milvus
* Embeddings and semantic search guides: OpenAI Embeddings, semantic search overview
* Prompt design and safety: best practices for context injection and hallucination mitigation

Links and references:

* [Pinecone Vector Database](https://www.pinecone.io/)
* [Weaviate](https://weaviate.io/)
* [Milvus](https://milvus.io/)
* [Semantic Search (overview)](https://en.wikipedia.org/wiki/Semantic_search)
* [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

RAG is a practical pattern to deliver timely, accurate, and auditable answers from private collections. Building an effective pipeline is an engineering process—choose chunking strategies and retrieval parameters that match your document types, and iterate on prompt and retrieval design to reduce noise and improve reliability.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/e24182c8-d1e4-4f98-a6e5-354ae7e8c3eb" />
</CardGroup>
