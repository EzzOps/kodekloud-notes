# example file paths or URLs the plugin can load from:
# /var/jenkins_home/casc_config/jenkins.yaml
# https://acme.org/jenkins.yaml
# accepted extensions: .yml, .yaml, .YAML
# environment option: casc.jenkins.config
JENKINS_JAVA_OPTIONS: "-Dcasc.jenkins.config=/jenkins/casc_configs"
# default fallback:
# $JENKINS_HOME/jenkins.yaml
```

After installing the plugin you may need to restart Jenkins. Once back up, go to Manage Jenkins → Configuration as Code. From that page you can:

* View the current configuration exported to YAML (auto-generated from the running instance).
* Point Jenkins to a file path, HTTP(S) URL, or Git repository with the YAML and apply it.
* Download the current configuration, reload a configuration, or inspect links to documentation and the JSON schema.

## Viewing the current configuration (auto-generated YAML)

When you click "View Configuration" JCasC renders a comprehensive YAML representation of the running Jenkins instance. The YAML includes core settings, tool installations, credentials, plugin global configuration (under `unclassified`), and more.

Representative excerpt for top-level and core settings:

```yaml theme={null}
providerFilter: "none"
typeFilter: "none"
appearance:
  pipelineGraphView:
    showGraphOnBuildPage: true
    showGraphOnJobPage: true
prism:
  theme: PRISM
themeManager:
  disableUserThemes: false
  theme: "darkSystem"
security:
  apiToken:
    creationOfLegacyTokenEnabled: false
    tokenGenerationOnCreationEnabled: false
  usageStatisticsEnabled: true
copyartifact:
  mode: PRODUCTION
cps:
  nodeSandbox: false
gitHooks:
  allowedOnAgents: false
  allowedOnController: false
gitHostKeyVerificationConfiguration:
  sshHostKeyVerificationStrategy: "knownHostsFileVerificationStrategy"
ssh:
  port: 1
unclassified:
  audit-trail:
    displayUserName: true
    logBuildCause: true
    logCredentialsUsage: true
  loggers:
    - logFileDailyRotation:
```

Representative excerpt for tool installations:

```yaml theme={null}
name: "Default"
maven:
  installations:
    - name: "M398"
      properties:
        - installSource:
            installers:
              - maven:
                  id: "3.9.8"
mavenGlobalConfig:
  globalSettingsProvider: "standard"
  settingsProvider: "standard"
nodejs:
  installations:
    - name: "nodejs-22-6-0"
      properties:
        - installSource:
            installers:
              - nodeJSInstaller:
                  id: "22.6.0"
  npmPackagesRefreshHours: 72
sonarRunnerInstallation:
  installations:
    - name: "sonarqube-scanner-610"
      properties:
        - installSource:
            installers:
              - sonarRunnerInstaller:
                  id: "6.1.0.4477"
```

## Credentials representation and sensitive data

Credentials are included in the YAML export in declarative form. Sensitive values appear as encrypted blobs or hashed tokens in the generated YAML — the real export hides plaintext secrets.

Representative credentials excerpt (sensitive fields shown as encrypted blobs in real exports):

```yaml theme={null}
credentials:
  system:
    domainCredentials:
      - credentials:
        - usernamePassword:
            description: "Gitea Server Credentials"
            id: "gitea-server-creds"
            username: "gitea-admin"
            password: "{AQAAABAAAAAQA4e7WfYLRu0yZL9NsHsLaqohKKpJFtItDGTyKUsxqCOU=}"
            scope: GLOBAL
        - usernamePassword:
            description: "Credentials for MongoDB"
            id: "mongo-db-credentials"
            username: "superuser"
            password: "{AQAAABAAAAAQFpgIHj2LB26zTPKnU+rDyr/G7Vm9oalKU8x8Rcp0iE0=}"
            scope: GLOBAL
        - string:
            description: "Mongo Database Username"
            id: "mongo-db-username"
            secret: "{AQAAABAAAAAQF0khJHh3HoKSatkFUUT2Y0YBQsY4d8tgCGOfpOBoBk0=}"
            scope: GLOBAL
        - string:
            description: "Mongo Database Password"
            id: "mongo-db-password"
            secret: "{AQAAABAAAAAQpXMp0KYcy2Hmc9h0VksHvChKdk8C9zO7YLPCyZ30t64=}"
            scope: GLOBAL
        - string:
            description: "Sonarqube Server Token"
            id: "sonar-qube-token"
            scope: GLOBAL
```

> **warning** Never store raw plaintext secrets in repository-controlled JCasC YAML. Use Jenkins Credentials, external secret stores, or encrypted credentials. If you must store secrets, ensure they are encrypted and access is tightly controlled.

## What else is included in the YAML export

The JCasC export can include:

* Jenkins core configuration: agent protocols (JNLP, Connect), authorization strategy (Global Matrix, etc.), security realm, system message, node definitions, health monitors, primary view.
* Unclassified section: plugin-specific global configurations such as audit trail, Git servers, SonarQube, Slack notifier, Prometheus, etc.
* Tools: Git, Maven, Node.js, SonarQube scanner, Dependency-Check, and other tool installers.

## Working with a JCasC YAML file on the controller

A common workflow is to export the YAML, edit it, and place the edited file on the Jenkins controller (often under `$JENKINS_HOME` or a mounted volume). Then configure JCasC to point to that file.

Quick example workflow on the Jenkins controller:

```bash theme={null}
# change to a backup or config directory
cd /var/lib/jenkins/JENKINS_BACKUP

# create/edit the JCasC YAML file
vi jenkins-casc.yaml
```

Example change inside `jenkins-casc.yaml` (fragment):

```yaml theme={null}
systemMessage: "Loading data from Jenkins JCasC"
```

Apply the configuration from Manage Jenkins → Configuration as Code:

1. On the Configuration as Code page, set the "Configuration source" to a path or URL Jenkins can read, for example:
   * `file:///var/lib/jenkins/JENKINS_BACKUP/jenkins-casc.yaml`
   * or just `jenkins-casc.yaml` if the plugin can resolve it in your deployment.
2. Click "Apply new configuration." The plugin will validate the YAML first.
3. If the YAML is valid the plugin will report success and show the timestamp when it was loaded.
4. Refresh the Jenkins UI to confirm changes (e.g., updated system message).

If the YAML is invalid, JCasC will block the apply and display validation errors. Fix the reported errors and reapply.

## JSON schema, downloads, and authoring help

* The Configuration as Code page lets you download the current YAML.
* A JSON schema is available and useful for tooling, editors, and programmatic validation of JCasC YAML.

Example start of the JCasC JSON schema:

```json theme={null}
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "description": "Jenkins Configuration as Code",
  "additionalProperties": false,
  "type": "object",
  "properties": {
    "security": {
      "additionalProperties": false,
      "type": "object",
      "title": "Configuration base for the security classifier",
      "properties": {
        "sshHostKeyVerificationStrategy": {
          "oneOf": [
            { "properties": { "nohostKeyVerificationStrategy": { "$id": "#/definitions/org.jenkinsci.plugins.gitclient.verifier.NoHostKeyVerificationStrategy" } } },
            { "properties": { "manuallyProvidedKeyVerificationStrategy": { "$id": "#/definitions/org.jenkinsci.plugins.gitclient.verifier.ManuallyProvidedKeyVerificationStrategy" } } },
            { "properties": { "acceptFirstConnectionStrategy": { "$id": "#/definitions/org.jenkinsci.plugins.gitclient.verifier.AcceptFirstConnectionStrategy" } } },
            { "properties": { "knownHostsFileVerificationStrategy": { "$id": "#/definitions/org.jenkinsci.plugins.gitclient.verifier.KnownhostsFileVerificationStrategy" } } }
          ],
          "type": "object"
        }
      }
    }
  }
}
```

Use the schema with editors that support JSON Schema validation (VS Code, JetBrains IDEs) to get autocompletion and inline validation while authoring JCasC YAML.

## Troubleshooting and validation tips

* Always validate YAML before applying. The JCasC page performs validation and lists problems.
* Check `jenkins.log` for stack traces if applying a configuration fails during runtime.
* When a plugin adds new global settings, reconciling YAML may require updating your config or using plugin-specific sections under `unclassified`.
* For large changes, apply incrementally and verify each step in the UI.

## Best practices

> **lightbulb** Keep your JCasC YAML in version control (Git). Avoid storing raw secrets in YAML; use Jenkins Credentials or an external secrets manager. Use the JCasC JSON schema and plugin documentation when authoring complex configurations to minimize validation errors and drift.

## Summary

Jenkins Configuration as Code (JCasC) converts the GUI-driven configuration surface area of Jenkins and many plugins into a declarative YAML format. You can export the current configuration, store it in version control, edit it for reproducible changes, and instruct Jenkins to apply a configuration file. For non-trivial Jenkins installations with many plugins, credentials, tools, and cloud integrations, JCasC improves maintainability and reproducibility.

Further reading and references:

* Jenkins Configuration as Code (plugin): [https://plugins.jenkins.io/configuration-as-code/](https://plugins.jenkins.io/configuration-as-code/)
* JCasC GitHub repository and examples: [https://github.com/jenkinsci/configuration-as-code-plugin](https://github.com/jenkinsci/configuration-as-code-plugin)
* Jenkins documentation: [https://www.jenkins.io/doc/](https://www.jenkins.io/doc/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/d36dbd91-0d4b-4bfe-adc7-778bf431a362)


# Github Actions Basics

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Github-Actions-Basics/page

Introduction to GitHub Actions explaining workflows, jobs, steps, runners, matrix strategies, and hosted versus self hosted runners for CI/CD and repository automation

Get a concise introduction to GitHub Actions — an integrated automation platform for repositories hosted on GitHub. If your code already lives on GitHub, Actions offers a seamless way to build CI/CD pipelines, run repository automations, and respond to events without adopting an external CI system.

What is GitHub Actions?

GitHub Actions is a flexible automation platform built into GitHub. You define automated processes as workflows using YAML files stored in your repository, and GitHub executes those workflows in response to repository events. With Actions you can:

* Build, test, and deploy code on pushes and pull requests.
* Run checks and analyses (linting, security scans, dependency updates).
* Orchestrate repository automations (comment bots, labeling, notifications).
* Schedule workflows or trigger them from webhooks and other GitHub events.

Workflows and jobs can run on multiple operating systems, including Ubuntu, Windows, and macOS.

<Frame>
  <img alt="A slide titled &#x22;GitHub Actions&#x22; showing three numbered OS icons: Ubuntu (orange), Windows (pink) and MacOS (green). Each OS is shown as a rounded-square logo with the labels &#x22;1&#x22;, &#x22;2&#x22;, and &#x22;3.&#x22;" />
</Frame>

Why choose GitHub Actions?

* Hosted infrastructure managed by GitHub (provisioning, scaling, and maintenance).
* Declarative workflows in YAML that live with your code (`.github/workflows/`).
* Built-in capabilities: dependency caching, artifact storage, and detailed logs.
* Automation reduces manual steps, lowers human error, and accelerates delivery.

Is GitHub Actions only for CI/CD pipelines?

No. CI/CD (build, test, release) is a primary use case, but Actions can run workflows on many repository events — pushes, pull requests, issues, package registry events, and more. For example, when a contributor opens a pull request you can automatically add labels, assign reviewers, post comments, or run security scans.

<Frame>
  <img alt="A GitHub Actions diagram with the GitHub logo over a box labeled &#x22;Automate CI/CD.&#x22; Below it are icons for pipeline steps: Building, Unit Testing, Linting, Dockerizing, Security, Deployment, and Tests." />
</Frame>

Core concepts: workflows, jobs, steps, and runners

* Workflow: an automated process defined in a YAML file stored in `/.github/workflows/`. A repository can contain multiple workflows triggered by different events.
* Job: a group of steps that runs on a single runner. Jobs run in parallel by default unless you specify dependencies with `needs`.
* Step: a single task in a job. Steps run sequentially within a job.
* Runner: the machine (virtual or physical) that executes a job. Runners are either GitHub-hosted or self-hosted.

Quick reference table

| Concept  | Purpose                               | Example                        |
| -------- | ------------------------------------- | ------------------------------ |
| Workflow | Defines automation and triggers       | `/.github/workflows/ci.yml`    |
| Job      | Group of steps that run on one runner | `jobs: build:`                 |
| Step     | Single task (action or command)       | `- name: Install dependencies` |
| Runner   | Execution environment                 | `runs-on: ubuntu-latest`       |

Matrix strategy and parallel jobs

A common pattern uses a matrix strategy to run the same job across multiple OSes or versions. Each matrix entry becomes a separate job executed concurrently on its own runner.

Example: run tests on Ubuntu, macOS, and Windows

```yaml theme={null}
name: My Awesome App
on: push
jobs:
  unit-testing:
    name: Unit Testing
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [16]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

Execution notes

* GitHub provisions a separate runner for each matrix job concurrently (three runners in the example).
* Steps inside a job execute sequentially (checkout → setup → install → test).
* Each matrix job is evaluated independently: a matrix instance’s success or failure is reported separately. The overall workflow succeeds only when all required jobs complete successfully.
* You can view logs, step output, and artifacts for each job in the repository’s Actions tab.

<Frame>
  <img alt="A screenshot of a GitHub Actions run on the left showing jobs and detailed unit-testing steps, and on the right three colored diagrams of GitHub-hosted runners (Windows, Ubuntu, macOS) each performing &#x22;Clone Repo,&#x22; &#x22;Install NodeJS,&#x22; and &#x22;Run Tests.&#x22;" />
</Frame>

Runner types — GitHub-hosted vs. self-hosted

There are two main runner options:

| Runner type   | Pros                                                                                               | Cons                                                                          | When to use                                                                     |
| ------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| GitHub-hosted | No server maintenance; fresh environment per job; common tooling preinstalled                      | Limited control over system-level config; usage subject to GitHub plan limits | Best for typical CI/CD where convenience and low ops overhead matter            |
| Self-hosted   | Full control over OS, installed software, and network access; can access private resources or GPUs | You manage maintenance, scaling, and security                                 | Use when you need custom software, specific hardware, or private network access |

> **lightbulb** Choose GitHub-hosted runners for convenience and low maintenance. Choose self-hosted runners when you need custom software, special hardware, or specific network access that hosted runners can't provide.

<Frame>
  <img alt="An infographic titled &#x22;Runner Types&#x22; that compares GitHub-hosted Runners (green) and Self-hosted Runners (orange) with icons and bullet-pointed features and trade-offs. The bottom shows colored buttons for Workflow, Jobs, Steps, and Runners." />
</Frame>

Summary and next steps

This article covered the essentials of GitHub Actions: what it is, how workflows, jobs, steps, and runners relate, how matrix jobs enable parallel runs across OSes, and the differences between GitHub-hosted and self-hosted runners. Use these fundamentals to design CI/CD workflows and repository automations.

Further reading and references

* GitHub Actions docs: [https://docs.github.com/actions](https://docs.github.com/actions)
* Actions marketplace: [https://github.com/marketplace?type=actions](https://github.com/marketplace?type=actions)
* actions/checkout: [https://github.com/actions/checkout](https://github.com/actions/checkout)
* actions/setup-node: [https://github.com/actions/setup-node](https://github.com/actions/setup-node)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/6f55f1ac-064a-4aec-a91a-450caaf82d63/lesson/9ec91e18-757e-464f-88b6-91c52c580116)
