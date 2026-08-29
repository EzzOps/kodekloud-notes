# Logfile created on 2025-05-21 18:19:51 +0000 by logger.rb/v1.6.0
I, [2025-05-21T18:19:51.860944 #1]  INFO -- : Using GitHub Features: Defaults
I, [2025-05-21T18:19:51.860996 #1]  INFO -- : Auditing 'http://139.84.149.83:8080/'
I, [2025-05-21T18:19:51.943207 #1]  INFO -- : request: GET http://139.84.149.83:8080/api/json?tree=jobs%5Bname%2Curl%2CfullName%5D
I, [2025-05-21T18:19:52.061601 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:52.062902 #1]  INFO -- : Thread collection size: 2
I, [2025-05-21T18:19:52.065400 #1]  INFO -- : request: GET http://139.84.149.83:8080/job/ci-pipeline-poll-scm/config.xml
I, [2025-05-21T18:19:52.065912 #1]  INFO -- : request: GET http://139.84.149.83:8080/job/Generate%20ASCII%20Artwork/config.xml
I, [2025-05-21T18:19:52.256241 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:52.547983 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:52.555698 #1]  INFO -- : request: GET http://139.84.149.83:8080/job/scripted-pipeline/config.xml
I, [2025-05-21T18:19:52.645484 #1]  INFO -- : request: GET REDACTED://api.github.com/repos/jenkins-demo-org/solar-system/contents/Jenkinsfile?ref=
I, [2025-05-21T18:19:52.645989 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:52.663528 #1]  INFO -- : request: GET http://139.84.149.83:8080/job/solar-system-ci-pipeline/config.xml
I, [2025-05-21T18:19:52.746682 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:52.751625 #1]  INFO -- : request: GET REDACTED://api.github.com/repos/jenkins-demo-org/solar-system/contents/Jenkinsfile?ref=
I, [2025-05-21T18:19:53.093094 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:53.094349 #1]  INFO -- : request: POST http://139.84.149.83:8080/pipeline-model-converter/toJson
I, [2025-05-21T18:19:53.152165 #1]  INFO -- : response: Status 200
I, [2025-05-21T18:19:53.153487 #1]  INFO -- : request: POST http://139.84.149.83:8080/pipeline-model-converter/toJson
...
D, [2025-05-21T18:19:58.553745 #1] DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::Defaults]: Failed to locate transformer
D, [2025-05-21T18:19:58.557727 #1] DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::RunsOn]: Located transformer
D, [2025-05-21T18:19:58.560897 #1] DEBUG -- : [Transformers::Jenkins::JenkinsfilePipeline::DeclarativePipeline::Container]: Failed to locate transformer
...
I, [2025-05-21T18:19:58.853152 #1] INFO -- : Output file(s):
I, [2025-05-21T18:19:58.944499 #1] INFO -- : tmp/audit/ci-pipeline-poll-scm/.github/workflows/ci-pipeline-poll-scm.yml
I, [2025-05-21T18:19:58.946512 #1] INFO -- : tmp/audit/ci-pipeline-poll-scm/config.json
I, [2025-05-21T18:19:58.948044 #1] INFO -- : tmp/audit/ci-pipeline-poll-scm/jenkinsfile
I, [2025-05-21T18:19:58.949097 #1] INFO -- : tmp/audit/Generate ASCII Artwork/.github/workflows/generate_ascii_artwork.yml
I, [2025-05-21T18:19:58.950993 #1] INFO -- : tmp/audit/Generate ASCII Artwork/config.json
I, [2025-05-21T18:19:58.954993 #1] INFO -- : tmp/audit/scripted-pipeline/error.txt
I, [2025-05-21T18:19:58.955692 #1] INFO -- : tmp/audit/scripted-pipeline/config.json
I, [2025-05-21T18:19:59.044062 #1] INFO -- : tmp/audit/solar-system-ci-pipeline/.github/workflows/solar-system-ci-pipeline.yml
I, [2025-05-21T18:19:59.045809 #1] INFO -- : tmp/audit/solar-system-ci-pipeline/config.json
I, [2025-05-21T18:19:59.048992 #1] INFO -- : tmp/audit/solar-system-ci-pipeline/jenkinsfile
I, [2025-05-21T18:19:59.864090 #1] INFO -- : tmp/audit/workflow_usage.csv
I, [2025-05-21T18:19:59.961311 #1] INFO -- : tmp/audit/audit_summary.md
W, [2025-05-21T18:20:20.571659 #1] WARN -- : Secrets redacted in file(s):
W, [2025-05-21T18:20:20.571857 #1] WARN -- : tmp/audit/Generate_ASCII_Artwork/.github/workflows/generate_ascii_artwork.yml
W, [2025-05-21T18:20:20.571952 #1] WARN -- : tmp/audit/Generate_ASCII_Artwork/config.json
W, [2025-05-21T18:20:20.572034 #1] WARN -- : tmp/audit/ci-pipeline-poll-scm/config.json
W, [2025-05-21T18:20:20.572233 #1] WARN -- : tmp/audit/solar-system-ci-pipeline/config.json
W, [2025-05-21T18:20:20.572721 #1] WARN -- : tmp/audit/log/valet-20250521-181951.log
I, [2025-05-21T18:20:20.574730 #1] INFO -- : request: GET https://api.github.com/user
```

What the audit produces

The audit writes a directory per job under `tmp/audit/`. Typical contents include:

| File / Path               | Purpose                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| `.github/workflows/*.yml` | Generated GitHub Actions workflow(s) for the job                       |
| `config.json`             | JSON representation of the Jenkins job config (converted `config.xml`) |
| `jenkinsfile`             | The original Jenkinsfile (if available)                                |
| `error.txt`               | Conversion error report for jobs that could not be parsed/converted    |
| `workflow_usage.csv`      | CSV report summarizing workflow usage across jobs                      |
| `audit_summary.md`        | Human-readable audit summary document                                  |

Generate ASCII Artwork — config.json

The exporter translates the Jenkins job configuration into JSON. For this job the `config.json` shows a shell builder that calls an external Advice API.

```json theme={null}
{
  "project": {
    "actions": null,
    "description": "Generate ASCII Artwork using Cowsay library and AdviceSlip Rest API",
    "keepDependencies": "false",
    "properties": null,
    "scm": {
      "class": "hudson.scm.NullSCM"
    },
    "canRoam": "true",
    "disabled": "false",
    "blockBuildWhenDownstreamBuilding": "false",
    "blockBuildWhenUpstreamBuilding": "false",
    "triggers": null,
    "concurrentBuild": "true",
    "builders": [
      {
        "hudson.tasks.Shell": {
          "command": "# Build a message by invoking ADVICESLIP API\ncurl -s REDACTED://api.adviceslip.com/advice > adv",
          "configuredLocalRules": null
        }
      }
    ],
    "publishers": null,
    "buildWrappers": "null"
  }
}
```

Generate ASCII Artwork — generated GitHub Actions workflow

The importer generated a GitHub Actions workflow that preserves job intent: run on Ubuntu, checkout code, query the Advice API, validate word count, install `cowsay`, and print the message with a random cow. Note how filenames were normalized (e.g., writing to `advice.json`) to match the generated workflow layout.

```yaml theme={null}
name: Generate_ASCII_Artwork
on:
  workflow_dispatch:
jobs:
  build:
    runs-on:
      - ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: run command
        shell: bash
        run: |-
          # Build a message by invoking ADVICESLIP API
          curl -s REDACTED://api.adviceslip.com/advice > advice.json
          cat advice.json
          # Test to make sure the advice message has more than 5 words.
          cat advice.json | jq -r .slip.advice > advice.message
          [ $(wc -w < advice.message) -gt 5 ] && echo "Advice has more than 5 words" || (echo "Advice - $(cat advice.message)")
          # Deploy
          sudo apt-get install cowsay -y
          echo $PATH
          export PATH="$PATH:/usr/games:/usr/local/games"
          cat advice.message | cowsay -f $(ls /usr/share/cowsay/cows | shuf -n 1)
```

Tip: After import, verify the generated workflow in the target repository and adjust filenames, environment variables, or permissions as needed.

ci-pipeline-poll-scm — config.json (declarative pipeline metadata)

Declarative (pipeline model) jobs include plugin metadata and trigger information in `config.json`. The Jenkins SCM trigger shows up as a cron-like schedule in the JSON:

```json theme={null}
{
  "flow-definition": {
    "plugin": "workflow-job@1520.v56d65e3b_4566",
    "actions": [
      {
        "org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction": {
          "plugin": "pipeline-model-definition@2.2255.v56a_15e805f12"
        }
      },
      {
        "org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction": {
          "plugin": "pipeline-model-definition@2.2255.v56a_15e805f12",
          "jobProperties": null,
          "triggers": null,
          "parameters": null,
          "options": null
        }
      }
    ],
    "description": null,
    "keepDependencies": "false",
    "properties": [
      {
        "org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty": {
          "triggers": [
            {
              "hudson.triggers.SCMTrigger": {
                "spec": "0 0 * * *",
                "ignorePostCommitHooks": "false"
              }
            }
          ]
        }
      }
    ]
  }
}
```

ci-pipeline-poll-scm — generated GitHub Actions workflow (partial)

The importer converts many declarative pipeline constructs into Actions equivalents. However, when a Jenkins step or plugin has no matching transformer, the tool inserts commented YAML blocks marked with "This item has no matching transformer". These commented sections indicate items that must be migrated manually or addressed by implementing custom transformers.

```yaml theme={null}
name: ci-pipeline-poll-scm
on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 0 * * *'
env:
  MONGO_URI: mongodb+srv://supercluster.d83jj.mongodb.net/superData
#  # This item has no matching transformer
#  MONGO_DB_CREDS:
#  # This item has no matching transformer
#  MONGO_USERNAME:
#  # This item has no matching transformer
jobs:
  Installing_Dependencies:
    name: Installing Dependencies
    runs-on:
      - self-hosted
      - us-west-1-ubuntu-22
    container:
      image: node:24

# Example of commented-out transformer output (illustrative — importer reports these as unmapped)
# This item has no matching transformer
# - dependencyCheck:
#   - key: additionalArguments
#     value:
#       isLiteral: true
#       value: "\n                      --scan './' \n                      --out './' \n                      --format
# - key: nvdCredentialsId
#   value:
#     isLiteral: true
#     value: owasp-dependency-check
# - key: odcInstallation
#   value:
#     isLiteral: true
#     value: OWASP-DepCheck-10
# This item has no matching transformer
# - dependencyCheckPublisher:
#   - key: failedTotalCritical
#     value:
#       isLiteral: true
#       value: 1
# - key: pattern
#   value:
#     isLiteral: true
#     value: dependency-check-report.xml
# - key: stopBuild
#   value:
#     isLiteral: true
#     value: true
```

When you encounter commented sections like these, plan to either:

* Implement a custom transformer to map the Jenkins plugin to a GitHub Action, or
* Rework that pipeline step manually in the generated workflow using equivalent Actions or scripts.

Scripted pipeline — config.json and error.txt

Scripted (CPS) Jenkins pipelines are not supported by the importer. For jobs using scripted pipelines the audit still saves the `config.json` (so you have the original pipeline script and metadata) and writes an `error.txt` describing the limitation.

> **warning** Scripted Jenkins pipelines are not supported by the importer. Jobs using scripted pipelines must be migrated manually to GitHub Actions or rewritten as declarative pipelines for automated conversion.

Example `config.json` captured for a scripted pipeline:

```json theme={null}
{
  "flow-definition": {
    "plugin": "workflow-job@1520.v56d65e3b_4566",
    "actions": null,
    "description": null,
    "keepDependencies": "false",
    "properties": null,
    "definition": {
      "class": "org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition",
      "plugin": "workflow-cps@4106.v7a_8a_8176d450",
      "script": "node {  // Runs on any available agent\n    stage('Greet') {\n      echo 'Hello, World!'\n    }\n",
      "sandbox": "true"
    },
    "triggers": null,
    "disabled": "false"
  }
}
```

Corresponding `error.txt` produced by the importer:

```text theme={null}
Unable to parse Jenkins pipeline. Scripted pipelines are not currently supported.
Pipeline type: flow-definition
Message: Jenkins scripted pipelines are not supported
```

This limitation means scripted pipelines require manual conversion efforts — either rewrite as declarative or design equivalent GitHub Actions workflows.

Best practices and next steps

* Start with declarative pipelines and plugin-dependent steps; those convert more cleanly.
* Inspect `tmp/audit/<job>/` for each job: review `.github/workflows/*.yml`, resolve commented/unmapped sections, and adjust secrets or environment variables.
* For jobs with `error.txt`, plan a manual migration or pipeline refactor to declarative form.
* Consider implementing custom transformers for frequently-used proprietary plugins to automate parts of the migration.

Quick checklist

| Action                           | Why                                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| Review `.github/workflows/*.yml` | Ensure generated workflows run in the target repository and adjust runner/container settings |
| Inspect `config.json`            | Confirm plugin metadata and triggers were captured                                           |
| Open `error.txt` (if present)    | Understand conversion failures and plan manual migration                                     |
| Replace/commented sections       | Implement custom transformers or manual workflow steps for unsupported plugins               |
| Validate secrets                 | Confirm redactions and move sensitive data into GitHub Secrets or OIDC solutions             |

Links and references

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Pipeline Model Definition Plugin (Jenkins)](https://plugins.jenkins.io/pipeline-model-definition/)
* Consider scanning or auditing generated workflows with repository-specific CI checks and tests after import.

Summary

* The audit fetches Jenkins job configurations and Jenkinsfiles, calls the pipeline-model-converter to produce an intermediate JSON representation, and writes converted artifacts into `tmp/audit/<job>/`.
* Per-job output commonly includes `.github/workflows/*.yml`, `config.json`, `jenkinsfile`, and `error.txt` (for failed conversions).
* Declarative pipelines convert best; plugin-specific or unsupported features are left commented in the generated YAML and require manual attention or custom transformers.
* Scripted pipelines are not automatically converted and must be migrated manually.

That's all for now.

- [Watch Video](https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/0d5d266b-347a-427c-a6ec-ffdede9021cf)


# Dry run

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Dry-run/page

Explains how to perform a dry-run conversion of Jenkins pipelines to GitHub Actions workflows, generating workflows locally for review without modifying the repository.

A dry-run simulates converting a Jenkins pipeline into GitHub Actions workflows without changing your repository. It writes the generated workflow files to an output directory you specify but does not open pull requests or modify existing configuration. This is a safe way to inspect the importer's translation of Jenkins constructs into GitHub Actions before applying any changes.

<Frame>
  <img alt="A presentation slide titled &#x22;Dry-run&#x22; with a highlighted line reading: &#x22;A safe, non-disruptive way to simulate converting a Jenkins pipeline into a GitHub Actions workflow.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

> **lightbulb** Use dry-run to verify how Jenkins pipeline constructs (agents, environment, stages/steps) are mapped to GitHub Actions concepts (`runs-on`, `env`, jobs/steps) before committing any changes.

> **warning** Always provide the full Jenkins job URL and an output directory you control. The dry-run will not change your repo, but incorrect URLs or output paths can cause confusing results or missed files.

## Command usage

Provide the Jenkins job URL and an output directory to write the generated workflows:

```bash theme={null}
gh actions-importer dry-run jenkins --url "https://jenkins.example.com/job/my-job/" --output-dir "./output"
```

Be sure to use the full Jenkins job URL (including `/job/<name>/` where applicable) and an output directory path that you control.

## What the dry-run produces

The dry-run generates files representing the GitHub Actions workflows equivalent to the given Jenkins pipeline. It preserves any items that the importer cannot automatically translate as commented entries in the YAML output so you can review them and implement custom handling.

Below is an example showing an original Jenkins Declarative Pipeline and the generated GitHub Actions workflow produced by a dry-run.

Original Jenkins pipeline (Declarative Pipeline syntax):

```groovy theme={null}
pipeline {
    agent {
        label 'TeamARunner'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE = 'sqlite'
    }

    stages {
        stage('build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                sleep 80
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
            }
        }
        stage('test') {
            steps {
                junit '**/target/*.xml'
            }
        }
    }
}
```

Generated GitHub Actions workflow (YAML). Notice how `environment` and `agent.label` map to `env` and `runs-on`. Items the importer could not translate (for example, `sleep 80`) are left as commented placeholders near where they would have been handled.

```yaml theme={null}
name: test_pipeline
on:
  push:
env:
  DISABLE_AUTH: 'true'
  DB_ENGINE: sqlite
jobs:
  build:
    runs-on:
      - self-hosted
      - TeamARunner
    steps:
      - name: checkout
        uses: actions/checkout@v2
      - name: echo message
        run: echo "Database engine is ${{ env.DB_ENGINE }}"
