# Demo Audit Jenkins 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Audit-Jenkins-2/page

Demo showing how to audit Jenkins, add a multibranch pipeline, add a secret binding, and regenerate GitHub Actions workflow snippets with redacted secrets

In this lesson we update the Jenkins instance, add a Multi-branch Pipeline, create a secret binding in an existing job, and re-run the audit to see how the audit summary and generated artifacts change.

What you'll see in this demo:

* Creating a Multi-branch Pipeline that discovers Jenkinsfiles in multiple branches.
* Indexing output from Jenkins showing discovered branches.
* Adding a secret via the job's Environment → Bindings and using it in a shell step.
* Re-running the `gh actions-importer audit jenkins` command and inspecting the updated audit summary and generated GitHub Actions workflow snippets.

Relevant references:

* [Jenkins Pipeline (Multibranch)](https://www.jenkins.io/doc/book/pipeline/multibranch/)
* [GitHub Actions documentation](https://docs.github.com/actions)
* gh actions-importer: use the tool's CLI to audit and migrate Jenkins jobs to GitHub Actions.

***

## Initial state: existing Jenkins jobs and previous audit

There were four Jenkins jobs discovered by the previous audit. One job was in a pending state (likely an agent issue); it was cancelled so it wouldn't interfere with the demo.

For reference, here is the trimmed audit summary from the previous run:

```markdown theme={null}
Summary for [Jenkins instance](http://139.84.149.83:8080/)

- GitHub Actions Importer version: **1.3.22397 ([AWS_SECRET_ACCESS_KEY])**
- Performed at: **5/21/25 at 18:19**

## Pipelines
Total: **4**

- Successful: **1 (25%)**
- Partially successful: **2 (50%)**
- Unsupported: **1 (25%)**
- Failed: **0 (0%)**

### Job types

Supported: **3 (75%)**

- flow-definition: **2**
- project: **1**

Unsupported: **1 (25%)**

- scripted: **1**

### Build steps
...
```

***

## Create a Multi-branch Pipeline

We created a new GitHub repo `jenkins-demo-org/demo-repo` containing two branches: `main` and `uat`. Each branch contains a Jenkinsfile — `main` includes a single stage, while `uat` contains two stages. To add the multi-branch job in Jenkins, choose **New Item → Multi-branch Pipeline** and point the Branch Source to the GitHub repository.

<Frame>
  <img alt="A screenshot of the Jenkins &#x22;New Item&#x22; page showing an item name field with &#x22;multi-branch&#x22; typed in. Below it are selectable job types like Freestyle project, Pipeline, and Multi-configuration project." />
</Frame>

The demo repository in GitHub:

<Frame>
  <img alt="A dark-themed GitHub repository page for &#x22;demo-repo&#x22; (jenkins-demo-org) showing branch and commit details including a Jenkinsfile. The page also shows an &#x22;Add a README&#x22; prompt and a &#x22;Compare & pull request&#x22; button." />
</Frame>

Example Jenkinsfile (used in both branches, with `uat` containing Stage-2):

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Stage-1') {
            steps {
                echo "stage-1"
            }
        }

        stage('Stage-2') {
            steps {
                echo "stage-2"
            }
        }
    }
}
```

In the Multi-branch Pipeline configuration we pointed Branch Source to the GitHub repository and validated the connection. This repo is public, so no Jenkins credentials were required when validating the branch source.

<Frame>
  <img alt="A screenshot of the Jenkins multi-branch pipeline Configuration page showing the Branch Sources section for a GitHub repo, including a Credentials dropdown and the Repository HTTPS URL field populated with https://github.com/jenkins-demo-org/demo-repo. The left sidebar lists other configuration panels and Save/Apply buttons are visible at the bottom." />
</Frame>

We left other settings at defaults and saved the job. Jenkins scanned the repository and indexed both branches, reporting that each branch contained a Jenkinsfile and was scheduled for indexing:

<Frame>
  <img alt="A dark-themed Jenkins web UI screenshot showing the Configuration page for a multi-branch pipeline, with sections like Build Configuration, Property strategy, and Script Path. The left sidebar lists configuration categories and there are &#x22;Save&#x22; and &#x22;Apply&#x22; buttons at the bottom." />
</Frame>

Indexing console output:

```text theme={null}
Examining jenkins-demo-org/demo-repo
Checking branches...
Getting remote branches...
Checking branch main
    'Jenkinsfile' found
    Met criteria
Scheduled build for branch: main
Checking branch uat
    'Jenkinsfile' found
    Met criteria
Scheduled build for branch: uat
2 branches were processed
Finished examining jenkins-demo-org/demo-repo
[Thu May 22 09:22:59 UTC 2025] Finished branch indexing. Indexing took 2.2 sec
Finished: SUCCESS
```

After indexing, the `main` branch showed a successful build:

<Frame>
  <img alt="A dark-themed Jenkins dashboard showing the &#x22;multi-branch-pipeline / main&#x22; job page with permalinks to the last builds and a sidebar of actions (Status, Changes, Build Now, etc.). The Builds panel at left shows a successful build #1." />
</Frame>

***

## Add a secret binding to an existing job

Next, we switched to an existing job (Generate ASCII Artwork) and added a secret via Configure → Environment → Bindings. We added a **Secret text** binding named `m_username` and selected an existing stored credential (`mongo-db-password`) for the demo.

<Frame>
  <img alt="A dark‑themed Jenkins dashboard showing a list of CI pipelines with status icons, last success/failure times, and play buttons. The left sidebar displays navigation items and build queue/executor status." />
</Frame>

Bindings configured in the job:

<Frame>
  <img alt="A Jenkins job &#x22;Configure&#x22; screen showing the Environment > Bindings section with a Secret text variable named &#x22;m_username&#x22; and a credentials dropdown (options include mongo-db-username, mongo-db-password, owasp-dependency-check). The Save and Apply buttons are visible at the bottom." />
</Frame>

We used that variable inside a shell build step. The original demo script had syntax issues; below is an improved and safer version suitable for a shell build step:

```bash theme={null}
#!/bin/bash
