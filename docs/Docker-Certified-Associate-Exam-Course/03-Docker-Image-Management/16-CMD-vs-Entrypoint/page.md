# 1. Base image
FROM ubuntu:20.04

# 2. OS-level dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 3. Install Python packages
RUN pip3 install --no-cache-dir flask flask-mysql

# 4. Copy application source
WORKDIR /opt/source-code
COPY . .

# 5. Environment and ports
ENV FLASK_APP=app.py
EXPOSE 5000

# 6. Start the Flask server
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
```

| Instruction | Purpose                                     | Example                              |
| ----------- | ------------------------------------------- | ------------------------------------ |
| FROM        | Sets the base image                         | `FROM ubuntu:20.04`                  |
| RUN         | Executes commands in a new layer            | `RUN pip3 install flask flask-mysql` |
| WORKDIR     | Sets working directory inside the container | `WORKDIR /opt/source-code`           |
| COPY        | Copies files from host to container         | `COPY . .`                           |
| EXPOSE      | Documents the port the container listens on | `EXPOSE 5000`                        |
| ENTRYPOINT  | Defines the startup command                 | `ENTRYPOINT ["flask", "run", ...]`   |

## 3. Build, Tag, and Push Your Image

1. **Build** the image locally and add a tag:

   ```bash theme={null}
   docker build -t your-dockerhub-username/flask-app:latest .
   ```

2. **Push** to Docker Hub (replace with your repository):

   ```bash theme={null}
   docker push your-dockerhub-username/flask-app:latest
   ```

## 4. Inspecting Image Layers with `docker history`

Each Dockerfile instruction creates a new image layer. To view these layers and their sizes, run:

```bash theme={null}
docker history your-dockerhub-username/flask-app:latest
```

The output lists layers in reverse order, showing the command and size of each layer.

> **triangle-alert** If you frequently change application code but not OS dependencies, structure your Dockerfile so that `COPY . .` appears after installing system and Python packages. This maximizes cache reuse and speeds up rebuilds.

## 5. Leveraging Build Cache for Faster Iteration

Docker caches successful build steps. On subsequent builds:

* Steps unchanged since the last build use cached layers.
* Only modified steps (and those that follow) are re-executed.

Example:

```bash theme={null}
$ docker build -t flask-app:latest .
...
Step 2/6 : RUN apt-get update && apt-get install -y python3 python3-pip
 ---> Using cache
...
Step 5/6 : COPY . .
 ---> 123abc456def      # Rebuilds only this layer and ENTRYPOINT step
```

By isolating frequently changing instructions toward the end of your Dockerfile, you accelerate development cycles.

## Links and References

* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/4150a680-21ed-4f35-a373-febfc3ee398b)


# CMD vs Entrypoint

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/CMD-vs-Entrypoint/page

This guide explores Docker's CMD and ENTRYPOINT instructions for defining a container's default process and how to override them at runtime.

In this guide, we’ll explore how Docker uses the `CMD` and `ENTRYPOINT` instructions to define the default process of a container. You’ll learn how to override or extend these defaults at runtime and bake permanent changes into your images.

## Why Containers Exit Immediately

When you run a container without specifying a command, Docker launches the default process defined in the image’s Dockerfile. If that process ends, the container exits:

```bash theme={null}
docker run ubuntu
docker ps              # no running containers
docker ps -a           # shows the new container in exited state
```

Unlike virtual machines, containers are lightweight and designed to run a single task—such as a web server, database, or script. When that main process completes or fails, the container stops.

> **lightbulb** A container only runs as long as its main process is alive. Defining a long-running service or shell will keep it running.

## Examining Official Images

Popular Docker images set up their primary service using `CMD` or `ENTRYPOINT`. Let’s look at two examples:

### Nginx Dockerfile Excerpt

```dockerfile theme={null}
