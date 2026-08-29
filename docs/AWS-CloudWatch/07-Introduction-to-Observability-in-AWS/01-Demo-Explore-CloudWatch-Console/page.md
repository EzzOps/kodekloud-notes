# Demo Explore CloudWatch Console

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/Introduction-to-Observability-in-AWS/Demo-Explore-CloudWatch-Console/page

Learn to navigate AWS CloudWatch and create SNS topics for email notifications when alarms trigger.

In this lesson, you’ll learn how to navigate the AWS CloudWatch console and create an Amazon SNS topic for email notifications. This SNS topic will be used in upcoming demos to send alert emails whenever your CloudWatch alarms trigger.

<Callout icon="lightbulb">
  If you’re on the AWS Free Tier, many CloudWatch metrics are free up to specified limits. Standard charges apply once you exceed those quotas.\
  Be sure to choose a region close to you—here we’re using **eu-central-1 (Frankfurt)** for optimal latency.
</Callout>

First, sign in to the AWS Management Console.

<Frame>
  ![The image shows the AWS Management Console home page, displaying sections for recently visited services, AWS health, cost and usage, and options to build solutions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862527/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/aws-management-console-home-page.jpg)
</Frame>

***

## 1. Navigating to CloudWatch

1. In the console’s search bar, type **CloudWatch**.
2. Select **CloudWatch** from the drop-down to open the **CloudWatch Overview**.

On the Overview page, you’ll find these main sections:

| Section                | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| Alarms                 | Set thresholds and trigger actions                         |
| Logs                   | Store, search, and analyze log streams                     |
| Metrics                | Visualize performance data over time                       |
| X-Ray                  | Trace and debug requests across distributed services       |
| Events                 | Respond to state changes in AWS resources                  |
| Application Monitoring | Monitor application health and dependencies                |
| Insights               | Query and visualize log data with CloudWatch Logs Insights |

Use the **Favorites** tab to bookmark dashboards or alarms you check frequently.

<Frame>
  ![The image shows the AWS CloudWatch dashboard interface, displaying options for setting alarms, creating dashboards, viewing logs, and configuring application insights.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862528/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/aws-cloudwatch-dashboard-interface-options.jpg)
</Frame>

***

## 2. Creating an SNS Topic

Amazon SNS (Simple Notification Service) lets you push notifications via email, SMS, HTTP endpoints, and more. To configure email alerts:

1. In the console search bar, type **SNS** and select **Simple Notification Service**.
2. In the left menu, click **Topics**, then **Create topic**.
3. Choose **Standard** as the topic type.
4. For **Name**, enter `CloudWatchCourse`.\
   *(You can optionally set a Display name for SMS protocols.)*
5. Leave other settings at their defaults and click **Create topic**.

<Frame>
  ![The image shows a web interface for creating a topic in Amazon SNS, with options for naming the topic and configuring settings like encryption and access policy.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862529/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/amazon-sns-topic-creation-interface.jpg)
</Frame>

***

## 3. Subscribing an Email Endpoint

Next, attach your email address to the SNS topic so you can receive notifications:

1. Select your newly created `CloudWatchCourse` topic.
2. Click **Create subscription**.
3. For **Protocol**, choose **Email**.
4. In **Endpoint**, enter your email address.
5. Click **Create subscription**.

This action sends a confirmation email to the address you specified.

<Frame>
  ![The image shows a web interface for creating a subscription in Amazon SNS, with fields for Topic ARN, Protocol, and Endpoint. The user is setting up an email subscription.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862530/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/amazon-sns-subscription-setup-interface.jpg)
</Frame>

| Protocol | Use Case                        | Example                          |
| -------- | ------------------------------- | -------------------------------- |
| Email    | Receive notifications via email | `user@example.com`               |
| SMS      | SMS/text message alerts         | `+15551234567`                   |
| HTTP     | Webhook delivery                | `https://my-endpoint.com/notify` |

***

## 4. Confirming the Subscription

Check your inbox for an email from **AWS Notifications**. It contains a **Confirm subscription** link. Click this link to activate your subscription.

<Callout icon="triangle-alert">
  If you do not confirm the subscription, SNS will not deliver any alerts to your email address.
</Callout>

<Frame>
  ![The image shows a Gmail inbox with an email from AWS Notifications about a subscription confirmation. The email includes a link to confirm the subscription to a specific AWS topic.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862531/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/gmail-inbox-aws-notifications-subscription.jpg)
</Frame>

***

## 5. Verifying the Subscription

Back in the SNS console, open your `CloudWatchCourse` topic. Under **Subscriptions**, you should see your email address listed with **Confirmed** status next to the Topic ARN. You’ll reference this ARN when creating CloudWatch alarms.

<Frame>
  ![The image shows an Amazon SNS (Simple Notification Service) console page for a topic named "cloudwatchcourse," displaying details such as the ARN, type, and a confirmed email subscription.](../../../../images/kodekloud.com/kk-media/image/upload/v1752862532/notes-assets/images/AWS-CloudWatch-Demo-Explore-CloudWatch-Console/amazon-sns-console-cloudwatchcourse-topic.jpg)
</Frame>

***

## 6. Switching Time Zones in CloudWatch

By default, CloudWatch displays all metrics and logs in UTC. To switch to your local time zone:

1. In the CloudWatch console, click the **clock** icon in the top-right corner.
2. Select **Local**.

Many teams prefer UTC for consistency across global deployments, but local time can simplify troubleshooting.

***

## Next Steps

* Use this SNS topic ARN when you create CloudWatch alarms in our next lesson.
* Explore [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html) to set up threshold-based notifications.
* Dive into [SNS Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) for advanced delivery options.

***

## Links and References

* [AWS CloudWatch Overview](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
* [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
* [AWS Free Tier Details](https://aws.amazon.com/free/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloudwatch/module/a65b6879-8775-41aa-b922-a289e26672f0/lesson/a2f44e0f-2dfe-42cf-a5f3-76851996400e" />
</CardGroup>
