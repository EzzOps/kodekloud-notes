# SNS Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Application-Integrations/SNS-Demo/page

This guide demonstrates using Amazon SNS to publish messages and integrate with AWS services for scalable architectures.

In this guide, we demonstrate how to use Amazon Simple Notification Service (SNS) to publish messages and integrate with other AWS services, such as Amazon SQS. This tutorial is ideal for developers looking to build scalable, loosely coupled architectures where multiple backend services communicate through pub/sub messaging.

## Creating an SNS Topic

Navigate to the SNS page and click "Create Topic" to start. For this demonstration, name your topic **createJob**. Imagine a backend system where every new job results in a message published to an SNS topic. Other backend services can subscribe to this topic to pick up messages and process them as needed.

<Frame>
  ![The image shows the Amazon Simple Notification Service (SNS) page on AWS, highlighting its features for pub/sub messaging in microservices and serverless applications, with options to create a topic and view pricing.](https://kodekloud.com/kk-media/image/upload/v1752858394/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/amazon-sns-pub-sub-messaging.jpg)
</Frame>

After entering the topic name, click **Next** to choose between a Standard or FIFO topic. This decision depends on your specific use case. You also have the option to enable encryption and configure various access policies. While additional settings such as data protection and delivery policy exist, we focus only on the essentials here. Finally, click **Create** to finalize the topic creation.

## Configuring Subscriptions

With your topic created, it's time to set up the endpoints that will subscribe to it. Each time a message is published, all subscribed endpoints will receive a notification.

<Frame>
  ![The image shows an Amazon SNS (Simple Notification Service) console screen with a topic named "createJob" successfully created, displaying its details and options for managing subscriptions and policies.](https://kodekloud.com/kk-media/image/upload/v1752858395/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/amazon-sns-createjob-console-screen.jpg)
</Frame>

### Creating a Subscription

1. Select the **createJob** topic.
2. Choose one of the available protocols (email, SMS, SQS, Lambda, or Kinesis Data Firehose) for your subscription.

   For this demo, we'll subscribe an SQS queue named **processJob**.

<Frame>
  ![The image shows an Amazon SNS (Simple Notification Service) subscription details page, indicating a confirmed subscription with specific ARN and endpoint information.](https://kodekloud.com/kk-media/image/upload/v1752858397/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/amazon-sns-subscription-details.jpg)
</Frame>

## Publishing a Message

Once the subscription is set up, return to the topic and click on **Publish a message**. In the message body, you might write a simple message such as:

```python theme={null}
