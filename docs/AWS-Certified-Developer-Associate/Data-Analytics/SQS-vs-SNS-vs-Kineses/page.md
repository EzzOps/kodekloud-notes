# SQS vs SNS vs Kineses

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Data-Analytics/SQS-vs-SNS-vs-Kineses/page

This article clarifies the distinct purposes and use cases of Amazon SQS, SNS, and Kinesis to help design efficient and scalable architectures.

In this article, we clarify the distinct purposes and use cases of Amazon SQS, SNS, and Kinesis. These AWS services are often mixed up, so understanding their unique features will help you design more efficient and scalable architectures.

## Amazon SQS

Amazon Simple Queue Service (SQS) is intended for creating decoupled architectures where applications and microservices communicate via message passing. Key features include:

* Maintaining message order with FIFO queues.
* Deleting messages from the queue once processed.
* Storing messages for up to 14 days.

<Callout icon="lightbulb">
  SQS is ideal when you need a reliable and scalable messaging system that decouples components, allowing each service to scale independently.
</Callout>

## Amazon SNS

Amazon Simple Notification Service (SNS) is designed for push-based, multi-subscriber messaging. When an event occurs, SNS publishes a message to a topic, which then broadcasts it to all subscribed endpoints. Important aspects include:

* Immediate message delivery to multiple subscribers.
* Non-persistence of messages; if a subscriber is unavailable at the time of publication, the message may be missed.
* Ability to segregate messages by using separate topics for different event types (e.g., new user registrations, system alerts).

<Callout icon="lightbulb">
  Use SNS when you require real-time communication between services or need to trigger simultaneous actions across multiple endpoints.
</Callout>

## Amazon Kinesis

Amazon Kinesis is tailored for real-time data ingestion and processing, making it suitable for streaming data scenarios such as:

* Big data analytics.
* Streaming logs and performance metrics.

Additional details about Kinesis include:

* Ability to send records up to one megabyte in size.
* A read rate of two megabytes per shard.
* With enhanced fan-out mode, every consumer benefits from a dedicated throughput of two megabytes per shard.

<Callout icon="lightbulb">
  Kinesis is optimal for applications that rely on continuous data streams and require rapid processing and analytics of large volumes of data.
</Callout>

<Frame>
  ![The image is a comparison chart of AWS services: SQS, SNS, and Kinesis, highlighting their features and use cases.](https://kodekloud.com/kk-media/image/upload/v1752858646/notes-assets/images/AWS-Certified-Developer-Associate-SQS-vs-SNS-vs-Kineses/aws-services-comparison-sqs-sns-kinesis.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/ac3fe785-4e7a-4f57-ae16-99fcd3cfde7e/lesson/d4a3bab9-8376-4d66-acd6-985d0bc10322" />
</CardGroup>
