# Create the repository (replace REGION and myapp as needed)
aws ecr create-repository --repository-name myapp --region REGION
```

Authenticate to ECR, tag, and push the image:

```bash theme={null}
# Authenticate to ECR (replace REGION and ACCOUNT_ID)
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com

# Tag the local image and push
docker tag myapp:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myapp:latest
```

Key considerations before choosing a deployment option

* Operational overhead: EKS (managed Kubernetes) introduces Kubernetes concepts and operational concerns. ECS (especially Fargate) reduces operational burden.
* Ecosystem needs: If you require Kubernetes operators, CRDs, or multi-cloud portability, EKS may be the right choice.
* Cost and scaling model: Fargate simplifies autoscaling and per-task billing; EC2 launch type can be more cost-efficient at scale with proper instance utilization.
* Networking & security: Plan VPC subnets, security groups, task execution roles, and IAM policies up front. Choose ALB vs NLB based on routing, TLS, and latency needs.
* CI/CD strategy: Decide between AWS-native tools ([CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline)/CodeBuild/CodeDeploy) or external CI (e.g., [GitHub Actions](https://learn.kodekloud.com/user/courses/github-actions)) that deploys to ECS.

<Callout icon="lightbulb">
  Before you deploy, ensure you have:

  * an ECR repository for your image,
  * an ECS cluster (Fargate or EC2),
  * appropriate IAM roles for task execution, and
  * networking (VPC/subnets/security groups) configured.

  These components are commonly automated with CloudFormation, Terraform, or the AWS CDK.
</Callout>

Recommended next steps (what we will cover next)

* Creating an ECR repository and pushing images from CI
* Writing ECS task definitions and container configuration
* Creating ECS services on Fargate and EC2, and attaching ALB for routing and health checks
* Setting up CI/CD pipelines (CodePipeline + CodeBuild or GitHub Actions) to automate build → push → deploy
* Best practices for monitoring (CloudWatch), IAM least-privilege, and deployment strategies (rolling, blue/green)

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/a5f47c01-ffdc-4186-8d6b-2b5189000482/lesson/9133cfba-d1a6-4aba-9e84-170c9361652b" />
</CardGroup>


# Overview of ECS

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Deploying-serivce-on-to-ECS/Overview-of-ECS/page

Overview of AWS ECS benefits, features, launch types and integrations, explaining when to use Fargate or EC2 and preparing to create an ECS cluster.

<Callout icon="lightbulb">
  In this lesson we’ll cover why AWS ECS (Elastic Container Service) is a practical choice for running containerized applications and prepare to create our first ECS cluster.
</Callout>

Welcome back.

Our chosen platform for running containers is [AWS ECS](https://learn.kodekloud.com/user/courses/amazon-elastic-container-service-aws-ecs).

Why pick AWS ECS?

* ECS is a fully managed container orchestration service from AWS. Using the Fargate launch type you can run containers without managing servers (serverless compute).
* ECS reduces operational complexity compared with managing a full Kubernetes cluster—no need to manage cluster nodes, Helm charts, cluster-level authentication, or Kubernetes-specific IAM intricacies.
* For many projects, ECS provides a faster path to production while integrating tightly with other AWS services.

AWS Elastic Container Service (ECS) helps you deploy, manage, and scale containerized applications. The main prerequisite is a containerized application; ECS focuses on orchestrating and operating those containers reliably.

<Frame>
  <img alt="The image is a flowchart describing AWS ECS as an orchestration service, showing the process from deployment, management, and scaling to efficient orchestration of containerized applications." />
</Frame>

ECS runs on two primary launch types:

| Launch Type | Description                                                                  | Best for                                                                      |
| ----------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Amazon EC2  | You provision and manage the EC2 instances that host your containers.        | Workloads needing custom AMIs, special drivers, or deeper host-level control. |
| AWS Fargate | Serverless compute for containers—AWS manages the underlying infrastructure. | Teams that want to avoid managing servers and focus on application code.      |

ECS also provides service scheduling to control how tasks are placed and run. It integrates with load balancers to distribute traffic and automates replacement of unhealthy tasks to maintain availability.

<Frame>
  <img alt="The image is a diagram explaining AWS ECS as an orchestration service, highlighting features like flexible scheduling, load balancing, application availability, and resource alignment." />
</Frame>

Key ECS features and practical benefits

* Tight integration with AWS developer tools and services—examples include [CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html), [CodePipeline](https://learn.kodekloud.com/user/courses/aws-codepipeline-ci-cd-pipeline), [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), and [CloudWatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch). These integrations streamline CI/CD, secrets management, and observability.
* Built-in scalability: scale tasks up or down manually or use ECS service autoscaling.
* Task definitions: versioned JSON/registration artifacts that define container images, CPU/memory, environment variables, volumes, networking mode, and runtime settings—making rollbacks and configuration management straightforward.
* Load balancing: native support for Application Load Balancers (ALB) and Network Load Balancers (NLB) via target groups to route traffic to running tasks.
* Fine-grained IAM: use IAM roles for tasks and task execution for secure, least-privilege access to AWS resources.
* Observability: integrate with CloudWatch Logs and Metrics (and other monitoring tools) to capture logs, set alarms, and trace task health.

<Frame>
  <img alt="The image lists key features of AWS ECS, including integration with AWS services, scalability, task definitions, container agent, load balancing support, role-based access control, and logging and monitoring." />
</Frame>

Quick reference: When to choose ECS (and why it matters)

| Situation                        | Choose ECS if...                                                                              |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| You want serverless containers   | Use Fargate to remove node management overhead                                                |
| You prefer tight AWS integration | ECS works well with CodeBuild/CodePipeline, Secrets Manager, and CloudWatch                   |
| You need simple orchestration    | ECS provides scheduling, load balancing, auto-replacement of unhealthy tasks, and autoscaling |
| You need control over the host   | Use EC2 launch type for custom host-level configuration                                       |

Good logging and monitoring are essential in both development and production. Without them, diagnosing deployment or runtime problems is much harder. ECS’s native integrations make it straightforward to collect logs, create metrics, and configure alerts so you can respond quickly to incidents.

If your team doesn’t yet require the complexity of a full Kubernetes platform, ECS—especially with Fargate—offers a pragmatic, production-ready solution with less operational overhead.

Next steps

Now that you understand why we’re using AWS ECS and the features it provides, the next lesson will guide you through creating an ECS cluster and deploying a containerized service to it.

That’s it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/a5f47c01-ffdc-4186-8d6b-2b5189000482/lesson/3a04defb-69fb-4f8e-a739-6f05b79d03b8" />
</CardGroup>
