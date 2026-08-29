# Verified Permissions

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Security/Verified-Permissions/page

This article explores Verified Permissions, an AWS service for scalable and centralized permission management in custom applications.

In this lesson, we explore Verified Permissions—a scalable AWS service that streamlines permission management for custom applications.

Verified Permissions centralizes authorization, allowing you to control user access after authentication is set up. Instead of hardcoding permissions in your application, AWS handles policy management for actions like viewing or deleting content. This centralized model enhances security, simplifies auditing, and decouples authorization from core business logic.

It leverages the Cedar policy language to define granular permissions. With Verified Permissions, you can manage policies via the AWS console, CLI, or SDK. Billing is based on the number of authorization requests processed each month, encouraging efficient permission management.

<Frame>
  ![The image is an infographic titled "Verified Permission" that outlines five features of a service for managing permissions in custom apps, including scalability, security, and pricing details.](../../../../images/kodekloud.com/kk-media/image/upload/v1752865928/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Verified-Permissions/verified-permission-infographic-features.jpg)
</Frame>

The process begins by creating a policy schema, where developers define the authorization model—specifying what actions users are permitted or forbidden to perform. These schemas and their associated policies are securely stored in Amazon Verified Permissions.

<Frame>
  ![The image is a flowchart explaining Amazon Verified Permissions, detailing the process of creating schemas, managing policies, and authorizing access for applications. It includes components like identity providers, Amazon API Gateway, AWS Lambda, and AWS AppSync.](../../../../images/kodekloud.com/kk-media/image/upload/v1752865929/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Verified-Permissions/amazon-verified-permissions-flowchart.jpg)
</Frame>

When your application—whether running on AWS Lambda, Amazon ECS, or another platform—needs to verify a user's permission, it sends a request to the Verified Permissions service. The service cross-references the relevant policy documents and responds with whether the user is authorized to perform the requested action.

<Callout icon="lightbulb">
  Decoupling authorization from your application development allows you to focus on business logic while ensuring secure, centralized permission management.
</Callout>

Verified Permissions embraces a zero-trust architecture, where every access request is authenticated in real time. This model prevents inadvertent permission escalation by ensuring that no user gains unauthorized access due to embedded logic in the application.

There are two primary ways to create policies:

* During development, you can define baseline permissions that serve as the foundation for your application.
* End users can also create custom policies, enabling dynamic and flexible authorization based on evolving needs.

<Callout icon="triangle-alert">
  Be aware that you're charged based on the number of authorization requests processed each month. Monitor your workload to manage costs effectively.
</Callout>

Transcribed by [Otter.ai](https://otter.ai)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/6b2d9e18-1714-499c-83d4-4d1f7ff29e66/lesson/10b9760a-ebf0-4a9f-b8b4-f6ab1d73fca1" />
</CardGroup>
