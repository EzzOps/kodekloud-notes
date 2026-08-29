# ECS Fargate Experiment Idea and Hypothesis

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Chaos-Engineering-on-Serverless-Fargate/ECS-Fargate-Experiment-Idea-and-Hypothesis/page

Learn to use AWS Fault Injection Service to test the resilience of an ECS Fargate microservice under high I/O stress.

Learn how to leverage AWS Fault Injection Service (FIS) to validate the resilience of an Amazon ECS Fargate–based microservice under high I/O stress. This guide demonstrates running a controlled I/O fault on Fargate tasks to ensure your Pet Adoption payment API remains available.

## Introduction

Amazon ECS Fargate is a serverless compute engine for containers that lets you run Docker workloads without provisioning or managing servers. In this experiment, we’ll deploy a Pet Adoption payment API as two Fargate tasks, fronted by an Application Load Balancer and backed by a Pet Adoption database. Then we’ll launch an AWS FIS experiment to inject I/O stress and observe the behavior.

<Callout icon="lightbulb">
  Before starting, ensure you have the following prerequisites:

  * An AWS account with permissions to create FIS experiments, ECS clusters, IAM roles, and CloudWatch alarms.
  * A running ECS Fargate service with at least two tasks.
  * A target database (e.g., Amazon RDS) for the Pet Adoption back end.
</Callout>

## Architecture Overview

<Frame>
  ![The image is a diagram illustrating a serverless compute architecture using AWS Fargate, with a focus on maintaining application availability despite high I/O tasks. It includes components like a Pet Payment API and a Pet Adoption Database within a virtual private cloud.](../../../../images/kodekloud.com/kk-media/image/upload/v1752871915/notes-assets/images/Chaos-Engineering-ECS-Fargate-Experiment-Idea-and-Hypothesis/serverless-architecture-aws-fargate-diagram.jpg)
</Frame>

1. **Application Load Balancer** distributes incoming traffic to Fargate tasks.
2. **ECS Fargate Tasks** run the Pet Payment API.
3. **Pet Adoption Database** serves as the back-end data store.

## FIS Experiment Phases

Every AWS FIS experiment consists of two main phases:

| Experiment Phase | Description                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| Given            | The current running state of our ECS Fargate service and its infrastructure. |
| Hypothesis       | The expected system behavior when an I/O fault is injected.                  |

### 1. Given

* Two Fargate tasks in an ECS service named `pet-payment-service`.
* An Application Load Balancer routing traffic to `pet-payment-service` on port 80.
* A connected Pet Adoption database (e.g., Amazon RDS or DynamoDB).

```bash theme={null}
