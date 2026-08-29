# Options to Host a Model for Inference Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/Persona-SageMaker-Activities-MLOps-Engineer/Options-to-Host-a-Model-for-Inference-Part-2/page

Comparison of using Boto3 versus the SageMaker Python SDK to create and invoke Amazon SageMaker real time endpoints, highlighting tradeoffs, workflows, and a hybrid approach

In this lesson we compare two primary ways to provision an Amazon SageMaker Endpoint for real-time inference: the low-level Boto3 SDK and the higher-level SageMaker Python SDK. Choose Boto3 when you need precise infrastructure control; choose the SageMaker SDK when you want ML-first convenience and faster development.

> **lightbulb** Both the Boto3 and SageMaker SDK approaches create the same underlying AWS resources (an Endpoint and an Endpoint Configuration). Choose the SDK based on whether you need fine-grained control (Boto3) or faster, ML-focused development (SageMaker SDK).

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: SDK Methods&#x22; comparing two ways to create endpoints: Boto3 SDK for more granular endpoint configuration and SageMaker SDK for simplified creation using an abstract Predictor class. It also notes that both methods deploy an endpoint and an endpoint configuration object." />
</Frame>

## Overview

Both SDKs ultimately produce the same SageMaker resources: an Endpoint Configuration and an Endpoint. The difference is how you get there:

* Boto3 (low-level): explicitly create an Endpoint Configuration, then create the Endpoint that references it. Gives maximal control over the infra.
* SageMaker Python SDK (high-level): create a Model object and call its deploy method; the SDK generates the Endpoint Configuration and Endpoint for you. Faster to iterate for ML workloads.

Quick comparison

| SDK                  | Best for                                     | Typical workflow                                                           |
| -------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| Boto3                | Fine-grained infra control, custom configs   | create\_endpoint\_config → create\_endpoint → invoke via sagemaker-runtime |
| SageMaker Python SDK | Rapid ML development, simpler inference code | Model(...) → model.deploy(...) → predictor.predict(...)                    |
| Hybrid               | Custom infra with SDK ergonomics             | create infra with Boto3 → use SageMaker Predictor for inference            |

## Boto3: create an Endpoint Configuration

With Boto3 you first create an Endpoint Configuration that describes the serving infrastructure (instance type, initial instance count, the model to serve, and other parameters). The following example assumes a SageMaker Model named "linear-learner-model" already exists in your account:

```python theme={null}
import boto3
