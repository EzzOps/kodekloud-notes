# Example message content
new job
```

This message indicates a new job submission. After entering your message (and optionally adding extra attributes), click **Publish**.

## Verifying in SQS

To confirm that messages flow correctly, check the **processJob** SQS queue by navigating to the "Send and receive messages" section and polling for messages.

![The image shows an Amazon SQS interface for sending and receiving messages from a queue, with options to enter a message body, set a delivery delay, and poll for messages.](https://kodekloud.com/kk-media/image/upload/v1752858398/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/amazon-sqs-message-interface.jpg)

> **lightbulb** If no messages are visible in your SQS queue, it may be due to insufficient permissions allowing SNS to send messages to SQS.

### Updating SQS Access Policy

SNS might be publishing messages correctly, but the SQS queue requires the proper permissions to accept these messages. To resolve this, update your SQS access policy. Below is an example of an SQS policy that grants SNS permission to send messages. **Make sure to adjust the ARNs for both the SQS queue and SNS topic to suit your environment.**

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage"
      ],
      "Resource": "arn:aws:sqs:us-east-1:841869297337:processJob",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:841869297337:createJob"
        }
      }
    }
  ]
}
```

After updating the policy, publish another message to your SNS topic using more detailed content (for example, "job details: ..."). Then, return to the SQS console and use the **Send and receive messages** function to poll for messages. You should now see the message delivered to the queue.

![The image shows an Amazon SNS interface where a message has been successfully published to a topic. It includes fields for message details like subject and message structure options.](https://kodekloud.com/kk-media/image/upload/v1752858399/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/amazon-sns-message-published-interface.jpg)

![The image shows an AWS SQS (Simple Queue Service) interface where users can send and receive messages from a queue. It includes fields for entering a message, setting a delivery delay, and options for receiving messages.](https://kodekloud.com/kk-media/image/upload/v1752858400/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Demo/aws-sqs-interface-message-queue.jpg)

## Examining the SQS Message Structure

When a message is delivered to SQS, it is structured in a JSON format. A portion of the message may look like the following:

```json theme={null}
{
  "Type": "Notification",
  "MessageId": "43d4b488-c180-834a-ea1f078528e6",
  "TopicArn": "arn:aws:sns:us-east-1:848186092733:createjob"
}
```

Additional details, such as the subject, content, timestamp, and signature, might be included:

```json theme={null}
{
  "Message": "job details: ...",
  "Timestamp": "2024-04-16T00:21:44.791Z",
  "SignatureVersion": "1"
}
```

## Conclusion

This demonstration shows how to set up Amazon SNS and integrate it with SQS to achieve efficient message-based communication between services. By configuring the correct permissions and subscriptions, you enable scalable and robust architectures where multiple endpoints—whether email, Lambda functions, SQS queues, or others—can consume messages published to an SNS topic.

For more information, visit the [AWS SNS Documentation](https://aws.amazon.com/sns/) and explore further integrations to match your application needs.

Happy coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/60c267ab-da8b-4408-97f4-b53aad3f4479/lesson/d356452a-bf4d-467f-8aab-fa594559c358)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/60c267ab-da8b-4408-97f4-b53aad3f4479/lesson/fefdfa9f-ba9a-4b5f-bf1d-9f0e4a32ec7c)


# SNS Overview

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Application-Integrations/SNS-Overview/page

This article explores AWS’s Simple Notification Service (SNS), a cloud messaging service that enables publishers to send notifications to multiple subscribers.

This article explores AWS’s Simple Notification Service (SNS), a robust cloud messaging service that functions like a digital postal system. SNS enables publishers to send notifications that are simultaneously delivered to multiple subscribers, making it a cornerstone in event-driven architectures.

## How SNS Works

AWS SNS leverages a publish/subscribe model that simplifies message distribution. Here’s an overview of the process:

1. A producer (or publisher) sends a message to an SNS topic.
2. The SNS topic acts as a communication channel, similar to a "radio frequency."
3. All subscribers listening to that topic receive the message.

![The image is a diagram showing the flow of data from a client to an AWS SNS Topic, which then triggers a Lambda function within an AWS account.](https://kodekloud.com/kk-media/image/upload/v1752858401/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Overview/aws-sns-topic-lambda-diagram.jpg)

> **lightbulb** When a message is published, only subscribers who have signed up for that specific topic will process it. This facilitates event-based communication across different system components. For example, a new user registration could trigger both a welcome email and a verification process.

## Publishers in SNS

SNS supports a variety of publishers, including several AWS services. Common examples include:

* CloudWatch alarms
* EC2 instances
* Elastic Beanstalk
* S3 events
* CodePipeline, among others

![The image is a diagram showing various AWS services as publishers (like CloudWatch, EC2 Auto Scaling, and S3) connected to Amazon SNS (Simple Notification Service).](https://kodekloud.com/kk-media/image/upload/v1752858402/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Overview/aws-services-publishers-sns-diagram.jpg)

## Subscribers in SNS

SNS offers flexible options for subscribers. Typical subscribers include:

* SQS queues
* Lambda functions
* HTTP endpoints
* EC2 instances
* Kinesis Data Firehose

In addition to these, SNS can deliver notifications via SMS, email, or mobile push notifications.

![The image is a diagram illustrating SNS subscribers, showing the flow from a publisher to SNS, and then to Application-to-Application (A2A) and Application-to-Person (A2P) subscribers, including services like SQS, AWS Lambda, and email.](https://kodekloud.com/kk-media/image/upload/v1752858404/notes-assets/images/AWS-Certified-Developer-Associate-SNS-Overview/sns-subscribers-diagram-flow.jpg)

## Fan-Out Architecture with SNS and SQS

SNS can be paired with SQS to implement a fan-out architecture, where a single SNS message is replicated across multiple endpoints. This approach allows different processing tasks to be executed concurrently by distinct SQS queues.

Consider a scenario inspired by video streaming platforms:

* When a user uploads a video, the video metadata is published to an SNS topic.
* One SQS queue processes tasks such as video format conversion (e.g., 4K or 1080p).
* Another SQS queue handles the generation of video thumbnails.

This architecture ensures multiple downstream processes react independently to a single event, thereby enhancing system scalability.

## Access Control with SNS Resource Policies

SNS resource policies are critical for enforcing security and controlling access. These policies define which entities can publish or subscribe to a topic. For instance, you might restrict publishing permissions only to a specific IAM role.

Below is an example policy that permits only a designated role to publish messages to an SNS topic:

```json theme={null}
{
  "Sid": "AllowSpecificRoleToPublish",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::123456789012:role/SpecificPublishingRole"
  },
  "Action": "SNS:Publish",
  "Resource": "arn:aws:sns:us-west-2:123456789012:MySNSTopic",
  "Condition": {
    "ArnEquals": {
      "aws:SourceArn": "arn:aws:iam::123456789012:role/SpecificPublishingRole"
    }
  }
}
```

> **triangle-alert** It is crucial to configure SNS resource policies correctly to prevent unauthorized access and ensure that only trusted entities can interact with your SNS topics.

## Summary

AWS SNS is a versatile and scalable messaging service designed to distribute messages efficiently to multiple subscribers. Its ability to integrate with various AWS services and external systems makes it an essential tool for building event-driven architectures. By leveraging SNS for secure and rapid message delivery, organizations can ensure that notifications reach the appropriate endpoints reliably.

For additional resources on AWS services and best practices, visit the [AWS Documentation](https://aws.amazon.com/documentation/).

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/60c267ab-da8b-4408-97f4-b53aad3f4479/lesson/e81dfdfe-9d70-4b89-865b-c9a17973234a)
