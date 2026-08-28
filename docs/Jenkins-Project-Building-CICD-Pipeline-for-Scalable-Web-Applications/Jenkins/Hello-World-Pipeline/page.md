# Hello World Pipeline

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Jenkins/Hello-World-Pipeline/page

This guide teaches how to set up a simple Jenkins pipeline with a Hello World example, covering essential steps for creating and running a pipeline.

In this guide, you'll learn how to set up your first Jenkins pipeline—a simple "Hello World" example that demonstrates the essential steps to create and run a pipeline. As you progress, more intricate pipelines will be covered, but we’ll start with the basics.

## Accessing Jenkins

Begin by opening your Jenkins instance. If you haven’t set it up before, navigate to your Jenkins IP address on port 8080. Follow the setup instructions to configure your username and other settings. Once completed, you should see a dashboard similar to the image below:

<Frame>
  ![The image shows the Jenkins dashboard, welcoming the user and providing options to create a job, set up a distributed build, and manage Jenkins settings.](https://kodekloud.com/kk-media/image/upload/v1752879891/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Hello-World-Pipeline/jenkins-dashboard-job-setup.jpg)
</Frame>

## Creating a New Pipeline

1. Click on **New Item**.
2. Provide a name for your pipeline; for this example, name it **Hello World Pipeline**.
3. Select the **Pipeline** option and then click **OK**.

## Pipeline Configuration

Scroll down to the pipeline configuration section. You will see an interface similar to the following:

<Frame>
  ![The image shows a Jenkins interface where a user can select different project types, such as Freestyle project, Pipeline, Multi-configuration project, Folder, Multibranch Pipeline, and Organization Folder.](https://kodekloud.com/kk-media/image/upload/v1752879893/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Hello-World-Pipeline/jenkins-project-types-interface.jpg)
</Frame>

Here, you have two options for defining your pipeline:

1. Create the pipeline script directly in Jenkins.
2. Load the pipeline script from source control (e.g., via a Jenkinsfile in your repository).

For this tutorial, we will use a pipeline script written directly in Jenkins.

<Callout icon="lightbulb">
  Jenkins provides sample pipelines to help you get started without writing the entire script from scratch. Feel free to use these examples as a learning tool.
</Callout>

## Sample Pipeline Script

Review the following pipeline script:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('hello') {
            steps {
                echo 'hello world'
            }
        }
    }
}
```

### Script Breakdown

* **pipeline block**: Encloses all instructions for the pipeline.
* **agent any**: Directs Jenkins to run the pipeline on any available agent. (An agent is a machine connected to the Jenkins controller for executing pipelines.)
* **stages block**: Groups the pipeline’s tasks into logical units (e.g., build, test, deploy).
* **hello stage**: Contains a `steps` block where the `echo 'hello world'` command prints "hello world" to the console output.

## Saving and Running the Pipeline

Once you have entered the pipeline script:

1. Click **Save**.
2. To execute your pipeline, click the **Build Now** button.

This triggers a build that will be numbered "1". To inspect the detailed execution:

* Click on the build number.
* Select **Console Output** to review the steps performed by Jenkins.

You should see output similar to the example below:

```bash theme={null}
Started by user sanjeev
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/[AWS_SECRET_ACCESS_KEY]
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Hello)
hello world
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
```

This output confirms that the **hello** stage executed successfully and printed "hello world" as expected.

## Build Interface Overview

After running your pipeline, you will encounter an interface that displays build details such as the start time, user who initiated the build, and duration metrics. Check out the build interface below:

<Frame>
  ![The image shows a Jenkins build interface for "HelloWorldPipeline" with details of Build #1, including the start time, user, and duration metrics. The sidebar contains options like Console Output, Pipeline Overview, and Pipeline Steps.](https://kodekloud.com/kk-media/image/upload/v1752879893/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Hello-World-Pipeline/jenkins-helloworldpipeline-build-interface.jpg)
</Frame>

<Callout icon="lightbulb">
  Now that you've successfully created and executed your first Jenkins pipeline, explore further by adding more stages or integrating additional tools to enhance your CI/CD workflow.
</Callout>

Enjoy building your pipelines and happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/5a2b722f-ec85-47f5-80d7-bb693179049c" />
</CardGroup>
