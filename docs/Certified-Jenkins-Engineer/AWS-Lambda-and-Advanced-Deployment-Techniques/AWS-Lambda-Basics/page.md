# AWS Lambda Basics

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/AWS-Lambda-and-Advanced-Deployment-Techniques/AWS-Lambda-Basics/page

Learn how AWS Lambda enables code execution without server management, ideal for event-driven architectures with automatic scaling and pay-per-use pricing.

In this lesson, you’ll learn how AWS Lambda empowers you to run code without provisioning or managing servers. Ideal for event-driven architectures, Lambda automatically scales your functions and charges you only for actual compute time.

## What Is AWS Lambda?

Imagine a clever inventor who wrote a program to spark fire by rubbing sticks together. In the old world, he’d wait days for a server to be built, provisioned, and maintained—delaying his warmth and dinner. AWS Lambda changes that:

* You simply upload your code as a “Lambda function.”
* Lambda takes care of the infrastructure, scaling from zero to thousands of concurrent executions.
* You pay **only** for the milliseconds your code runs.

<Callout icon="lightbulb">
  AWS Lambda is a Functions-as-a-Service (FaaS) offering. It abstracts away servers, operating systems, and scaling concerns so you can focus entirely on your application logic.
</Callout>

<Frame>
  ![The image explains AWS Lambda as a serverless compute service, featuring the Lambda logo and icons representing server management, tools, and time efficiency.](https://kodekloud.com/kk-media/image/upload/v1752870252/notes-assets/images/Certified-Jenkins-Engineer-AWS-Lambda-Basics/aws-lambda-serverless-compute-diagram.jpg)
</Frame>

## Key Benefits of AWS Lambda

| Feature                    | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| Serverless Management      | No servers to provision, patch, or maintain                       |
| Automatic Scaling          | Instantly scales based on incoming requests                       |
| Pay-per-Use Pricing        | Billed in 100 ms increments for only the compute time you consume |
| Built-in High Availability | Fault-tolerant across multiple Availability Zones                 |
| Integrated Security        | IAM-based permissions and VPC integrations out of the box         |

## Supported Languages and Runtimes

AWS Lambda natively supports these runtimes:

| Runtime                    | Common Use Cases                     |
| -------------------------- | ------------------------------------ |
| Node.js (12.x, 14.x, 16.x) | APIs, microservices                  |
| Python (3.7, 3.8, 3.9)     | Data processing, machine learning    |
| Java (8, 11)               | Enterprise applications              |
| C# (.NET Core 3.1, .NET 5) | Windows workflows, back-end services |
| Go (1.x)                   | High-performance microservices       |
| Ruby (2.7)                 | Web applications                     |
| PowerShell (6.x)           | Automation and scripting             |

If you need a different language or version, use the [Lambda Runtime API](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html) to bring your own runtime. AWS even demonstrates running legacy COBOL applications on Lambda via custom runtimes.

<Frame>
  ![The image shows the AWS Lambda logo surrounded by icons representing supported programming languages: Python, Java, C#, Node.js, Ruby, Go, and PowerShell.](https://kodekloud.com/kk-media/image/upload/v1752870253/notes-assets/images/Certified-Jenkins-Engineer-AWS-Lambda-Basics/aws-lambda-programming-languages-icons.jpg)
</Frame>

<Callout icon="triangle-alert">
  Lambda functions can experience **cold starts**, especially in VPCs or when using large deployment packages. Design for stateless, short-duration handlers to minimize latency.
</Callout>

## About This Course

In this hands-on module, we will:

1. Create and configure a **Node.js** Lambda function.
2. Set up a **Jenkins** pipeline to deploy and invoke the Lambda.
3. Monitor performance using **CloudWatch** logs and metrics.

If you’d like to deepen your Lambda expertise, check out [Matthew’s AWS Lambda course on KodeKloud](https://kodekloud.com/courses/aws-lambda).

## Further Reading

* [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* [Serverless Framework](https://www.serverless.com/)
* [AWS Well-Architected Serverless Lens](https://aws.amazon.com/architecture/well-architected/?wa-lens-whitepapers-sort-by=item.additionalFields.sortDate\&wa-lens-whitepapers-sort-order=desc\&serverless-lens)

Thank you for learning AWS Lambda with us!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7e65cc00-b745-498e-8351-c294cbe958ec/lesson/4d248814-17e2-4c22-90b0-64343d944b9c" />
</CardGroup>
