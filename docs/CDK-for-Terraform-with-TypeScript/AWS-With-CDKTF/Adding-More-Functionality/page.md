# or, if using the generated package scripts:
yarn deploy
```

Deploying the Lambda's execution role

Every Lambda function must assume an IAM role. The role must include an assume role policy that allows `lambda.amazonaws.com` to assume the role. Example CDKTF TypeScript snippet to create a minimal role:

```typescript theme={null}
import { IamRole } from '@cdktf/provider-aws/lib/iam-role';

const lambdaRole = new IamRole(this, 'lambda-execution-role', {
  name: 'lambda-execution-role',
  assumeRolePolicy: JSON.stringify({
    Version: '2012-10-17',
    Statement: [
      {
        Action: 'sts:AssumeRole',
        Principal: {
          Service: 'lambda.amazonaws.com',
        },
        Effect: 'Allow',
      },
    ],
  }),
});
```

You will typically attach either managed policies (for example, `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole` for CloudWatch Logs) or inline policies to grant the Lambda the permissions it needs.

Once the role is created you can confirm it in the IAM console:

<Frame>
  <img alt="A screenshot of the AWS Identity and Access Management (IAM) console showing the role &#x22;cdktf-name-picker-api-execution-role.&#x22; The page displays the role summary (creation date, ARN, max session duration) and the Permissions tab with no attached policies." />
</Frame>

Recap

* We performed a manual console deployment of a Lambda + API Gateway NamePicker app to illustrate the components and how they interact.
* We validated AWS credentials with `aws sts get-caller-identity`.
* We created a basic CDKTF app and configured the AWS provider.
* We defined an IAM role for Lambda using CDKTF code.
* Next, we’ll expand the CDKTF stack to provision the Lambda function code package, the Lambda resource, the API Gateway REST API and proxy configuration, the IAM policies, and related outputs — all fully defined as code so Arthur can share and reproduce the environment reliably.

<Frame>
  <img alt="A slide titled &#x22;Connecting to AWS – Recap&#x22; showing a simple diagram where a rounded &#x22;CDKTF App&#x22; box points with an arrow to a rounded &#x22;AWS Provider&#x22; box. (© KodeKloud in the corner.)" />
</Frame>

References

* CDKTF documentation: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* AWS Lambda docs: [https://docs.aws.amazon.com/lambda/latest/dg/welcome.html](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* Amazon API Gateway docs (REST APIs): [https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api.html](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api.html)
* Terraform AWS provider: [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

We'll now expand the CDKTF stack to create the Lambda deployment package, Lambda resource, API Gateway resources, and the necessary IAM policies — all as code so Arthur can share the project and reproduce the setup reliably.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/4625ff69-dbd8-42ac-9542-d0e60a85e2ae/lesson/6b3e89b0-6156-475c-a2cf-0b3771783e10" />
</CardGroup>


# Adding More Functionality

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/AWS-With-CDKTF/Adding-More-Functionality/page

Guide to extending a CDK for Terraform AWS project with reusable Lambda constructs, multiple stacks and environments, deterministic packaging, remote state backend, environment variable configuration, and deployment workflows

In this final section we recap the project and show practical ways to extend the application: adding new stacks for features or environments, and controlling runtime behavior via environment variables. The patterns below focus on CDK for Terraform (CDKTF) with AWS: building reusable Constructs (LambdaFunction, LambdaRestApi), packaging Lambda assets correctly, moving Terraform state to a remote backend (S3 + DynamoDB), and importing Terraform modules via CDKTF.

Key outcomes:

* Reusable Constructs: `LambdaFunction` and `LambdaRestApi`.
* Packaging strategy: prefer `TerraformAsset` over `execSync` for deterministic Lambda packaging.
* Remote backend: transition local state to S3/DynamoDB for team collaboration.
* CDKTF modules: import generated modules with `cdktf get`.

The deployed name-picker API returns a random family member to do chores — and the patterns here let Arthur add more features and environments safely.

<Frame>
  <img alt="A slide titled &#x22;Recap&#x22; with a blue gradient sidebar and a vertical list of colorful numbered markers: 01 Problem, 02 Manual process, 03 LambdaFunction construct, and 04 Packaging with execSync vs TerraformAsset. The slide includes a small © KodeKloud notice at the bottom." />
</Frame>

## Adding a new stack (WeekPlannerStack)

To add a separate feature as its own deployable unit, create a new stack class that extends your shared `AwsBaseStack` (this base stack centralizes provider/backend configuration). The WeekPlanner example below demonstrates a minimal stack that reuses the base stack and exposes an output.

```typescript theme={null}
// stacks/WeekPlannerStack.ts
import { Construct } from 'constructs';
import { AwsBaseStack } from './AwsBaseStack';
import { TerraformOutput } from 'cdktf';

export class WeekPlannerStack extends AwsBaseStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Pretend we deployed a resource and expose its URL as an output
    new TerraformOutput(this, 'weekPlannerUrl', {
      value: 'https://example.com',
    });
  }
}
```

Register the stack in your CDKTF app:

```typescript theme={null}
// main.ts
import { App } from 'cdktf';
import { NamePickerStack } from './stacks/NamePickerStack';
import { WeekPlannerStack } from './stacks/WeekPlannerStack';

const app = new App();
new NamePickerStack(app, 'cdktf-name-picker');
new WeekPlannerStack(app, 'cdktf-week-planner');
app.synth();
```

When multiple stacks exist the default CDKTF CLI needs an explicit target. Example CLI output when more than one stack is present:

```bash theme={null}
