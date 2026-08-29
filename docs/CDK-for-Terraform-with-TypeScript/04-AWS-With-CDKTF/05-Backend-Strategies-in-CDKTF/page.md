# Example console output when multiple stacks exist
Error: Usage Error: Found more than one stack, please specify a target stack.
Run cdktf deploy <stack> with one of these stacks: cdktf-name-picker, cdktf-week-planner
```

Deploy a specific stack by name:

```bash theme={null}
yarn deploy cdktf-week-planner
```

Or deploy multiple/all stacks using a quoted wildcard to prevent shell expansion:

```bash theme={null}
yarn deploy "*"
```

When you deploy, CDKTF will prompt to confirm which stacks to deploy and then print outputs from each stack (for example, the Week Planner URL).

## When to split functionality into separate stacks

A stack should map to a deployable unit of business functionality. Typical reasons to split into separate stacks:

| Reason                 | Description                                                   | Example                                                                         |
| ---------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Feature isolation      | Deploy and maintain a feature independently from the main app | `WeekPlanner` is deployed separately from `NamePicker`                          |
| Environment separation | Keep `dev` and `prod` state and resources isolated            | `cdktf-name-picker` vs `cdktf-name-picker-prod`                                 |
| Team boundaries        | Allow teams to manage their own stacks and CI/CD pipelines    | A backend team manages a `PaymentsStack`, frontend team manages `FrontendStack` |
| Experimental work      | Try proofs-of-concept without affecting production            | Create a `feature-x` stack for testing                                          |

Below is the S3 console showing separate per-stack Terraform state files. Using a per-stack backend configuration results in distinct state objects per stack in your backend bucket.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing the bucket &#x22;cdktf-name-picker-prereq-992382811848&#x22; with three objects listed (cdktf-name-picker, cdktf-name-picker-prod, cdktf-week-planner) and controls like Upload, Create folder, and Copy URL. The page also shows object sizes, last-modified timestamps, and the S3 navigation sidebar." />
</Frame>

## Creating a prod stack (example)

A simple way to add a production environment is to instantiate the same stack class with a different ID. To avoid resource name collisions across stacks, use a helper that prefixes names with the stack identifier:

```typescript theme={null}
// utils/getConstructName.ts
import { TerraformStack } from 'cdktf';
import { Construct } from 'constructs';

export const getConstructName = (scope: Construct, id: string) =>
  `${TerraformStack.of(scope).node.id}-${id}`;
```

Instantiate dev and prod stacks in `main.ts`:

```typescript theme={null}
// main.ts
import { App } from 'cdktf';
import { NamePickerStack } from './stacks/NamePickerStack';

const app = new App();
new NamePickerStack(app, 'cdktf-name-picker');           // dev
new NamePickerStack(app, 'cdktf-name-picker-prod');      // prod
app.synth();
```

Deploying both stacks will create separate Terraform state files and outputs (for example, two API endpoints). Note: the StageName in the exercise example still shows `/dev` for both stacks — update stage naming if you want distinct stage paths for each environment.

## Visual: multiple stacks and components

This diagram shows three stacks (dev/prod for the name picker and a WeekPlanner). Each stack can contain Constructs such as `LambdaFunction` and `LambdaRestApi`.

<Frame>
  <img alt="A presentation slide titled &#x22;Adding More Stacks&#x22; showing three colorful boxes labeled &#x22;Name Picker Stack (dev)&#x22;, &#x22;Name Picker Stack (prod)&#x22;, and &#x22;Week Planner (dev)&#x22;, each containing components like &#x22;LambdaFunction Construct&#x22; and &#x22;LambdaRestApi Construct.&#x22; A footer reads &#x22;Multiple stacks illustrate different app components.&#x22;" />
</Frame>

## Overriding runtime behavior with environment variables

Making Lambda runtime behavior configurable via environment variables is a practical way to change behavior without changing code. The name-picker Lambda supports a JSON array (`NAMES`) and a `SHUFFLE` flag. The handler below supports both modes:

* Roulette (random): return a random name on each invocation.
* Shuffle: maintain a shuffled in-memory list and return names sequentially; the in-memory state persists for the lifetime of the execution environment.

```javascript theme={null}
// function-name-picker/index.js
let shuffledNames = [];
let currentIndex = 0;

function shuffleArray(arr) {
  // Fisher-Yates shuffle
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

exports.handler = async (event) => {
  console.log('Received event', JSON.stringify(event));

  // Parse environment variables with defaults
  const names = (() => {
    try {
      return JSON.parse(process.env.NAMES || '["Arthur","Martin","Douglas","Carolyn"]');
    } catch (e) {
      console.warn('Invalid NAMES env var, using default list', e);
      return ["Arthur","Martin","Douglas","Carolyn"];
    }
  })();

  const shuffle = (process.env.SHUFFLE || 'false') === 'true';

  if (!shuffle) {
    // Roulette/random mode: return a random name each invocation
    const randomName = names[Math.floor(Math.random() * names.length)];
    return {
      statusCode: 200,
      body: JSON.stringify(randomName),
    };
  } else {
    // Shuffle mode: maintain an in-memory shuffled list and return the next name
    if (!shuffledNames.length || currentIndex >= shuffledNames.length) {
      shuffledNames = shuffleArray([...names]);
      currentIndex = 0;
    }
    const selectedName = shuffledNames[currentIndex++];
    return {
      statusCode: 200,
      body: JSON.stringify(selectedName),
    };
  }
};
```

You can edit environment variables directly in the AWS Lambda console. The screenshot below shows the Lambda configuration page when no environment variables are set.

<Frame>
  <img alt="Screenshot of the AWS Lambda console on a function's Configuration > Environment variables tab, showing &#x22;No environment variables&#x22; with an Edit button. The left navigation menu and a tutorial panel are also visible." />
</Frame>

Instead of manual edits, define default environment variables in your Lambda construct so they are deployed with the function. The project’s `LambdaFunction` construct forwards standard Lambda configuration (including `environment`) directly to the underlying AWS resource. Example:

```typescript theme={null}
// inside NamePickerStack.ts (example extract)
const functionNamePicker = new LambdaFunction(this, 'lambda-function', {
  functionName: getConstructName(this, 'api'),
  bundle: './function-name-picker',
  handler: 'index.handler',
  environment: {
    variables: {
      NAMES: '["Fred","Bob"]',
      SHUFFLE: 'false',
    },
  },
});

const lambdaRestApi = new LambdaRestApi(this, 'lambda-rest-api', {
  handler: functionNamePicker.lambdaFunction,
  stageName: 'dev',
});
```

Because the construct forwards arbitrary Lambda properties, you can add or change environment variables in your stack code and re-deploy — the deployment will overwrite manual console edits.

## Hints and type-safety (as const)

TypeScript's `as const` can help narrow literal types for compile-time checks. For example:

```typescript theme={null}
for (const type of ['roulette', 'shuffle'] as const) {
  // `type` is either 'roulette' or 'shuffle' as a string literal type
}
```

This pattern is optional but improves type-safety in code that branches on a small set of known values.

## How to deploy the full project (quick start)

Include a README with the following step-by-step commands for a fresh checkout. This short sequence is the recommended quick-start for collaborators:

> **lightbulb** Run these commands after cloning to fetch providers/modules and deploy the backend and app stacks:

  * `yarn install` — install dependencies
  * `yarn cdktf get` — generate module bindings
  * `yarn deploy:prereq` — deploy the S3/DynamoDB remote backend
  * `yarn deploy "*"` — deploy all stacks (dev, prod, and feature stacks)

Notes:

* `yarn cdktf get` generates the `.gen` folder used for imported Terraform modules.
* `yarn deploy:prereq` deploys the prerequisite infrastructure (remote state bucket and locking table).

## package.json scripts

Here are the useful npm/yarn scripts included in the project and what they do:

| Script         | Command               | Purpose                                                                |
| -------------- | --------------------- | ---------------------------------------------------------------------- |
| get            | `yarn get`            | Runs `cdktf get` to generate module bindings                           |
| build          | `yarn build`          | Runs `tsc` to compile TypeScript                                       |
| synth          | `yarn synth`          | Runs `cdktf synth` to synthesize Terraform JSON                        |
| deploy         | `yarn deploy`         | Runs `cdktf deploy` for targeted stacks                                |
| deploy prereq  | `yarn deploy:prereq`  | Runs `cdktf deploy --app='yarn ts-node prereq.ts'` to create backend   |
| destroy        | `yarn destroy`        | Runs `cdktf destroy` to destroy stacks                                 |
| destroy prereq | `yarn destroy:prereq` | Runs `cdktf destroy --app='yarn ts-node prereq.ts'` to destroy backend |

Example `package.json` scripts snippet:

```json theme={null}
{
  "scripts": {
    "get": "cdktf get",
    "build": "tsc",
    "synth": "cdktf synth",
    "deploy": "cdktf deploy",
    "deploy:prereq": "cdktf deploy --app='yarn ts-node prereq.ts'",
    "destroy": "cdktf destroy",
    "destroy:prereq": "cdktf destroy --app='yarn ts-node prereq.ts'"
  }
}
```

## Cleaning up (destroying your infrastructure)

Destroying resources follows the reverse order of deployment. Important: destroy the application stacks first, then destroy the remote backend stack (the S3 bucket and DynamoDB table). If you destroy the backend first (remove the state bucket), Terraform will lose state and cannot reliably destroy the managed resources.

> **warning** Warning: Always destroy application stacks before destroying the remote state backend. If the S3 bucket containing state is removed while resources still exist, Terraform cannot track or destroy those resources (you may encounter `BucketNotEmpty` or orphaned resources).

Steps to clean up:

1. Destroy application stacks:
   ```bash theme={null}
   yarn destroy "*"
   ```
2. Empty the backend S3 bucket if required (Terraform will fail with `BucketNotEmpty` if the bucket is not empty).
3. Destroy the prereq backend stack:
   ```bash theme={null}
   yarn destroy:prereq
   ```

The console shows an "Empty bucket" confirmation flow when you manually clear a bucket:

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing an &#x22;Empty bucket&#x22; confirmation page. It displays warnings, a textbox requiring you to type &#x22;permanently delete,&#x22; and an orange &#x22;Empty&#x22; button to confirm deletion." />
</Frame>

After the backend is removed and everything is destroyed, the DynamoDB tables list should be empty:

<Frame>
  <img alt="A screenshot of the AWS DynamoDB console showing the Tables page with no tables in this region and a prominent &#x22;Create table&#x22; button. The left sidebar lists DynamoDB navigation items like Dashboard, Explore items, Backups, and Settings." />
</Frame>

With these steps Arthur can fully tear down the application and avoid surprise cloud costs.

***

That concludes this lesson. The final summary covers everything learned across the course: problem definition, manual AWS deployment, reusable constructs, packaging strategies, remote backend setup, and importing modules via CDKTF — all combining to produce an automated, shareable, and maintainable infrastructure.

## Links and References

* CDK for Terraform (CDKTF) — [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform documentation — [https://www.terraform.io/docs](https://www.terraform.io/docs)
* AWS Lambda Developer Guide — [https://docs.aws.amazon.com/lambda/latest/dg/welcome.html](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* S3 documentation — [https://docs.aws.amazon.com/s3/index.html](https://docs.aws.amazon.com/s3/index.html)
* DynamoDB documentation — [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/4625ff69-dbd8-42ac-9542-d0e60a85e2ae/lesson/4c12891b-f4d1-42b9-a6d7-855716897e82)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/4625ff69-dbd8-42ac-9542-d0e60a85e2ae/lesson/b53f0026-82f8-4e86-b92d-abba0923d2b3)


# Backend Strategies in CDKTF

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/AWS-With-CDKTF/Backend-Strategies-in-CDKTF/page

Best practices for managing Terraform state with CDKTF, migrating from local to remote S3 backend with DynamoDB locking and using a two-app pattern to avoid circular dependencies

In this lesson you’ll learn best practices for managing Terraform state with CDK for Terraform (CDKTF), why local state doesn’t scale for teams, and a recommended pattern for moving to a remote S3 backend with DynamoDB state locking.

A quick recap: Terraform state is a file that records the resources managed by Terraform, their current configuration, and relationships. CDKTF synthesizes Terraform configuration and Terraform uses the state to compare actual infrastructure with the desired state declared in code — enabling accurate creates, updates, and deletes.

## Local state — example

Local state is convenient for single-developer experimentation. Here’s an excerpt of a local Terraform state file for the NamePicker app:

```json theme={null}
{
  "serial": 12,
  "lineage": "1853f402-815b-2006-68e8-6c12a043cebb",
  "outputs": {
    "namePickerApiUrl": {
      "value": "https://exgnru9me6.execute-api.us-east-1.amazonaws.com/dev",
      "type": "string"
    }
  },
  "resources": [
    {
      "mode": "managed",
      "type": "aws_api_gateway_deployment",
      "name": "lambda-rest-api_deployment_FCE7AD5D",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": []
    }
  ]
}
```

When deployed locally, the CLI output might look like:

```bash theme={null}
cdktf-name-picker
Apply complete! Resources: 11 added, 0 changed, 0 destroyed.

Outputs:
namePickerApiUrl = "https://exgnru9me6.execute-api.us-east-1.amazonaws.com/dev"

> curl https://exgnru9me6.execute-api.us-east-1.amazonaws.com/dev
"Arthur"
```

While local state works for experiments, it becomes problematic in team environments: there is no single shared source of truth, which leads to conflicts, drift, and accidental overwrites when multiple people change infrastructure.

## Remote backend: S3 + DynamoDB (recommended for AWS)

A common production-ready approach on AWS is to store state in an S3 bucket and use a DynamoDB table for state locking. Terraform supports many backends (including Terraform Cloud), but S3 + DynamoDB is a simple, widely-used pattern for teams using AWS.

Example: configure the S3 backend in a CDKTF stack so Terraform uses S3 for state and DynamoDB for locking:

```typescript theme={null}
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new provider.AwsProvider(this, 'aws-provider', {
      region: 'us-east-1',
    });

    new S3Backend(this, {
      bucket: 'cdktf-name-picker-backend', // existing S3 bucket name
      dynamodbTable: 'cdktf-name-picker-locks', // existing DynamoDB table name
      region: 'us-east-1',
      key: 'state-file',
    });

    // ...
  }
}
```

S3Backend parameters:

|       Parameter | Description                                            |
| --------------: | ------------------------------------------------------ |
|        `bucket` | S3 bucket name to store the state file                 |
| `dynamodbTable` | DynamoDB table name for state locking                  |
|        `region` | AWS region for the backend resources                   |
|           `key` | Object key (path) in the S3 bucket for this state file |

<Frame>
  <img alt="Slide titled &#x22;Deploying Backend Resources — To store Terraform State.&#x22; It shows an author icon with an arrow pointing to an AWS box containing icons for an S3 bucket and a DynamoDB table." />
</Frame>

## Creating the S3 bucket and DynamoDB table

You have three main choices to create the backend resources:

* Manual: create the S3 bucket and DynamoDB table in the AWS Console (quick, but not automated or reproducible).
* CDKTF code: add resource definitions in your CDKTF app (automated, but may create circular dependency issues — see below).
* Terraform Registry module: import and reuse a community or org-maintained module (recommended for reproducibility and speed).

Using an existing Terraform module is common—creating backend resources is a well-known pattern and rarely needs custom code. CDKTF can import Terraform modules by adding them to `cdktf.json` and running `cdktf get`.

Example `cdktf.json` that references a module:

```json theme={null}
{
  "language": "typescript",
  "app": "npx ts-node main.ts",
  "terraformModules": [
    {
      "name": "s3-dynamodb-remote-backend",
      "source": "my-devops-way/s3-dynamodb-remote-backend/aws"
    }
  ],
  "context": {}
}
```

Then run:

```bash theme={null}
yarn cdktf get
```

Expected output (abbreviated):

```bash theme={null}
Generated typescript constructs in the output directory: .gen
```

cdktf generates TypeScript wrappers for modules under `.gen`. A trimmed example of a generated wrapper:

```typescript theme={null}
// generated by cdktf get
// my-devops-way/s3-dynamodb-remote-backend/aws
import { TerraformModule, TerraformModuleUserConfig } from 'cdktf';
import { Construct } from 'constructs';

export interface S3DynamodbRemoteBackendConfig extends TerraformModuleUserConfig {
  readonly bucket?: string;
  readonly bucketPrefix?: string;
  readonly dynamodbTable: string;
  readonly kmsMasterKeyId?: string;
}

export class S3DynamodbRemoteBackend extends TerraformModule {
  constructor(scope: Construct, id: string, config: S3DynamodbRemoteBackendConfig) {
    super(scope, id, {
      ...config,
      source: 'my-devops-way/s3-dynamodb-remote-backend/aws',
    });
    this.bucket = config.bucket;
    this.bucketPrefix = config.bucketPrefix;
    this.dynamodbTable = config.dynamodbTable;
    this.kmsMasterKeyId = config.kmsMasterKeyId;
  }

  // getters and setters...
}
```

You can instantiate the generated module and then configure the S3 backend:

```typescript theme={null}
import { S3DynamodbRemoteBackend } from './.gen/modules/s3-dynamodb-remote-backend';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new provider.AwsProvider(this, 'aws-provider', { region: 'us-east-1' });

    const backend = new S3DynamodbRemoteBackend(this, 's3-dynamodb-remote-backend', {
      bucket: 'cdktf-name-picker-backend',
      dynamodbTable: 'cdktf-name-picker-locks',
    });

    new S3Backend(this, {
      bucket: 'cdktf-name-picker-backend',
      dynamodbTable: 'cdktf-name-picker-locks',
      region: 'us-east-1',
      key: 'state-file',
    });
  }
}
```

<Frame>
  <img alt="A slide titled &#x22;Importing Modules to CDKTF&#x22; showing a Terraform Registry box on the left with a module being fetched (arrow labeled &#x22;CDKTF get&#x22;) into a CDKTF box on the right that contains CDKTF.json and a Module. It illustrates importing Terraform registry modules into CDK for Terraform." />
</Frame>

## The circular dependency problem (and a warning)

When the same CDKTF app both *creates* the backend and *uses* it in the S3Backend configuration, you can hit a circular dependency:

* Synthesizing the main app asks “does the remote backend exist?”
* If the backend is defined in the same app, Terraform/CDKTF needs the backend available to synthesize/deploy.
* That creates a circular synth/deploy dependency.

> **warning** Do not create and use the same S3/DynamoDB backend from a single CDKTF app. Doing so introduces a synth/deploy circular dependency and prevents the app from being synthesized and deployed reliably.

This issue is illustrated here:

<Frame>
  <img alt="A presentation slide titled &#x22;Problem&#x22; that diagrams how the cdk.tf name-picker app's Deploy and Synthesize steps depend on each other. The right side highlights this circular dependency with a colorful snake-in-a-ring illustration." />
</Frame>

## Recommended pattern: split into two apps (prereq + main)

To avoid the circular dependency, split the workflow into two separate CDKTF apps:

1. A prereq app that creates the S3 bucket and DynamoDB table (local state).
2. The main app that uses the created backend (remote S3 state) — it reads the prereq outputs to configure the S3Backend.

Flow:

* synth & deploy prereq app → creates S3 bucket + DynamoDB table and writes outputs to a local tfstate file.
* synth main app (reads prereq tfstate locally to obtain bucket and table names) → configures S3Backend to point to the created resources.
* deploy main app (now using the remote S3 backend).

Diagram:

<Frame>
  <img alt="A diagram showing the deployment flow for two CDKTF apps (&#x22;cdktf-name-picker-prereq&#x22; and &#x22;cdktf-name-picker&#x22;) with Synthesize → Deploy steps. It shows resources used (S3 Bucket, DynamoDB for prereqs; Lambda and API Gateway for the app) and state backends (local state vs S3 backend state)." />
</Frame>

## Implementation overview

1. Create a prereq stack that deploys the S3 bucket and DynamoDB table using the imported module. The prereq stack can use the AWS account ID to create a globally unique bucket name.

Example (abridged):

```typescript theme={null}
// stacks/PreReqStack.ts (abridged)
import { Construct } from 'constructs';
import { TerraformStack, TerraformOutput } from 'cdktf';
import { data } from '@cdktf/provider-aws';
import { S3DynamodbRemoteBackend } from '../.gen/modules/s3-dynamodb-remote-backend';

export class PreReqStack extends TerraformStack {
  constructor(scope: Construct, id: string, config: { backendName: string }) {
    super(scope, id);

    const currentAccount = new data.AwsCallerIdentity(this, 'current-account');

    const backend = new S3DynamodbRemoteBackend(this, 's3-dynamodb-remote-backend', {
      bucket: `${config.backendName}-${currentAccount.accountId}`,
      dynamodbTable: config.backendName,
    });

    new TerraformOutput(this, 'bucket', { value: backend.bucket });
    new TerraformOutput(this, 'dynamodbTable', { value: backend.dynamodbTable });
  }
}
```

2. Add an npm script to deploy only the prereq app. Example `package.json` scripts:

```json theme={null}
"scripts": {
  "get": "cdktf get",
  "build": "tsc",
  "synth": "cdktf synth",
  "deploy": "cdktf deploy",
  "deploy:prereq": "cdktf deploy --app='yarn ts-node prereq.ts'"
}
```

Deploy the prereq app:

```bash theme={null}
yarn deploy:prereq
```

You should see a Terraform plan/apply that creates the S3 bucket and DynamoDB table, and prints outputs such as the created bucket name and DynamoDB table name.

3. Use the prereq outputs to configure the main app's S3 backend. One practical approach is to create a base stack class (for example, `AwsBaseStack`) that reads the prereq tfstate file produced by the prereq deployment and configures `S3Backend` from those outputs.

Example (abridged):

```typescript theme={null}
// stacks/AwsBaseStack.ts (abridged)
import { Construct } from 'constructs';
import { TerraformStack, S3Backend } from 'cdktf';
import { provider } from '@cdktf/provider-aws';
import * as path from 'path';
import * as fs from 'fs';
import { BACKEND_NAME } from '../config';

export class AwsBaseStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new provider.AwsProvider(this, 'aws-provider', { region: 'us-east-1' });

    const prereqStateFile = path.join(process.env.INIT_CWD!, `./terraform.${BACKEND_NAME}.tfstate`);

    let prereqState: any = null;
    try {
      prereqState = JSON.parse(fs.readFileSync(prereqStateFile, 'utf-8'));
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        throw new Error(`Could not find prerequisite state file: ${prereqStateFile}`);
      }
      throw error;
    }

    new S3Backend(this, {
      bucket: prereqState.outputs.bucket.value,
      dynamodbTable: prereqState.outputs.dynamodbTable.value,
      region: 'us-east-1',
      key: 'cdktf-name-picker',
    });
  }
}
```

Notes:

* `process.env.INIT_CWD` ensures the prereq state file is read from the directory where you executed the deploy command.
* The prereq stack must be deployed first so the state file containing `bucket` and `dynamodbTable` outputs is available locally.

After deploying the prereq app, confirm in the AWS Console that:

* The S3 bucket exists and contains the state key for the main app.
* The DynamoDB table for state locking exists.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing the bucket &#x22;cdktf-name-picker-prereq-992382811848&#x22; with one object listed. The interface shows actions like Upload, Create folder, Copy URL, and object details (last modified, size, storage class)." />
</Frame>

4. With the `AwsBaseStack` reading the prereq outputs, synthesize and deploy the main stack normally. When you run the main deploy (for example, `yarn deploy`), Terraform should detect no differences against the state stored in S3 if nothing else changed:

```bash theme={null}
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
Outputs:
namePickerApiUrl = "https://p67gu4qdc4.execute-api.us-east-1.amazonaws.com/dev"
```

You can then delete the main app’s local tfstate files (but keep the prereq tfstate file — it documents the S3/DynamoDB resources used for the backend).

> **lightbulb** Tips:

  * CDKTF generates raw Terraform in the `cdktf.out` directory. If you need to run low-level Terraform commands, use `cdktf.out` as an escape hatch.
  * When starting new projects, configure a remote backend from the start. Use the two-app prereq pattern primarily when migrating existing local-state projects.
  * Consider using IAM permissions and encryption (KMS) for S3 buckets that hold sensitive state.

## Summary

* Local state is convenient for experiments but fragile in team environments. Use a remote backend for collaboration.
* On AWS, S3 + DynamoDB is a common remote backend that provides shared state and locking.
* Avoid creating and using the same backend in a single CDKTF app — this causes a synth/deploy circular dependency.
* Use a two-app pattern (prereq app + main app) to reliably create backend resources and then switch the main app to the remote backend.
* Use `cdktf get` to import Terraform Registry modules and `.gen` wrappers to instantiate module constructs in CDKTF.

<Frame>
  <img alt="A horizontal five-step timeline for backend development. It lists: 01 Deploy and Configure IAM Role, 02 Lambda Function Construct, 03 API Gateway Construct, 04 Backend Strategies (highlighted), and 05 Adding More Functionality (Multiple Stacks)." />
</Frame>

## Links and references

* [CDK for Terraform (CDKTF) documentation](https://developer.hashicorp.com/terraform/cdktf)
* [Terraform Cloud and backends](https://www.terraform.io/cloud)
* [Terraform Registry](https://registry.terraform.io)
* [AWS Console](https://console.aws.amazon.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/4625ff69-dbd8-42ac-9542-d0e60a85e2ae/lesson/259a73bf-3532-457a-a4ae-f30b8eea25c6)
