# create the client
endpoint = "https://<your-endpoint>"
key = "<your-key>"
client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

# specify your deployed model ID and the document URL
model_id = "your-custom-model-id"
file_url = "https://example.com/path/to/document.pdf"

# begin analysis; returns a poller for a long-running operation
poller = client.begin_analyze_document_from_url(model_id=model_id, document_url=file_url)

# wait for completion and obtain the result
result = poller.result()

# 'result' contains pages, extracted fields, confidence scores, and other structured output
```

Common SDK method mapping

|                     SDK / Language | Method to start analysis                                      | Returns                                     |
| ---------------------------------: | ------------------------------------------------------------- | ------------------------------------------- |
|     C# (Azure.AI.DocumentAnalysis) | AnalyzeDocumentFromUriAsync(WaitUntil, modelId, uri)          | AnalyzeDocumentOperation (poller)           |
| Python (azure.ai.documentanalysis) | begin\_analyze\_document\_from\_url(model\_id, document\_url) | LROPoller -> result() returns AnalyzeResult |

> **warning** Be careful with secrets and endpoint values. Never check your Azure keys into source control. If using storage URIs with tokens, ensure the token provides read access and is valid for the duration of the analysis.

Inspecting results

* Once the poller completes, the returned AnalyzeResult (C#) or result (Python) contains:
  * Extracted fields as defined by your custom model (names, values, and confidence scores).
  * Page and layout information (text lines, bounding regions).
  * Additional metadata such as page ranges and any warnings produced during processing.
* Use these fields to populate downstream processes, persist structured data, or drive business logic that depends on the extracted content.

Links and references

* [Azure Document Intelligence documentation](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/)
* [Quickstart: Analyze documents using the Document Analysis client library](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/quickstarts)
* SDK packages:
  * C#: Azure.AI.DocumentAnalysis
  * Python: azure.ai.documentanalysis

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/0188c6a9-34fd-4f24-a143-ad9ce7b7e5d0)


# Document Intelligence Service

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Document-Intelligence-Service/page

Explains automating extraction and structuring of text and data from documents using Document Intelligence for faster, accurate processing, model types, deployments, outputs, and a university admissions scenario.

Document Intelligence automates extraction and structuring of information from documents — PDFs, scanned pages, images, and handwritten forms — enabling faster, more accurate processing of large document volumes.

Below we’ll walk through a real-world scenario, the benefits, available model types, deployment options, and practical outputs you can expect when integrating Document Intelligence into your workflows.

## Real-world scenario: University admissions

Imagine a university receiving thousands of student applications during each admissions cycle. Applicants submit a variety of documents: admission forms, mark sheets, identity proofs, and more. Manual verification of these documents is time-consuming, error-prone, and delays decision-making.

<Frame>
  <img alt="A slide titled &#x22;Document Intelligence Service&#x22; showing three connected document types — Admission forms, Mark sheets, and Identity proofs — with icons for a PDF, a scanned document, and an image. Text at the bottom reads &#x22;Manual verification becomes tedious and time-consuming,&#x22; with a © Copyright KodeKloud note in the corner." />
</Frame>

Manual processing forces admission staff to repeatedly open files, transcribe data, and validate entries — consuming hours that could be spent on counselling students or improving the admission process. Document Intelligence replaces repetitive tasks with an automated, auditable pipeline.

> **lightbulb** Using Document Intelligence reduces human error and accelerates application throughput by converting unstructured documents into structured data automatically.

## How Document Intelligence streamlines admissions

1. Students upload documents (application forms, mark sheets, IDs) to the admissions portal, creating a centralized digital repository.
2. Document Intelligence analyzes uploaded files and extracts key fields — student name, grades, date of birth, ID numbers — even from scanned or handwritten documents.

<Frame>
  <img alt="A presentation slide titled &#x22;Document Intelligence Service&#x22; showing an illustration of a woman next to a progress window and a vertical list of extracted fields: Name, Grades, Date of Birth, and ID Numbers. The slide states that Document Intelligence extracts data from uploaded files." />
</Frame>

3. Extracted data is validated, enriched (if necessary), and auto‑populated into the university’s student information system — eliminating manual entry and reducing processing time.

<Frame>
  <img alt="A presentation slide titled &#x22;Document Intelligence Service&#x22; explaining that student data (Name, Grades, Date of Birth, ID Numbers) is auto‑filled into the student system. The slide is illustrated with a person holding a tablet on the left and another person reviewing a large monitor showing a spreadsheet on the right." />
</Frame>

Benefits realized in this scenario include:

* Faster admissions review through automated extraction.
* Reduced manual data-entry workload for administrative staff.
* Lower error rates and improved consistency of student records.

<Frame>
  <img alt="A presentation slide titled &#x22;Document Intelligence Service&#x22; with three numbered dark boxes. The boxes list benefits: speeds up admissions process, reduces manual data entry, and minimizes errors and document mismatches." />
</Frame>

## Model types and when to use them

Document Intelligence supports multiple model types to match your document variety and complexity. The table below summarizes the built-in and custom model options and their best-fit use cases.

| Model Type       | Use Case                                         | Notes / Example                                                      |
| ---------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Read (OCR)       | Extract printed or handwritten text              | General-purpose OCR for text recognition                             |
| Layout           | Understand structural elements                   | Detects paragraphs, headings, tables, and layout regions             |
| General Document | Broad extraction (text, tables, key-value pairs) | Good for mixed formats and semi-structured documents                 |
| Prebuilt models  | Quick deployment for common doc types            | Receipts, invoices, IDs, business cards, contracts, tax forms        |
| Custom template  | Static, fixed-layout forms                       | Fast to train for consistent forms such as standardized applications |
| Custom neural    | Variable layouts and diverse document sets       | Neural-based approach for highly variable documents                  |
| Custom composed  | Complex pipelines combining models               | Merge models for multi-step workflows and complex documents          |

<Frame>
  <img alt="A presentation slide titled &#x22;Document Intelligence Service&#x22; showing deployment options on the left and a diagram on the right of a cloud-based document analysis system with prebuilt models (receipts, invoices, IDs, contracts) and custom models (template, neural, composed)." />
</Frame>

Deployment options:

* Standalone Document Intelligence service — best when document processing is the primary requirement.
* Azure AI Services (multi-service accounts) — combine vision, language, and search capabilities for broader solutions.

> **warning** When processing sensitive PII (e.g., student IDs, dates of birth), ensure compliance with data protection policies and secure storage/encryption in transit and at rest.

## Common prebuilt model outputs (examples)

Prebuilt models are optimized for common document types and provide structured outputs ready for validation and ingestion.

* Receipts: merchant name, transaction date/time, items, totals.
* Invoices: vendor name, invoice number, dates, line items, totals.
* Business cards: contact names, job titles, company, phone, email.

Example outputs (JSON):

Receipt example:

```json theme={null}
{
  "MerchantName": "Fourth Coffee",
  "TransactionDate": "2021-01-01",
  "TransactionTime": "09:34",
  "Items": [
    {
      "Description": "Latte",
      "Quantity": 1,
      "Price": 3.75
    }
  ],
  "Total": 3.75
}
```

Invoice example:

```json theme={null}
{
  "VendorName": "Contoso",
  "InvoiceNumber": "1234",
  "InvoiceDate": "2021-01-01",
  "Tables": [
    {
      "Description": "Consulting Services",
      "Amount": 3.99
    }
  ],
  "TotalInvoiceAmount": 3.99
}
```

Business card example:

```json theme={null}
{
  "ContactNames": [
    {
      "FirstName": "Hank",
      "LastName": "Zoeng"
    }
  ],
  "JobTitle": "Sales Manager",
  "Company": "Contoso",
  "Phone": "+1-555-0100",
  "Email": "hank.zoeng@contoso.com"
}
```

These structured outputs can be validated, enriched (e.g., cross-referencing student records or credit checks), and ingested into downstream systems such as Student Information Systems (SIS), ERPs, or CRMs to drive faster, data-driven decisions.

## Next steps: working with Document Intelligence

To implement Document Intelligence in your environment:

1. Choose the appropriate model type (prebuilt vs custom) based on document variability.
2. Configure secure ingestion (portal uploads, APIs, or blob storage).
3. Validate and map extracted fields to your target system schemas.
4. Add quality checks and human-in-the-loop review for edge cases.
5. Monitor model performance and retrain or refine custom models as needed.

Further reading and references:

* [Azure Document Intelligence documentation](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/)
* [Azure AI Services overview](https://learn.microsoft.com/azure/ai-services/)

If you’d like, I can add a sample ingestion pipeline, code snippets for calling the Document Intelligence REST/SDK APIs, or a checklist for PII compliance and security best practices.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/463d2abd-dba6-4382-8294-df4781def708)
