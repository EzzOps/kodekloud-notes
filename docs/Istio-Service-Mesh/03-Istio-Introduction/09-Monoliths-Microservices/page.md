# Monoliths Microservices

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Istio-Introduction/Monoliths-Microservices/page

This article discusses the evolution from monolithic to microservices architecture in software development, highlighting benefits, challenges, and the role of service meshes.

Before diving into Service Mesh and Istio, let's review the evolutionary changes in software design over the past two decades. In the early 2000s, a groundbreaking proposition reshaped how we think about software development.

<Frame>
  ![The image is a blue background slide with the text "MONOLITHS & MICROSERVICES" in white, and a downward arrow icon below.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879341/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/monoliths-microservices-slide.jpg)
</Frame>

At that time, software development was highly process-oriented and slow. In industries such as defense and aviation, projects could take nearly 20 years to complete. A significant lag existed between the emergence of software needs and the actual delivery, resulting in businesses evolving while projects were underway. This disconnect frequently led to projects being abandoned midway, causing substantial financial losses and widespread frustration among business owners and software professionals.

In 2001, a group of seventeen forward-thinking practitioners published the Agile Manifesto. They boldly criticized traditional software development, proposing a new set of priorities:

* Individuals and interactions over processes and tools
* Working software over comprehensive documentation
* Customer collaboration over contract negotiation
* Responding to change over following a plan

They emphasized that while the items on the right side of each statement had value, the items on the left were even more critical.

<Frame>
  ![The image presents the Agile Manifesto, highlighting four key values: "Individuals & Interactions," "Working Software," "Customer Collaboration," and "Responding to Change," prioritized over their counterparts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879342/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/agile-manifesto-four-key-values.jpg)
</Frame>

<Callout icon="lightbulb">
  The Agile Manifesto fundamentally changed collaboration and adaptability in software development, leading teams to experiment with new business models and faster deployment methods.
</Callout>

Building on Agile practices, development teams began to work more closely with customers. This collaboration enabled rapid experimentation and adaptive changes in both business models and software. With large, monolithic applications, a single failure could disrupt the entire system. By decomposing applications into smaller, isolated components, risks were reduced, and deployments became faster and more frequent.

Traditional integrated systems, however, started impeding innovation and agility. A monolithic application typically deploys all functionalities together within a unified codebase, with minimal separation between components. This tight coupling often leads to issues such as a single database acting as a performance bottleneck.

<Frame>
  ![The image illustrates a monolithic application architecture with four interconnected modules (Module 1, Module 2, Module 3, and Module 4) linked to a single database (DB).](../../../../images/kodekloud.com/kk-media/image/upload/v1752879344/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/monolithic-application-architecture-diagram.jpg)
</Frame>

## Bookinfo Application: A Case Study

Consider our Bookinfo application as a real-life example. The application comprises four modules:

<Frame>
  ![The image is a diagram of a monolithic book info app, showing components like Details, Reviews, Product Page, and Ratings, all connected to a database (DB).](../../../../images/kodekloud.com/kk-media/image/upload/v1752879345/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/monolithic-book-info-app-diagram.jpg)
</Frame>

* Details
* Reviews
* Ratings
* Product Page

Although the design is modular, the Bookinfo app remains a monolith. Each service depends on a specific version of another, requiring the whole package to be deployed simultaneously and often involving database scripts. For example, the Product Page aggregates data from the Details, Reviews, and Ratings modules even though these modules are not independently scalable.

<Frame>
  ![The image is a webpage from a book information app featuring "The Comedy of Errors" by William Shakespeare, including a summary, book details, and reviews with star ratings.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879346/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/comedy-of-errors-book-info.jpg)
</Frame>

In this monolithic setup, consider the following scenario:

* A customer visits the Product Page, which gathers data from the Reviews and Details modules.
* The Reviews service then pulls rating data from the Ratings service.

Since all modules use the same programming language (Java) and share a single database, any issue—such as the Ratings module struggling with heavy data load—affects the entire system. Even minor updates require a full redeployment, making scalability and independent upgrades challenging.

Furthermore, if a team wants to introduce a new campaign module using a different programming language, incorporating critical functionalities like authentication and authorization within the monolith becomes cumbersome. Product owners might also wish to test new ideas—such as a revised Reviews module with a red star rating system—on a subset of users before a full-scale rollout.

In larger enterprise applications with hundreds of modules maintained by numerous developers, loosely defined architectural rules can quickly transform the system into what is often referred to as a "big ball of mud"—an unmanageable, complex codebase.

<Frame>
  ![The image illustrates a complex software architecture labeled "A Big Ball of Mud," featuring interconnected components like "Details," "Product Page," "Reviews," "Ratings," and "Campaign," with various functionalities such as authentication, authorization, and logging. It also includes icons representing different programming languages and a database.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879347/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/big-ball-of-mud-architecture-diagram.jpg)
</Frame>

## Transitioning to Microservices

Let's now explore how the Bookinfo monolith can evolve into a microservices architecture. This transformation is complex and requires cultural, technical, and organizational shifts toward cloud-native practices. In a microservices architecture, each module becomes an independent application:

* The Product Page is transformed into a Python application.
* The Book Details module is rewritten in Ruby.
* The Reviews module remains implemented in Java.
* The Ratings module is redesigned using Node.js.
* Additionally, the Reviews service is versioned (e.g., no-star, black star, and red star versions) to facilitate testing and experimentation.

Despite these significant changes, the user experience remains seamless. When accessing the Product Page, users interact with independent services like Details and Reviews to display comprehensive book information.

<Frame>
  ![The image is a diagram of a microservices architecture for a book info app, showing different services like Product Page, Details, Reviews, and Ratings, each implemented with different technologies such as Python, Ruby, Java, and Node.js.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879348/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/microservices-architecture-book-app-diagram.jpg)
</Frame>

This microservices approach offers several benefits:

| Benefit                   | Description                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------- |
| Independent Scaling       | The Ratings module can scale based on customer load.                                                    |
| Faster Releases           | Independent deployments lead to smaller, less risky releases.                                           |
| Technological Flexibility | Teams can choose different programming languages for each service.                                      |
| Enhanced Resilience       | Loose coupling increases the overall system resilience, simplifying monitoring, updates, and rollbacks. |
| Manageability             | Maintaining smaller, autonomous applications reduces the risk of developing a "big ball of mud."        |

However, moving to microservices also introduces challenges. In the monolith, functionalities such as networking, authentication, authorization, data transfer, logging, monitoring, and tracing were centrally managed. With microservices, these cross-cutting concerns are duplicated across independent teams, leading to increased complexity in managing certificates, monitoring agents, traffic rules, timeouts, and service discovery.

<Frame>
  ![The image illustrates the concept of "Fat Microservices," showing four microservices (Product Page, Details, Reviews, Ratings) each with duplicated functionalities like authentication, authorization, and monitoring, using different programming languages.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879350/notes-assets/images/Istio-Service-Mesh-Monoliths-Microservices/fat-microservices-architecture-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  While microservices offer flexibility and scalability, they demand a robust observability strategy to troubleshoot issues across distributed components. Teams must work collaboratively to standardize cross-cutting functionalities.
</Callout>

In larger systems, these operational challenges can be a significant bottleneck without modern solutions such as DevOps, where development and operations collaborate closely.

In the upcoming lesson, we will explore how service meshes can help address these challenges by managing cross-cutting concerns and simplifying inter-service communication.

For more insights on modern architectures and service management, check out our [Kubernetes Documentation](https://kubernetes.io/docs/) and [Docker Hub](https://hub.docker.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-service-mesh/module/dc0a9efc-09ce-4310-86e9-1c7aaab6a7d8/lesson/6ff78455-0835-4735-b9d2-0127361749ea" />
</CardGroup>
