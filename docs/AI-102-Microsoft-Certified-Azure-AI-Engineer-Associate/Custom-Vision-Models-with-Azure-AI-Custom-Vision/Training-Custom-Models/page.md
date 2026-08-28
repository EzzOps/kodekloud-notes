# Training Custom Models

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Custom-Vision-Models-with-Azure-AI-Custom-Vision/Training-Custom-Models/page

Guide to building, training, evaluating, and publishing image classification and object detection models with Azure Custom Vision Studio.

Train custom image classification and object detection models using Azure Custom Vision Studio: a visual, low-code interface for building, training, and publishing models that detect or classify objects in images. Start with labeled images (for example, apples, oranges, and bananas) and let Custom Vision do the heavy lifting of model training, evaluation, and publishing.

Explore Custom Vision Studio: [https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/](https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/)

<Frame>
  <img alt="Screenshot of the &#x22;Train a Custom Model&#x22; page in Azure Custom Vision Studio, showing a grid of training images (mostly oranges and a few bananas) and tag/filter controls on the left. It's an interface for building and labeling images for image classification." />
</Frame>

Once your images are uploaded and tagged, use the Train button (top of the project page) to start training. The UI guides you from upload → labeling → training → evaluation, making iteration straightforward.

<Frame>
  <img alt="An infographic slide titled &#x22;Steps to Train a Custom Model&#x22; showing five colorful gear icons numbered 01–05. Each gear lists a step: Create a New Project; Select a Resource; Upload and Configure Data (image classification, object detection); Label Images; and Train the Model." />
</Frame>

## End-to-end workflow (high level)

| Step | What to do                     | Notes                                                                                            |
| ---- | ------------------------------ | ------------------------------------------------------------------------------------------------ |
| 1    | Create a Custom Vision project | Use the Custom Vision web app or portal. Choose classification or object detection.              |
| 2    | Link an Azure resource         | Create/link a Custom Vision or Cognitive Services resource in the Azure portal.                  |
| 3    | Upload and configure images    | For classification: tag each full image. For object detection: draw bounding boxes per instance. |
| 4    | Train the model                | Click Train to create an iteration; try quick or advanced training options.                      |
| 5    | Evaluate & publish             | Review Precision/Recall/AP or mAP. Publish an iteration to obtain prediction endpoints and keys. |

Benefits of using Custom Vision Studio:

* Visual, user-friendly tooling for labeling and training (no deep ML expertise required).
* Domain-specific optimizations (Food, Retail, Landmarks, etc.) that can influence model architecture.
* Iterative improvement: add more labeled images and retrain to increase accuracy.

Next, walk through creating the Azure resource and the Custom Vision project.

## Create a Custom Vision resource in Azure

Create a Custom Vision resource in the Azure portal. You can enable both training and prediction on the same resource or separate them into training and prediction resources depending on your security and billing needs. Pick a subscription, resource group, region, and pricing tier (there is a free tier for testing).

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Create Custom Vision&#x22; page with form fields for project and instance details (subscription, resource group, region, name) and a training pricing-tier dropdown. The bottom shows navigation buttons like Previous, Next, and Review + create." />
</Frame>

## Create a project in the Custom Vision web app

Open the Custom Vision web app ([https://www.customvision.ai/](https://www.customvision.ai/)) and create a new project. Provide a name and optional description, select the linked resource, then choose:

* Project type:
  * Classification — whole-image labels (Multiclass: one tag per image; Multilabel: multiple tags per image).
  * Object detection — localize objects with bounding boxes and return tag predictions.
* Domain — e.g., General, Food, Retail, Landmarks. Domains may optimize architecture or export options.

<Frame>
  <img alt="A browser screenshot of the Microsoft Custom Vision web app showing a &#x22;Create new project&#x22; dialog with the project name set to &#x22;DogBreedClassifier&#x22; and options for resource, project type, classification type, and domain. The Custom Vision Projects page is visible in the faded background." />
</Frame>

## Upload and label images

* For classification: upload images and assign a single (or multiple for multilabel) tag per image.
* For object detection: upload images, create tags, then draw tight bounding boxes around each object instance and assign the correct tag.

<Frame>
  <img alt="A screenshot of a web-based image uploader (Custom Vision) showing a grid of dog photos being added. The dialog includes tag options like &#x22;Golden Retriever&#x22; and &#x22;Husky&#x22; for the 28 images." />
</Frame>

After tagging, click Train. The platform produces iterations you can evaluate and compare.

<Frame>
  <img alt="A screenshot of a Custom Vision &#x22;DogBreedClassifier&#x22; performance dashboard showing Precision, Recall and AP each at 100%. The Performance Per Tag table lists Husky, Golden Retriever, and German Shepherd with image counts and 100% metrics." />
</Frame>

## Evaluation metrics (what they mean)

| Metric    | What it measures                                                           | When to focus on it                                       |
| --------- | -------------------------------------------------------------------------- | --------------------------------------------------------- |
| Precision | Fraction of predicted positives that are correct                           | When false positives are costly                           |
| Recall    | Fraction of actual positives that were found                               | When missing a positive is costly                         |
| AP / mAP  | Average Precision across confidence thresholds (object detection uses mAP) | Overall balance of precision and recall across thresholds |

After training, use Quick Test or the Predictions API to test on images held out from training.

## Testing with images stored in Azure Storage

You can test images stored in Azure Blob Storage by copying the blob URL (make it public or use a SAS token) and pasting it into Quick Test or sending it via the Predictions API.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the Storage accounts overview for a storage account named &#x22;azai102imagestore.&#x22; The screen displays the left navigation and account list on the left and detailed properties and settings (Blob service, File service, Security, Networking) for the selected account on the right." />
</Frame>

<Frame>
  <img alt="A screenshot of the Microsoft Azure Storage container view showing an &#x22;images&#x22; container with a list of image files on the left and the properties/details pane for &#x22;dog.jpg&#x22; open on the right. The properties pane displays blob metadata like URL, last modified time, size, and content-type." />
</Frame>

Quick Test displays predicted tags and probabilities for classification models. For example, a golden retriever image might return "Golden Retriever — 99.7%."

<Frame>
  <img alt="A screenshot of a &#x22;Quick Test&#x22; page in a custom vision web app showing a photo of a golden retriever sitting in a grassy field. The predictions panel on the right lists &#x22;Golden Retriever&#x22; with about 99.7% probability." />
</Frame>

Validate generalization by testing with diverse images, including web images and held-out datasets.

<Frame>
  <img alt="A screenshot of a web app showing a black-and-white Siberian husky standing on a rocky outcrop against a blue sky. The app's prediction panel on the right labels the image &#x22;Husky&#x22; with 99.8% probability." />
</Frame>

## Object detection: annotate, train, and evaluate

Object detection projects return both labels and bounding boxes. Workflow:

1. Create an object detection project (e.g., DogDetector).
2. Upload images.
3. Create tags (e.g., Golden Retriever, Husky).
4. Select images, draw bounding boxes for each instance, and assign tags.
5. Train and review metrics (Precision, Recall, mAP).

<Frame>
  <img alt="A computer screenshot of a Custom Vision-style web interface labeled &#x22;DogDetector&#x22; showing three dog photos at the top and a centered &#x22;Create a new tag&#x22; dialog box for entering a tag name. The page UI includes workspace filters and buttons for adding or training images." />
</Frame>

<Frame>
  <img alt="A screenshot of an image-annotation web app. It shows a husky dog lying on grass with a bounding box around it labeled &#x22;Husky.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  For object detection, Custom Vision recommends a minimum of \~15 images per tag to start achieving reasonable results. More images, varied scenes, and tightly drawn bounding boxes significantly improve robustness and reduce false positives/negatives.
</Callout>

After annotating, train the model and inspect per-tag performance. Use Quick Test to verify bounding box outputs, confidence scores, and multiple detections per image.

<Frame>
  <img alt="A browser screenshot of an Azure Custom Vision &#x22;DogDetector&#x22; project performance page showing three circular metrics (Precision 85.7%, Recall 85.7%, mAP 80.2%). Below is a &#x22;Performance Per Tag&#x22; table listing results for Golden Retriever and Husky." />
</Frame>

<Frame>
  <img alt="A screenshot of a Custom Vision &#x22;Quick Test&#x22; window showing two smiling dogs — a golden retriever on the left and a husky on the right — with red detection boxes. The sidebar shows model predictions (e.g., Golden Retriever 99.8% and Husky 97.8%)." />
</Frame>

If detection quality is insufficient:

* Add images that increase variation (lighting, scale, occlusion, orientation).
* Correct and tighten bounding boxes.
* Increase labeled instances per tag and retrain.

## Publish for production

When satisfied with an iteration, publish it to create a prediction endpoint and obtain keys/credentials. Use the SDK or REST Prediction API to integrate the model into web, mobile, or backend systems.

API & SDK references:

* Predictions API: [https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/](https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/)
* Custom Vision documentation: [https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/](https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/)

## Summary

* Use Custom Vision Studio to create classification or object detection projects, upload and tag images, train iterations, evaluate precision/recall/mAP, and test with Quick Test.
* Publish trained iterations to obtain prediction endpoints for programmatic integration.
* Improve models iteratively—collect diverse labeled data, correct annotations, and retrain to improve real-world performance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/ebc335c9-6d06-4770-9bc9-8fd3f250d3e6/lesson/bde50303-2b9e-4018-b89d-420426d0636f" />
</CardGroup>
