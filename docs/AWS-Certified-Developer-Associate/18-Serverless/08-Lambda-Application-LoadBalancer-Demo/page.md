# Lambda Application LoadBalancer Demo

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Serverless/Lambda-Application-LoadBalancer-Demo/page

Learn to integrate an Application Load Balancer with an AWS Lambda function for processing requests and returning responses.

In this lesson, you'll learn how to integrate an Application Load Balancer with an [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda) function. The load balancer distributes incoming requests to your Lambda function, which processes the requests and returns appropriate responses.

***

## Creating the Lambda Function

Begin by creating a simple Lambda function using the Node.js runtime from the [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda) console. For this demo, we are naming the function "my app" (the exact name is not critical). This function logs the incoming event and returns a response with a status code of 200 along with a message.

<Frame>
  ![The image shows the AWS Lambda console where a new function is being created. It includes options for setting the function name, runtime, architecture, and permissions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859476/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-lambda-function-creation-console.jpg)
</Frame>

Enter the following code for your Lambda function:

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

Deploy your changes. Once the deployment is successful, your Lambda function will log the event and return the message. You can verify the update in the AWS Lambda console.

<Frame>
  <img alt="The image shows an AWS Lambda console with a function named &#x22;myAPP&#x22; successfully updated. It includes options for adding triggers and destinations, and displays code source details at the bottom." />
</Frame>

***

## Creating the Application Load Balancer

Next, set up the Application Load Balancer that will forward requests to your Lambda function. In the AWS Management Console, navigate to the Load Balancer service and choose to create a new Application Load Balancer.

<Frame>
  ![The image shows a webpage from the AWS Management Console for creating an Application Load Balancer, with options for basic configuration such as load balancer name, scheme, and IP address type.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859478/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-application-load-balancer-console.jpg)
</Frame>

Configure the following settings:

* Name your load balancer (e.g., "Lambda LB").
* Set the scheme to **internet-facing**.
* Use **IPv4**.
* Select your desired VPC (the default VPC is acceptable).
* Choose a security group that allows web traffic on port 80 (or port 443 for HTTPS).

<Frame>
  ![The image shows an AWS console interface for configuring an application load balancer, including settings for security groups and listener routing.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859479/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-console-application-load-balancer.jpg)
</Frame>

***

## Configuring Listeners and Target Group

Set up the listeners for your load balancer. For a web application, create a listener on port 80 (and port 443 if using HTTPS). When configuring the target group:

1. Select **Lambda function** as the target type.
2. Name the target group (e.g., "my app Lambda").
3. Choose your Lambda function directly or register it by entering its ARN.
4. Keep the version as "latest" and create the target group.

<Frame>
  ![The image shows an AWS console screen where a user is configuring a target group for a Lambda function, with options for load balancing and health checks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859480/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-console-target-group-lambda.jpg)
</Frame>

After registering your target, return to the load balancer configuration and refresh the view. Your target group ("my app Lambda") should now be visible. Proceed to create the load balancer.

<Frame>
  <img alt="The image shows an AWS console interface for registering targets in a target group, specifically selecting a Lambda function named &#x22;myAPP.&#x22;" />
</Frame>

Review the summary of your settings:

<Frame>
  ![The image shows an AWS console page for creating an application load balancer, displaying configuration details such as security groups, network mapping, and listeners.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859482/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-console-application-load-balancer-2.jpg)
</Frame>

Click **Create Load Balancer** and allow a few minutes for initialization. You can verify the load balancer's provision by checking its DNS entry in the [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) console.

<Frame>
  ![The image shows an AWS EC2 console page displaying details of an active application load balancer named "lambda-lb," including its status, VPC, and availability zones.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859484/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-ec2-application-load-balancer.jpg)
</Frame>

***

## Testing the Integration and Correcting the Content Type

Open your browser and paste the DNS entry of the load balancer. Initially, you might find that your browser downloads a file instead of displaying the response properly. This occurs because the Lambda function response omits the Content-Type header.

When you open the downloaded file in a text editor, you'll see "Hello from Lambda". To resolve this, update your Lambda function to include a Content-Type header in the response. Choose one of the following formats based on your content type:

For an API (JSON response):

```javascript theme={null}
export const handler = async (event) => {
    console.log(event);
    const response = {
        statusCode: 200,
        body: 'Hello from Lambda!',
        headers: {
            "Content-Type": "application/json"
        },
    };
    return response;
};
```

Or for HTML content:

```javascript theme={null}
export const handler = async (event) => {
    console.log(event);
    const response = {
        statusCode: 200,
        body: '<h1>Hello from Lambda!</h1>',
        headers: {
            "Content-Type": "text/html"
        },
    };
    return response;
};
```

Deploy the updated code. Now, when you access the DNS entry, the load balancer forwards the request to Lambda, and you will see the response rendered properly in your browser.

<Callout icon="lightbulb">
  When using an API, the browser will display the JSON response directly:

  Hello from Lambda!
</Callout>

***

## Understanding the Event Object

When the Application Load Balancer invokes your Lambda function, it passes an event object structured as shown below:

```json theme={null}
{
  "requestContext": {
    "elb": {
      "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/lambda-279XGDqGZ5srHC2Fjr/49e9d65c45c"
    }
  },
  "httpMethod": "GET",
  "path": "/lambda",
  "queryStringParameters": {
    "query": "1234ABCD"
  },
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip",
    "accept-language": "en-US,en;q=0.9",
    "connection": "keep-alive",
    "host": "lambda-alb-123578498.us-east-1.elb.amazonaws.com",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "x-amzn-trace-id": "Root=1-5c536348-3d683b83744fae56f1676096",
    "x-forwarded-for": "72.12.164.125",
    "x-forwarded-port": "80",
    "x-forwarded-proto": "http",
    "x-ingress": "20"
  },
  "body": {}
}
```

Your Lambda function logs this event, and you can inspect the details in CloudWatch Logs.

<Frame>
  ![The image shows an AWS CloudWatch interface displaying log details for a Lambda function, including request context, HTTP method, headers, and other metadata.](../../../../images/kodekloud.com/kk-media/image/upload/v1752859485/notes-assets/images/AWS-Certified-Developer-Associate-Lambda-Application-LoadBalancer-Demo/aws-cloudwatch-lambda-logs-interface.jpg)
</Frame>

To view these logs, navigate to the "Monitor" tab of your Lambda function's page and open CloudWatch Logs. Here, you'll find information such as the HTTP method, path, query string parameters, and headers.

***

## Summary

In this lesson, you successfully set up an Application Load Balancer to route client requests on port 80 to an AWS Lambda function. You learned how to create a Lambda function, configure a load balancer along with its listener and target group, and properly format the Lambda response by including the Content-Type header. Finally, you examined the structure of the event object passed to your Lambda function via CloudWatch Logs. This integration provides a scalable and cost-effective strategy for building modern applications using AWS Lambda behind an Application Load Balancer.

Happy deploying!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/3c842ffc-5841-456d-9fad-7bb3af5fdbfc/lesson/1c71fd54-394d-4a0e-8b92-a5649d9f2a98" />
</CardGroup>
