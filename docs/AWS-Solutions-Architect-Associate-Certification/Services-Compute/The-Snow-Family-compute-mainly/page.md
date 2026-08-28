# The Snow Family compute mainly

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Compute/The-Snow-Family-compute-mainly/page

This article explores AWS Snowcone and the Snow Family devices designed for data storage, transfer, and local compute capabilities in rugged environments.

In this article, we explore AWS Snowcone as part of the broader AWS Snow Family—a suite of devices designed primarily for data storage and transfer, with select models that also offer compute capabilities. These features make them ideal for scenarios where local processing is required before transferring data to AWS.

AWS Snow Family devices are physical storage solutions that enable the efficient movement of large volumes of data in and out of AWS. Transferring terabytes or petabytes over the internet can be impractical due to speed and security concerns, even with encryption. Instead, AWS ships a physical device to you. Once you load your data onto the device, you send it back to AWS, where the data is securely uploaded to your account.

<Callout icon="lightbulb">
  The typical workflow is as follows:

  1. Order a Snow Family device.
  2. Configure the device locally.
  3. Copy your data onto the device.
  4. Ship it back to AWS.
  5. AWS uploads your data and securely wipes the device after processing.
</Callout>

<Frame>
  ![The image illustrates an operational process flow with icons representing steps: ordering, order received, setup, and data transfer. Each step is depicted with a corresponding icon and label.](https://kodekloud.com/kk-media/image/upload/v1752865006/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-The-Snow-Family-compute-mainly/operational-process-flow-icons.jpg)
</Frame>

Among the Snow Family products, this article focuses on two models with compute capabilities: Snowball Edge and Snowcone. Both devices are equipped with processors that allow you to run services such as [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda) functions directly on the device, which is particularly valuable in rugged environments where deploying a full server is not feasible.

<Frame>
  ![The image illustrates the "Snow Family" with AWS Cloud services, specifically AWS Snowball Edge and AWS Snowcone, connected to icons representing a ship and a windmill.](https://kodekloud.com/kk-media/image/upload/v1752865007/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-The-Snow-Family-compute-mainly/snow-family-aws-services-diagram.jpg)
</Frame>

These ruggedized devices are built to endure extreme conditions, making them suitable for remote locations such as construction sites, ships, airplanes, or other challenging environments. They allow you to perform local computations, securely store data, and later transfer the data to AWS when connectivity becomes available.

## AWS Snowcone Device Overview

The AWS Snowcone is designed for portability and resilience. Key specifications include:

* **Storage Capacity:** 8 terabytes of usable storage
* **Portability:** Weighs about 4.5 pounds
* **Dimensions:** Approximately 9 inches x 6 inches x 3 inches
* **Durability:** Dust-tight and water-resistant construction

<Frame>
  ![The image describes a product called "Snowcone" with 8 terabytes of storage, lightweight and portable dimensions, and ruggedness for harsh conditions.](https://kodekloud.com/kk-media/image/upload/v1752865008/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-The-Snow-Family-compute-mainly/snowcone-8tb-portable-rugged.jpg)
</Frame>

Additional security features of the Snowcone include built-in encryption using AWS Key Management Service and support for a Trusted Platform Module (TPM) that establishes a hardware-based root of trust. Beyond data transfer, the Snowcone is capable of handling localized edge computing workloads. Services such as [AWS IoT Greengrass](https://aws.amazon.com/greengrass/) or launching [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instances at the edge enable processing to occur right where your data is collected.

Devices across the Snow Family offer similar functionalities with varying capacities and form factors, all providing rugged durability, secure storage, and onboard compute capabilities.

## Key Features at a Glance

| Feature             | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| Edge Computing      | Run compute workloads at the data source for faster processing and real-time analytics.     |
| Data Migration      | Collect data locally and securely ship the device back to AWS for smooth data integration.  |
| Rugged Design       | Built to operate in harsh environments such as remote construction sites or maritime areas. |
| Built-in Encryption | Protects data with AWS Key Management Service and a hardware-based Trusted Platform Module. |
| Portability         | Compact and lightweight design ensures easy transport and deployment in the field.          |

This article demonstrates how AWS Snowcone effectively bridges the gap between secure data storage, swift data migration, and on-site computational power, offering a versatile solution for environments where traditional data centers are inaccessible.

For further information on AWS services, you can explore these resources:

* [AWS Documentation](https://aws.amazon.com/documentation/)
* [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda)
* [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/4a24ed66-f258-46c8-ad7c-1c0587d87d41" />
</CardGroup>
