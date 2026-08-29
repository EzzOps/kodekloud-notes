# Organizations

Source: https://notes.kodekloud.com/docs/AWS-Cloud-Practitioner-CLF-C02/Security-and-Compliance/Organizations/page

This article explores AWS Organizations, a feature for simplifying multi-account management and enhancing operational efficiency in cloud infrastructure.

In this lesson, we explore AWS Organizations—a powerful feature designed to simplify your multi-account management. AWS Organizations is particularly useful as your cloud infrastructure grows and you add accounts for various environments such as development, staging, and production, or even for different departments within your organization.

<Callout icon="lightbulb">
  AWS Organizations centralizes billing and user management, thereby reducing the administrative overhead associated with managing multiple AWS accounts.
</Callout>

## Overview of AWS Organizations

Managing separate AWS accounts can quickly become complex because:

* Each account produces its own bill, even if they share the same payment method.
* User management and permissions are handled individually, leading to repetitive administrative tasks.

AWS Organizations bridges these gaps by enabling you to manage multiple AWS accounts efficiently. One of its standout features is Service Control Policies (SCPs).

### Service Control Policies (SCPs)

SCPs are similar to IAM policies but operate at the account level. They allow you to define boundaries on the services and actions that an account is permitted to use. By setting these limits, SCPs ensure that each account adheres to your organization's security and operational standards.

<Frame>
  ![The image illustrates AWS Service Control Policies (SCP) for development environments, showing different AWS services and their associated policies within an organization.](../../../../images/kodekloud.com/kk-media/image/upload/v1752861738/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-Organizations/frame_70.jpg)
</Frame>

### Organizational Units (OUs)

When dealing with multiple AWS accounts that share similar business and security requirements, it is beneficial to group them using Organizational Units (OUs). An OU acts as a container for similarly configured accounts, allowing you to apply a single Service Control Policy across the entire group. This streamlined approach ensures consistency and compliance across your organization.

<Frame>
  ![The image depicts an organizational structure with a root node branching into accounts for Dev, Staging, and App1, and a Production organizational unit.](../../../../images/kodekloud.com/kk-media/image/upload/v1752861740/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-Organizations/frame_100.jpg)
</Frame>

## Summary of Key Points

| Feature                         | Benefit                                                                 | Example Scenario                                      |
| ------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| AWS Organizations               | Simplifies management of multiple accounts                              | Centralized billing and account management            |
| Service Control Policies (SCPs) | Restricts services and actions at the account level                     | Limiting specific services in development accounts    |
| Organizational Units (OUs)      | Groups similarly configured accounts for streamlined policy enforcement | Applying uniform security settings across departments |

<Callout icon="lightbulb">
  AWS Organizations not only enhances security but also improves operational efficiency by allowing you to manage multiple accounts under a unified system.
</Callout>

<Frame>
  ![The image summarizes AWS Organizations, highlighting management of multiple accounts, organizational units, service control policies, and their application to accounts or units.](../../../../images/kodekloud.com/kk-media/image/upload/v1752861741/notes-assets/images/AWS-Cloud-Practitioner-CLF-C02-Organizations/frame_140.jpg)
</Frame>

For additional reading on AWS account management and best practices, consider visiting the [AWS Organizations Documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-practitioner-clf-c02/module/4528372a-a177-43ff-b4b6-236c0eee4029/lesson/ed30a5c9-a3f1-416a-a523-febba96ca132" />
</CardGroup>
