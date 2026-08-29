# Need of Independently Deployable Components

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Monolith-to-Microservice-design/Need-of-Independently-Deployable-Components/page

Explains why and how to migrate a monolithic app to independently deployable services, covering CI/CD changes, scaling benefits, communication patterns, and migration steps.

Welcome to this lesson.

In this lesson we’ll examine why migrating a monolithic application to an architecture of independently deployable components (microservices) matters. We’ll review the current CI/CD and deployment flow, identify the scaling challenges of a monolith, and outline the benefits and patterns for splitting the application into services that can be developed and deployed independently.

## Current CI/CD and Deployment Flow

Developers commit changes to a repository. When changes are pushed, AWS CodePipeline pulls from CodeCommit, runs the build stage, and deploys the application to Amazon ECS. An Application Load Balancer (ALB) fronts the ECS service, and end users access the app through the ALB. This flow works well initially and can scale, but it introduces a key limitation as the application grows.

<Frame>
  <img alt="The image is a flowchart depicting the current architecture of an application using AWS services. It includes components such as AWS CodeCommit, AWS CodePipeline, Amazon ECS, and an Application Load Balancer." />
</Frame>

## The Scaling Problem with Monoliths

From the end-user perspective, the flow is simple: log in, visit the product page, choose a product, pay, and complete the transaction. For many early web apps this was implemented as a single monolithic application: built, tested, and deployed together.

However, this creates an operational problem. Suppose a developer is changing only the product page. Because the product page is part of the same monolith as the login flow, every change requires rebuilding and redeploying the entire application. You cannot deploy just the product page in isolation. Deploying the whole application for each small change is not a scalable operational pattern.

Key drawbacks of a monolithic design:

* Single point of failure: one CI/CD pipeline and one deployment impacts every feature.
* Longer build and deploy times: any change triggers a full build of the codebase.
* Difficult rollbacks: a small faulty change forces rolling back the entire app.
* Reduced team agility: teams must coordinate releases across the whole application.

<Frame>
  <img alt="The image is a flowchart depicting the breakdown of a single application process, showing steps from accessing a webpage to adding items to a cart and making a payment. It highlights potential issues like complexity, single points of failure, longer build times, difficult rollbacks, and lack of agility." />
</Frame>

## The Solution: Independently Deployable Components

Splitting the application into isolated, independently deployable services resolves many of the constraints above. Each service is a smaller codebase with its own lifecycle, pipeline, and deployment target.

Benefits:

* Accelerated deployment: smaller repositories and images mean faster builds and shorter deploy windows.
* Improved fault isolation: failures are contained to the affected service instead of the whole app.
* Enhanced scalability: scale services independently according to demand (e.g., increase Product replicas without touching Login).
* Increased team productivity: teams can iterate and release independently.
* Cost efficiency: while there may be infrastructure overhead, faster time-to-market and team autonomy often outweigh those costs.

<Frame>
  <img alt="The image lists five benefits of independently deployable components: accelerated deployment, improved fault isolation, enhanced scalability, increased team productivity, and cost efficiency, each with an icon and a numbered label." />
</Frame>

<Callout icon="lightbulb">
  Independently deployable components are a tradeoff: you gain deployability, resilience, and team autonomy at the cost of additional infrastructure and operational complexity (service discovery, inter-service communication, and monitoring). Plan for those operational needs when designing your migration.
</Callout>

## Example Target Architecture

Rather than a single repository and pipeline, teams own specific services and repositories. For example:

* Product team owns the Product repository and pipeline; their changes build and deploy only the Product service (containerized and running on ECS).
* Login team owns the Login repository and pipeline; their changes build and deploy only the Login service.

Each service has its own CodeCommit repo and CodePipeline (or other CI/CD), which independently builds and deploys to ECS. The ALB (or internal routing) directs traffic to the appropriate service. This decoupling enables services to be developed, deployed, and scaled independently.

<Frame>
  <img alt="The image depicts a workflow for transitioning from a monolithic architecture to microservices using AWS. It includes components like code repositories, AWS CodePipeline, Amazon ECS, and an application load balancer." />
</Frame>

## How Services Communicate

Design communication patterns and contracts carefully to avoid tight coupling and brittle integrations. Common approaches include:

* ALB routing: route external user requests to the appropriate front-facing service.
* Internal load balancers or service discovery: enable internal HTTP/gRPC calls between services.
* APIs and well-defined contracts: use versioned APIs and backward-compatible changes to avoid breaking consumers.
* Messaging/event buses: use asynchronous messaging (e.g., SQS, SNS, or Kafka) for decoupled, resilient interactions.

## Quick Comparison

| Concern                | Monolithic Application                       | Independently Deployable Services                               |
| ---------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| Build & Deploy         | Single pipeline builds everything            | Per-service pipelines, smaller builds                           |
| Fault Isolation        | Entire app affected by one change            | Failures isolated to service                                    |
| Scalability            | Scale whole app or heavy manual partitioning | Scale each service independently                                |
| Team Autonomy          | Tight coordination required                  | Teams can release independently                                 |
| Operational Complexity | Lower initial complexity                     | Higher operational requirements (service discovery, monitoring) |

## Practical Next Steps

To begin the migration:

1. Identify a bounded context to extract (e.g., Login).
2. Create a new repository for the service and set up a dedicated CI/CD pipeline (CodeCommit + CodePipeline or equivalent).
3. Containerize the service and create an ECS task definition and service for it.
4. Update ALB routing rules or internal service discovery so the new Login service receives the correct traffic.
5. Implement API contracts, integration tests, and monitoring/alerts for the service.
6. Repeat iteratively for other components, validating at each step.

In the next lesson we will start by extracting the Login application into its own repository, pipeline, and ECS service, then integrate it back into the overall solution.

That is it for this lesson. Speak with you in the next lesson.

## Links and References

* [Amazon ECS documentation](https://docs.aws.amazon.com/ecs/)
* [AWS CodePipeline documentation](https://docs.aws.amazon.com/codepipeline/)
* [Application Load Balancer overview](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]/introduction.html)
* [Microservices architecture patterns](https://martinfowler.com/articles/microservices.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/d14608f9-c900-4ec7-9bdd-ed8e215da540/lesson/6b01a929-389e-4efb-bc03-2167fab9948f" />
</CardGroup>
