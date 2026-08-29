# Global Accelerator

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Networking/Global-Accelerator/page

This article explores AWS Global Accelerator and its role in enhancing performance and reliability for globally distributed applications.

In this lesson, we dive into AWS Global Accelerator and explore how it enhances the performance and reliability of your globally distributed applications.

## Why Use Global Accelerator?

Imagine deploying an application in North America while users from all around the world access it. Typically, their requests traverse the public internet via local service providers, which may not offer the most direct or efficient path. This routing can introduce higher latency and less reliable connections, ultimately degrading the user experience.

AWS Global Accelerator overcomes these challenges by connecting users to the nearest edge location and routing their traffic over a dedicated AWS backbone network. This approach not only reduces latency but also improves overall network reliability for global applications.

## How Global Accelerator Optimizes Connectivity

When Global Accelerator is enabled, user traffic is efficiently managed through the following steps:

1. A user sends a request from their location.
2. The request is routed to the closest Global Accelerator edge location.
3. From the edge location, the request travels over the AWS backbone network—a dedicated infrastructure built for high speed, enhanced security, and reliability.
4. Finally, the request reaches the target application hosted within an AWS region or data center.

<Callout icon="lightbulb">
  By bypassing the unpredictable public internet and leveraging the AWS backbone, Global Accelerator ensures your users experience faster and more consistent connections.
</Callout>

<Frame>
  ![The image is a map illustrating the AWS Backbone Network with various global locations marked by icons, labeled "Global Accelerator."](../../../../images/kodekloud.com/kk-media/image/upload/v1752865556/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Global-Accelerator/aws-backbone-network-map.jpg)
</Frame>

The diagram above demonstrates how user traffic is swiftly routed onto the AWS backbone network, making the connection significantly faster compared to traditional internet routing.

## CloudFront vs. Global Accelerator

While both CloudFront and Global Accelerator make use of edge locations, they serve distinct purposes:

| Service            | Primary Focus             | How It Works                                                                                           |
| ------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------ |
| CloudFront         | Caching static content    | Delivers cached content from nearby edge locations to end users                                        |
| Global Accelerator | Optimized network routing | Routes user traffic to the nearest edge, then over the AWS backbone for enhanced speed and reliability |

<Callout icon="lightbulb">
  Explore more about AWS networking solutions and best practices by visiting the [AWS Documentation](https://aws.amazon.com/documentation/).
</Callout>

<Frame>
  ![The image is a summary slide discussing AWS services, specifically CloudFront for caching data at the edge and Global Accelerator for routing users to edge locations for optimized network access.](../../../../images/kodekloud.com/kk-media/image/upload/v1752865557/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Global-Accelerator/aws-cloudfront-global-accelerator-summary.jpg)
</Frame>

Global Accelerator leverages the robust AWS global network to provide secure, fast, and efficient network paths, ensuring your application performs effectively regardless of user location.

## Conclusion

AWS Global Accelerator improves the end-user experience by:

* Routing traffic over a dedicated, high-performance AWS backbone.
* Reducing latency by connecting users to the nearest edge location.
* Enhancing the reliability and security of global network communication.

By integrating Global Accelerator into your infrastructure, you ensure that your global applications are accessible quickly and reliably—delivering a superior experience to your users.

For more information, check out these resources:

* [AWS Global Accelerator](https://aws.amazon.com/global-accelerator/)
* [AWS Networking](https://aws.amazon.com/networking/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/e03ffb87-3345-4fbb-9576-cb53d21d7a6a/lesson/54809d05-e3ad-49e5-8e7e-756bf285f3c7" />
</CardGroup>
