# Key Takeaways

Source: https://notes.kodekloud.com/docs/CDK-for-Terraform-with-TypeScript/Introduction-to-CDKTF/Key-Takeaways/page

Guide to using CDK for Terraform with TypeScript to build reusable constructs that automate project folder and file creation, synthesize Terraform configuration, and follow best practices.

This final section summarizes the CDK for Terraform (CDKTF) concepts introduced earlier, highlights the practical benefits, and lists recommended best practices for building reusable, type-safe infrastructure automation with TypeScript.

A quick success story: Arthur can now automate bootstrapping new projects, reducing manual steps and the chance of errors. Below is how the KodeKloud Labs sample project is organized and what the code does.

## Project stack (main.ts)

The application stack initializes the local provider, sets a base project directory, and instantiates a reusable construct that creates the project folder and files.

```typescript theme={null}
import * as path from 'path';
import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import * as provider from '@cdktf/provider-local';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Initialize the local provider
    new provider.LocalProvider(this, 'local', {});

    const projectDirectory = path.join(process.env.INIT_CWD!, './authors-projects');

    const projectName = 'project-1';

    new ProjectFolder(this, 'project-folder', {
      projectName,
      projectDirectory,
    });

    // Create the .gitignore file independently if needed
  }
}
```

* What this does: adds the local provider and creates a `ProjectFolder` construct for `project-1` under `./authors-projects`.
* Why this helps: defining resources via constructs keeps your infrastructure code modular and reusable.

## Reusable construct: ProjectFolder

The `ProjectFolder` construct encapsulates file creation using the local provider. It demonstrates how to expose created resources (e.g., `readMeFile`) and how to provide typed props for clarity and autocompletion.

```typescript theme={null}
import { Construct } from 'constructs';
import * as file from '@cdktf/provider-local/lib/file';

interface ProjectFolderProps {
  projectName: string;
  projectDirectory: string;
  ignoreFiles?: string[];
}

class ProjectFolder extends Construct {
  public readonly readMeFile: file.File;

  constructor(scope: Construct, id: string, props: ProjectFolderProps) {
    super(scope, id);

    const { projectName, projectDirectory, ignoreFiles = [] } = props;
    const basePath = `${projectDirectory}/${projectName}`;

    // Create the README file with the project name inside
    this.readMeFile = new file.File(this, 'ReadmeFile', {
      filename: `${basePath}/README.md`,
      content: `# ${projectName}\n\nThis is the ${projectName} project.`,
    });

    // Create the package.json file with basic content
    new file.File(this, 'package-json-file', {
      filename: `${basePath}/package.json`,
      content: JSON.stringify(
        {
          name: projectName,
          version: '1.0.0',
          main: 'index.js',
          scripts: {
            start: 'node index.js',
          },
        },
        null,
        2
      ),
    });

    // Additional files (e.g., .gitignore) can be created here as separate resources
    // or managed independently according to your needs.
  }
}
```

* The construct pattern makes it easy to reuse folder/file creation across multiple projects.
* Exposing resource references (like `readMeFile`) allows other constructs or stacks to consume outputs if needed.

## Application entrypoint

After defining constructs and stacks, create the app and synthesize the Terraform configuration:

```typescript theme={null}
import { App } from 'cdktf';

const app = new App();
new MyStack(app, 'cdktf-project-builder');
app.synth();
```

Synthesis converts your CDKTF TypeScript code into a Terraform JSON configuration that Terraform can apply.

<Frame>
  <img alt="A slide titled &#x22;Benefits&#x22; with three colored rounded boxes numbered 01–03 listing: &#x22;Reduces manual errors,&#x22; &#x22;Saves time,&#x22; and &#x22;Increases productivity.&#x22;" />
</Frame>

## What we covered

* Adding and using providers and resources in CDKTF.
* Encapsulating related resources using constructs for better organization and reuse.
* Exposing outputs and checking them to verify created resources.
* Synthesizing CDKTF code to Terraform configuration for validation and deployment.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with an aqua gradient panel on the left and three colored markers down a center divider listing &#x22;01 Providers & Resources,&#x22; &#x22;02 Outputs,&#x22; and &#x22;03 Constructs.&#x22; The right side is mostly white space for content." />
</Frame>

## Practical recommendations and best practices

| Topic         | Recommendation                                      | Example / Notes                                                                         |
| ------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Project setup | Start from a tested boilerplate or run `cdktf init` | Avoid redoing TypeScript/CDKTF configuration for each project.                          |
| Reusability   | Use constructs to group related resources           | Create `ProjectFolder`, `Network`, `Database` constructs and compose them.              |
| Type safety   | Declare typed props and interfaces                  | Use interfaces like `ProjectFolderProps` to get autocompletion and compile-time checks. |
| Modularity    | Break functionality across constructs and stacks    | Design constructs to be small and focused so they can be recombined.                    |
| Validation    | Synthesize and validate frequently                  | `yarn cdktf synth` converts your code into Terraform JSON to catch issues early.        |

* Break constructs into logical units and pass outputs as required between constructs or stacks for larger deployments.
* When managing files, decide whether to create `.gitignore` and other files inside the construct or manage them independently—both approaches are valid depending on your workflow.

<Callout icon="lightbulb">
  Run `yarn cdktf synth` frequently during development to validate your CDKTF code quickly.
</Callout>

## Final notes

This example is intentionally small—creating local folders and files could be done with a shell script—but it demonstrates the CDKTF fundamentals: providers, resources, constructs, type-safe props, and synthesis. These fundamentals scale to more complex, cloud-based infrastructure automation where the benefits of type safety, reusability, and testability become even more valuable.

Further reading and references:

* CDK for Terraform (CDKTF) docs: [https://developer.hashicorp.com/terraform/cdktf](https://developer.hashicorp.com/terraform/cdktf)
* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Constructs programming model: [https://github.com/aws/constructs](https://github.com/aws/constructs)

This concludes the introduction to CDKTF. Future modules will cover more advanced construct composition, cross-stack outputs, and multi-component deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/948c0a82-faa1-4f16-83d1-8ee8df2336b3/lesson/89a73ddb-a522-41d5-9a1b-bd2d77ead829" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/cdk-for-terraform-with-typescript/module/948c0a82-faa1-4f16-83d1-8ee8df2336b3/lesson/7a594043-5778-437f-9a97-a931b11b3ef3" />
</CardGroup>
