# .github/workflows/ci.yml
name: My Awesome App
on:
  push:
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'
```

<Callout icon="lightbulb">
  Workflow files must reside under `.github/workflows/` with a `.yml` or `.yaml` extension.
</Callout>

### Jobs and Steps

A workflow runs one or more **jobs**, each made up of sequential **steps**. Jobs run on **runners**—either GitHub-hosted VMs or your own self-hosted machines.

```yaml theme={null}
jobs:
  unit-testing:
    name: Unit Testing
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [14, 16]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
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

In this example:

1. The workflow triggers on `push` and `pull_request`.
2. A **matrix strategy** runs tests across multiple OS and Node.js versions.
3. Each runner checks out code, installs Node.js, installs dependencies, and executes `npm test`.

## Hosted Runners

GitHub-managed runners are provisioned on-demand (Linux, Windows on Azure, and macOS on GitHub’s cloud). Each job gets a clean VM:

<Frame>
  ![The image illustrates a GitHub Actions workflow, showing a job running on different hosted runners (Windows, Ubuntu, macOS) with steps like cloning a repository, installing NodeJS, and running tests.](https://kodekloud.com/kk-media/image/upload/v1752870456/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-actions-workflow-runners.jpg)
</Frame>

After a run completes, you can inspect logs, review step details, and download build artifacts from the **Actions** tab.

## Runner Types: GitHub-Hosted vs. Self-Hosted

Self-hosted runners let you use your own hardware, install custom software, or target GPUs. Compare the two options:

| Runner Type   | Hosting                    | Customization                 | Cost Model                                   | Managed By |
| ------------- | -------------------------- | ----------------------------- | -------------------------------------------- | ---------- |
| GitHub-hosted | GitHub cloud (Azure/macOS) | Limited to preinstalled tools | Included in GitHub plan (usage limits apply) | GitHub     |
| Self-hosted   | Your servers or cloud      | Full control                  | You bear infrastructure & maintenance        | You        |

<Frame>
  ![The image compares GitHub-hosted and self-hosted runners, highlighting their features and differences in terms of hosting, customization, and control.](https://kodekloud.com/kk-media/image/upload/v1752870456/notes-assets/images/Certified-Jenkins-Engineer-Github-Actions-Basics/github-self-hosted-runners-comparison.jpg)
</Frame>

<Callout icon="triangle-alert">
  GitHub-hosted runners have usage quotas based on your plan. Monitor minutes and storage under [Billing settings](https://github.com/settings/billing).
</Callout>

***

This article covered the essentials of GitHub Actions: defining workflows, splitting tasks into jobs and steps, leveraging matrix builds, and choosing the right runner. For more details, see the [GitHub Actions documentation](https://docs.github.com/actions).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/9ec91e18-757e-464f-88b6-91c52c580116" />
</CardGroup>


# Jenkins Configuration as Code JCasC

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Jenkins-Configuration-as-Code-JCasC/page

Jenkins Configuration as Code enables declarative, version-controlled management of Jenkins configurations, enhancing automation and reducing manual errors in CI/CD processes.

Managing Jenkins at scale demands the same declarative, version-controlled approach you use for your infrastructure. Jenkins Configuration as Code (JCasC) brings the principles of Infrastructure as Code (IaC) directly into your CI/CD server’s configuration.

## Why Configuration as Code?

As organizations grow, manual server and application setup slows down delivery, introduces errors, and lacks repeatability. Infrastructure as Code tools like Ansible, Terraform, Chef, and Puppet enable you to define infrastructure declaratively:

<Frame>
  ![The image illustrates "Infrastructure as Code" with tools like Ansible, Terraform, Chef, and Puppet, and highlights components such as templates, scripts, policies, network, application, storage, security, and cloud infrastructure.](https://kodekloud.com/kk-media/image/upload/v1752870458/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/infrastructure-as-code-tools-diagram.jpg)
</Frame>

Key benefits of IaC:

* Repeatable deployments
* Version control of infrastructure definitions
* Faster onboarding and consistency across environments

Extending these benefits to Jenkins means you can store your CI/CD configuration in Git, automate changes, and roll back when needed.

***

## Extending IaC to Jenkins

Jenkins Configuration as Code lets you define in code:

* **Jenkins infrastructure**: agents, nodes, clouds
* **Job and pipeline definitions**: steps, triggers, settings
* **Global system settings**: security, credentials, plugins

You can automate Jenkins through multiple interfaces:

<Frame>
  ![The image is a diagram titled "Managing Jenkins as Code," highlighting five components: Command-Line Tools, RESTful API, Client Libraries, Infrastructure as Code (IaC) Tools, and Containerization. It categorizes these under "Jenkins Infrastructure" with additional sections for "Jenkins Job Configurations" and "Jenkins System Configurations."](https://kodekloud.com/kk-media/image/upload/v1752870459/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/managing-jenkins-as-code-diagram.jpg)
</Frame>

| Approach                             | Description                                 |
| ------------------------------------ | ------------------------------------------- |
| Jenkins CLI                          | `jenkins-cli.jar` commands                  |
| REST API                             | HTTP endpoints for configuration and jobs   |
| Client libraries (Java, Python, Go)  | SDKs to script Jenkins                      |
| IaC tools (Ansible, Chef, Terraform) | Modules and playbooks for Jenkins resources |
| Containerization (Docker images)     | Prebuilt Jenkins images with custom configs |

***

## Managing Jenkins Jobs at Scale

When you have dozens or hundreds of jobs, the Jenkins web UI becomes unwieldy. Code-centric approaches include:

* **Job DSL Plugin**: Define jobs using a Groovy-based domain-specific language
* **Job Builder Plugin**: Write job configurations in YAML or JSON
* **Pipelines (Declarative/Scripted)**: Create `Jenkinsfile` workflows in SCM
* **Multibranch Pipeline**: Automatically generate pipelines per Git branch

<Frame>
  ![The image is a diagram titled "Managing Jenkins as Code," showing three main categories: Jenkins Infrastructure, Jenkins Job Configurations, and Jenkins System Configurations, with specific tools like JobDSL plugin, Job builder plugin, Jenkins Pipeline, and Multibranch listed under Job Configurations.](https://kodekloud.com/kk-media/image/upload/v1752870460/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/managing-jenkins-as-code-diagram-2.jpg)
</Frame>

<Callout icon="lightbulb">
  By defining jobs in code, you get full audit trails, PR-driven changes, and reproducible pipelines.
</Callout>

***

## Challenges of Manual System Configuration

Using **Manage Jenkins** in the UI for credentials, nodes, tools, plugins, and security:

* Becomes time-consuming for complex setups
* Introduces human error with repeated clicks
* Makes consistency across multiple instances difficult

<Frame>
  ![The image is about managing Jenkins as code, highlighting Jenkins Infrastructure, Job Configurations, and System Configurations, with a detailed view of system configuration options.](https://kodekloud.com/kk-media/image/upload/v1752870462/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/jenkins-as-code-infrastructure-configurations.jpg)
</Frame>

<Frame>
  ![The image is a presentation slide about managing Jenkins as code, highlighting Jenkins infrastructure, job configurations, and system configurations, with a focus on issues like being time-consuming, error-prone, and inefficient.](https://kodekloud.com/kk-media/image/upload/v1752870462/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/managing-jenkins-as-code-slide.jpg)
</Frame>

Before JCasC, many teams wrote Apache Groovy init scripts to automate setup. Although powerful, these scripts:

* Require deep knowledge of Jenkins internals
* Depend on undocumented APIs
* Are difficult to maintain as Jenkins evolves

<Frame>
  ![The image is about managing Jenkins as code, highlighting Jenkins infrastructure, job configurations, and system configurations, with a focus on Groovy scripting and Jenkins internals.](https://kodekloud.com/kk-media/image/upload/v1752870463/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/jenkins-as-code-infrastructure-job-configs.jpg)
</Frame>

<Callout icon="triangle-alert">
  Groovy init scripts can break after Jenkins upgrades. Prefer JCasC for long-term maintainability.
</Callout>

***

## Introducing Jenkins Configuration as Code

The [Jenkins Configuration as Code Plugin](https://plugins.jenkins.io/configuration-as-code/) lets you declare your entire Jenkins controller in YAML. It mirrors the UI settings so you can:

* Store configurations in Git for version control
* Apply changes automatically on startup or via the UI
* Eliminate manual form-filling and clicks
* Reduce human errors and simplify rollbacks

After installing the plugin, navigate to **Manage Jenkins → Configuration as Code → View Configuration** to export a snapshot of your setup:

```yaml theme={null}
jenkins:
  agentProtocols:
    - "JNLP4-connect"
    - "Ping"
  crumbIssuer:
    standard:
      excludeClientIPFromCrumb: false
      disableRememberMe: false
      disabledAdministrativeMonitors:
        - "hudson.util.DoubleLaunchChecker"
  globalNodeProperties:
    - envVars:
        key: "test1"
        value: "22222222222222222222222222222222"
  labelAtoms:
    - name: "built-in"
  markupFormatter:
    rawHtml:
      disableSyntaxHighlighting: false
  mode: NORMAL
  myViewsTabBar: "standard"
  nodeMonitors:
    - "architecture"
    - "Clock"
  diskspace:
    freeSpaceThreshold: "1GB"
    freeSpaceWarningThreshold: "261B"
  tmpSpace:
    freeSpaceThreshold: "1GB"
    freeSpaceWarningThreshold: "261B"
  responseTime:
  numExecutors: 2
  primaryView:
    all:
      name: "all"
      projectNamingStrategy: "standard"
      quietPeriod: 5
      remotingSecurity:
        enabled: true
        scmCheckoutRetryCount: 3
        securityRealm:
          local:
            allowsSignup: false
            enableCaptcha: false
```

<Callout icon="lightbulb">
  Always commit your exported YAML to your SCM. Even without immediate customization, it provides a historical configuration record.
</Callout>

***

## Structure of a JCasC YAML File

A standard JCasC YAML includes these top-level sections:

| Section      | Purpose                                            |
| ------------ | -------------------------------------------------- |
| jenkins      | Core system settings (security, views, executors)  |
| tools        | Tool installations (JDKs, Maven, Git, etc.)        |
| unclassified | Plugin-specific or miscellaneous configurations    |
| credentials  | Credentials for pipelines, jobs, and system access |

Additional sections may appear depending on installed plugins, nodes, clouds, and other extensions.

<Frame>
  ![The image illustrates Jenkins Configuration as Code (JCasC) with a YAML file structure and a cartoon character holding a wrench. It includes sections for system settings, nodes, and cloud configurations.](https://kodekloud.com/kk-media/image/upload/v1752870464/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Configuration-as-Code-JCasC/jenkins-configuration-code-yaml-diagram.jpg)
</Frame>

***

## Customizing Your JCasC File

Edit your YAML to tailor Jenkins. For example:

```yaml theme={null}
jenkins:
  systemMessage: "Welcome to the DevOps revolution!"

tools:
  maven:
    installations:
      - name: "maven-3.8.0"
        mavenHome: "/usr/share/maven"

views:
  list:
    - name: "My Jobs"
      filter: "name=.*"
    - name: "My Active Jobs"
      filter: "status != COMPLETED"
```

After saving changes, apply them via **Manage Jenkins → Configuration as Code**. No restart is required.

With JCasC, Jenkins becomes a fully automated, version-controlled service that scales with your team’s growth.

***

## Links and References

* [Jenkins Configuration as Code Plugin](https://plugins.jenkins.io/configuration-as-code/)
* [Official Jenkins Documentation](https://www.jenkins.io/doc/)
* [Infrastructure as Code Overview](https://www.hashicorp.com/resources/what-is-infrastructure-as-code)
* [Job DSL Plugin](https://plugins.jenkins.io/job-dsl/)
* [Pipeline as Code](https://www.jenkins.io/doc/book/pipeline/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/09048dab-99bb-4c08-8e0a-525499fb3b6c" />
</CardGroup>
