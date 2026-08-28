# Custom Vision Model

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Custom-Vision-Models-with-Azure-AI-Custom-Vision/Custom-Vision-Model/page

Guide to using Azure Custom Vision to train, deploy, and improve image classification and object detection models for domain specific defect detection, inspection workflows, and best practices.

Custom Vision model.

In this lesson we'll use a practical scenario to explain why you'd choose Azure Custom Vision for image classification or object detection.

Imagine you run a car manufacturing plant. The inspection team struggles to detect minor defects in car parts during quality checks—tiny cracks, hairline scratches, or slight misalignments that are hard to see with the naked eye.

<Frame>
  <img alt="A slide titled &#x22;Custom Vision Model&#x22; with the prompt &#x22;Imagine a car manufacturing company.&#x22; It shows an illustration of a person, a robotic arm and a car, with a caption saying the company &#x22;struggles to detect minor defects in car parts during quality checks.&#x22;" />
</Frame>

Why generic image models often fall short:

* Small scratches that affect surface integrity
* Dents that impact fit or finish
* Missing or misaligned components that cause assembly failures

These are domain-specific problems that require a tailored model trained on your own data. Azure Custom Vision provides that capability by letting you train classification or object-detection models on images captured in your environment.

<Frame>
  <img alt="A presentation slide titled &#x22;Custom Vision Model&#x22; showing three icons under a &#x22;Standard Image Recognition Models&#x22; banner labeled &#x22;Small scratches,&#x22; &#x22;Dents,&#x22; and &#x22;Missing components.&#x22; Each icon has a red X, indicating these problems are not handled by standard image recognition models." />
</Frame>

High-level workflow to build a Custom Vision model:

1. Collect and upload images of both defective and non-defective parts.
2. Label (tag) defects such as scratches, dents, cracks, or "clean."
3. Train the model on this labeled dataset.
4. Deploy the trained model to an inspection pipeline that scores new images and flags issues.

Because the model is trained on images from your factory (lighting, camera angle, part variations), it learns to operate reliably in your environment rather than relying on generic datasets.

A simple illustration: teach a model to recognize apples. Upload \~50 images labeled "apple," train a classifier, and the model predicts "apple" for similar new images.

<Frame>
  <img alt="A slide titled &#x22;Custom Vision Model&#x22; showing apple images fed into a cloud-shaped model icon. The model is then used to predict the label &#x22;Apple&#x22; for new images." />
</Frame>

Training process (four main steps):

* Step 1 — Upload images: Include all relevant variations (angles, lighting, part conditions).
* Step 2 — Label images: Tag regions (for detection) or whole images (for classification) with categories like scratch, dent, missing-component, or ok.
* Step 3 — Train the model: Choose the right domain (classification vs object detection), then start a training run in Custom Vision.
* Step 4 — Query for predictions: Send new images to the model via the REST API or SDK to receive labels, bounding boxes (object detection), and confidence scores.

<Frame>
  <img alt="A slide titled &#x22;Steps to Train a Custom Vision Model&#x22; showing a four-step flow: Step 1 Upload Images, Step 2 Label Images, Step 3 Train the Model, and Step 4 Query for Predictions." />
</Frame>

Quick example — Calling the prediction API (HTTP):

* Endpoint: your Custom Vision prediction endpoint (region-specific)
* Key: your prediction resource key
* Project and iteration: the model you trained

Example curl (replace placeholders):

```bash theme={null}
curl -s -X POST "https://<your-endpoint>/customvision/v3.0/Prediction/<project-id>/classify/iterations/<iteration-name>/image" \
  -H "Prediction-Key: <your-prediction-key>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@sample.jpg"
```

The response returns predicted tags and confidence scores (and bounding boxes if the model is object detection).

When to use Custom Vision

| Use case                  | Why Custom Vision                                                                               | Example                                    |
| ------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Domain-specific detection | Generic models miss subtle, domain-specific defects—use your factory images to improve accuracy | Detect hairline cracks in tempered glass   |
| Production consistency    | Model trained on your camera, lighting, and part variants reduces false positives               | Verify screw placement on an assembly line |
| Iterative improvement     | Add hard examples and retrain to improve recall/precision over time                             | Reduce misses for rare defect types        |
| Fast prototyping          | Web UI + SDKs let you get a proof-of-concept quickly                                            | Classify ripe vs spoiled fruit for sorting |

Benefits include tailored recognition for your use case, improved accuracy from domain-specific training data, and the ability to refine performance by collecting new labeled images and retraining.

<Frame>
  <img alt="A presentation slide titled &#x22;Key Benefits of Custom Vision Model&#x22; with three numbered panels. The panels list: customized image recognition for specific use cases, improved accuracy from domain-specific training, and support for ongoing refinement by adding data and retraining." />
</Frame>

<Callout icon="lightbulb">
  Best practices: collect diverse, well-labeled examples that reflect real operating conditions (lighting, camera position, part variants). Start with a balanced dataset across classes and continuously add hard examples where the model fails. Use object detection when localization of defects is required, and monitor performance using precision/recall and confusion matrices.
</Callout>

Next steps and references

This article covered image classification with Custom Vision — dataset preparation, choosing a domain, training, and calling the prediction API. For detailed guides and SDKs, see:

* [Azure Custom Vision documentation](https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/)
* [Quickstart: Train and export a model (Custom Vision)](https://learn.microsoft.com/azure/cognitive-services/custom-vision-service/quickstarts/)
* [Custom Vision REST API reference](https://learn.microsoft.com[AWS_SECRET_ACCESS_KEY]/)

If you want sample code (Python, C#, or Node.js) for training or predictions, use the SDK examples in the Azure docs and replace placeholders with your project ID, iteration name, endpoint, and prediction key.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/ebc335c9-6d06-4770-9bc9-8fd3f250d3e6/lesson/2dd296bc-43d0-4274-875b-3e2c1cf3c9b3" />
</CardGroup>
