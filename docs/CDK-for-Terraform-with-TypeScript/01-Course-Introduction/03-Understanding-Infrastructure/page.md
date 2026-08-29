# Understanding Infrastructure

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Course-Introduction/Understanding-Infrastructure/page

Explains software and cloud infrastructure using an office building analogy, detailing compute, storage, networking, security, observability, resilience, and why distinguishing infrastructure from applications matters.

In this lesson we return to the fundamentals and clarify what we mean by "infrastructure" in modern software systems and cloud environments.

A simple, practical way to reason about infrastructure is to compare it to an office building:

* The building itself—the walls, rooms, power supply, heating/cooling, and network cabling—represents the infrastructure.
* The people who work inside the building, who perform tasks, collaborate, and deliver value, represent the applications (and teams) that run on that infrastructure.

In this analogy, infrastructure is everything that makes the work possible: the physical structure and the systems that provide power, connectivity, and a safe environment. The workers are the ones who do the business work.

Apply the analogy to software: the application contains business logic, UI/UX, and domain-specific functionality—this is like the workers. Infrastructure provides the foundation and environment the application needs to run: compute, storage, networking, security, and observability.

<Frame>
  <img alt="A slide titled &#x22;Infrastructure's Role&#x22; showing a central office-building graphic with worker icons, flanked by an &#x22;Application&#x22; panel (Business Logic, UI/UX) on the left and an &#x22;Infrastructure&#x22; panel (Computing Power, Storage, Networking, Security) on the right. The diagram illustrates how application components rely on underlying infrastructure services." />
</Frame>

## What infrastructure provides

Infrastructure delivers the runtime, capacity, connectivity, and protections that enable applications to operate reliably and securely. Common infrastructure responsibilities include:

* Compute resources (virtual machines, containers, serverless functions)
* Storage (object storage, block storage, file systems)
* Networking (VPCs, subnets, routing, DNS, load balancers)
* Identity and access management (IAM, service principals)
* Security (network policies, encryption, firewalls)
* Observability and telemetry (logging, metrics, tracing)
* Resilience and backups (replication, snapshots, disaster recovery)

> **lightbulb** Key takeaway: Well-designed and correctly configured infrastructure is the foundation that enables applications to deliver value reliably, securely, and efficiently—just as a well-designed office supports productive work.

## Quick comparison: Office analogy vs. Cloud infrastructure

| Concept                  | Office analogy                | Cloud / Software equivalent               |
| ------------------------ | ----------------------------- | ----------------------------------------- |
| Physical structure       | Building, rooms, power        | Data centers, availability zones, regions |
| Utilities & cabling      | Power, HVAC, network cabling  | Compute, networking, storage              |
| Security & access        | Keycards, locks, guard        | IAM, network security groups, firewalls   |
| Operations & monitoring  | Building maintenance, cameras | Monitoring, logging, alerting             |
| Workers (doing the work) | Employees                     | Applications, microservices, teams        |

## Examples of infrastructure components

| Component         | Purpose                       | Real-world/cloud example                                             |
| ----------------- | ----------------------------- | -------------------------------------------------------------------- |
| Compute           | Run application code          | Virtual machines (EC2), containers (Kubernetes), serverless (Lambda) |
| Storage           | Persist data                  | Object storage (S3), block storage (EBS), managed databases          |
| Networking        | Enable connectivity           | VPC, load balancer, VPN, DNS                                         |
| Identity & Access | Secure access and permissions | IAM roles, service accounts, RBAC                                    |
| Observability     | Understand system behavior    | Logs, metrics, distributed tracing                                   |
| Resilience        | Ensure availability           | Auto-scaling, multi-AZ deployments, backups                          |

## Why the distinction matters

Understanding the separation between application and infrastructure helps teams:

* Design scalable and resilient architectures
* Choose appropriate managed services vs. self-hosted solutions
* Apply security and compliance controls at the right layer
* Automate delivery and infrastructure through Infrastructure as Code (IaC)

For further reading on core concepts:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Documentation](https://www.terraform.io/docs/)
* [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

By thinking of infrastructure as the building and the application as the people inside it, you get a clear mental model for designing systems that are maintainable, secure, and efficient.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/813d9207-e35e-4698-babc-436986515d19/lesson/c4430535-9e32-4142-8c43-161dd740743c)
