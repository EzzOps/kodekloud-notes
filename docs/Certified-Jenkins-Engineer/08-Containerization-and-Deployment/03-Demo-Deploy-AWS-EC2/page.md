# Placeholder environment variables for MongoDB credentials
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000
CMD [ "npm", "start" ]
```

Key steps:

1. **FROM**: Start from the lightweight `node:18-alpine3.17` base image.
2. **WORKDIR**: Set `/usr/app` as the working directory.
3. **COPY package\*.json**: Copy dependency manifests and install packages.
4. **COPY . .**: Add application source code.
5. **ENV**: Define placeholders for MongoDB connection.
6. **EXPOSE**: Open port 3000.
7. **CMD**: Launch the app with `npm start`.

For complete details, refer to the [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).

***

## .dockerignore

Optimize build context by excluding unnecessary files. Place this **.dockerignore** in the project root:

```text theme={null}
# Source control and metadata
.git
.github/

# Node.js dependencies
node_modules

# Configuration and reports
.*  
!.README*.md
README-secret.md
solar-system.png
.nyc_output
.talismanrc
coverage
test-results.xml
reports*
zap*
dependency*
jenkins*
trivy-image*
```

> **triangle-alert** Be cautious when excluding files. Make sure you don’t accidentally omit critical configuration, scripts, or assets required at runtime.

See the [Dockerignore reference](https://docs.docker.com/engine/reference/builder/#dockerignore-file) for patterns and best practices.

***

## Jenkins Pipeline Environment Variables

Jenkins exposes numerous environment variables in multibranch pipelines. Visit **Pipeline Syntax** → **Global variables reference** to explore them all.

| Variable      | Description                                      |
| ------------- | ------------------------------------------------ |
| GIT\_COMMIT   | Current commit SHA (requires `checkout`)         |
| BRANCH\_NAME  | Active branch in a multibranch pipeline          |
| CHANGE\_ID    | Pull request or change request identifier        |
| BUILD\_NUMBER | Sequential build number                          |
| BUILD\_ID     | Unique build identifier                          |
| WORKSPACE     | Path to the workspace on the agent               |
| NODE\_NAME    | Name of the Jenkins agent node running the build |

![The image shows a Jenkins Pipeline Syntax page detailing environment variables available for multibranch projects, such as BRANCH\_NAME, CHANGE\_ID, and CHANGE\_AUTHOR.](https://kodekloud.com/kk-media/image/upload/v1752870501/notes-assets/images/Certified-Jenkins-Engineer-Demo-Build-Docker-Image/jenkins-pipeline-syntax-environment-variables.jpg)

***

## Pipeline Execution

After committing and pushing the updated `Jenkinsfile`, Jenkins triggers a new run. Once earlier stages finish, the **Build Docker Image** stage will begin:

```shell theme={null}
docker build -t siddharth67/solar-system:$GIT_COMMIT .
```

### Print Environment Variables

This step logs all environment variables visible to the build stage:

```shell theme={null}
+ printenv
JENKINS_HOME=/var/lib/jenkins
GIT_PREVIOUS_SUCCESSFUL_COMMIT=10f241dbfe4218e2d9acd44b9950c4144
MONGO_DB_CREDS_PSW=****
USER=jenkins
CI=true
…  
GIT_COMMIT=0bb4c412562f4f1db4c2149f834e29f3
BUILD_URL=http://jenkins.example.com/job/.../28/
WORKSPACE=/var/lib/jenkins/workspace/solar-system_feature_enabling-cicd
STAGE_NAME=Build Docker Image
GIT_BRANCH=feature/enabling-cicd
BUILD_TAG=jenkins-Gitea-Organization-solar-system-feature%252Fenabling-cicd-28
```

### Docker Build Logs

Jenkins streams the Docker build output, showing layer creation and tagging:

```shell theme={null}
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 2828B done
…
#9 naming to docker.io/siddharth67/solar-system:9dbc4b421562f410b4dec2141938fd2a5ac0ad1 done
#9 DONE 0.0s
```

Verify the image tag in your registry or local Docker daemon to ensure it matches the commit SHA.

![The image shows a code repository interface with a list of files and recent commits, including a branch named "feature/enabling-cicd."](https://kodekloud.com/kk-media/image/upload/v1752870502/notes-assets/images/Certified-Jenkins-Engineer-Demo-Build-Docker-Image/code-repository-files-commits.jpg)

***

## Next Steps

You’ve successfully built and tagged a Docker image via Jenkins. In the next tutorial, we’ll scan this image for vulnerabilities and push it to Docker Hub.

***

## Links and References

* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Dockerignore file](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
* [Jenkins Environment Variables](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/62a5104f-415a-4733-bb3d-38db220267fb)


# Demo Deploy AWS EC2

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Containerization-and-Deployment/Demo-Deploy-AWS-EC2/page

Learn to deploy a Dockerized Node.js application on AWS EC2 using a Jenkins Pipeline, covering all necessary steps and configurations.

In this guide, you’ll learn how to deploy a Dockerized Node.js application to an AWS EC2 instance using a Jenkins Pipeline. We’ll cover every step—from adding a deploy stage and managing Docker containers on EC2, to conditional execution and verifying your deployment.

**Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Adding the Deploy Stage](#1-adding-the-deploy-stage)
3. [Stopping & Removing the Existing Container](#2-stopping--removing-the-existing-container)
4. [Running the New Container](#3-running-the-new-container)
5. [Wrapping in a `script` Block](#4-wrapping-in-a-script-block)
6. [Conditional Execution with `when`](#5-conditional-execution-with-when)
7. [Verifying the Deployment](#6-verifying-the-deployment)
8. [Links and References](#links-and-references)

***

## Prerequisites

* A Jenkins instance with the **SSH Agent** plugin installed
* An AWS EC2 Ubuntu server accessible via SSH
* A Dockerized application pushed to a Docker registry
* Jenkins credentials configured for:
  * SSH key (e.g., `aws-dev-deploy-ec2-instance`)
  * MongoDB username & password (`mongo-db-username`, `mongo-db-password`)

***

## 1. Adding the Deploy Stage

After your `Push Docker Image` stage, insert a new stage called **Deploy - AWS EC2**. Here’s the skeleton of your declarative pipeline:

```groovy theme={null}
pipeline {
    agent any

    stages {
        stage('Build Docker Image') { /* ... */ }
        stage('Trivy Vulnerability Scanner') { /* ... */ }
        stage('Push Docker Image') { /* ... */ }
        stage('Deploy - AWS EC2') {
            steps { /* To be implemented */ }
        }
    }

    post {
        always { /* ... */ }
    }
}
```

| Stage Name                  | Description                            |
| --------------------------- | -------------------------------------- |
| Build Docker Image          | Build and tag your Docker image        |
| Trivy Vulnerability Scanner | Scan the image for vulnerabilities     |
| Push Docker Image           | Push the image to your Docker registry |
| Deploy - AWS EC2            | SSH into EC2 and restart the container |

We’ll use the [SSH Agent plugin](https://plugins.jenkins.io/ssh-agent) to authenticate to EC2 using the private key credential `aws-dev-deploy-ec2-instance`.

***

## 2. Stopping & Removing the Existing Container

Use an SSH one-liner to detect if the `solar-system` container is running, then stop and remove it:

```bash theme={null}
ssh -o StrictHostKeyChecking=no ubuntu@3.140.244.188 "
if sudo docker ps -a | grep -q 'solar-system'; then
    echo 'Container found. Stopping...'
    sudo docker stop solar-system && sudo docker rm solar-system
    echo 'Container stopped and removed.'
fi
"
```

> **lightbulb** Suppressing `StrictHostKeyChecking` avoids interactive host key prompts, which is essential for unattended CI/CD pipelines.

***

## 3. Running the New Container

Next, start a fresh container with your environment variables. These variables come from the global `environment` block in your Jenkinsfile:

```bash theme={null}
ssh -o StrictHostKeyChecking=no ubuntu@3.140.244.188 "
sudo docker run --name solar-system \
  -e MONGO_URI=$MONGO_URI \
  -e MONGO_USERNAME=$MONGO_USERNAME \
  -e MONGO_PASSWORD=$MONGO_PASSWORD \
  -p 3000:3000 \
  -d siddharth67/solar-system:$GIT_COMMIT
"
```

Define your environment variables at the top of the Jenkinsfile:

```groovy theme={null}
pipeline {
    agent any

    environment {
        MONGO_URI         = 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
        MONGO_USERNAME    = credentials('mongo-db-username')
        MONGO_PASSWORD    = credentials('mongo-db-password')
        SONAR_SCANNER_HOME = tool 'sonarqube-scanner-610'
    }

    stages { /* ... */ }
}
```

| Variable        | Source                                 |
| --------------- | -------------------------------------- |
| MONGO\_URI      | Hard-coded connection string           |
| MONGO\_USERNAME | Jenkins credential `mongo-db-username` |
| MONGO\_PASSWORD | Jenkins credential `mongo-db-password` |
| GIT\_COMMIT     | Jenkins built-in variable              |

***

## 4. Wrapping in a `script` Block

Because we’re using conditional logic (`if`), wrap the SSH commands in a `script` step inside the declarative stage:

```groovy theme={null}
stage('Deploy - AWS EC2') {
    steps {
        script {
            sshagent(['aws-dev-deploy-ec2-instance']) {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@3.140.244.188 "
                if sudo docker ps -a | grep -q 'solar-system'; then
                    echo 'Container found. Stopping...'
                    sudo docker stop solar-system && sudo docker rm solar-system
                    echo 'Container stopped and removed.'
                fi

                sudo docker run --name solar-system \
                  -e MONGO_URI=$MONGO_URI \
                  -e MONGO_USERNAME=$MONGO_USERNAME \
                  -e MONGO_PASSWORD=$MONGO_PASSWORD \
                  -p 3000:3000 -d siddharth67/solar-system:$GIT_COMMIT
                "
                '''
            }
        }
    }
    post {
        always { /* cleanup or notifications */ }
    }
}
```

***

## 5. Conditional Execution with `when`

Run the deploy stage only on feature branches by adding a `when` condition. You can also configure this filter in the Jenkins UI:

```groovy theme={null}
stage('Deploy - AWS EC2') {
    when {
        branch 'feature/*'
    }
    steps {
        script {
            sshagent(['aws-dev-deploy-ec2-instance']) {
                sh '''<same SSH block as above>'''
            }
        }
    }
}
```

> **lightbulb** Using `when { branch 'feature/*' }` ensures that deployment only triggers for feature branches, preventing accidental prod deployments.

***

## 6. Verifying the Deployment

1. **Check Jenkins Console**
   ```bash theme={null}
   ssh -o StrictHostKeyChecking=no ubuntu@3.140.244.188 "
   if sudo docker ps -a | grep -q 'solar-system'; then
       echo 'Container found. Stopping...'
       sudo docker stop solar-system && sudo docker rm solar-system
   fi
   "
   ```
   **Sample logs:**
   ```plaintext theme={null}
   Warning: Permanently added '3.140.244.188' (ECDSA) to the list of known hosts.
   Container found. Stopping...
   Container stopped and removed.
   Unable to find image 'siddharth67/solar-system:5376ef9094c...' locally
   Status: Downloaded newer image for siddharth67/solar-system:5376ef9094c...
   cab883d639d9
   ```

2. **On the EC2 Instance**
   ```bash theme={null}
   sudo docker ps
   ```
   **Expected output:**
   ```plaintext theme={null}
   CONTAINER ID   IMAGE                                        NAMES
   cab88363d990   siddharth67/solar-system:5376ef09...         solar-system

   COMMAND             CREATED          STATUS             PORTS
   "docker-entrypoint.s..." About a minute ago Up About a minute 0.0.0.0:3000->3000/tcp
   ```

3. **Access the Application**\
   Open a browser and navigate to:
   ```text theme={null}
   http://<EC2_PUBLIC_IP>:3000
   ```

Integration testing should follow to validate your application endpoints and data flow.

***

## Links and References

* [AWS EC2 Documentation](https://aws.amazon.com/ec2/)
* [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)
* [SSH Agent Plugin](https://plugins.jenkins.io/ssh-agent)
* [Docker Documentation](https://docs.docker.com/)

Happy Deploying!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/e16e4b93-31c4-479b-96b8-f0d26cde31cd/lesson/bbebaeeb-ba14-42f1-ab36-e2d692e3123a)
