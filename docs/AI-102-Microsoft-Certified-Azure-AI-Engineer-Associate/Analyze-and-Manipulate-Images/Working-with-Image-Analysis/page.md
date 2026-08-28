# Image URL
image_url = "https://azai102imagestore.blob.core.windows.net/images/note.webp"

# Initialize the client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Analyze the image for read (OCR)
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.READ]
)

try:
    # Convert to a dictionary if the SDK result supports as_dict()
    result_dict = result.as_dict() if hasattr(result, "as_dict") else result

    # Extract text from readResult -> blocks -> lines
    extracted_text = ""
    if "readResult" in result_dict and "blocks" in result_dict["readResult"]:
        for block in result_dict["readResult"]["blocks"]:
            for line in block.get("lines", []):
                extracted_text += line.get("text", "") + "\n"

    print("Extracted Text:\n" + extracted_text)

    # Optionally print the raw JSON (pretty)
    print("Raw JSON output:")
    print(json.dumps(result_dict, indent=2))
except Exception as e:
    print("Error analyzing image:", e)
```

<Callout icon="warning">
  Keep your Azure endpoint and key secure. Do not hard-code secrets in source files; use environment variables or a secrets manager.
</Callout>

## Sample console output

Running the script prints the extracted human-readable text and, optionally, the full JSON structure with model version, metadata, blocks, lines, words, bounding polygons, and confidence scores.

Example printed output:

```text theme={null}
$ python3 app_ocr.py
Extracted Text:
Happy Birthday!
you're the best.
love
Erin

Raw JSON output:
{
  "modelVersion": "2023-10-01",
  "metadata": { "width": 1946, "height": 1946 },
  "readResult": {
    "blocks": [
      {
        "lines": [
          {
            "text": "Happy Birthday!",
            "boundingPolygon": [
              { "x": 3, "y": 2 },
              { "x": 814, "y": 2 },
              { "x": 1383, "y": 312 },
              { "x": 1452, "y": 123 }
            ],
            "words": [
              { "text": "Happy", "confidence": 0.657, "boundingPolygon": [...] },
              { "text": "Birthday!", "confidence": 0.211, "boundingPolygon": [...] }
            ]
          },
          {
            "text": "you're the best.",
            "words": [
              { "text": "you're", "confidence": 0.165 },
              { "text": "the", "confidence": 0.994 },
              { "text": "best.", "confidence": 0.894 }
            ]
          },
          { "text": "love", "words": [{ "text": "love", "confidence": 0.667 }] },
          { "text": "Erin", "words": [{ "text": "Erin", "confidence": 0.666 }] }
        ],
        "language": "en"
      }
    ]
  }
}
```

## Example: Handwritten note

This lesson used a photographed handwritten birthday note. The Read API extracted the content and returned bounding polygons and confidence values for each recognized word, enabling UI overlays or further processing.

<Frame>
  <img alt="A handwritten birthday note on white paper that says, &#x22;Happy Birthday! You're the best. Love, Erin.&#x22; The photo is taken at an angle and shows a cursor near the center." />
</Frame>

## Summary

* Use Vision Read for extracting printed or handwritten text from images (short notes, signs, labels).
* Use Document Intelligence for multi-page, structured, or complex document extraction tasks (receipts, invoices, contracts).
* The Read API returns hierarchical JSON (blocks → lines → words) with bounding polygons and confidence scores — ideal for UI overlays and downstream analytics.
* The provided Python example shows a straightforward integration pattern to call the Read API and extract text.

## Links and References

* [Azure AI Vision Overview](https://learn.microsoft.com/azure/cognitive-services/computer-vision/overview)
* [Azure AI Vision Read API documentation](https://learn.microsoft.com/azure/cognitive-services/vision/ai-vision/overview)
* [Azure SDK for Python](https://learn.microsoft.com/python/api/overview/azure/?view=azure-python)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/5cda8d31-98d4-41a8-bf89-637b6195487b/lesson/95586178-e24f-4288-9777-906825e6bd42" />
</CardGroup>


# Working with Image Analysis

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Analyze-and-Manipulate-Images/Working-with-Image-Analysis/page

Guide to using Azure AI Vision to analyze images via REST and SDKs, configure analysis options, and parse structured results like captions, objects, OCR, and smart crops.

In this lesson we'll explore how to analyze images with Azure AI Vision. You'll learn what goes into image analysis, how to call the service via the REST API and SDKs (C# and Python), how to configure analysis options, and how to parse the structured responses the service returns.

We cover:

* What the Analyze API returns (captions, detected objects and people, OCR/read, smart crops, etc.)
* How to select Visual Features to limit and focus the response
* SDK usage patterns and a full Python example to parse results
* REST usage patterns and a sample query string for the Analyze endpoint
* Practical options (smart crops, language, gender-neutral captions, model versioning)

Key aspects of image analysis are summarized in the table below.

| Resource             | Purpose                                       | Typical Use Case                                               |
| -------------------- | --------------------------------------------- | -------------------------------------------------------------- |
| Analyze API          | Single call to extract visual insights        | Generate captions, detect objects/people, OCR, suggest crops   |
| Visual Features enum | Select which features to return               | Reduce latency and payload by choosing only needed outputs     |
| SDKs (C#, Python)    | Wrap the REST calls and provide typed results | Faster integration in apps and fewer manual request steps      |
| REST API             | Direct HTTPS calls to the analyze endpoint    | Flexibility for non-.NET/Python environments or custom clients |
| Input formats        | Image URL or raw bytes                        | Use blob/storage URLs or upload binary bytes in request body   |

<Frame>
  <img alt="An infographic titled &#x22;Working with Image Analysis&#x22; showing five numbered panels that summarize: Analyze AI Overview, Visual Features Enum, SDK Integration, REST API Usage, and Input Requirements. Each panel includes a short description and an icon explaining the corresponding image-analysis feature." />
</Frame>

## REST API example

A typical REST Analyze request is performed against the Image Analysis endpoint. Example URL (replace \<your-endpoint> and ):

```text theme={null}
https://<your-endpoint>/computervision/imageanalysis:analyze?
features=caption,people&model-name=latest&
language=en&api-version={version}
```

* Query parameters:
  * features — comma-separated visual features to return (example: caption, people, objects, read, smartCrops).
  * model-name — model to use (e.g., latest or a specific version).
  * language — language for captions / OCR results.
  * api-version — service API version.

You include the image either as:

* an image URL in the JSON request body, or
* raw image bytes in the request body (binary upload).

The service responds with structured JSON containing captionResult, objectsResult, peopleResult, smartCropsResult, tagsResult/read results, metadata, and modelVersion.

## SDK usage (C# and Python — conceptual)

SDKs simplify calls and return typed objects. Below are conceptual method signatures to illustrate common patterns.

C# (conceptual):

```csharp theme={null}
// C# (conceptual)
ImageAnalysisResult result = client.Analyze(
    new Uri("<uri-to-image>"),
    VisualFeatures.Caption | VisualFeatures.People,
    analysisOptions // Optional ImageAnalysisOptions
);
```

Python (conceptual):

```python theme={null}
