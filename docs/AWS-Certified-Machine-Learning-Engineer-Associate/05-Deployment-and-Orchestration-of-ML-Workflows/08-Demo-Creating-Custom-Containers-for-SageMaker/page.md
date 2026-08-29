# Authenticate (example, replace <aws-region> and <account-id>)
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<aws-region>.amazonaws.com

# Build and push
docker build -t my-ml-service:latest .
docker tag my-ml-service:latest <account-id>.dkr.ecr.<aws-region>.amazonaws.com/my-ml-service:latest
docker push <account-id>.dkr.ecr.<aws-region>.amazonaws.com/my-ml-service:latest
```

Monitoring pipeline for containerized ML
A reliable monitoring stack includes logs, metrics, and audit trails:

1. Build and train the model; package and publish the container image.
2. Push the image to Amazon ECR.
3. Deploy to runtime: SageMaker endpoint, ECS service, or EKS pods.
4. Emit logs/metrics to Amazon CloudWatch and capture API/activity audit logs with AWS CloudTrail.
5. Use SageMaker Model Monitor (if available) and CloudWatch dashboards/alarms to observe model performance, latency, and data drift.

This combination provides visibility into operational health, security, and model quality.

<Frame>
  <img alt="The image is a flowchart illustrating the process of monitoring containerized machine learning, involving steps from building/training the model to deployment, and utilizing AWS services like CloudWatch, CloudTrail, and SageMaker Monitoring for logs and metrics." />
</Frame>

Anti-patterns to avoid

* Oversized images: include only the runtime dependencies you need. Smaller images reduce attack surface and speed deployments.
* Hard-coded secrets: never bake API keys or passwords into images. Use secrets management.
* Mixing training and inference in the same runtime: training can consume resources and destabilize inference—use separate environments.
* Skipping orchestration in production: rely on ECS/EKS/SageMaker for scaling, health checks, and rollbacks.

<Callout icon="warning">
  Avoid storing secrets in images or environment variables that are committed to source control. Use secret stores and IAM to reduce compromise risk.
</Callout>

<Frame>
  <img alt="The image lists three anti-patterns to avoid: oversized containers, hardcoded secrets, and mixing training with inference." />
</Frame>

Key takeaways

* Use containers to make ML deployments portable, consistent, and reproducible across environments.
* Choose the right AWS service:
  * SageMaker for managed ML training/inference and model lifecycle tooling.
  * ECS for simple container orchestration with EC2/Fargate.
  * EKS for Kubernetes-driven orchestration and complex deployments.
* Secure your environment with IAM, VPC networking, image scanning (ECR), and secrets management.
* Monitor systems using CloudWatch, CloudTrail, and SageMaker Model Monitor to detect drift, latency spikes, and operational issues.
* Optimize hosting costs: use Multi-Model Endpoints where appropriate, right-size instances, evaluate serverless options, and automate model lifecycle actions.

<Frame>
  <img alt="The image presents a summary slide with three key points: using containers for portability, choosing the right service (SageMaker, ECS, or EKS), and securing with IAM, VPC, and ECR while avoiding anti-patterns." />
</Frame>

Further reading and references

* AWS SageMaker documentation: [https://docs.aws.amazon.com/sagemaker/](https://docs.aws.amazon.com/sagemaker/)
* Amazon ECR image scanning: [https://aws.amazon.com/ecr/](https://aws.amazon.com/ecr/)
* Amazon ECS: [https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs)
* Amazon EKS: [https://learn.kodekloud.com/user/courses/aws-eks](https://learn.kodekloud.com/user/courses/aws-eks)
* CloudWatch and CloudTrail for observability: [https://learn.kodekloud.com/user/courses/aws-cloudwatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch) and [https://aws.amazon.com/cloudtrail/](https://aws.amazon.com/cloudtrail/)

And finally: actively optimize hosting costs and operational overhead by leveraging multi-model endpoints, right-sizing, serverless options where suitable, and automating model deployments and rollbacks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/d9cc3da2-e722-44d0-8cec-ce5ceda6236e" />
</CardGroup>


# Demo Creating Custom Containers for SageMaker

Source: https://notes.kodekloud.com/docs/AWS-Certified-Machine-Learning-Engineer-Associate/Deployment-and-Orchestration-of-ML-Workflows/Demo-Creating-Custom-Containers-for-SageMaker/page

Guide to registering and creating Amazon SageMaker models from existing ECR container images and S3 model artifacts via the console, including required fields, VPC and IAM permissions.

If you already have a model container image pushed to Amazon ECR and your model artifacts packaged in Amazon S3, you can register that image and artifact location with Amazon SageMaker and create a SageMaker model directly from the console. This guide walks through the console workflow and highlights the key fields you must complete to register a model that uses an existing ECR image.

Useful references:

* [Amazon SageMaker Models](https://docs.aws.amazon.com/sagemaker/latest/dg/models.html)
* [Amazon ECR documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [IAM permissions for Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html)

Prerequisites

* An ECR image containing your inference code (public or private).
* A model artifact archive (for example, `model.tar.gz`) uploaded to S3.
* A SageMaker execution role with permissions to pull from ECR and read the S3 artifact.
* If the image or S3 bucket is in another AWS account, verify cross-account access and roles.

Console workflow (step-by-step)

1. Open the Amazon SageMaker console and navigate to Inference → Models.
2. Click **Create model**.
3. In the Create model form choose the container input option that lets you "Provide model artifacts and inference image location." This option points SageMaker to:
   * an ECR image for inference, and
   * an S3 URI for your model artifacts.
4. Fill in the container details:
   * Inference image location: the full ECR image URI (for example, `123456789012.dkr.ecr.us-west-2.amazonaws.com/my-inference-image:latest`).
   * Model artifacts: the S3 URI where your model archive is stored (for example, `s3://my-bucket/models/my-model.tar.gz`).
   * (Optional) Environment variables to pass to your container at runtime.
   * (Optional) Container entrypoint or command overrides if your image expects them.
5. (Optional) Configure network isolation and VPC settings:
   * If the model needs access to resources inside a VPC, select the VPC and specify subnets and security groups. When you create an endpoint using this model, SageMaker will create ENIs in the selected subnets.
6. (Optional) Add tags for cost allocation or organizational metadata.
7. Click **Create model**. The new model will appear in the Models list and can be used to create real-time endpoints or batch transform jobs.

Container details — what to provide

* Inference image location: full ECR URI including account, region, repository, and tag.
* Model artifacts: S3 URI to the `.tar.gz` or tarred model directory.
* Environment variables: key/value pairs your inference container reads at startup.
* VPC settings: subnets and security groups if your model requires access to VPC resources.
* Tags: optional metadata to help manage and track costs.

Example values

| Resource             | Example                                                                  |
| -------------------- | ------------------------------------------------------------------------ |
| ECR image URI        | `123456789012.dkr.ecr.us-west-2.amazonaws.com/my-inference-image:latest` |
| Model artifacts (S3) | `s3://my-bucket/models/my-model.tar.gz`                                  |

<Callout icon="lightbulb">
  Ensure the SageMaker execution role you select has permissions to read the S3 model artifact and to pull the image from ECR. For private ECR repositories, the role typically needs `ecr:GetAuthorizationToken`, `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer`, and commonly `ecr:BatchCheckLayerAvailability`, plus S3 `s3:GetObject` for your model artifact. See the [IAM documentation for SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html) for more details.
</Callout>

<Callout icon="warning">
  If the image or artifacts are in a different AWS account or behind VPC networking rules, verify cross-account permissions, VPC endpoints, route tables, and security groups. Incorrect permissions or networking will prevent SageMaker from pulling the image or accessing the model artifacts.
</Callout>

<Frame>
  <img alt="The image shows an Amazon SageMaker console interface for creating a model, with options for selecting VPC, subnets, and security groups. There is also a section for adding optional tags." />
</Frame>

After creation

* The model will be listed in the SageMaker Models page.
* You can use the model to create a real-time endpoint (for low-latency inference) or a Batch Transform job (for offline inference).
* When you create an endpoint, SageMaker uses the model configuration (including VPC settings) to provision resources and attach ENIs into the selected subnets.

Additional resources

* [Create a model using a custom container (SageMaker Developer Guide)](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html)
* [Amazon ECR: authentication and authorization](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html)
* [Amazon S3 access control](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html)

That’s it — after the model is created you can proceed to deploy it as an endpoint for real-time inference or run a batch transform job for offline scoring.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-machine-learning-associates/module/c3d1a3a2-07f8-4702-8653-061263bb5db2/lesson/09a64291-7e73-44cb-bc71-42f3fa291ee2" />
</CardGroup>
