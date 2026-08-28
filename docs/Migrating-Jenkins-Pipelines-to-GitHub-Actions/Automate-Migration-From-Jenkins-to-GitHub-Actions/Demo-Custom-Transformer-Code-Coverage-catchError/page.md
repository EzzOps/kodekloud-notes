# Example placeholder (replace with the actual token you generated)
GITHUB_PAT=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Create a Jenkins API token

1. Log into your Jenkins instance as the user the importer will use (example: `siddharth`).
2. Navigate to the user’s Security / API Token section.
3. Create a new token (for example, `GH Importer 2`).
4. Copy the generated token and store it in a secure secret store.

<Frame>
  <img alt="A screenshot of the Jenkins Security settings page showing API token management, with an existing token listed and a field to create a new token. The lower part shows masked password and confirm-password fields and Save/Apply buttons." />
</Frame>

Example placeholder (store securely; never post real tokens publicly):

```text theme={null}
# Example placeholders (replace with the actual values you generated)
JENKINS_API_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
JENKINS_USERNAME=siddharth
JENKINS_BASE_URL=http://139.84.149.83:8080/
GITHUB_BASE_URL=https://github.com
```

## Configure the GitHub Actions Importer

Run the interactive configure command and follow the prompts to provide the tokens and base URLs:

```bash theme={null}
gh actions-importer configure
```

Illustrative interactive session:

```text theme={null}
✓ Which CI providers are you configuring?: Jenkins
Enter the following values (leave empty to omit):
✓ Personal access token for GitHub: *******************************
✓ Base url of the GitHub instance: https://github.com
✓ Personal access token for Jenkins: *******************************
✓ Username of Jenkins user: siddharth
✓ Base url of the Jenkins instance: http://139.84.149.83:8080/
Environment variables successfully updated.
```

<Callout icon="lightbulb">
  Store generated tokens securely (for example, in a credential manager or an encrypted secrets store). Avoid copying tokens into unencrypted text files or source control.
</Callout>

## Next steps

You have now configured the GitHub Actions Importer with credentials for your Jenkins CI server. Next, run an audit to analyze your Jenkins CI/CD footprint and plan the migration:

```bash theme={null}
gh actions-importer audit --provider jenkins --base-url http://139.84.149.83:8080/
```

## Links and references

* GitHub: Create a personal access token (classic) — [https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
* Jenkins: API token documentation — [https://www.jenkins.io/redirect/user-admin/#api-token](https://www.jenkins.io/redirect/user-admin/#api-token)
* GitHub Actions Importer extension (repository) — [https://github.com/github/gh-actions-importer](https://github.com/github/gh-actions-importer)

By following these steps you’ll ensure the GitHub Actions Importer has the required, securely-stored credentials to interact with both GitHub and your Jenkins instance.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/5414377c-c286-47e4-a377-602efa278f5c" />
</CardGroup>


# Demo Custom Transformer Code Coverage catchError

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-Code-Coverage-catchError/page

Demonstrates a custom transformer that converts Jenkins catchError wrapping a code coverage step into GitHub Actions steps preserving continue on error behavior and HTML artifact upload

In this lesson we build a custom transformer to convert a Jenkins `catchError` wrapper used in a Code Coverage stage into equivalent GitHub Actions steps. Jenkins's `catchError` lets a failing step continue the pipeline while setting a specific build or stage result. When migrating to GitHub Actions we want the workflow to run the same coverage command, continue on error so downstream jobs still run, and preserve HTML artifacts for later inspection.

This article walks through the original Jenkins stage, the parsed AST-like representation the importer prints in dry-run, the Ruby transformer implementation, the importer dry-run invocation and output, the generated GitHub Actions job snippet, and the run results.

## Jenkinsfile snippet (Code Coverage stage — original)

```groovy theme={null}
stage('Code Coverage') {
    agent {
        docker {
            image 'node:24'
            args '-u root:root'
        }
    }
    steps {
        catchError(buildResult: 'SUCCESS', message: 'Oops! it will be fixed in future releases', stageResult: 'UNSTABLE') {
            sh 'npm run coverage'
        }
        publishHTML([
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'coverage/lcov-report',
            reportFiles: 'index.html',
            reportName: 'Code Coverage'
        ])
    }
}
```

## What the importer sees (AST-like JSON)

Run the importer in dry-run mode to print parsed identifiers and their arguments. In this case the importer detected a `catchError` node whose child is a `sh` invocation of the coverage command.

Sample parsed representation for `catchError` (converted to valid JSON for clarity):

```json theme={null}
{
  "name": "catchError",
  "arguments": [
    {
      "key": "buildResult",
      "value": { "isLiteral": true, "value": "SUCCESS" }
    },
    {
      "key": "message",
      "value": { "isLiteral": true, "value": "Oops! it will be fixed in future releases" }
    },
    {
      "key": "stageResult",
      "value": { "isLiteral": true, "value": "UNSTABLE" }
    }
  ],
  "children": [
    {
      "name": "sh",
      "arguments": [
        {
          "key": "script",
          "value": { "isLiteral": true, "value": "npm run coverage" }
        }
      ]
    }
  ]
}
```

## Approach — desired mapping to GitHub Actions

Goal: mirror Jenkins behavior so coverage failures do not block the pipeline, but HTML reports are still produced and uploaded.

Steps:

* Extract the inner coverage command from `item.dig("children", 0, "arguments", 0, "value", "value")`.
* Fall back to `npm run coverage` if the command is not found.
* Emit two GitHub Actions steps:
  1. Install dependencies: `npm install --no-audit`.
  2. Run coverage: set `continue-on-error: true` so the workflow continues even if the command exits non‑zero.
* Let the existing importer conversion handle `publishHTML` → `actions/upload-artifact@v4` (artifact upload of the coverage HTML).

## Transformer implementation (helper-transformer.rb)

The transformer below is added to the importer's custom transformers so that `catchError` nodes are converted into a lightweight sequence of GitHub Actions steps.

```ruby theme={null}
