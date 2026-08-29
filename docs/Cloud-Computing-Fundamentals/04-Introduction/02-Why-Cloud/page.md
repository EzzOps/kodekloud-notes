# Why Cloud

Source: https://notes.kodekloud.com/docs/Cloud-Computing-Fundamentals/Introduction/Why-Cloud/page

Overview of cloud computing fundamentals, NIST definition, five essential characteristics, service and deployment models, benefits and trade offs illustrated with a viral app scaling example.

If you took the [Database Fundamentals](https://learn.kodekloud.com/user/courses/database-fundamentals) course, you'll remember MeowTube — Kody's homegrown video site for cats.

Back then, MeowTube ran on a single server in a spare room. When it went viral, the team scrambled to scale: buying and wiring extra servers just to keep up with demand. Scaling back after the spike wasn’t worth the hassle, so the extra machines sat idle, wasting space and money. Working away from the office was a headache.

<Frame>
  <img alt="An illustration of four dark server towers with purple highlights, each marked by numbered gradient circles, alongside four small neon line charts. A presenter wearing a KodeKloud t-shirt stands to the right of the diagrams." />
</Frame>

Every maintenance task — updating MeowTube's website, fixing backend bugs, or patching servers — depended on clunky VPNs and slow remote access.

<Frame>
  <img alt="A split illustration showing a worried cartoon developer at a laptop beside a man wearing a KodeKloud t-shirt, with a large dashboard-style UI above them. The UI shows a www.miaowtube.com search bar, a table of video entries (Title, Username, Email, Link, Upload_Date) and three gradient buttons labeled &#x22;Updating,&#x22; &#x22;Fixing Bugs,&#x22; and &#x22;Patching Servers.&#x22;" />
</Frame>

Sometimes the systems wouldn’t respond at all. Then they found the cloud.

By the end of this lesson you'll be able to:

* Explain how cloud computing differs from traditional on-premises infrastructure.
* Evaluate the core benefits and trade-offs of cloud computing.
* Identify everyday examples of cloud computing in consumer and business contexts.

<Callout icon="lightbulb">
  This lesson covers cloud fundamentals: what cloud computing is, its essential characteristics, the basic service and deployment models, and common real-world examples.
</Callout>

What is cloud computing?

At a basic level: instead of buying and managing your own computers, you rent computing resources from a provider. A formal definition from NIST (the US National Institute of Standards and Technology) explains the model more precisely.

<Frame>
  <img alt="A slide displaying the US NIST definition of cloud computing in large white text on a purple-to-black background. A presenter stands to the right wearing a black &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

NIST defines cloud computing as a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources — for example, networks, servers, storage, applications, and services — that can be rapidly provisioned and released with minimal management effort or service provider interaction.

That definition is compact but important: cloud computing combines several essential characteristics that change how teams build and operate systems. NIST groups these into five essential characteristics, three service models, and four deployment models. Below we focus on the five essential characteristics and their practical impact for Kody and her team.

5 essential characteristics

1. On-demand self-service\
   Kody can provision MeowTube’s resources — a server, a database, or a container — instantly without human intervention from the provider. Provisioning is fast and self-directed.

2. Broad network access\
   Cloud services are available over the internet (not just across internal networks), so Kody and her team can access resources from anywhere and on many device types.

<Frame>
  <img alt="A presentation slide reading &#x22;5 Essential Characteristics&#x22; and &#x22;Broad Network Access&#x22; with a purple globe graphic and a cute cartoon animal on the left. A presenter stands on the right wearing a black t-shirt with a &#x22;KodeKloud&#x22; logo." />
</Frame>

3. Resource pooling\
   Cloud providers pool hardware across many customers. Virtualization and isolation mechanisms ensure each customer’s compute and storage remain logically separated while benefiting from shared, enterprise-grade infrastructure.

<Frame>
  <img alt="A presentation slide titled &#x22;5 Essential Characteristics&#x22; highlighting &#x22;Resource Pooling&#x22; with a cloud/server diagram connecting VMs to laptops and a small cartoon cat on the left. A presenter wearing a KodeKloud t-shirt gestures on the right." />
</Frame>

This lets teams use powerful infrastructure without capital investment or maintenance overhead.

4. Rapid elasticity\
   Cloud platforms support quick horizontal scaling — adding more machines to share load — and fast vertical scaling when needed. When a kitten video goes viral, additional servers can spin up in seconds and be torn down when traffic drops.

<Frame>
  <img alt="A presenter wearing a KodeKloud t-shirt stands to the right of a slide titled &#x22;5 Essential Characteristics&#x22; that highlights &#x22;Rapid Elasticity&#x22; with cloud and server rack graphics. The slide also features a cute cartoon cat character and purple-themed visuals." />
</Frame>

5. Measured service\
   Cloud usage is metered: CPU cycles, storage GBs, and network bandwidth are tracked and billed. Usage reports, metrics, and logs make consumption visible and actionable.

<Frame>
  <img alt="A presentation slide titled &#x22;5 Essential Characteristics&#x22; showing &#x22;Measured Service&#x22; with progress bars for CPU Cycle, GB of Storage, and Bandwidth. A presenter wearing a KodeKloud t‑shirt stands on the right and a small cartoon cat is at the bottom left." />
</Frame>

Service models and deployment models — quick preview

Service models (what you rent) and deployment models (where it runs) are central to cloud strategy. The following table summarizes the core options:

|         Category | Common models                      | What it means                                                                                         |
| ---------------: | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
|    Service model | IaaS (Infrastructure as a Service) | Raw compute, storage, and networking you configure and manage.                                        |
|                  | PaaS (Platform as a Service)       | Managed runtime and services for building and running applications (less infrastructure to manage).   |
|                  | SaaS (Software as a Service)       | Fully managed applications delivered over the internet (e.g., email, CRM).                            |
| Deployment model | Public cloud                       | Shared infrastructure managed by a provider (e.g., AWS, Azure, GCP).                                  |
|                  | Private cloud                      | Dedicated infrastructure for a single organization, often on-premises or in a provider’s data center. |
|                  | Hybrid cloud                       | A mix of public and private environments for flexibility and compliance.                              |
|                  | Community cloud                    | Shared infrastructure for organizations with common needs (e.g., regulatory constraints).             |

As you move from IaaS → PaaS → SaaS, the provider assumes more responsibility for maintenance and operations.

Pros and cons of the five characteristics (practical view)

On-demand self-service

* Pros: Rapid provisioning speeds development, testing, and recovery. No long hardware procurement cycles.
* Cons: Without governance, it's easy to lose track of resources and incur unexpected costs.

Broad network access

* Pros: Enables remote work, multi-device access, and distributed teams.
* Cons: Reliance on network connectivity — outages or poor links affect access.

Resource pooling

* Pros: Access to enterprise-grade hardware and managed services without capital expense.
* Cons: Shared infrastructure introduces multi-tenant risk; misconfigurations can create exposure.

Rapid elasticity

* Pros: Automatically match capacity to demand; horizontal scaling increases fault tolerance.
* Cons: Applications not designed for scaling can be costly to autoscale or fail to scale properly.

<Frame>
  <img alt="A presenter wearing a KodeKloud T‑shirt stands to the right of a graphic showing four stacked server icons with an arrow and the label &#x22;Horizontal Scaling.&#x22; The image illustrates the concept of scaling out by adding more server instances." />
</Frame>

Measured service

* Pros: Detailed metrics and billing help optimize costs and improve security/operations.
* Cons: You must actively monitor usage and configure alerts or cost controls to avoid surprises.

<Callout icon="warning">
  Cloud is powerful, but poor governance or architecture can lead to cost overruns, security gaps, or availability issues. Plan resource lifecycle and monitoring from day one.
</Callout>

Everyday examples of cloud computing

Cloud services power many apps you use daily:

* Travel booking sites (e.g., Booking.com) fetch reservations from cloud backends rather than local device storage.
* Music streaming (e.g., Spotify) streams tracks and metadata from cloud servers on demand rather than storing everything locally.

<Frame>
  <img alt="An illustration on the left shows a woman tapping a large smartphone with the Spotify logo, linked to server boxes labeled &#x22;Artist.&#x22; On the right a presenter in a KodeKloud t-shirt stands and speaks against a black background." />
</Frame>

* Food delivery apps coordinate menus, payments, and courier locations in real time through cloud systems.
* Collaboration tools (e.g., Google Docs) enable simultaneous editing because the document state lives in the cloud.
* Many business databases and managed services now run in the cloud — see the [Database Fundamentals](https://learn.kodekloud.com/user/courses/database-fundamentals) course for examples.

Quick quiz

Which of the following statements is true?

A. Cloud computing lets you rent IT resources from providers instead of buying servers.\
B. The biggest benefit of cloud is that it's always cheaper than on-premises.\
C. Everyday apps like Spotify and Booking.com mostly run on your phone, not in the cloud.

Pause now. Welcome back.

Correct answer: A. Cloud resources are delivered from providers' data centers, so you don't own the hardware.\
B is a myth — total cost depends on design, usage patterns, and management. C is misleading — user devices provide the interface, but heavy compute and storage are typically in the cloud.

Recap

Before cloud adoption, organizations depended on slow, expensive on-premises infrastructure. NIST’s definition and the five essential characteristics capture why cloud changed the game:

* On-demand self-service
* Broad network access
* Resource pooling
* Rapid elasticity
* Measured service

Cloud computing offers flexible, scalable, and potentially cost-effective access to IT resources with reduced setup and maintenance. To realize those benefits, teams need strong architecture, governance, and monitoring to control costs and maintain security and availability.

Next steps

We'll dive next into the three service models (IaaS, PaaS, SaaS) to clarify responsibilities and trade-offs so you can choose the right model for MeowTube or your own projects.

Links and references

* NIST Cloud Definition: [https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf)
* [Database Fundamentals — KodeKloud course](https://learn.kodekloud.com/user/courses/database-fundamentals)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cloud-computing-fundamentals/module/011c3039-0ef4-42f9-8ac1-0633bb3bf667/lesson/0c524470-858d-484d-9248-60dc2e27b789" />
</CardGroup>
