# Understanding the Foundations of Reliability in any Design

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Designing-for-Reliability/Understanding-the-Foundations-of-Reliability-in-any-Design/page

This article explores how reliability is integrated into design and outlines the shared responsibilities between users and AWS.

Welcome, Solutions Architect Associates. In this lesson, we explore how reliability is built into any design—a comprehensive overview that also explains the shared responsibilities between you and AWS.

## The Shared Responsibility Model

For the Solutions Architecture Associate exam, it is important to understand that while AWS manages much of the underlying infrastructure, you are responsible for key aspects such as application architecture, change management, and failure response. AWS takes care of foundational services like EC2 (infrastructure as a service) and RDS (platform as a service), allowing you to interact with managed services. For instance, while you can adjust parameters on an RDS instance, services like DynamoDB are fully managed via API calls without direct server access.

<Frame>
  ![The image illustrates the AWS Shared Responsibility Model for reliability, dividing responsibilities between the customer (resilience "in" the cloud) and AWS (resilience "of" the cloud). It highlights areas like infrastructure testing, workload architecture, and AWS global infrastructure components.](https://kodekloud.com/kk-media/image/upload/v1752863932/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/aws-shared-responsibility-model-reliability.jpg)
</Frame>

When using managed services, AWS assumes most reliability tasks. However, you maintain a crucial role in designing your application's architecture to better mitigate potential failures.

## Areas of Focus

Below are four critical areas to consider while designing resilient systems:

1. **Infrastructure Architecture**\
   Ensure that components like networking, storage, and connectivity are designed with redundancy and resilience in mind. Cloud workloads incorporate service quotas (or service limits) to avoid accidental overuse. Understanding these limits for AWS or third-party services is essential.

   Resistant architectures commonly feature redundant communication paths and efficient IP address management, as outlined in the Well-Architected Framework. For example, AWS storage services often maintain multiple copies of your data. Services like Aurora might store up to six copies to reinforce reliability.

2. **Application (Service) Architecture**\
   Design your applications to be distributed and resilient. A microservices architecture can ensure that a failure in one component does not bring down the entire system. Define clear service contracts through APIs, SLAs, and SLOs to formalize how components interact.

   Strategies to improve reliability include:

   * Implementing graceful degradation to maintain service during partial failures.
   * Using idempotent operations and rate limiting to prevent cascading issues.
   * Applying automatic retry strategies with exponential backoff to handle temporary service endpoint failures.

   Additionally, incorporating stateless design principles—where session and configuration data are managed externally—allows services to recover independently.

<Frame>
  ![The image is a slide titled "Foundations of Reliability – Application Architecture," outlining three steps: Segment Your Works, Build Applications, and Provide Service Contracts, each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752863932/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/foundations-of-reliability-architecture.jpg)
</Frame>

<Frame>
  ![The image outlines six principles of application architecture for reliability: fail gracefully, throttle requests, limit retry calls, limit queues, make services stateless, and make emergency levers.](https://kodekloud.com/kk-media/image/upload/v1752863934/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/application-architecture-reliability-principles.jpg)
</Frame>

3. **Change Management**\
   Reliable systems rely on robust change management practices. This includes continuous monitoring of system metrics, automatically scaling resources based on demand, and setting up proactive notifications to flag unexpected changes. Regular load testing, isolating changes to individual components, and automating deployment, testing, and rollback processes are key.

<Frame>
  ![The image outlines the "Foundations of Reliability – Change Management" with seven steps: monitoring components, defining metrics, sending notifications, automated responses, analytics and data display, reviewing data and metrics, and monitoring sessions.](https://kodekloud.com/kk-media/image/upload/v1752863935/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/foundations-reliability-change-management.jpg)
</Frame>

For example, if your service experiences an unexpected surge, automated systems should detect the shift, scale resources accordingly, and notify the administrators. Periodic reviews and enhancements to your change process will further stabilize your system.

<Frame>
  ![The image outlines four steps in change management for reliability: enabling/disabling changes, limiting changes to isolated zones, reviewing and improving change capability, and automating change.](https://kodekloud.com/kk-media/image/upload/v1752863937/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/change-management-reliability-steps.jpg)
</Frame>

4. **Failure Management**\
   Even with robust AWS infrastructure, you must have a plan to handle application-level failures. This involves regular backups, automated restoration processes, and continuous testing of your disaster recovery plans. Techniques such as [Chaos Engineering](https://learn.kodekloud.com/user/courses/chaos-engineering) or "game days" can be effective for simulating failures and verifying recovery strategies.

<Frame>
  ![The image shows four computer monitor icons in different colors, with the first and last monitors displaying a gear symbol. The text above reads "Foundations of Reliability – Failure Management."](https://kodekloud.com/kk-media/image/upload/v1752863938/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/foundations-reliability-failure-management-monitors.jpg)
</Frame>

Proactive testing, autoscaling, load testing, and chaos engineering can dramatically improve the mean time between failures and ensure rapid recovery when issues occur.

<Callout icon="lightbulb">
  Designing resilient systems requires balancing between AWS-managed infrastructure and your application's unique configuration and response strategies.
</Callout>

## Summary

The AWS Shared Responsibility Model clearly splits roles: AWS manages the underlying infrastructure, while you are accountable for your application's reliability through strategic design in infrastructure, application architecture, change management, and failure management. As the level of managed services increases, direct responsibility for reliability decreases, but understanding these components remains crucial for building resilient systems.

<Frame>
  ![The image illustrates the AWS Shared Responsibility Model, dividing security responsibilities between the customer and AWS. It shows customer responsibilities for security "in" the cloud and AWS responsibilities for security "of" the cloud, including data, applications, infrastructure, and more.](https://kodekloud.com/kk-media/image/upload/v1752863939/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/aws-shared-responsibility-model-2.jpg)
</Frame>

<Frame>
  ![The image is a summary slide explaining the AWS Shared Responsibility Model, highlighting customer and AWS responsibilities, and noting that more managed services reduce customer responsibility.](https://kodekloud.com/kk-media/image/upload/v1752863940/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Understanding-the-Foundations-of-Reliability-in-any-Design/aws-shared-responsibility-model-summary.jpg)
</Frame>

I'm Michael Forrester. If you have any questions, feel free to reach out at [Michael@KodeKloud.com](mailto:Michael@KodeKloud.com). I look forward to connecting with you in the forums, and I hope you found this lesson insightful.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/2a99d085-acf0-4910-924f-737bfc1652da/lesson/dd2809f4-b993-414c-9558-71ce8672ee21" />
</CardGroup>
