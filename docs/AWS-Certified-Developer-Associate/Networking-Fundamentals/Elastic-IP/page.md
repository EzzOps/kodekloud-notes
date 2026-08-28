# Elastic IP

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Networking-Fundamentals/Elastic-IP/page

This article explores AWS Elastic IPs, their benefits for maintaining consistent public IP addresses for EC2 instances, and their pricing considerations.

In this lesson, we explore AWS Elastic IPs and how they help maintain a consistent public IP address for your EC2 instances. This is especially useful when you require a stable endpoint for backend servers or client communications.

## Why Use Elastic IPs?

When you deploy an EC2 instance within a public subnet, it automatically receives a public IP address (for example, 1.1.1.1). However, this IP is dynamically allocated and can change upon reboot or restart. This dynamic behavior may disrupt applications that rely on a fixed IP address.

Elastic IP addresses resolve this issue by providing static IPv4 addresses exclusively allocated to your AWS account. Once you allocate an Elastic IP, it remains reserved for you, ensuring the instance maintains the same IP regardless of reboots or hardware migrations.

<Callout icon="lightbulb">
  Elastic IPs offer the flexibility to disassociate from one instance and reassociate with another during maintenance, ensuring uninterrupted service.
</Callout>

<Frame>
  ![The image illustrates an AWS Cloud setup with two servers, Server A and Server B. Server A is marked with an error, while Server B is associated with the IP address 1.1.1.1.](https://kodekloud.com/kk-media/image/upload/v1752859132/notes-assets/images/AWS-Certified-Developer-Associate-Elastic-IP/aws-cloud-setup-servers-error.jpg)
</Frame>

## Pricing Considerations

AWS provides an Elastic IP at no extra cost when it is associated with a running EC2 instance. However, if you attach more than one Elastic IP to an instance or reserve an Elastic IP without linking it to a running instance, AWS charges a small hourly fee for the additional allocation.

<Frame>
  ![The image illustrates "Elastic IP Pricing" with a diagram showing additional IPs being charged per hour, represented by a chip-like graphic.](https://kodekloud.com/kk-media/image/upload/v1752859133/notes-assets/images/AWS-Certified-Developer-Associate-Elastic-IP/elastic-ip-pricing-diagram.jpg)
</Frame>

## Key Points to Remember

* Elastic IPs are region-specific and cannot be transferred across AWS regions.
* They can only be associated with EC2 instances within the same region.
* You can obtain Elastic IPs from either Amazon's pool of IPv4 addresses or your custom IPv4 address pool.

<Frame>
  ![The image is a diagram about Elastic IPs, highlighting that they are specific to a region and come from Amazon's pool of IPv4 addresses.](https://kodekloud.com/kk-media/image/upload/v1752859134/notes-assets/images/AWS-Certified-Developer-Associate-Elastic-IP/elastic-ips-amazon-ipv4-diagram.jpg)
</Frame>

## How to Allocate and Associate an Elastic IP

To leverage the benefits of an Elastic IP, follow these steps:

1. Allocate the Elastic IP to your AWS account.
2. Associate the Elastic IP with your EC2 instance or network interface.

This process guarantees that your instance maintains a static public IP even during modifications or migrations.

<Callout icon="lightbulb">
  Elastic IPs are essential for applications that demand fixed IP endpoints, particularly during service migrations or routine maintenance.
</Callout>

## Summary

EC2 instances with standard public IPs can experience address changes on reboot, whereas Elastic IPs provide a static alternative that ensures continuity and reliability. This stability is fundamental for applications that rely on consistent communication endpoints.

<Frame>
  ![The image is a summary slide explaining the differences between public IPs and Elastic IPs, highlighting that public IPs are not static, while Elastic IPs are static IPv4 addresses. It also describes the process of allocating and associating an Elastic IP with an instance or network interface.](https://kodekloud.com/kk-media/image/upload/v1752859135/notes-assets/images/AWS-Certified-Developer-Associate-Elastic-IP/public-vs-elastic-ips-summary.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/c8f3ca76-9178-474e-a33b-bf1de4fd948c/lesson/152fd3e8-be1f-411b-9827-304b4b199ec6" />
</CardGroup>
