# Build a Jenkins file

Source: https://notes.kodekloud.com/docs/Jenkins/Pipelines/Build-a-Jenkins-file/page

This article teaches the structure and functionality of Jenkinsfiles through examples, from basic to complex multi-stage pipelines.

In this lesson, we dive into Jenkinsfiles to learn their structure and functionality, using several examples along the way. We begin by creating a basic Jenkinsfile in Visual Studio Code (VS Code) and then progress to more complex, multi-stage pipelines.

***

## Creating a Basic Jenkinsfile

To get started, create a new file in VS Code named "Jenkinsfile". VS Code automatically recognizes this file extension, enabling syntax highlighting and other helpful features.

Let's start with a simple "Hello World" pipeline:

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

In this example:

* The `agent any` directive allows Jenkins to run the pipeline on any available build agent or on the Jenkins server.
* The `stages` block contains a single stage labeled "Hello".
* Under the `steps` section, the command `echo 'Hello World'` prints the message to the console.

You can also rename the stage to better align with your project context. For instance, changing "Hello" to "Dev" is equally effective:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Dev') {
            steps {
                echo 'Hello World'
            }
        }
    }
}
```

***

## Introducing a Pipeline that Pulls Code from GitHub

Next, we examine a Jenkinsfile that interacts with GitHub. In this example, the pipeline checks out code from a GitHub repository during the build stage:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Get some code from a GitHub repository
                git 'https://github.com/AdminTurnedDevOps/go-webapp-sample.git'
            }
        }
    }
}
```

In this pipeline:

* The `agent any` directive indicates that any available build agent can be used.
* A single stage, "Build", is defined.
* Within the "Build" stage, the `git` step retrieves the code from the specified GitHub repository, making it available for further processes such as testing or deployment.

***

## Constructing a Multi-Stage Pipeline

Multi-stage pipelines enable you to separate your build, test, and deployment processes into distinct stages within a single Jenkinsfile. Below is an example demonstrating two stages, "Dev" and "UAT", that both pull code from GitHub:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Dev') {
            steps {
                // Get some code from a GitHub repository
                git 'https://github.com/AdminTurnedDevOps/go-webapp-sample.git'
            }
        }
        stage('UAT') {
            steps {
                // Get some code from a GitHub repository
                git 'https://github.com/AdminTurnedDevOps/go-webapp-sample.git'
            }
        }
    }
}
```

In this multi-stage pipeline:

* The `stages` block is divided into two stages: "Dev" and "UAT".
* Both stages use the `git` step to pull code from the GitHub repository.
* This structure allows you to extend each stage with additional tasks such as running tests, performing quality checks, or deploying to different environments.

> **lightbulb** This basic multi-stage design can be easily extended to fit more complex deployment workflows, ensuring that each environment receives the necessary configuration and testing procedures.

***

Now that we've covered the basics of creating and structuring Jenkinsfiles—from a single-stage "Hello World" pipeline to a more advanced multi-stage pipeline—it's time to put this knowledge into practice. Head over to the Jenkins portal to start building and experimenting with your own code pipelines.

That’s it for this lesson. We'll see you in the next one!

- [Watch Video](https://learn.kodekloud.com/user/courses/jenkins/module/4eff829b-dd2c-4051-8090-35e8525b8874/lesson/2a3d25b1-320f-460d-ad4f-65625e3d05d3)
