# Real world Applications of VMs and Containers

Source: https://notes.kodekloud.com/docs/Virtualization-and-Containers/Real-world-Applications-of-VMs-and-Containers/Real-world-Applications-of-VMs-and-Containers/page

Explains using microservices, containers, and virtual machines to build scalable, resilient online shopping platforms with Docker, Kubernetes, and orchestration best practices

Let's wrap up by showing how the concepts we've covered—microservices, virtualization, and containers—come together in a real-world example: an online shopping site. This practical walkthrough explains how tools like Docker and Kubernetes are used to build systems that are fast, reliable, and cost-effective.

Goals for the example site (xFusionCorp.com)

* Fast, reliable performance under heavy load (e.g., thousands of concurrent shoppers).
* Zero or minimal downtime during updates.
* Rapid fixes and independent updates to parts of the system.

<Frame>
  <img alt="The image shows a person wearing a KodeKloud t-shirt in front of an online shopping interface with icons for various products and text highlighting fast, reliable performance and zero downtime." />
</Frame>

Overview: the legacy approach and its drawbacks
Historically, web applications were often deployed as a single monolithic application or as separate apps each tied to its own physical server. That model introduces several problems:

* High hardware and maintenance costs (every new feature could require new servers).
* Slow, manual scaling during traffic spikes.
* Risky deployments where one change can break the whole site.

<Frame>
  <img alt="The image shows a person in a KodeKloud t-shirt standing next to a graphic highlighting issues like high cost, slow scaling, and risky deployment related to app servers." />
</Frame>

Modern architecture: microservices, containers, and VMs
Modern teams replace the monolith with a combination of microservices, containers, and virtual machines (VMs). Below we walk through each layer—what it is, why it helps, and how it fits into the deployment stack.

Microservices
Split the application into small, independently deployable services: product search, cart, checkout, notifications, payment, wishlist, etc. Each service owns its own code, data model, and lifecycle. This isolation reduces blast radius and allows teams to develop, test, and deploy independently.

<Frame>
  <img alt="The image shows a person standing next to a diagram of a microservices architecture with four components: Product Search, Cart, Checkout, and Notification. Buttons labeled &#x22;Built&#x22; and &#x22;Updated&#x22; are at the top." />
</Frame>

Example microservices at xFusionCorp:

* Payment — handles payments and transactions.
* Product Search — indexes and responds to search queries.
* Wishlist — manages customers’ saved items.
  Each service can be updated or restarted independently; a failure in Wishlist does not take down Payment or Search.

Containerization
Package each microservice with its runtime, libraries, and environment into a container image for reproducible behavior across environments (local dev, CI, staging, production). Containers are fast to start and portable across hosts.

<Frame>
  <img alt="The image shows a person wearing a KodeKloud t-shirt standing next to a diagram of containers labeled &#x22;Cart,&#x22; &#x22;Update,&#x22; &#x22;Product Search,&#x22; and &#x22;Checkout,&#x22; with a label &#x22;Fast to Launch.&#x22;" />
</Frame>

Common commands

* Build a Docker image:

```bash theme={null}
docker build -t xfusion/product-search:1.0 .
```

* Run a container locally:

```bash theme={null}
docker run --rm -p 8080:80 xfusion/product-search:1.0
```

Virtual Machines
Containers share the host OS kernel, which is efficient. For stronger isolation, different kernel requirements, or additional security boundaries, run containers inside VMs. A physical server hosts multiple VMs; each VM can host many containers. VMs provide isolation and flexibility while containers provide consistency and speed.

<Callout icon="lightbulb">
  Use containers for portability and rapid scaling. Use VMs when you need stronger isolation, different OS environments, or additional security boundaries.
</Callout>

Scaling and updates (how orchestration helps)
During traffic spikes—say, a holiday sale—components like Product Search can experience a surge. Orchestration platforms (Kubernetes, ECS, etc.) automate scaling and updates:

* Reuse the container image for the search service.
* The orchestrator schedules many container replicas across the VM fleet.
* Load balancers distribute traffic to healthy replicas.
* If demand grows, add VMs (or rely on cloud autoscaling) and schedule more containers on them.

If a bug is discovered, build a fixed container image and perform a rolling update. The orchestrator replaces old replicas with new ones with minimal or no downtime. A failing microservice only affects its own containers; the rest of the system stays available.

<Callout icon="warning">
  Containers are lightweight but share the host kernel. For workloads that handle sensitive data or require different OS kernels, run them inside VMs to get stronger isolation.
</Callout>

How the layers map to responsibilities

| Layer                   | Primary responsibility                                          | Example / Command                        |
| ----------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| Microservice            | Encapsulates a single business capability (search, checkout)    | N/A                                      |
| Container               | Packages service + runtime + libs for consistent deployment     | `docker build -t xfusion/checkout:1.2 .` |
| Virtual machine         | Provides isolation, different OS, and a place to run containers | `cloud provider VM`                      |
| Server (physical/cloud) | Hardware or cloud instance powering the VMs                     | `AWS EC2`, `GCE`, `Azure VM`             |

Deployment and orchestration example

* Container registry stores images (e.g., Docker Hub, ECR).
* Kubernetes (or another orchestrator) pulls images and schedules pods/containers onto nodes (VMs).
* Horizontal Pod Autoscaler (HPA) or cloud autoscaler scales replicas and VMs based on load.
* Services and Ingress manage routing and load balancing.

Example Kubernetes rolling update:

```bash theme={null}
kubectl set image deployment/product-search product-search=xfusion/product-search:1.1
```

Putting everything together — conceptual order to remember

1. Microservice — business logic (e.g., search, checkout).
2. Container — packages the microservice and its dependencies.
3. Virtual machine — runs multiple containers with stronger isolation.
4. Server — the physical or cloud machine that hosts the VMs.

Small services run in containers; containers run on VMs; VMs run on cloud infrastructure. Containers enable speed and scale; VMs add isolation and flexibility. This combination supports everything from student projects to global platforms like Amazon.

Review and takeaway
Virtualization and containers let you build and operate massive, fast, and reliable services. Microservices reduce blast radius and enable team autonomy. Containers ensure consistent, fast deployments. VMs provide isolation when required. Orchestration tools (Kubernetes, ECS, etc.) handle scaling, updates, and resilience—making it possible to scale to thousands of users affordably and reliably.

<Frame>
  <img alt="The image is a presentation slide focused on &#x22;Virtualization & Containers,&#x22; &#x22;Microservice,&#x22; and &#x22;With Docker & Virtualization,&#x22; featuring a speaker from KodeKloud." />
</Frame>

Links and further reading

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Documentation](https://docs.docker.com/)
* [Introduction to Virtualization](https://en.wikipedia.org/wiki/Virtual_machine)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/virtualization-and-containers/module/b3d0490b-ab50-46bb-837a-e82707aeb4d4/lesson/905433f6-5d36-450a-9c67-3500d7c5de46" />
</CardGroup>
