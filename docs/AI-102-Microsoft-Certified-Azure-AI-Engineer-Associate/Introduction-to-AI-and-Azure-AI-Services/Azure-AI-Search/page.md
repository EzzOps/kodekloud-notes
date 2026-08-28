# python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def authenticate_client(endpoint: str, key: str) -> TextAnalyticsClient:
    """
    Authenticate and return a TextAnalyticsClient using the provided endpoint and key.
    """
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

def sentiment_analysis(client: TextAnalyticsClient, text: str):
    """
    Perform sentiment analysis on a single document string.
    """
    try:
        response = client.analyze_sentiment([text])[0]
        print(f"\nDocument Sentiment: {response.sentiment}")
        print(
            f"Overall scores: positive={response.confidence_scores.positive:.2f}, "
            f"neutral={response.confidence_scores.neutral:.2f}, "
            f"negative={response.confidence_scores.negative:.2f}"
        )
        return response
    except Exception as err:
        print(f"Encountered exception: {err}")
        return None

def main():
    # Replace with your endpoint and key (do not hard-code in production)
    endpoint = "https://ai102cogservices909.cognitiveservices.azure.com/"
    key = "<YOUR_KEY>"
    sample_text = "Learning AI is good for career growth."
    client = authenticate_client(endpoint, key)
    print("Performing sentiment analysis:")
    sentiment_result = sentiment_analysis(client, sample_text)

if __name__ == "__main__":
    main()
```

What the SDK returns:

* Document-level sentiment (positive / neutral / negative)
* Confidence scores for each class
* Optional per-sentence sentiment and additional metadata if requested

## REST approach (Python + requests)

The REST approach requires building the analyze-text URL and POSTing a JSON body. Ensure boolean values in the JSON are proper booleans (true / false), not strings. Use the endpoint that you copied from Keys and Endpoint. The endpoint should usually end with a trailing slash (or adjust URL concatenation accordingly).

Example Python REST code:

```python theme={null}
# python
import requests
import json

def sentiment_analysis(endpoint: str, key: str, text: str):
    """
    Call the Azure Language analyze-text REST API for sentiment analysis.
    The endpoint should include the trailing slash, e.g. "https://<name>.cognitiveservices.azure.com/".
    """
    url = f"{endpoint}language/:analyze-text?api-version=2023-04-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = {
        "kind": "SentimentAnalysis",
        "parameters": {
            "modelVersion": "latest",
            "opinionMining": True
        },
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": text
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            sentiment_data = response.json()
            document = sentiment_data["results"]["documents"][0]
            print(f"\nDocument Sentiment: {document['sentiment']}")
            scores = document["confidenceScores"]
            print(
                f"Overall scores: positive={scores['positive']:.2f}, "
                f"neutral={scores['neutral']:.2f}, "
                f"negative={scores['negative']:.2f}"
            )
            return document
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as err:
        print(f"Encountered exception: {err}")
        return None

def main():
    endpoint = "https://ai102cogservices909.cognitiveservices.azure.com/"  # Endpoint URL (include trailing slash)
    key = "<YOUR_KEY>"
    sample_text = "The food and service were unacceptable."
    print("Performing sentiment analysis:")
    sentiment_analysis(endpoint, key, sample_text)

if __name__ == "__main__":
    main()
```

Notes on the REST example:

* The REST payload reveals the exact request structure (kind, parameters, analysisInput.documents).
* Set "opinionMining": true to enable opinion mining in results; omit or set false if not needed.
* The header shown uses Ocp-Apim-Subscription-Key; depending on your resource type, you may also see header variants (follow the current Azure REST docs).

## Comparing results and examples

Both SDK and REST return a sentiment label and confidence scores. Example inputs and typical outcomes:

* "Learning AI is good for career growth." — typically returns positive with a high positive confidence score.
* "The food and service were unacceptable." — typically returns negative.
* Mixed content — e.g., "Hotel is awesome. The food and service were unacceptable." — shows how per-sentence analysis can reveal mixed sentiments inside a single document.

Use per-sentence results when you need more granular insights about different parts of a document.

## Best practices & next steps

* For production, never hard-code credentials. Use:
  * Azure Key Vault
  * Managed identities (when running in Azure)
  * Environment variables with secure deployment pipelines
* Prefer SDKs for simpler, cleaner code and better integration with client libraries.
* Use REST for custom clients, language/platforms without an SDK, or to inspect raw payloads.

<Callout icon="warning">
  Always restrict and rotate keys regularly. Grant the minimum required permissions and monitor usage for unexpected calls.
</Callout>

You can apply the same patterns shown here to other Azure AI services (Vision, Speech, OpenAI, Content Safety). In later examples we'll use a mix of SDKs and other languages (for example, C#/.NET) where applicable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/10ea4eb0-486e-4464-a864-dda671e1b308/lesson/ebf9325a-2e32-4fc7-9d93-187cb7347f2e" />
</CardGroup>


# Azure AI Search

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Introduction-to-AI-and-Azure-AI-Services/Azure-AI-Search/page

Overview of Azure AI Search, an AI-powered service that enriches, indexes, and semantically ranks documents using OCR, NLP, embeddings, and knowledge mining for improved enterprise search

Azure AI Search (formerly Azure Cognitive Search) is an AI-powered search and knowledge-mining service that helps users find the most relevant information across large, heterogeneous data collections. It combines document cracking, AI enrichment, indexing, semantic ranking, and querying to turn raw documents into actionable, searchable knowledge.

Key SEO terms: Azure AI Search, Azure Cognitive Search, AI enrichment, semantic ranking, vector search, knowledge mining, indexing, OCR, entity recognition.

## What Azure AI Search does — at a glance

* AI-powered indexing: Automatically extracts and structures searchable fields from documents, databases, and file stores.
* Natural-language understanding: Uses NLP to interpret user intent and return conceptually relevant results beyond exact keyword matches.
* Semantic ranking: Prioritizes results that are most relevant by understanding relationships between words and concepts.
* Knowledge mining: Extracts entities, key phrases, and relationships from structured and unstructured sources (PDFs, images, spreadsheets, etc.) for downstream use.

|              Capability | What it does                                                                                  | Typical use case                                                       |
| ----------------------: | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
|     AI-powered indexing | Enriches content (OCR, entity extraction, key phrases) and converts it into searchable fields | Indexing large sets of PDFs or scanned documents for enterprise search |
| Natural-language search | Interprets intent and matches concepts rather than exact keywords                             | Conversational search queries like “top-selling product in Q1”         |
|        Semantic ranking | Ranks results using embeddings/semantic models to surface most helpful answers                | Improving relevance for question-answering or knowledge base lookups   |
|        Knowledge mining | Detects entities and builds relationships across documents                                    | Building knowledge graphs or metadata layers for BI and analytics      |

<Frame>
  <img alt="A presentation slide titled &#x22;Azure AI Search&#x22; with the tagline &#x22;An intelligent search and data exploration service powered by AI.&#x22; It shows colored feature boxes labeled AI-Powered Indexing, Cognitive Search, Semantic Ranking, Knowledge Mining, and a note about extracting insights from structured and unstructured data." />
</Frame>

## How Azure AI Search works — the pipeline

Azure AI Search usually follows a simple pipeline: ingestion → AI enrichment → indexing → querying. Each stage transforms your raw data into structured, searchable knowledge.

1. Raw data sources
   * Files, blobs, databases, or other storage systems.
2. AI enrichment pipeline
   * Applies cognitive skills such as OCR (for scanned images), entity recognition, key-phrase extraction, language detection, translation, and custom skills to extract structured content from unstructured documents.
3. Indexing
   * Converts enriched content into a searchable index: text fields, filters, facets, scoring profiles, and optionally vector embeddings for semantic or vector search.
4. Querying and ranking
   * Applications and users query the index using text queries, filters, facets, or semantic queries. Results are ranked by relevance, scoring profiles, and semantic ranking when enabled.

| Pipeline stage | Primary function                                    | Output                                |
| -------------- | --------------------------------------------------- | ------------------------------------- |
| Ingestion      | Bring raw files and data into the pipeline          | Documents/blobs/records               |
| AI enrichment  | Extract structured fields and metadata from content | Enriched documents (JSON)             |
| Indexing       | Create searchable index and optional vectors        | Search index with fields & embeddings |
| Querying       | Execute queries and return ranked results           | Ranked search results & facets        |

<Frame>
  <img alt="A diagram titled &#x22;Azure AI Search&#x22; showing data (storage/files) being document-cracked and sent through an AI enrichment pipeline into an indexing process. The indexed output becomes a searchable index, with a developer/user represented at the bottom." />
</Frame>

<Callout icon="lightbulb">
  If terms like "indexing", "AI enrichment", or "skillset" are unfamiliar, think of them this way: indexing is how documents are organized for fast search; enrichment is the AI work that extracts searchable metadata; a skillset is the collection of enrichment steps (OCR, entity extraction, custom code).
</Callout>

## Core concepts explained

* Index: A data structure that Azure Search uses to enable fast search operations (fields, data types, analyzers).
* Skillset: A pipeline of cognitive skills that transform raw content into enriched JSON fields.
* Cognitive skills: Prebuilt (OCR, language detection) or custom functions that extract entities, key phrases, or apply business logic.
* Semantic configurations: Settings that enable semantic ranking and passage retrieval using embeddings or language models.
* Vector/semantic search: Uses vector embeddings to find conceptually similar content, especially useful for natural language queries and question-answering.

## Example: Minimal REST search request

Below is a simplified example of a search POST request to an Azure Search index (semantic search preview API). Replace placeholders with your service name, index name, and API key.

```http theme={null}
POST https://<your-service>.search.windows.net/indexes/<index-name>/docs/search?api-version=2021-04-30-Preview
api-key: <your-api-key>
Content-Type: application/json

{
  "search": "top-selling product in Q1",
  "queryType": "semantic",
  "semantic": {
    "configuration": "default"
  },
  "top": 5
}
```

Use the latest API version for production and consult Azure docs for semantic features and vector search options:

* [https://learn.microsoft.com/azure/search/](https://learn.microsoft.com/azure/search/)

## When to use Azure AI Search

* Enterprise search portals across documents and knowledge bases.
* Customer support knowledge bases, to power FAQ and conversational interfaces.
* Content discovery for digital asset management (images, video transcripts, PDFs).
* Building knowledge graphs and downstream analytics from mined entities.

## Quick-start checklist

* Create an Azure AI Search service in the Azure portal.
* Define an index schema for fields and data types.
* Create a skillset for AI enrichments (OCR, named-entity recognition, key phrases).
* Run indexer to ingest and enrich documents.
* Configure semantic settings or vector search for better relevance.
* Integrate via REST SDKs or client libraries and tune scoring profiles.

## Links and references

* [Azure AI Search documentation](https://learn.microsoft.com/azure/search/)
* [Azure Cognitive Services overview](https://learn.microsoft.com/azure/cognitive-services/)
* [Semantic search with Azure Cognitive Search](https://learn.microsoft.com/azure/search/semantic-search-overview)

We have completed the introduction to Azure AI Services. Upcoming lessons will cover how to deploy these services, configure indexes and skillsets, and make REST API calls to interact with the search service.

<Callout icon="lightbulb">
  Next up: hands-on configuration — creating a search service, defining an index, and applying AI enrichments to real data.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/608629a7-1574-4eb2-95a4-f026fc8888b2/lesson/30f13e1a-767e-4d36-a46e-f07812ace779" />
</CardGroup>
