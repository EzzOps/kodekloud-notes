# 'result' now contains structured output: pages, lines, words, tables, fields, etc.
```

Response structure and metadata
The service returns a structured hierarchy that makes it easy to navigate OCR output:

Pages → Lines → Words

This structure lets you extract entire paragraphs, iterate line-by-line, or work with word-level details (content, bounding boxes, confidence, etc.).

<Frame>
  <img alt="A slide titled &#x22;API Response&#x22; showing a three-circle Venn diagram that labels data as structured into Pages, Lines, and Words with &#x22;AWD&#x22; at the center. The design has a dark blue background and a small &#x22;© Copyright KodeKloud&#x22; note." />
</Frame>

A simplified REST JSON snippet (analyzeResult) showing modelId, pages, and word-level data:

```json theme={null}
{
  "analyzeResult": {
    "apiVersion": "{version}",
    "modelId": "prebuilt-invoice",
    "pages": [
      {
        "pageNumber": 1,
        "angle": 0,
        "width": 8.5,
        "height": 11,
        "unit": "inch",
        "words": [
          {
            "content": "Margie's",
            "boundingBox": [
              0.5911,
              0.6857,
              1.7451,
              0.6857,
              1.7451,
              0 ...
            ],
            "confidence": 1.0,
            "span": { "offset": 0, "length": 7 }
          }
        ]
      }
    ]
  }
}
```

The response contains rich metadata — bounding box coordinates, confidence scores, detected text style (including handwriting) — which you can use to validate fields, overlay extracted text on images, or apply post-processing rules.

<Frame>
  <img alt="A dark presentation slide titled &#x22;API Response&#x22; that shows three rounded panels describing additional metadata from an OCR-like API. The panels list: Bounding box coordinates / Detected text, Confidence scores / Accuracy assessment, and Text style details / Handwritten detection." />
</Frame>

Deploying Document Intelligence in Azure and trying prebuilt models
You can create either an AI multi-service (Cognitive Services) resource or a dedicated Document Intelligence resource in the Azure portal. After provisioning, open Document Intelligence Studio to test prebuilt models: invoices, receipts, IDs, health insurance cards, bank statements, and more.

<Frame>
  <img alt="A screenshot of the Azure AI Document Intelligence Studio web interface showing OCR and document-processing options and a grid of prebuilt model cards (Invoices, Receipts, Identity documents, US health insurance cards, etc.). Each card has an icon and a &#x22;Try it out&#x22; link for extracting data from those document types." />
</Frame>

To use a prebuilt model in the Studio, configure the API endpoint and a key for your service and then run sample documents through the UI.

<Frame>
  <img alt="A screenshot of the Azure Document Intelligence Studio welcome dialog, prompting the user to configure a service resource by entering a Document Intelligence/Cognitive Services endpoint and an API key." />
</Frame>

Try sample identity documents (passport, driver’s license, green card, etc.) and inspect extracted fields such as name, date of birth, document number, and expiration.

<Frame>
  <img alt="A screenshot of Azure AI Document Intelligence Studio displaying a scanned U.S. Permanent Resident (green card) image in the center with extracted identity fields (name, date of birth, document number, etc.) shown in a panel on the right. Thumbnails of other sample ID images appear in a left sidebar." />
</Frame>

Python SDK example — analyze an identity document from a URL
This consolidated Python example uses the Document Intelligence SDK to analyze an identity document at a given URL and iterate over extracted fields.

```python theme={null}
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

DOCUMENT_URL = "https://azai102imagestore.blob.core.windows.net/us-id-cards/id1.jpeg"
DOC_INTEL_ENDPOINT = "https://aiservicesai900.cognitiveservices.azure.com/"
DOC_INTEL_KEY = "2nDOsJoeWNZsci1GmRVpC88rpvMsF3wF5KjGqcrSUqmjAXIN6zrLJQQJ99AKACYeBjFXJ3w3AAAAACOGR0oi"

client = DocumentIntelligenceClient(
    endpoint=DOC_INTEL_ENDPOINT,
    credential=AzureKeyCredential(DOC_INTEL_KEY)
)

poller = client.begin_analyze_document(
    model_id="prebuilt-idDocument",
    body={"urlSource": DOCUMENT_URL}
)

result = poller.result()

for i, doc in enumerate(result.documents, start=1):
    print(f"\n— Document #{i} (type: {doc.doc_type}) -----------------------------")
    for name, field in doc.fields.items():
        value = field.content if field.content is not None else "<no value>"
        print(f"{name:20s}: {str(value):30s} (confidence: {field.confidence:.2f})")
```

Sample trimmed output for id1.jpeg:

```text theme={null}
— Document #1 (type: idDocument.residencePermit) -----------------------------
Category             : IRL                            (confidence: 0.55)
CountryRegion        : <no value>                     (confidence: 0.99)
DateOfBirth          : 09 SEP 1988                    (confidence: 0.71)
DateOfExpiration     : 11/12/30                       (confidence: 0.76)
DateOfIssue          : 11/12/20                       (confidence: 0.72)
DocumentNumber       : 000-000-000                    (confidence: 0.72)
FirstName            : TIMOTHY                        (confidence: 0.72)
LastName             : TOMPKINS                       (confidence: 0.75)
PlaceOfBirth         : Ireland                        (confidence: 0.66)
```

Handling download errors
If the service cannot download the document from the supplied URL (for example, wrong filename or access issues) you may receive an HttpResponseError similar to this:

```text theme={null}
azure.core.exceptions.HttpResponseError: (InvalidRequest) Invalid request.
Code: InvalidRequest
Message: Invalid request.
Inner error: {
  "code": "InvalidContent",
  "message": "Could not download the file from the given URL."
}
```

<Callout icon="warning">
  Common causes: incorrect blob name/extension, broken URL, or container not publicly accessible. Ensure the URL is reachable and points to the correct file before re-running the analysis.
</Callout>

Example: wrong extension (id2.jpeg vs id2.jpg) prevented download — after fixing the blob name and re-running the same code against id2.jpg the expected extraction was returned:

```text theme={null}
— Document #1 (type: idDocument.residencePermit) ---------------------------
Category             : IR1                      (confidence: 0.48)
CountryRegion        : <no value>               (confidence: 0.99)
DateOfBirth          : 20 OCT 2002              (confidence: 0.66)
DateOfExpiration     : 10/26/32                 (confidence: 0.71)
DateOfIssue          : 10/25/20                 (confidence: 0.66)
DocumentNumber       : 123-456-789              (confidence: 0.67)
FirstName            : TEST V                   (confidence: 0.65)
LastName             : SPECIMEN                 (confidence: 0.70)
PlaceOfBirth         : Mexico                   (confidence: 0.56)
```

Quick comparison: REST vs SDK

| Feature              | REST API                                      | SDKs (C#, Python, etc.)                               |
| -------------------- | --------------------------------------------- | ----------------------------------------------------- |
| Polling              | Manual polling of Operation-Location required | Polling handled internally (begin\_\* returns poller) |
| Language integration | Raw JSON and headers                          | Language-native objects and helpers                   |
| Error handling       | HTTP status + headers                         | Rich exceptions (typed)                               |
| Ease of use          | More control, more work                       | Faster startup and easier consumption                 |

Best practices and tips

* Use api-version to pin behavior and avoid breaking changes.
* Prefer SDKs for quicker integration and less polling code.
* Validate confidence scores and bounding boxes before trusting critical fields.
* When overlaying text on images, use bounding box coordinates and page dimensions returned in the response.
* Test prebuilt models in Document Intelligence Studio to verify expected fields and sample accuracy.

Links and references

* [Document Intelligence (Azure) documentation](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/)
* [Azure SDK for Python — azure-ai-documentintelligence](https://pypi.org/project/azure-ai-documentintelligence/)
* [C# Azure SDK — Document Intelligence client library](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/quickstarts/client-libraries?pivots=programming-language-csharp)
* [Azure Cognitive Services overview](https://learn.microsoft.com/azure/cognitive-services/)

That demonstrates how to work with Document Intelligence: configure access, call the analyze endpoint (REST or SDK), poll (if REST), and consume the structured output (pages → lines → words and high-level fields).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/55a31339-a704-4760-9398-6225b21fd76e" />
</CardGroup>


# Fine Tuning Question Answering Performance

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Question-Answering-Solution/Fine-Tuning-Question-Answering-Performance/page

Guide to improving Azure Custom Question Answering using implicit learning, explicit user feedback, and synonyms to increase accuracy and relevance.

Improve the accuracy and coverage of a question-answering solution built with Custom Question Answering in Azure Language Studio. This guide explains practical techniques—implicit learning, explicit learning (user feedback), and synonyms—and shows where to make these adjustments in Language Studio to produce faster, more relevant answers.

## Overview

Fine-tuning a QnA knowledge base combines three complementary approaches:

* Implicit learning: automatic alternate phrasing detection.
* Explicit learning: using user feedback to reinforce correct answers.
* Synonyms: mapping equivalent terms to improve intent matching.

These techniques work together to reduce ambiguous matches and increase the hit rate for real user queries.

## Implicit learning (automatic alternate phrasing)

Implicit learning runs behind the scenes to detect alternate phrasings users might use for the same question. For instance, when a user asks, "How do I change my flight?", the system may propose variations such as "Can I modify my booking?" or "I need to update my reservation." Language Studio surfaces these suggested alternates so you can review and accept them into your knowledge base.

Example of a suggestion (as shown in Language Studio):

```json theme={null}
{
  "answers": [
    {
      "questions": ["How do I change my flight?"],
      "answer": "You can modify your flight booking by visiting our airline portal or calling 888-555-7890.",
      "score": 76.55,
      "id": 2
    }
  ]
}
```

<Callout icon="lightbulb">
  Accepting implicit suggestions reduces manual work and helps the system generalize to real user language patterns without you adding every alternate phrasing.
</Callout>

## Explicit learning (user feedback)

Explicit learning collects confirmatory signals from users. When the system returns multiple candidate answers, and a user selects one, that selection is stored as feedback. Over time, feedback helps the model rank the correct answer higher for similar queries by linking the feedback to the matched answer ID.

Example: the answered entry returned to the user:

```json theme={null}
{
  "answers": [
    {
      "questions": ["How do I change my flight?"],
      "answer": "You can modify your flight booking by visiting our airline portal or calling 888-555-7890.",
      "score": 76.55,
      "id": 2
    }
  ]
}
```

Corresponding feedback record sent back to the system:

```json theme={null}
{
  "feedbackRecords": [
    {
      "userId": "user1",
      "userQuestion": "I need to reschedule my flight",
      "matchedId": 2
    }
  ]
}
```

Collecting these feedback records and submitting them to the service incrementally trains the matching behavior so the selected answer is favored for similar future queries.

<Callout icon="warning">
  Collecting user feedback can involve personal data. Ensure you follow your organization’s privacy policy and any applicable legal requirements before storing or sending identifiable feedback.
</Callout>

## Synonyms for better matching

Define synonyms to treat different words or phrases as equivalent for intent matching. This is especially useful for domain-specific vocabulary (e.g., “reschedule”, “modify”, “change” for flight updates).

Example synonyms configuration:

```json theme={null}
{
  "synonyms": {
    "alterations": ["reschedule", "modify", "change"]
  }
}
```

You can add synonyms via the API or directly in Language Studio. When used together with implicit and explicit learning, synonyms increase the system’s robustness to vocabulary variations.

## Where to fine-tune in Language Studio

After deploying your knowledge base, use Language Studio to review and refine content. The primary areas to manage fine-tuning are:

| Area                 | Purpose                                       | Action                                                          |
| -------------------- | --------------------------------------------- | --------------------------------------------------------------- |
| Review Suggestions   | Inspect implicit alternate phrasing proposals | Accept, edit, or reject suggested alternates                    |
| Edit Knowledge Base  | Manual curation of Q\&A pairs                 | Add alternate questions, edit answers, pin or remove alternates |
| Feedback / Telemetry | Submit user selections for explicit learning  | Send feedbackRecords to link user selections to answer IDs      |
| Synonyms             | Normalize vocabulary across questions         | Add synonyms to map equivalent terms to a canonical form        |

In the Review Suggestions (or similar) section, alternate phrasing suggestions appear once the system has observed enough interactions. Initially you may see no suggestions; they populate as user traffic and feedback increase.

Where to perform manual edits in the editor view:

* Add alternate questions for an existing answer (e.g., add "Define Cognitive Services" as an alternate phrasing for "What is Cognitive Services?").
* Remove or pin alternate questions to control which variants are preferred.
* Configure follow-up prompts or multi-turn dialog behavior to handle compound queries.

<Frame>
  <img alt="A screenshot of Azure AI Language Studio's Custom Question Answering editor, showing a knowledge base with question-answer pairs listed on the left and a selected answer plus many alternate questions displayed on the right. The top shows the Azure navigation and user account bar." />
</Frame>

The editor displays each Q\&A entry with its alternate questions and controls to accept, edit, remove, or pin alternates. Use these fine-tuning actions—accepting implicit suggestions, sending explicit feedback, and defining synonyms—to improve accuracy and reduce response ambiguity.

## Best practices

* Start with a focused set of high-confidence Q\&A pairs and grow coverage iteratively.
* Combine synonyms with alternate questions to capture both word-level and phrase-level variants.
* Regularly review suggestion history and feedback telemetry to find gaps or misclassifications.
* Automate feedback submission where appropriate, but always respect privacy and consent.

## Links and references

* [Azure AI Language Studio - Custom Question Answering](https://learn.microsoft.com/azure/ai-services/language/question-answering/overview)
* [Collecting and submitting user feedback](https://learn.microsoft.com/azure/ai-services/language/how-to/feedback)
* [Synonyms and language normalization guidance](https://learn.microsoft.com/azure/ai-services/language/concepts-synonyms)

With these steps, you can systematically fine-tune a Custom Question Answering knowledge base to deliver more accurate and relevant responses to your users.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/f55ce98d-afd9-45b6-8f51-9668bad8705d/lesson/63664277-c207-41bb-b13f-027a95e6202a" />
</CardGroup>
