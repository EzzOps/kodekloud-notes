# Build Docker Image

Source: https://notes.kodekloud.com/docs/Jenkins-Pipelines/Containerization-and-Deployment/Build-Docker-Image/page

This article demonstrates building a Docker image within a Jenkins pipeline using the Docker CLI and environment variables.

In this lesson, we demonstrate how to build a Docker image within a Jenkins pipeline. After the [SonarQube](https://www.sonarqube.org/) stage, the pipeline includes a stage to build the Docker image using the Docker CLI. The image is tagged with your [Docker Hub](https://hub.docker.com) username (siddharth67), the image name (solar-system), and the Git commit hash obtained from the environment variable GIT\_COMMIT.

> **lightbulb** Ensure that your pipeline has executed a checkout stage before this build step so that the necessary environment variables, including the Git commit hash, are available.

## Jenkinsfile Stage for Building the Docker Image

Below is the Groovy snippet for the Docker image build stage. It uses the `docker build` command to tag the image with the specified username, image name, and Git commit:

```groovy theme={null}
stage('Build Docker Image') {
    steps {
        sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
    }
}
```

The complete pipeline structure, with the new stage added, is shown below:

```groovy theme={null}
stages {
    stage('Installing Dependencies') {
        // Steps to install dependencies
    }
    stage('Dependency Scanning') {
        // Steps for dependency scanning
    }
    stage('Unit Testing') {
        // Steps for running unit tests
    }
    stage('Code Coverage') {
        // Steps for code coverage analysis
    }
    stage('SAST - SonarQube') {
        // Steps for static analysis with SonarQube
    }
    stage('Build Docker Image') {
        steps {
            sh 'printenv'
            sh 'docker build -t siddharth67/solar-system:$GIT_COMMIT .'
        }
    }
}

post {
    always {
        // Post-build actions
    }
}
```

In this updated pipeline, the `printenv` command is invoked to display all environment variables available in the pipeline. These variables include custom ones defined in the Jenkinsfile and built-in variables such as the Git commit hash, build ID, job URL, branch name, among others. This output is useful for debugging and ensuring that the correct values are being used.

## Dockerfile for Building the Image

Next, review the Dockerfile that is used to build the Docker image. This file performs the following actions:

* Uses a Node 18 Alpine base image.
* Sets the working directory to `/usr/app`.
* Copies package files and installs dependencies.
* Copies the remaining source code.
* Sets placeholder environment variables for MongoDB.
* Exposes port 3000.
* Starts the application using `npm start`.

```dockerfile theme={null}
FROM node:18-alpine3.17
WORKDIR /usr/app
COPY package*.json /usr/app/
RUN npm install
COPY . .
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder
EXPOSE 3000
CMD [ "npm", "start" ]
```

> **lightbulb** Use a `.dockerignore` file to exclude unnecessary files and directories from the Docker build context, improving build performance.

## The .dockerignore File

The `.dockerignore` file functions similarly to a `.gitignore` file and prevents certain files from being copied to the Docker image during the build. Below is an example of its contents:

```dockerignore theme={null}
npm-debug.log
.git
.cache
