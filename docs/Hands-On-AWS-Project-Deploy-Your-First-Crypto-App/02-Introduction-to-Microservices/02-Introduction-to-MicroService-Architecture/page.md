# Introduction to MicroService Architecture

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Introduction-to-Microservices/Introduction-to-MicroService-Architecture/page

Introduction to microservice architecture contrasting monolithic design, explaining independent services, database-per-service, communication via APIs, scalability, fault isolation, and operational trade offs

Hello and welcome back.

Earlier we examined a monolithic application in practice. Let’s quickly recap the typical flow:

A user loads an application that presents a login page, browses a product/catalog page to select items, and completes the flow via a payment gateway. From the user’s perspective this is a single, unified experience. Under the hood, a monolithic architecture often implements all these features in one codebase and backs them with a single centralized database.

This tight coupling—where multiple functional areas are built, tested, and deployed as one unit—creates constraints (for example, on scalability and team autonomy) and can slow down development and releases.

What is a microservice application?

To contrast with the monolith, consider the same user-facing experience: login, product pages, and payment. From the end user’s point of view nothing changes. Internally, however, these functions are implemented as independent services.

Now this is a microservice application.

<Frame>
  <img alt="The image illustrates a microservices application, showing a user interface with three functional modules labeled 01, 02, and 03, with icons representing security, shopping, and payment, connected to a user and a server." />
</Frame>

In a microservice-based design:

* Each feature (login, product/catalog, payment) is an independently developed and deployable service.
* Services commonly have separate codebases and can own their own datastore (database-per-service).
* Services interact through well-defined APIs (for example, HTTP/REST, gRPC, or message queues).
* Teams can choose the best technology stack for each service, optimizing for requirements like latency, throughput, and developer productivity.
* Failures or changes in one service tend to be isolated, reducing blast radius compared to a tightly coupled monolith.

> **lightbulb** From the user's perspective the application remains seamless. The main change is architectural: responsibility is split into smaller, autonomous services, enabling independent development, deployment, and scaling.

Key differences at a glance:

| Aspect             | Monolithic Architecture              | Microservice Architecture                       |
| ------------------ | ------------------------------------ | ----------------------------------------------- |
| Deployment unit    | Single deployable artifact           | Multiple independent services                   |
| Data management    | Single, centralized database         | `Database-per-service` (independent datastores) |
| Scaling            | Scale the whole app                  | Scale services individually                     |
| Technology choices | One stack for the whole app          | Polyglot — choose per service                   |
| Fault isolation    | Failures often affect the whole app  | Failures are more contained                     |
| Communication      | In-process calls or direct DB access | Network calls over APIs or messaging            |

Considerations and trade-offs:

* Microservices improve modularity, team autonomy, and scalability.
* They introduce additional operational complexity: service discovery, distributed tracing, monitoring, and data consistency across services.
* Effective API design, observability, and automation (CI/CD, infrastructure as code) are essential for successful microservices adoption.

> **warning** Microservices are not a silver bullet. They add architectural and operational overhead—such as network latency, distributed transactions, and increased DevOps needs—that must be managed carefully.

Next steps

Now that you have a basic understanding of the structural differences between monoliths and microservices, the next lesson will explore the specific benefits and trade-offs in more detail, and introduce common patterns for service communication, data management, and observability.

Links and References

* [Microservices (Martin Fowler)](https://martinfowler.com/articles/microservices.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Designing Data-Intensive Applications (Book)](https://dataintensive.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/99acec5c-de76-478d-aa21-c72de78a1726/lesson/3681162f-6749-4eb2-8622-e4178047f68f)
