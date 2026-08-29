# app.py
import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Configuration (use environment variables in production)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://<your_openai_endpoint>")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "<your_openai_api_key>")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT", "https://<your_search_endpoint>")
SEARCH_KEY = os.getenv("SEARCH_KEY", "<your_search_key>")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX", "rag")

# Initialize Azure OpenAI client (key-based auth example)
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)

def query_search_service(query_text, top_n=5):
    """Query Azure Cognitive Search and return top N documents."""
    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_KEY)
    )

    results = search_client.search(query_text, top=top_n)
    docs = []
    for r in results:
        # r is a SearchResult; r.document contains the indexed fields
        docs.append(r.document)
    return docs

def format_documents_for_prompt(documents):
    """Convert search documents to a single context string for the model."""
    parts = []
    for i, doc in enumerate(documents, start=1):
        # Adjust fields according to your index schema. Example uses 'title' and 'content'
        title = doc.get("title", f"Document {i}")
        content = doc.get("content", "")
        parts.append(f"Source: {title}\n{content}\n")
    return "\n---\n".join(parts)

def ask_question_with_rag(question):
    # 1) Retrieve relevant documents
    docs = query_search_service(question, top_n=5)
    if not docs:
        return "I don't have information on that topic."

    # 2) Prepare context from documents
    context_block = format_documents_for_prompt(docs)

    # 3) Prepare messages (system instructs to only answer with supporting evidence)
    messages = [
        {
            "role": "system",
            "content": "Answer only if you find supporting content in the provided data. Do not guess. If unsure, say: \"I don't have information on that topic.\""
        },
        {
            "role": "user",
            "content": question
        },
        {
            "role": "system",
            "content": f"Context documents:\n{context_block}"
        }
    ]

    # 4) Send request to Azure OpenAI (RAG enabled via explicit context handling)
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        max_tokens=800,
        temperature=0.0
    )

    # Extract the assistant message
    assistant_msg = response.choices[0].message["content"]
    return assistant_msg

def main():
    print("Azure OpenAI RAG Demo")
    print("----------------------")

    # Example question (replace with your prompt)
    question = "Who are the lead researchers for Project Orion?"
    print(f"\nQuestion: {question}")

    print("\nRetrieving information and generating answer...")
    answer = ask_question_with_rag(question)

    print("\nAnswer:")
    print(answer)

if __name__ == "__main__":
    main()
```

Note: This example demonstrates one pattern—client-side retrieval and context injection. The REST/SDK approaches also support a data\_sources parameter so the service performs retrieval alongside generation. Choose the approach that best fits your architecture and security requirements.

Example console output (expected behavior)

* If documents are indexed and retrieved, the assistant responds with a supported answer and cites the source.
* If no relevant documents are found, the assistant replies: "I don't have information on that topic."

Example:

```text theme={null}
Azure OpenAI RAG Demo
----------------------

Question: Who are the lead researchers for Project Orion?

Retrieving information and generating answer...

Answer:
The lead researchers for Project Orion are:
- Dr. Eliza Tran (AI Systems Architect)
- Major Samuel Drake (Defense Operations Liaison)
- Ava Kohli (Azure Systems Engineer)
```

## Closing notes and references

* Ensure Azure Cognitive Search and its authentication method (API key, managed identity) are configured properly — data-source auth is tied to the search resource.
* Use clear system messages to constrain the assistant and reduce hallucinations.
* Choose between service-side retrieval (data\_sources parameter) and app-side retrieval (explicit queries) based on latency, cost, and security trade-offs.
* Monitor Azure release notes for new data-source connectors and SDK updates.

Helpful links

* [Azure OpenAI Service documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
* [Azure Cognitive Search documentation](https://learn.microsoft.com/azure/search/)
* [Azure Blob Storage documentation](https://learn.microsoft.com/azure/storage/blobs/)

This workflow demonstrates how to ground Azure OpenAI responses with your own documents, helping you move from experiments to robust RAG-enabled applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/a4cc50fb-4b34-41eb-845e-d527ee8eb362/lesson/301b6a09-61de-488f-811b-2f8f05f5691b)


# Azure AI Search

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Implementing-an-Intelligent-Search-Solution/Azure-AI-Search/page

Cloud search service that uses AI for semantic understanding, spell correction, enrichment, and personalized relevance to improve search and product discovery.

[Azure AI Search](https://learn.microsoft.com/azure/search/)

Azure AI Search is a cloud search-as-a-service that moves beyond literal keyword matching to understand user intent, synonyms, and context. For example, an e-commerce site that relies on exact keyword matching might never show "Bluetooth Earbuds" for a user searching "wireless headphones." Azure AI Search closes that gap by extracting meaning, correcting typos, expanding synonyms, and applying semantic ranking to surface relevant results even when the query terms differ from document text.

Why this matters

* Exact-match dependency: Traditional keyword search misses items when query terms don't appear verbatim in product titles or descriptions.
* Typos and misspellings: Users often mistype (e.g., "shose" vs. "shoes"), leading to poor results.
* Vocabulary differences: Different users choose different words for the same concept (e.g., "athletic shoes" vs. "running sneakers").

Azure AI Search addresses these problems so queries like "lightweight running shoes" can surface breathable sneakers even when the exact phrase is not present.

Key benefits and features

Semantic search

* Understands intent and contextual meaning rather than relying only on token frequency.
* Uses semantic ranking to order results by relevance to the user’s intent.

Spell correction and synonyms

* Provides spelling correction and suggestions.
* Supports synonym maps so different terms map to the same concepts.

Personalized recommendations

* Integrates with personalization services (for example, [Azure Personalizer](https://learn.microsoft.com/azure/cognitive-services/personalizer/)) and user behavior signals to surface relevant products and increase engagement and conversion.

<Frame>
  <img alt="A presentation slide titled &#x22;Azure AI Search&#x22; showing three ways to improve search accuracy. It lists Semantic Search (understand intent), Spell Correction and Synonyms (fixes typos), and Personalized Recommendations (suggests products based on past searches)." />
</Frame>

Business outcomes

Integrating Azure AI Search produces measurable improvements:

* Higher conversions: Improved product discovery and relevance frequently yield double-digit uplifts depending on scenario and tuning.
* Faster, more relevant results: Reduced search friction improves UX, engagement, and lowers abandonment.

<Frame>
  <img alt="A slide titled &#x22;Azure AI Search&#x22; showing a rising bar chart with a green arrow and the caption &#x22;30% Increase in sales.&#x22; Below are two circular icons labeled &#x22;Faster search results&#x22; and &#x22;Better customer experience&#x22; on a dark background." />
</Frame>

Knowledge discovery and enrichment

Azure AI Search is not just a query engine — it’s an intelligent pipeline that extracts and enriches data from diverse sources before indexing:

* Ingest content from Azure Blob Storage, SQL databases, Cosmos DB, or flat JSON files.
* Apply built-in or custom AI enrichments (cognitive skills) to extract key phrases, detect language, perform sentiment analysis, run OCR on images, and identify entities like people, places, and product attributes.
* Persist enriched outputs in structured formats for downstream analytics, relevance tuning, or integration with other applications.

Use case example: Enrich product reviews with sentiment labels and extracted feature mentions (e.g., "battery life", "noise cancellation") to improve ranking and filtering for queries that target those features.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Azure AI Search&#x22; that highlights AI-driven knowledge discovery. It lists two features: &#x22;Extract and index data from diverse sources&#x22; and &#x22;Enhance indexing with AI-powered enrichment,&#x22; each shown with a circular icon." />
</Frame>

Core solution architecture

A typical Azure AI Search solution consists of three broad areas:

* AI Search (core): Indexing and query engine that stores documents and serves search requests.
* Azure AI Services / cognitive skills: Optional AI enrichments used during indexing to extract meaning from unstructured content.
* Storage account: Persists intermediate and final artifacts (enriched documents, knowledge store outputs) for durability and reprocessing.

This layered architecture supports fast, relevant queries while enabling richer analysis of extracted knowledge.

<Frame>
  <img alt="A slide titled &#x22;Azure AI Search: Components&#x22; showing a cloud search icon connected to AI, data sources, and a client search interface. On the right are three components: Azure AI Search (core indexing/querying), Azure AI Services (cognitive enrichment), and Storage Account (persistence of extracted knowledge)." />
</Frame>

Four major indexing components

When designing an AI Search pipeline, you will work with these core components:

* Data source: Where raw content resides — Azure Blob Storage, Cosmos DB, SQL, or uploaded JSON. This is the indexing origin.
* Skillset: A sequence of AI enrichments (built-in cognitive skills or custom skills) to extract entities, detect language, perform OCR, sentiment analysis, or other transformations.
* Indexer: Orchestrates fetching data from the data source, applies the skillset, and writes enriched documents to the index. Indexers run on schedules, on demand, or can be event-driven (Event Grid, Azure Functions).
* Index: The final searchable artifact — a structured collection of JSON documents with enriched and extracted fields.

<Frame>
  <img alt="A slide titled &#x22;AI Search Solution – Core Components&#x22; showing four colored circular icons labeled Data Source, Skillset, Indexer, and Index. The Index icon has a caption noting it’s &#x22;a structured, searchable collection of JSON documents with enriched and extracted fields.&#x22;" />
</Frame>

| Component   | Responsibility                                 | Example / Notes                                           |
| ----------- | ---------------------------------------------- | --------------------------------------------------------- |
| Data source | Source of raw content for indexing             | Azure Blob, Cosmos DB, Azure SQL, JSON files              |
| Skillset    | AI enrichments applied during indexing         | Language detection, OCR, entity extraction, sentiment     |
| Indexer     | Orchestrates enrichment and indexing           | Scheduled runs, event-driven triggers, on-demand runs     |
| Index       | Searchable, structured collection of documents | Fields marked searchable, facetable, filterable, sortable |

> **lightbulb** Design indexes with query patterns in mind: choose which fields are searchable, retrievable, facetable, filterable, and sortable to balance relevance and performance.

Putting it together: typical workflow

1. Configure your data source (Blob, SQL, Cosmos DB, or JSON upload).
2. Create a skillset to enrich content (built-in or custom cognitive skills).
3. Point an indexer at the data source and attach the skillset.
4. Optionally persist enriched artifacts to a knowledge store (Storage Account).
5. Index the structured documents into an index.
6. Query the index via the Search API using semantic ranking, filters, facets, and personalized signals.

This pipeline enables fast, relevant, and context-aware search experiences while preserving enriched knowledge for analytics and reuse.

Links and references

* [Azure AI Search documentation](https://learn.microsoft.com/azure/search/)
* [Azure Cognitive Services documentation](https://learn.microsoft.com/azure/cognitive-services/)
* [Azure Personalizer](https://learn.microsoft.com/azure/cognitive-services/personalizer/)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/668a922e-e573-4bcc-8a97-443ae22d225f/lesson/86d14702-b047-4a87-a28c-5f8ade23c2a1)
