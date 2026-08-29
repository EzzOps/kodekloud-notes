# Example assumes `result` is the output from the analyzed document (begin_analyze_document / analyze_document)
# Iterate over pages, lines, words, and selection marks
for page in result.pages:
    print(f"\nLines found on page {page.page_number}")
    for line in page.lines:
        print(f"...Line: '{line.content}' (confidence: {line.confidence})")
    if page.words:
        for word in page.words:
            print(f"...Word: '{word.content}' (confidence: {word.confidence})")
    if page.selection_marks:
        for selection_mark in page.selection_marks:
            print(
                f"...Selection mark: '{selection_mark.state}' (confidence: {selection_mark.confidence})"
            )

# Iterate over tables found in the result
for i, table in enumerate(result.tables, start=1):
    # Print pages where the table exists using bounding_regions
    pages = ", ".join(str(region.page_number) for region in table.bounding_regions)
    print(f"\nTable {i} can be found on page(s): {pages}")
    for cell in table.cells:
        print(
            f"...Cell[{cell.row_index}][{cell.column_index}] has content: '{cell.content}'"
        )

print("---------------------------------------------------------")
```

Adapt this snippet to map extracted field names (from the model output) into your application's domain model and persist results (database, search index, or business workflows).

> **lightbulb** You can find full Python and JavaScript examples in the studio's code snippets and the [official SDK documentation](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/client-libraries) to integrate trained models into your applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/d5494e2e-898f-4862-ae4f-f873811c9044)


# Working with Document Intelligence Service

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Working-with-Document-Intelligence-Service/page

Guide to Azure AI Document Intelligence covering REST and SDK calls, polling for results, interpreting structured OCR outputs, and testing prebuilt document models in Document Intelligence Studio.

Working with Azure AI Document Intelligence — practical guidance for calling the API, handling results, and using prebuilt models in the portal.

This article shows the common request pattern (REST and SDK), how to poll and retrieve results, what the structured response contains, and how to test prebuilt models in Document Intelligence Studio.

How the API call pattern works

1. Set up the request — define your resource endpoint and include the API key to authenticate.
2. Send the request — the service accepts the request and returns a poller/tracker. For REST this is the Operation-Location response header; SDKs handle polling internally.
3. Retrieve results — poll the Operation-Location URL until the operation completes (REST) or call the SDK's wait/complete mechanism to get the final results.

> **lightbulb** When using the REST API you must explicitly poll the Operation-Location URL to receive results. SDKs abstract the polling and return a language-native result object when processing completes.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Calling the API&#x22; showing a three-step horizontal flow. Steps: set up the request with resource endpoint and key, send the request and receive a poller to track results, then query the poller to retrieve extracted data." />
</Frame>

REST call pattern example
Below is a minimal REST POST to the prebuilt layout analyze endpoint. Note the Operation-Location header returned after submission — you poll that URL to check the status and fetch results.

```http theme={null}
POST {endpoint}/documentintelligence/documentModels/prebuilt-layout:analyze?api-version={version}
Ocp-Apim-Subscription-Key: {key}
Content-Type: application/json

{
  "urlSource": "{document_url}"
}
```

Example Operation-Location response header:

```text theme={null}
Operation-Location:
{endpoint}/documentintelligence/documentModels/prebuilt-layout/analyzeResults/ab12345c-12ab-23cd-b19c-2322a7f11034?api-version={version}
```

The api-version parameter in the request and operation URL selects which API behavior/version you want to use when Microsoft introduces changes.

SDK usage (C# and Python)

* C# (Azure SDK): call AnalyzeDocumentFromUriAsync, wait for completion, then read Operation.Value for the AnalyzeResult.

```csharp theme={null}
AnalyzeDocumentOperation operation = await client.AnalyzeDocumentFromUriAsync(
    WaitUntil.Completed,
    "prebuilt-layout",
    fileUri
);

AnalyzeResult result = operation.Value;
// result contains extracted contents such as text, tables, and layout information
```

* Python (Azure SDK): start the analysis with a begin\_\* method and call poller.result() to obtain the structured result object.

```python theme={null}
poller = document_analysis_client.begin_analyze_document_from_url(
    "prebuilt-document",
    doc_url
)

result = poller.result()
