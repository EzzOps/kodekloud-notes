# Demystifying Advanced SageMaker Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Wrap-Up/Demystifying-Advanced-SageMaker-Part-2/page

Advanced SageMaker practices for production ML including human-in-the-loop inference, scalable data labeling with Ground Truth, and managed RStudio integration with Python interoperability

This lesson focuses on three practical problems you’ll often face when deploying ML in production:

1. When to add a human in the loop for model inference (human review).
2. How to create labeled training data at scale (data labeling).
3. Providing a familiar R experience in the cloud (RStudio integration with SageMaker).

Each section below explains the problem, the managed SageMaker solution, and best-practice patterns you can adopt.

***

## 1) Human-in-the-loop: Why and when to involve people

Many applications require human validation of model predictions because of safety, fairness, or regulatory risk. Examples include medical imaging (false negatives are dangerous), loan approvals (regulatory and reputational risk), or high-value fraud decisions. Other common triggers for human review:

* Low-confidence model outputs (e.g., confidence \< configured threshold).
* Compliance or audit requirements.
* High-impact or ambiguous outcomes that demand human judgment.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: AI/ML Predictions Often Require Human Oversight&#x22; stating that many AI/ML applications need human review. It lists examples: sensitive decisions (e.g., medical diagnoses, loan approvals), low-confidence model predictions, and compliance/auditing requirements in regulated industries." />
</Frame>

<Callout icon="lightbulb">
  Humans-in-the-loop are appropriate when the cost of an incorrect automated decision is high or when regulations require an auditable human sign-off. You can combine ML confidence thresholds and business rules to automatically route ambiguous cases for review.
</Callout>

### SageMaker Augmented AI (A2I)

[SageMaker Augmented AI (A2I)](https://aws.amazon.com/sagemaker/augmented-ai/) is the managed AWS service for adding human review to inference workflows. Typical pattern:

1. Model produces a prediction and an associated confidence score.
2. If confidence is below a configured threshold (or a rule triggers), route the request into an A2I workflow.
3. A2I presents the prediction and supporting context to a human reviewer and captures their response.
4. The human decision is used to produce the final inference result.

You can choose built-in templates (e.g., image, document, text) or design custom reviewer UIs and quality controls.

Who can perform reviews?

| Workforce                               | Use case                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------ |
| Private (in-house) workforce            | Sensitive data, internal audits, regulated industries                    |
| Amazon Mechanical Turk                  | Large-scale, on-demand labeling or review for low-sensitivity data       |
| Third-party vendors via AWS Marketplace | Outsourced, specialized labeling providers with vetted security controls |

A2I is suited to scenarios that require human validation for safety, legal, or business reasons. It provides routing control, reviewer UI configuration, and integration with a variety of workforces.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Augmented AI (A2I)&#x22; that explains A2I as a way to add human review to ML workflows. Three highlighted points describe automated triggers for human review, custom/built-in workflows for document/image/NLP processing, and integration with Mechanical Turk or other workforces." />
</Frame>

***

## 2) Labeling training data at scale

If your training dataset is not pre-labeled, you need a reliable, scalable labeling strategy. Manual labeling is expensive, slow, and prone to inconsistencies—especially at scale.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Manual Data Labeling Is Costly and Error-Prone&#x22; that says &#x22;Labelling large datasets manually is:&#x22; and shows three icons labeled Expensive, Time-consuming, and Prone to human errors. The slide has a dark blue background and a small &#x22;© Copyright KodeKloud&#x22; note." />
</Frame>

### SageMaker Ground Truth

[SageMaker Ground Truth](https://aws.amazon.com/sagemaker/ground-truth/) coordinates human labelers, supplies UI templates and instructions, and offers automation/active-learning options to reduce cost and improve throughput.

Labeling workflow overview:

1. Create a labeling job with clear instructions and UI templates (classification, bounding boxes, segmentation, captions, etc.).
2. Select the workforce (private, Mechanical Turk, or marketplace vendor).
3. Aggregate outputs and apply quality controls (consensus, review, or automated checks).

Ground Truth reduces cost and increases throughput by enabling parallel annotation and by using automation where possible.

<Frame>
  <img alt="A screenshot of the &#x22;Solution: SageMaker Ground Truth&#x22; labeling interface, showing form fields to create an image caption. The task image displays a fluffy tan cat relaxing next to a large dog inside a house." />
</Frame>

### Ground Truth labeling modes

| Mode                                | Description                                                                                                              | Best for                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| Human-only                          | Every item is labeled by human workers                                                                                   | High-sensitivity or complex tasks                        |
| Human-in-the-loop (active learning) | Ground Truth trains an incremental model from human labels and auto-labels easy cases, sending uncertain items to humans | Balanced cost and quality                                |
| Fully automated                     | Automated labeling without humans                                                                                        | Low-risk, high-volume tasks where automation is reliable |

<Callout icon="warning">
  Quality controls are essential. Use redundancy (multiple annotators per item), consensus algorithms, spot-check reviews, and clear instructions to reduce label noise and achieve consistent datasets.
</Callout>

***

## 3) RStudio in SageMaker Studio: enabling R workflows

Many data scientists prefer R and the RStudio IDE. Running RStudio in the cloud requires integration with enterprise networking, security, and shared data access. Manual setup can be time-consuming for teams.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: SageMaker Studio Application – RStudio&#x22; showing an illustrated data scientist at a laptop with charts and a clipboard labeled &#x22;DATA,&#x22; alongside two R logos and the line &#x22;Many data scientists and statisticians use R and RStudio IDE.&#x22;" />
</Frame>

Challenges include:

* Installing and maintaining RStudio instances.
* Secure networking and IAM-based authentication.
* Collaboration and access to shared datasets.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: SageMaker Studio Application – RStudio&#x22; that lists three issues: setting up RStudio in the cloud is complex, it's difficult to ensure security and collaboration, and it requires manual configuration, networking, and authentication management. Icons and labels across the bottom highlight Manual configuration, Networking, and Authentication management." />
</Frame>

### Managed RStudio Workbench in SageMaker Studio

SageMaker Studio includes a managed RStudio Workbench (via [Posit RStudio Workbench](https://posit.co/products/workbench/)) that integrates with IAM, S3, and SageMaker training/inference. Users get the familiar multi-tab RStudio interface and can run R workflows without manual infrastructure setup.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: SageMaker Studio Application – RStudio&#x22; listing three points about a fully managed RStudio workbench integrated into SageMaker Studio, secure scalable collaborative cloud usage, and integration with AWS services. Icons for S3, SageMaker, and IAM appear across the bottom." />
</Frame>

R users can run standard R workflows (preprocessing, training, saving artifacts) and also interoperate with Python-based SageMaker tooling.

### Example: training with caret in R and saving artifacts

```r theme={null}
