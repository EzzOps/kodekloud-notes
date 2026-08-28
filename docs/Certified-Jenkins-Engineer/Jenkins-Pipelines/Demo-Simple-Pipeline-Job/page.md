# View Jenkins home directory
cd /var/lib/jenkins
ls -l
```

```bash theme={null}
# List job workspaces
cd workspace/
ls -l
```

```bash theme={null}
# Inspect hello-world-pipeline workspace
cd hello-world-pipeline
ls -l
```

That’s it! You’ve learned how to manage your Jenkins pipeline script in SCM, run builds, and explore both the SCM repo and Jenkins workspace.

***

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [Pipeline as Code](https://www.jenkins.io/doc/book/pipeline/)
* [Git SCM](https://git-scm.com/)
* [Jenkinsfile Reference](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/054c2c42-f54a-42a4-ab39-4b432a36aaa1/lesson/5ae5093c-2fee-4ad3-b54e-151b5f6ee520" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/054c2c42-f54a-42a4-ab39-4b432a36aaa1/lesson/5393d884-7ae7-403e-9649-3af9dc096ff2" />
</CardGroup>


# Demo Simple Pipeline Job

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Jenkins-Pipelines/Demo-Simple-Pipeline-Job/page

This guide explains setting up a basic Jenkins Pipeline to print Hello World and run Maven commands.

In this guide, you’ll learn how to set up a basic Jenkins Pipeline that prints “Hello World” and then extends to run Maven commands. We’ll cover:

* Creating a Pipeline project
* Configuring the pipeline script
* Running a Hello World job
* Viewing build output and timing
* Adding automatic Maven installation

Whether you’re new to Jenkins or looking for a refresher, this step-by-step tutorial will get you up and running quickly.

## 1. Create a Pipeline Project

1. In the Jenkins UI, click **New Item**.
2. Enter **hello-world-pipeline** as the name.
3. Select **Pipeline** and click **OK**.

You now have a fresh Pipeline project ready to configure.

<Frame>
  ![The image shows a Jenkins interface where a new item named "hello-world-pipeline" is being created, with the "Pipeline" option selected.](https://kodekloud.com/kk-media/image/upload/v1752870787/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-hello-world-pipeline-creation.jpg)
</Frame>

## 2. Configure the Pipeline

Open your new project’s configuration to see sections like **General**, **Build Triggers**, and **Pipeline**. You can:

| Option                       | Description                                                   |
| ---------------------------- | ------------------------------------------------------------- |
| **Description**              | Add context about the job’s purpose.                          |
| **Build Triggers**           | Schedule with cron or poll SCM.                               |
| **Pipeline script**          | Paste your Declarative Pipeline directly in Jenkins.          |
| **Pipeline script from SCM** | Store your `Jenkinsfile` in a repository for version control. |

1. Under **Pipeline**, choose **Pipeline script**.
2. (Optional) Enable **Use Groovy Sandbox** to restrict script permissions.

<Frame>
  ![The image shows a configuration screen for a "hello-world-pipeline" in a web interface, where a pipeline script can be defined and edited. There are options to use a Groovy Sandbox and buttons to save or apply changes.](https://kodekloud.com/kk-media/image/upload/v1752870788/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/hello-world-pipeline-configuration.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins configuration screen for a pipeline project, with options for defining the pipeline script from SCM, selecting SCM type, and specifying the script path.](https://kodekloud.com/kk-media/image/upload/v1752870789/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-pipeline-configuration-screen.jpg)
</Frame>

## 3. Hello World Pipeline

Paste this Declarative Pipeline into the script box:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
    }
}
```

* **agent any** runs on any available node.
* **stage('Hello')** contains an `echo 'Hello World'` step.

<Callout icon="lightbulb">
  Enabling the Groovy Sandbox is recommended if you’re running untrusted scripts. It prevents unauthorized method calls.
</Callout>

Click **Apply**, **Save**, then **Build Now**.

## 4. View the Results

After triggering the job, the dashboard shows build status, history, and links to console output.

<Frame>
  ![The image shows a Jenkins dashboard for a pipeline named "hello-world-pipeline," displaying its status, build history, and permalinks for recent builds.](https://kodekloud.com/kk-media/image/upload/v1752870790/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-dashboard-hello-world-pipeline.jpg)
</Frame>

Click the build number or stage name to open the console log:

<Frame>
  ![The image shows a Jenkins pipeline console with a successful build labeled "Build #1," displaying details of the "Hello" stage and a "Hello World" print message.](https://kodekloud.com/kk-media/image/upload/v1752870791/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-pipeline-success-build1-hello.jpg)
</Frame>

**Raw console output:**

```text theme={null}
Started by user admin
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/hello-world-pipeline
[Pipeline] {
[Pipeline]   stage (Hello)
[Pipeline]   { (Hello)
[Pipeline]     echo
Hello World
[Pipeline]   } // stage
[Pipeline] } // node
[Pipeline] End of Pipeline
Finished: SUCCESS
```

Switch to **Pipeline Steps** or **Timing** to see per-step durations:

<Frame>
  ![The image shows a Jenkins dashboard displaying the status of a build process, including details like build duration and timing. The interface includes options for viewing console output, editing build information, and pipeline overview.](https://kodekloud.com/kk-media/image/upload/v1752870792/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-dashboard-build-status-overview.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins interface displaying the steps of a pipeline execution, including stages and their execution times. The pipeline steps are listed with their respective arguments and status indicators.](https://kodekloud.com/kk-media/image/upload/v1752870793/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-pipeline-execution-steps.jpg)
</Frame>

## 5. Extending with Maven

Let’s enhance the pipeline to print the Maven version. Add a `tools` block:

```groovy theme={null}
pipeline {
    agent any
    tools {
        // Install the Maven version configured as "M3"
        maven "M3"
    }
    stages {
        stage('Echo Version') {
            steps {
                sh 'echo Print Maven Version'
                sh 'mvn -version'
            }
        }
    }
}
```

<Callout icon="triangle-alert">
  If you run this now, you’ll get a compilation error because the tool name **M3** isn’t defined in Jenkins yet.
</Callout>

```text theme={null}
WorkflowScript: 6: Tool type "maven" does not have an install of "M3" configured - did you mean "null"? @ line 6, column 15.
    maven "M3"
             ^
1 error
Finished: FAILURE
```

## 6. Configure Maven in Jenkins

1. Navigate to **Manage Jenkins** > **Global Tool Configuration**.
2. Under **Maven installations**, click **Add Maven**.
3. Name it **M398**, enable **Install automatically**, and choose version **3.9.8**.
4. Save your changes.

<Frame>
  ![The image shows the "Manage Jenkins" dashboard interface, displaying various configuration and security options for managing Jenkins settings. It includes sections for system configuration, tools, plugins, and security settings.](https://kodekloud.com/kk-media/image/upload/v1752870795/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/manage-jenkins-dashboard-interface.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins configuration page for managing Maven installations, with options to install specific versions automatically.](https://kodekloud.com/kk-media/image/upload/v1752870796/notes-assets/images/Certified-Jenkins-Engineer-Demo-Simple-Pipeline-Job/jenkins-maven-installation-config.jpg)
</Frame>

Now update your Pipeline to use **M398**:

```groovy theme={null}
pipeline {
    agent any
    tools {
        maven "M398"
    }
    stages {
        stage('Echo Version') {
            steps {
                sh 'echo Print Maven Version'
                sh 'mvn -version'
            }
        }
    }
}
```

## 7. Build and Verify

Click **Build Now** again. You’ll see **Tool Installation** followed by **Echo Version**.

**Console snippet:**

```text theme={null}
+ echo Print Maven Version
Print Maven Version
+ mvn -version
Apache Maven 3.9.8 (36645f6c9b57998e5a5009217e36f2cff343256)
Maven home: /var/lib/jenkins/tools/hudson.tasks.Maven_MavenInstallation/M398
Java version: 17.0.12, vendor: Ubuntu, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "6.8.0-39-generic", arch: "amd64", family: "unix"
Finished: SUCCESS
```

## Conclusion

You’ve now:

* Created a Jenkins Pipeline project
* Written and executed a “Hello World” pipeline
* Viewed build logs and timing
* Configured Jenkins to install Maven automatically

Next steps: integrate SCM checkout, add test and deploy stages, and configure post-build notifications.

## Links and References

* [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
* [Jenkins Global Tool Configuration](https://www.jenkins.io/doc/book/managing/tools/)
* [Maven Plugin for Jenkins](https://plugins.jenkins.io/maven-plugin/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/054c2c42-f54a-42a4-ab39-4b432a36aaa1/lesson/7ab1975f-b612-4671-8e0d-70021f6c929e" />
</CardGroup>
