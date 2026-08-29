# Analyzing Documents Using Custom Model

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Analyzing-Documents-Using-Custom-Model/page

Guide for running a deployed Azure Document Intelligence custom model to analyze documents, authenticate requests, use SDKs, and retrieve structured AnalyzeResult via poller.

Analyze documents with a custom-trained model in [Azure Document Intelligence](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/). This guide covers the authentication and request pattern needed to run a deployed custom model and retrieve the structured results returned by the service.

Key workflow summary:

* Provide the Document Intelligence resource endpoint and an access key to authenticate API calls.
* Include the deployed custom model's ID in the analysis request so the service knows which model to execute.
* The service returns a poller object for long-running analysis operations; use it to monitor progress and obtain the final AnalyzeResult once processing completes.

<Frame>
  <img alt="A presentation slide titled &#x22;Analyzing Documents Using Custom Model&#x22; showing three numbered steps about needing an endpoint and key, including the deployed model ID in requests, and querying the poller to retrieve processed data. The design uses a dark blue background with teal accent bars and numbering." />
</Frame>

<Callout icon="lightbulb">
  Before calling the SDK, confirm your custom model is deployed and take note of the model ID. Ensure the document URI is reachable by the service (public URL or storage with proper access). If you use SAS-secured blobs, verify the token grants read access to the file.
</Callout>

Below are example usage patterns for the SDKs. The primary difference from built-in models is that you explicitly pass your custom model's ID when starting the analysis so the service can run the correct trained model.

C# example (async, using DocumentAnalysisClient)

```csharp theme={null}
using Azure;
using Azure.AI.DocumentAnalysis;
using System;

// create the client with the endpoint and key
var client = new DocumentAnalysisClient(new Uri("<your-endpoint>"), new AzureKeyCredential("<your-key>"));

// provide your deployed model ID and the document URI
string modelId = "your-custom-model-id";
Uri documentUri = new Uri("https://example.com/path/to/document.pdf");

// start analysis and wait for completion (poller)
AnalyzeDocumentOperation operation = await client.AnalyzeDocumentFromUriAsync(WaitUntil.Completed, modelId, documentUri);

// get the result once the operation finishes
AnalyzeResult result = operation.Value;

// 'result' now contains pages, fields extracted by your model, confidence scores, and layout metadata
```

Python example (poller)

```python theme={null}
from azure.ai.documentanalysis import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
