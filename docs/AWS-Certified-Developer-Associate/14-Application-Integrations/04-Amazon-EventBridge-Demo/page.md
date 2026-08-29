# Amazon EventBridge Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Application-Integrations/Amazon-EventBridge-Demo/page

This guide explores using AWS EventBridge to build event-driven architectures with EC2 instance events and custom application events.

In this guide, we'll explore how to work with AWS EventBridge to build event-driven architectures. You will learn how to generate events triggered by changes to your AWS resources—specifically when EC2 instance statuses change—and how to use these events to invoke Lambda functions. Additionally, we’ll demonstrate how to create and send custom events from your application code.

***

## Using the Default Event Bus and Creating Rules

Every AWS account starts with a default EventBridge event bus. You can send events to this default bus or create custom event buses as required. For the purpose of this demo, we will use the default event bus.

Navigate to the Event Buses section in the EventBridge console. You will see a display similar to the image below, featuring the default event bus along with the option to create a custom bus if needed.

<Frame>
  ![The image shows the Amazon EventBridge console, displaying options for managing event buses, including a default event bus and the ability to create custom event buses.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858384/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/amazon-eventbridge-console-event-buses.jpg)
</Frame>

Proceed to the Rules section where you define which events will trigger specific actions. Click on **Create Rule**. You will be prompted to choose an event bus for the rule; here, select the default event bus.

Assign a meaningful name (for example, "instance-status-change") and provide a description. You have the option to trigger the rule either by an event pattern or on a scheduled basis (similar to a cron job). For this demo, choose the event pattern option.

<Frame>
  ![The image shows an AWS EventBridge console screen where a user is defining rule details for an event, including fields for name, description, and event bus selection.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858385/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/aws-eventbridge-rule-details-console.jpg)
</Frame>

***

### Configuring an Event Pattern for EC2 Instance Changes

Follow these steps to configure your rule to capture EC2 instance events:

1. Choose **AWS services** as the event source and select **EC2**.
2. Under event types, select **EC2 Instance State-change Notification**.
3. For simplicity, this demo captures any state change. (You can further tailor the event pattern by specifying states such as "running", "stopped", "terminated", or "shutting-down".)

The basic event pattern is as follows:

```json theme={null}
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"]
}
```

If you prefer to filter for a specific state change (for example, when an instance is shutting down), modify the event pattern like this:

```json theme={null}
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["shutting-down"]
  }
}
```

After confirming your event pattern, designate the target for the rule. In this demo, the target is a Lambda function that logs the event details. Below is a sample Lambda function code:

```javascript theme={null}
export const handler = async (event) => {
    console.log(event);
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda'),
    };
    return response;
};
```

<Frame>
  ![The image shows an AWS EventBridge console screen where a user is selecting targets for a rule, with options to choose target types and configure settings for a Lambda function.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858386/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/aws-eventbridge-console-targets-lambda.jpg)
</Frame>

After selecting your target (for example, a Lambda function named "test one"), complete the tagging and review steps, then click **Create rule**. Your EventBridge rule is now active.

***

## Testing the EC2 Instance Rule

To test the configured rule, access the EC2 console and select a running instance. Change its state (for example, stop the instance) to trigger the event.

Once the instance status changes, EventBridge emits an event that invokes the Lambda function. Check the CloudWatch logs of the Lambda function to confirm that the event has been received. A typical log entry might include details such as the source ("aws.ec2"), detail type ("EC2 Instance State-change Notification"), and the state of the instance.

<Frame>
  ![The image shows the Amazon EventBridge console with a rule named "instance-status-change" that is enabled. The interface includes options for managing event buses and rules.](../../../../images/kodekloud.com/kk-media/image/upload/v1752858387/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/amazon-eventbridge-instance-status-rule.jpg)
</Frame>

A sample log output might look like:

```json theme={null}
{
  "id": "79688aec-7218-794f-df39d9af2d40",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "account": "841860292737",
  "time": "2023-10-12T03:40:40Z",
  "region": "us-east-1",
  "resources": ["arn:aws:ec2:us-east-1:841860292737:instance/i-0dbc8ce8bd81ca2c"],
  "detail": {
    "instance-id": "i-0dbc8ce8bd81ca2c",
    "state": "stopped"
  }
}
```

***

## Creating and Testing a Custom Event

Apart from AWS-generated events, you can create custom events from your own application code. This demo includes an Express.js-based Node.js API that sends a custom event when a new user signs up.

### API Code for Custom Event Generation

The code below demonstrates how to set up an Express.js API that triggers an event at the `/signup` endpoint. It utilizes the AWS SDK's EventBridge client to post the custom event:

```javascript theme={null}
require("dotenv").config();
const express = require("express");
const { EventBridgeClient, PutEventsCommand } = require("@aws-sdk/client-eventbridge");

const app = express();
app.use(express.json());

const client = new EventBridgeClient();

app.post("/signup", async (req, res) => {
    const { username } = req.body;

    const event = {
        Source: "my-app",
        DetailType: "New User",
        Detail: JSON.stringify({ user: username }),
    };

    try {
        const response = await client.send(
            new PutEventsCommand({
                Entries: [event],
            })
        );
        console.log(response);
        res.status(201).json({ status: "success" });
    } catch (error) {
        console.error(error);
        res.status(500).json({ status: "error" });
    }
});

app.listen(3000, () => {
    console.log("API is running on port 3000");
});
```

This API accepts POST requests containing a JSON payload (e.g., `{ "username": "user1" }`) and sends a custom event to EventBridge with the source "my-app" and detail type "New User".

### Configuring an EventBridge Rule for the Custom Event

Return to the EventBridge console and create a new rule tailored for your custom event. Instead of an AWS provided event pattern, select **Custom pattern** and paste the following JSON:

```json theme={null}
{
  "source": ["my-app"],
  "detail-type": ["New User"]
}
```

Choose the target for this rule (for example, a Lambda function named "test two") and complete the rule creation.

<Frame>
  ![The image shows an AWS EventBridge console screen where a user is selecting targets for a rule, with options to choose an EventBridge event bus, API destination, or AWS service. The selected target is a Lambda function named "test2."](../../../../images/kodekloud.com/kk-media/image/upload/v1752858388/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/aws-eventbridge-targets-lambda-test2.jpg)
</Frame>

After the rule is set up, test the event directly from the Event Bus by clicking **Send event**. Enter the source ("my-app"), detail type ("New User"), and additional event details as shown in the example:

```json theme={null}
{
  "username": "user1"
}
```

Verify the event reception by inspecting the logs of the Lambda function "test two". An example log entry might be:

```json theme={null}
{
  "version": "0",
  "id": "apafe6fb-cb37-ef59-e34c069f7268",
  "detail-type": "New User",
  "source": "my-app",
  "account": "841802997373",
  "time": "2023-10-12T03:47:59Z",
  "region": "us-east-1",
  "resources": [],
  "detail": {
    "username": "user1"
  }
}
```

<Frame>
  ![The image shows the Amazon EventBridge interface with a focus on the "Rules" section, displaying two enabled rules named "instance-status-change" and "my-api."](../../../../images/kodekloud.com/kk-media/image/upload/v1752858389/notes-assets/images/AWS-Certified-Developer-Associate-Amazon-EventBridge-Demo/amazon-eventbridge-rules-interface.jpg)
</Frame>

### End-to-End Custom Event Test

Test your API by sending a POST request to the `/signup` endpoint with a JSON payload, for example:

```json theme={null}
{
  "username": "user2",
  "password": "password123"
}
```

You should receive a successful JSON response like:

```json theme={null}
{
  "status": "success"
}
```

After a short delay, check the Lambda logs to confirm the receipt of the event. A sample log output for the custom event might be:

```json theme={null}
{
  "version": "0",
  "id": "a9ae6fb8-cbe8-3bf9-e34c069f7268",
  "detail-type": "New User",
  "source": "my-app",
  "account": "841608927337",
  "time": "2023-10-13T03:47:59Z",
  "region": "us-east-1",
  "resources": [],
  "detail": { "username": "user2" }
}
```

<Callout icon="lightbulb">
  Always verify your EventBridge and Lambda configurations using CloudWatch logs to ensure events are being processed as expected.
</Callout>

***

## Conclusion

This tutorial has walked you through configuring AWS EventBridge to trigger Lambda functions based on both AWS-generated events—like EC2 instance state changes—and custom events generated by your applications. By leveraging EventBridge rules and custom event patterns, you can seamlessly integrate AWS services with your own applications to create scalable, event-driven architectures.

Happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/60c267ab-da8b-4408-97f4-b53aad3f4479/lesson/b69ad83f-54d5-4c44-a4b2-85b182afcc43" />
</CardGroup>
