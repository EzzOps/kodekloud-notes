# Working with Azure AI Language Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyzing-Text/Working-with-Azure-AI-Language-Services/page

Guide to Azure AI Language Services text analysis features and examples, covering language detection, key phrase extraction, sentiment, named entity recognition, entity linking, summarization, and PII detection.

This guide demonstrates the core text-analysis capabilities available in Azure AI Language Services. It covers language detection, key phrase extraction, sentiment analysis, named entity recognition (NER), entity linking, summarization, and PII detection — with REST-style JSON payload examples and concise Python SDK snippets that illustrate common usage patterns.

Use these features to build multilingual, privacy-aware, and searchable applications that extract meaningful information from unstructured text.

> **warning** Never hard-code secrets (endpoint, keys) in production code. Store credentials in environment variables or a secure secrets store and load them at runtime.

> **lightbulb** For local testing, put your Azure Language endpoint and key in environment variables (or a .env file) and load them at runtime. The samples below assume you already have those values available.

***

## At-a-glance: capabilities and common SDK methods

|                     Capability | Typical use case                                              | Python SDK method (concise)                    |
| -----------------------------: | ------------------------------------------------------------- | ---------------------------------------------- |
|             Language detection | Identify language and confidence score                        | client.detect\_language(...)                   |
|          Key phrase extraction | Discover important topics for indexing or summarization       | client.extract\_key\_phrases(...)              |
|             Sentiment analysis | Classify text sentiment at document and sentence level        | client.analyze\_sentiment(...)                 |
| Named entity recognition (NER) | Extract people, organizations, locations, dates, emails, etc. | client.recognize\_entities(...)                |
|                 Entity linking | Resolve entities to external sources (e.g., Wikipedia)        | client.recognize\_linked\_entities(...)        |
|                  Summarization | Generate extractive or abstractive summaries                  | Check SDK docs — some methods are long-running |
|      PII detection & redaction | Detect and optionally redact sensitive personal data          | client.recognize\_pii\_entities(...)           |

For full API reference and details about model versions, see the Azure AI Language Service documentation: [https://learn.microsoft.com/azure/cognitive-services/language-service/](https://learn.microsoft.com/azure/cognitive-services/language-service/)

***

## Language detection

Detects the language of a text and returns a confidence score. It supports automatic detection across many scripts (Latin, Arabic, Chinese, etc.). You can optionally provide a country hint to influence detection, but it is not required.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Language Detection&#x22; with three numbered panels that list features: automatic language detection, support for multiple scripts, and returning confidence scores. Each panel includes a small icon and brief explanatory text." />
</Frame>

Example request payload (REST-style):

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "countryHint": "Spain",
      "text": "Hola, ¿cómo estás?"
    },
    {
      "id": "2",
      "text": "Guten Morgen, wie geht es Ihnen?"
    }
  ]
}
```

Illustrative response structure:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "detectedLanguage": {
        "name": "Spanish",
        "iso6391Name": "es",
        "confidenceScore": 0.99
      }
    },
    {
      "id": "2",
      "detectedLanguage": {
        "name": "German",
        "iso6391Name": "de",
        "confidenceScore": 0.98
      }
    }
  ]
}
```

Python SDK example — detects primary language and prints confidence:

```python theme={null}
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

input_texts = [
    "Bonjour tout le monde, je suis ravi de vous rencontrer.",
    "Hola, ¿cómo estás?",
    "مرحبا، كيف حالك؟"
]

credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

response = client.detect_language(documents=input_texts)

for idx, doc in enumerate(response):
    if not doc.is_error:
        lang = doc.primary_language
        print(f"Text: {input_texts[idx]}")
        print(f"Detected Language: {lang.name} (ISO: {lang.iso6391_name}, Confidence: {lang.confidence_score:.2f})\n")
    else:
        print(f"Error detecting language for doc {idx + 1}: {doc.error}")
```

***

## Key phrase extraction

Extracts prominent words and short phrases (topics) from text. This is helpful for search indexing, content tagging, and summarization—best applied to longer passages.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Key Phrase Extraction&#x22; with three numbered panels. The panels note: 01 Extracts key topics or phrases from text; 02 Works best with longer text passages; 03 Useful for summarization and search optimization." />
</Frame>

Request payload example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "Artificial intelligence is transforming industries with automation and analytics."
    },
    {
      "id": "2",
      "language": "en",
      "text": "Climate change is a critical issue that affects global economies and ecosystems."
    }
  ]
}
```

Illustrative response:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "keyPhrases": [
        "Artificial intelligence",
        "automation",
        "analytics"
      ]
    },
    {
      "id": "2",
      "keyPhrases": [
        "Climate change",
        "global economies",
        "ecosystems"
      ]
    }
  ]
}
```

Python SDK example — extract key phrases from a single long document:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

documents = [
    "Golden retrievers are one of the most popular dog breeds, known for their friendly, intelligent, and devoted nature. They are excellent family pets and are often used as guide dogs, therapy dogs, and in search-and-rescue operations due to their trainability and gentle temperament."
]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.extract_key_phrases(documents=documents)

for idx, doc in enumerate(response):
    print(f"\nText: {documents[idx]}")
    if not doc.is_error:
        print("\nKey Phrases:")
        for phrase in doc.key_phrases:
            print(f" - {phrase}")
    else:
        print(f"Document error: {doc.error}")
```

***

## Sentiment analysis

Classifies documents (and sentences) as positive, neutral, negative, or mixed and returns confidence scores. Useful for product feedback, social-media analysis, and customer support automation.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Sentiment Analysis&#x22; showing four colored boxes labeled Neutral, Positive, Negative, and Mixed. Each box has a short description explaining which sentence sentiments (neutral, positive, negative, or combinations) it represents." />
</Frame>

Request example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "I love the new design! However, the app crashes frequently, which is frustrating."
    }
  ]
}
```

Illustrative response structure — shows document sentiment, sentence-level labels, and confidence scores:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "sentiment": "mixed",
      "confidenceScores": {
        "positive": 0.65,
        "neutral": 0.10,
        "negative": 0.25
      },
      "sentences": [
        {
          "text": "I love the new design!",
          "sentiment": "positive",
          "confidenceScores": { "positive": 0.98, "neutral": 0.01, "negative": 0.01 },
          "offset": 0,
          "length": 24
        },
        {
          "text": "However, the app crashes frequently, which is frustrating.",
          "sentiment": "negative",
          "confidenceScores": { "positive": 0.05, "neutral": 0.10, "negative": 0.85 },
          "offset": 26,
          "length": 59
        }
      ]
    }
  ]
}
```

Python SDK example — analyze sentiment with confidence scores:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

documents = [
    "Golden retriever puppies are the cutest."
]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.analyze_sentiment(documents=documents)

for idx, doc in enumerate(response):
    if not doc.is_error:
        print(f"\nText: {documents[idx]}")
        print(f"Sentiment: {doc.sentiment}")
        scores = doc.confidence_scores
        print(f"Confidence Scores: Positive={scores.positive:.2f}, Neutral={scores.neutral:.2f}, Negative={scores.negative:.2f}")
    else:
        print(f"Error analyzing document {idx + 1}: {doc.error}")
```

***

## Named entity recognition (NER)

NER extracts entities such as people, organizations, locations, datetimes, addresses, emails, and URLs from text. Use this to populate structured metadata, build knowledge graphs, or enhance search relevance.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Named Entity Recognition&#x22; displays six turquoise icons labeled Person, Location, DateTime, Organization, Address, and Email & URL. A caption below reads &#x22;Identify key entities such as people, places, and dates in a text&#x22; with a small &#x22;© Copyright KodeKloud&#x22; in the corner." />
</Frame>

Request example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "Elon Musk announced a new Tesla model in California last Friday."
    }
  ]
}
```

Illustrative response:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "entities": [
        { "text": "Elon Musk", "category": "Person", "confidenceScore": 0.99 },
        { "text": "Tesla", "category": "Organization", "confidenceScore": 0.98 },
        { "text": "California", "category": "Location", "confidenceScore": 0.97 },
        { "text": "last Friday", "category": "DateTime", "confidenceScore": 0.95 }
      ]
    }
  ]
}
```

Python SDK example — recognize and list named entities:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

documents = [
    "The capital of United States is Washington, D.C."
]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.recognize_entities(documents=documents)

for idx, doc in enumerate(response):
    print(f"\nText: {documents[idx]}")
    if not doc.is_error:
        print("\nNamed Entities:")
        for entity in doc.entities:
            print(f"- {entity.text} ({entity.category}, Confidence: {entity.confidence_score:.2f})")
    else:
        print(f"Error: {doc.error}")
```

***

## Entity linking

Entity linking (or entity resolution) maps recognized mentions to entries in an external knowledge base (for example, Wikipedia). This disambiguates mentions such as "Paris" (city) vs "Paris" (person) and provides authoritative metadata (IDs and URLs).

<Frame>
  <img alt="A presentation slide titled &#x22;Entity Linking&#x22; with three numbered panels summarizing benefits: disambiguates similar names, links entities to authoritative sources, and improves search and content categorization." />
</Frame>

Request example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "Apple launched a new iPhone."
    }
  ]
}
```

Illustrative response (entity link output):

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "entities": [
        {
          "name": "Apple",
          "matches": [{"text": "Apple", "offset": 0, "length": 5, "confidenceScore": 0.95}],
          "id": "a1b2c3d4",
          "wikipediaUrl": "https://en.wikipedia.org/wiki/Apple_Inc.",
          "dataSource": "Wikipedia"
        },
        {
          "name": "iPhone",
          "matches": [{"text": "iPhone", "offset": 26, "length": 6, "confidenceScore": 0.97}],
          "id": "x9y8z7w6",
          "wikipediaUrl": "https://en.wikipedia.org/wiki/IPhone",
          "dataSource": "Wikipedia"
        }
      ]
    }
  ]
}
```

Python SDK example — resolve mentions to knowledge sources:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

documents = [
    "Eiffel tower is located in Paris."
]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.recognize_linked_entities(documents=documents)

for idx, doc in enumerate(response):
    print(f"\nText: {documents[idx]}")
    if not doc.is_error:
        print("\nLinked Entities:")
        for entity in doc.entities:
            print(f"- Name: {entity.name}")
            print(f"  ID: {entity.data_source_entity_id}")
            print(f"  URL: {entity.url}")
            print(f"  Source: {entity.data_source}")
            for match in entity.matches:
                print(f"    > '{match.text}' (Confidence: {match.confidence_score:.2f})")
    else:
        print(f"Error: {doc.error}")
```

***

## Summarization

Summarization creates concise representations of long documents. You can choose:

* Extractive summarization — select the most important sentences verbatim.
* Abstractive summarization — generate a rewritten, shorter summary.

Summarization is useful for overviews of documents, slide decks, and long reports. Implementation details vary by SDK version and whether the operation is long-running (poller-based). Consult the Azure docs for the exact method name and behavior in your installed package.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Summarization&#x22; showing three numbered panels with icons. The panels list: extracting key sentences from documents, supporting extractive and abstractive summarization, and usefulness for document analysis and content summarization." />
</Frame>

Input example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "Artificial intelligence is shaping the future. AI helps in automation, decision-making and improving efficiency in various industries."
    }
  ]
}
```

Illustrative extractive summary output:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "sentences": [
        {
          "text": "Artificial intelligence is shaping the future.",
          "rankScore": 0.80
        },
        {
          "text": "AI helps in automation, decision-making, and improving efficiency in various industries.",
          "rankScore": 0.75
        }
      ]
    }
  ]
}
```

***

## Personally Identifiable Information (PII) detection and redaction

PII detection identifies sensitive data such as names, phone numbers, emails, and Social Security numbers. After detection you can redact or mask values to help meet privacy and compliance requirements (for example, GDPR or HIPAA).

<Frame>
  <img alt="A presentation slide titled &#x22;Personally Identifiable Information Detection&#x22; with three numbered feature boxes. It says the system identifies personal details like phone numbers, emails and addresses, redacts sensitive data for privacy compliance, and helps anonymize text." />
</Frame>

Request example:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "language": "en",
      "text": "Contact me at john.doe@email.com or call me at +1-555-123-4567."
    }
  ]
}
```

Illustrative redacted output:

```json theme={null}
{
  "documents": [
    {
      "id": "1",
      "redactedText": "Contact me at *************** or call me at ***************.",
      "entities": [
        { "text": "john.doe@email.com", "category": "Email", "confidenceScore": 0.99 },
        { "text": "+1-555-123-4567", "category": "PhoneNumber", "confidenceScore": 0.98 }
      ]
    }
  ]
}
```

Python SDK example — detect PII entities:

```python theme={null}
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
key = "<your-key>"

documents = [
    "My name is John Doe, and my phone number is (555) 123-4567. My SSN is 123-45-6789."
]

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
response = client.recognize_pii_entities(documents=documents)

for idx, doc in enumerate(response):
    print(f"\nText: {documents[idx]}")
    if not doc.is_error:
        print("\nDetected PII Entities:")
        for entity in doc.entities:
            print(f" - {entity.text} ({entity.category}, Confidence: {entity.confidence_score:.2f})")
    else:
        print(f"Error: {doc.error}")
```

For legal or compliance-sensitive scenarios, combine detection with secure redaction and follow organizational privacy controls.

***

## Example: single Flask app that runs multiple analyses

You can combine multiple analyses in a single application, keeping each call focused and handling errors per document. The example below shows how to load credentials, initialize a client, and call several analyzers (language, key phrases, sentiment, NER, entity linking, and PII) from a Flask route. This compact pattern is suitable for demos and small apps — for production, add proper error handling, rate limiting, and secrets management.

```python theme={null}
import os
from flask import Flask, request, render_template
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
