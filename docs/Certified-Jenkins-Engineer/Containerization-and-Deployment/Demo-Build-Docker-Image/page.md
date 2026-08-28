# Demo Build Docker Image

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Demo-Build-Docker-Image/page

This guide explains how to build a Docker image in a Jenkins CI/CD pipeline, tagging it with the Git commit SHA for traceability.

In this guide, we’ll walk through building a Docker image in a Jenkins **CI/CD pipeline**, tagging each build with the Git commit SHA for traceability.

## Add the Build Docker Image Stage

Open your `Jenkinsfile` and, right after the SonarQube stage, insert a new stage named **Build Docker Image**. This stage prints all environment variables and then builds the Docker image using the current Git commit hash (`GIT_COMMIT`) as the tag.

```groovy theme={null}
stage('Build Docker Image') {
    steps {
        // Print all available environment variables
        sh 'printenv'
        
        // Build and tag the Docker image
        sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
    }
}
```

<Callout icon="lightbulb">
  `GIT_COMMIT` is a built-in Jenkins variable provided when you use the `checkout` step. It resolves to the current commit SHA, ensuring each Docker image is uniquely tagged.
</Callout>

## Jenkinsfile Reference

For more information on pipeline syntax and environment variables, see the [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/) documentation.

***

## Dockerfile Breakdown

Your repository includes this `Dockerfile`, which defines how to build the Node.js application image.

```Dockerfile theme={null}
FROM node:18-alpine3.17

WORKDIR /usr/app

COPY package*.json /usr/app/
RUN npm install

COPY . .
