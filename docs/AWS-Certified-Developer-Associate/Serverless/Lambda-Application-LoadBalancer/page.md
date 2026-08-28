# Lambda Application LoadBalancer

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Serverless/Lambda-Application-LoadBalancer/page

This article explains how to integrate AWS Lambda with an Elastic Load Balancer for improved application scalability and performance.

In this lesson, we explore how to integrate [AWS Lambda](https://learn.kodekloud.com/user/courses/aws-lambda) with an Elastic Load Balancer. This integration enables the load balancer to invoke AWS Lambda functions based on specific HTTP requests, enhancing your application's scalability and performance.

## How It Works

When a user sends a request from the internet, it first reaches the load balancer. The load balancer uses listeners configured with rules that examine various HTTP request properties (such as URL paths or domains) to decide how to route the request. When a listener rule matches the incoming request, the load balancer forwards the request to a target group. In this integration, the target group is associated with AWS Lambda functions.

The load balancer converts the incoming HTTP request into a JSON payload with properties including the HTTP method, path, headers, and body. Below is an example JSON representation for an incoming HTTP request:

```json theme={null}
{
  "httpMethod": "GET",
  "path": "/example",
  "headers": { ... },
  "body": "encoded",
  "isBase64Encoded": false
}
```

The AWS Lambda function processes this JSON payload and returns a JSON-formatted response. The load balancer then transforms this JSON response back into a standard HTTP response. An example AWS Lambda response is shown below:

```json theme={null}
{
  "statusCode": 200,
  "statusDescription": "200 OK",
  "headers": { ... },
  "body": "Hello from Lambda!",
  "isBase64Encoded": false
}
```

<Callout icon="lightbulb">
  The conversion mechanism ensures that the AWS Lambda function’s output—comprising the status code, status description, headers, and body—is correctly transformed into a standard HTTP response for the end user.
</Callout>

## Handling Multi-Header Values

When a request includes duplicate query parameters or headers (for example, the query parameter "color" with both "blue" and "green"), the load balancer transforms them into an array. Consider the following JSON representation:

```json theme={null}
{
  "queryStringParameters": {
    "color": ["blue", "green"]
  },
  "headers": {
    "Accept": ["text/plain", "text/html"]
  }
}
```

When multi-header values are enabled, the load balancer forwards these values as arrays to the AWS Lambda function. This behavior is critical to understand while configuring and testing your AWS Lambda integrations with an Elastic Load Balancer.

## Summary

By understanding the process—converting HTTP requests to JSON payloads for AWS Lambda and managing multi-header values—you can effectively integrate and troubleshoot AWS Lambda functions behind an Elastic Load Balancer. For additional details and further reading, check out the [AWS Lambda documentation](https://learn.kodekloud.com/user/courses/aws-lambda).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/3c842ffc-5841-456d-9fad-7bb3af5fdbfc/lesson/9e542e05-5a26-4014-af9c-21a2d97b0c8c" />
</CardGroup>
