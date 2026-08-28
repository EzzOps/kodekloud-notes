# example: classify a local document using the Text Analytics SDK
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def classify_local_document(file_path, endpoint, key, project_name, deployment_name):
    # Initialize client
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Read the document to classify
    with open(file_path, "r", encoding="utf-8") as f:
        document_text = f.read()

    # Start the classification job (single-label in this example)
    poller = client.begin_single_label_classify(
        documents=[document_text],
        project_name=project_name,
        deployment_name=deployment_name
    )

    # Wait for result
    results = poller.result()

    # results is an iterable of document results
    for doc in results:
        if not doc.is_error:
            # The SDK may expose classifications in either 'classifications' or 'classification'
            classifications = getattr(doc, "classifications", None) or getattr(doc, "classification", None)
            if classifications:
                # If it's a list of classifications, print them
                if isinstance(classifications, list):
                    for c in classifications:
                        print(f"Predicted Label: {c.category}")
                        print(f"Confidence Score: {c.confidence_score:.2f}")
                else:
                    # single classification object
                    print(f"Predicted Label: {classifications.category}")
                    print(f"Confidence Score: {classifications.confidence_score:.2f}")
            else:
                print("No classifications returned for this document.")
        else:
            print(f"Error: {doc.error.code} - {doc.error.message}")
```

<Callout icon="warning">
  If you see an ImportError such as:

  ```Python theme={null}
  ImportError: cannot import name 'SingleCategoryClassifyAction' from 'azure.ai.textanalytics'
  ```

  it means the code tried to import a non-existent action class. Import only TextAnalyticsClient and AzureKeyCredential and call the classification method on the client, as shown above.
</Callout>

Deploy the model
After successful training and evaluation:

* Add a deployment (give it a name and choose region/resource).
* The portal will provide a prediction URL and SDK code snippets to call the endpoint.

<Frame>
  <img alt="Screenshot of Azure Language Studio's &#x22;Deploying a model&#x22; page with an &#x22;Add deployment&#x22; dialog open, showing a new deployment name (&#x22;article-depl&#x22;) being entered. The modal also shows fields to assign a trained model and choose deployment regions." />
</Frame>

<Frame>
  <img alt="Screenshot of the Azure AI Language Studio &#x22;Deploying a model&#x22; page showing a deployment named &#x22;article-dep&#x22; (model article-trn-job) with a highlighted &#x22;Get prediction URL&#x22; button and deployment details. The left sidebar shows project navigation and the page includes SDK and GitHub sample links." />
</Frame>

Test from the portal
Language Studio includes a quick test UI. Example results from the demo:

* Input: "Argentina won the 2022 FIFA World Cup."\
  Output: Predicted "Sports" (confidence \~0.39)

* Input: "Avengers is a great movie."\
  Output: Predicted "Entertainment"

The portal also displays raw JSON output for predictions. Example single-label JSON:

```json theme={null}
{
  "classes": [
    {
      "category": "Entertainment",
      "confidenceScore": 0.37
    }
  ]
}
```

Improving accuracy
If your model has low confidence (common with small datasets), apply these best practices:

* Increase dataset size: add more labeled examples per class with diverse phrasing.
* Label quality: ensure labels are consistent and representative of real inputs.
* Data split: use a validation/test split to detect overfitting.
* Auto-labeling: bootstrap with auto-labeling, then review and correct suggestions.
* Domain examples: include domain-specific vocabulary and realistic documents.

Use cases
Custom text classification is useful for:

* Routing support tickets automatically
* Tagging news and articles
* Classifying legal or HR documents (NDAs, contracts)
* Content moderation and internal document organization

Quick reference table

| Resource Type   | Use Case                       | Example / Command                                                                                                  |
| --------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Language Studio | Create and manage projects     | [https://learn.microsoft.com/azure/ai-services/language/](https://learn.microsoft.com/azure/ai-services/language/) |
| Storage account | Store labeled documents        | Assign Storage Blob Data Contributor role                                                                          |
| Deployment      | Host trained model             | Get prediction URL from Language Studio                                                                            |
| SDK (Python)    | Call endpoint programmatically | azure.ai.textanalytics.TextAnalyticsClient                                                                         |

Links and references

* Azure Language documentation: [https://learn.microsoft.com/azure/ai-services/language/](https://learn.microsoft.com/azure/ai-services/language/)
* Azure Language Studio overview: [https://learn.microsoft.com/azure/ai-services/language/overview](https://learn.microsoft.com/azure/ai-services/language/overview)
* Azure Storage RBAC roles: [https://learn.microsoft.com/azure/storage/common/storage-auth-aad-roles](https://learn.microsoft.com/azure/storage/common/storage-auth-aad-roles)

Train with domain-specific examples and iterate — more high-quality labeled data and consistent labeling practices yield the best classification performance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/59765c98-dac0-42f2-bf92-2f6fd2dc38d2/lesson/d2e6098c-adc0-4ee1-8a71-35c3ffbf73e8" />
</CardGroup>


# Module Introduction

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Custom-Classification-and-Named-Entity-Extraction/Module-Introduction/page

Guide to building custom document classifiers and named entity extraction models covering labeling, training, evaluation, deployment, and post-deployment monitoring and best practices.

Custom classification and named-entity extraction

Text analytics platforms provide powerful pre-built capabilities—such as entity recognition and document classification—that work well out of the box and require no training. These prebuilt features are excellent for general scenarios like detecting people’s names, dates, or common PII in documents.

When your application needs to recognize domain-specific items (for example, medical terminology, contract clauses, or proprietary product SKUs) or apply your organization’s own document categories, you’ll need custom models trained on labeled examples. This module walks through the full lifecycle: labeling data, training models, evaluating performance, and deploying production endpoints for real-time inference.

Below are the learning objectives for this lesson/article.

<Frame>
  <img alt="A presentation slide titled &#x22;Learning Objectives&#x22; listing three numbered items: 01 Document labeling and model training, 02 Performance evaluation, and 03 Model deployment." />
</Frame>

Learning objectives (overview)

* Document labeling and model training\
  Learn how to label documents and annotate text spans for both classification and named-entity extraction. Labeling is the manual process of tagging documents or text fragments with the categories and entity types you want the model to learn. Those labeled examples form the training set for a custom machine-learning model.

* Performance evaluation\
  Learn to evaluate custom models with standard metrics such as precision, recall, and F1 score. These metrics quantify model behavior on held-out test data, reveal weaknesses (for example, poor recall on rare classes), and guide iterative improvements.

* Model deployment\
  Learn how to deploy a trained model as a REST API endpoint so your application can call it in real time to classify new documents or extract custom entities.

Quick-reference: objectives and outcomes

| Objective                    | Key activities                                                      | Deliverable / outcome                                      | Example use case                                                              |
| ---------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Document labeling & training | Define labels, annotate examples, prepare datasets, run training    | A trained custom model ready for evaluation                | Classify invoices vs. contracts; extract medication names from clinical notes |
| Performance evaluation       | Split data, calculate precision/recall/F1, analyze confusion matrix | Metrics and error analysis guiding data/model improvements | Identify low-performing classes and add more labeled examples                 |
| Model deployment             | Create REST endpoint, secure access, monitor predictions            | Production endpoint for real-time inference and monitoring | Integrate into ingestion pipeline to tag documents on arrival                 |

<Callout icon="lightbulb">
  Use prebuilt text analytics features when they meet your needs (e.g., general entity recognition for common named entities). Choose custom models when you must detect domain-specific entities or apply organization-specific classifications that prebuilt models cannot capture.
</Callout>

Best practices covered in this module

* Labeling guidelines: tips to create high-quality, consistent annotations (for example: label spans consistently, define clear label definitions, and include edge cases).
* Balanced datasets: approaches to handle class imbalance such as targeted labeling, data augmentation, or sampling strategies.
* Iterative evaluation: how to use metrics and error analysis to prioritize where to add more labeled data or adjust modeling choices.
* Monitoring after deployment: methods for tracking model drift, collecting real-world feedback, and scheduling re-training.

Links and references

* [Introduction to Named Entity Recognition (NER)](https://en.wikipedia.org/wiki/Named-entity_recognition) — conceptual overview of entity extraction.
* [Evaluation metrics for classification](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall) — primer on precision, recall, and F1.
* [Text analytics and custom model guidance](https://learn.microsoft.com/azure/cognitive-services/text-analytics/) — vendor documentation and examples for deploying text analytics solutions.

Throughout this module you will learn practical steps and tools to create robust custom text models, plus workflows to maintain model quality after deployment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/59765c98-dac0-42f2-bf92-2f6fd2dc38d2/lesson/f90750db-f7d7-40ac-a860-9589f538648b" />
</CardGroup>
