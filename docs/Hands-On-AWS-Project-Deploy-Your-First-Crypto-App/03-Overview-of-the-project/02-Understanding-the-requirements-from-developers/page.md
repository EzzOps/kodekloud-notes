# Understanding the requirements from developers

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Overview-of-the-project/Understanding-the-requirements-from-developers/page

Designing and deploying a scalable, automated AWS-based CI/CD architecture for a crypto coin web app covering hosting, databases, networking, observability, security, and cost optimization.

Welcome back.

In this lesson we’ll design and deploy a cloud-hosted application: a crypto coin website running on AWS. The primary challenge is scalability: the solution must enable rapid development, repeatable deployments, and the ability to grow seamlessly to handle variable traffic patterns.

As the DevOps engineer, you’ll create a fast, automated development and deployment workflow that supports both front-end and back-end teams while ensuring production reliability and cost control.

<Frame>
  <img alt="The image shows a team structure for setting up a Crypto Coin website on AWS, highlighting frontend and backend developers, with a focus on addressing deployment challenges for scalability." />
</Frame>

Can we achieve this? Absolutely.

To build a solution that favors speed, automation, and scalability, we’ll map concrete AWS services and architectural patterns to developer needs. Below is a concise inventory of the primary AWS building blocks we’ll consider.

| Category                | AWS Services / Patterns                                                                                         | Recommended Uses                                                                                                                                                                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compute & Orchestration | [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/), Amazon ECS / Fargate, Amazon EKS, AWS Lambda | Managed platforms for running web apps and microservices: Beanstalk for simple deployments, ECS/Fargate for containerized services without managing servers, EKS for Kubernetes-based deployments, Lambda for serverless functions and event-driven workloads. |
| Databases & Caching     | Amazon RDS / Aurora, Amazon DynamoDB, Amazon ElastiCache                                                        | RDS/Aurora for relational data, DynamoDB for high-scale NoSQL, ElastiCache for in-memory caching (Redis/Memcached).                                                                                                                                            |
| Storage & CDN           | Amazon S3, Amazon CloudFront                                                                                    | S3 for static assets and backups; CloudFront for low-latency global content delivery and caching.                                                                                                                                                              |
| Networking & Scaling    | Application Load Balancer (ALB), Network Load Balancer (NLB), Auto Scaling groups                               | ALB for HTTP(s) routing with path/host rules, NLB for high-performance TCP, Auto Scaling for dynamic capacity based on traffic.                                                                                                                                |
| CI/CD & Automation      | AWS CodePipeline, CodeBuild, CodeDeploy — or third-party CI/CD (GitHub Actions, GitLab CI, CircleCI)            | Automate builds, tests, deployments, implement blue/green or canary releases and automated rollback on failures.                                                                                                                                               |

Why choose AWS? It provides managed services and automation that speed development, offer built-in scalability (Auto Scaling, serverless), and optimize delivery through managed storage and global CDNs.

<Frame>
  <img alt="The image illustrates four benefits with icons: Speed, Scalability, Managed Databases, and Optimized Content Delivery." />
</Frame>

Developers expect more than just hosting. Key functional requirements to address:

* Rapid, iterative testing via staging environments, feature branches, and ephemeral preview environments for pull requests.
* A reliable, automated CI/CD pipeline that supports frequent releases, health checks, rollbacks, and deployment strategies (blue/green, canary).
* Predictable autoscaling and cost-awareness to handle traffic spikes without overspending.
* Clear separation of concerns between the static front end and the API back end (single-page app served from S3/CloudFront vs. containerized or serverless API).

> **lightbulb** Design for environments: implement at least `development`, `staging`, and `production` pipelines. Use ephemeral preview environments for PR validation and automated integration tests to catch regressions before merge.

<Frame>
  <img alt="The image lists two developer requirements: setting up CI/CD for application deployment, and choosing scalability services for deployment." />
</Frame>

Operational considerations (non-functional requirements) you should plan for:

* Observability: centralized logging, metrics, distributed tracing, and alerts.
* Security: least-privilege IAM roles, secrets management (AWS Secrets Manager or Parameter Store), TLS everywhere, and secure CI/CD credentials.
* Cost optimization: right-size instances, use on-demand vs. spot where appropriate, and set up budgets and alerts.
* Resilience: multi-AZ deployments, database backups/replication, and health-check-driven automated recovery.

> **warning** Beware of runaway costs: aggressive autoscaling without proper scaling policies or missing resource cleanup for ephemeral environments can lead to unexpected charges. Implement budgets, alerts, and lifecycle policies.

Next steps

1. Inspect the application repository to determine:
   * Is the frontend a static SPA or server-rendered?
   * Is the backend monolithic or split into microservices?
   * Database schema and expected traffic patterns.
2. Map these findings to deployment patterns:
   * Static SPA → S3 + CloudFront + invalidation strategy.
   * Containerized API → ECS/Fargate or EKS with ALB and Auto Scaling.
   * Serverless endpoints → API Gateway + Lambda for low-management overhead.
3. Define the CI/CD flow:
   * Build → test → deploy to ephemeral preview → promote to staging → smoke tests → promote to production.
   * Integrate automated rollback and health-check gating.

Links and references

* AWS Documentation: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)
* CI/CD on AWS: [https://aws.amazon.com/devops/continuous-delivery/](https://aws.amazon.com/devops/continuous-delivery/)
* Kubernetes Basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Amazon S3 and CloudFront: [https://aws.amazon.com/cloudfront/](https://aws.amazon.com/cloudfront/)

We’ll now locate and inspect the application codebase to make architecture decisions (monolith vs. microservices, static front end vs. API backend, database requirements) and map those choices to concrete AWS services and deployment flows.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/9f95967c-83f1-492d-ba1e-b56e9fcad0d6/lesson/40d573a4-f392-4ae7-8ea9-a122f6ed02c1)
