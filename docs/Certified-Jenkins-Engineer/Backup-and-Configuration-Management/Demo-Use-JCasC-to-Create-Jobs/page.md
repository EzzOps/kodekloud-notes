# Stop Jenkins
sudo systemctl stop jenkins
```

<Callout icon="triangle-alert">
  Always back up or rename your current WAR before replacing it.
</Callout>

```bash theme={null}
# Backup the existing WAR
sudo mv /usr/share/java/jenkins.war /usr/share/java/jenkins.war.bak

# Download the new WAR
sudo wget -O /usr/share/java/jenkins.war \
  https://updates.jenkins.io/download/war/2.492.1/jenkins.war

# Restart Jenkins
sudo systemctl start jenkins
```

***

## 5. Verify the Upgrade

After Jenkins restarts, log back in and confirm the new version under **Manage Jenkins** or in the dashboard footer. It should display **2.492.1**.

***

## Links and References

* [Jenkins Downloads](https://www.jenkins.io/download/)
* [Jenkins Changelog (LTS)](https://www.jenkins.io/changelog-stable/)
* [Jenkins “Prepare for Shutdown” Documentation](https://www.jenkins.io/doc/book/managing/#shutdown)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/b1d25fb2-4127-4e4b-b638-e3d94ed436cf" />
</CardGroup>


# Demo Use JCasC to Create Jobs

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Backup-and-Configuration-Management/Demo-Use-JCasC-to-Create-Jobs/page

Learn to use the Jenkins Configuration as Code plugin to define jobs, manage settings, and install tools using YAML.

In this lesson, you’ll learn how to leverage the Jenkins Configuration as Code (JCasC) plugin to define pipeline jobs, manage global settings, and install build tools—all through YAML. We’ll explore official demos, customize configurations, and apply them in your Jenkins instance.

## Prerequisites

* Jenkins with Configuration as Code plugin installed
* Access to Jenkins controller shell
* Basic familiarity with YAML and Jenkins plugins

## 1. Explore Example Configurations

The [JCasC plugin demos on GitHub](https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos) contain ready-made use cases:

<Callout icon="lightbulb">
  You can browse the **demos** directory for examples ranging from security setups to cloud integrations.
</Callout>

## 2. Configure Global Authorization

To set up a matrix-based authorization strategy, add the following to your `jenkins-casc.yaml`:

```yaml theme={null}
jenkins:
  authorizationStrategy:
    globalMatrix:
      permissions:
        - "USER:Overall/Read:anonymous"
        - "GROUP:Overall/Administer:authenticated"
        - "USER:Overall/Administer:admin"
```

## 3. Configure a Kubernetes Cloud

Click **Config YAML** under the Kubernetes demo to copy this snippet:

```yaml theme={null}
unclassified:
  location:
    url: http://jenkins/

jenkins:
  clouds:
    - kubernetes:
        name: "advanced-k8s-config"
        serverUrl: "https://advanced-k8s-config:443"
        serverCertificate: "serverCertificate"
        skipTlsVerify: true
        credentialsId: "advanced-k8s-credentials"
        namespace: "default"
        jenkinsUrl: "http://jenkins/"
        jenkinsTunnel: "JenkinsTunnel"
        containerCapStr: 42
        maxRequestsPerHostStr: 64
        retentionTimeout: 5
        connectTimeout: 10
```

<Frame>
  ![The image shows a GitHub repository page for a project related to configuring a Kubernetes plugin, with a list of files and a README section providing instructions.](https://kodekloud.com/kk-media/image/upload/v1752870436/notes-assets/images/Certified-Jenkins-Engineer-Demo-Use-JCasC-to-Create-Jobs/github-repo-kubernetes-plugin-config.jpg)
</Frame>

## 4. Install Build Tools

You can also install Node.js, Git, Maven, and SonarQube Scanner using JCasC. Here’s an example for Node.js:

```yaml theme={null}
tool:
  nodejs:
    installations:
      - name: "NodeJS Latest"
        home: ""  # required until nodejs-1.3.4 release (JENKINS-57508)
        properties:
          installSource:
            installers:
              - nodeJSInstaller:
                  id: "12.11.1"
                  npmPackagesRefreshHours: 48  # default is 72
```

### Tool Installation Summary

| Tool              | Version Identifier | Notes                                                 |
| ----------------- | ------------------ | ----------------------------------------------------- |
| Node.js           | 12.11.1            | Auto-installed; refreshes npm packages every 48 hours |
| Git               | Default            | Uses system `git` binary                              |
| Maven             | 3.9.8              | Managed via internal installer                        |
| SonarQube Scanner | 6.10               | Installed through the SonarRunner installer           |

## 5. Edit Your jenkins-casc.yaml

On the controller, open or create your configuration file:

```bash theme={null}
cd /var/lib/jenkins/JENKINS_BACKUP
vi jenkins-casc.yaml
```

A comprehensive file may include credentials, SCM settings, tool definitions, and more:

```yaml theme={null}
credentials:
  system:
    domainCredentials:
      - usernamePassword:
          description: 'Gitea Server Credentials'
          id: gitea-server-creds
          username: gitea-admin
          password: '{AQAAB...}'
          scope: GLOBAL
      - usernamePassword:
          description: 'Credentials for MongoDB'
          id: mongo-db-credentials
          username: superuser
          password: '{AQAAB...}'
          scope: GLOBAL
      - string:
          description: 'Mongo Database Username'
          id: moneo-db-username

git:
  installations:
    - home: "git"
      name: "Default"

maven:
  installations:
    - name: "M398"
      properties:
        - installSource:
            installers:
              - maven:
                  id: "3.9.8"

sonarRunnerInstallation:
  installations:
    - name: "sonarqube-scanner-610"
      properties:
        - installSource:
            installers:
              - sonarRunnerInstaller: {}
```

## 6. Define Pipeline Jobs with Job DSL

In the demos folder, there’s a sample that uses the [Job DSL plugin](https://plugins.jenkins.io/job-dsl) to create a folder and pipeline job:

<Frame>
  ![The image shows a GitHub repository page for a Jenkins configuration-as-code plugin, displaying a list of YAML files and a README section about configuring seed jobs.](https://kodekloud.com/kk-media/image/upload/v1752870437/notes-assets/images/Certified-Jenkins-Engineer-Demo-Use-JCasC-to-Create-Jobs/github-jenkins-config-yaml-files.jpg)
</Frame>

Add these job definitions to your `jenkins-casc.yaml`:

```yaml theme={null}
jobs:
  - script: >
      folder('test-jobs')
  - script: >
      pipelineJob('test-jobs/default-agent') {
        definition {
          cps {
            script("""
              pipeline {
                agent any
                stages {
                  stage('test') {
                    steps {
                      echo 'hello'
                    }
                  }
                }
              }
            """.stripIndent())
          }
        }
      }
```

## 7. Reload Configuration and Troubleshoot

After saving, go to **Manage Jenkins** → **Configuration as Code** → **Reload Existing Configuration**. You may see:

<Frame>
  ![The image shows a Jenkins configuration page with a warning about a missing configurator for root elements. There are options to apply a new configuration, reload, download, and view the configuration.](https://kodekloud.com/kk-media/image/upload/v1752870438/notes-assets/images/Certified-Jenkins-Engineer-Demo-Use-JCasC-to-Create-Jobs/jenkins-configuration-warning-page.jpg)
</Frame>

<Callout icon="triangle-alert">
  If you encounter `UnknownConfiguratorException: No configurator for the following root elements: jobs`, it means the **Job DSL** plugin is not installed.
</Callout>

To resolve:

1. **Manage Jenkins** → **Manage Plugins**
2. Search for **Job DSL** and install.
3. Reload or reapply your JCasC configuration.

## 8. Verify Jobs and Tools

Once the DSL plugin is active, Jenkins will create the `test-jobs` folder and the `default-agent` pipeline automatically. You can also confirm tool installations under **Manage Jenkins** → **Global Tool Configuration**:

```groovy theme={null}
pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        echo "Hello"
      }
    }
  }
}
```

<Frame>
  ![The image shows a Jenkins configuration interface with dropdown menus for managing system settings, plugins, and security options. The user is navigating through the "Manage Jenkins" menu.](https://kodekloud.com/kk-media/image/upload/v1752870439/notes-assets/images/Certified-Jenkins-Engineer-Demo-Use-JCasC-to-Create-Jobs/jenkins-configuration-manage-menu.jpg)
</Frame>

## References

* [Configuration as Code Plugin](https://github.com/jenkinsci/configuration-as-code-plugin)
* [Job DSL Plugin](https://plugins.jenkins.io/job-dsl)
* [Kubernetes Cloud](https://plugins.jenkins.io/kubernetes)
* [NodeJS Plugin](https://plugins.jenkins.io/nodejs)
* [Maven Integration Plugin](https://plugins.jenkins.io/maven-plugin)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/77043650-89c2-4ad3-bbd1-e06eabe35581/lesson/89c33efb-e680-4434-9c44-d900a625b5dc" />
</CardGroup>
