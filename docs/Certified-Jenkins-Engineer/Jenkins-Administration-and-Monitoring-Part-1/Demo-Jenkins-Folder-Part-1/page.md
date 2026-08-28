# Demo Jenkins Folder Part 1

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Administration-and-Monitoring-Part-1/Demo-Jenkins-Folder-Part-1/page

This tutorial teaches how to use folders in Jenkins to isolate jobs, credentials, and configurations for better organization.

In this tutorial, you’ll learn how to isolate jobs, credentials, and configurations in Jenkins using folders. Folders create independent namespaces so that:

* Identically named jobs (e.g., `build`) don’t collide
* Credentials and properties are scoped per folder
* Pipelines access only the libraries, credentials, and cloud profiles in their folder tree

This guide is **Part 1 of 4** in our Jenkins Folders series.

**Table of Contents**

1. Create a Shared Infrastructure Folder
2. Add Folder-Scoped Credentials
3. Nest a Team A Folder
4. Build and Run a Pipeline in Team A

***

## 1. Create a Shared Infrastructure Folder

Add a new folder called **Shared Infrastructure**:

<Frame>
  ![The image shows a Jenkins interface where a user is creating a new item named "shared-infrastructure" and selecting an item type from options like Freestyle project, Pipeline, Multi-configuration project, and Folder.](https://kodekloud.com/kk-media/image/upload/v1752870608/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-create-shared-infrastructure-item.jpg)
</Frame>

Configure **Display Name**, **Description**, health metrics, and custom properties:

<Frame>
  ![The image shows a Jenkins configuration page with options for setting a display name, description, health metrics, and properties. The interface is dark-themed and includes buttons for saving and applying changes.](https://kodekloud.com/kk-media/image/upload/v1752870609/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-configuration-dark-theme.jpg)
</Frame>

Scroll to advanced settings to add Docker labels, registry URLs, pipeline libraries, or Kubernetes cloud support:

<Frame>
  ![The image shows a configuration page for a shared infrastructure, featuring fields for Docker label, Docker registry URL, registry credentials, and options for adding pipeline libraries and Kubernetes support. There are buttons for saving and applying changes.](https://kodekloud.com/kk-media/image/upload/v1752870610/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/shared-infrastructure-configuration-docker.jpg)
</Frame>

After saving, the **Shared Infrastructure** folder appears on your dashboard:

<Frame>
  ![The image shows a Jenkins dashboard for a folder named "shared-infrastructure," which is currently empty. There are options on the left for configuring and managing items within Jenkins.](https://kodekloud.com/kk-media/image/upload/v1752870612/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-dashboard-shared-infrastructure-empty.jpg)
</Frame>

<Callout icon="lightbulb">
  Use clear, consistent folder names (e.g., `shared-infrastructure`) to help teams find shared resources quickly.
</Callout>

***

## 2. Add Folder-Scoped Credentials

Inside **Shared Infrastructure**, go to **Credentials** and click **Add Credentials**:

<Frame>
  ![The image shows a Jenkins interface displaying a list of credentials, including IDs and names for various services like MongoDB, DockerHub, and AWS.](https://kodekloud.com/kk-media/image/upload/v1752870613/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-credentials-list-mongodb-dockerhub-aws.jpg)
</Frame>

Select **Username with password** and enter:

* **Username**: Shared Database Username
* **Password**: (demo value)
* **ID**: shared-db-creds
* **Description**: Shared DB Credential

<Frame>
  ![The image shows a Jenkins interface where new credentials are being added, including fields for username, password, ID, and description.](https://kodekloud.com/kk-media/image/upload/v1752870615/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-add-credentials-interface.jpg)
</Frame>

After saving, verify the credential under the Shared Infrastructure domain:

<Frame>
  ![The image shows a Jenkins interface displaying global credentials, specifically a shared database credential with a username and password.](https://kodekloud.com/kk-media/image/upload/v1752870616/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-global-credentials-database.jpg)
</Frame>

<Callout icon="triangle-alert">
  Never print full secret values in logs. Always reference credentials via `credentials()` to keep them masked.
</Callout>

### Credential Summary

| Credential ID   | Scope                 | Description          |
| --------------- | --------------------- | -------------------- |
| shared-db-creds | Shared Infrastructure | Shared DB Credential |

***

## 3. Nest a Team A Folder

Under **Shared Infrastructure**, create a subfolder named **Team A**. It inherits parent settings but allows its own additions:

<Frame>
  ![The image shows a web interface displaying a list of credentials and their associated domains, likely from a shared infrastructure management system. It includes sections for "Stores scoped to shared-infrastructure » team-a" and "Stores from parent."](https://kodekloud.com/kk-media/image/upload/v1752870617/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/web-interface-credentials-list.jpg)
</Frame>

Inside **Team A**, add credentials:

* **Username**: Team A Username
* **Password**: (demo)
* **ID**: team-a-creds
* **Description**: Team A Bricks

<Frame>
  ![The image shows a Jenkins interface displaying global credentials, specifically a username with a password for "team-a-creds."](https://kodekloud.com/kk-media/image/upload/v1752870618/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-global-credentials-team-a-creds.jpg)
</Frame>

| Credential ID | Scope                          | Description   |
| ------------- | ------------------------------ | ------------- |
| team-a-creds  | Shared Infrastructure > Team A | Team A Bricks |

***

## 4. Build and Run a Pipeline in Team A

Still within **Team A**, create a **Pipeline** named **Team A Pipeline**. Use this Jenkinsfile to demonstrate folder-scoped credential access:

```groovy theme={null}
pipeline {
    agent any
    environment {
        SHARED_DB_CREDS = credentials('shared-db-creds')
        TEAM_A_CREDS    = credentials('team-a-creds')
    }
    stages {
        stage('Accessing Credentials') {
            steps {
                script {
                    echo "Shared DB Username: ${SHARED_DB_CREDS_USR}"
                    echo "Team A Username: ${TEAM_A_CREDS_USR}"
                }
            }
        }
    }
}
```

Save and run the pipeline. In [Blue Ocean](https://www.jenkins.io/projects/blueocean/) or the classic UI, you’ll see both usernames echoed:

<Frame>
  ![The image shows a Jenkins pipeline interface displaying a successful build process, with credentials being accessed and verified.](https://kodekloud.com/kk-media/image/upload/v1752870619/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-pipeline-successful-build.jpg)
</Frame>

After the build, verify the pipeline status on the dashboard:

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of a pipeline named "team-A-pipeline," with stages marked as completed. The interface includes options for configuring, building, and managing the pipeline.](https://kodekloud.com/kk-media/image/upload/v1752870620/notes-assets/images/Certified-Jenkins-Engineer-Demo-Jenkins-Folder-Part-1/jenkins-dashboard-team-a-pipeline.jpg)
</Frame>

***

## Next Steps

In **Part 2**, we’ll explore folder-level pipeline libraries and cloud agents for advanced CI/CD workflows.

***

## References

* [Jenkins Folders Plugin](https://plugins.jenkins.io/cloudbees-folder/)
* [Using Credentials in Jenkins](https://www.jenkins.io/doc/book/using/using-credentials/)
* [Blue Ocean Documentation](https://www.jenkins.io/projects/blueocean/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/bf3ddc28-a03d-4738-9f98-2779d81482f5/lesson/80fa03c2-7f20-4a22-afa0-85c921fae53c" />
</CardGroup>
