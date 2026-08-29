# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Module-Introduction/page

Overview of Azure AI Document Intelligence, covering model types, labeling and training custom models, and integrating document analysis APIs into applications.

Developing a Document Intelligence solution

This lesson introduces Azure AI Document Intelligence (referred to here as the Document Intelligence Service). This managed service automatically extracts structured information from documents such as invoices, forms, contracts, and reports—reducing manual data entry and enabling downstream automation.

Below are the key learning objectives for this lesson:

* Explore the different models available in Azure AI Document Intelligence: prebuilt models, layout models, and custom models. Learn when to use each model type based on document formality, layout complexity, and extraction needs.
* Develop and train a custom model: label training data, run training in Azure AI Studio, and evaluate model accuracy and field confidence.
* Integrate Document Intelligence into applications using the Document Intelligence Service APIs and SDKs to analyze documents and consume extracted fields.

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; listing three numbered items about Azure AI Document Intelligence. The items are: exploring different models, developing and training a custom Document Intelligence model, and integrating an application with Document Intelligence APIs." />
</Frame>

This module covers the following topics:

* Model types and selection criteria (structured vs. semi-structured vs. domain-specific).
* Labeling best practices and the training workflow in Azure AI Studio.
* Calling the Document Intelligence Service API from an application to analyze documents and consume extracted fields.

<Callout icon="lightbulb">
  Tip: Choose the right model type before labeling data. Prebuilt models are quick for common document types (invoices, receipts), layout models are ideal for extracting structure (tables, text blocks), and custom models are best when you need domain-specific fields or document formats.
</Callout>

Model selection at a glance:

| Model Type      | Best for                                                     | When to choose                                                                                     |
| --------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Prebuilt models | Common business documents (invoices, receipts, ID documents) | You need fast, out-of-the-box extraction with minimal configuration.                               |
| Layout model    | Document structure, tables, and coordinates                  | You need raw layout information (bounding boxes, table structure) or are building a custom parser. |
| Custom model    | Domain-specific fields and complex formats                   | Documents contain specialized fields or inconsistent layouts; you can provide labeled examples.    |

Key steps you'll perform in this module:

1. Understand the differences between model types and decide which fits your scenario.
2. Label sample documents effectively (tips on annotation consistency and minimum dataset size).
3. Train and evaluate model performance in Azure AI Studio; iterate on labels to improve accuracy.
4. Integrate Document Intelligence into an application using the REST API or an SDK (e.g., Python, .NET), handle authentication, and parse the returned JSON for fields and confidence scores.

References and further reading:

* [Azure AI Document Intelligence overview](https://learn.microsoft.com/azure/applied-ai-services/form-recognizer/overview)
* [Azure AI Studio — Train custom models](https://learn.microsoft.com/azure/applied-ai-services/form-recognizer/quickstarts/try-sdk-client-library)
* SDKs and samples: [Azure SDKs for Document Intelligence](https://learn.microsoft.com/azure/applied-ai-services/form-recognizer/sdks)

<Callout icon="warning">
  Warning: When training and testing models, ensure you comply with data privacy regulations. Redact or anonymize personally identifiable information (PII) as required by your organization and legal guidelines before uploading documents to cloud services.
</Callout>

So let's get started with an introduction to Document Intelligence and how to choose the right model for your use case.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/3880411e-3a00-4557-8a6b-28a6c318dc4b" />
</CardGroup>
