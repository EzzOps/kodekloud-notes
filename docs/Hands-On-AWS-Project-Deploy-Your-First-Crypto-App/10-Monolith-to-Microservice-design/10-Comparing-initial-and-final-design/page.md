# Comparing initial and final design

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Comparing-initial-and-final-design/page

Transforming a monolithic crypto app into AWS microservices, comparing initial and final architectures, CI/CD, deployment strategies, and operational best practices

Welcome back. In this lesson we'll review how we started and how the final architecture evolved, highlighting the practical steps, trade-offs, and operational improvements made while transforming a monolithic crypto application into a microservices-based system on AWS.

## Project starting point — what you were given

You joined as a DevOps engineer with access to the application's codebase only. From that starting point the first working setup was deliberately simple and meant to validate the application end-to-end:

* Access to the AWS CodeCommit repository for source control.
* An AWS Cloud9 development environment for quick, browser-based development.
* Containerization of the application (Docker) and local validation of the container image.

These steps provided a minimal reproducible deployment and a foundation for iterating toward a more robust, scalable architecture.

## Key technical learnings and trade-offs

During the project you made several architecture and operational decisions. Each choice had trade-offs related to reliability, scalability, and team productivity:

* Docker image tagging strategies — immutable tags (e.g., content-hash) vs. mutable tags (e.g., `latest`) and how mutable tags can cause unpredictable deployments.
* Amazon ECS as the chosen container orchestration platform to run Docker containers in a managed service.
* CI/CD design using AWS services (CodeCommit, CodeBuild, CodePipeline) for automated builds and deployments.
* Safe rollback and deployment reliability strategies such as blue/green or canary deployments and use of Application Load Balancer (ALB) for traffic shifting.

> **lightbulb** Prefer immutable Docker image tags (for example, the image digest or a unique build number) to ensure reproducible, auditable deployments and simpler rollback procedures.

Some choices that were appropriate early in development needed revisiting as requirements, traffic patterns, and team structure changed. The architecture therefore evolved from a monolithic application into a microservices-oriented design.

## Architectural evolution: Monolith → Microservices

You refactored by separating concerns into distinct services. The product functionality and the login/authentication functionality were decoupled into separate services and repositories. Each service has its own build and deployment pipeline, enabling independent releases and reducing cross-team coupling.

Benefits of this refactor include:

* Independent deployability for each team.
* Reduced blast radius for failures.
* Finer-grained scaling per service to optimize cost and performance.
* Clearer ownership and faster CI/CD cycles.

All of your teams can now develop independently, and — as the diagram shows — application scalability and

<Frame>
  <img alt="The image is a flowchart illustrating the transition from monolithic to microservices architecture using AWS Cloud services such as AWS CodePipeline, Amazon ECS, and Application Load Balancer. It shows the separation of &#x22;Product&#x22; and &#x22;Login&#x22; applications, each with their own build and deployment processes." />
</Frame>

service reliability are now much easier to guarantee.

## Side-by-side: Initial vs Final architecture

| Aspect                | Initial (Monolith)                | Final (Microservices)                                              |
| --------------------- | --------------------------------- | ------------------------------------------------------------------ |
| Source control        | Single repository                 | Multiple repositories (per service)                                |
| CI/CD                 | Single pipeline for entire app    | Service-specific pipelines (CodeCommit → CodeBuild → CodePipeline) |
| Runtime               | Single container instance/service | Multiple ECS services, one per microservice                        |
| Scaling model         | Scale whole application           | Independent scaling per service                                    |
| Deployment strategies | Coarse-grained, riskier rollbacks | Blue/green or canary, safer rollbacks                              |
| Team ownership        | High coupling between teams       | Clear boundaries, independent teams                                |

## Recommended next steps and operational best practices

* Adopt immutable image tagging and store images in Amazon ECR with proper lifecycle policies.
* Implement deployment strategies that minimize downtime: blue/green or canary deployments with accurate health checks on the ALB.
* Automate observability: centralized logging (CloudWatch Logs), metrics (CloudWatch / Prometheus), and distributed tracing.
* Harden CI/CD pipelines with automated tests, security scans (container image scanning), and IAM least-privilege for build/deploy roles.
* Document service contracts and API versioning to reduce integration friction between teams.

## Links and references

* [AWS CodeCommit](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
* [AWS Cloud9](https://docs.aws.amazon.com/cloud9/latest/user-guide/welcome.html)
* [Amazon ECS](https://docs.aws.amazon.com/ecs/latest/developerguide/what-is-ecs.html)
* [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)
* [Application Load Balancer (ALB)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)

Congratulations — you’ve moved from understanding requirements and running a monolithic app to refactoring for microservices and applying deployment and operational best practices.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/f1739ca6-d0b6-41bc-af42-5c9f416ea819)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/7071ec0e-46f8-49c0-9178-aab5f9ea1ce9)
