# Accuracy and Confidence Scores

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Develop-a-Document-Intelligence-Solution/Accuracy-and-Confidence-Scores/page

Explains estimated per-field accuracy versus per-prediction confidence in Azure Document Intelligence, how to view them in Studio, and how to use them for deployment and runtime decisions

Understanding the difference between estimated accuracy and per-prediction confidence is essential when evaluating and operating custom Document Intelligence models. This article explains what each metric represents, how to inspect them in Azure Document Intelligence Studio, and practical patterns for using them in production.

What these metrics mean

* Estimated accuracy: an overall, per-field metric that predicts how well the model will perform on unseen documents. It’s computed by comparing the model’s predictions against labeled ground-truth examples during training and evaluation. Use it to select and compare models before wide deployment.
* Confidence: a per-prediction score returned with every extracted field in an inference response. Confidence indicates how certain the model is about a specific extraction and can be used to decide whether to accept, reject, or escalate an extraction for human review.

Visual example: field-level accuracy and per-prediction confidence

The image below shows two complementary views: the left panel summarizes per-field accuracy measured across test data, while the right panel lists confidence values for individual extracted entries.

<Frame>
  <img alt="A presentation slide titled &#x22;Accuracy and Confidence Scores&#x22; with two panels: the left shows three fields (Email, CompanyAddress, Signature) each at 80% accuracy, and the right shows confidence percentages and example extracted values for those fields. The right panel lists individual confidence scores next to sample extracted entries." />
</Frame>

In this example, per-field accuracy for Email, CompanyAddress, and Signature is 80%. Per-prediction confidence varies—for example, email extractions may show >95% confidence while signature extractions may be under 45%. This highlights why both metrics matter: accuracy forecasts aggregate performance, while confidence indicates reliability of a single extraction.

Where to view these metrics in Azure

* Model-level estimated accuracy: open Document Intelligence Studio and view the model overview. The per-field accuracy scores are derived from labeled evaluation data.
* Per-document confidence scores: run the model in the Test/Analyze view. The results pane lists each extracted field together with its confidence for that specific document.

<Frame>
  <img alt="A screenshot of the Azure AI Document Intelligence Studio showing a modal for a &#x22;marriage-cert-model&#x22; with a list of extracted field names (Bridegroom, Bride, DateOfMarriage, etc.) and their accuracy percentages. The background shows the Models view in a project called &#x22;marriage-cert-project.&#x22;" />
</Frame>

<Frame>
  <img alt="A screenshot of Azure AI Document Intelligence Studio showing a &#x22;Test model marriage-cert-model&#x22; analyzing a scanned marriage certificate (marked &#x22;Sample&#x22;) in the center. The right pane lists extracted fields (bride/groom, dates, place, signature) with confidence scores." />
</Frame>

Quick comparison

| Metric                      | What it measures                                             | Typical use                                             |
| --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| Estimated accuracy          | Per-field performance estimated from labeled evaluation data | Choose or compare models before production              |
| Confidence (per-prediction) | Model’s certainty for an individual extracted field          | Drive runtime decisions (accept/reject/flag for review) |

Practical guidance

<Callout icon="lightbulb">
  Use estimated accuracy to evaluate and select models. Use per-prediction confidence to decide whether to accept an extraction automatically, reject it, or route it for human verification. Common patterns include rejecting or flagging extractions below a confidence threshold (for example, under \~70%), or sending them to an operator for review.
</Callout>

<Callout icon="warning">
  Do not rely only on estimated accuracy when operating in production—accuracy represents average behavior across a dataset and may not reflect edge cases in your live documents. Always combine accuracy assessments with runtime confidence checks and periodic real-world validation.
</Callout>

Implementation notes and links

* Confidence values are returned in the inference response payload. Use them in your application logic to implement gating, human-in-the-loop workflows, or automated acceptance rules.
* Inspect models and run tests in Document Intelligence Studio:
  * Document Intelligence Studio: [https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/studio/](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/studio/)
  * Analyze documents API docs: [https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/how-to/analyze-documents](https://learn.microsoft.com/azure/applied-ai-services/document-intelligence/how-to/analyze-documents)

Summary

* Estimated accuracy is a per-field score from labeled evaluation data and predicts expected model performance on unseen documents.
* Confidence is a per-prediction score returned with inference responses indicating certainty for each extraction.
* Use both metrics together: estimated accuracy to assess model fitness and confidence to drive runtime decisions such as automated acceptance, rejection, or escalation to human review.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/85c9f500-329b-4e86-b15c-f2e499d8bee6/lesson/742fa30d-9d37-4ac4-89de-6ca91dc6cd6d" />
</CardGroup>
