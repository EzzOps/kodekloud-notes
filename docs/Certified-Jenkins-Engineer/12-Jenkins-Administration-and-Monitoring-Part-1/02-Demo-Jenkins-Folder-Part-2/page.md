# Demo Jenkins Folder Part 2

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Jenkins-Folder-Part-2/page

This guide extends Jenkins folder hierarchy by creating a new folder and pipeline to illustrate folder-scoped credential inheritance.

In this guide, we’ll extend our Jenkins folder hierarchy by creating a new `team-b` folder under `shared-infrastructure` and then add a pipeline to illustrate how folder-scoped credentials are inherited (or not).

## 1. Create the `team-b` Folder and Pipeline

1. In Jenkins UI, navigate to **shared-infrastructure**.
2. Click **New Item**, enter `team-b`, select **Folder**, and hit **OK**.
3. Inside **team-b**, click **New Item** again, name it `team-b-pipeline`, choose **Pipeline**, then **OK**.
4. Under **Pipeline** → **Definition**, point to the same Jenkinsfile:

```groovy theme={null}
pipeline {
    agent any
    environment {
        SHARED_DB_CREDS = credentials('shared-db-creds')
        TEAM_A_CREDS   = credentials('team-a-creds')
    }
    stages {
        stage('Accessing Credentials') {
            steps {
                script {
                    echo "Username from Shared-Folder Credentials: ${SHARED_DB_CREDS_USR}"
                    echo "Username from Team-A folder Credentials: ${TEAM_A_CREDS_USR}"
                }
            }
        }
    }
    post {
        success { echo "Build completed successfully" }
        failure { echo "Build failed" }
    }
}
```

> **lightbulb** Jenkins uses [folder-based permission checks](https://plugins.jenkins.io/cloudbees-folder/) to isolate credentials. Anything defined in a parent folder is inherited by its subfolders.

## 2. Trigger the Pipeline

Click **Build Now** on `team-b-pipeline`. The job will start but ultimately fail:

### 2.1 Console Output

```console theme={null}
Started by user siddharth
[Pipelines] Start of Pipeline
[Pipelines] node
Running on Jenkins in /var/lib/jenkins/workspace/shared-infrastructure/team-b/team-b-pipeline
[Pipelines] {
[Pipelines]   stage
[Pipelines]     (Accessing Credentials)
[Pipelines]   { ... }
[Pipelines]   // stage
[Pipelines]   End of Pipeline
ERROR: team-a-creds
Finished: FAILURE
```

> **triangle-alert** `team-b-pipeline` cannot retrieve `team-a-creds`. Credentials scoped to **team-a** are invisible to **team-b**, which is a sibling folder.

## 3. Understanding Folder-Scoped Credential Inheritance

| Credential Location   | Visible To                              |
| --------------------- | --------------------------------------- |
| shared-infrastructure | `team-a`, `team-b` (and any subfolders) |
| team-a                | Items in **team-a** only                |
| team-b                | Items in **team-b** only                |

1. **Shared folder credentials** (`shared-db-creds`) are inherited by all child folders.
2. **Folder-specific credentials** (`team-a-creds`) only apply within their own folder.

This clear separation ensures that sensitive data remains scoped to the appropriate teams.

***

## Links and References

* [Jenkins Folder Plugin](https://plugins.jenkins.io/cloudbees-folder/)
* [Jenkins Credentials Plugin](https://plugins.jenkins.io/credentials/)
* [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

Thank you for following this demonstration on Jenkins folder-scoped credential inheritance!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/c96f42df-bc44-4a57-a5ca-0a00976ebb4c)
