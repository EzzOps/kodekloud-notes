# building with "default" instance using docker driver
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 2768 done
#1 DONE 0.0s
#2 [internal] load metadata for docker.io/library/python:3.12.0b3-alpine3.18
#2 DONE 0.1s
#3 [1/5] FROM docker.io/library/python:3.12.0b3-alpine3.18@sha256:[SECRET_REDACTED]
#3 CACHED
#4 [internal] load .dockerignore
#4 transferring context: 1398 done
#4 DONE 0.0s
#5 [internal] load build context
#5 transferring context: 175.92kB 0.0s done
#5 DONE 0.0s
#6 [2/5] COPY ./application
#6 DONE 0.0s
#7 [3/5] WORKDIR /application
#7 DONE 0.1s
#8 [4/5] COPY requirements.txt .
#8 DONE 0.0s
```

Once the image is built, the pipeline pushes it to Docker Hub. You can also push the image manually with a command like:

```bash theme={null}
docker push sanjeevkt720/jenkins-flask-app:e787c436a79bb92e1c822545f59d0dc2f130
```

A typical push output might include:

```bash theme={null}
The push refers to repository [docker.io/sanjeevkt720/jenkins-flask-app]
d182718f0571: Preparing
b257846d686b: Preparing
feb5cabfe56d: Preparing
b831d4be96e5: Preparing
8a328213b96e: Preparing
cd18a2bc1cce: Preparing
78a82283f2c8: Waiting
cb72ec1da28c: Waiting
78a82283f2c8: Layer already exists
```

## Verifying the Commit and Docker Image Tag

Tagging your Docker images with the Git commit hash creates a direct link between the image and a specific commit in your repository. This makes it easy to track deployments back to the source code changes. For example, checking the commit history on GitHub can help you verify that the correct changes have been deployed.

<Frame>
  ![The image shows a GitHub repository page displaying a list of commits for a project named "course-jenkins-project" under the user "kodekloudhub." Each commit entry includes a message, author, and timestamp.](https://kodekloud.com/kk-media/image/upload/v1752879865/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Jenkins-Pipeline-with-Docker/github-repo-commits-course-jenkins.jpg)
</Frame>

If you view a commit diff, you might see something like this:

<Frame>
  ![The image shows a GitHub commit page for a project, displaying changes in files with additions and deletions highlighted in a diff view.](https://kodekloud.com/kk-media/image/upload/v1752879866/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Jenkins-Pipeline-with-Docker/github-commit-diff-view.jpg)
</Frame>

After making changes (for example, updating the version to "version four"), commit and push the modifications. Jenkins will trigger another build, and your updated Docker image—now tagged with the new commit hash—will be pushed to Docker Hub.

## Viewing the Docker Image on Docker Hub

Finally, you can verify the pushed Docker image on Docker Hub. The Docker Hub interface displays details such as the manifest digest, OS/architecture, compressed size, and image layers.

<Frame>
  ![The image shows a Docker Hub page displaying details of a Docker image, including its manifest digest, OS/architecture, compressed size, and image layers.](https://kodekloud.com/kk-media/image/upload/v1752879867/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Demo-Configuring-Jenkins-Pipeline-with-Docker/docker-hub-image-details-manifest.jpg)
</Frame>

This completes the process of integrating Docker into your Jenkins CI/CD pipeline, enabling streamlined testing, building, and deployment of your applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/9eb65ce1-0aef-4f00-b661-5f8308aef2bd/lesson/71491108-5621-40e1-9b47-b091bc18bb35" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/9eb65ce1-0aef-4f00-b661-5f8308aef2bd/lesson/86910176-a0dd-4cc7-897a-7a1390f4748c" />
</CardGroup>


# Docker Overview

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Docker/Docker-Overview/page

This article introduces Docker containers, their benefits, and integration into CI/CD pipelines with Jenkins.

In this lesson, we delve into Docker containers, exploring their core concepts and how they can be integrated into a CI/CD pipeline with [Jenkins](https://learn.kodekloud.com/user/courses/jenkins). We will start by discussing what Docker is and its benefits, then demonstrate its practical applications, and finally detail the steps to configure a CI/CD pipeline using Jenkins.

## What is Docker?

Docker is a platform that packages every component your application requires into a single, portable container. Think of a Docker container like a shipping container: just as shipping containers transport a variety of goods without repacking at each stop, Docker containers bundle your application’s source code, libraries, dependencies, and runtime environment. This ensures that your application runs reliably regardless of the deployment environment.

<Frame>
  ![The image compares a ship container and a Docker container, illustrating the concept of containers in computing with symbolic representations.](https://kodekloud.com/kk-media/image/upload/v1752879869/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Docker-Overview/ship-container-vs-docker-container.jpg)
</Frame>

The isolated nature of Docker containers ensures that everything an application needs is encapsulated, allowing it to run immediately upon deployment—eliminating the need for additional configuration.

<Frame>
  ![The image illustrates a concept of Docker Containers, featuring a central cube labeled "Docker Container" with four surrounding icons representing different aspects of containerization.](https://kodekloud.com/kk-media/image/upload/v1752879870/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Docker-Overview/docker-containers-concept-diagram.jpg)
</Frame>

## How Docker Works

Using the shipping container analogy further: once your goods are securely packaged into a container, they are loaded onto a ship. In the Docker ecosystem, the role of the ship is played by the Docker engine. The Docker engine is vital for:

* Deploying containers
* Starting and monitoring container health
* Managing container lifecycles by restarting them as required

<Frame>
  ![The image shows an illustration of a cargo ship carrying containers on the ocean, with the text "Moving Docker Containers" above it.](https://kodekloud.com/kk-media/image/upload/v1752879872/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Docker-Overview/cargo-ship-moving-docker-containers.jpg)
</Frame>

The Docker engine also ensures that containers run in isolation from one another, efficiently managing resources and overseeing lifecycle operations.

<Frame>
  ![The image shows a stylized Docker whale with containers on its back, floating on waves, alongside icons representing code and settings, with the text "Moving Docker Containers."](https://kodekloud.com/kk-media/image/upload/v1752879872/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Docker-Overview/docker-whale-containers-waves.jpg)
</Frame>

## Advantages of Docker

Docker provides several powerful advantages that make it ideal for modern application development and deployment:

* **Standardization:** Much like shipping containers, Docker containers offer a standardized environment. This means that an application packaged as a Docker container will run consistently across any machine with Docker installed, independent of the underlying operating system or hardware.

* **Isolation:** Each container operates independently, ensuring that the dependencies and runtime setup of one application do not interfere with another. This isolation is key to running multiple applications on the same host without conflicts.

* **Efficiency:** Docker containers are highly efficient and lightweight compared to traditional virtual machines. They start quickly and use system resources more effectively, enabling you to run more containers on a single host.

* **Portability:** Docker containers can be easily pushed to container registries and deployed on any Docker-compatible system, enabling seamless transfers across environments.

* **Scalability:** Docker simplifies the scaling process. When additional capacity is needed, additional container instances can be quickly deployed to handle increased demand.

<Frame>
  ![The image lists five advantages: Standardization, Isolation, Efficiency, Portability, and Scaling, each represented with an icon.](https://kodekloud.com/kk-media/image/upload/v1752879873/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Docker-Overview/advantages-standardization-isolation-efficiency-portability-scaling.jpg)
</Frame>

<Callout icon="lightbulb">
  Docker's portability ensures that your development and production environments are identical, reducing the notorious "it works on my machine" dilemma.
</Callout>

## Conclusion

This article provided an introduction to Docker containers, highlighting their benefits in terms of standardization, isolation, efficiency, portability, and scalability. By encapsulating applications in isolated containers, Docker simplifies deployment and scaling significantly. In the upcoming sections, we will explore how to harness Docker alongside [Jenkins](https://learn.kodekloud.com/user/courses/jenkins) to build robust CI/CD pipelines for scalable web applications.

Transcribed by [https://otter.ai](https://otter.ai)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/9eb65ce1-0aef-4f00-b661-5f8308aef2bd/lesson/8d8da417-2f5a-4926-bf69-0ded2772dd38" />
</CardGroup>
