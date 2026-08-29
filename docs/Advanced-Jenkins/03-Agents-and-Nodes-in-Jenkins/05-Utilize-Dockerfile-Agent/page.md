# Utilize Dockerfile Agent

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Utilize-Dockerfile-Agent/page

Explains using Jenkins dockerfile agent to build a custom Docker image that installs missing CLI tools such as cowsay so pipeline stages run correctly inside a container

In this lesson you'll learn how to build a custom Docker image from a Dockerfile and run a Jenkins pipeline stage inside a container created from that image using the `dockerfile` agent. This approach is useful when the base image from Docker Hub lacks command-line tools or libraries required by your pipeline steps.

Problem overview

* The example uses `node:18-alpine` as the agent image, which includes Node and npm but does not include the `cowsay` CLI.
* Running `cowsay` in that container fails because the binary is missing.

Reproducing the failure
Below is the initial declarative pipeline stage that attempts to use `node:18-alpine` as an agent and run `node`, `npm`, and `cowsay` inside the container:

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('S1-Any Agent') {
      steps { /* ... */ }
    }

    stage('S2-Ubuntu Agent') {
      steps { /* ... */ }
    }

    stage('S3-Docker Image Agent') {
      steps { /* ... */ }
    }

    stage('S4-Dockerfile Agent') {
      agent {
        docker {
          image 'node:18-alpine'
          label 'ubuntu-docker-jdk17-node20'
        }
      }
      steps {
        sh 'node -v'
        sh 'npm -v'
        sh 'cowsay -f dragon This is running on Docker Container'
      }
    }
  }
}
```

Example console output (excerpt):

```text theme={null}
+ node -v
v18.20.4

+ npm -v
10.7.0

+ cowsay -f dragon This is running on Docker Container
/home/jenkins-agent/workspace/pipeline-external-agent@tmp/durable-7cf90c4e/script.sh.copy: line 1: cowsay: not found
```

Cause

* The `node:18-alpine` image includes Node.js and npm but not the `cowsay` package, so invoking `cowsay` fails.
* To fix this, create a custom image that extends `node:18-alpine` and installs the missing CLI(s).

Create a custom Dockerfile
Create a file (for example `Dockerfile.cowsay`) in your repository workspace with the following contents. Because the base image uses Alpine Linux, use `apk` to install required packages, then clone and install `cowsay` from its GitHub repo:

```dockerfile theme={null}
FROM node:18-alpine

RUN apk update && \
    apk add --no-cache git perl && \
    cd /tmp && \
    git clone https://github.com/jasonm23/cowsay.git && \
    cd cowsay && \
    ./install.sh /usr/local
```

Switch the pipeline to the `dockerfile` agent
Update the pipeline stage to use the `dockerfile` agent so Jenkins will build the image from the Dockerfile in the workspace and run the stage inside a container created from that image.

> **lightbulb** Note: This is `dockerfile` (not `docker`). The `dockerfile` agent builds the image from the specified Dockerfile in the workspace, then runs your steps inside a container created from that image.

Corrected pipeline stage (using `Dockerfile.cowsay`):

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('S1-Any Agent') {
      steps { /* ... */ }
    }

    stage('S2-Ubuntu Agent') {
      steps { /* ... */ }
    }

    stage('S3-Docker Image Agent') {
      steps { /* ... */ }
    }

    stage('S4-Dockerfile Agent') {
      agent {
        dockerfile {
          filename 'Dockerfile.cowsay'
          label 'ubuntu-docker-jdk17-node20'
        }
      }
      steps {
        sh 'node -v'
        sh 'npm -v'
        sh 'cowsay -f dragon This is running on Docker Container'
      }
    }
  }
}
```

What Jenkins will do when this runs

* Read `Dockerfile.cowsay` from the workspace.
* Build a Docker image (you'll see a `docker build -t ... -f Dockerfile.cowsay .` invocation in the logs).
* Start a container from the built image and run your `sh` steps inside it.

Build log excerpt showing the image build and install step:

```text theme={null}
+ docker build -t `unique-image-id` -f Dockerfile.cowsay .
#1 [internal] load build definition from Dockerfile.cowsay
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/node:18-alpine
#2 DONE 0.0s

#4 [1/2] FROM docker.io/library/node:18-alpine
#4 DONE 0.1s

#5 [2/2] RUN apk update &&      apk add --no-cache git perl &&      cd /tmp &&      git clone https://github.com/jasonm23/cowsay.git &&      cd cowsay && ./install.sh /usr/local
#5 1.045 OK: 24168 distinct packages available
#5 4.487 Installation complete! Enjoy the cows!
#5 DONE 4.6s

#6 exporting to image
#6 DONE 0.4s

+ docker inspect -f . `unique-image-id`
.
+ node -v
v18.20.4
```

After successful build and run, `cowsay` executes as expected. Example final output:

```text theme={null}
+ cowsay -f dragon This is running on Docker Container

< This is running on Docker Container >
------------------------------
```

Quick reference table

| Item                          | Purpose                                        | Example / Note                                                                |
| ----------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------- |
| Dockerfile filename           | Path to the Dockerfile in workspace            | `Dockerfile.cowsay`                                                           |
| Jenkins agent block           | Use dockerfile to build image from repository  | `agent { dockerfile { filename 'Dockerfile.cowsay' } }`                       |
| Installing packages in Alpine | Use `apk` to add required packages             | `apk add --no-cache git perl`                                                 |
| Installing third‑party CLI    | Clone and run install script inside Dockerfile | `git clone https://github.com/jasonm23/cowsay.git && ./install.sh /usr/local` |

Troubleshooting and important notes

> **warning** Warning: The Jenkins node that builds the Docker image must have Docker (or a compatible container runtime) available and properly configured for the Jenkins user. If Docker is not accessible from the agent, the `docker build` step will fail. Ensure the agent has permission to run Docker (or use a dedicated Docker-in-Docker or privileged agent).

* If builds are slow, consider pushing a pre-built image to a registry and using `agent { docker { image 'your-registry/your-image:tag' } }` in production.
* For complex images, include a small changelog or versioning tag in the Dockerfile to help with caching and reproducible builds.
* Monitor Jenkins logs to confirm the `docker build` and container start steps.

Summary

* Use a Dockerfile when the base image lacks required CLI tools or libraries.
* Add the Dockerfile to your repository workspace (e.g., `Dockerfile.cowsay`).
* Configure the declarative pipeline with `agent { dockerfile { filename 'Dockerfile.cowsay' } }`.
* Verify Jenkins build logs show `docker build` and that `cowsay` (or other tools) run successfully inside the container.

Links and references

* [Jenkins Pipeline: Docker](https://www.jenkins.io/doc/book/pipeline/docker/)
* [Cowsay GitHub repository](https://github.com/jasonm23/cowsay)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/10aeb450-17d4-4a8f-8ee5-481ad7662ee7)
