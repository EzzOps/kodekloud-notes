# OCR Using Azure AI Vision

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyze-and-Manipulate-Images/OCR-Using-Azure-AI-Vision/page

Guide to using Azure AI Vision Read API for OCR, comparing Read and Document Intelligence, explaining JSON output structure and showing a Python example for extracting text and coordinates

Welcome to this lesson on OCR (Optical Character Recognition) with Azure AI Vision. This guide explains how Azure extracts text from images — from photos of signs and labels to scanned documents and handwritten notes — using the Read capability. You’ll learn when to use the Read API versus Document Intelligence, how the JSON output is structured, and how to call the Read feature with a concise Python example.

## When to use Read vs Document Intelligence

Choose the right service based on document complexity and scale.

|               Feature | Best for                                                          | Notes                                                                         |
| --------------------: | ----------------------------------------------------------------- | ----------------------------------------------------------------------------- |
|           Vision Read | Printed or handwritten text in images, short notes, signs, labels | Typically synchronous and optimized for smaller images and short text blocks  |
| Document Intelligence | Multi-page PDFs, invoices, receipts, structured forms             | Richer parsing, field extraction, and often asynchronous for larger workloads |

<Callout icon="lightbulb">
  Document Intelligence is intended for richer document processing (forms, invoices, multi-page PDFs). For short images or quick handwritten notes, the Read feature is usually sufficient and simpler to integrate.
</Callout>

## Key outputs from the Read API

* JSON-based output containing recognized text, confidence scores, and positional coordinates.
* Hierarchical structure (blocks → lines → words) with bounding polygons for each text element.
* Useful for highlighting text in UI overlays, computing coordinates, or downstream analytics.

<Frame>
  <img alt="A presentation slide titled &#x22;OCR using Azure AI Vision&#x22; that outlines four features—Vision Read, Document Intelligence, JSON-Based Output, and Hierarchical Text Data—each shown in colored boxes with brief descriptions. The slide explains extracting text with the READ feature and returning structured data (text, confidence scores, bounding coordinates)." />
</Frame>

## Sample JSON output (excerpt)

The Read API returns structured JSON where each line includes a bounding polygon and words with their own polygons and confidence scores. This abbreviated example demonstrates the typical nesting and coordinates you can expect:

```json theme={null}
[
  {
    "lines": [
      {
        "text": "You must be the change you",
        "boundingPolygon": [
          { "x": 251, "y": 265 },
          { "x": 673, "y": 260 },
          { "x": 674, "y": 308 },
          { "x": 252, "y": 318 }
        ],
        "words": [
          {
            "text": "You",
            "boundingPolygon": [
              { "x": 251, "y": 265 },
              { "x": 320, "y": 260 },
              { "x": 320, "y": 308 },
              { "x": 251, "y": 308 }
            ],
            "confidence": 0.996
          },
          {
            "text": "must",
            "boundingPolygon": [
              { "x": 321, "y": 265 },
              { "x": 380, "y": 260 },
              { "x": 380, "y": 308 },
              { "x": 321, "y": 308 }
            ],
            "confidence": 0.992
          }
        ]
      }
    ]
  }
]
```

This structure makes it straightforward to extract human-readable text, compute confidence metrics, or render spatial overlays in a UI.

## Sample Python code to call Read (ImageAnalysisClient)

The following Python snippet demonstrates calling the Read feature using ImageAnalysisClient, converting the SDK result to a dictionary, and extracting text from readResult → blocks → lines. Ensure you set `endpoint` and `key` variables and install required Azure SDK packages.

```python theme={null}
from azure.ai.vision import ImageAnalysisClient, VisualFeatures
from azure.core.credentials import AzureKeyCredential
import json
