# global CLI (optional)
npm install -g cdktf-cli

# in an empty directory
cdktf init --template=typescript
```

Sample init prompts (abbreviated)

```bash theme={null}
Welcome to CDK for Terraform!

? Do you want to continue with Terraform Cloud remote state management? no
? Project Name cdktf-project-builder
? Project Description A simple getting started project for cdktf.
? Do you want to start from an existing Terraform project? no
? What providers do you want to use? local
```

The init command scaffolds a TypeScript project (tsconfig, package.json, `main.ts`) and installs provider packages such as `@cdktf/provider-local`.

Console logs may show provider installation:

```bash theme={null}
[INFO] Found pre-built provider.
Adding package @cdktf/provider-local @ 10.1.1
[INFO] Installing package @cdktf/provider-local @ 10.1.1 using npm.
[INFO] Package installed.
```

Generated package.json (dependencies snippet)

```json theme={null}
{
  "dependencies": {
    "@cdktf/provider-local": "10.1.1",
    "cdktf": "^0.20.9",
    "constructs": "^10.4.2"
  },
  "devDependencies": {
    "@types/jest": "^29.5.13",
    "@types/node": "^22.7.6",
    "jest": "^29.7.0",
    "ts-jest": "^29.2.5",
    "ts-node": "^10.9.2",
    "typescript": "^5.6.3"
  }
}
```

Switch package manager to Yarn (optional)
If you prefer Yarn (and Yarn 2+/Corepack-managed installs), prepare and activate it with Corepack, then migrate the lockfile.

```bash theme={null}
corepack prepare yarn@stable --activate
rm -f package-lock.json
touch yarn.lock
yarn install
yarn -v
```

<Frame>
  <img alt="A presentation slide titled &#x22;Change Package Manager to Yarn (Optional)&#x22; that states the problem &#x22;npm is slow and does not have modern tooling.&#x22; Below it is a black rounded callout/button reading &#x22;Delete package-lock.json.&#x22;" />
</Frame>

Add the CLI as a project dev dependency (recommended for CI)

```bash theme={null}
yarn add -D cdktf-cli
# or with npm:
# npm install --save-dev cdktf-cli
```

With a local `cdktf` binary, scripts like `yarn cdktf synth` or `npm run synth` will use the project's executable, improving consistency across environments.

Project structure and main TypeScript file
After `cdktf init`, the scaffold contains a `main.ts` (or `main.js`) entrypoint and a stack class. Key concepts:

* App: the root construct that contains stacks.
* TerraformStack: extend this class to define resources.
* app.synth(): synthesizes TypeScript constructs into Terraform configuration (JSON files).

Example `main.ts` with a Terraform output

```typescript theme={null}
import { Construct } from "constructs";
import { App, TerraformOutput, TerraformStack } from "cdktf";

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // define resources here
    new TerraformOutput(this, "helloWorld", {
      value: "Hello World",
    });
  }
}

const app = new App();
new MyStack(app, "code");
app.synth();
```

Notes on constructs

* `scope` builds the construct tree and creates parent-child relationships.
* `id` uniquely identifies a construct within its parent.
* `app.synth()` converts your TypeScript code into `.tf.json` Terraform configuration; it does not apply changes to infrastructure.

cdktf.json
`cdktf init` generates a `cdktf.json` file with metadata and the `app` command used to run your CDKTF application:

```json theme={null}
{
  "language": "typescript",
  "app": "yarn ts-node main.ts",
  "projectId": "c24105e3-e5b6-40ce-941b-f0c1ae8d7356",
  "sendCrashReports": "true",
  "terraformProviders": [],
  "terraformModules": [],
  "context": {}
}
```

Set the `app` value to `npx ts-node main.ts` or a Yarn script (e.g., `yarn ts-node main.ts`) depending on your workflow.

Synthesizing and deploying
Synthesize your CDKTF TypeScript into Terraform JSON files:

```bash theme={null}
# using Yarn (if cdktf-cli is local): 
yarn cdktf synth

# if the CLI is global:
cdktf synth
```

Synthesis output appears in `cdktf.out/stacks/<stack-name>` and includes Terraform JSON and metadata.

Example synth output:

```text theme={null}
Generated Terraform code for the stacks: code
```

Deploy (synth + terraform apply)

```bash theme={null}
# with Yarn wrapper
yarn cdktf deploy

# or with a global CLI
cdktf deploy
```

`cdktf deploy` runs `app.synth()` and then invokes `terraform apply`. In interactive mode you will be prompted to approve changes; use automation flags in CI pipelines for non-interactive runs.

Helpful package.json scripts
Add useful commands to speed development and CI:

```json theme={null}
"scripts": {
  "get": "cdktf get",
  "build": "tsc",
  "synth": "cdktf synth",
  "compile": "tsc --pretty",
  "watch": "tsc -w",
  "test": "jest",
  "upgrade": "npm i cdktf@latest cdktf-cli@latest"
}
```

Terraform state
For this example we used local state; Terraform will create a local state file (e.g., `terraform.<stack>.tfstate`) when you apply. For team workflows or production, use a remote backend such as Terraform Cloud, S3 with DynamoDB locking, or other supported options.

Example state metadata (abbreviated)

```json theme={null}
{
  "version": 3,
  "terraform_version": "1.9.5",
  "backend": {
    "type": "local",
    "config": {
      "path": "/root/code/terraform.code.tfstate"
    }
  }
}
```

Summary

* CDKTF allows you to author Terraform-managed infrastructure using TypeScript (and other languages), combining Terraform providers with familiar programming constructs.
* We covered prerequisites, how to run `cdktf init` to scaffold a TypeScript project, and how the synth/deploy workflow maps to Terraform JSON and `terraform apply`.
* Optional items covered: switching package managers (Yarn) and installing `cdktf-cli` locally for reproducible CI.
* Next: continue Arthur's journey by implementing the local file generation stack and then applying these same patterns to cloud infrastructure such as AWS.

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/948c0a82-faa1-4f16-83d1-8ee8df2336b3/lesson/594ed4f5-804b-418c-86e0-8598dac096c3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/948c0a82-faa1-4f16-83d1-8ee8df2336b3/lesson/700f2c9c-0cf8-4ba8-a5d1-74eb03e83c74)


# Constructs

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-CDKTF/Constructs/page

Explains building reusable CDKTF constructs in TypeScript using a ProjectFolder example to encapsulate resources, enable reuse, and expose resource properties for stacks

This article explains how to create reusable constructs in CDK for Terraform (CDKTF). Constructs let you encapsulate resource creation and logic in reusable, programmatic units—similar in purpose to Terraform modules but with the power of TypeScript.

Arthur wants to reuse his project setups, so he creates a ProjectFolder construct to encapsulate repetitive tasks and to group together the resources we've created so far into a reusable building block.

<Frame>
  <img alt="A slide titled &#x22;Creating Constructs in CDKTF – Solution&#x22; showing a stylized person and monitor with code, and the instruction &#x22;Create a construct ProjectFolder to handle repetitive tasks.&#x22; A footer notes the Terraform equivalent: constructs → Terraform modules (HCL)." />
</Frame>

## Why use constructs?

* Reuse: package common patterns (folders, files, provider initialization) once and reuse across stacks and projects.
* Composition: compose small constructs into larger systems.
* Type-safety & programmability: use TypeScript for control flow, loops, and conditional logic that would be awkward in HCL modules.
* Direct object references: CDKTF lets you expose resource objects directly (not just primitive outputs), enabling richer composition.

## Minimal ProjectFolder construct (boilerplate)

The example below shows a minimal construct shell that illustrates common TypeScript patterns used in CDKTF constructs.

```typescript theme={null}
import { Construct } from 'constructs';
import { file } from '@cdktf/provider-local';

interface ProjectFolderProps {
  readonly projectName: string;
  readonly projectDirectory: string;
}

export class ProjectFolder extends Construct {
  constructor(scope: Construct, id: string, props: ProjectFolderProps) {
    super(scope, id);

    const { projectName, projectDirectory } = props;
    // Reusable code...
  }
}
```

> **lightbulb** Key TypeScript notes:

  * `extends`: creates a class that inherits from a base class (here `Construct`).
  * `super(scope, id)`: calls the parent class constructor to initialize inherited behavior.
  * `readonly`: marks a property as immutable after initialization.
  * Destructuring (`const { projectName, projectDirectory } = props`) is a concise shorthand for extracting properties from an object.

Place construct files in a `constructs` folder. When a file exports a single class, it's common to name the file after that class (for example, `project-folder.ts`).

## Example stack that uses the construct

This stack initializes the `local` provider, sets up base variables (project directory and name), and instantiates the `ProjectFolder` construct. It also demonstrates exposing a value from the construct as a Terraform output.

```typescript theme={null}
import { App, TerraformOutput, TerraformStack } from 'cdktf';
import { LocalProvider, file } from '@cdktf/provider-local';
import { Construct } from 'constructs';
import * as path from 'path';
import { ProjectFolder } from './constructs/project-folder';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Initialize the local provider
    new LocalProvider(this, 'local', {});

    // Base directory and project name
    const projectDirectory = path.join(process.env.INIT_CWD!, 'authors-projects');
    const projectName = 'project-1';

    // Instantiate the reusable construct
    const projectFolder = new ProjectFolder(this, 'project-folder', {
      projectName,
      projectDirectory,
    });

    // Expose the readme content from the construct as a Terraform output
    new TerraformOutput(this, 'readMeContent', {
      value: projectFolder.readmeFile.content,
    });
  }
}

const app = new App();
new MyStack(app, 'cdktf-project-builder');
app.synth();
```

## Move resource creation into the construct

The construct should:

* Define the properties it needs (via `ProjectFolderProps`).
* Create the resources it manages.
* Expose any values or resource references the stack or other constructs might need by assigning them to `readonly` class properties.

Example `constructs/project-folder.ts`:

```typescript theme={null}
import { Construct } from 'constructs';
import { file } from '@cdktf/provider-local';
import * as path from 'path';

interface ProjectFolderProps {
  readonly projectName: string;
  readonly projectDirectory: string;
}

export class ProjectFolder extends Construct {
  // Expose the File resource so other constructs/stacks can access it.
  readonly readmeFile: file.File;

  constructor(scope: Construct, id: string, props: ProjectFolderProps) {
    super(scope, id);

    const { projectName, projectDirectory } = props;
    const basePath = path.join(projectDirectory, projectName);

    // Create a README file resource and assign it to the read-only property.
    this.readmeFile = new file.File(this, 'readme-file', {
      filename: `${basePath}/README.md`,
      content: `# ${projectName}\n\nThis is the ${projectName} project`,
    });
  }
}
```

By assigning the resource to `this.readmeFile` (instead of a local `const`), the stack that instantiates this construct can reference `projectFolder.readmeFile` to access resource attributes (for example, its `content`).

When the construct is instantiated in the stack (as shown earlier), you create a Terraform output from an attribute exposed by the construct:

```typescript theme={null}
// In the stack constructor, after creating the ProjectFolder instance:
new TerraformOutput(this, 'readMeContent', {
  value: projectFolder.readmeFile.content,
});
```

<Frame>
  <img alt="A presentation slide titled &#x22;Creating Constructs in CDKTF – Solution&#x22; with an icon of a person at a monitor displaying code brackets. The slide includes the instruction: &#x22;Expose a read-only property from ProjectFolder construct.&#x22;" />
</Frame>

## Quick reference

| Item             | Purpose                                             | Example / Notes                                                                           |
| ---------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Construct folder | Organize reusable constructs                        | `constructs/project-folder.ts`                                                            |
| Props interface  | Defines inputs required by construct                | `ProjectFolderProps` with `projectName`, `projectDirectory`                               |
| Exposed property | Let stacks reference resources created by construct | `readonly readmeFile: file.File`                                                          |
| Terraform output | Export values from the stack                        | `new TerraformOutput(this, 'readMeContent', { value: projectFolder.readmeFile.content })` |

## Pattern benefits

* Encapsulate resource creation in a reusable construct.
* Expose meaningful, read-only properties (resource objects and attributes) for use by the stack or other constructs.
* Keep stacks declarative while composing constructs programmatically.
* Unlike HCL modules, CDKTF allows direct object references and richer composition patterns via TypeScript.

> **lightbulb** Best practice: Keep constructs small and focused. Expose only the properties that other stacks or constructs need to keep the API surface minimal and easier to maintain.

## Links and references

* CDK for Terraform: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Constructs programming model: [https://github.com/aws/constructs](https://github.com/aws/constructs)
* Terraform modules (HCL): [https://www.terraform.io/language/modules](https://www.terraform.io/language/modules)
* Node.js path module (used for `path.join`): [https://nodejs.org/api/path.html](https://nodejs.org/api/path.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/948c0a82-faa1-4f16-83d1-8ee8df2336b3/lesson/d7c50a2d-2293-4c68-a052-52a1fe00d47a)
