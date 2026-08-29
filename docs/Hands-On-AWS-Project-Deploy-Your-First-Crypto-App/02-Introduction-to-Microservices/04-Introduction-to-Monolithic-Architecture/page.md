# Introduction to Monolithic Architecture

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Introduction-to-Microservices/Introduction-to-Monolithic-Architecture/page

Overview of monolithic application architecture, its characteristics, benefits, drawbacks, and why organizations eventually migrate to microservices, illustrated by Airbnb's early Rails monolith.

Hello and welcome to this lesson.

In this module you'll learn what a monolithic application is, why teams initially choose it, and what drives organizations to adopt microservices later. To make these concepts concrete, we’ll walk through a real-world origin story and then examine the technical characteristics, benefits, and trade-offs of monolithic systems.

Brian and Joe attended a conference in San Francisco in 2008. To save money on lodging, they used air mattresses in a living room. They quickly realized this idea could be extended: they rented multiple apartments and offered air mattresses to conference attendees.

<Frame>
  <img alt="The image depicts a &#x22;Monolithic Application&#x22; with illustrations of an air mattress and living room furniture, likely symbolizing components of a single, unified system." />
</Frame>

Their experiment worked well — they made money and expanded the idea. Brian and Joe started AirBed in 2008. Later, Nathan Blecharczyk joined, and the service became AirBed & Breakfast.

<Frame>
  <img alt="The image is a timeline depicting the evolution of a monolithic application from &#x22;AirBed&#x22; in 2017 to &#x22;AirBed and Breakfast&#x22; in 2018, involving individuals named Brian, Joe, and Nathan Blecharczyk." />
</Frame>

That small idea scaled into the company we now know as Airbnb — a global platform operating in over 200 countries with millions of hosts and billions of guest stays.

<Frame>
  <img alt="The image is a timeline illustrating the evolution of a monolithic application from 2017 to today, starting with &#x22;AirBed&#x22; and reaching &#x22;Airbnb,&#x22; highlighting growth and expansion to over 200 countries, 4 million hosts, and 1.5 billion guests." />
</Frame>

How did the engineering team build Airbnb’s initial product? Early on, the Airbnb web application was implemented using Ruby on Rails as a monolithic application. In a monolith, the presentation layer (UI), business logic, and data access layer are developed, tested, and deployed together as a single unit, typically backed by a single database.

<Frame>
  <img alt="The image illustrates a monolithic application architecture, showing a Ruby-on-Rails web app with interconnected components: Presentation View, Business Logic, and Data Access Layer. It includes user and server icons indicating interaction." />
</Frame>

Key characteristics of a monolithic application

* Single codebase and single deployable: UI, business logic, and data access are packaged and released together.
* Single repository workflow: most developers push changes into the same repo and CI/CD pipeline.
* Single database: data models and persistence are centralized.
* Tight coupling: components are often interdependent, which makes isolated changes and independent scaling difficult.

Advantages (why teams choose monoliths early)

* Simplicity: easier to develop, test, and deploy for small teams and early-stage products.
* Low operational overhead: one deployment unit and one database to manage.
* Faster initial iteration: fewer integration boundaries and simpler debugging when the codebase is small.
* Clear local context: developers can reason about flows end-to-end without cross-service coordination.

Drawbacks as the product and teams grow

* Slower team velocity: multiple teams working in a single repository can cause merge conflicts and coordination overhead.
* Coarse scalability: scaling often requires replicating the entire application rather than scaling only the bottleneck component.
* Larger blast radius for failures: small changes may force redeploying the whole application.
* Technology lock-in: migrating to new frameworks, languages, or databases becomes harder.
* Reduced fault isolation: a defect in one area can affect unrelated features.

Table — Monolith trade-offs at a glance

| Aspect                   | Benefit                                      | Trade-off                                                 |
| ------------------------ | -------------------------------------------- | --------------------------------------------------------- |
| Development & deployment | Simpler pipeline, one artifact               | Changes affect the whole system; slower releases at scale |
| Scalability              | Easy to replicate the whole app              | Can be inefficient; cannot scale only the heavy component |
| Operations               | Single database and fewer services to manage | Single point of failure; harder to isolate faults         |
| Team workflow            | Fast feedback for small teams                | Coordination and merge conflicts for many contributors    |

<Callout icon="lightbulb">
  Monolithic architectures work well for early-stage products due to their simplicity. However, as an organization grows, the tight coupling and single-deployable nature often lead teams to consider decomposing the system into microservices to achieve independent scaling, faster releases, and better fault isolation.
</Callout>

Airbnb’s Ruby on Rails monolith served them well during their early growth phase: it enabled rapid iteration and helped them achieve product–market fit. As user demand and organizational complexity increased, they began evolving their architecture—introducing service boundaries, separate data stores, and more independent deployment units—to address the operational and organizational challenges of a large monolith.

That is it for this lesson. We will explore how teams move from a monolithic application to microservices.

Links and references

* [Ruby on Rails](https://rubyonrails.org/)
* [Microservices overview — Martin Fowler](https://martinfowler.com/articles/microservices.html)
* [Kubernetes: What is a microservice?](https://kubernetes.io/blog/2018/06/04/what-are-microservices/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/99acec5c-de76-478d-aa21-c72de78a1726/lesson/f280e2c3-2033-40bc-8e55-b23fc3828220" />
</CardGroup>
