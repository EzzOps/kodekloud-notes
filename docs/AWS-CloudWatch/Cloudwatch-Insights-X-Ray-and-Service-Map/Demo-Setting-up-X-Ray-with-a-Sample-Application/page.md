# Demo Setting up X Ray with a Sample Application

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/Cloudwatch-Insights-X-Ray-and-Service-Map/Demo-Setting-up-X-Ray-with-a-Sample-Application/page

Learn to deploy a demo app on AWS, instrument it with AWS X-Ray, and analyze traces and service maps in Amazon CloudWatch for microservices visibility.

In this guide, you’ll learn how to deploy a demo app on AWS, instrument it with AWS X-Ray, and analyze traces and service maps in Amazon CloudWatch. By the end, you’ll have end-to-end visibility into a microservices architecture using HTTP endpoints, ECS, and DynamoDB.

## Prerequisites

* An AWS account with permissions for CloudWatch, X-Ray, CloudFormation, ECS, DynamoDB, and IAM
* AWS CLI or Console access

<Callout icon="lightbulb">
  Make sure your IAM user or role has the required permissions for deploying CloudFormation stacks and viewing X-Ray service maps.
</Callout>

## Step 1: Deploy the Sample Application via CloudFormation

1. Log in to the AWS Console and open **CloudWatch**.
2. In the left sidebar, expand **X-Ray Traces** and select **Service Map**.
3. Click **Setup Demo App**, then choose **Create Sample Application with CloudFormation**.
4. Proceed through the wizard without changing defaults:
   * **Next** → **Next**
   * Acknowledge IAM capabilities → **Submit**

This creates a CloudFormation stack named `xray-sample`.

<Frame>
  ![The image shows an AWS CloudFormation console page with options for notification and stack creation, including capabilities and IAM resource acknowledgments.](https://kodekloud.com/kk-media/image/upload/v1752862513/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudformation-console-notification-stack.jpg)
</Frame>

<Callout icon="triangle-alert">
  The demo stack provisions ECS clusters, an Application Load Balancer, and DynamoDB tables. You may incur AWS charges—remember to delete the stack when you're done.
</Callout>

## Step 2: Wait for Stack Completion

Monitor the stack events and wait until the status changes to **CREATE\_COMPLETE**.

<Frame>
  ![The image shows an AWS CloudFormation console with a stack named "xray-sample" in the process of being created. The status is "CREATE\_IN\_PROGRESS" and the event is user-initiated.](https://kodekloud.com/kk-media/image/upload/v1752862514/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudformation-xray-sample-creation.jpg)
</Frame>

## Step 3: Retrieve the Load Balancer URL

1. Once complete, switch to the **Outputs** tab.
2. Copy the **LoadBalancerUrl** value.

<Frame>
  ![The image shows an AWS CloudFormation console with a stack named "xray-sample" that has a status of "CREATE\_COMPLETE." The Outputs tab displays a LoadBalancerUrl with a specific URL value.](https://kodekloud.com/kk-media/image/upload/v1752862516/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudformation-xray-sample-output.jpg)
</Frame>

## Step 4: Launch the Scorekeep Web App

Paste the LoadBalancerUrl into your browser to open the Scorekeep application.

<Frame>
  ![The image shows a web page titled "Scorekeep" with options to create or join a session, powered by AWS's EC2 Launch Type via Elastic Container Service. There are input fields for a session name and session ID, along with "Create" and "Join" buttons.](https://kodekloud.com/kk-media/image/upload/v1752862517/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/scorekeep-web-page-aws-ec2.jpg)
</Frame>

## Step 5: Create and Play a Game Session

1. Click **Create**.
2. Enter a session name (e.g., “ABC Tools Tic-Tac-Toe”).
3. Click **Create**, then **Play**.

<Frame>
  ![The image shows a web page titled "Scorekeep" where users can create a game by entering a name and selecting rules, with an option to view session traces. It is powered by AWS's EC2 Launch Type via Elastic Container Service.](https://kodekloud.com/kk-media/image/upload/v1752862518/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/scorekeep-game-creation-webpage-aws.jpg)
</Frame>

Play several rounds of tic-tac-toe. AWS X-Ray collects traces for every request behind the scenes.

<Frame>
  ![The image shows a tic-tac-toe game where "X" has won. It is displayed on a webpage with options to view game traces and a service map.](https://kodekloud.com/kk-media/image/upload/v1752862519/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/tic-tac-toe-x-wins-webpage.jpg)
</Frame>

## Step 6: View the Service Map

1. In the Scorekeep UI, click **View Service Map**.
2. This opens the X-Ray console displaying your microservices topology.

<Frame>
  ![The image shows an AWS CloudWatch service map interface, displaying connections between various services like ECS containers, SNS topics, and DynamoDB tables. The interface includes options for filtering and viewing logs, traces, and dashboards.](https://kodekloud.com/kk-media/image/upload/v1752862520/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudwatch-service-map-interface.jpg)
</Frame>

### Drill Into Nodes and Traces

* Select any node (e.g., **DynamoDB** for user data).
* View metrics, latency distributions, and HTTP metadata.
* Click **View traces** to access individual X-Ray segments.

<Frame>
  ![The image shows an AWS CloudWatch interface displaying X-Ray traces with details about various nodes, including latency and request metrics. The interface includes options for refining queries and viewing trace details.](https://kodekloud.com/kk-media/image/upload/v1752862522/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudwatch-xray-traces-interface.jpg)
</Frame>

Opening a specific trace reveals each segment’s timeline:

<Frame>
  ![The image shows an AWS CloudWatch X-Ray trace view, detailing a trace with segments for "Scorekeep" and "DynamoDB," including response codes and durations. The timeline visualizes the execution time of each segment.](https://kodekloud.com/kk-media/image/upload/v1752862523/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudwatch-xray-trace-view.jpg)
</Frame>

Here you’ll see:

* A `GET` call to the Scorekeep endpoint
* The corresponding **GetItem** action on DynamoDB
* Latency and HTTP status codes for each segment

This full-stack visibility helps you pinpoint latency spikes, errors, and resource bottlenecks.

<Frame>
  ![The image shows an AWS CloudWatch service map interface, displaying a network of connected nodes representing different services and resources.](https://kodekloud.com/kk-media/image/upload/v1752862525/notes-assets/images/AWS-CloudWatch-Demo-Setting-up-X-Ray-with-a-Sample-Application/aws-cloudwatch-service-map-interface-2.jpg)
</Frame>

## AWS X-Ray Key Components

| Resource       | Purpose                             | AWS Service               |
| -------------- | ----------------------------------- | ------------------------- |
| ECS Container  | Hosts the Scorekeep application     | Amazon ECS                |
| Load Balancer  | Routes HTTP traffic to containers   | Application Load Balancer |
| DynamoDB Table | Stores game session and move data   | Amazon DynamoDB           |
| SNS Topic      | Publishes game events notifications | Amazon SNS                |

## Best Practices

* Enable X-Ray tracing in production by integrating the [AWS X-Ray SDK](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk.html) into your code.
* Use sampling rules to control data volume and cost.
* Tag resources for trace grouping and filtering.

<Callout icon="lightbulb">
  Regularly review your service map to detect anomalies and optimize the performance of microservices.
</Callout>

***

## References

* [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
* [Amazon CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloudwatch/module/d95c04dd-f122-4f6b-93dc-d0b2fe015b29/lesson/6804b9ea-8ae6-4b9a-a94c-ffb1b44d38d9" />
</CardGroup>
