# Python (conceptual)
result = client.analyze(
    image_url="<uri-to-image>",
    visual_features=[
        VisualFeatures.CAPTION,
        VisualFeatures.PEOPLE,
    ],
    <analysis_options>  # Optional analysis options (e.g., language, gender_neutral_caption)
)
```

### Visual features (examples)

| Visual Feature | What it returns                                           |
| -------------- | --------------------------------------------------------- |
| Caption        | Short descriptive caption and confidence                  |
| Objects        | Detected objects with bounding boxes and confidence       |
| People         | Detected people with bounding boxes and confidence        |
| Read / OCR     | Text regions and recognized text                          |
| Tags           | Labels/tags with confidence scores                        |
| Smart Crops    | Suggested crop bounding boxes for specified aspect ratios |
| Dense Captions | Multiple region captions with context                     |

## Analysis options

You can tune the behavior of the analysis call with these options:

* Cropping aspect ratios — request smart-crop suggestions for thumbnail generation or fixed aspect ratios.
* Gender-neutral captioning — enable gender-neutral language for generated captions.
* Language selection — specify language for OCR and captions.
* Model versioning — pin to a specific model for reproducible results.
* Additional flags — options vary between SDKs and REST; consult the model-name and API docs.

<Frame>
  <img alt="A dark-themed infographic titled &#x22;Image Analysis options&#x22; that lists configurable settings for image analysis. It highlights four features: Cropping Aspect Ratios, Gender-Neutral Captioning, Language Selection, and Model Versioning, each with an icon and short description." />
</Frame>

### Example: setting analysis options

C# (conceptual):

```csharp theme={null}
ImageAnalysisOptions options = new ImageAnalysisOptions {
    GenderNeutralCaption = true,
    Language = "en"
};
ImageAnalysisResult result = client.Analyze(
    imageURL,
    visualFeatures,
    options
);
```

Python (conceptual):

```python theme={null}
result = client.analyze(
    image_url=image_url,
    visual_features=visual_features,
    gender_neutral_caption=True,
    language="en"
)
```

## Image analysis results

Responses from the service are structured and predictable so you can parse them reliably. Typical top-level sections:

* captionResult — best caption and confidence
* objectsResult — array of detected objects with bounding boxes and confidence
* peopleResult — array of people detections with bounding boxes and confidence
* smartCropsResult — suggested crop boxes for requested aspect ratios
* tagsResult / tags — label/tag information and confidence
* read / ocr results — recognized text blocks/lines
* metadata — image dimensions and format
* modelVersion — the model used for inference

<Frame>
  <img alt="A dark-themed infographic titled &#x22;Image Analysis Result&#x22; with four colored panels labeled Caption Result, Object Detection, Smart Crops, and Hierarchical Data, each showing an icon and a short description. It explains that successful image analysis returns structured data (JSON/SDK)." />
</Frame>

Example JSON structure (illustrative):

```json theme={null}
{
  "captionResult": {
    "text": "a man pointing at a screen",
    "confidence": 0.4891590476036072
  },
  "objectsResult": {
    "values": [
      {
        "name": "laptop",
        "confidence": 0.95
      }
    ]
  },
  "smartCropsResult": {
    "values": [
      {
        "aspectRatio": 1.33,
        "boundingBox": {
          "x": 0,
          "y": 0,
          "w": 0,
          "h": 0
        }
      }
    ]
  },
  "peopleResult": {
    "values": [
      {
        "boundingBox": { "x": 164, "y": 21, "w": 329, "h": 378 },
        "confidence": 0.9396107197
      }
    ]
  },
  "metadata": {
    "width": 600,
    "height": 400
  },
  "modelVersion": "latest"
}
```

Use these fields to:

* render captions for accessibility,
* draw bounding boxes for objects and people,
* select recommended crops for thumbnails, and
* display detected tags and OCR text in the UI.

## Hands-on: Python SDK example

Install the Azure AI Vision package for Python:

```bash theme={null}
pip install azure-ai-vision
```

<Callout icon="lightbulb">
  Replace endpoint and key values below with the endpoint and key from your Azure AI service (Keys and Endpoint in the Azure portal). Never commit production keys into source control.
</Callout>

A consolidated, practical Python example demonstrating initialization, choosing visual features, calling analysis, and parsing results safely:

```python theme={null}
# python
import json
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Replace with your service values
endpoint = "https://<your-endpoint>.cognitiveservices.azure.com/"
key = "<your-key>"

# Example image URL (replace as needed)
image_url = "https://azai102imagestore.blob.core.windows.net/images/young-smiling-happy-cheerful-owner-600nw-2397244269.webp"

# Initialize client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Select features
visual_features = [
    VisualFeatures.TAGS,
    VisualFeatures.OBJECTS,
    VisualFeatures.CAPTION,
    VisualFeatures.DENSE_CAPTIONS,
    VisualFeatures.READ,
    VisualFeatures.SMART_CROPS,
    VisualFeatures.PEOPLE,
]

# Request analysis
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=visual_features,
    smart_crops_aspect_ratios=[0.9, 1.33],
    gender_neutral_caption=True,
    language="en"
)

# Format SDK response into a dict for flexible parsing
try:
    result_dict = result.as_dict() if hasattr(result, "as_dict") else dict(result)
    print("Raw response as formatted JSON:")
    print(json.dumps(result_dict, indent=2))
    print("\n")
except Exception as e:
    print(f"Could not format result as JSON: {str(e)}")
    print(f"Raw response: \n {result} \n\n")
    result_dict = {}

# Helper: safe nested getter
def safe_get(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

# Parse people
people = safe_get(result_dict, "peopleResult", "values", default=[])
if people:
    print("People detected:")
    for person in people:
        bbox = person.get("boundingBox", {})
        confidence = person.get("confidence", 0)
        print(f"  Bounding Box: x={bbox.get('x')}, y={bbox.get('y')}, width={bbox.get('w')}, height={bbox.get('h')}")
        print(f"  Confidence: {confidence:.2f}")
else:
    print("No people detected.")

# Parse caption
caption = safe_get(result_dict, "captionResult")
if caption:
    text = caption.get("text", "")
    conf = caption.get("confidence", 0)
    print(f"\nCaption: {text} (Confidence: {conf:.2f})")

# Parse tags (some responses use tagsResult.values or tags)
tags = safe_get(result_dict, "tagsResult", "values", default=None)
if tags is None:
    tags = safe_get(result_dict, "tags", default=None)

if tags:
    print("\nTags:")
    for t in tags:
        name = t.get("name") or (t.get("tag", {}) or {}).get("name")
        confidence = t.get("confidence", 0)
        print(f"  {name}: {confidence:.2f}")

# Parse objects
objects = safe_get(result_dict, "objectsResult", "values", default=[])
if objects:
    print("\nObjects:")
    for obj in objects:
        name = obj.get("name") or "object"
        confidence = obj.get("confidence", 0)
        bbox = obj.get("boundingBox", {})
        print(f"  {name}: bbox={bbox}, confidence={confidence:.2f}")

# Metadata & model version
metadata = safe_get(result_dict, "metadata", default={})
if metadata:
    print(f"\nImage width: {metadata.get('width')}, height: {metadata.get('height')}")
print(f"Model version: {result_dict.get('modelVersion')}")
```

This script:

* Initializes ImageAnalysisClient with your endpoint and key.
* Chooses the visual features to analyze.
* Calls analyze\_from\_url with optional analysis options.
* Prints the raw JSON response and demonstrates robust parsing of common result sections (people, caption, tags, objects).

<Callout icon="warning">
  Protect your API keys: rotate keys regularly, store secrets in a secure vault (e.g., Azure Key Vault), and avoid hard-coding secrets in source control.
</Callout>

## Live demonstration notes and best practices

* Provision an [Azure AI service](https://learn.microsoft.com/azure/ai-services/overview) in the [Azure portal](https://portal.azure.com). Use the Keys and Endpoint values from the portal for your client.
* Use blob storage URLs or public URLs for images. For private images, upload binary image bytes in the request body.
* Gender-neutral captions help avoid gender assumptions in generated text (e.g., "a person hugging a dog").
* Smart crops return bounding boxes for the aspect ratios you specify—use these to create thumbnails that preserve important content.
* Pin model versions for reproducible results; use "latest" for new features and model improvements.
* Always validate and sanitize service outputs before surface-level display in production applications.

Example parsed output (illustrative):

```text theme={null}
People detected!
  Bounding Box: x=164, y=21, width=329, height=378
  Confidence: 0.94

Caption: a person hugging a dog (Confidence: 0.89)

Tags:
  pet: 0.90
  golden retriever: 0.89

Model version: latest
```

## Links and references

* [Azure AI Vision overview](https://learn.microsoft.com/azure/cognitive-services/vision/ai-vision/overview)
* [Analyze concept: Image Analysis](https://learn.microsoft.com/azure/cognitive-services/vision/ai-vision/concept-analyze)
* [Azure AI services: overview](https://learn.microsoft.com/azure/ai-services/overview)
* [Azure portal](https://portal.azure.com)
* [azure-ai-vision PyPI package](https://pypi.org/project/azure-ai-vision/)

This guide demonstrates how to call Azure AI Vision to obtain captions, detect objects and people, extract OCR text, and request smart crops. Use these structured outputs to annotate images, drive UI decisions (smart cropping), and provide accessible descriptions for your applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/5cda8d31-98d4-41a8-bf89-637b6195487b/lesson/16e7ad3b-4b32-4224-a7d0-8b8696372cbb" />
</CardGroup>


# Azure AI Language Services

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyzing-Text/Azure-AI-Language-Services/page

Overview of Azure AI Language Services and its text analysis capabilities, examples and best practices for summarization, entity recognition, PII redaction, sentiment, and SDK or REST integration

Azure AI Language Services is a suite of AI-powered text-processing tools that help researchers, analysts, and developers extract meaning from large volumes of text. Use cases include document summarization, key insight extraction, PII detection and redaction, entity recognition and linking, and automated Q\&A generation — all designed to speed up workflows so you can focus on insights instead of manual reading.

Imagine you’re a researcher with hundreds of papers to review: reading each in full is impractical, and producing summaries or question/answer material is time-consuming. Azure AI Language Services automates the heavy lifting so you can review findings faster and act on results.

<Frame>
  <img alt="A slide titled &#x22;Azure AI Language Services&#x22; showing an illustration of a person working on a laptop at a desk. Two callouts list pain points: &#x22;Too many research papers to read.&#x22; and &#x22;Summarizing and creating Q&A takes forever.&#x22;" />
</Frame>

You can call Azure AI Language features from client SDKs or directly via the REST API. Prebuilt models let you perform common tasks immediately; if you need domain-specific behavior you can train or configure custom models.

<Callout icon="lightbulb">
  Access Azure AI Language via SDKs (Python, JavaScript, .NET) or the REST API. Prebuilt endpoints accelerate common scenarios (summarization, NER, sentiment), while custom models and prompt tuning help adapt results to your data and workflow.
</Callout>

## Core capabilities

Below are the primary text-analysis capabilities available in Azure AI Language Services, with typical use cases and short descriptions to help you choose the right tool.

| Capability                     | What it does                                                                                              | Typical use case                                                           |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Language detection             | Detects the language of a text snippet and returns a language code and confidence score                   | Route multilingual content to the appropriate processing pipeline or model |
| Key phrase extraction          | Identifies main phrases and concepts in text                                                              | Summarize meeting notes or index documents for search                      |
| Sentiment analysis             | Classifies text sentiment (positive / neutral / negative), often with sentence-level scores               | Monitor customer feedback or flag negative comments for escalation         |
| Named Entity Recognition (NER) | Extracts entities (people, organizations, locations, products) and labels their types                     | Build knowledge graphs, power search facets, or tag documents              |
| Entity linking                 | Links recognized entities to an external knowledge base (e.g., Wikipedia or custom KB)                    | Enrich extracted entities with canonical identifiers and external context  |
| Summarization                  | Produces concise summaries (extractive or abstractive) of long documents                                  | Provide quick overviews of long reports, papers, or transcripts            |
| PII detection & redaction      | Identifies and optionally redacts personally identifiable information (credit cards, SSNs, phone numbers) | Ensure compliance and privacy before sharing or storing data               |

<Frame>
  <img alt="A slide titled &#x22;Azure AI Language Capabilities&#x22; showing three feature panels. They list Entity Linking (connects recognized entities to external knowledge bases), Summarization (creates concise summaries), and PII Detection (identifies and redacts sensitive personal data)." />
</Frame>

## Quick examples

The examples below illustrate how to call Language capabilities. Replace \<your-resource-endpoint> and \<your-key-or-token> with your Azure resource values.

<Callout icon="lightbulb">
  Use the REST API for platform-agnostic integration; use an SDK for ergonomics and built-in authentication helpers. Refer to the official API docs for the exact endpoint and API version you should use.
</Callout>

### REST (curl) — Language detection (illustrative)

```bash theme={null}
curl -X POST "https://<your-resource-endpoint>/language/:analyze?api-version=2023-10-01" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-access-token>" \
  -d '{
    "kind": "languageDetection",
    "analysisInput": {
      "documents": [
        { "id": "1", "text": "Este es un texto de ejemplo." }
      ]
    },
    "parameters": {}
  }'
```

Response (trimmed, illustrative):

```JSON theme={null}
{
  "results": [
    {
      "id": "1",
      "detectedLanguage": { "language": "es", "confidenceScore": 0.99 }
    }
  ]
}
```

### SDK (Python) — Summarization (illustrative)

```Python theme={null}
from azure.ai.language import TextAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-resource-endpoint>"
key = "<your-key>"

client = TextAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = ["Long document text to summarize..."]
response = client.begin_analyze_actions(
    documents,
    actions=[
        {"kind": "abstractiveSummarization", "parameters": {}}
    ]
).result()

for doc in response:
    print(doc)
```

Note: SDK names, classes, and method signatures evolve; consult the official SDK docs for the latest samples and installation instructions.

## Best practices

* Preprocess text to remove irrelevant formatting and noise (HTML tags, scripts) before analysis.
* For large-scale document processing, batch inputs and parallelize requests within service limits.
* When working with sensitive data, prefer PII redaction and follow your organization’s compliance policies.
* Validate entity linking results against your knowledge base before automatic ingestion.

## Links and references

* Azure AI Language overview: [https://learn.microsoft.com/azure/ai-services/language/](https://learn.microsoft.com/azure/ai-services/language/)
* REST API and endpoint reference: [https://learn.microsoft.com/azure/ai-services/language/reference](https://learn.microsoft.com/azure/ai-services/language/reference)
* SDK documentation and samples:
  * Python: [https://learn.microsoft.com/azure/ai-services/language/sdk/python](https://learn.microsoft.com/azure/ai-services/language/sdk/python)
  * JavaScript: [https://learn.microsoft.com/azure/ai-services/language/sdk/javascript](https://learn.microsoft.com/azure/ai-services/language/sdk/javascript)
  * .NET: [https://learn.microsoft.com/azure/ai-services/language/sdk/dotnet](https://learn.microsoft.com/azure/ai-services/language/sdk/dotnet)
* Example external KB for entity linking: [https://en.wikipedia.org/wiki/Albert\_Einstein](https://en.wikipedia.org/wiki/Albert_Einstein)

This article introduced the core Azure AI Language features and provided quick REST and SDK examples to get you started. For production deployments, review the service limits, authentication models (API key vs. Azure AD), and pricing on the official Azure documentation pages.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/c9630dfe-8597-4a05-bb2f-de84e8e2a7b7/lesson/c823fa0b-6f18-4b04-980b-10d5a7a78911" />
</CardGroup>
