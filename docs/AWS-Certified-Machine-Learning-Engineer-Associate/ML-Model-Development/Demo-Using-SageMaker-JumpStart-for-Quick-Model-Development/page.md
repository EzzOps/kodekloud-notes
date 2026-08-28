# Demo Using SageMaker JumpStart for Quick Model Development

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/ML-Model-Development/Demo-Using-SageMaker-JumpStart-for-Quick-Model-Development/page

How to quickly develop, customize, fine tune and deploy models using Amazon SageMaker JumpStart with one click deployment, Studio UI or AI agents and endpoint configuration

This article demonstrates how to accelerate model development and deployment using Amazon SageMaker JumpStart. JumpStart provides ready-made models, end-to-end customization workflows, and one-click deployment to SageMaker real-time endpoints — enabling rapid experimentation, fine-tuning, and production serving with minimal setup.

<Frame>
  <img alt="This image shows the AWS SageMaker Studio interface, specifically the Models section where users can discover, deploy, and customize various machine learning models. It highlights &#x22;Spotlight Models&#x22; with options like Qwen3.5-4B and Nvidia Nemotron3 Nano Omni." />
</Frame>

In SageMaker Studio’s Models section you can browse pretrained and starter models, inspect model details, and begin customization or deployment. JumpStart supports two primary customization paths:

<Frame>
  <img alt="The image shows a screen from SageMaker Studio with options to customize a model using either a UI or an AI agent. The interface provides a description and a &#x22;Continue&#x22; button for each option." />
</Frame>

* Customize with the UI: follow a guided, point-and-click flow to select a technique, upload your dataset, configure hyperparameters, and run fine-tuning or evaluation jobs.
* Customize with an AI agent: use conversational prompts and agent recommendations to automate common steps and accelerate iteration.

You can also skip customization and deploy a chosen model directly (for example, a linear classifier). Deployment configuration centers on two main aspects:

1. The endpoint name — the SageMaker real-time endpoint that clients call for inference (e.g., `my-model-endpoint`).
2. The compute backing the endpoint — the instance type and initial instance count that host the model.

<Frame>
  <img alt="This image shows the AWS SageMaker Studio interface where a user is deploying a model to an endpoint, with options for setting the endpoint name, instance type, and initial instance count." />
</Frame>

When choosing instance types, select from the SageMaker-supported ML instance families. Pick an instance that aligns with your latency, memory, and throughput needs. Example instance choices:

| Instance type  | vCPU / Memory (approx.) | Use case                        | Example price (region-dependent) |
| -------------- | ----------------------- | ------------------------------- | -------------------------------- |
| `ml.m5.large`  | 2 vCPU / 8 GiB RAM      | Small models, dev/testing       | \~\$0.115 / hour                 |
| `ml.m5.xlarge` | 4 vCPU / 16 GiB RAM     | Moderate workloads, low-latency | \~\$0.23 / hour                  |

For the most up-to-date instance family options and region pricing, see the SageMaker instance types documentation: [https://docs.aws.amazon.com/sagemaker/latest/dg/instance-types.html](https://docs.aws.amazon.com/sagemaker/latest/dg/instance-types.html)

You can also review and adjust additional deployment settings such as the execution IAM role, VPC/networking, and environment variables. SageMaker Studio provides a default execution role; however, if your workflow needs to read training data or save artifacts to S3, ensure the role grants the necessary Amazon S3 permissions.

<Frame>
  <img alt="The image shows the AWS SageMaker Studio interface with settings for deploying a model, including IAM Role and VPC configuration options. On the left, there are various application icons like JupyterLab and Canvas." />
</Frame>

Quick deployment checklist:

* Decide an endpoint name (`my-model-endpoint`).
* Select instance type(s) and initial replica count.
* Confirm the execution role has S3 access (for data/model artifacts).
* Configure VPC and networking if you require private access.
* Review costs for chosen instance types and replica counts.

Deployment steps (Studio UI):

1. Select the model and click Deploy.
2. Enter an endpoint name, choose instance type and count.
3. Verify IAM role and networking settings.
4. Click Deploy — SageMaker will provision the endpoint and start serving after deployment is complete.

CLI example (create model → create endpoint config → create endpoint):

```bash theme={null}
