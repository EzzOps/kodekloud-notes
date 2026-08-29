# SSH into the instance (example)
ssh -i main.pem ec2-user@10.0.129.234

# Check current CPU usage (you can use top)
top

# Install stress if not present (on Amazon Linux)
sudo yum install -y stress    # or use your distribution's package manager

# Run a single worker to saturate one CPU
stress -c 1
```

Sample `top` output before stressing:

```bash theme={null}
top - 04:33:30 up 3 min,  2 users,  load average: 0.01, 0.04, 0.01
%Cpu(s):  0.0 us,  6.2 sy, 93.8 id
MiB Mem :   949.4 total,    572.5 free,    159.3 used,    217.6 buff/cache
```

After starting `stress -c 1` you should see CPU usage increase toward 100% on one core:

```bash theme={null}
top - 04:34:00 up 4 min,  2 users,  load average: 0.29, 0.10, 0.03
%Cpu(s):100.0 us, 0.0 sy, 0.0 id
  PID USER      PR  NI    VIRT    RES  SHR S  %CPU %MEM     TIME+ COMMAND
 2556 ec2-user  20   0    3512   112    0 R  99.7  0.0   0:19.71 stress
```

The ASG target-tracking policy detects the higher average CPU and will scale out by launching additional instances, up to your configured maximum.

> **lightbulb** Target tracking maintains the average metric (CPU in this case) across all instances in the group. Setting a lower target causes scale-out sooner; set targets conservatively for production.

## 9) Observe scaling events and capacity limits

When the average CPU breaches the target, the ASG Activity tab shows alarms and capacity adjustments (for example: Desired capacity increases from 1 to 3). The ASG will never exceed the configured maximum capacity (3 in this demo), even if CPU remains high.

Confirm new instances in the EC2 Instances list and watch the Target Group for additional registered targets.

<Frame>
  <img alt="A screenshot of the AWS EC2 Auto Scaling Groups console showing an Auto Scaling group named &#x22;web-autoscale.&#x22; The group uses the &#x22;myweb-template&#x22;, shows 3 instances but a Desired/Min/Max capacity of 0 and is marked &#x22;Deleting.&#x22;" />
</Frame>

## 10) Cleanup

When you finish the demo, delete the Auto Scaling Group. If you created an ALB and target group specifically for this demo, delete those too to avoid ongoing charges. Also remove any EC2 instances, security groups, and unused key pairs you no longer need.

> **warning** Remember to clean up ALBs, target groups, EC2 instances, and ASGs after testing to avoid unexpected costs.

This completes the basic walkthrough for:

* Creating an Auto Scaling Group from a launch template
* Attaching an Application Load Balancer and a target group
* Verifying instance replacement behavior
* Using a CPU-based target tracking scaling policy

## Links and references

* [Auto Scaling Groups - AWS Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
* [Application Load Balancer - AWS Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
* [Launch templates - AWS Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html)
* [Target tracking scaling policies - AWS Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/95fa1e2d-e2a0-4a66-a7a2-6da1a8ee7050)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/8b2409bc-5fa2-47d8-bd78-e38e354e57a7)


# AWS SNSSQS

Source: https://notes.kodekloud.com/docs/AWS-For-Beginners-with-Hands-On-Labs/AWS-Essentials-Part-2/AWS-SNSSQS/page

Guide to building a serverless AWS video processing pipeline using S3 event notifications, SNS fan-out, SQS buffering, and Lambda for transcoding and thumbnail generation.

In this guide you'll learn how to build a simple, serverless video-processing pipeline on AWS using S3 event notifications, Amazon SNS for fan-out, Amazon SQS for durable buffering, and Lambda for processing (transcoding and thumbnail generation). The architecture is scalable, cost-effective, and works well for workloads that need to fan out a single upload to multiple consumers.

High-level flow:

* A user uploads a raw video to an S3 bucket (MP4, MOV, etc.).
* S3 publishes an ObjectCreated event to an SNS topic (video-uploaded).
* SNS fans out the notification to two SQS queues:
  * video-processing — consumed by a Lambda that transcodes the video (e.g., to HLS) and writes outputs to processed-videos.
  * thumbnail-processing — consumed by a Lambda that generates thumbnails and writes outputs to thumbnails.

<Frame>
  <img alt="A simple AWS video-processing diagram showing a user uploading raw videos to a storage bucket, which sends new-video messages to queues that trigger Lambda functions. Those functions create processed videos and thumbnails saved to separate storage buckets." />
</Frame>

Quick reference table — resources and purpose:

|   Resource type | Purpose                         | Example name(s)                        |
| --------------: | ------------------------------- | -------------------------------------- |
|       S3 bucket | Store raw uploads               | raw-videos-kodekloud                   |
|       SNS topic | Fan-out notification            | video-uploaded                         |
|       SQS queue | Durable queue for each consumer | video-processing, thumbnail-processing |
| Lambda function | Process messages from SQS       | video-processing, thumbnail-processing |

We’ll walk through the exact steps: buckets, SNS topic, SQS queues, subscribing queues to SNS, Lambda functions, event parsing, S3 notification wiring, testing, and cleanup.

Buckets

* Create three S3 buckets (you can use default settings for this demo):
  * raw-videos-kodekloud (incoming uploads)
  * processed-videos-kodekloud (transcoded outputs, e.g., HLS files)
  * thumbnails-kodekloud (generated thumbnails)
* In production, consider encryption, lifecycle rules, and access policies.

<Frame>
  <img alt="A screenshot of the AWS S3 Management Console showing a list of five S3 buckets with their names, regions, access settings, and creation dates. A green banner at the top indicates a bucket (&#x22;thumbnails-kodekloud&#x22;) was successfully created." />
</Frame>

Create the SNS topic

* In the SNS console, create a topic named video-uploaded.
* Choose Standard (FIFO ordering is not required here).
* Keep encryption and access policy defaults for now. You will later add an explicit statement allowing S3 to publish to the topic when you configure S3 event notifications.

Default access policy snippet (trimmed to show structure). Keep the default policy and merge additional statements when needed:

```json theme={null}
{
  "Version": "2012-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__default_statement_ID",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "SNS:Publish",
        "SNS:RemovePermission",
        "SNS:SetTopicAttributes",
        "SNS:DeleteTopic"
      ],
      "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:topic-name"
    }
  ]
}
```

Create the SQS queues

* Create two standard SQS queues:
  * video-processing
  * thumbnail-processing
* Standard queues provide at-least-once delivery and are usually sufficient for this pipeline.
* Use default visibility timeout, message retention, and delivery delay unless your application requires adjustments.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the Amazon SQS &#x22;Create queue&#x22; page with the queue name set to &#x22;video-processing&#x22; and configurable fields like visibility timeout, delivery delay, message retention period, and maximum message size. The browser tabs and AWS footer/CloudShell bar are also visible." />
</Frame>

Subscribe the SQS queues to the SNS topic

* In the SNS topic, create subscriptions of type Amazon SQS for:
  * arn:aws:sqs:REGION:ACCOUNT\_ID:video-processing
  * arn:aws:sqs:REGION:ACCOUNT\_ID:thumbnail-processing
* After subscribing, every publish to video-uploaded will be delivered to both queues.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the Amazon SQS queue named &#x22;video-processing.&#x22; The page displays queue details (ARN, URL, encryption), SNS subscriptions, and action buttons like Edit, Delete, Purge, and Send and receive messages." />
</Frame>

Subscribe example (SNS topic ARN):

```text theme={null}
arn:aws:sns:us-east-1:841860927337:video-uploaded
```

Testing SNS → SQS end-to-end (manual publish)

* Use the SNS console's Publish message feature to verify subscriptions.
* Publish a message body containing the S3 bucket name and object key (JSON is recommended).

Example message body:

```json theme={null}
{
  "bucket": "raw-videos-kodekloud",
  "key": "b415c94e-de85-4f6a-949c-2eb2e93bf830"
}
```

* After publishing, both SQS queues should show the message(s) available for consumers.

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the Amazon SNS topic page for &#x22;video-uploaded.&#x22; A green banner reports a message was published successfully, and the page displays the topic ARN, details, and subscription controls." />
</Frame>

Publish another test message (example):

```json theme={null}
{
  "bucket": "raw-videos-kodekloud",
  "key": "b415c94e-de85-4f6a-949c-2eb2e93bf83sdfasdf0"
}
```

* Refresh the SQS console — you should see multiple messages in both queues.

<Frame>
  <img alt="A screenshot of the Amazon SQS console showing two queues named &#x22;thumbnail-processing&#x22; and &#x22;video-processing.&#x22; Each queue is of type Standard, created on 2023-10-11, with 2 messages available and 0 messages in flight." />
</Frame>

Create Lambda functions

* Create two Node.js 18.x Lambda functions:
  * video-processing
  * thumbnail-processing
* Create an IAM role (example: lambda-sqs-s3) and attach:
  * AWS managed policy that allows Lambda to poll SQS (AWSLambdaSQSQueueExecutionRole or similar).
  * S3 permissions (least privilege: GetObject/PutObject on the relevant buckets). For demos you might use AmazonS3FullAccess, but restrict in production.

<Frame>
  <img alt="A screenshot of the AWS Lambda &#x22;Create function&#x22; console showing the &#x22;Author from scratch&#x22; option and fields for Function name (filled with &#x22;myFunctionName&#x22;), Runtime set to Node.js 18.x, and Architecture x86_64. The page also shows options for using a blueprint or container image and sections for permissions and advanced settings." />
</Frame>

Attach S3 & SQS permissions to the Lambda role (example role creation UI shown):

<Frame>
  <img alt="A screenshot of the AWS Lambda &#x22;Create function&#x22; page showing a new IAM role named &#x22;lambda-sqs-s3&#x22; with the &#x22;Amazon SQS poller permissions&#x22; policy selected. The lower section displays Advanced settings options (Enable Code signing, Enable function URL, Enable tags, Enable VPC)." />
</Frame>

Important: permissions and message structure

> **warning** S3 must be allowed to publish to your SNS topic when you configure S3 event notifications. Add an SNS topic policy statement that allows the s3.amazonaws.com principal to Publish from your bucket's ARN (we provide an example policy later). Without this, S3 event notifications to SNS will fail.

Inspecting the SQS-triggered Lambda event

* When Lambda polls SQS, the invoked event contains event.Records — an array of SQS records.
* Because SNS delivered to SQS, each SQS record's body is a stringified SNS notification. To get your original payload you typically parse twice:
  1. JSON.parse(event.Records\[i].body) → SNS notification object
  2. JSON.parse(parsed.Message) → your original message object

Example Lambda that prints the raw event (useful for debugging):

```javascript theme={null}
export const handler = async (event) => {
  console.log(JSON.stringify(event, null, 2));
  return {
    statusCode: 200,
    body: JSON.stringify('OK'),
  };
};
```

Extracting the actual message in Node.js (batch-friendly pattern):

```javascript theme={null}
export const handler = async (event) => {
  // Handle multiple records if batchSize > 1
  for (const record of event.Records) {
    // SQS record body is an SNS notification (string)
    const snsNotification = JSON.parse(record.body);
    // The SNS notification has a Message field (string), which is the JSON we originally published
    const message = JSON.parse(snsNotification.Message);
    console.log('Parsed message:', message);
    // message.bucket and message.key are now accessible
  }

  return { statusCode: 200, body: 'Processed' };
};
```

Lambda event source mapping: batch size and maximum batching window

* Configure the SQS trigger on your Lambda with:
  * Batch size — max messages delivered per invocation (tune for cost/throughput).
  * Maximum batching window — how long Lambda waits to fill a batch before invoking.
* Larger batch sizes improve cost efficiency but require your handler to iterate records and handle partial failures correctly.

<Frame>
  <img alt="A screenshot of the AWS Lambda console showing the &#x22;Add trigger&#x22; panel for an SQS event source. Visible options include &#x22;Activate trigger&#x22;, Batch size (set to 10), Batch window, Maximum concurrency, filter criteria, and Cancel/Add buttons." />
</Frame>

Viewing CloudWatch logs

* After Lambda runs, view CloudWatch Logs (Monitor → View logs). The logged event shows event.Records\[0].body as a stringified SNS notification with a Message property that contains your original JSON string.

Sample (abbreviated) structure from logs:

```text theme={null}
{
  "Records": [
    {
      "messageId": "...",
      "body": "{\n  \"Type\": \"Notification\", ... , \"Message\": \"{\\n  \\\"bucket\\\": \\\"raw-videos-kodekloud\\\", \\n  \\\"key\\\": \\\"b415c94e-...\\\"}\\n\" ... }",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:ACCOUNT_ID:video-processing",
      "awsRegion": "us-east-1"
    }
  ]
}
```

Video-processing Lambda (skeleton)

* The heavy lifting (ffmpeg, HLS packaging) is out-of-scope for this article, but the following skeleton shows correct message parsing and S3 GetObject usage with AWS SDK v3:

```javascript theme={null}
// video-processing Lambda (Node.js 18.x)
import fs from "fs";
import { S3Client, GetObjectCommand, PutObjectCommand } from "@aws-sdk/client-s3";

export const handler = async (event) => {
  const s3 = new S3Client({});

  // Process each SQS record (batching-friendly)
  for (const record of event.Records) {
    const snsNotification = JSON.parse(record.body);
    const message = JSON.parse(snsNotification.Message);
    console.log("Message:", message);

    const getCmd = new GetObjectCommand({
      Bucket: message.bucket,
      Key: message.key,
    });

    try {
      const resp = await s3.send(getCmd);
      // resp.Body is a stream. You would pipe or buffer it and then run ffmpeg to transcode.
      // The implementation of ffmpeg processing and uploading output files is omitted here.
      console.log(`Successfully retrieved ${message.key} from ${message.bucket}`);
    } catch (err) {
      console.error("Error retrieving object from S3:", err);
      throw err; // Let Lambda/SQS retry or dead-letter depending on configuration
    }
  }

  return { statusCode: 200, body: "Processed" };
};
```

* Typical production steps in the video Lambda:
  * Stream the object to /tmp or buffer it,
  * Run ffmpeg to transcode to HLS (.m3u8 + .ts segments),
  * Upload outputs to processed-videos-kodekloud with PutObjectCommand,
  * Remove temporary files to free /tmp.

Final packaging note

> **lightbulb** ffmpeg is not included in Lambda by default. To run ffmpeg you can either use a Lambda Layer containing a static ffmpeg binary or deploy a container-based Lambda with ffmpeg baked into the image. Choose the approach that best fits build and deployment workflows.

Thumbnail Lambda

* Create thumbnail-processing Lambda, reuse the same IAM role (SQS poller + S3 permissions).
* Use batch size = 1 for simpler thumbnail extraction (one message one invocation is easier to manage).

<Frame>
  <img alt="A screenshot of the AWS Lambda &#x22;Add trigger&#x22; page showing the Trigger configuration panel, with &#x22;sqs&#x22; typed into the source search and the SQS trigger option displayed. The page includes Cancel and Add buttons and the AWS console header." />
</Frame>

Thumbnail handler skeleton (Node.js):

```javascript theme={null}
// thumbnail-processing Lambda (Node.js 18.x)
import { S3Client, GetObjectCommand, PutObjectCommand } from "@aws-sdk/client-s3";

export const handler = async (event) => {
  const s3 = new S3Client({});

  for (const record of event.Records) {
    const snsNotification = JSON.parse(record.body);
    const message = JSON.parse(snsNotification.Message);
    console.log("Thumbnail message:", message);

    const getCmd = new GetObjectCommand({
      Bucket: message.bucket,
      Key: message.key,
    });

    try {
      const resp = await s3.send(getCmd);
      // Extract a frame and upload to thumbnails bucket (ffmpeg or image processing).
      // Upload thumbnail(s) with PutObjectCommand to thumbnails-kodekloud.
    } catch (err) {
      console.error("Error in thumbnail Lambda:", err);
      throw err;
    }
  }

  return { statusCode: 200, body: "Thumbnails generated" };
};
```

Configure S3 to publish events to SNS

* You can configure S3 to send ObjectCreated:\* events to the SNS topic so that uploads automatically trigger the pipeline.
* In the raw-videos-kodekloud bucket:
  * Properties → Event notifications → Create event notification
  * Event types: ObjectCreated (All object create events)
  * Destination: SNS topic → video-uploaded

<Frame>
  <img alt="A screenshot of the Amazon S3 Management Console showing a list of five S3 buckets (including names like processed-videos-kodekloud and thumbnails-kodekloud) with columns for region, access, and creation date. A green banner at the top confirms the bucket &#x22;thumbnails-kodekloud&#x22; was successfully created." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;Create event notification&#x22; page with General configuration fields filled (Event name &#x22;video-uploaded&#x22;, Prefix &#x22;images/&#x22;, Suffix &#x22;.jpg&#x22;) and the Event types section below. The page is in a web browser with multiple tabs visible along the top." />
</Frame>

S3 → SNS permission: example topic policy statement

* Add this statement to the SNS topic's access policy (Topics → select topic → Edit → Access policy). Replace the ARNs and account IDs with your values:

```json theme={null}
{
  "Sid": "AllowS3Publish",
  "Effect": "Allow",
  "Principal": {
    "Service": "s3.amazonaws.com"
  },
  "Action": [
    "SNS:Publish"
  ],
  "Resource": "arn:aws:sns:us-east-1:841860927337:video-uploaded",
  "Condition": {
    "ArnLike": {
      "aws:SourceArn": "arn:aws:s3:::raw-videos-kodekloud"
    },
    "StringEquals": {
      "aws:SourceAccount": "841860927337"
    }
  }
}
```

* Merge this statement into the existing policy's Statement array and save.
* Then configure the S3 event notification to use the topic.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;Destination&#x22; section for configuring event notifications, with options to choose a Lambda function, SNS topic, or SQS queue and a notice about granting S3 permissions. The top of the page also shows lifecycle/intelligent-tiering event options." />
</Frame>

Testing the full flow by uploading a video

* Upload a sample video to raw-videos-kodekloud (console, SDK, or CLI).
* The expected sequence:
  1. S3 emits ObjectCreated → SNS topic.
  2. SNS fans out to both SQS queues.
  3. Lambda functions (configured with SQS triggers) are invoked to process the file.
  4. Processed outputs are written to processed-videos-kodekloud and thumbnails-kodekloud.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing a list of five S3 buckets. The table displays each bucket's name, AWS region, access settings, and creation date." />
</Frame>

Upload succeeded example:

<Frame>
  <img alt="A screenshot of the AWS S3 console showing an &#x22;Upload succeeded&#x22; status with a summary that 1 file (video.mp4, 38.2 MB) was uploaded to the bucket s3://raw-videos-kodekloud. The file list below shows the upload succeeded with no errors." />
</Frame>

Verify processed output

* Check the processed-videos-kodekloud bucket for HLS outputs (.m3u8 playlist and .ts segments).
* Check thumbnails-kodekloud for generated thumbnails.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing a bucket folder with three objects: output.m3u8 and two .ts video segment files, along with their sizes and last-modified timestamps." />
</Frame>

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing a folder with three images (thumbnails) created from a processed video, displayed with their sizes and last-modified timestamps." />
</Frame>

* The screenshots above illustrate expected outputs after successful Lambda execution.

Cleanup

* To avoid charges after testing, delete resources you created:
  * Delete SQS queues.
  * Delete SNS topic.
  * Delete Lambda functions.
  * Empty and delete S3 buckets (note: emptying may be required before deletion).

<Frame>
  <img alt="A screenshot of the AWS Management Console showing the Amazon SQS &#x22;Queues&#x22; page with two queues listed: &#x22;thumbnail-processing&#x22; and &#x22;video-processing&#x22; (both Standard). Both queues show zero messages and use Amazon SQS key (SSE-SQS) encryption." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS Lambda Functions page showing two functions, &#x22;video-processing&#x22; and &#x22;thumbnail-processing&#x22;, both packaged as Zip and running Node.js 18.x. The table also shows last-modified times (20 minutes and 18 minutes ago) and UI controls like Create function and Actions." />
</Frame>

Emptying and deleting a bucket (confirm dialog):

<Frame>
  <img alt="Screenshot of the AWS S3 console showing the &#x22;Empty bucket&#x22; confirmation for bucket &#x22;processed-videos-kodekloud&#x22;, with a textbox where the user must type &#x22;permanently delete&#x22; to confirm. The page includes warnings that emptying the bucket deletes all objects and cannot be undone." />
</Frame>

Delete bucket confirmation:

<Frame>
  <img alt="A screenshot of the AWS S3 console showing a &#x22;Delete bucket&#x22; confirmation for the bucket named &#x22;thumbnails-kodekloud.&#x22; It displays warnings that deletion cannot be undone and a text field to enter the bucket name to confirm deletion." />
</Frame>

Summary

* This guide demonstrated how to wire S3 → SNS → SQS → Lambda to implement a fan-out processing pipeline for uploaded videos. Key takeaways:
  * Use SNS to fan-out a single S3 event to multiple consumers via SQS.
  * S3 event notifications can publish directly to SNS; ensure SNS topic policies allow S3 to Publish.
  * When SNS publishes to SQS, Lambda receives SQS records whose body contains an SNS notification string — JSON.parse twice to retrieve the original payload.
  * Tune SQS batch size and batching window on Lambda triggers for cost and throughput trade-offs.
  * For ffmpeg in Lambda, use a Layer or container-based Lambda.

Further reading and references

* [Amazon S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)
* [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
* [Amazon SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
* [AWS Lambda event source mapping for SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html)
* [AWS SDK for JavaScript v3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/index.html)
* [FFmpeg](https://ffmpeg.org/) — packaging options for Lambda: layer vs container

> **lightbulb** When SNS publishes to SQS, the Lambda handler sees an SQS record whose body contains an SNS notification as a string. You must JSON.parse the SQS record body to get the SNS notification, then JSON.parse the notification.Message to get your original payload.

That completes this lesson on integrating SNS and SQS for a serverless video-processing pipeline.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/311ec21b-57a6-4d8e-a22d-8554b565f3a6)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/68a80d2a-9ede-43f1-a18e-84e7efe89dc6/lesson/8e8bc71b-9b8d-4741-b365-b4f2fc18b9d7)
