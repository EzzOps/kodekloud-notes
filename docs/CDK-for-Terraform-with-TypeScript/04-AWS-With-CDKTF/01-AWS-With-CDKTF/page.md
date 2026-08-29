# AWS With CDKTF

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/AWS-With-CDKTF/AWS-With-CDKTF/page

Tutorial for automating AWS Lambda and API Gateway deployment with CDK for Terraform in TypeScript for a NamePicker sample app.

Welcome back.

In the previous module we used the Terraform local provider to build a simple app. In this lesson we'll use the AWS provider with CDK for Terraform (CDKTF) to deploy resources into Amazon Web Services and manage them as code.

What you'll learn

* Define the problem that informs the sample app we’ll build.
* Review prerequisites and the essential tools for deploying to AWS.
* Demonstrate a manual (console) deployment to show the moving parts.
* Recreate the same setup with CDKTF (TypeScript) for repeatable, version-controlled deployments.

Use case summary — the NamePicker app
Arthur needs a small service to decide who does the washing up each night. The NamePicker app exposes a simple HTTP endpoint. A client calls API Gateway, which invokes a Lambda function. The Lambda returns a randomly selected family member (either a pure random pick or a shuffled sequential draw so names don’t repeat until the list is exhausted).

High-level architecture:

<Frame>
  <img alt="A high-level architecture diagram showing an Author (client/developer) sending requests to an API Gateway which forwards them to an AWS Lambda function. Icons depict a person at a computer, a cloud/API gateway, and the AWS Lambda logo with arrows between them." />
</Frame>

Manual deployment (console demo)

The manual approach is useful to visualize the pieces before automating them with CDKTF. We’ll:

1. Create and deploy the AWS Lambda.
2. Create an API Gateway REST API that proxies requests to the Lambda.
3. Test the endpoint.

1) Create the Lambda function

* Open the AWS Lambda console and create a function (for example, `console-name-picker`) using Node.js 20 runtime.
* Paste your business logic (the NamePicker handler) into the Lambda function code and deploy.

Example NamePicker handler (Node.js). This simple implementation supports two modes:

* random pick from an array, or
* shuffled sequential draw (no repeats until list exhausted).

```javascript theme={null}
// lambda/index.js
let shuffledNames = [];
let currentIndex = 0;

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

exports.handler = async (event) => {
  console.log('Received event', event);

  const names = JSON.parse(process.env.NAMES || '["Arthur","Martin","Douglas","Carolyn"]');
  const shuffle = (process.env.SHUFFLE || 'false') === 'true';

  if (!shuffle) {
    // Return a random name
    const randomName = names[Math.floor(Math.random() * names.length)];
    return {
      statusCode: 200,
      body: JSON.stringify(randomName),
    };
  } else {
    // Maintain a shuffled list in memory so names are not repeated until list exhausted
    if (shuffledNames.length === 0 || currentIndex >= shuffledNames.length) {
      shuffledNames = shuffleArray([...names]);
      currentIndex = 0;
    }
    const nameToReturn = shuffledNames[currentIndex];
    currentIndex += 1;
    return {
      statusCode: 200,
      body: JSON.stringify(nameToReturn),
    };
  }
};
```

> **lightbulb** This implementation uses in-memory state (`shuffledNames` and `currentIndex`) inside the Lambda execution environment. That memory can persist between warm invocations but will be lost on cold starts or when the execution environment is replaced. For durable or shared state across invocations or multiple concurrent instances, store state externally (for example, DynamoDB, S3, or ElastiCache).

After deploying, you can test the function in the Lambda console. Example test output:

```json theme={null}
{
  "statusCode": 200,
  "body": "\"Douglas\""
}
```

Once deployed you should see the function in the Lambda console:

<Frame>
  <img alt="A screenshot of the AWS Lambda console showing the function &#x22;console-name-picker&#x22; with its overview diagram, ARN and execution status. A green banner at the top indicates the function was successfully updated." />
</Frame>

2. Create an API in API Gateway and connect it to the Lambda

* In API Gateway create a REST API (for example, `console-name`).
* Create the root resource and add a method such as `ANY`. Choose "Lambda Function" as the integration and enable Lambda proxy integration so the Lambda receives the full request data.
* Add a proxy resource (`/{proxy+}`) to route any path to the Lambda (so requests to `/hello`, `/goodbye`, etc. are all handled).
* Deploy the API to a stage (for example `dev`) and use the invoke URL.

When creating the API, choose Lambda function as the integration and enable Lambda proxy integration:

<Frame>
  <img alt="Screenshot of the AWS API Gateway &#x22;Create REST API&#x22; console showing the API details form. The &#x22;New API&#x22; option is selected, the API name field contains &#x22;console-name&#x22;, and a &#x22;Create API&#x22; button is visible." />
</Frame>

<Frame>
  <img alt="A screenshot of the AWS API Gateway &#x22;Method details&#x22; integration type panel showing options like Lambda function (selected), HTTP, Mock, AWS service, and VPC link. The lower area shows the Lambda proxy toggle and a dropdown to choose a Lambda function/region." />
</Frame>

Enable the proxy resource so the Lambda receives any URL path:

<Frame>
  <img alt="A screenshot of the AWS API Gateway console showing the &#x22;Create resource&#x22; page with a proxy resource enabled (resource path &#x22;/&#x22;, name &#x22;{proxy+}&#x22;) and CORS checked. A green banner at the top confirms a method was successfully created." />
</Frame>

After wiring the Lambda integration you may see an integration status message or warning while the console creates permissions and links:

<Frame>
  <img alt="A screenshot of the AWS API Gateway console showing the Resources page for an API with the /{proxy+} ANY method selected, displaying the method → integration flow and an &#x22;Undefined integration&#x22; warning. The left sidebar shows API navigation items and a green success banner appears at the top." />
</Frame>

Deploy the API:

<Frame>
  <img alt="A screenshot of the AWS API Gateway console showing a &#x22;Deploy API&#x22; dialog. The modal contains a Stage dropdown, a Deployment description text box, and Cancel and Deploy buttons." />
</Frame>

After deployment you receive an invoke URL (for example):
`https://0ik9wc8zpj.execute-api.us-east-1.amazonaws.com/dev`

Open that in a browser or call it with curl and you should receive a JSON response with a name on each request.

> **warning** Why the console approach is not ideal:

  * Manual steps are error-prone and hard to reproduce.
  * Not easily shareable or automatable across teams.
  * Difficult to version-control and review infrastructure changes.
    Use CDKTF to express this architecture as code so it can be committed, reviewed, and redeployed reliably.

Prerequisites

| Requirement                        | Notes / Example                                                                                                                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AWS account                        | Use your AWS account or a lab-provided account (e.g., KodeKloud Labs).                                                                                                        |
| AWS CLI (optional but recommended) | Install with Homebrew on macOS: `brew install awscli`                                                                                                                         |
| CDKTF and tooling                  | Install CDKTF, Node.js, and package manager (yarn or npm). See CDKTF docs: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf) |

Authenticate locally (if needed)

* Create an IAM user with programmatic access (access key + secret) or use an existing role.
* Configure credentials locally:

```bash theme={null}
aws configure
```

Verify the credentials being used:

```bash theme={null}
aws sts get-caller-identity
```

Example output:

```json theme={null}
{
  "UserId": "AIDA3FLDYW3LPP24HQHEN",
  "Account": "767397770966",
  "Arn": "arn:aws:iam::767397770966:user/kk_labs_user_335488"
}
```

If `get-caller-identity` returns your expected user or role, CDKTF (using the AWS provider) will pick up those credentials and deploy into that account.

Getting started with CDKTF and the AWS provider

Create a minimal TypeScript CDKTF app that configures the AWS provider and emits a Terraform output to validate the stack:

```typescript theme={null}
import { Construct } from 'constructs';
import { App, TerraformStack, TerraformOutput } from 'cdktf';
import { AwsProvider } from '@cdktf/provider-aws';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new AwsProvider(this, 'aws-provider', {
      region: 'us-east-1',
    });

    // simple Terraform output to validate the stack
    new TerraformOutput(this, 'lets-go', { value: 'lets go!' });
  }
}

const app = new App();
new MyStack(app, 'cdktf-name-picker');
app.synth();
```

Install the AWS provider for CDKTF (example using yarn):

```bash theme={null}
yarn add @cdktf/provider-aws
```

To deploy:

```bash theme={null}
yarn cdktf synth
yarn cdktf deploy
