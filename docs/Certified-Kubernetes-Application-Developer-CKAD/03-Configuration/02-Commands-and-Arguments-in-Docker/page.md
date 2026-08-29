# Commands and Arguments in Docker

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Commands-and-Arguments-in-Docker/page

This article explores Docker commands and arguments, focusing on container behavior, Dockerfile instructions, and the differences between CMD and ENTRYPOINT.

Welcome to this detailed lesson on Docker commands and arguments. My name is Mumshad Mannambeth, and in this article we will explore how commands work in containers and Docker. Although this topic may not be explicitly featured in certification curriculums, understanding it is crucial since it is often overlooked. We will begin by reviewing container commands with Docker and then translate these concepts to Pods in Kubernetes.

## Running a Container with an Ubuntu Image

Imagine running a Docker container using an Ubuntu image. Executing the commands below creates a container instance that immediately exits:

```bash theme={null}
docker run ubuntu
docker ps
docker ps -a
```

The container does not appear in the list of running containers because, unlike virtual machines, containers are designed for specific tasks (such as hosting a web server, application server, or performing computations) and terminate once these tasks complete. Essentially, a container’s life cycle is tied to its main process. For instance, if the web service inside the container stops or crashes, the container will exit.

> **lightbulb** Containers are ideal for running single processes because they are lightweight and are not intended to persist beyond the execution of their primary task.

## Understanding the CMD Instruction in Dockerfiles

The behavior of a container is defined by its Dockerfile. Many popular Docker images, such as nginx or MySQL, use the CMD instruction to specify the default command that runs when the container starts. For example, the nginx image is configured to launch the nginx process, whereas the MySQL image starts the MySQL server process.

Consider the following Dockerfile excerpt that installs and configures nginx as well as MySQL:

```dockerfile theme={null}
