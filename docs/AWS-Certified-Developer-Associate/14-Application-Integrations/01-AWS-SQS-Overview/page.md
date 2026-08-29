# AWS SQS Overview

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Application-Integrations/AWS-SQS-Overview/page

This article provides an overview of Amazon Simple Queue Service (SQS) and its role in decoupling microservices for scalable architectures.

In this lesson, we explore the Amazon Simple Queue Service (SQS), a fully managed messaging service that decouples microservices to build scalable and resilient architectures. SQS is particularly useful when you need to buffer communications between components of distributed systems, smoothing out spikes in traffic and reducing bottlenecks.

Imagine an e-commerce application composed of various services. For instance, the cart service handles a user's shopping cart, and when a purchase is initiated, it sends a message to trigger a payment service. The payment service then invokes the invoice service, which generates an invoice. Other services like inventory, labeling, dispatch, and tracking take over thereafter to process and deliver the order. In such microservice architectures, running operations sequentially can become a performance bottleneck.

<Frame>
  ![The image illustrates an e-commerce application's workflow, highlighting the need for SQS (Simple Queue Service) to address issues like sequential processing, degraded performance, and high cost.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858340/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/ecommerce-workflow-sqs-issues.jpg)
</Frame>

If a surge in user activity—such as during a holiday sale—overwhelms the payment service, the sequential design can lead to degraded performance and increased costs. SQS resolves this issue by acting as a message queue: once the purchase is initiated, the cart service sends a message to the queue and continues processing immediately without waiting for the payment service to respond.

<Frame>
  ![The image is a flowchart illustrating the need for SQS in an e-commerce application, showing processes like cart, payment, invoice, inventory, labeling, dispatch, and tracking.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858342/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-ecommerce-flowchart-processes.jpg)
</Frame>

When the payment service has the capacity, it retrieves the next message from the queue. This decoupling ensures that spikes in one service do not overwhelm others.

## Key Features of SQS

SQS is designed to decouple components within distributed applications. Producers can send messages to the queue without knowing the specifics of the consumers, promoting flexible and loosely coupled system design. By buffering messages, SQS helps smooth out traffic bursts and supports asynchronous processing in serverless and event-driven architectures.

<Frame>
  ![The image illustrates four SQS solutions: Message Decoupling, Load Leveling, Asynchronous Processing, and Scalable Architecture, each represented with an icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858343/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-solutions-message-decoupling-icons.jpg)
</Frame>

### Terminology and Components

* **Queue:** Serves as a buffer that holds messages from producers until consumers are ready to process them.
* **Messages:** Units of communication up to 256 KB in size. They can include metadata as key-value pairs.
* **Producers:** Entities (such as EC2 instances, Lambda functions, or EventBridge events) that send messages to the queue.
* **Consumers:** Entities that poll and process messages from the queue.
* **Dead Letter Queue:** A secondary queue that stores messages which could not be processed successfully after multiple attempts.
* **Configuration Options:** Settings such as timeouts and message visibility that help prevent duplicate processing.

<Frame>
  ![The image illustrates the components of Amazon Simple Queue Service (SQS), showing producers, messages, and queues.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858344/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/amazon-sqs-components-producers-queues.jpg)
</Frame>

When using AWS Lambda functions as both producers and consumers, one function sends a message to the SQS queue, and another function later processes and deletes the message.

## Queue Types: Standard vs. FIFO

SQS offers two types of queues: Standard and FIFO. Each type is suited to different use cases.

### Standard Queues

Standard queues provide:

* **Best-Effort Ordering:** The order in which messages are sent might not be preserved.
* **At-Least-Once Delivery:** Messages can be delivered more than once.
* **Unlimited Throughput:** Ideal for high-volume applications.

<Frame>
  ![The image shows two types of SQS queues: Standard Queues and FIFO Queues, each represented with a gradient-colored card and an icon.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858345/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-queues-standard-fifo-diagram.jpg)
</Frame>

For example, if messages 1, 2, and 3 are sent sequentially in a standard queue, they may arrive out of order, and duplicates might occur.

<Frame>
  ![The image illustrates the concept of SQS Standard Queues, showing unordered message delivery and highlighting advantages like best-effort ordering, at-least-once delivery, and maximum throughput. It also depicts various application/subscriber icons.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858346/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-standard-queues-message-delivery.jpg)
</Frame>

Both Standard and FIFO queues share several features:

* **Maximum Retention Period:** Up to 14 days.
* **Maximum Message Size:** 256 kilobytes.
* **Low Latency:** Ensuring rapid message processing.

<Frame>
  ![The image describes features of a "Standard Queue," highlighting unlimited throughput, a maximum retention of 14 days, a maximum of 256 KB per message sent, and low latency.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858348/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/standard-queue-features-throughput-retention.jpg)
</Frame>

### FIFO Queues

FIFO (First-In-First-Out) queues are ideal for scenarios requiring:

* **Strict Ordering:** Messages are processed exactly in the order they are sent.
* **Exactly-Once Processing:** Each message is processed just once, preventing duplicates.
* **Limited Throughput:** Supports up to 3000 messages per second with batching or 300 messages per second without batching. Higher throughput modes are available with configuration.
* **Message Grouping:** Allows messages to be processed in parallel while maintaining order within each group.
* **Message Deduplication:** Eliminates duplicate messages based on a deduplication ID.

<Frame>
  ![The image is a diagram titled "FIFO Queue" listing six features: order preservation, exactly-once processing, limited throughput, message grouping, message deduplication, and maximum retention period.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858349/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/fifo-queue-features-diagram.jpg)
</Frame>

## SQS Extended Client Library

For messages that exceed the standard 256 KB size limit, the Amazon SQS Extended Client Library provides a solution. When a message’s payload is too large, the library automatically uploads the content to an Amazon S3 bucket and sends a reference to that object via SQS. Consumers then retrieve the full message from S3 using the provided reference.

Key features include:

* Support for messages up to 2 GB by storing payloads in S3.
* Seamless integration with existing SQS workflows.
* Customizable options for S3 bucket policies, encryption, and lifecycle management.
* Backward compatibility with standard SQS clients.
* Awareness of potential cost and performance considerations due to S3 usage.

<Frame>
  ![The image illustrates the workflow of the SQS Extended Client Library, showing how a producer sends a message with a reference to an S3 object to an SQS queue, which is then received by a consumer.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858350/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-extended-client-workflow-diagram.jpg)
</Frame>

<Frame>
  ![The image lists features of the SQS Extended Client Library, including large message support, seamless integration, customizable S3 storage, backward compatibility, cost and performance considerations, and ease of use.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858351/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-extended-client-library-features.jpg)
</Frame>

## Integration with Auto Scaling

You can integrate SQS with EC2 Auto Scaling Groups to dynamically adjust processing capacity based on message volume. By configuring a CloudWatch alarm to monitor the "ApproximateNumberOfMessages" metric, you can automatically scale the number of consumer instances accordingly.

<Frame>
  ![The image illustrates the integration of an SQS queue with an Auto Scaling Group (ASG), showing message polling and scaling based on the approximate number of messages.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858352/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/sqs-auto-scaling-group-integration.jpg)
</Frame>

## Access Policies

SQS supports fine-grained access policies to control which entities can publish or consume messages. For example, the following policy grants specific AWS accounts the permission to send messages to the queue:

```json theme={null}
{
  "Version": "2012-10-17",
  "Id": "QueuePolicy",
  "Statement": [
    {
      "Sid": "Allow-SendMessage",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::111122223333:root",
          "arn:aws:iam::444455556666:root"
        ]
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:123456789012:MyQueue"
    }
  ]
}
```

<Callout icon="lightbulb">
  This configuration is particularly useful for enabling secure cross-account access to your SQS queues.
</Callout>

## Summary

SQS is a fully managed messaging queuing service that enhances microservice architectures, distributed systems, and serverless applications. Key takeaways include:

* Producers send messages to a queue, and consumers process and delete them.
* Standard queues provide best-effort ordering with at-least-once delivery and unlimited throughput.
* FIFO queues ensure strict ordering, exactly-once processing, and support message grouping and deduplication.
* The SQS Extended Client Library allows handling of larger messages by leveraging Amazon S3.
* Access policies enable granular control over who can publish or consume messages.

<Frame>
  ![The image is a summary slide highlighting key points about message queuing, including its management for microservices, the process of sending and consuming messages, and details on message size and retention.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858354/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/message-queuing-summary-microservices.jpg)
</Frame>

<Frame>
  ![The image is a summary slide highlighting three points about message queues: FIFO queues ensure ordering and no duplicates, the SQS extended client library allows processing larger messages using S3 buckets, and access policies control who can send and consume messages.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858355/notes-assets/images/AWS-Certified-Developer-Associate-AWS-SQS-Overview/message-queues-summary-fifo-sqs.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/60c267ab-da8b-4408-97f4-b53aad3f4479/lesson/af4598a4-31a1-4fc3-80f0-0996343d7eee" />
</CardGroup>
