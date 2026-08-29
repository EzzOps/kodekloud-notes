# Initialize and push a new repository
touch README.md
git init
git checkout -b main
git add README.md
git commit -m "first commit"
git remote add origin http://64.227.187.25:5555/dasher-org/shared-libraries.git
git push -u origin main
```

Always consult the official Jenkins documentation for Shared Libraries for configuration details and the expected directory layout:

* Jenkins Shared Libraries documentation: [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)

<Frame>
  <img alt="A screenshot of the Jenkins documentation page showing the &#x22;Extending with Shared Libraries&#x22; section from the Pipeline User Handbook, with a left navigation menu and a Table of Contents on the right. The page uses a dark theme and displays explanatory text about shared libraries for Jenkins Pipelines." />
</Frame>

Shared libraries use a specific layout. A minimal structure looks like this:

```text theme={null}
(root)
+- src                      # Groovy source files (compiled classes)
|   +- org
|   |   +- foo
|   |   |   +- Bar.groovy   # for org.foo.Bar class
+- vars
|   +- foo.groovy           # for global 'foo' variable/step
|   +- foo.txt              # help for 'foo' variable
+- resources                # resource files (for classes to load)
|   +- org
|   |   +- foo
|   |   |   +- bar.json     # static helper data for org.foo.Bar
```

Directory purpose at a glance:

| Directory   | Purpose                                        | Example                              |
| ----------- | ---------------------------------------------- | ------------------------------------ |
| `src`       | Compiled Groovy classes, organized by package  | `src/org/foo/Bar.groovy`             |
| `vars`      | Global step scripts (each file exposes a step) | `vars/foo.groovy` and `vars/foo.txt` |
| `resources` | Static files that your classes may load        | `resources/org/foo/bar.json`         |

To create a step-style global function (so you can call it like a built-in step such as `sh` or `git`), add a Groovy file under `vars/` and define a `call` method.

Create the file `vars/slackNotification.groovy` in your `shared-libraries` repository.

<Frame>
  <img alt="A dark-themed repository webpage (dasher-org / shared-libraries) showing a code view with a filename input containing &#x22;slackNotification&#x22; and a &#x22;New File&#x22; button. Browser tabs and the address bar are visible at the top." />
</Frame>

Example implementation for `vars/slackNotification.groovy`. This exposes a `slackNotification(...)` step that your pipelines can call directly:

```groovy theme={null}
// vars/slackNotification.groovy
def call(String buildStatus = 'STARTED') {
    def color
    if (buildStatus == 'SUCCESS') {
        color = '#47ec05'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#d5ee0d'
    } else {
        color = '#ec2805'
    }

    def msg = "${buildStatus}: ${env.JOB_NAME} #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"

    slackSend(color: color, message: msg)
}
```

> **lightbulb** Define `call` in `vars/<name>.groovy` to allow invoking the library step directly as `<name>(...)` from a Pipeline (this mirrors built-in steps like `sh` or `git`).

After committing the repository and pushing the file, make the Shared Library available to Jenkins.

Option 1 — Configure as a Global Pipeline Library

* In Jenkins: Manage Jenkins → Configure System → Global Pipeline Libraries
* Add your `shared-libraries` repository with a name (for example, `shared-libraries`) so it can be referenced by name from any pipeline.

Option 2 — Use `@Library` annotation per-repository

* Add `@Library('<library-name>') _` at the top of a Jenkinsfile to import the library for that pipeline.

Example usage in a Jenkinsfile (after the shared library is configured):

```groovy theme={null}
@Library('shared-libraries') _

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // build steps ...
            }
        }
    }

    post {
        success {
            script {
                // call the shared library step
                slackNotification('SUCCESS')
            }
        }
        unstable {
            script {
                slackNotification('UNSTABLE')
            }
        }
        failure {
            script {
                slackNotification('FAILURE')
            }
        }
    }
}
```

Next steps and references

* Review the Jenkins documentation on Shared Libraries to learn about loading strategies, caching, and versioning: [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* Consider adding a `vars/slackNotification.txt` file to document usage/help for the step.
* If your notification logic requires credentials or tokens (e.g., Slack webhook), use Jenkins Credentials and refer to them securely from your library code.

Further reading and references

* Jenkins Shared Libraries — [https://www.jenkins.io/doc/book/pipeline/shared-libraries/](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* Jenkins Pipeline Syntax — [https://www.jenkins.io/doc/book/pipeline/syntax/](https://www.jenkins.io/doc/book/pipeline/syntax/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/7e7be52f-69f5-496b-8a46-322d6b8df0ce/lesson/7cd4292e-6460-4a27-9271-c70d332a22f0)


# Demo Refactor existing Jenkinsfile

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Shared-Libraries-in-Jenkins/Demo-Refactor-existing-Jenkinsfile/page

Refactoring a Jenkinsfile to create reusable CI pipelines with Slack notifications, integrated Trivy scanning and in-stage report publishing while disabling long running deployment stages for demo use

This lesson refactors an existing `Jenkinsfile` so the same pipeline can be reused across upcoming demos. It builds on concepts from the Jenkins Pipelines course. If you haven't completed that course, review it first:

* [Jenkins Pipelines course](https://learn.kodekloud.com/user/courses/jenkins-pipelines)

> **lightbulb** This demo shows a practical Jenkinsfile refactor to:

  * Reduce and focus stages for CI-focused demos.
  * Keep Slack notifications and critical scans.
  * Move report generation into the stage that produces the artifacts (Trivy).

Prerequisites

* Familiarity with Declarative Jenkins Pipelines.
* Basic Git usage (branching, committing, pushing).
* Basic knowledge of Trivy for container vulnerability scanning.
* The repository used in this demo (details below).

Repository and branch being used

This repo lives under the `dasher` organization as `solar-system`. In the previous course we used the `feature/enabling-slack` branch. For the advanced demos we create a new branch from that branch so we can experiment without affecting the original.

<Frame>
  <img alt="A dark-themed Gitea organization page for &#x22;dasher-org&#x22; showing a list of repositories (like &#x22;solar-system&#x22;, &#x22;solar-system-gitops-argocd&#x22;, etc.) and a right-hand sidebar with Members and Teams. The top has navigation and buttons for &#x22;New Repository&#x22; and &#x22;New Migration.&#x22;" />
</Frame>

Open the repository in your editor or terminal. Example shell prompt:

```bash theme={null}
root@jenkins-controller-1 in ~ on ☁ (us-east-2)
◯>
```

Goals of the refactor

* Retain Slack notification logic to keep CI visibility.
* Keep Docker build and Trivy vulnerability scan stages.
* Keep `npm install`, unit tests, and code coverage stages.
* Comment out long-running or environment-specific stages we won't use (SonarQube, OWASP dependency-check, pushing to registries, EC2/K8s deployments).
* Move Trivy `convert` and report publishing (`publishHTML`, `junit`) into the Trivy stage so artifacts are grouped with their generating stage.

Slack notification helper

The Slack helper function is a small Groovy method used inside the `post` blocks. It remains unchanged and will be reused by the simplified top-level `post` block.

```groovy theme={null}
def slackNotificationMethod(String buildStatus = 'STARTED') {
    buildStatus = buildStatus ?: 'SUCCESS'

    def color
    if (buildStatus == 'SUCCESS') {
        color = '#47ec05'
    } else if (buildStatus == 'UNSTABLE') {
        color = '#d5ee0d'
    } else {
        color = '#ec2805'
    }

    def msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"
    slackSend(color: color, message: msg)
}
```

Top of the Jenkinsfile — agent, tools, environment

Example snippet from the top of the `Jenkinsfile` showing `agent`, `tools`, `environment`, and the simplified `post` block. This remains the structural basis for the pipeline:

```groovy theme={null}
pipeline {
    agent any

    tools {
        // tool installations, e.g. nodejs, maven etc.
        // ...
    }

    environment {
        MONGO_URI = "mongodb+srv://supercluster.d83jj.mongodb.net/superData"
        MONGO_DB_CREDS = credentials('mongo_db_credentials')
        GITEA_TOKEN = credentials('gitea-api-token')
    }

    options {
        // pipeline/options ...
    }

    stages {
        // stages defined below
    }

    post {
        always {
            slackNotificationMethod("${currentBuild.result}")

            // If we still want to clean up repo copies that the pipeline clones:
            script {
                if (fileExists('solar-system-gitops-argocd')) {
                    sh 'rm -rf solar-system-gitops-argocd'
                }
            }
        }
    }
}
```

Which stages we keep vs. comment out

To make the pipeline concise and focused for demos, we kept the core CI stages and commented out most environment-dependent or long-running stages.

| Kept (active)                                 | Commented out / Disabled                               |
| --------------------------------------------- | ------------------------------------------------------ |
| Installing Dependencies (`npm install`)       | `Push Docker Image`                                    |
| Dependency Scanning (`npm audit`)             | `Deploy - AWS EC2`                                     |
| Build Docker Image                            | `Integration Testing - AWS EC2`                        |
| Trivy Vulnerability Scanner (with local post) | `K8S - Update Image Tag`                               |
| Unit Tests + Code Coverage                    | `K8S - Raise PR`                                       |
|                                               | `App Deployed?`                                        |
|                                               | OWASP ZAP, SonarQube, S3 uploads, Lambda deploys, etc. |

For readability the disabled stages are preserved in the file as commented placeholders to show they exist but are not executed in this demo:

```groovy theme={null}
stage('Build Docker Image') {
    // kept
}

stage('Trivy Vulnerability Scanner') {
    // kept
}

stage('Push Docker Image') {
    // commented out for these demos
}

stage('Deploy - AWS EC2') {
    // commented out
}

stage('Integration Testing - AWS EC2') {
    // commented out
}

stage('K8S - Update Image Tag') {
    // commented out
}

stage('K8S - Raise PR') {
    // commented out
}

stage('App Deployed?') {
    // commented out
}
```

Trivy stage: run, convert, and publish reports locally within the stage

Rather than publishing Trivy’s HTML/XML reports from a global `post` block, move the conversion and publishing into the Trivy stage's own `post` so that report generation stays close to its source. The workflow in the Trivy stage typically:

1. Run Trivy scans for different severity sets.
2. Output JSON results.
3. Convert JSON to HTML and JUnit XML using `trivy convert`.
4. Publish JUnit and HTML reports using `junit` and `publishHTML`.

Example Trivy scan commands used in the Trivy stage (shell commands executed by the stage):

```bash theme={null}
