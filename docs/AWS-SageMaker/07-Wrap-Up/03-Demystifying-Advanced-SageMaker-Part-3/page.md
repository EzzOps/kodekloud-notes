# Example R training snippet using caret
df_train_transformed <- predict(preProcValues, df_train)

# train a model on df_train_transformed
library(caret)
fitControl <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 10,
  classProbs = TRUE,
  summaryFunction = twoClassSummary
)

set.seed(825)
gbmFit <- train(
  Class ~ .,
  data = df_train_transformed[, 2:11],
  method = "gbm",
  trControl = fitControl,
  verbose = FALSE,   # passed through to the underlying method
  metric = "ROC"
)

print(gbmFit)

saveRDS(preProcValues, file = "./preProcessor.rds")
saveRDS(gbmFit, file = "./gbm_model.rds")
saveRDS(df_test[, 1:10], file = "./breast_cancer_test_data.rds")
```

### Interoperability: calling the SageMaker Python SDK from R

Use the [reticulate](https://rstudio.github.io/reticulate/) package to import Python modules and call the SageMaker Python SDK directly from RStudio. This allows R users to provision training jobs, endpoints, and other SageMaker resources from R.

```r theme={null}
# Example using reticulate to call the SageMaker Python SDK from R
library(reticulate)

sagemaker <- import("sagemaker")
Estimator <- sagemaker$estimator$Estimator

# Create a SageMaker Estimator via the Python SDK
est <- Estimator(
  image_uri = "123456789012.dkr.ecr.us-west-2.amazonaws.com/my-image:latest",
  role = "arn:aws:iam::123456789012:role/SageMakerRole",
  instance_count = 1L,
  instance_type = "ml.m5.large",
  sagemaker_session = sagemaker$Session()
)

# Start a training job (S3 path should contain training data)
est$fit("s3://my-bucket/my-training-data/")
```

Using reticulate provides the best of both worlds: RStudio as the native IDE for R users, and access to SageMaker's Python SDK for orchestration.

***

## Summary

This lesson covered three production concerns and the SageMaker solutions to address them:

* Human-in-the-loop inference with SageMaker Augmented AI (A2I) — route low-confidence or regulated decisions for human review.
* Scalable labeling with SageMaker Ground Truth — hybrid labeling, active learning, and automation to reduce cost and increase throughput.
* Managed RStudio Workbench inside SageMaker Studio and Python interoperability via reticulate — enable R users to work securely and integrate with SageMaker services.

Additional references:

* [SageMaker Augmented AI (A2I)](https://aws.amazon.com/sagemaker/augmented-ai/)
* [SageMaker Ground Truth](https://aws.amazon.com/sagemaker/ground-truth/)
* [SageMaker Studio](https://aws.amazon.com/sagemaker/studio/)
* [Posit RStudio Workbench](https://posit.co/products/workbench/)
* [reticulate R package](https://rstudio.github.io/reticulate/)
* [caret package documentation](https://topepo.github.io/caret/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b8b80e38-7fae-401c-a5ff-d6f0af493cea/lesson/7f40c556-0f5d-445f-8a34-9b54acafb32f)


# Demystifying Advanced SageMaker Part 3

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Wrap-Up/Demystifying-Advanced-SageMaker-Part-3/page

Explains using MLflow with Amazon SageMaker to unify experiment tracking, model registry, and multi-platform deployment for consistent ML lifecycle management

In this lesson we address a common pain point: fragmentation of the ML lifecycle. When teams run experiments across different platforms—local machines, on-prem clusters, Kubernetes, SageMaker, or Databricks—tracking experiments, versions, and deployments becomes difficult. Typical issues include:

* Incomplete experiment tracking (hyperparameters, metrics, and artifacts not consistently recorded).
* Fragmented model versioning across teams and environments.
* Inefficient serving patterns when each model is containerized and hosted separately.
* Divergent local vs cloud workflows that make productionization error-prone.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: ML Lifecycle Management Is Fragmented&#x22; that lists four challenges: lack of experiment tracking, difficulty with model versioning across teams, inefficient deployment/serving, and inconsistent local vs cloud workflows. Each challenge is shown in a numbered card with a small icon." />
</Frame>

The solution we cover here is MLflow: an open-source ML lifecycle tool that standardizes experiment tracking, model registry, and deployment orchestration across platforms.

## What is MLflow and why use it?

MLflow provides three core capabilities:

* Experiment tracking: log parameters, metrics, and artifacts to compare runs.
* Model registry: version and promote models through stages (Staging → Production).
* Deployment management: package models for deployment to multiple targets.

Its platform-agnostic design makes it a good fit when teams need a consistent lifecycle system that spans local development, on-prem infrastructure, Kubernetes, SageMaker, and other cloud providers.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: MLflow.&#x22; It highlights MLflow's features—experiment tracking, model registry, and deployment—shown in a three-lobed diagram with icons." />
</Frame>

## MLflow and SageMaker: complementary, not competing

SageMaker can host MLflow as a managed application, providing a hosted tracking server, model registry, and integration points without you managing the underlying infrastructure. This setup lets teams:

* Use MLflow for consistent experiment tracking and model governance across environments.
* Leverage SageMaker for managed training, scalable compute, and production-grade endpoints.

> **lightbulb** SageMaker includes native experiment-tracking and model registry features that are tightly integrated into the SageMaker experience. If you need an industry-standard, cross-platform lifecycle system, MLflow is a useful alternative for tracking and registry, while still allowing you to use SageMaker for training and hosting.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: MLflow&#x22; showing five numbered boxes that outline MLflow features and SageMaker integration. The items list MLflow Tracking Server, Model Registry, deployment to SageMaker endpoints, SageMaker Pipelines automation, and scalability via SageMaker-managed infrastructure." />
</Frame>

## Core MLflow strengths (quick reference)

| Feature                | Benefit                                              | Example                                                      |
| ---------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Experiment tracking    | Compare runs, visualize metrics, and store artifacts | `mlflow.log_param("lr", 0.01)`                               |
| Model registry         | Versioned models with stage transitions and metadata | Promote model v1 → staging → production                      |
| Reproducibility        | Run metadata and artifacts provide lineage           | Reproduce a training run with stored artifacts               |
| Platform-agnostic      | Single lifecycle layer across local, on-prem, cloud  | MLflow tracking server accessible from multiple environments |
| Pipeline orchestration | Automate lifecycle steps (train → register → deploy) | MLflow + CI/CD to deploy a registered model                  |

## Typical MLflow + SageMaker workflow

A common pattern blends MLflow’s lifecycle features with SageMaker’s managed compute. Example flow:

1. Train the model using SageMaker training jobs (or local/remote training).
2. Log hyperparameters, metrics, and artifacts to the MLflow tracking server.
3. Register the trained model in the MLflow Model Registry.
4. Deploy the registered model to a SageMaker endpoint for real-time inference.
5. Monitor production predictions with SageMaker Model Monitor and feed metrics back to MLflow as needed.

<Frame>
  <img alt="A slide titled &#x22;Solution: MLflow&#x22; showing a five-step workflow diagram for integrating MLflow with SageMaker. It outlines: train with SageMaker, log metrics to MLflow tracking, register models in the MLflow Model Registry, deploy to SageMaker endpoints, and monitor with SageMaker Model Monitor." />
</Frame>

## Deployment targets and packaging

MLflow can package models as a Docker container or a Python function and orchestrate deployments to multiple targets. This makes it easy to maintain a single source of truth (the model registry) while choosing the most appropriate serving platform.

<Frame>
  <img alt="A diagram titled &#x22;Solution: MLflow&#x22; showing ML model development with MLflow tracking and a model registry, packaging the model into a Docker container. It shows deployments to production targets (Databricks Model Serving, Amazon SageMaker, Kubernetes, Azure ML) or local inference via a Flask server or batch prediction." />
</Frame>

Deployment targets include:

| Target type                     | Use case                                                           |
| ------------------------------- | ------------------------------------------------------------------ |
| SageMaker endpoints             | Managed real-time inference with autoscaling and monitoring        |
| Azure ML                        | Cloud-native model serving and MLOps integration                   |
| Kubernetes                      | Self-managed scalable serving with k8s operators or KFServing/Vela |
| Databricks Model Serving        | Integrated serving for Databricks environments                     |
| Local/Batch (Flask, batch jobs) | Development, testing, or large-scale offline inference             |

MLflow can also trigger platform-specific automation—e.g., invoking SageMaker Pipelines or CI/CD jobs—so it functions as a lifecycle orchestrator while letting platform services execute hosting, scaling, and monitoring.

> **lightbulb** MLflow is platform-agnostic and integrates with SageMaker—use MLflow for consistent experiment tracking and registry, and use SageMaker for managed training, serving, and monitoring. They can be combined rather than treated as mutually exclusive.

## Lesson summary

* Foundation models: adopt pre-trained vendor models (OpenAI, Anthropic, Meta, etc.) and fine-tune or prompt-engineer for production.
* Distributed training: coordinate large-scale training with cluster controllers for networking, GPU scheduling, and recoverability.
* Human-in-the-loop: add reviewers for low-confidence or edge-case predictions to improve model quality.
* Managed data labeling: combine human workflows with model-assisted labeling to speed labeling cycles.
* Hosted RStudio: provide managed RStudio for teams that require R-based analysis and modeling.
* MLflow: use an industry-standard lifecycle tool for experiment tracking, model registry, and cross-platform deployment; optionally run MLflow as a managed app on SageMaker.

That wraps up this lesson. Next, we’ll look at what’s new in SageMaker for 2025 and walk through recent product announcements.

## Links and references

* [MLflow documentation](https://mlflow.org/docs/latest/index.html)
* [Amazon SageMaker documentation](https://docs.aws.amazon.com/sagemaker/)
* [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
* [Databricks Model Serving](https://docs.databricks.com/model-serving/index.html)
* [Kubernetes documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/b8b80e38-7fae-401c-a5ff-d6f0af493cea/lesson/cc28e60a-563a-4a4f-b0d1-f83849203cad)
