# Summary of Domain 2 ML Model Development

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Bringing-it-all-together/Summary-of-Domain-2-ML-Model-Development/page

Overview of machine learning model development covering lifecycle stages, algorithms, training and tuning, regularization, fine tuning and ensemble methods, deployment patterns, automation, and production monitoring on AWS

This lesson summarizes the core concepts from this domain, highlighting the end-to-end machine learning lifecycle, common algorithms and techniques, troubleshooting tips, and production-ready deployment patterns.

At a high level, the machine learning lifecycle has four stages:

* Prepare: gather, clean, and explore raw data.
* Build: design data pipelines and select appropriate model families.
* Train and Tune: optimize model parameters and hyperparameters.
* Deploy and Manage: release models into production and monitor them continuously.

<Frame>
  <img alt="The image is a flowchart illustrating the four stages of the machine learning lifecycle: Prepare, Build, Train and Tune, and Deploy and Manage. Each stage has a brief description of its purpose." />
</Frame>

Supervised learning is one of the most common paradigms and splits into two main tasks:

* Regression — predicts continuous values (for example, estimating a house price). Often visualized as fitting a best-fit line or curve to data points.
* Classification — predicts discrete labels (for example, detecting whether an email is spam). Conceptually this finds decision boundaries that separate classes.

<Frame>
  <img alt="The image presents two types of supervised learning: regression, illustrated with a linear line fitting data points, and classification, shown with a curve distinguishing different groups of data points." />
</Frame>

Model training loop — concise steps for iterative learning:

1. Feed inputs and training data into the learning model.
2. The model produces predictions (outputs).
3. Compute an error (loss) using a chosen loss function.
4. Pass the error to the learning algorithm (optimizer).
5. Update model parameters to reduce error and repeat until convergence.

<Frame>
  <img alt="The image is a flowchart depicting the process of machine learning training, showing interactions between the input, learning model, training data, learning algorithm, and output. It includes labeled arrows for parameter updates and error functions." />
</Frame>

Algorithms commonly used for structured (tabular) data

| Algorithm                 | Use case                             | Notes                                                             |
| ------------------------- | ------------------------------------ | ----------------------------------------------------------------- |
| Linear Learner            | Regression / classification baseline | Fast, interpretable, good for linearly separable problems         |
| XGBoost                   | Regression / classification          | Gradient-boosted trees — strong performance on many tabular tasks |
| Factorization Machines    | Recommendation / sparse interactions | Models pairwise feature interactions effectively                  |
| K-Nearest Neighbors (KNN) | Classification / simple regression   | Non-parametric; performance sensitive to feature scaling          |
| Object2Vec                | Embedding categorical/item features  | Learns vector representations for discrete objects                |

<Frame>
  <img alt="The image lists types of machine learning algorithms used for tabular data: Linear Learner, XGBoost, Factorization Machines, K-Nearest Neighbors (KNN), and Object2Vec." />
</Frame>

Regularization techniques control model complexity and reduce overfitting. Common strategies:

| Regularization | Penalty                   | Effect                                         |
| -------------- | ------------------------- | ---------------------------------------------- |
| L1 (Lasso)     | Absolute value of weights | Encourages sparsity — many weights become zero |
| L2 (Ridge)     | Square of weights         | Smoothly shrinks weights toward zero           |
| ElasticNet     | Combination of L1 and L2  | Balances sparsity (L1) and stability (L2)      |

<Frame>
  <img alt="The image is a diagram titled &#x22;Types of Regularization in ML,&#x22; showing L1 Regularization (Lasso), L2 Regularization (Ridge), and Elastic Net, with brief explanations of their penalties." />
</Frame>

Managed AI services (example AWS offerings) let you add intelligence to apps without building models from scratch:

* Amazon Translate — real-time language translation
* Amazon Rekognition — image and video analysis (objects, faces, content)
* Amazon Transcribe — speech-to-text transcription
* Amazon Polly — text-to-speech synthesis

Popular foundation model families provide pre-trained base models you can adapt for tasks. Examples from major providers include command and instruction-tuned families and text/vision generators.

<Frame>
  <img alt="The image lists popular foundation model families with their logos, including Command by Cohere, J1-Jumbo-Instruct by AI21 Labs, Titan by Amazon, Claude by Anthropic, Stable Diffusion by Stability AI, Llama 3 by Meta, and Mistral by Mistral AI." />
</Frame>

Fine-tuning workflow — high-level pattern:

* Start with a pre-trained base model that encodes general knowledge.
* Add task-specific layers or adapt existing layers for your objective.
* Train on domain-specific data (often with lower learning rates and regularization).
* Validate and iterate until the model meets performance and safety criteria.

Parallelism strategies for large fine-tuned models:

* Data parallelism: replicate the full model across devices; each replica processes a different batch and synchronizes gradients.
* Model parallelism: split the model across devices so a single example flows through model partitions (useful for very large architectures).

<Frame>
  <img alt="The image illustrates concepts of data parallelism and model parallelism within a fine-tuned model architecture, showing how data and computations are distributed." />
</Frame>

Ensemble methods increase robustness and often improve predictive performance. Key points:

* Combine multiple models (averaging, majority voting, stacking).
* Benefit from error reduction: different models make different errors.
* Help manage the bias–variance tradeoff and improve generalization.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Why Ensembles Work,&#x22; listing reasons such as Error Reduction, Diversity of Models, Bias-Variance Tradeoff, Robustness, and Wisdom of the Crowd (Intuition)." />
</Frame>

Common causes for non-convergence during training

| Cause                     | Symptom                                | Quick remediation                                      |
| ------------------------- | -------------------------------------- | ------------------------------------------------------ |
| Learning rate too high    | Loss diverges or oscillates            | Reduce learning rate, use learning rate schedule       |
| Poor data quality         | High validation error, noisy gradients | Clean labels, remove outliers, feature selection       |
| Improper preprocessing    | Slow or unstable training              | Normalize/scale features, encode categorical variables |
| Bad weight initialization | Stalled or slow learning               | Use better initialization schemes (He, Xavier)         |
| Poor hyperparameters      | Suboptimal performance                 | Tune batch size, optimizer, momentum, regularization   |

<Frame>
  <img alt="The image lists root causes of non-convergence in machine learning: high learning rate, poor data quality, improper data preprocessing, and bad initialization of weights." />
</Frame>

<Callout icon="lightbulb">
  High-quality, well-preprocessed data and sensible initialization/hyperparameter choices are often the fastest way to fix convergence problems.
</Callout>

Automating ML development and delivery on AWS (example architecture)

A typical automated pipeline using SageMaker Pipelines and other AWS services:

1. Trigger via EventBridge schedule or when new data arrives in `Amazon S3`.
2. SageMaker Pipelines runs a processing job to preprocess and validate data.
3. A SageMaker training job trains the model using the cleaned data.
4. A subsequent processing job evaluates the trained model.
5. If the model meets criteria, it is approved and registered in the SageMaker Model Registry.
6. An `AWS Lambda` step or a pipeline deployment step deploys the registered model to an endpoint (asynchronous or synchronous), with autoscaling for client traffic.
7. Clients access the deployed endpoint for inference.

Most of this workflow is expressed in Python within SageMaker Studio notebooks, enabling reproducibility and CI/CD integration.

<Frame>
  <img alt="The image illustrates an automated development pipeline using AWS services, including EventBridge, S3, SageMaker, and Lambda, for model training, evaluation, and deployment. It shows a flow from data preprocessing to model registration and deployment with clients accessing the final endpoint." />
</Frame>

Shadow deployments — safe testing with real traffic

* Route user requests to the production (primary) variant as usual.
* Send a copy of each request to the shadow (candidate) variant for evaluation.
* The shadow processes requests and logs outputs for offline analysis but does not return responses to users.
* Compare shadow predictions to production behavior to detect regressions or improvements under real-world traffic patterns.

<Frame>
  <img alt="The image is a diagram showing when to use shadow deployment in AWS SageMaker, illustrating the flow between production and shadow variants, including components like the model, container, and instance." />
</Frame>

Key takeaways

* Machine learning categories: supervised, unsupervised, and reinforcement learning.
* Good data, correct error (loss) functions, and appropriate validation are essential for effective model training and evaluation.
* Regularization (L1, L2, ElasticNet) helps control overfitting and shapes model sparsity and weight magnitudes.
* Foundation models and pre-trained checkpoints accelerate development; fine-tuning adapts them to specific tasks.
* Address convergence issues by adjusting learning rates, improving data quality and preprocessing, using better initializations, and tuning hyperparameters.
* Production workflows include automated pipelines, model registries, safe rollout strategies (blue/green, canary, shadow), and continuous monitoring to manage drift and performance.

<Frame>
  <img alt="The image is a summary slide showing key points about foundation, pre-trained, and fine-tuned models, reasons for model non-convergence, and deploying machine learning models in production." />
</Frame>

Practical deployment checklist

* Register and version models in a model registry.
* Implement approval gates (automated tests, performance thresholds).
* Use controlled rollout strategies (blue/green, canary, shadow) for safe releases.
* Monitor endpoint performance and drift; be ready to roll forward, roll back, or retrain.

Links and references

* [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* For foundational reading on model regularization and optimization: consider standard ML textbooks and the latest practitioner blogs for real-world tuning advice.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/dd1231df-ce1b-453d-92d6-e6250b5d45cf/lesson/f9aed433-b248-4451-b565-7832c815311a" />
</CardGroup>
