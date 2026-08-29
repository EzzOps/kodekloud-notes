# Custom Text Classification

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Custom-Classification-and-Named-Entity-Extraction/Custom-Text-Classification/page

Guide for building, training, and deploying custom text classification models using Azure Language Studio including data labeling, evaluation, deployment, SDK examples, and best practices.

Custom Text Classification

This guide walks through the end-to-end process for building a custom text classification model in Azure Language Studio — from connecting your data to deploying a trained model for inference. Follow these steps to create accurate, production-ready classifiers for scenarios like article tagging, support-ticket routing, or internal document classification.

Overview — pipeline steps

* Data connection: connect your stored documents to Language Studio.
* Class definition: define the set of labels (single-label or multi-label).
* Label assignment: tag documents with the appropriate class labels.
* Model training: train and evaluate the classifier.
* Deployment: deploy the model as an endpoint for integration.

<Frame>
  <img alt="A presentation slide titled &#x22;Custom Text Classification&#x22; showing two steps: Data Connection and Class Definition. On the right is a screenshot of an Azure data-labeling interface listing example documents and labels like Sports, News, and Entertainment." />
</Frame>

Step 1 — Data connection and class definition
Start by integrating the documents you want to classify (e.g., news articles, support tickets, internal docs) with Azure Language Studio. Clean, relevant data improves model quality, so filter out noisy files and ensure the content represents the categories you intend to predict.

Next, define your classes — these are the categories the model will predict. Examples in this article include Arts, Entertainment, and Sports. Add enough representative examples per class to enable effective learning. You can add, rename, or remove classes later in the project settings.

Step 2 — Label assignment
Assign labels to each document to build the supervised dataset used for training. Label consistently: similar content should receive the same tag (e.g., a match report → Sports; a movie review → Entertainment). The portal shows dataset status and whether files are assigned to training or test sets. Proper and consistent labeling is critical to good results.

Step 3 — Training and evaluation
After labeling, start a training job. Choose a data split (commonly 80/20 or 70/30) to hold out evaluation data and monitor generalization. The training process learns patterns that map text to classes and provides an evaluation report on the held-out set to estimate expected performance.

Step 4 — Deployment
When satisfied with evaluation metrics, deploy the model as an endpoint (REST + SDK support). Choose a deployment name and resource region. Deployed models become callable from your applications for real-time or batch classification.

<Frame>
  <img alt="A presentation slide titled &#x22;Custom Text Classification&#x22; showing three numbered steps—03 Label Assignment, 04 Model Training, and 05 Deployment—with short descriptions for each. The slide also notes it supports both single- and multi-label classification." />
</Frame>

Using Language Studio for Custom Text Classification

This section provides a practical walkthrough inside Azure Language Studio.

Open Language Studio and choose “Classify text (Custom text classification).” The studio includes pre-built features (Analyze sentiment, Detect language), but here we focus on creating a custom classification project.

<Frame>
  <img alt="A browser screenshot of the Azure AI Language Studio dashboard showing a list of projects and menu tabs (like Classify text, Extract information, Summarize text). The page also displays feature cards for Analyze sentiment, Detect language, and Custom text classification along with learning resources." />
</Frame>

Create a project

* Click “Create a project”.
* Select the Azure Language resource to back the project.
* If this is your first time, attach a storage account (documents used for labeling are uploaded to blob storage). Grant the storage account an RBAC role such as Storage Blob Data Contributor so Language Studio can read the blobs.

> **lightbulb** Ensure the storage account has the Storage Blob Data Contributor role (or equivalent) assigned so Language Studio can access files for labeling and training.

<Frame>
  <img alt="A dialog window from Azure AI Studio titled &#x22;Select an Azure resource,&#x22; showing form fields to choose an Azure directory, subscription, resource type (Language) and resource name. The modal overlays the project creation screen with Cancel/Done buttons." />
</Frame>

During creation you choose:

* single-label classification (one category per document) or
* multi-label classification (documents can belong to multiple categories).

In the example here, we select single-label and name the project “Article Classification,” with English as the primary language. Also select the target storage container where labeled files reside.

<Frame>
  <img alt="Screenshot of the Microsoft Azure portal showing the contents of a storage container named &#x22;textclass.&#x22; The view lists multiple .txt blob files and their properties (modified date, access tier, blob type, size, lease state)." />
</Frame>

Choose the container and finish the project setup.

<Frame>
  <img alt="A screenshot of Azure AI Language Studio with a &#x22;Create a project&#x22; popup open, showing steps on the left and a &#x22;Choose dataset location&#x22; form on the right (including a Blob store container dropdown). The background shows the Custom Text Classification project selection page." />
</Frame>

Label the data
Add classes (e.g., Arts, Entertainment, Sports) and begin labeling each document. The portal indicates dataset readiness and shows segmentation into training and test sets. For meaningful performance, use as many varied, labeled examples as possible — dozens to hundreds per label is common for higher accuracy.

<Frame>
  <img alt="A screenshot of the Azure Language Studio &#x22;Data labeling&#x22; page showing a list of document files (e.g., arts1.txt, entertainment1.txt, sports1.txt) with their assigned labels and dataset status. The right-side activity pane shows label options and controls for assigning documents to training or test sets." />
</Frame>

Auto-labeling (preview)
Language Studio can suggest labels using auto-labeling (generative models) to help bootstrap large datasets. Always review and correct auto-labeled items before training to avoid propagating errors.

<Frame>
  <img alt="Screenshot of the Azure AI Language Studio &#x22;Auto-labeling&#x22; page for a text classification project, showing a central illustration and a message that no auto-labeling jobs exist yet. The left sidebar displays project navigation items like Data labeling, Training jobs, and Model performance." />
</Frame>

Start a training job

* Choose a model name.
* Configure data split (for example, 80% training / 20% testing).
* Start training and wait for completion; review evaluation metrics and logs on the Training jobs page.

<Frame>
  <img alt="A screenshot of Azure AI Language Studio’s &#x22;Start a training job&#x22; page showing options to train or overwrite a model, a model-name input field, and data-splitting settings (80% training / 20% testing)." />
</Frame>

Example: calling the model from Python (SDK)
Below is a compact Python example showing how to classify a local text file using the Text Analytics client. Note: import only the client and AzureKeyCredential — some older examples import non-existent action classes (e.g., SingleCategoryClassifyAction), which will raise ImportError.

```python theme={null}
