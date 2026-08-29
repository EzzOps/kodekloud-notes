# Training Custom Models

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Training-Custom-Models/page

Guide to training custom classification and extraction models with Azure Document Intelligence, covering requirements, model types, Studio workflow, auto-labeling, and a Python example.

Learn how to train custom models with Azure Document Intelligence to classify documents or extract specific fields. This guide walks through when to use custom classification vs custom extraction, dataset requirements, model types, the end-to-end training workflow in Document Intelligence Studio, and a short Python example to inspect results.

Overview

* Azure Document Intelligence supports two primary custom model scenarios:
  * Custom classification: assigns a single label to an entire document (useful for routing or sorting).
  * Custom extraction: extracts specific named fields or regions from documents (useful for invoices, IDs, certificates).
* Use Document Intelligence Studio to annotate, auto-label, train, and obtain a Model ID for API integration.

Custom classification (document-level labeling)

When to use:

* You want to assign an overall category or label to an entire document (e.g., "resume", "contract", "tax form").
* Useful for automated sorting and routing of incoming document batches.

Requirements:

* At least two distinct classes (categories).
* Minimum of five labeled documents per class.
* A single model makes classification decisions across entire documents.

> **lightbulb** - At least two distinct classes (categories).
  - A minimum of five labeled documents per class.
  - Classification uses a single training model that makes decisions across entire documents.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of Custom Models&#x22; describing &#x22;Custom Classification.&#x22; It lists the purpose (assigns a label to an entire document), best use (organizing/sorting large volumes of incoming documents), and requirements (minimum two classes, at least five labeled documents per class, single training model)." />
</Frame>

Custom extraction (field-level labeling)

When to use:

* You need to extract specific pieces of information from documents (e.g., invoice number, total, names, dates, signatures).
* Works for both structured forms (consistent layouts) and unstructured documents (varying layouts).

Requirement:

* At least five example documents of the same type to train the model to recognize fields.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of Custom Models — Custom Extraction&#x22; that explains its purpose, use case, and requirements. It states the purpose is to assign labels to specific text within documents, it's best for extracting custom fields from structured or unstructured text, and requires five example documents of the same type." />
</Frame>

Model types for extraction

Choose the model type based on layout variability and training tolerance:

| Model Type                          |                                          Best for |          Training time | Notes                                                         |
| ----------------------------------- | ------------------------------------------------: | ---------------------: | ------------------------------------------------------------- |
| Custom Template (Structured Forms)  | Consistent, repeatable layouts (forms, templates) |     Fast (1–5 minutes) | Relies on fixed layout to locate fields accurately            |
| Custom Neural (Flexible Extraction) |                  Varied or mixed document layouts | Longer (20–60 minutes) | Uses neural approaches to generalize across different formats |

* Custom Template: optimized for fixed formats where field positions are predictable.
* Custom Neural: better when forms vary in layout or when extracting from semi-structured/unstructured documents.

<Frame>
  <img alt="A presentation slide titled &#x22;Types of Custom Models&#x22; showing two side-by-side boxes. The left describes &#x22;Custom Template (Structured Forms)&#x22; with short training time and use for templates/forms, and the right describes &#x22;Custom Neural (Flexible Extraction)&#x22; with longer training time and support for structured and unstructured documents." />
</Frame>

Training workflow (high-level)

Follow these steps to create a custom extraction model:

1. Create a project in Document Intelligence Studio.
2. Upload training files or connect the project to an Azure Blob Storage container so the studio can access your documents.
3. Define the fields (data types) you want the model to extract (for example, invoice\_number, date\_of\_birth, signature).
4. Annotate (label) documents by selecting text or drawing regions and assigning field labels across multiple training documents.
5. Use Layout Analysis and Auto-Labeling (optional) to speed up annotation by leveraging prebuilt models.
6. Train the model. After training completes, Document Intelligence provides a trained model and a Model ID to use with the APIs.

<Frame>
  <img alt="The image is a slide titled &#x22;Training Custom Models&#x22; showing a three-step horizontal timeline. It summarizes: Step 1 — create a project and upload training files or connect to blob storage; Step 2 — define data types (e.g., field or signature) to label your dataset; Step 3 — highlight words in documents and assign them to relevant field labels." />
</Frame>

The quality of extraction improves with more well-labeled examples per field—label multiple instances and variations (different fonts, positions, and noise).

Layout Analysis and Auto-Labeling

* Layout Analysis: detects document regions (text blocks, tables, selection marks) to help you target fields quickly.
* Auto-Labeling: leverages prebuilt models (e.g., invoice, ID, credit card) to propose field labels automatically, reducing manual effort when documents match known templates.

<Frame>
  <img alt="A slide titled &#x22;Training Custom Models&#x22; showing a horizontal timeline with Step 4–Step 6. The steps summarize repeating labeling for all fields/documents, using layout analysis and auto-labeling to streamline labeling, and training the model to generate a Model ID for API requests." />
</Frame>

Using the trained model

* After training, take the Model ID and call the Document Intelligence REST API or SDKs to analyze new documents.
* The studio and SDKs provide example code (Python, JavaScript) to integrate analysis into your applications.

Practical walkthrough: training in Document Intelligence Studio

The following screenshots illustrate the typical project flow for a custom extraction model.

1. Label data view — annotate fields directly on sample documents in the studio.

<Frame>
  <img alt="A slide titled &#x22;Training Custom Models&#x22; showing a Document Intelligence Studio &#x22;Label data&#x22; interface. The screenshot displays a scanned invoice/form with regions and fields highlighted for labeling and model training." />
</Frame>

2. Prepare your training set in Azure Blob Storage — for this demo, a container holds five marriage certificate PDFs used as training examples.

<Frame>
  <img alt="A Microsoft Azure Storage portal view showing a container named &#x22;marriage-certificates.&#x22; The container lists five PDF blobs (marriageCertificateCa*.pdf) with modification timestamps, access tier &#x22;Hot (Inferred),&#x22; block blob type, and size about 2.06 MiB each." />
</Frame>

3. Choose Custom Extraction in Document Intelligence Studio (we're extracting named fields rather than classifying whole documents).

<Frame>
  <img alt="A screenshot of the Azure AI Document Intelligence Studio web interface showing cards for features like &#x22;Business cards&#x22; and &#x22;Custom models&#x22; (custom extraction and classification) with &#x22;Try it out&#x22; options. The page is displayed in a browser window on a macOS-like desktop." />
</Frame>

4. Create a new project and link it to your Document Intelligence resource (select subscription, resource group, and the Document Intelligence resource).

<Frame>
  <img alt="A browser screenshot of Azure AI Document Intelligence Studio with a &#x22;Custom extraction model&#x22; configuration dialog open, showing fields for subscription, resource group, Document Intelligence resource and API version. The modal overlays the My Projects page and includes Back, Continue and Cancel buttons." />
</Frame>

5. Connect the project to your storage container (e.g., the "marriage-certificates" container). If files are in the container root, leave the folder path empty.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal open to a Storage accounts page, showing the storage account &#x22;azai102imagestore&#x22; with its overview, properties, security, and networking details. The left pane lists other storage accounts and navigation options like Containers, File shares, and Access keys." />
</Frame>

6. Start labeling. Optionally run Layout Analysis and Auto-Label to obtain suggested tags from prebuilt models.

<Frame>
  <img alt="A screenshot of Azure AI Document Intelligence Studio with an &#x22;Auto label current document&#x22; dialog open, showing a dropdown list of prebuilt model IDs (e.g., prebuilt-idDocument, prebuilt-creditCard, prebuilt-invoice). A blue &#x22;Upload documents&#x22; pop-up on the left prompts the user to upload at least five documents for labeling." />
</Frame>

7. If auto-labeling is insufficient, add fields and manually tag regions (e.g., bride\_name, groom\_name, date\_of\_marriage, place\_of\_marriage, signature). Label each field across multiple documents, then click Train. Choose:

* Template (structured) for consistent layouts (faster).
* Neural (flexible) for diverse layouts (more time but better generalization).

After training completes, the studio displays success, the new model, and accuracy/confidence metrics. Test the model by analyzing a document in your storage container (for example: https\://\<your-storage-account>.blob.core.windows.net/marriage-certificates/marriageCertificateCa2.pdf). The studio will display extracted fields and confidence scores.

Integration and code samples

* Document Intelligence Studio provides generated code snippets (Python, JavaScript) and the official SDK documentation contains full examples to call the model using the Model ID.
* See Azure Document Intelligence docs for client libraries and API references:
  * [https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/overview](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/overview)
  * [https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/client-libraries](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/client-libraries)

Example: iterate analysis results in Python

Below is a Python snippet that inspects pages, lines, words, selection marks, and tables from an analysis result. Assume `result` is the output from the SDK method (e.g., begin\_analyze\_document).

```python theme={null}
