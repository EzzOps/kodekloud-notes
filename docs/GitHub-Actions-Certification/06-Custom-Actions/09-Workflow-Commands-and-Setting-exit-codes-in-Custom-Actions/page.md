# .github/actions/my-composite/action.yml
name: "My Composite Action"
description: "Install deps, run tests, and lint code"
runs:
  using: composite
  steps:
    - name: Checkout code
      uses: actions/checkout@v3
    - name: Install dependencies
      run: npm ci
    - name: Run tests
      run: npm test
```

* **Pros**: Simplifies workflows, DRY principle, cross-platform
* **Cons**: Can become hard to maintain if too many steps are bundled

## Docker Container Actions

Container Actions run inside a Docker environment defined by you.

```dockerfile theme={null}
# .github/actions/my-docker/Dockerfile
FROM node:16
RUN npm install -g aws-cli
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```yaml theme={null}
# .github/actions/my-docker/action.yml
name: "My Docker Action"
runs:
  using: docker
  image: Dockerfile
  args:
    - "--region"
    - "us-east-1"
```

* **Pros**: Full OS control, consistent environment, ideal for complex dependencies
* **Cons**: Linux only, requires Docker knowledge, startup overhead

> **triangle-alert** Docker container Actions run exclusively on Linux runners. Make sure your workflow requirements align with Linux-only execution.

## JavaScript Actions

JavaScript Actions execute directly on the runner via Node.js.

```javascript theme={null}
// .github/actions/my-js-action/index.js
import core from "@actions/core";

async function run() {
  try {
    const name = core.getInput("name");
    core.info(`Hello, ${name}!`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
```

```yaml theme={null}
# .github/actions/my-js-action/action.yml
name: "My JS Action"
runs:
  using: "node16"
  main: "index.js"
inputs:
  name:
    description: "Your name"
    required: true
```

* **Pros**: Fast startup, cross-platform, simple scripting
* **Cons**: Less isolated—be mindful of side effects on the host runner

| Criteria               | Composite | Docker Container | JavaScript |
| ---------------------- | --------- | ---------------- | ---------- |
| Speed                  | Fast      | Moderate         | Fastest    |
| Isolation              | Low       | High             | Medium     |
| Cross-platform support | Yes       | No               | Yes        |
| Maintenance overhead   | Moderate  | High             | Low        |

Select the type that best aligns with your project’s needs—whether you prioritize simplicity, isolation, performance, or cross-platform support.

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Creating a composite run steps action](https://docs.github.com/actions/creating-actions/creating-a-composite-run-steps-action)
* [Docker container actions](https://docs.github.com/actions/creating-actions/creating-a-docker-container-action)
* [JavaScript actions](https://docs.github.com/actions/creating-actions/creating-a-javascript-action)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions-certification/module/428391ee-45d0-4e9c-9e06-78d0c5ff7657/lesson/171274e9-ecd7-42a2-8206-53fd50b9c0cc)


# Workflow Commands and Setting exit codes in Custom Actions

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/Workflow-Commands-and-Setting-exit-codes-in-Custom-Actions/page

This guide covers GitHub Actions workflow commands, variable management, logging, and exit codes for custom actions in JavaScript and Docker.

In this guide, you’ll dive into **GitHub Actions workflow commands**, learn how to export variables, emit logs, and manage **exit codes** in both JavaScript and Docker-based custom actions. Whether you’re writing a simple workflow file or building a full-fledged action with the [Actions Toolkit](https://github.com/actions/toolkit), these patterns will help you create robust CI/CD pipelines.

## Table of Contents

* [Workflow Commands](#workflow-commands)
  * [Setting Environment Variables](#setting-environment-variables)
  * [Defining Step Outputs](#defining-step-outputs)
  * [Emitting Debug Messages](#emitting-debug-messages)
* [Actions Toolkit Library](#actions-toolkit-library)
* [Using `@actions/core`](#using-actionscore)
  * [Inputs and Outputs](#inputs-and-outputs)
  * [Logging and Messages](#logging-and-messages)
  * [Environment Variables and Secrets](#environment-variables-and-secrets)
* [Exit Codes in Custom Actions](#exit-codes-in-custom-actions)
  * [JavaScript Actions](#javascript-actions)
  * [Docker Container Actions](#docker-container-actions)
* [Links and References](#links-and-references)

***

## Workflow Commands

Workflow commands let you interact with the runner environment—setting variables, emitting outputs, grouping logs, and more. You can use them directly in your workflow YAML or via the Actions Toolkit for a higher-level API.

### Setting Environment Variables

Append key-value pairs to the special `$GITHUB_ENV` file to make them available in all subsequent steps:

```yaml theme={null}
- name: Export AWS region
  run: echo "AWS_REGION=us-east-1" >> $GITHUB_ENV
```

After this step, `$AWS_REGION` can be referenced in later steps:

```yaml theme={null}
- name: Show AWS region
  run: echo "Region is $AWS_REGION"
```

### Defining Step Outputs

To pass dynamic values between steps, write to `$GITHUB_OUTPUT`:

```yaml theme={null}
- name: Compute and export result
  id: compute
  run: |
    result=$(( 42 + 25 ))
    echo "RESULT=$result" >> $GITHUB_OUTPUT
```

Consume the output in another step:

```yaml theme={null}
- name: Use computed result
  run: echo "The result was ${{ steps.compute.outputs.RESULT }}"
```

### Emitting Debug Messages

Debug logs are only visible when you enable debug mode (`ACTIONS_STEP_DEBUG`):

```yaml theme={null}
- name: Log debug info
  run: echo "::debug::Current build number is $BUILD_NUMBER"
```

> **lightbulb** Enable debug logging by setting `ACTIONS_STEP_DEBUG` to `true` in your repository’s secrets.

For a full list of workflow commands (grouping, warnings, notices, and more), see the [official GitHub Actions documentation](https://docs.github.com/en/actions/learn-github-actions/workflow-commands-for-github-actions).

***

## Actions Toolkit Library

The [Actions Toolkit](https://github.com/actions/toolkit) provides JavaScript and TypeScript libraries that wrap raw workflow commands into secure, well-tested APIs. Below are the most commonly used packages:

| Package             | Purpose                                                  |
| ------------------- | -------------------------------------------------------- |
| @actions/core       | Core functions for inputs, outputs, logging, and secrets |
| @actions/github     | Octokit client with workflow context                     |
| @actions/exec       | Execute commands with streamed stdout/stderr             |
| @actions/io         | File system operations (copy, move, remove)              |
| @actions/tool-cache | Download and manage tools for your workflow              |

![The image lists various components of the GitHub Actions toolkit library, each with an icon and a corresponding URL. It includes links like @actions/core, @actions/exec, and others, with a reference to the GitHub repository.](https://kodekloud.com/kk-media/image/upload/v1752876098/notes-assets/images/GitHub-Actions-Certification-Workflow-Commands-and-Setting-exit-codes-in-Custom-Actions/github-actions-toolkit-components-list.jpg)

Refer to the [Actions Toolkit docs](https://github.com/actions/toolkit) for detailed examples and best practices.

***

## Using `@actions/core`

The `@actions/core` package offers three main feature sets for building custom JavaScript actions.

### Inputs and Outputs

```typescript theme={null}
getInput(name: string, options?: { required?: boolean }): string
getBooleanInput(name: string, options?: { required?: boolean }): boolean
getMultilineInput(name: string, options?: { required?: boolean }): string[]
setOutput(name: string, value: any): void
```

* **getInput**, **getBooleanInput**, **getMultilineInput**: Read user-defined inputs from `action.yml`.
* **setOutput**: Emit step outputs for consumption in downstream steps.

### Logging and Messages

```typescript theme={null}
setFailed(message: string): void
warning(message: string): void
error(message: string): void
info(message: string): void
notice(message: string): void
debug(message: string): void
isDebug(): boolean
startGroup(name: string): void
endGroup(): void
```

* **setFailed**: Fails the action and sets exit code to 1.
* **warning**, **error**, **notice**, **info**, **debug**: Emit logs at various levels.
* **startGroup** / **endGroup**: Collapse related log lines into a group.

### Environment Variables and Secrets

```typescript theme={null}
exportVariable(name: string, value: any): void
setSecret(secret: string): void
```

* **exportVariable**: Equivalent to writing to `$GITHUB_ENV`.
* **setSecret**: Masks sensitive values in workflow logs.

![The image is a diagram of the actions/core package, showing functions categorized under "Inputs and Outputs," "Logging and Messages," and "Environment and Secrets." Functions include getInput, setOutput, setFailed, debug, and exportVariable.](https://kodekloud.com/kk-media/image/upload/v1752876099/notes-assets/images/GitHub-Actions-Certification-Workflow-Commands-and-Setting-exit-codes-in-Custom-Actions/actions-core-package-functions-diagram.jpg)

***

## Exit Codes in Custom Actions

GitHub Actions interprets the exit code of each step to decide success or failure:

* **0**: Success — runner continues with downstream steps.
* **Non-zero**: Failure — runner halts concurrent jobs and skips subsequent steps.

> **triangle-alert** Always handle errors and set exit codes explicitly. A forgotten error can cause unexpected pipeline success.

![The image explains exit codes in custom actions, showing a green checkmark for successful actions with an exit code of zero, and a red cross for failed actions with non-zero exit codes.](https://kodekloud.com/kk-media/image/upload/v1752876100/notes-assets/images/GitHub-Actions-Certification-Workflow-Commands-and-Setting-exit-codes-in-Custom-Actions/exit-codes-custom-actions-checkmark-cross.jpg)

### JavaScript Actions

Use `core.setFailed` to log the error and exit with code 1:

```javascript theme={null}
const core = require('@actions/core');

try {
  // Your custom logic here
} catch (error) {
  core.setFailed(error.message);
}
```

### Docker Container Actions

In your `entrypoint.sh`, leverage shell exit codes:

```bash theme={null}
#!/bin/sh
if [ -z "$INPUT_SOME_PARAM" ]; then
  echo "Missing required input: some-param" >&2
  exit 1
fi
